"""Auditoría de selección de features: prueba TODOS los candidatos de la tabla del informe,
hace forward-selection con CV anidada por target, y compara contra los sets actuales. + colinealidad."""
import warnings, os; os.environ['PYTHONWARNINGS']='ignore'; warnings.filterwarnings('ignore')
import duckdb, numpy as np, pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import RepeatedStratifiedKFold, cross_val_score
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
RNG=42; SEV={'normal':0,'leve':1,'leve_moderado':2,'moderado':3,'moderado_grave':4,'grave':5}

con=duckdb.connect('db/evaluaciones_v2.duckdb',read_only=True)
r=con.execute("SELECT eval_id,test,subtest,z_final FROM resultados_v2 WHERE z_final IS NOT NULL").df()
ev=con.execute("SELECT eval_id,persona_id,fecha_ev,edad,educacion FROM evaluaciones_v2 WHERE cohorte<>'wisc_v'").df()
ps=con.execute("SELECT persona_id,fecha_ev,perfil_severidad FROM perfil_conclusiones").df()
con.close()
ev['f']=pd.to_datetime(ev.fecha_ev,errors='coerce')
ev=ev.dropna(subset=['f']).sort_values(['persona_id','f']).drop_duplicates(['persona_id','f'])
ev['t']=ev.groupby('persona_id').f.rank(method='dense'); ev=ev[ev.groupby('persona_id').t.transform('max')>=2]
basal=ev.sort_values('t').groupby('persona_id').first().reset_index()

CAND={'mr_diferido':('Memoria de Relatos','Diferido'),'mr_inmediato':('Memoria de Relatos','Inmediato'),
 'rey_diferido':('Lista de Rey','Diferido'),'rey_trial1':('Lista de Rey','Trial 1'),
 'figura_inmediato':('Figura de Rey','Inmediato'),'figura_recon':('Figura de Rey','Reconocimiento'),
 'ifs':('IFS',None),'hayling':('Test de Hayling',None),'digitos_atras':('Dígitos-span','Atrás'),
 'flu_semantica':('F Verbal Semántica',None),'wat':('WAT',None)}
r['zc']=r.z_final.clip(-6,4); rb=r.merge(basal[['eval_id','persona_id']],on='eval_id')
F=pd.DataFrame({'persona_id':basal.persona_id})
for c,(tt,ss) in CAND.items():
    sub=rb[(rb.test==tt)&((rb.subtest==ss) if ss else rb.subtest.isna())][['persona_id','zc']].drop_duplicates('persona_id')
    F=F.merge(sub.rename(columns={'zc':c}),on='persona_id',how='left')
F=F.merge(basal[['persona_id','edad','educacion']],on='persona_id',how='left')
ps['s']=ps.perfil_severidad.map(SEV); ps['f']=pd.to_datetime(ps.fecha_ev,errors='coerce')
ps=ps.dropna(subset=['f','s']).sort_values(['persona_id','f']).drop_duplicates(['persona_id','f'])
ps['t']=ps.groupby('persona_id').f.rank(method='dense'); ps=ps[ps.groupby('persona_id').t.transform('max')>=2]
fb=ps.sort_values('t').groupby('persona_id').first().s; lb=ps.sort_values('t').groupby('persona_id').last().s
tg=pd.DataFrame({'persona_id':fb.index,'sev_ord':fb.values,'y_dem':(lb>=3).astype(int).values})
F=F.merge(tg,on='persona_id',how='inner')
prev=pd.read_csv('data/interim/model_dataset_plus.csv')[['persona_id','y_rci','y_conv']]
F=F.merge(prev,on='persona_id',how='left')

ALLF=list(CAND)+['edad','educacion','sev_ord']
def auc(cols,d,y):
    p=Pipeline([('i',SimpleImputer(strategy='median',add_indicator=True)),('s',StandardScaler()),
                ('m',LogisticRegression(penalty='l1',solver='liblinear',C=0.4,class_weight='balanced',max_iter=5000))])
    return cross_val_score(p,d[cols],y,scoring='roc_auc',cv=RepeatedStratifiedKFold(n_splits=5,n_repeats=15,random_state=RNG),n_jobs=-1).mean()
def forward(d,y,cand,kmax=5):
    sel=[]; best=0.5
    while len(sel)<kmax:
        candi=[(auc(sel+[c],d,y),c) for c in cand if c not in sel]
        candi.sort(reverse=True)
        if not candi or candi[0][0]<=best+0.003: break
        best=candi[0][0]; sel.append(candi[0][1])
    return sel,best

CURRENT={'demencia_predem(y_dem,sev<=2)':(['mr_diferido','rey_diferido','ifs','edad','sev_ord'],'y_dem',F.sev_ord<=2),
 'demencia_dclleve(y_dem,sev==1)':(['mr_diferido','rey_diferido','ifs','edad'],'y_dem',F.sev_ord==1),
 'declive(y_rci)':(['rey_diferido','ifs','flu_semantica','edad','digitos_atras'],'y_rci',pd.Series(True,index=F.index)),
 'conversion(y_conv,sev<5)':(['ifs','digitos_atras','edad','educacion','sev_ord'],'y_conv',F.sev_ord<5)}

print("=== COBERTURA candidatos ===")
for c in CAND: print(f"  {c:16s} {100*F[c].notna().mean():.0f}%")
print("\n=== COLINEALIDAD memoria (r) ===")
print(F[['mr_diferido','rey_diferido','rey_trial1','mr_inmediato']].corr().round(2).to_string())

for name,(cur,ycol,mask) in CURRENT.items():
    d=F[mask].dropna(subset=[ycol]).copy(); y=d[ycol].astype(int).values
    cand=[c for c in ALLF if c!=ycol]
    a_cur=auc(cur,d,y); best_set,a_best=forward(d,y,cand)
    print(f"\n### {name}  n={len(y)} ev={int(y.sum())}")
    print(f"  ACTUAL  {cur}  → AUC={a_cur:.3f}")
    print(f"  FORWARD {best_set}  → AUC={a_best:.3f}")
    # univariate top5
    uni=sorted([(auc([c],d,y),c) for c in cand if d[c].notna().sum()>len(y)*0.7],reverse=True)[:5]
    print("  Top univariado:", [(c,round(a,2)) for a,c in uni])
