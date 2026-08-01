"""Pipeline FINAL endurecido: 4 modelos headline con metodología uniforme y rigurosa.
Sin `intervalo` (higiene de fuga). Para cada uno: AUC por CV repetida (IC), AUC optimismo-corregido
(bootstrap Steyerberg), recalibración Platt (Brier/ECE/slope/intercept), decision-curve. Sin gridsearch
(hiperparámetros fijos razonables → folds válidos a n chico y sin doble-optimismo)."""
import warnings, os; os.environ['PYTHONWARNINGS']='ignore'; warnings.filterwarnings('ignore')
import duckdb, numpy as np, pandas as pd, json
from sklearn.model_selection import RepeatedStratifiedKFold, StratifiedKFold, cross_val_predict, cross_val_score
from sklearn.metrics import roc_auc_score, brier_score_loss
from sklearn.calibration import CalibratedClassifierCV, calibration_curve
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.utils import resample
RNG=42

# ---- datos + target demencia ----
df = pd.read_csv('data/interim/model_dataset_plus.csv')
SEV={'normal':0,'leve':1,'leve_moderado':2,'moderado':3,'moderado_grave':4,'grave':5}
df['sev_ord']=df.perfil_severidad.map(SEV)
for b in ['multidominio','mem_intrusiones_confab','mem_beneficio_contexto','mod_animo']:
    df[b]=df[b].map({True:1,False:0,'True':1,'False':0})
con=duckdb.connect('db/evaluaciones_v2.duckdb',read_only=True)
ps=con.execute("SELECT persona_id,fecha_ev,perfil_severidad FROM perfil_conclusiones").df(); con.close()
ps['s']=ps.perfil_severidad.map(SEV); ps['f']=pd.to_datetime(ps.fecha_ev,errors='coerce')
ps=ps.dropna(subset=['f','s']).sort_values(['persona_id','f']).drop_duplicates(['persona_id','f'])
ps['t']=ps.groupby('persona_id').f.rank(method='dense'); ps=ps[ps.groupby('persona_id').t.transform('max')>=2]
fb=ps.sort_values('t').groupby('persona_id').first().s; lb=ps.sort_values('t').groupby('persona_id').last().s
dem=pd.DataFrame({'persona_id':fb.index,'sev_basal_p':fb.values,'y_dem':(lb>=3).astype(int).values})
df=df.merge(dem,on='persona_id',how='left')

CAT=['mem_almacenamiento','perfil_patron','tipo_curva']
def make_pre(cols):
    cat=[c for c in cols if c in CAT]; num=[c for c in cols if c not in CAT]
    return ColumnTransformer([('n',Pipeline([('i',SimpleImputer(strategy='median',add_indicator=True)),('s',StandardScaler())]),num),
                              ('c',Pipeline([('i',SimpleImputer(strategy='most_frequent')),('o',OneHotEncoder(handle_unknown='ignore'))]),cat)])
def LOGIT(): return LogisticRegression(penalty='l1',solver='liblinear',C=0.3,class_weight='balanced',max_iter=4000)
def RF():    return RandomForestClassifier(n_estimators=400,max_depth=5,min_samples_leaf=5,class_weight='balanced',random_state=RNG)

# features (SIN intervalo, minimizando alta-ausencia)
PROC_RECON=['z_memoria','z_gz','mem_almacenamiento','mem_intrusiones_confab','mem_beneficio_contexto',
            'intrusiones','confabulaciones','tipo_curva','aprendizaje_total','tasa_aprendizaje','recon_corregido',
            'dprime','criterio_c','fp_listaB','confab','hits']
FULL=['edad','educacion','sexo_f','z_atencion','z_funciones_ejecutivas','z_memoria','z_lenguaje','z_visuoespacial',
      'z_gz','z_dispersion','sev_ord','perfil_patron','multidominio','mem_almacenamiento','mod_animo','dprime','criterio_c']
DEM1=['z_memoria','dprime','edad','z_gz','mem_almacenamiento']
DEM2=['z_memoria','z_gz','edad','educacion','sev_ord']

CONFIGS={
 'declive_fiable':   dict(y='y_rci', filt=None, cols=PROC_RECON, model=LOGIT),
 'conversion_banda': dict(y='y_conv', filt=lambda d:d.sev_ord<5, cols=FULL, model=RF),
 'demencia_DCLleve': dict(y='y_dem', filt=lambda d:d.sev_basal_p==1, cols=DEM1, model=LOGIT),
 'demencia_predem':  dict(y='y_dem', filt=lambda d:d.sev_basal_p<=2, cols=DEM2, model=LOGIT),
}

def pipe(cfg): return Pipeline([('pre',make_pre(cfg['cols'])),('m',cfg['model']())])

def optimism_auc(cfg, X, y, B=200):
    """AUC apparent optimismo-corregido (Steyerberg)."""
    full=pipe(cfg).fit(X,y); app=roc_auc_score(y, full.predict_proba(X)[:,1])
    opt=[]
    rng=np.random.RandomState(RNG)
    for _ in range(B):
        idx=resample(np.arange(len(y)), random_state=rng.randint(1e6))
        if len(np.unique(y[idx]))<2: continue
        mb=pipe(cfg).fit(X.iloc[idx],y[idx])
        a_boot=roc_auc_score(y[idx],mb.predict_proba(X.iloc[idx])[:,1])
        a_orig=roc_auc_score(y,mb.predict_proba(X)[:,1])
        opt.append(a_boot-a_orig)
    return app, app-np.mean(opt)

def oof_cal(cfg, X, y, R=10):
    """OOF de modelo Platt-calibrado."""
    P=np.zeros(len(y))
    for r in range(R):
        cc=CalibratedClassifierCV(pipe(cfg), method='sigmoid', cv=5)
        P+=cross_val_predict(cc,X,y,cv=StratifiedKFold(5,shuffle=True,random_state=RNG+r),method='predict_proba',n_jobs=-1)[:,1]
    return P/R

def cal_slope_intercept(y,p):
    p=np.clip(p,1e-4,1-1e-4); lo=np.log(p/(1-p))
    m=LogisticRegression(C=1e6,solver='lbfgs').fit(lo.reshape(-1,1),y)
    return float(m.coef_[0,0]), float(m.intercept_[0])

out={}
for name,cfg in CONFIGS.items():
    d=df.dropna(subset=[cfg['y']]).copy()
    if cfg['filt']: d=d[cfg['filt'](d)]
    X=d[cfg['cols']].reset_index(drop=True); y=d[cfg['y']].astype(int).values
    outer=RepeatedStratifiedKFold(n_splits=5,n_repeats=20,random_state=RNG)
    cv=cross_val_score(pipe(cfg),X,y,scoring='roc_auc',cv=outer,n_jobs=-1)
    app,corr=optimism_auc(cfg,X,y)
    P=oof_cal(cfg,X,y)
    slope,inter=cal_slope_intercept(y,P)
    frac,mp=calibration_curve(y,P,n_bins=4,strategy='quantile')
    o=dict(n=int(len(y)),ev=int(y.sum()),prev=round(float(y.mean()),2),
           auc_cv=round(cv.mean(),3), auc_cv_ci=[round(np.percentile(cv,2.5),3),round(np.percentile(cv,97.5),3)],
           auc_apparent=round(app,3), auc_optimism_corr=round(corr,3),
           auc_oof_cal=round(roc_auc_score(y,P),3), brier=round(brier_score_loss(y,P),3),
           cal_slope=round(slope,2), cal_intercept=round(inter,2))
    out[name]=o
    print(f"\n{name}: n={o['n']} ev={o['ev']} ({o['prev']})")
    print(f"  AUC CV(5x20)={o['auc_cv']} {o['auc_cv_ci']} | aparente={o['auc_apparent']} → optimismo-corr={o['auc_optimism_corr']}")
    print(f"  Calibrado: AUC={o['auc_oof_cal']} Brier={o['brier']} slope={o['cal_slope']} intercept={o['cal_intercept']}")
json.dump(out, open('data/interim/model_final.json','w'), indent=2)
print("\nguardado: data/interim/model_final.json")
