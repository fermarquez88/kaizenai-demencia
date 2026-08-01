"""Cambio continuo (Δz), RCI empírico y modelos ajustados por basal (ANCOVA)."""
import duckdb, pandas as pd, numpy as np
np.set_printoptions(suppress=True)
CORE = ['atencion','funciones_ejecutivas','memoria','lenguaje','visuoespacial']

con = duckdb.connect('db/evaluaciones_v2.duckdb', read_only=True)
de = con.execute("SELECT eval_id, dominio, z_peor FROM dominio_eval").df()
ev = con.execute("SELECT eval_id, persona_id, fecha_ev, cohorte, edad, educacion FROM evaluaciones_v2 WHERE cohorte<>'wisc_v'").df()
perf = con.execute("SELECT eval_id, perfil_patron, perfil_severidad, mem_almacenamiento, mod_animo, perfil_estabilidad FROM perfil_conclusiones").df()
con.close()

ev['fecha'] = pd.to_datetime(ev.fecha_ev, errors='coerce')
d = de[de.dominio.isin(CORE)].merge(ev, on='eval_id').dropna(subset=['fecha','z_peor'])
d = d.sort_values(['persona_id','fecha']).drop_duplicates(['persona_id','fecha','dominio'])
# global z por eval = media de dominios core
gz = d.groupby(['persona_id','fecha','eval_id']).z_peor.mean().rename('gz').reset_index()
gz['t'] = gz.groupby('persona_id').fecha.rank(method='dense')
nt = gz.groupby('persona_id').t.transform('max')
gz = gz[nt>=2]                                     # reeval real
first = gz.sort_values('t').groupby('persona_id').first()
last  = gz.sort_values('t').groupby('persona_id').last()
traj = pd.DataFrame({'gz_basal':first.gz,'gz_ult':last.gz,'eval_basal':first.eval_id})
traj['intervalo'] = (last.fecha - first.fecha).dt.days/365.25
traj['dz'] = traj.gz_ult - traj.gz_basal
traj['eval_ult'] = last.eval_id
traj = traj.merge(perf, left_on='eval_basal', right_on='eval_id', how='left')   # fenotipo/ánimo del BASAL
traj = traj.merge(perf[['eval_id','perfil_estabilidad']].rename(columns={'perfil_estabilidad':'estab_ult'}),
                  left_on='eval_ult', right_on='eval_id', how='left')            # estabilidad de la REEVAL
print(f"n trayectorias (global z): {len(traj)}  | intervalo med={traj.intervalo.median():.2f}")

print("\n=== 1. REGRESIÓN A LA MEDIA (global z) ===")
b,a = np.polyfit(traj.gz_basal, traj.gz_ult, 1)
r = np.corrcoef(traj.gz_basal, traj.gz_ult)[0,1]
print(f"  gz_ult = {a:+.2f} + {b:.2f}·gz_basal   (r test-retest={r:.2f})")
print(f"  pendiente {b:.2f}<1 ⇒ regresión a la media (Δz crudo confundido por basal). Ajustamos por ANCOVA.")
# cambio ajustado por basal = residuo de gz_ult ~ gz_basal
traj['pred'] = a + b*traj.gz_basal
traj['dz_ajust'] = traj.gz_ult - traj.pred        # <0 = peor de lo esperado (declive real)

def resumen(col, groups):
    print(f"\n=== {col} ===")
    for g,sub in traj.groupby(groups):
        if len(sub)>=8:
            print(f"  {str(g):26s} n={len(sub):3d}  Δz_crudo={sub.dz.mean():+.2f}  Δz_AJUST={sub.dz_ajust.mean():+.2f}  %declive_ajust={100*(sub.dz_ajust<-0.3).mean():.0f}")

print("\n=== 2. TRAYECTORIA POR FENOTIPO — cruda vs ajustada por basal ===")
resumen('perfil_patron','perfil_patron')
print("\n=== 3. ÁNIMO basal (semilla) — ajustado por basal ===")
resumen('mod_animo','mod_animo')
print("\n=== 4. ALMACENAMIENTO basal ===")
resumen('mem_almacenamiento','mem_almacenamiento')

print("\n=== 5. RCI EMPÍRICO por dominio (referencia = pares declarados 'estable') ===")
# Δz por dominio
dd = d.merge(gz[['persona_id','fecha']].assign(k=1), on=['persona_id','fecha'], how='inner')
piv = d.pivot_table(index=['persona_id','dominio'], columns=d.groupby(['persona_id','dominio']).fecha.rank(method='dense'),
                    values='z_peor', aggfunc='first')
# usar t=1 (basal) y máximo t (última)
piv = piv.dropna(subset=[1.0])
dzr = []
for (pid,dom),row in piv.iterrows():
    vals = row.dropna()
    if len(vals)>=2:
        dzr.append({'persona_id':pid,'dominio':dom,'dz':vals.iloc[-1]-vals.iloc[0]})
dzr = pd.DataFrame(dzr)
# etiqueta de estabilidad declarada (del basal)
est = perf.merge(ev[['eval_id','persona_id']], on='eval_id')[['persona_id','perfil_estabilidad']]
# z de piso extremos (tests cronometrados) inflan el SD → estadística robusta (MAD) + clip clínico
def mad(x): x=x.dropna(); return 1.4826*(x-x.median()).abs().median()
dzr['dz'] = dzr.dz.clip(-8, 8)
ref = traj[traj.estab_ult=='estable'].dz.clip(-8,8)
print(f"  referencia = pares con reeval declarada 'estable' (n={len(ref)}): MAD(Δz global)={mad(ref):.2f} → RCI≈1.96·MAD={1.96*mad(ref):.2f}")
for dom,sub in dzr.groupby('dominio'):
    m=mad(sub.dz); rci=1.96*m
    print(f"  {dom:22s} n={len(sub):3d}  Δz_medn={sub.dz.median():+.2f}  MAD={m:.2f}  RCI±{rci:.2f}  %declive_fiable={100*(sub.dz< -rci).mean():.0f}  %mejora_fiable={100*(sub.dz> rci).mean():.0f}")

print("\n=== 6. TRIANGULACIÓN: Δz global ajustado por basal vs estabilidad DECLARADA en la reeval ===")
print(traj.groupby('estab_ult').dz_ajust.agg(['size','mean']).round(2).to_string())
