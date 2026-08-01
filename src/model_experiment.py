"""Experimento supervisado: 3 targets x 5 feature-sets x modelos, con CV anidada.
Rigor: baselines, RepeatedStratifiedKFold, tuning interno (GridSearch cv=3), IC por percentiles."""
import os, warnings
os.environ['PYTHONWARNINGS']='ignore'; warnings.filterwarnings('ignore')   # también en workers paralelos
import pandas as pd, numpy as np, json
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.linear_model import LogisticRegression, ElasticNet
from sklearn.ensemble import RandomForestClassifier, HistGradientBoostingClassifier, \
    RandomForestRegressor, HistGradientBoostingRegressor
from sklearn.dummy import DummyClassifier, DummyRegressor
from sklearn.model_selection import RepeatedStratifiedKFold, RepeatedKFold, GridSearchCV, cross_validate

RNG = 42
df = pd.read_csv('data/interim/model_dataset.csv').merge(
     pd.read_csv('data/interim/model_clusters.csv'), on='persona_id', how='left')
SEV = {'normal':0,'leve':1,'leve_moderado':2,'moderado':3,'moderado_grave':4,'grave':5}
df['sev_ord'] = df.perfil_severidad.map(SEV)
for b in ['multidominio','mem_intrusiones_confab','mem_beneficio_contexto','mod_animo','mod_sueno','mod_ansiedad','mod_sensorial']:
    df[b] = df[b].map({True:1,False:0,'True':1,'False':0})

CAT = ['perfil_patron','mem_almacenamiento','tipo_curva']
FE = {
 'A_parsimonioso': ['edad','educacion','sexo_f','z_gz','z_memoria','sev_ord','mem_almacenamiento','mod_animo','intervalo'],
 'B_full': ['edad','educacion','sexo_f','intervalo','z_atencion','z_funciones_ejecutivas','z_memoria','z_lenguaje',
            'z_visuoespacial','z_gz','z_dispersion','z_premorbido','z_ci_wais','caida_premorb','sev_ord','perfil_patron',
            'multidominio','mem_almacenamiento','mem_intrusiones_confab','mem_beneficio_contexto','mod_animo','mod_sueno',
            'mod_ansiedad','mod_sensorial','intrusiones','confabulaciones','tipo_curva','aprendizaje_total','tasa_aprendizaje','recon_corregido'],
 'C_proceso': ['z_memoria','z_gz','mem_almacenamiento','mem_intrusiones_confab','mem_beneficio_contexto','intrusiones',
               'confabulaciones','tipo_curva','aprendizaje_total','tasa_aprendizaje','recon_corregido','intervalo'],
 'D_reserva': ['edad','educacion','z_premorbido','caida_premorb','z_gz','sexo_f','intervalo'],
 'E_full+cluster': None,   # = B_full + cluster
}
FE['E_full+cluster'] = FE['B_full'] + ['cluster']

def make_pre(cols):
    cat = [c for c in cols if c in CAT]
    num = [c for c in cols if c not in CAT]
    return ColumnTransformer([
        ('num', Pipeline([('imp', SimpleImputer(strategy='median', add_indicator=True)), ('sc', StandardScaler())]), num),
        ('cat', Pipeline([('imp', SimpleImputer(strategy='most_frequent')),
                          ('oh', OneHotEncoder(handle_unknown='ignore'))]), cat)])

def clf_models():
    return {
      'dummy': (DummyClassifier(strategy='prior'), {}),
      'logit_en': (LogisticRegression(penalty='elasticnet', solver='saga', max_iter=3000, tol=1e-3, class_weight='balanced'),
                   {'m__C':[0.03,0.1,0.3,1.0], 'm__l1_ratio':[0.2,0.5,0.8]}),
      'rf': (RandomForestClassifier(n_estimators=250, class_weight='balanced', random_state=RNG),
             {'m__max_depth':[3,5,None], 'm__min_samples_leaf':[1,5]}),
      'hgb': (HistGradientBoostingClassifier(random_state=RNG),
              {'m__max_depth':[2,3], 'm__learning_rate':[0.05,0.1]}),
    }
def reg_models():
    return {
      'dummy': (DummyRegressor(strategy='mean'), {}),
      'elasticnet': (ElasticNet(max_iter=6000), {'m__alpha':[0.05,0.1,0.3,1.0], 'm__l1_ratio':[0.2,0.5,0.8]}),
      'rf': (RandomForestRegressor(n_estimators=250, random_state=RNG), {'m__max_depth':[3,5,None], 'm__min_samples_leaf':[1,5]}),
      'hgb': (HistGradientBoostingRegressor(random_state=RNG), {'m__max_depth':[2,3], 'm__learning_rate':[0.05,0.1]}),
    }

def run_binary(target, exclude_ceiling=False):
    d = df.dropna(subset=[target]).copy()
    if exclude_ceiling: d = d[d.sev_ord < 5]
    y = d[target].astype(int).values
    outer = RepeatedStratifiedKFold(n_splits=5, n_repeats=5, random_state=RNG)
    rows = []
    for fename, cols in FE.items():
        X = d[cols]
        for mname,(est,grid) in clf_models().items():
            pipe = Pipeline([('pre', make_pre(cols)), ('m', est)])
            model = GridSearchCV(pipe, grid, scoring='roc_auc', cv=3, n_jobs=1) if grid else pipe
            cv = cross_validate(model, X, y, scoring=['roc_auc','average_precision'], cv=outer, n_jobs=-1)
            auc = cv['test_roc_auc']; ap = cv['test_average_precision']
            rows.append({'target':target,'fe':fename,'model':mname,'auc':auc.mean(),
                         'auc_lo':np.percentile(auc,2.5),'auc_hi':np.percentile(auc,97.5),'ap':ap.mean()})
            print(f"  [{target}] {fename:16s} {mname:9s} AUC={auc.mean():.3f} [{np.percentile(auc,2.5):.3f},{np.percentile(auc,97.5):.3f}]  AP={ap.mean():.3f}", flush=True)
    return pd.DataFrame(rows)

def run_cont(target='dz_ajust'):
    d = df.dropna(subset=[target]).copy()
    y = d[target].values
    outer = RepeatedKFold(n_splits=5, n_repeats=5, random_state=RNG)
    rows=[]
    for fename, cols in FE.items():
        X = d[cols]
        for mname,(est,grid) in reg_models().items():
            pipe = Pipeline([('pre', make_pre(cols)), ('m', est)])
            model = GridSearchCV(pipe, grid, scoring='r2', cv=3, n_jobs=1) if grid else pipe
            cv = cross_validate(model, X, y, scoring=['r2','neg_mean_absolute_error'], cv=outer, n_jobs=-1)
            r2 = cv['test_r2']; mae = -cv['test_neg_mean_absolute_error']
            rows.append({'target':target,'fe':fename,'model':mname,'r2':r2.mean(),
                         'r2_lo':np.percentile(r2,2.5),'r2_hi':np.percentile(r2,97.5),'mae':mae.mean()})
            print(f"  [{target}] {fename:16s} {mname:9s} R2={r2.mean():+.3f} [{np.percentile(r2,2.5):+.3f},{np.percentile(r2,97.5):+.3f}]  MAE={mae.mean():.3f}", flush=True)
    return pd.DataFrame(rows)

if __name__ == '__main__':
    all_res=[]
    print("=== T1: DECLIVE FIABLE (RCI global, binario) ===")
    all_res.append(run_binary('y_rci'))
    print("\n=== T3: CONVERSIÓN DE BANDA (binario, excl. techo grave) ===")
    all_res.append(run_binary('y_conv', exclude_ceiling=True))
    print("\n=== T2: Δz AJUSTADO POR BASAL (continuo) ===")
    all_res.append(run_cont('dz_ajust'))
    res = pd.concat(all_res, ignore_index=True)
    res.to_csv('data/interim/model_results.csv', index=False)
    print("\n=== CAMPEONES por target (excl. dummy) ===")
    for t in ['y_rci','y_conv']:
        sub = res[(res.target==t)&(res.model!='dummy')].sort_values('auc', ascending=False)
        dummy = res[(res.target==t)&(res.model=='dummy')].auc.mean()
        print(f"  {t}: champion {sub.iloc[0].fe}/{sub.iloc[0].model} AUC={sub.iloc[0].auc:.3f} (dummy={dummy:.3f})")
    subc = res[(res.target=='dz_ajust')&(res.model!='dummy')].sort_values('r2', ascending=False)
    print(f"  dz_ajust: champion {subc.iloc[0].fe}/{subc.iloc[0].model} R2={subc.iloc[0].r2:+.3f}")
    print("\nguardado: data/interim/model_results.csv")
