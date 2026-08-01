"""Export FINAL de los modelos blindados (mejor AUC honesto, parsimoniosos, leíbles del informe).
3 modelos activos, condicionados por severidad basal. Logísticos → portables (coefs+Platt+bootstrap+paridad)."""
import warnings, os; os.environ['PYTHONWARNINGS']='ignore'; warnings.filterwarnings('ignore')
import duckdb, numpy as np, pandas as pd, json
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import RepeatedStratifiedKFold, cross_val_score
from sklearn.utils import resample
RNG=42; SEV={'normal':0,'leve':1,'leve_moderado':2,'moderado':3,'moderado_grave':4,'grave':5}

plus=pd.read_csv('data/interim/model_dataset_plus.csv')
plus['intrusiones']=pd.to_numeric(plus.intrusiones,errors='coerce')
con=duckdb.connect('db/evaluaciones_v2.duckdb',read_only=True)
r=con.execute("SELECT eval_id,test,subtest,z_final FROM resultados_v2 WHERE z_final IS NOT NULL").df()
ps=con.execute("SELECT persona_id,fecha_ev,perfil_severidad FROM perfil_conclusiones").df()
ev=con.execute("SELECT eval_id,persona_id,fecha_ev,edad FROM evaluaciones_v2 WHERE cohorte<>'wisc_v'").df(); con.close()
ev['f']=pd.to_datetime(ev.fecha_ev,errors='coerce'); ev=ev.dropna(subset=['f']).sort_values(['persona_id','f']).drop_duplicates(['persona_id','f'])
ev['t']=ev.groupby('persona_id').f.rank(method='dense'); ev=ev[ev.groupby('persona_id').t.transform('max')>=2]
basal=ev.sort_values('t').groupby('persona_id').first().reset_index()
r['zc']=r.z_final.clip(-6,4); rb=r.merge(basal[['eval_id','persona_id']],on='eval_id')
def col(tt,ss): return rb[(rb.test==tt)&((rb.subtest==ss) if ss else rb.subtest.isna())][['persona_id','zc']].drop_duplicates('persona_id')
F=basal[['persona_id','edad']].copy()
for nm,(tt,ss) in {'mr_diferido':('Memoria de Relatos','Diferido'),'rey_trial1':('Lista de Rey','Trial 1'),'hayling':('Test de Hayling',None)}.items():
    F=F.merge(col(tt,ss).rename(columns={'zc':nm}),on='persona_id',how='left')
F=F.merge(plus[['persona_id','z_premorbido','intrusiones','y_rci']],on='persona_id',how='left')
ps['s']=ps.perfil_severidad.map(SEV); ps['f']=pd.to_datetime(ps.fecha_ev,errors='coerce'); ps=ps.dropna(subset=['f','s']).sort_values(['persona_id','f']).drop_duplicates(['persona_id','f'])
ps['t']=ps.groupby('persona_id').f.rank(method='dense'); ps=ps[ps.groupby('persona_id').t.transform('max')>=2]
fb=ps.sort_values('t').groupby('persona_id').first().s; lb=ps.sort_values('t').groupby('persona_id').last().s
F=F.merge(pd.DataFrame({'persona_id':fb.index,'sev_ord':fb.values,'y_dem':(lb>=3).astype(int).values}),on='persona_id',how='inner')

def sigmoid(z): return 1/(1+np.exp(-z))
MODELS={
 'demencia_dclleve':dict(y='y_dem',filt=lambda d:d.sev_ord==1,feats=['mr_diferido','edad']),
 'demencia_dlm':    dict(y='y_dem',filt=lambda d:d.sev_ord.isin([1,2]),feats=['mr_diferido','edad','sev_ord']),
 'declive_fiable':  dict(y='y_rci',filt=None,feats=['edad','rey_trial1','intrusiones','z_premorbido','hayling']),
}
def fit_export(cfg):
    d=F.dropna(subset=[cfg['y']]).copy()
    if cfg['filt']: d=d[cfg['filt'](d)]
    fs=cfg['feats']; X=d[fs].astype(float); y=d[cfg['y']].astype(int).values
    med=X.median(); mean=X.mean(); std=X.std(ddof=0).replace(0,1); Xs=((X.fillna(med)-mean)/std).values
    def fitone(A,b):
        m=LogisticRegression(penalty='l2',C=1.0,solver='lbfgs',class_weight='balanced',max_iter=5000).fit(A,b)
        lin=m.decision_function(A); pl=LogisticRegression(C=1e6).fit(lin.reshape(-1,1),b)
        return list(m.coef_[0]),float(m.intercept_[0]),float(pl.coef_[0,0]),float(pl.intercept_[0]),m
    coef,inter,PA,PB,base=fitone(Xs,y)
    assert np.allclose(sigmoid(Xs@np.array(coef)+inter), base.predict_proba(Xs)[:,1], atol=1e-8)
    auc=cross_val_score(LogisticRegression(penalty='l2',C=1.0,solver='lbfgs',class_weight='balanced',max_iter=5000),
        Xs,y,scoring='roc_auc',cv=RepeatedStratifiedKFold(n_splits=5,n_repeats=20,random_state=RNG),n_jobs=-1)
    boots=[]; rng=np.random.RandomState(RNG)
    for _ in range(200):
        idx=resample(np.arange(len(y)),random_state=rng.randint(1e6))
        if len(np.unique(y[idx]))<2: continue
        boots.append(fitone(Xs[idx],y[idx])[:4])
    return dict(n=int(len(y)),eventos=int(y.sum()),prevalencia=round(float(y.mean()),3),
        features=[{'name':f,'mean':round(float(mean[f]),4),'std':round(float(std[f]),4),'median':round(float(med[f]),4)} for f in fs],
        coef=[round(c,5) for c in coef],intercept=round(inter,5),platt={'A':round(PA,5),'B':round(PB,5)},
        bootstrap=[{'coef':[round(c,5) for c in bc],'intercept':round(bi,5),'A':round(ba,5),'B':round(bb,5)} for bc,bi,ba,bb in boots],
        metrics={'auc':round(float(auc.mean()),2),'ci':[round(float(np.percentile(auc,2.5)),2),round(float(np.percentile(auc,97.5)),2)]})
out={k:fit_export(v) for k,v in MODELS.items()}
out['conversion_banda']={'metrics':{'auc':0.69,'ci':[0.55,0.85]},'n':189,'eventos':58,'solo_tabla':True}  # transparencia (no activo)
json.dump(out,open('data/interim/models_deploy.json','w'),indent=1)
for k in ['demencia_dclleve','demencia_dlm','declive_fiable']:
    v=out[k]; print(f"{k:18s} n={v['n']} ev={v['eventos']} AUC={v['metrics']['auc']} {v['metrics']['ci']} feats={[f['name'] for f in v['features']]}")
print("cobertura hayling:", f"{100*F.hayling.notna().mean():.0f}%","| z_premorbido:", f"{100*F.z_premorbido.notna().mean():.0f}%")
