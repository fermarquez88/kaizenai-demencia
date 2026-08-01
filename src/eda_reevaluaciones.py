"""EDA amplio del estudio de reevaluaciones. Descriptivo + cruces con conclusiones."""
import duckdb, pandas as pd, numpy as np
pd.set_option('display.width', 160)

con = duckdb.connect('db/evaluaciones_v2.duckdb', read_only=True)
ev = con.execute("""SELECT eval_id, persona_id, edad, educacion, sexo, obra_social, cohorte,
                    fecha_ev, n_scores FROM evaluaciones_v2 WHERE cohorte<>'wisc_v'""").df()
ref = con.execute("SELECT * FROM reference_standard").df()
per = con.execute("SELECT persona_id, n_episodios, longitudinal FROM personas").df()
perf = con.execute("SELECT * FROM perfil_conclusiones").df()
con.close()

ev['fecha'] = pd.to_datetime(ev.fecha_ev, errors='coerce')
df = ev.merge(ref, on='eval_id', how='left').merge(per, on='persona_id', how='left')
# dedup mismo-día
df = df.sort_values(['persona_id','fecha']).drop_duplicates(['persona_id','fecha'])
df['t_real'] = df.groupby('persona_id').fecha.rank(method='dense')
nfech = df.groupby('persona_id').t_real.transform('max')
df['reeval_real'] = nfech >= 2          # persona con >=2 fechas reales
df['es_basal'] = df.t_real == 1
SEV = {'normal':0,'leve':1,'leve_moderado':2,'moderado':3,'moderado_grave':4,'grave':5}
perf['sev_n'] = perf.perfil_severidad.map(SEV)

print("="*70, "\nA. SESGO DE SELECCIÓN — ¿quién vuelve a reevaluarse?")
base = df[df.es_basal].copy()
g = base.groupby('reeval_real')
print(f"  personas basales: reeval={int((base.reeval_real).sum())}  1-toma={int((~base.reeval_real).sum())}")
for col in ['edad','educacion','n_dom_deficitario','n_dominios_evaluados']:
    m = g[col].mean()
    print(f"  {col:22s} reeval={m.get(True,np.nan):.1f}  1toma={m.get(False,np.nan):.1f}")
print("  % femenino:", g.sexo.apply(lambda s:(s.astype(str).str.upper().str[0]=='F').mean()).round(2).to_dict())
print("  top obra_social (reeval):", base[base.reeval_real].obra_social.value_counts().head(3).to_dict())

print("="*70, "\nB. ESTRUCTURA DE SEGUIMIENTO")
rr = df[df.reeval_real]
span = rr.groupby('persona_id').fecha.agg(lambda s:(s.max()-s.min()).days/365.25)
print(f"  personas reeval real: {rr.persona_id.nunique()} | intervalo años med={span.median():.2f} IQR[{span.quantile(.25):.2f},{span.quantile(.75):.2f}]")
print("  tomas reales por persona:", df[df.reeval_real].groupby('persona_id').t_real.max().value_counts().sort_index().to_dict())

print("="*70, "\nC. VALIDEZ DE CONSTRUCTO — severidad codificada vs z objetivo")
m = perf.merge(df[['eval_id','n_dom_deficitario','n_dominios_evaluados','deterioro_deficitario']], on='eval_id', how='left')
print(m.groupby('perfil_severidad').agg(n=('eval_id','size'),
      n_dom_defic_medio=('n_dom_deficitario','mean'),
      pct_deterioro_z=('deterioro_deficitario','mean')).round(2).reindex(list(SEV)+['no_concluyente']).to_string())

print("="*70, "\nD. TRAYECTORIAS POR FENOTIPO (basal→última reeval)")
pm = perf.merge(df[['eval_id','t_real','reeval_real']], on='eval_id', how='left')
pm = pm[pm.reeval_real==True].dropna(subset=['sev_n'])
first = pm.sort_values('t_real').groupby('persona_id').first()
last = pm.sort_values('t_real').groupby('persona_id').last()
traj = pd.DataFrame({'patron_basal':first.perfil_patron,'sev_basal':first.sev_n,'sev_ult':last.sev_n,
                     'almac_basal':first.mem_almacenamiento,'animo_basal':first.mod_animo})
traj['delta']=traj.sev_ult-traj.sev_basal
print(f"  n trayectorias: {len(traj)}")
for pat,grp in traj.groupby('patron_basal'):
    if len(grp)>=8:
        print(f"  {pat:24s} n={len(grp):3d}  Δmedio={grp.delta.mean():+.2f}  %empeora={100*(grp.delta>0).mean():.0f}")

print("="*70, "\nE. REGRESIÓN A LA MEDIA / TECHO — Δ por severidad basal")
for sb,grp in traj.groupby('sev_basal'):
    lab=[k for k,v in SEV.items() if v==sb][0]
    print(f"  basal={lab:16s} n={len(grp):3d}  Δmedio={grp.delta.mean():+.2f}  %empeora={100*(grp.delta>0).mean():.0f}  %mejora={100*(grp.delta<0).mean():.0f}")

print("="*70, "\nF. MEMORIA (almacenamiento) y ÁNIMO basal → declive")
print("  almacenamiento basal:")
for a,grp in traj.groupby('almac_basal'):
    print(f"    {a:14s} n={len(grp):3d}  Δmedio={grp.delta.mean():+.2f}  %empeora={100*(grp.delta>0).mean():.0f}")
print("  ánimo (modulador) basal:")
for a,grp in traj.groupby('animo_basal'):
    print(f"    animo={str(a):6s} n={len(grp):3d}  Δmedio={grp.delta.mean():+.2f}  %empeora={100*(grp.delta>0).mean():.0f}")
