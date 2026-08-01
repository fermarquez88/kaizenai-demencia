"""Ensambla el dataset de modelado predictivo: 1 fila/persona reeval-real,
features del BASAL + 3 targets de empeoramiento."""
import duckdb, pandas as pd, numpy as np, re
CORE = ['atencion','funciones_ejecutivas','memoria','lenguaje','visuoespacial']
RCI_GLOBAL = 0.97

con = duckdb.connect('db/evaluaciones_v2.duckdb', read_only=True)
ev = con.execute("""SELECT eval_id, persona_id, path, fecha_ev, cohorte, edad, educacion, sexo
                    FROM evaluaciones_v2 WHERE cohorte<>'wisc_v'""").df()
de = con.execute("SELECT eval_id, dominio, z_peor FROM dominio_eval").df()
perf = con.execute("SELECT * FROM perfil_conclusiones").df()
rav = con.execute("""SELECT path, intrusiones, confabulaciones, tipo_curva, aprendizaje_total,
                     tasa_aprendizaje, recon_corregido FROM ravlt_proceso""").df()
cl = con.execute("SELECT fuente, ape, nom, persona_id FROM cuest_link").df()
cp = con.execute("""SELECT pac_apellido, pac_nombre, gds_total_calc, cqc_total_provisto,
                    adlq_severidad, adlq_alterados FROM cuestionario_paciente""").df()
con.close()

# clip de z extremos: z_peor≤-6 = artefacto de piso (tests cronometrados reverse-scored, ver
# APRENDIZAJES_EXTRACCION §1); clínicamente ≤-6 ya es 'deficitario profundo'. Preserva ordinalidad, quita ruido.
de['z_peor'] = de.z_peor.clip(-6, 4)

ev['fecha'] = pd.to_datetime(ev.fecha_ev, errors='coerce')
ev = ev.dropna(subset=['fecha']).sort_values(['persona_id','fecha']).drop_duplicates(['persona_id','fecha'])
ev['t'] = ev.groupby('persona_id').fecha.rank(method='dense')
nt = ev.groupby('persona_id').t.transform('max')
ev = ev[nt>=2]                                    # reeval real

# z por dominio (ancho) por eval
zp = de[de.dominio.isin(CORE+['premorbido','ci_wais'])].pivot_table(
        index='eval_id', columns='dominio', values='z_peor', aggfunc='first')
zp['gz'] = zp[CORE].mean(axis=1)
zp['dispersion'] = zp[CORE].std(axis=1)

basal = ev.sort_values('t').groupby('persona_id').first().reset_index()
ult   = ev.sort_values('t').groupby('persona_id').last().reset_index()
intervalo = (ult.set_index('persona_id').fecha - basal.set_index('persona_id').fecha).dt.days/365.25

# --- features del basal ---
df = basal[['persona_id','eval_id','path','edad','educacion','sexo']].rename(columns={'eval_id':'eval_basal'})
df['intervalo'] = df.persona_id.map(intervalo)
df['sexo_f'] = (df.sexo.astype(str).str.upper().str[0]=='F').astype(int)
df = df.merge(zp.add_prefix('z_'), left_on='eval_basal', right_index=True, how='left')
# perfil basal
pcols = ['perfil_severidad','perfil_patron','multidominio','mem_almacenamiento',
         'mem_intrusiones_confab','mem_beneficio_contexto','mod_animo','mod_sueno','mod_ansiedad','mod_sensorial']
df = df.merge(perf[['eval_id']+pcols].rename(columns={'eval_id':'eval_basal'}), on='eval_basal', how='left')
# RAVLT proceso basal (por path)
df = df.merge(rav, on='path', how='left')
# cuestionarios → persona por nombre NORMALIZADO (acentos/case) vía cuest_link
import unicodedata
def _n(s):
    s=''.join(c for c in unicodedata.normalize('NFD',str(s)) if unicodedata.category(c)!='Mn')
    return re.sub(r'[^a-z]','',s.lower())
cl['k']=cl.ape.map(_n)+'|'+cl.nom.map(_n)
cp['k']=cp.pac_apellido.map(_n)+'|'+cp.pac_nombre.map(_n)
cpx = cp.merge(cl[['k','persona_id']].drop_duplicates('k'), on='k', how='left').dropna(subset=['persona_id'])
cpx = cpx.drop_duplicates('persona_id')[['persona_id','gds_total_calc','cqc_total_provisto','adlq_severidad','adlq_alterados']]
df = df.merge(cpx, on='persona_id', how='left')
# reserva: caída desde premórbido
df['caida_premorb'] = df['z_gz'] - df['z_premorbido']

# --- targets (del último toma) ---
gz_last = ult.set_index('persona_id').eval_id.map(zp['gz'])
gz_basal = basal.set_index('persona_id').eval_id.map(zp['gz'])
sev_ord = {'normal':0,'leve':1,'leve_moderado':2,'moderado':3,'moderado_grave':4,'grave':5}
sev_basal = basal.set_index('persona_id').eval_id.map(perf.set_index('eval_id').perfil_severidad).map(sev_ord)
sev_last  = ult.set_index('persona_id').eval_id.map(perf.set_index('eval_id').perfil_severidad).map(sev_ord)

tg = pd.DataFrame(index=basal.persona_id)
tg['dz'] = (gz_last - gz_basal)
# ajuste por basal (ANCOVA residual)
m = tg.dz.notna() & gz_basal.notna()
b,a = np.polyfit(gz_basal[m], gz_last[m], 1)
tg['dz_ajust'] = gz_last - (a + b*gz_basal)                       # T2 continuo
tg['y_rci'] = (tg.dz < -RCI_GLOBAL).astype('Int64')              # T1 declive fiable global
tg['y_conv'] = ((sev_last - sev_basal) >= 1).astype('Int64')     # T3 conversión de banda
df = df.merge(tg.reset_index(), on='persona_id', how='left')

df.to_csv('data/interim/model_dataset.csv', index=False)
print("dataset:", df.shape, "→ data/interim/model_dataset.csv")
print("\nTargets (prevalencia):")
print("  T1 declive fiable (RCI):", int(df.y_rci.sum()), "/", int(df.y_rci.notna().sum()), f"({100*df.y_rci.mean():.0f}%)")
print("  T3 conversión banda    :", int(df.y_conv.sum()), "/", int(df.y_conv.notna().sum()), f"({100*df.y_conv.mean():.0f}%)")
print("  T2 dz_ajust: media %.2f sd %.2f" % (df.dz_ajust.mean(), df.dz_ajust.std()))
print("\nMissingness (features clave):")
for c in ['edad','educacion','z_gz','z_memoria','z_premorbido','perfil_patron','intrusiones','gds_total_calc','cqc_total_provisto','adlq_severidad']:
    print(f"  {c:22s} {100*df[c].notna().mean():.0f}% presente")
