"""Modelo de progresión a DEMENCIA (severidad moderado+) desde estado pre-demencia.
Cohortes: DCL leve (primario, pedido) y pre-demencia amplia (companion, mejor potenciado).
EPV muy bajo → ultra-parsimonioso, regularización fuerte, CV repetida, IC bootstrap. Honesto."""
import warnings, os; os.environ['PYTHONWARNINGS']='ignore'; warnings.filterwarnings('ignore')
import duckdb, numpy as np, pandas as pd
from sklearn.model_selection import RepeatedStratifiedKFold, StratifiedKFold, cross_val_score, cross_val_predict
from sklearn.metrics import roc_auc_score, brier_score_loss
from sklearn.calibration import calibration_curve
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.dummy import DummyClassifier
from sklearn.inspection import permutation_importance
RNG=42

# --- target: severidad final >= moderado (demencia) ---
con=duckdb.connect('db/evaluaciones_v2.duckdb',read_only=True)
ps=con.execute("SELECT persona_id, fecha_ev, perfil_severidad FROM perfil_conclusiones").df(); con.close()
SEV={'normal':0,'leve':1,'leve_moderado':2,'moderado':3,'moderado_grave':4,'grave':5,'no_concluyente':None}
ps['s']=ps.perfil_severidad.map(SEV); ps['fecha']=pd.to_datetime(ps.fecha_ev,errors='coerce')
ps=ps.dropna(subset=['fecha','s']).sort_values(['persona_id','fecha']).drop_duplicates(['persona_id','fecha'])
ps['t']=ps.groupby('persona_id').fecha.rank(method='dense'); nt=ps.groupby('persona_id').t.transform('max')
ps=ps[nt>=2]
f=ps.sort_values('t').groupby('persona_id').first(); l=ps.sort_values('t').groupby('persona_id').last()
tg=pd.DataFrame({'persona_id':f.index,'sev_basal':f.s.values,'y_dem':(l.s>=3).astype(int).values})

feat=pd.read_csv('data/interim/model_dataset_plus.csv')
d=tg.merge(feat, on='persona_id', how='inner')

CAT=['mem_almacenamiento']
FSETS={
 'amnesica':   ['z_memoria','dprime','mem_almacenamiento','intrusiones'],
 'clinica':    ['z_memoria','z_gz','edad','educacion'],
 'combinada':  ['z_memoria','dprime','edad','z_gz','mem_almacenamiento'],
}
def pre(cols):
    num=[c for c in cols if c not in CAT]; cat=[c for c in cols if c in CAT]
    return ColumnTransformer([('n',Pipeline([('i',SimpleImputer(strategy='median',add_indicator=True)),('s',StandardScaler())]),num),
                              ('c',Pipeline([('i',SimpleImputer(strategy='most_frequent')),('o',OneHotEncoder(handle_unknown='ignore'))]),cat)])
def model(cols):  # logística L1 fuerte (EPV bajo → sin tuning, regularización fija)
    return Pipeline([('pre',pre(cols)),('m',LogisticRegression(penalty='l1',solver='liblinear',C=0.2,class_weight='balanced',max_iter=3000))])

def evaluate(name, sub):
    y=sub.y_dem.values
    print(f"\n{'='*64}\n{name}: n={len(y)}  eventos(demencia)={int(y.sum())} ({100*y.mean():.0f}%)")
    outer=RepeatedStratifiedKFold(n_splits=5,n_repeats=20,random_state=RNG)
    # baseline: solo severidad basal + edad (referencia trivial)
    for fn,cols in list(FSETS.items())+[('_baseline_dummy',None)]:
        if cols is None:
            s=cross_val_score(DummyClassifier(strategy='prior'), sub[['edad']], y, scoring='roc_auc', cv=outer, n_jobs=-1)
        else:
            s=cross_val_score(model(cols), sub[cols], y, scoring='roc_auc', cv=outer, n_jobs=-1)
        print(f"  {fn:16s} AUC={s.mean():.3f} [{np.percentile(s,2.5):.3f},{np.percentile(s,97.5):.3f}]")
    # champion = mejor FSET; OOF + bootstrap + calibración + importancia
    best=max(FSETS, key=lambda k: cross_val_score(model(FSETS[k]),sub[FSETS[k]],y,scoring='roc_auc',cv=outer,n_jobs=-1).mean())
    cols=FSETS[best]
    P=np.zeros(len(y))
    for r in range(10):
        P+=cross_val_predict(model(cols),sub[cols],y,cv=StratifiedKFold(5,shuffle=True,random_state=RNG+r),method='predict_proba',n_jobs=-1)[:,1]
    P/=10
    rng=np.random.RandomState(RNG); au=[]
    for _ in range(3000):
        i=rng.randint(0,len(y),len(y))
        if len(np.unique(y[i]))>1: au.append(roc_auc_score(y[i],P[i]))
    frac,mp=calibration_curve(y,P,n_bins=4,strategy='quantile')
    print(f"  → champion={best} ({cols})")
    print(f"    OOF AUC={roc_auc_score(y,P):.3f} IC95%=[{np.percentile(au,2.5):.3f},{np.percentile(au,97.5):.3f}]  Brier={brier_score_loss(y,P):.3f}")
    print(f"    calibración pred/obs: {[f'{a:.2f}/{b:.2f}' for a,b in zip(mp,frac)]}")
    # importancia permutación (5-fold)
    imp={}; skf=StratifiedKFold(5,shuffle=True,random_state=RNG); Xc=sub[cols].reset_index(drop=True)
    for tr,te in skf.split(Xc,y):
        m=model(cols).fit(Xc.iloc[tr],y[tr])
        pi=permutation_importance(m,Xc.iloc[te],y[te],scoring='roc_auc',n_repeats=10,random_state=RNG)
        for c,v in zip(cols,pi.importances_mean): imp.setdefault(c,[]).append(v)
    print("    importancia (ΔAUC):", {c:round(np.mean(v),3) for c,v in sorted(imp.items(),key=lambda x:-np.mean(x[1]))})
    return best, roc_auc_score(y,P)

if __name__=='__main__':
    evaluate("DCL LEVE → demencia (PRIMARIO, pedido)", d[d.sev_basal==1])
    evaluate("PRE-DEMENCIA (normal/leve/leve-mod) → demencia (companion)", d[d.sev_basal<=2])
