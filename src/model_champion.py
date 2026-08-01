"""Análisis del modelo campeón por target: OOF repetido, calibración, decision-curve,
comparación bootstrap de AUC (champion vs parsimonioso vs baseline), importancia por permutación (CV), SHAP."""
import warnings; warnings.filterwarnings('ignore')
import numpy as np, pandas as pd, json
from sklearn.model_selection import StratifiedKFold, GridSearchCV, cross_val_predict
from sklearn.metrics import roc_auc_score, average_precision_score, brier_score_loss
from sklearn.calibration import calibration_curve
from sklearn.inspection import permutation_importance
from sklearn.pipeline import Pipeline
from model_experiment import FE, make_pre, clf_models, df

RNG=42
res = pd.read_csv('data/interim/model_results.csv')

def build(fe, model):
    cols = FE[fe]; est,grid = clf_models()[model]
    pipe = Pipeline([('pre', make_pre(cols)), ('m', est)])
    return (GridSearchCV(pipe, grid, scoring='roc_auc', cv=3, n_jobs=-1) if grid else pipe), cols

def oof_proba(fe, model, X, y, R=5):
    P = np.zeros(len(y))
    for r in range(R):
        est,_ = build(fe, model)
        skf = StratifiedKFold(5, shuffle=True, random_state=RNG+r)
        P += cross_val_predict(est, X, y, cv=skf, method='predict_proba', n_jobs=-1)[:,1]
    return P/R

def dca(y, p, thr):
    N=len(y); nb=[]
    for t in thr:
        pred = p>=t
        tp=np.sum((pred)&(y==1)); fp=np.sum((pred)&(y==0))
        nb.append(tp/N - fp/N*(t/(1-t)))
    return np.array(nb)

def analyze(target, exclude_ceiling=False):
    d = df.dropna(subset=[target]).copy()
    if exclude_ceiling: d = d[d.sev_ord<5]
    y = d[target].astype(int).values
    sub = res[(res.target==target)&(res.model!='dummy')].sort_values('auc', ascending=False)
    champ = sub.iloc[0]
    print(f"\n{'='*66}\n{target}: CAMPEÓN = {champ.fe}/{champ.model} (AUC CV={champ.auc:.3f})")
    _,cols_c = build(champ.fe, champ.model)
    out = {'target':target,'champion':f"{champ.fe}/{champ.model}",'prevalencia':float(y.mean()),'n':int(len(y))}

    # OOF de champion, parsimonioso (A/logit_en) y baseline (prior)
    Pc = oof_proba(champ.fe, champ.model, d[FE[champ.fe]], y)
    Pp = oof_proba('A_parsimonioso','logit_en', d[FE['A_parsimonioso']], y)
    prev = y.mean(); Pd = np.full(len(y), prev)
    for nm,P in [('champion',Pc),('parsimonioso',Pp)]:
        out[nm]={'auc':float(roc_auc_score(y,P)),'ap':float(average_precision_score(y,P)),'brier':float(brier_score_loss(y,P))}
        print(f"  {nm:13s} AUC={out[nm]['auc']:.3f}  AP={out[nm]['ap']:.3f}  Brier={out[nm]['brier']:.3f}")

    # bootstrap: AUC champion, parsimonioso, y su diferencia
    rng=np.random.RandomState(RNG); diffs=[]; aucs_c=[]
    for _ in range(2000):
        idx=rng.randint(0,len(y),len(y))
        if len(np.unique(y[idx]))<2: continue
        ac=roc_auc_score(y[idx],Pc[idx]); ap_=roc_auc_score(y[idx],Pp[idx])
        aucs_c.append(ac); diffs.append(ac-ap_)
    out['champion']['auc_ci']=[float(np.percentile(aucs_c,2.5)),float(np.percentile(aucs_c,97.5))]
    out['diff_champ_vs_parsi']={'mean':float(np.mean(diffs)),'ci':[float(np.percentile(diffs,2.5)),float(np.percentile(diffs,97.5))],
                                'p_gt0':float(np.mean(np.array(diffs)>0))}
    print(f"  AUC champion IC95%=[{out['champion']['auc_ci'][0]:.3f},{out['champion']['auc_ci'][1]:.3f}]  "
          f"Δ(champ-parsi)={out['diff_champ_vs_parsi']['mean']:+.3f} IC[{out['diff_champ_vs_parsi']['ci'][0]:+.3f},{out['diff_champ_vs_parsi']['ci'][1]:+.3f}]")

    # calibración
    frac,mean_pred = calibration_curve(y, Pc, n_bins=5, strategy='quantile')
    out['calibration']={'mean_pred':mean_pred.tolist(),'frac_pos':frac.tolist()}
    # decision curve
    thr=np.arange(0.05,0.55,0.05)
    out['dca']={'thr':thr.tolist(),'nb_model':dca(y,Pc,thr).tolist(),
                'nb_all':[float(prev-(1-prev)*(t/(1-t))) for t in thr]}

    # importancia por permutación (CV): champion refit por fold, permuta en test
    imp={}; skf=StratifiedKFold(5,shuffle=True,random_state=RNG)
    Xc=d[cols_c].reset_index(drop=True)
    for tr,te in skf.split(Xc,y):
        est,_=build(champ.fe,champ.model); est.fit(Xc.iloc[tr],y[tr])
        pi=permutation_importance(est,Xc.iloc[te],y[te],scoring='roc_auc',n_repeats=10,random_state=RNG)
        for c,v in zip(cols_c,pi.importances_mean): imp.setdefault(c,[]).append(v)
    impm={c:float(np.mean(v)) for c,v in imp.items()}
    out['importancia']=dict(sorted(impm.items(), key=lambda x:-x[1])[:12])
    print("  Top importancia (permutación, ΔAUC):")
    for c,v in list(out['importancia'].items())[:8]: print(f"    {c:26s} {v:+.4f}")
    return out

if __name__=='__main__':
    results={}
    for t,exc in [('y_rci',False),('y_conv',True)]:
        results[t]=analyze(t,exc)
    json.dump(results, open('data/interim/model_champion.json','w'), indent=2)
    print("\nguardado: data/interim/model_champion.json")
