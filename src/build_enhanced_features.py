"""Features aumentadas: RAVLT reconocimiento (d'/criterio C/fp_listaB), ADLQ funcional,
gap normativo (z esperado por edad/educación), y target memoria-específico.
Parte de model_dataset.csv y escribe model_dataset_plus.csv."""
import duckdb, pandas as pd, numpy as np, re, unicodedata
from sklearn.ensemble import HistGradientBoostingRegressor
CORE=['atencion','funciones_ejecutivas','memoria','lenguaje','visuoespacial']

df = pd.read_csv('data/interim/model_dataset.csv')
con = duckdb.connect('db/evaluaciones_v2.duckdb', read_only=True)
rec = con.execute("SELECT path, dprime, criterio_c, fp_listaB, confab, hits FROM ravlt_reconocimiento").df()
de  = con.execute("SELECT eval_id, dominio, z_peor FROM dominio_eval").df()
ev  = con.execute("SELECT eval_id, persona_id, path, fecha_ev, edad, educacion FROM evaluaciones_v2 WHERE cohorte<>'wisc_v'").df()
adlq= con.execute("SELECT pac_key, adlq_pct FROM adlq_pct").df()
cq  = con.execute("SELECT pac_key, pac_apellido, pac_nombre FROM cuestionario_paciente").df()
cl  = con.execute("SELECT ape, nom, persona_id FROM cuest_link").df()
con.close()

# ---- 1) RAVLT reconocimiento (por path del basal) ----
rec = rec.drop_duplicates('path')
df = df.merge(rec, on='path', how='left')
print("RAVLT recon presente (d'):", f"{100*df.dprime.notna().mean():.0f}%")

# ---- 2) ADLQ funcional (pac_key -> nombre -> persona) ----
def _n(s):
    s=''.join(c for c in unicodedata.normalize('NFD',str(s)) if unicodedata.category(c)!='Mn')
    return re.sub(r'[^a-z]','',s.lower())
cl['k']=cl.ape.map(_n)+'|'+cl.nom.map(_n)
cq['k']=cq.pac_apellido.map(_n)+'|'+cq.pac_nombre.map(_n)
key2pers = cq.merge(cl[['k','persona_id']].drop_duplicates('k'), on='k', how='left')[['pac_key','persona_id']].dropna()
adlqp = adlq.merge(key2pers, on='pac_key', how='left').dropna(subset=['persona_id']).drop_duplicates('persona_id')
df = df.merge(adlqp[['persona_id','adlq_pct']], on='persona_id', how='left')
print("ADLQ funcional presente:", f"{100*df.adlq_pct.notna().mean():.0f}%")

# ---- 3) Gap normativo: z_esperado(edad,educacion) sobre TODA la cohorte adulta ----
ev['fecha']=pd.to_datetime(ev.fecha_ev, errors='coerce')
zp = de[de.dominio.isin(CORE)].assign(z=lambda x:x.z_peor.clip(-6,4)).pivot_table(
        index='eval_id', columns='dominio', values='z', aggfunc='first')
zp['gz']=zp[CORE].mean(axis=1)
full = ev.merge(zp, left_on='eval_id', right_index=True, how='inner').dropna(subset=['edad','educacion'])
# modelo normativo no-lineal por dominio + global; residuo = gap (obs - esperado)
gaps={}
for col in ['gz','memoria']:
    d2 = full.dropna(subset=[col])
    m = HistGradientBoostingRegressor(max_depth=3, max_iter=150, random_state=0).fit(d2[['edad','educacion']], d2[col])
    # predecir para los basales del df
    base = df[['edad','educacion']].copy()
    df[f'gap_{col}'] = df[f'z_{col}'] - m.predict(base.fillna(base.median()))
print("gaps normativos añadidos: gap_gz, gap_memoria")

# ---- 4) Target nuevo: declive fiable MEMORIA-específico ----
evl = ev.dropna(subset=['fecha']).sort_values(['persona_id','fecha']).drop_duplicates(['persona_id','fecha'])
evl['t']=evl.groupby('persona_id').fecha.rank(method='dense'); nt=evl.groupby('persona_id').t.transform('max')
evl=evl[nt>=2]
mem = de[de.dominio=='memoria'].assign(zm=lambda x:x.z_peor.clip(-6,4))[['eval_id','zm']]
evl=evl.merge(mem, on='eval_id', how='left')
first=evl.sort_values('t').groupby('persona_id').first(); last=evl.sort_values('t').groupby('persona_id').last()
dzm=(last.zm-first.zm).dropna()
mad=1.4826*(dzm-dzm.median()).abs().median(); rci_mem=1.96*mad
ytab=pd.DataFrame({'persona_id':dzm.index,'y_rci_mem':(dzm< -rci_mem).astype(int).values})
df=df.merge(ytab, on='persona_id', how='left')
print(f"target memoria: RCI_mem±{rci_mem:.2f} → prevalencia {100*df.y_rci_mem.mean():.0f}% ({int(df.y_rci_mem.sum())}/{int(df.y_rci_mem.notna().sum())})")

df.to_csv('data/interim/model_dataset_plus.csv', index=False)
print("guardado: data/interim/model_dataset_plus.csv", df.shape)
