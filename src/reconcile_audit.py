"""Reconciliación de las cifras disputadas por la auditoría, con las definiciones originales."""
import warnings; warnings.filterwarnings('ignore')
import duckdb, numpy as np, pandas as pd
CORE=['atencion','funciones_ejecutivas','memoria','lenguaje','visuoespacial']
SEV={'normal':0,'leve':1,'leve_moderado':2,'moderado':3,'moderado_grave':4,'grave':5}
con=duckdb.connect('db/evaluaciones_v2.duckdb',read_only=True)
de=con.execute("SELECT eval_id,dominio,z_peor FROM dominio_eval").df()
ev=con.execute("SELECT eval_id,persona_id,fecha_ev,edad,educacion,sexo FROM evaluaciones_v2 WHERE cohorte<>'wisc_v'").df()
perf=con.execute("SELECT eval_id,persona_id,fecha_ev,perfil_severidad,mod_animo FROM perfil_conclusiones").df()
con.close()
ev['fecha']=pd.to_datetime(ev.fecha_ev,errors='coerce')

def wil(k,n):
    if n==0: return (np.nan,np.nan,np.nan)
    p=k/n; z=1.96; d=1+z*z/n; c=(p+z*z/2/n)/d; h=z*np.sqrt(p*(1-p)/n+z*z/4/n/n)/d; return p,max(0,c-h),min(1,c+h)

print("="*80,"\nA) REGRESIÓN A LA MEDIA — pendiente vs correlación (z global SIN clip, def original)\n","="*80)
d=de[de.dominio.isin(CORE)].merge(ev,on='eval_id').dropna(subset=['fecha','z_peor'])
d=d.sort_values(['persona_id','fecha']).drop_duplicates(['persona_id','fecha','dominio'])
gz=d.groupby(['persona_id','fecha','eval_id']).z_peor.mean().rename('gz').reset_index()
gz['t']=gz.groupby('persona_id').fecha.rank(method='dense'); gz=gz[gz.groupby('persona_id').t.transform('max')>=2]
fb=gz.sort_values('t').groupby('persona_id').first(); ll=gz.sort_values('t').groupby('persona_id').last()
tj=pd.DataFrame({'b':fb.gz,'l':ll.gz}).dropna()
b,a=np.polyfit(tj.b,tj.l,1); r=np.corrcoef(tj.b,tj.l)[0,1]
print(f"  n={len(tj)}  pendiente b={b:.3f}  intercepto a={a:.2f}  r={r:.3f}")
print(f"  => manuscrito debe decir: PENDIENTE 0,26 (r=0,38), no 'correlación 0,26'")

print("\n"+"="*80,"\nB) TABLA 1 — grupo 'una visita' (definiciones alternativas)\n","="*80)
evv=ev.dropna(subset=['fecha']).sort_values(['persona_id','fecha']).drop_duplicates(['persona_id','fecha'])
ndates=evv.groupby('persona_id').fecha.nunique()
arch=ev.groupby('persona_id').size()
reev=set(ndates[ndates>=2].index)
first=ev.sort_values('fecha').groupby('persona_id').first()
for defn,ids in [("arch==1 (1 sola eval archivada)", set(arch[arch==1].index)),
                 ("1 sola fecha distinta (incluye same-day dups)", set(ndates[ndates==1].index)),
                 ("NO reeval (todos menos 250)", set(first.index)-reev)]:
    d1=first.loc[sorted(ids)]
    sx=d1.sexo.astype(str).str.lower(); fem=sx.isin(['f','femenino','2','mujer']).mean()*100
    print(f"  [{defn}] n={len(ids)}  edad={d1.edad.mean():.1f}±{d1.edad.std():.1f}  educ={d1.educacion.mean():.1f}±{d1.educacion.std():.1f}  fem={fem:.0f}%")
dR=first.loc[sorted(reev)]; sx=dR.sexo.astype(str).str.lower()
print(f"  [REEVAL n={len(reev)}] edad={dR.edad.mean():.1f}±{dR.edad.std():.1f}  educ={dR.educacion.mean():.1f}±{dR.educacion.std():.1f}  fem={sx.isin(['f','femenino','2','mujer']).mean()*100:.0f}%")

print("\n"+"="*80,"\nC) VALIDEZ DE CONSTRUCTO — dominios deficitarios por banda a distintos umbrales\n","="*80)
band=perf.drop_duplicates('eval_id').set_index('eval_id').perfil_severidad.map(SEV)
for thr in (-1.5,-2.0):
    zw=de[de.dominio.isin(CORE)].pivot_table(index='eval_id',columns='dominio',values='z_peor',aggfunc='min')
    ndef=(zw<=thr).sum(axis=1); any_def=(zw<=thr).any(axis=1).astype(int)
    cv=pd.DataFrame({'ndef':ndef,'any':any_def,'band':band}).dropna()
    m={k:round(cv[cv.band==v].ndef.mean(),2) for k,v in [('normal',0),('leve',1),('moderado',3),('grave',5)]}
    pnorm=100*cv[cv.band==0]['any'].mean(); pge=100*cv[cv.band>=2]['any'].mean()
    print(f"  umbral z<={thr}:  medias {m}  | %≥1 def: normal={pnorm:.0f}%  ≥leve-mod={pge:.0f}%")
print("  (manuscrito: 0,44/1,98/3,83/4,50 ; 29% -> 100%)")

print("\n"+"="*80,"\nD) MODULADOR ANÍMICO — progresión a demencia por ánimo basal\n","="*80)
perf['f']=pd.to_datetime(perf.fecha_ev,errors='coerce'); perf['s']=perf.perfil_severidad.map(SEV)
ps=perf.dropna(subset=['f','s']).sort_values(['persona_id','f']).drop_duplicates(['persona_id','f'])
ps['t']=ps.groupby('persona_id').f.rank(method='dense'); ps=ps[ps.groupby('persona_id').t.transform('max')>=2]
sb=ps.sort_values('t').groupby('persona_id').first(); sl=ps.sort_values('t').groupby('persona_id').last().s
prof=pd.DataFrame({'sb':sb.s,'ebasal':sb.eval_id,'sl':sl}).dropna(); prof['ydem']=(prof.sl>=3).astype(int)
def tb(x): return str(x).strip().lower() in ('true','1','si','sí')
prof['mood']=prof.ebasal.map(perf.drop_duplicates('eval_id').set_index('eval_id').mod_animo).map(tb)
for lab,sub in [("TODOS 182",prof),("deterioro leve-mod (sb∈1,2)",prof[prof.sb.isin([1,2])])]:
    for mv,mn in [(True,'con ánimo'),(False,'sin ánimo')]:
        s=sub[sub.mood==mv]; k=int(s.ydem.sum()); n=len(s); p,lo,hi=wil(k,n)
        print(f"  [{lab}] {mn}: {k}/{n} = {100*p:.0f}% [{100*lo:.0f}-{100*hi:.0f}]")

print("\n"+"="*80,"\nE) PERSONA-AÑOS y tasa (cohorte deterioro leve-mod)\n","="*80)
fu=((ll.fecha-fb.fecha).dt.days/365.25)
dlm=prof[prof.sb.isin([1,2])].index
py=fu.reindex(dlm).dropna().sum(); ev32=int(prof[prof.sb.isin([1,2])].ydem.sum())
print(f"  eventos={ev32}  persona-años={py:.0f}  tasa={100*ev32/py:.1f}%/año   (manu: 32 / 261 / 12,3)")
