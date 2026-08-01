"""Exporta los modelos logísticos deployables a JSON para la calculadora client-side.
Por modelo: preprocesamiento (media/desvío por feature), coeficientes, calibración Platt,
y 200 bootstraps (banda de incertidumbre por paciente). Verifica que la matemática manual
(la que reimplementa el JS) reproduce a sklearn."""
import warnings, os; os.environ['PYTHONWARNINGS']='ignore'; warnings.filterwarnings('ignore')
import duckdb, numpy as np, pandas as pd, json
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
from sklearn.utils import resample
RNG=42

df=pd.read_csv('data/interim/model_dataset_plus.csv')
SEV={'normal':0,'leve':1,'leve_moderado':2,'moderado':3,'moderado_grave':4,'grave':5}
df['sev_ord']=df.perfil_severidad.map(SEV)
df['almac_bin']=df.mem_almacenamiento.map({'comprometido':1,'conservado':0})  # na→imputa
con=duckdb.connect('db/evaluaciones_v2.duckdb',read_only=True)
ps=con.execute("SELECT persona_id,fecha_ev,perfil_severidad FROM perfil_conclusiones").df(); con.close()
ps['s']=ps.perfil_severidad.map(SEV); ps['f']=pd.to_datetime(ps.fecha_ev,errors='coerce')
ps=ps.dropna(subset=['f','s']).sort_values(['persona_id','f']).drop_duplicates(['persona_id','f'])
ps['t']=ps.groupby('persona_id').f.rank(method='dense'); ps=ps[ps.groupby('persona_id').t.transform('max')>=2]
fb=ps.sort_values('t').groupby('persona_id').first().s; lb=ps.sort_values('t').groupby('persona_id').last().s
dem=pd.DataFrame({'persona_id':fb.index,'sev_basal_p':fb.values,'y_dem':(lb>=3).astype(int).values})
df=df.merge(dem,on='persona_id',how='left')

def sigmoid(z): return 1/(1+np.exp(-z))

# modelos deployables (todos logísticos = portables). basico/avanzado marcado.
MODELS={
 'demencia_predem': dict(y='y_dem', filt=lambda d:d.sev_basal_p<=2,
     feats=['z_memoria','z_gz','edad','educacion','sev_ord'], nivel='basico',
     titulo='Progresión a demencia · pre-demencia', desc='Riesgo de que un paciente sin demencia (normal/DCL leve/leve-moderado) progrese a demencia (~2 años).'),
 'demencia_dclleve': dict(y='y_dem', filt=lambda d:d.sev_basal_p==1,
     feats=['z_memoria','z_gz','edad','dprime','almac_bin'], nivel='avanzado',
     titulo='Progresión a demencia · DCL leve', desc='Riesgo de que un DCL leve progrese a demencia (~2 años). Firma amnésica.'),
 'declive_fiable': dict(y='y_rci', filt=None,
     feats=['z_memoria','z_gz','edad','z_atencion'], nivel='basico',
     titulo='Declive cognitivo fiable', desc='Riesgo de un declive cognitivo real (índice de cambio fiable) en la próxima reevaluación.'),
 'conversion_banda': dict(y='y_conv', filt=lambda d:d.sev_ord<5,
     feats=['z_atencion','z_gz','edad','educacion','sev_ord'], nivel='basico',
     titulo='Conversión de banda de severidad', desc='Riesgo de que la severidad del perfil empeore ≥1 banda. (Modelo más débil.)'),
}

def fit_export(cfg):
    d=df.dropna(subset=[cfg['y']]).copy()
    if cfg['filt']: d=d[cfg['filt'](d)]
    feats=cfg['feats']; X=d[feats].astype(float); y=d[cfg['y']].astype(int).values
    med=X.median(); mean=X.mean(); std=X.std(ddof=0).replace(0,1)
    def prep(M): return ((M.fillna(med)-mean)/std).values
    Xs=prep(X)
    def fitone(Xs_,y_):
        m=LogisticRegression(penalty='l1',solver='liblinear',C=0.3,class_weight='balanced',max_iter=5000).fit(Xs_,y_)
        lin=m.decision_function(Xs_)
        pl=LogisticRegression(C=1e6,solver='lbfgs').fit(lin.reshape(-1,1),y_)  # Platt
        return list(m.coef_[0]), float(m.intercept_[0]), float(pl.coef_[0,0]), float(pl.intercept_[0]), m
    coef,inter,A,B,base=fitone(Xs,y)
    # verificación de PARIDAD: la matemática que reimplementa el JS (sigmoid(X·coef+inter))
    # reproduce exactamente a sklearn.predict_proba del MISMO modelo.
    lin_manual=Xs@np.array(coef)+inter
    assert np.allclose(sigmoid(lin_manual), base.predict_proba(Xs)[:,1], atol=1e-8), "PARIDAD FALLA"
    # bootstrap 200 (coefs + Platt) para banda de incertidumbre
    boots=[]; rng=np.random.RandomState(RNG)
    for _ in range(200):
        idx=resample(np.arange(len(y)),random_state=rng.randint(1e6))
        if len(np.unique(y[idx]))<2: continue
        boots.append(fitone(Xs[idx],y[idx])[:4])
    # AUC OOF calibrado (para metadata) — rápido: apparent Platt
    p_cal=sigmoid(A*lin_manual+B)
    return dict(titulo=cfg['titulo'], desc=cfg['desc'], nivel=cfg['nivel'], y=cfg['y'],
                n=int(len(y)), eventos=int(y.sum()), prevalencia=round(float(y.mean()),3),
                features=[{'name':f,'mean':round(float(mean[f]),4),'std':round(float(std[f]),4),'median':round(float(med[f]),4)} for f in feats],
                coef=[round(c,5) for c in coef], intercept=round(inter,5),
                platt={'A':round(A,5),'B':round(B,5)},
                bootstrap=[{'coef':[round(c,5) for c in bc],'intercept':round(bi,5),'A':round(ba,5),'B':round(bb,5)} for bc,bi,ba,bb in boots])

out={k:fit_export(v) for k,v in MODELS.items()}
# métricas honestas (del análisis final, hardcode desde model_final/deep)
AUCS={'demencia_predem':{'auc':0.77,'ci':[0.60,0.93]},'demencia_dclleve':{'auc':0.85,'ci':[0.65,0.98]},
      'declive_fiable':{'auc':0.73,'ci':[0.55,0.82]},'conversion_banda':{'auc':0.66,'ci':[0.53,0.81]}}
for k in out: out[k]['metrics']=AUCS[k]
json.dump(out, open('data/interim/models_deploy.json','w'), indent=1)
print("Exportado data/interim/models_deploy.json — modelos:", list(out.keys()))
for k,v in out.items(): print(f"  {k:18s} n={v['n']} ev={v['eventos']} feats={len(v['features'])} boots={len(v['bootstrap'])} AUC={v['metrics']['auc']}")
print("Verificación matemática manual==sklearn: OK")
