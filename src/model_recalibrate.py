"""Recalibración de los modelos campeones (Platt/sigmoid e isotónica) y métricas finales.
El T1 sobre-predecía (class_weight balanced infla probas) → CalibratedClassifierCV lo corrige."""
import warnings, os; os.environ['PYTHONWARNINGS']='ignore'; warnings.filterwarnings('ignore')
import numpy as np, pandas as pd, json
from sklearn.model_selection import StratifiedKFold, cross_val_predict
from sklearn.calibration import CalibratedClassifierCV, calibration_curve
from sklearn.metrics import roc_auc_score, brier_score_loss
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from model_experiment import FE, make_pre, df

RNG=42
CHAMP = {  # (fe, estimador base con hiperparámetros razonables del tuning)
 'y_rci':  ('C_proceso', LogisticRegression(penalty='elasticnet', solver='saga', C=0.1, l1_ratio=0.5,
                                            max_iter=4000, tol=1e-3, class_weight='balanced')),
 'y_conv': ('B_full', RandomForestClassifier(n_estimators=400, max_depth=5, min_samples_leaf=5,
                                             class_weight='balanced', random_state=RNG)),
}

def oof(est, X, y, R=5):
    P=np.zeros(len(y))
    for r in range(R):
        P += cross_val_predict(est, X, y, cv=StratifiedKFold(5,shuffle=True,random_state=RNG+r),
                               method='predict_proba', n_jobs=-1)[:,1]
    return P/R

def cal_report(y,P):
    frac,mp = calibration_curve(y,P,n_bins=5,strategy='quantile')
    ece = np.mean(np.abs(frac-mp))
    return {'auc':float(roc_auc_score(y,P)),'brier':float(brier_score_loss(y,P)),
            'ece':float(ece),'bins':[[round(a,2),round(b,2)] for a,b in zip(mp,frac)]}

out={}
for tgt,(fe,base) in CHAMP.items():
    d = df.dropna(subset=[tgt]).copy()
    if tgt=='y_conv': d=d[d.perfil_severidad!='grave']  # excl. techo
    # recodificar sev_ord/bools igual que en el experimento
    SEV={'normal':0,'leve':1,'leve_moderado':2,'moderado':3,'moderado_grave':4,'grave':5}
    d['sev_ord']=d.perfil_severidad.map(SEV)
    for b in ['multidominio','mem_intrusiones_confab','mem_beneficio_contexto','mod_animo','mod_sueno','mod_ansiedad','mod_sensorial']:
        d[b]=d[b].map({True:1,False:0,'True':1,'False':0})
    cols=FE[fe]; X=d[cols]; y=d[tgt].astype(int).values
    base_pipe = Pipeline([('pre',make_pre(cols)),('m',base)])
    variants={'sin_calibrar':base_pipe,
              'platt':CalibratedClassifierCV(base_pipe, method='sigmoid', cv=5),
              'isotonica':CalibratedClassifierCV(base_pipe, method='isotonic', cv=5)}
    print(f"\n=== {tgt}  ({fe}) ===")
    out[tgt]={}
    for name,est in variants.items():
        rep=cal_report(y, oof(est,X,y))
        out[tgt][name]=rep
        print(f"  {name:13s} AUC={rep['auc']:.3f}  Brier={rep['brier']:.3f}  ECE={rep['ece']:.3f}  bins(pred/obs)={rep['bins']}")
    best=min(['platt','isotonica','sin_calibrar'], key=lambda k:out[tgt][k]['brier'])
    print(f"  → mejor calibración: {best} (Brier {out[tgt][best]['brier']:.3f})")
    out[tgt]['best']=best
json.dump(out, open('data/interim/model_recalibration.json','w'), indent=2)
print("\nguardado: data/interim/model_recalibration.json")
