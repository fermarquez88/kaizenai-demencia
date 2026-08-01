"""Auditoría end-to-end del pipeline predictivo. Chequea fuga, definiciones, missingness, sanity."""
import warnings, os; os.environ['PYTHONWARNINGS']='ignore'; warnings.filterwarnings('ignore')
import duckdb, numpy as np, pandas as pd
from scipy.stats import pointbiserialr

df = pd.read_csv('data/interim/model_dataset_plus.csv')
SEV={'normal':0,'leve':1,'leve_moderado':2,'moderado':3,'moderado_grave':4,'grave':5}
df['sev_ord']=df.perfil_severidad.map(SEV)

print("="*70,"\n1) FUGA DE INTERVALO — ¿el tiempo de seguimiento predice el target?")
for t in ['y_rci','y_conv']:
    d=df.dropna(subset=[t,'intervalo'])
    r,p=pointbiserialr(d[t], d.intervalo)
    print(f"   intervalo↔{t}: r={r:+.2f} p={p:.3f}  (intervalo medio evento={d[d[t]==1].intervalo.mean():.2f} vs no={d[d[t]==0].intervalo.mean():.2f})")

print("\n2) DEFINICIONES / EVENTOS")
con=duckdb.connect('db/evaluaciones_v2.duckdb',read_only=True)
ps=con.execute("SELECT persona_id,fecha_ev,perfil_severidad FROM perfil_conclusiones").df(); con.close()
ps['s']=ps.perfil_severidad.map(SEV); ps['f']=pd.to_datetime(ps.fecha_ev,errors='coerce')
ps=ps.dropna(subset=['f','s']).sort_values(['persona_id','f']).drop_duplicates(['persona_id','f'])
ps['t']=ps.groupby('persona_id').f.rank(method='dense'); ps=ps[ps.groupby('persona_id').t.transform('max')>=2]
f=ps.sort_values('t').groupby('persona_id').first(); l=ps.sort_values('t').groupby('persona_id').last()
print("   personas c/severidad basal+final:", len(f))
print("   DCL leve→demencia(≥mod):", int(((f.s==1)&(l.s>=3)).sum()),"/",int((f.s==1).sum()))
print("   pre-dem→demencia:", int(((f.s<=2)&(l.s>=3)).sum()),"/",int((f.s<=2).sum()))

print("\n3) MISSINGNESS de features clave")
for c in ['z_memoria','z_gz','dprime','criterio_c','fp_listaB','z_premorbido','adlq_pct','gap_gz','intrusiones','educacion']:
    print(f"   {c:16s} {100*df[c].notna().mean():.0f}% presente")

print("\n4) SANITY de features nuevas (rango/outliers)")
for c in ['dprime','criterio_c','fp_listaB','gap_gz','gap_memoria','adlq_pct']:
    s=df[c].dropna(); print(f"   {c:14s} n={len(s):3d} min={s.min():.2f} med={s.median():.2f} max={s.max():.2f}")

print("\n5) CORRELACIÓN feature↔target (¿algún feature sospechosamente perfecto = fuga?)")
for t in ['y_rci','y_conv']:
    d=df.dropna(subset=[t]); cors={}
    for c in ['z_memoria','z_gz','dprime','intrusiones','sev_ord','edad','educacion','gap_gz']:
        dd=d.dropna(subset=[c]);
        if dd[c].std()>0: cors[c]=pointbiserialr(dd[t],dd[c])[0]
    top=sorted(cors.items(),key=lambda x:-abs(x[1]))[:4]
    print(f"   {t}: "+" ".join(f"{c}={r:+.2f}" for c,r in top))
