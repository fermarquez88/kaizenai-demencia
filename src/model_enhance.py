"""Experimento aumentado: ¿suben el AUC las features nuevas? (RAVLT d'/criterio, ADLQ, gap normativo).
Comparación honesta base-vs-plus con CV anidada + bootstrap de la diferencia sobre OOF."""
import warnings, os; os.environ['PYTHONWARNINGS']='ignore'; warnings.filterwarnings('ignore')
import numpy as np, pandas as pd
from sklearn.model_selection import RepeatedStratifiedKFold, StratifiedKFold, GridSearchCV, cross_val_score, cross_val_predict
from sklearn.metrics import roc_auc_score
from sklearn.pipeline import Pipeline
from model_experiment import make_pre, clf_models, FE

RNG=42
df = pd.read_csv('data/interim/model_dataset_plus.csv')
SEV={'normal':0,'leve':1,'leve_moderado':2,'moderado':3,'moderado_grave':4,'grave':5}
df['sev_ord']=df.perfil_severidad.map(SEV)
for b in ['multidominio','mem_intrusiones_confab','mem_beneficio_contexto','mod_animo','mod_sueno','mod_ansiedad','mod_sensorial']:
    df[b]=df[b].map({True:1,False:0,'True':1,'False':0})

RECOG=['dprime','criterio_c','fp_listaB','confab','hits']
GAPS=['gap_gz','gap_memoria','adlq_pct']
SETS={
 'proceso_base': FE['C_proceso'],
 'proceso_plus': FE['C_proceso']+RECOG,
 'full_base':    FE['B_full'],
 'full_plus':    FE['B_full']+RECOG+GAPS,
}

def nested_auc(cols, y, X):
    outer=RepeatedStratifiedKFold(n_splits=5,n_repeats=5,random_state=RNG)
    est,grid=clf_models()[MODEL]
    pipe=Pipeline([('pre',make_pre(cols)),('m',est)])
    model=GridSearchCV(pipe,grid,scoring='roc_auc',cv=3,n_jobs=1) if grid else pipe
    s=cross_val_score(model,X,y,scoring='roc_auc',cv=outer,n_jobs=-1)
    return s.mean(), np.percentile(s,2.5), np.percentile(s,97.5)

def oof(cols, y, X, R=4):
    est,grid=clf_models()[MODEL]
    pipe=Pipeline([('pre',make_pre(cols)),('m',est)])
    mdl=GridSearchCV(pipe,grid,scoring='roc_auc',cv=3,n_jobs=1) if grid else pipe
    P=np.zeros(len(y))
    for r in range(R):
        P+=cross_val_predict(mdl,X,y,cv=StratifiedKFold(5,shuffle=True,random_state=RNG+r),method='predict_proba',n_jobs=-1)[:,1]
    return P/R

def compare(target, base_key, plus_key, exc=False):
    d=df.dropna(subset=[target]).copy()
    if exc: d=d[d.sev_ord<5]
    y=d[target].astype(int).values
    print(f"\n### {target}  ({MODEL})  n={len(y)} eventos={int(y.sum())}")
    for key in [base_key, plus_key]:
        cols=SETS[key]; m,lo,hi=nested_auc(cols,y,d[cols])
        print(f"  {key:14s} AUC={m:.3f} [{lo:.3f},{hi:.3f}]  ({len(cols)} feats)")
    # bootstrap Δ sobre OOF
    Pb=oof(SETS[base_key],y,d[SETS[base_key]]); Pp=oof(SETS[plus_key],y,d[SETS[plus_key]])
    rng=np.random.RandomState(RNG); diffs=[]
    for _ in range(2000):
        i=rng.randint(0,len(y),len(y))
        if len(np.unique(y[i]))<2: continue
        diffs.append(roc_auc_score(y[i],Pp[i])-roc_auc_score(y[i],Pb[i]))
    print(f"  OOF: base={roc_auc_score(y,Pb):.3f}  plus={roc_auc_score(y,Pp):.3f}  "
          f"Δ={np.mean(diffs):+.3f} IC[{np.percentile(diffs,2.5):+.3f},{np.percentile(diffs,97.5):+.3f}]  P(Δ>0)={np.mean(np.array(diffs)>0):.2f}")

if __name__=='__main__':
    global MODEL
    MODEL='logit_en'
    print("="*70,"\nDECLIVE FIABLE GLOBAL — ¿RAVLT reconocimiento ayuda?")
    compare('y_rci','proceso_base','proceso_plus')
    print("\n"+"="*70,"\nDECLIVE MEMORIA-ESPECÍFICO (sub-potenciado, 17 eventos)")
    compare('y_rci_mem','proceso_base','proceso_plus')
    MODEL='rf'
    print("\n"+"="*70,"\nCONVERSIÓN — ¿ADLQ + gaps + recon ayudan? (Random Forest)")
    compare('y_conv','full_base','full_plus',exc=True)
