"""Comparación LIMPIA: sets de features FIJOS a priori (sin selección data-driven → sin fuga),
evaluados con CV repetida honesta + optimismo-corregido. Clava el mejor AUC real por target."""
import warnings, os; os.environ['PYTHONWARNINGS']='ignore'; warnings.filterwarnings('ignore')
import duckdb, numpy as np, pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.model_selection import RepeatedStratifiedKFold, cross_val_score
from sklearn.metrics import roc_auc_score
from sklearn.utils import resample
RNG=42; SEV={'normal':0,'leve':1,'leve_moderado':2,'moderado':3,'moderado_grave':4,'grave':5}
# --- frame (idéntico a model_best) ---
df=pd.read_csv('data/interim/model_dataset_plus.csv'); df['sev_ord']=df.perfil_severidad.map(SEV)
df['intrusiones']=pd.to_numeric(df.intrusiones,errors='coerce'); df['almac_bin']=df.mem_almacenamiento.map({'comprometido':1,'conservado':0})
for b in ['mod_animo']: df[b]=df[b].map({True:1,False:0,'True':1,'False':0})
con=duckdb.connect('db/evaluaciones_v2.duckdb',read_only=True)
r=con.execute("SELECT eval_id,test,subtest,z_final FROM resultados_v2 WHERE z_final IS NOT NULL").df()
ps=con.execute("SELECT persona_id,fecha_ev,perfil_severidad FROM perfil_conclusiones").df()
ev=con.execute("SELECT eval_id,persona_id,fecha_ev FROM evaluaciones_v2 WHERE cohorte<>'wisc_v'").df(); con.close()
ev['f']=pd.to_datetime(ev.fecha_ev,errors='coerce'); ev=ev.dropna(subset=['f']).sort_values(['persona_id','f']).drop_duplicates(['persona_id','f'])
ev['t']=ev.groupby('persona_id').f.rank(method='dense'); ev=ev[ev.groupby('persona_id').t.transform('max')>=2]
basal=ev.sort_values('t').groupby('persona_id').first().reset_index()
r['zc']=r.z_final.clip(-6,4); rb=r.merge(basal[['eval_id','persona_id']],on='eval_id')
TESTS={'mr_diferido':('Memoria de Relatos','Diferido'),'mr_inmediato':('Memoria de Relatos','Inmediato'),'rey_diferido':('Lista de Rey','Diferido'),'rey_trial1':('Lista de Rey','Trial 1'),'figura_inmediato':('Figura de Rey','Inmediato'),'figura_recon':('Figura de Rey','Reconocimiento'),'ifs':('IFS',None),'hayling':('Test de Hayling',None),'digitos_atras':('Dígitos-span','Atrás')}
ST=pd.DataFrame({'persona_id':basal.persona_id})
for c,(tt,ss) in TESTS.items():
    sub=rb[(rb.test==tt)&((rb.subtest==ss) if ss else rb.subtest.isna())][['persona_id','zc']].drop_duplicates('persona_id'); ST=ST.merge(sub.rename(columns={'zc':c}),on='persona_id',how='left')
df=df.merge(ST,on='persona_id',how='left')
ps['s']=ps.perfil_severidad.map(SEV); ps['f']=pd.to_datetime(ps.fecha_ev,errors='coerce'); ps=ps.dropna(subset=['f','s']).sort_values(['persona_id','f']).drop_duplicates(['persona_id','f'])
ps['t']=ps.groupby('persona_id').f.rank(method='dense'); ps=ps[ps.groupby('persona_id').t.transform('max')>=2]
fb=ps.sort_values('t').groupby('persona_id').first().s; lb=ps.sort_values('t').groupby('persona_id').last().s
df=df.merge(pd.DataFrame({'persona_id':fb.index,'sev_basal_p':fb.values,'y_dem':(lb>=3).astype(int).values}),on='persona_id',how='left')

def evalset(cols,d,y,model='logit'):
    num=[c for c in cols if c!='perfil_patron']; cat=[c for c in cols if c=='perfil_patron']
    P=ColumnTransformer([('n',Pipeline([('i',SimpleImputer(strategy='median',add_indicator=True)),('s',StandardScaler())]),num)]+([('c',Pipeline([('i',SimpleImputer(strategy='most_frequent')),('o',OneHotEncoder(handle_unknown='ignore'))]),cat)] if cat else []))
    m=HistGradientBoostingClassifier(max_depth=3,max_iter=200,learning_rate=0.05,random_state=RNG) if model=='hgb' else LogisticRegression(penalty='l1',solver='liblinear',C=0.4,class_weight='balanced',max_iter=5000)
    pipe=Pipeline([('pre',P),('m',m)])
    s=cross_val_score(pipe,d[cols],y,scoring='roc_auc',cv=RepeatedStratifiedKFold(n_splits=5,n_repeats=20,random_state=RNG),n_jobs=-1)
    # optimismo
    pipe.fit(d[cols],y); app=roc_auc_score(y,pipe.predict_proba(d[cols])[:,1]); opt=[]; rng=np.random.RandomState(RNG)
    for _ in range(120):
        idx=resample(np.arange(len(y)),random_state=rng.randint(1e6))
        if len(np.unique(y[idx]))<2: continue
        pipe.fit(d[cols].iloc[idx],y[idx]); opt.append(roc_auc_score(y[idx],pipe.predict_proba(d[cols].iloc[idx])[:,1])-roc_auc_score(y,pipe.predict_proba(d[cols])[:,1]))
    return s.mean(),np.percentile(s,2.5),np.percentile(s,97.5),app-np.mean(opt)

CAND={
 'demencia_predem':(df.sev_basal_p<=2,'y_dem',{
    'derived':['z_memoria','z_gz','edad','educacion','sev_ord'],
    'tabla':['mr_diferido','rey_diferido','ifs','edad','sev_ord'],
    'compacto':['edad','mr_diferido','sev_ord'],
    'stability':['edad','mr_diferido','z_memoria','sev_ord','hayling']}),
 'demencia_dclleve':(df.sev_basal_p==1,'y_dem',{
    'derived':['z_memoria','z_gz','edad','dprime','almac_bin'],
    'tabla':['mr_diferido','rey_diferido','ifs','edad'],
    'minimo':['mr_diferido','edad'],
    'stability':['edad','mr_diferido','z_memoria','z_premorbido','criterio_c']}),
 'declive_fiable':(pd.Series(True,index=df.index),'y_rci',{
    'derived':['z_memoria','z_gz','edad','z_atencion'],
    'stability':['edad','rey_trial1','intrusiones','z_premorbido','hayling']}),
 'conversion_banda':(df.sev_ord<5,'y_conv',{
    'derived_hgb':['z_atencion','z_gz','edad','sev_ord'],
    'stability_hgb':['edad','figura_inmediato','sev_ord','z_premorbido','ifs']}),
}
for name,(mask,ycol,sets) in CAND.items():
    d=df[mask].dropna(subset=[ycol]).copy(); y=d[ycol].astype(int).values
    print(f"\n{'='*66}\n{name}  n={len(y)} ev={int(y.sum())}")
    best=None
    for sn,cols in sets.items():
        mdl='hgb' if 'hgb' in sn else 'logit'
        cv,lo,hi,opt=evalset(cols,d,y,mdl)
        print(f"  {sn:14s} AUC={cv:.3f} [{lo:.3f},{hi:.3f}]  optimismo-corr={opt:.3f}  ({mdl}, {len(cols)} feats)")
        if best is None or cv>best[1]: best=(sn,cv)
    print(f"  → mejor honesto: {best[0]} (AUC {best[1]:.3f})")
