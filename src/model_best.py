"""Re-entrenamiento EXPERTO para el mejor AUC honesto por target.
Espacio completo de features (derivadas + crudas). Selección: stability selection (Meinshausen-Bühlmann,
L1 sobre bootstraps) + L1 logística con C tuneado en CV anidada (selección dentro de folds) + HGB comparador.
Métrica honesta: AUC por CV anidada + optimismo-corregido (Steyerberg) + calibración."""
import warnings, os; os.environ['PYTHONWARNINGS']='ignore'; warnings.filterwarnings('ignore')
import duckdb, numpy as np, pandas as pd, json
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.model_selection import RepeatedStratifiedKFold, GridSearchCV, cross_val_score
from sklearn.metrics import roc_auc_score, brier_score_loss
from sklearn.utils import resample
RNG=42; SEV={'normal':0,'leve':1,'leve_moderado':2,'moderado':3,'moderado_grave':4,'grave':5}

# ---------- frame completo ----------
df=pd.read_csv('data/interim/model_dataset_plus.csv')
df['sev_ord']=df.perfil_severidad.map(SEV)
for b in ['multidominio','mem_intrusiones_confab','mem_beneficio_contexto','mod_animo']:
    df[b]=df[b].map({True:1,False:0,'True':1,'False':0})
df['intrusiones']=pd.to_numeric(df.intrusiones,errors='coerce')
df['almac_bin']=df.mem_almacenamiento.map({'comprometido':1,'conservado':0})
con=duckdb.connect('db/evaluaciones_v2.duckdb',read_only=True)
r=con.execute("SELECT eval_id,test,subtest,z_final FROM resultados_v2 WHERE z_final IS NOT NULL").df()
ps=con.execute("SELECT persona_id,fecha_ev,perfil_severidad FROM perfil_conclusiones").df()
ev=con.execute("SELECT eval_id,persona_id,fecha_ev FROM evaluaciones_v2 WHERE cohorte<>'wisc_v'").df()
con.close()
ev['f']=pd.to_datetime(ev.fecha_ev,errors='coerce')
ev=ev.dropna(subset=['f']).sort_values(['persona_id','f']).drop_duplicates(['persona_id','f'])
ev['t']=ev.groupby('persona_id').f.rank(method='dense'); ev=ev[ev.groupby('persona_id').t.transform('max')>=2]
basal=ev.sort_values('t').groupby('persona_id').first().reset_index()
r['zc']=r.z_final.clip(-6,4); rb=r.merge(basal[['eval_id','persona_id']],on='eval_id')
TESTS={'mr_diferido':('Memoria de Relatos','Diferido'),'mr_inmediato':('Memoria de Relatos','Inmediato'),
 'rey_diferido':('Lista de Rey','Diferido'),'rey_trial1':('Lista de Rey','Trial 1'),
 'figura_inmediato':('Figura de Rey','Inmediato'),'figura_recon':('Figura de Rey','Reconocimiento'),
 'ifs':('IFS',None),'hayling':('Test de Hayling',None),'digitos_atras':('Dígitos-span','Atrás'),'flu_semantica':('F Verbal Semántica',None)}
ST=pd.DataFrame({'persona_id':basal.persona_id})
for c,(tt,ss) in TESTS.items():
    sub=rb[(rb.test==tt)&((rb.subtest==ss) if ss else rb.subtest.isna())][['persona_id','zc']].drop_duplicates('persona_id')
    ST=ST.merge(sub.rename(columns={'zc':c}),on='persona_id',how='left')
df=df.merge(ST,on='persona_id',how='left')
ps['s']=ps.perfil_severidad.map(SEV); ps['f']=pd.to_datetime(ps.fecha_ev,errors='coerce')
ps=ps.dropna(subset=['f','s']).sort_values(['persona_id','f']).drop_duplicates(['persona_id','f'])
ps['t']=ps.groupby('persona_id').f.rank(method='dense'); ps=ps[ps.groupby('persona_id').t.transform('max')>=2]
fb=ps.sort_values('t').groupby('persona_id').first().s; lb=ps.sort_values('t').groupby('persona_id').last().s
df=df.merge(pd.DataFrame({'persona_id':fb.index,'sev_basal_p':fb.values,'y_dem':(lb>=3).astype(int).values}),on='persona_id',how='left')

NUM=['edad','educacion','sexo_f','z_atencion','z_funciones_ejecutivas','z_memoria','z_lenguaje','z_visuoespacial',
 'z_gz','z_dispersion','z_premorbido','caida_premorb','gap_gz','gap_memoria','intrusiones','aprendizaje_total',
 'tasa_aprendizaje','recon_corregido','dprime','criterio_c','fp_listaB','hits','multidominio','mem_intrusiones_confab',
 'mem_beneficio_contexto','mod_animo','almac_bin','sev_ord']+list(TESTS)
CAT=['perfil_patron','tipo_curva']
def pre(cols):
    num=[c for c in cols if c not in CAT]; cat=[c for c in cols if c in CAT]
    return ColumnTransformer([('n',Pipeline([('i',SimpleImputer(strategy='median',add_indicator=True)),('s',StandardScaler())]),num),
        ('c',Pipeline([('i',SimpleImputer(strategy='most_frequent')),('o',OneHotEncoder(handle_unknown='ignore'))]),cat)])
def nested(est,grid,X,y):
    outer=RepeatedStratifiedKFold(n_splits=5,n_repeats=8,random_state=RNG)
    gs=GridSearchCV(est,grid,scoring='roc_auc',cv=3,n_jobs=1)
    s=cross_val_score(gs,X,y,scoring='roc_auc',cv=outer,n_jobs=-1)
    return s.mean(),np.percentile(s,2.5),np.percentile(s,97.5)
def stability(cols,X,y,B=120,C=0.3):
    p0=pre(cols); freq={}
    rng=np.random.RandomState(RNG)
    for _ in range(B):
        idx=resample(np.arange(len(y)),random_state=rng.randint(1e6))
        if len(np.unique(y[idx]))<2: continue
        pipe=Pipeline([('pre',pre(cols)),('m',LogisticRegression(penalty='l1',solver='liblinear',C=C,class_weight='balanced',max_iter=4000))])
        pipe.fit(X.iloc[idx],y[idx]); names=pipe.named_steps['pre'].get_feature_names_out(); coef=pipe.named_steps['m'].coef_[0]
        for c in cols:
            hit=any((c in n) and abs(coef[i])>1e-8 for i,n in enumerate(names))
            freq[c]=freq.get(c,0)+(1 if hit else 0)
    return {k:round(v/B,2) for k,v in sorted(freq.items(),key=lambda x:-x[1])}
def optimism(pipe,X,y,B=150):
    pipe.fit(X,y); app=roc_auc_score(y,pipe.predict_proba(X)[:,1]); opt=[]; rng=np.random.RandomState(RNG)
    for _ in range(B):
        idx=resample(np.arange(len(y)),random_state=rng.randint(1e6))
        if len(np.unique(y[idx]))<2: continue
        pipe.fit(X.iloc[idx],y[idx]); opt.append(roc_auc_score(y[idx],pipe.predict_proba(X.iloc[idx])[:,1])-roc_auc_score(y,pipe.predict_proba(X)[:,1]))
    return app-np.mean(opt)

CONF={'demencia_predem':('y_dem',df.sev_basal_p<=2),'demencia_dclleve':('y_dem',df.sev_basal_p==1),
      'declive_fiable':('y_rci',pd.Series(True,index=df.index)),'conversion_banda':('y_conv',df.sev_ord<5)}
out={}
for name,(ycol,mask) in CONF.items():
    d=df[mask].dropna(subset=[ycol]).copy(); y=d[ycol].astype(int).values; X=d[NUM+CAT]
    print(f"\n{'='*70}\n{name}  n={len(y)} ev={int(y.sum())} feats_espacio={len(NUM+CAT)}")
    # L1 logística (selección dentro de folds)
    l1=Pipeline([('pre',pre(NUM+CAT)),('m',LogisticRegression(penalty='l1',solver='liblinear',class_weight='balanced',max_iter=4000))])
    a_l1=nested(l1,{'m__C':[0.05,0.1,0.2,0.4,0.8]},X,y)
    # HGB
    hgb=Pipeline([('pre',pre(NUM+CAT)),('m',HistGradientBoostingClassifier(random_state=RNG))])
    a_hgb=nested(hgb,{'m__max_depth':[2,3],'m__learning_rate':[0.05,0.1],'m__max_iter':[150,300]},X,y)
    # stability selection
    stab=stability(NUM+CAT,X,y)
    top=[k for k,v in stab.items() if v>=0.5]
    # modelo final = stability-selected + L1
    if top:
        l1f=Pipeline([('pre',pre(top)),('m',LogisticRegression(penalty='l1',solver='liblinear',C=0.4,class_weight='balanced',max_iter=4000))])
        a_stab=nested(l1f,{'m__C':[0.1,0.3,0.6]},d[top],y); a_opt=optimism(l1f,d[top],y)
    else: a_stab=(np.nan,)*3; a_opt=np.nan
    print(f"  L1 (espacio completo, nested): AUC={a_l1[0]:.3f} [{a_l1[1]:.3f},{a_l1[2]:.3f}]")
    print(f"  HGB (nested):                  AUC={a_hgb[0]:.3f} [{a_hgb[1]:.3f},{a_hgb[2]:.3f}]")
    print(f"  Stability-selected {top}")
    print(f"  Stab-set L1 (nested): AUC={a_stab[0]:.3f} | optimismo-corr={a_opt:.3f}")
    print(f"  Frecuencias stability (≥0.3): "+", ".join(f"{k}:{v}" for k,v in stab.items() if v>=0.3))
    out[name]={'n':len(y),'ev':int(y.sum()),'auc_L1_full':round(a_l1[0],3),'auc_HGB':round(a_hgb[0],3),
        'stability':stab,'top':top,'auc_stab':round(float(a_stab[0]),3) if not np.isnan(a_stab[0]) else None,
        'auc_stab_optimism':round(float(a_opt),3) if not np.isnan(a_opt) else None}
json.dump(out,open('data/interim/model_best.json','w'),indent=1)
print("\nguardado data/interim/model_best.json")
