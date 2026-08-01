"""
AUDITORÍA INTEGRAL del manuscrito (texto + Tabla 1 + Tabla 2 + Figuras 1-5).
Recomputa cada cifra desde db/evaluaciones_v2.duckdb y la compara con lo escrito.
Salida: [OK]/[DIF]/[CHECK] por afirmación.
"""
import warnings; warnings.filterwarnings('ignore')
import duckdb, numpy as np, pandas as pd
from scipy.stats import chi2_contingency
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_predict, StratifiedKFold, RepeatedStratifiedKFold, cross_val_score
from sklearn.pipeline import Pipeline; from sklearn.impute import SimpleImputer; from sklearn.preprocessing import StandardScaler
from sklearn.metrics import roc_auc_score

SEV={'normal':0,'leve':1,'leve_moderado':2,'moderado':3,'moderado_grave':4,'grave':5}
CORE=['memoria','atencion','funciones_ejecutivas','lenguaje','visuoespacial']; RNG=42
con=duckdb.connect('db/evaluaciones_v2.duckdb',read_only=True)
ev=con.execute("SELECT eval_id,persona_id,fecha_ev,edad,educacion,sexo,cohorte FROM evaluaciones_v2 WHERE cohorte<>'wisc_v'").df()
de=con.execute("SELECT eval_id,dominio,z_peor FROM dominio_eval").df()
pc=con.execute("""SELECT eval_id,persona_id,fecha_ev,perfil_severidad,perfil_patron,multidominio,
                  dom_memoria,mem_almacenamiento,mod_animo,perfil_estabilidad,estabilidad_magnitud FROM perfil_conclusiones""").df()
r=con.execute("SELECT eval_id,test,subtest,z_final FROM resultados_v2 WHERE z_final IS NOT NULL").df()
con.close()
RES=[]
def chk(label, manu, calc, tol=0.05, kind='num'):
    if kind=='num':
        try: ok = abs(float(manu)-float(calc))<=tol
        except: ok=False
    else: ok = str(manu)==str(calc)
    RES.append((('OK ' if ok else 'DIF'), label, manu, calc))
def note(label, calc): RES.append(('CHK', label, '—', calc))

# ---------- cohorte ----------
ev['f']=pd.to_datetime(ev.fecha_ev,errors='coerce')
arch=ev.groupby('persona_id').size()                      # evals archivadas por persona
evv=ev.dropna(subset=['f']).sort_values(['persona_id','f']).drop_duplicates(['persona_id','f'])
ndates=evv.groupby('persona_id').f.nunique()
multi_arch=(arch>=2).sum(); reeval=(ndates>=2).sum(); single=(arch==1).sum()
chk("334 pacientes ≥2 evals archivadas", 334, multi_arch, tol=2)
chk("250 reevaluación genuina (≥2 fechas)", 250, reeval, tol=2)
chk("Tabla1: una visita n=2648", 2648, single, tol=30)

evd=evv[evv.groupby('persona_id').persona_id.transform('size')>=0]
evd['t']=evd.groupby('persona_id').f.rank(method='dense'); evd=evd[evd.groupby('persona_id').t.transform('max')>=2]
first=evd.sort_values('t').groupby('persona_id').first().reset_index()
last=evd.sort_values('t').groupby('persona_id').last().reset_index()
# seguimiento
fu=((last.set_index('persona_id').f-first.set_index('persona_id').f).dt.days/365.25)
chk("seguimiento mediana 1,83 años", 1.83, fu.median(), tol=0.08)
note("seguimiento IQR (manu 1,25–2,97)", f"{fu.quantile(.25):.2f}–{fu.quantile(.75):.2f}")
# nº evals por persona (2/3/4) entre reevaluados
nper=ndates[ndates>=2]
note("nº evals 2/3/4 (manu 213/36/1)", dict(nper.value_counts().sort_index()))

# Tabla 1 demografía: reeval vs una visita (a nivel persona, usando 1ra eval)
firsteval=ev.sort_values('f').groupby('persona_id').first()
reev_ids=set(nper.index); firsteval['grp']=firsteval.index.map(lambda p:'reeval' if p in reev_ids else 'single')
for g,lab in [('reeval','Reeval'),('single','Una visita')]:
    d=firsteval[firsteval.grp==g]
    note(f"T1 {lab}: edad media (manu {'67,0' if g=='reeval' else '63,8'})", f"{d.edad.mean():.1f}±{d.edad.std():.1f}")
    note(f"T1 {lab}: educ (manu {'13,3' if g=='reeval' else '12,9'})", f"{d.educacion.mean():.1f}±{d.educacion.std():.1f}")
    sx=d.sexo.astype(str).str.lower()
    fem=sx.isin(['f','femenino','2','mujer']).mean()*100
    note(f"T1 {lab}: % femenino (manu {'55' if g=='reeval' else '56'})", f"{fem:.0f}%")

# ---------- severidad basal/final (perfil_conclusiones) ----------
pc['f']=pd.to_datetime(pc.fecha_ev,errors='coerce'); pc['s']=pc.perfil_severidad.map(SEV)
ps=pc.dropna(subset=['f','s']).sort_values(['persona_id','f']).drop_duplicates(['persona_id','f'])
ps['t']=ps.groupby('persona_id').f.rank(method='dense'); ps=ps[ps.groupby('persona_id').t.transform('max')>=2]
sb=ps.sort_values('t').groupby('persona_id').first().s; sl=ps.sort_values('t').groupby('persona_id').last().s
prof=pd.DataFrame({'sb':sb,'sl':sl}).dropna()
chk("182 con perfil basal+final", 182, len(prof), tol=3)
chk("DCL basal=leve n=85", 85, (prof.sb==1).sum(), tol=3)
chk("deterioro leve-mod basal∈{1,2} n=122", 122, prof.sb.isin([1,2]).sum(), tol=3)
prof['ydem']=(prof.sl>=3).astype(int)
chk("DCL→demencia eventos=16", 16, prof[prof.sb==1].ydem.sum(), tol=1)
chk("deterioro leve-mod→demencia eventos=32", 32, prof[prof.sb.isin([1,2])].ydem.sum(), tol=1)
# transiciones (todas las bandas basales)
allp=pd.DataFrame({'sb':sb,'sl':sl}).dropna()
worse=(allp.sl>allp.sb).mean()*100; same=(allp.sl==allp.sb).mean()*100; better=(allp.sl<allp.sb).mean()*100
chk("33% empeoró ≥1 banda", 33, worse, tol=4); chk("55% estable", 55, same, tol=4); chk("13% mejoró", 13, better, tol=4)
rev=allp[(allp.sb==1)]; chk("reversión DCL→normal 5/85", 5, (rev.sl==0).sum(), tol=2)
# tasa de progresión: eventos/persona-años en cohorte deterioro leve-mod
dlm_ids=prof[prof.sb.isin([1,2])].index
py=fu.reindex(dlm_ids).dropna().sum()
note("persona-años deterioro leve-mod (manu 261)", f"{py:.0f}")
note("tasa %/año (manu 12,3)", f"{100*prof[prof.sb.isin([1,2])].ydem.sum()/py:.1f}")
# normales basal
norm_ids=allp[allp.sb==0].index; note("normales basal n (manu 14) y eventos (manu 0)",
    f"n={len(norm_ids)}, →dem={(allp.loc[norm_ids].sl>=3).sum()}")

# ---------- regresión a la media ----------
gz=de[de.dominio.isin(CORE)].assign(z=lambda x:x.z_peor.clip(-6,4)).groupby('eval_id').z.mean()
gb=first.set_index('persona_id').eval_id.map(gz); gl=last.set_index('persona_id').eval_id.map(gz)
rtm=pd.DataFrame({'b':gb,'l':gl}).dropna()
chk("regresión a la media r=0,26", 0.26, rtm.b.corr(rtm.l), tol=0.05)

# ---------- subtipos objetivos (ya auditado; re-confirmar) ----------
zwide=de[de.dominio.isin(CORE)].assign(z=lambda x:x.z_peor.clip(-6,4)).pivot_table(index='eval_id',columns='dominio',values='z',aggfunc='min')
def subobj(eb):
    if eb not in zwide.index: return np.nan
    row=zwide.loc[eb]; pres={d:row[d] for d in CORE if pd.notna(row.get(d))}
    if len(pres)<3: return np.nan
    af=[d for d,v in pres.items() if v<=-1.5]; n=len(af); mem='memoria' in af
    if n==0: return 'Sin det'
    return ('Amn' if mem else 'noAmn')+('MD' if n>=2 else 'DU')
risk=prof[prof.sb.isin([1,2])].copy(); risk['sub']=[subobj(first.set_index('persona_id').eval_id.get(p)) for p in risk.index]
vc=risk.dropna(subset=['sub']).groupby('sub').ydem.agg(['sum','count'])
note("subtipos objetivos (manu AmnMD 30/94, noAmnMD 1/11, AmnDU 0/9, noAmnDU 0/5)", vc.to_dict('index'))
amnmd=vc.loc['AmnMD'] if 'AmnMD' in vc.index else None
if amnmd is not None: chk("AmnMD progresión 32%", 0.32, amnmd['sum']/amnmd['count'], tol=0.03)

# ---------- modulador anímico ----------
pcb=pc.drop_duplicates('eval_id').set_index('eval_id')
mood=first.set_index('persona_id').eval_id.map(pcb.mod_animo)
mm=pd.DataFrame({'mood':mood,'ydem':prof.ydem}).dropna()
def tb(x): return str(x).strip().lower() in ('true','1','si','sí')
mm['mood']=mm.mood.map(tb)
note("mood: con ánimo (manu 20%, n=30) vs sin (manu 36%)",
     f"con={100*mm[mm.mood].ydem.mean():.0f}% n={mm.mood.sum()}, sin={100*mm[~mm.mood].ydem.mean():.0f}%")

# ---------- construct validity: dominios deficitarios por banda ----------
ndef=(zwide<=-1.5).sum(axis=1)
band=pc.drop_duplicates('eval_id').set_index('eval_id').perfil_severidad.map(SEV)
cv=pd.DataFrame({'ndef':ndef,'band':band}).dropna()
means={k:round(cv[cv.band==v].ndef.mean(),2) for k,v in [('normal',0),('leve',1),('moderado',3),('grave',5)]}
note("dominios deficitarios por banda (manu 0,44/1,98/3,83/4,50)", means)

# ---------- modelos: re-correr AUC OOF (DCL y deterioro leve-mod) ----------
mr=r[(r.test=='Memoria de Relatos')&(r.subtest=='Diferido')].assign(zc=lambda x:x.z_final.clip(-6,4))
mrb=mr.merge(first[['eval_id','persona_id']],on='eval_id')[['persona_id','zc']].drop_duplicates('persona_id').set_index('persona_id').zc
M=prof.copy(); M['edad']=first.set_index('persona_id').edad; M['mr']=M.index.map(mrb)
def oof_auc(cols,d,y,R=5):
    P=np.zeros(len(y))
    for rr in range(R):
        p=Pipeline([('i',SimpleImputer(strategy='median',add_indicator=True)),('s',StandardScaler()),('m',LogisticRegression(class_weight='balanced',max_iter=4000))])
        P+=cross_val_predict(p,d[cols],y,cv=StratifiedKFold(5,shuffle=True,random_state=RNG+rr),method='predict_proba',n_jobs=-1)[:,1]
    return roc_auc_score(y,P/R)
d1=M[M.sb==1].dropna(subset=['mr','edad','ydem']); a1=oof_auc(['mr','edad'],d1,d1.ydem.values)
d2=M[M.sb.isin([1,2])].dropna(subset=['mr','edad','ydem']); a2=oof_auc(['mr','edad','sb'],d2,d2.ydem.values)
note("AUC DCL→dem (manu 0,84)", f"{a1:.2f} (n={len(d1)}, ev={int(d1.ydem.sum())})")
note("AUC deterioro leve-mod→dem (manu 0,80)", f"{a2:.2f} (n={len(d2)}, ev={int(d2.ydem.sum())})")
# valor incremental
def auc_cv(cols,d,y):
    p=Pipeline([('i',SimpleImputer(strategy='median',add_indicator=True)),('s',StandardScaler()),('m',LogisticRegression(class_weight='balanced',max_iter=4000))])
    return cross_val_score(p,d[cols],y,scoring='roc_auc',cv=RepeatedStratifiedKFold(n_splits=5,n_repeats=20,random_state=RNG),n_jobs=-1).mean()
note("incremental deterioro leve-mod: edad sola / mem sola / completo (manu 0,69/–/0,78)",
     f"{auc_cv(['edad'],d2,d2.ydem.values):.2f} / {auc_cv(['mr'],d2,d2.ydem.values):.2f} / {auc_cv(['edad','mr','sb'],d2,d2.ydem.values):.2f}")

# EPV arithmetic
for lab,ev_,k in [("EPV DCL 8,0",16,2),("EPV det leve-mod 10,7",32,3),("EPV declive 6,8",34,5)]:
    note(lab, f"{ev_/k:.1f}")

# ---------- imprimir ----------
print(f"\n{'='*90}\nAUDITORÍA INTEGRAL — {sum(1 for x in RES if x[0]=='OK ')} OK / "
      f"{sum(1 for x in RES if x[0]=='DIF')} DIF / {sum(1 for x in RES if x[0]=='CHK')} CHECK\n{'='*90}")
for flag,lab,manu,calc in RES:
    print(f"[{flag}] {lab:52s} manu={manu}  calc={calc}")
