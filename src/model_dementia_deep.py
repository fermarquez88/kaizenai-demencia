"""Profundización del modelo de progresión a demencia: LOOCV, decision-curve, estabilidad de
features (L1 bootstrap), learning curve, y coeficientes interpretables (odds ratios)."""
import warnings, os; os.environ['PYTHONWARNINGS']='ignore'; warnings.filterwarnings('ignore')
import duckdb, numpy as np, pandas as pd
from sklearn.model_selection import LeaveOneOut, cross_val_predict, StratifiedKFold
from sklearn.metrics import roc_auc_score
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.utils import resample
RNG=42

df=pd.read_csv('data/interim/model_dataset_plus.csv')
SEV={'normal':0,'leve':1,'leve_moderado':2,'moderado':3,'moderado_grave':4,'grave':5}
df['sev_ord']=df.perfil_severidad.map(SEV)
con=duckdb.connect('db/evaluaciones_v2.duckdb',read_only=True)
ps=con.execute("SELECT persona_id,fecha_ev,perfil_severidad FROM perfil_conclusiones").df(); con.close()
ps['s']=ps.perfil_severidad.map(SEV); ps['f']=pd.to_datetime(ps.fecha_ev,errors='coerce')
ps=ps.dropna(subset=['f','s']).sort_values(['persona_id','f']).drop_duplicates(['persona_id','f'])
ps['t']=ps.groupby('persona_id').f.rank(method='dense'); ps=ps[ps.groupby('persona_id').t.transform('max')>=2]
fb=ps.sort_values('t').groupby('persona_id').first().s; lb=ps.sort_values('t').groupby('persona_id').last().s
dem=pd.DataFrame({'persona_id':fb.index,'sev_basal_p':fb.values,'y_dem':(lb>=3).astype(int).values})
df=df.merge(dem,on='persona_id',how='left')

CAT=['mem_almacenamiento']
def make_pre(cols):
    cat=[c for c in cols if c in CAT]; num=[c for c in cols if c not in CAT]
    return ColumnTransformer([('n',Pipeline([('i',SimpleImputer(strategy='median',add_indicator=True)),('s',StandardScaler())]),num),
                              ('c',Pipeline([('i',SimpleImputer(strategy='most_frequent')),('o',OneHotEncoder(handle_unknown='ignore'))]),cat)])
def mk(cols): return Pipeline([('pre',make_pre(cols)),('m',LogisticRegression(penalty='l1',solver='liblinear',C=0.3,class_weight='balanced',max_iter=4000))])

def dca(y,p,thr):
    N=len(y); out=[]
    for t in thr:
        pred=p>=t; tp=np.sum(pred&(y==1)); fp=np.sum(pred&(y==0))
        out.append((t, tp/N-fp/N*(t/(1-t)), y.mean()-(1-y.mean())*(t/(1-t))))
    return out

for NAME,filt,cols in [("DCL leve → demencia", df.sev_basal_p==1, ['z_memoria','dprime','edad','z_gz','mem_almacenamiento']),
                       ("pre-demencia → demencia", df.sev_basal_p<=2, ['z_memoria','z_gz','edad','educacion','sev_ord'])]:
    d=df[filt].dropna(subset=['y_dem']).reset_index(drop=True); y=d.y_dem.astype(int).values; X=d[cols]
    print(f"\n{'='*66}\n{NAME}  (n={len(y)}, eventos={int(y.sum())})")
    # LOOCV
    P_loo=cross_val_predict(mk(cols),X,y,cv=LeaveOneOut(),method='predict_proba',n_jobs=-1)[:,1]
    print(f"  LOOCV AUC={roc_auc_score(y,P_loo):.3f}")
    # decision curve (OOF 5x)
    P=np.zeros(len(y))
    for r in range(10): P+=cross_val_predict(mk(cols),X,y,cv=StratifiedKFold(5,shuffle=True,random_state=RNG+r),method='predict_proba',n_jobs=-1)[:,1]
    P/=10
    print("  Decision-curve (net benefit modelo vs tratar-a-todos):")
    for t,nbm,nba in dca(y,P,[0.15,0.25,0.35]): print(f"    umbral {t:.2f}: modelo={nbm:+.3f}  tratar-todos={nba:+.3f}  {'✓ gana' if nbm>max(nba,0) else ''}")
    # estabilidad de features (L1 bootstrap: % coef != 0)
    sel={c:0 for c in cols}; B=200; rng=np.random.RandomState(RNG)
    for _ in range(B):
        idx=resample(np.arange(len(y)),random_state=rng.randint(1e6))
        if len(np.unique(y[idx]))<2: continue
        m=mk(cols).fit(X.iloc[idx],y[idx])
        coefs=m.named_steps['m'].coef_[0]
        names=m.named_steps['pre'].get_feature_names_out()
        for c in cols:
            if any((c in n) and abs(coefs[i])>1e-6 for i,n in enumerate(names)): sel[c]+=1
    print("  Estabilidad L1 (% bootstraps con coef≠0):", {c:f"{100*v/B:.0f}%" for c,v in sel.items()})
    # learning curve
    print("  Learning curve (AUC LOO por tamaño):", end=" ")
    for frac in [0.5,0.75,1.0]:
        n=int(len(y)*frac); sub=d.sample(n,random_state=RNG); ys=sub.y_dem.astype(int).values
        if ys.sum()<3: continue
        pl=cross_val_predict(mk(cols),sub[cols],ys,cv=LeaveOneOut(),method='predict_proba',n_jobs=-1)[:,1]
        print(f"n={n}:{roc_auc_score(ys,pl):.2f}", end="  ")
    print()
    # coeficientes interpretables (odds ratios) del modelo full
    m=mk(cols).fit(X,y); coefs=m.named_steps['m'].coef_[0]; names=m.named_steps['pre'].get_feature_names_out()
    ors={names[i].split('__')[-1]:round(np.exp(coefs[i]),2) for i in range(len(names)) if abs(coefs[i])>1e-6}
    print("  Odds ratios (por SD, modelo final):", dict(sorted(ors.items(),key=lambda x:-abs(np.log(x[1])))))
