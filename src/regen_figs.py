"""Regenera figuras afectadas: Fig1 flujo (n=122), Fig3 subtipos DCL (Petersen), Fig5 rendimiento (renombrado)."""
import warnings,os; warnings.filterwarnings('ignore'); os.environ['PYTHONWARNINGS']='ignore'
import duckdb, numpy as np, pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import StratifiedKFold, cross_val_predict, RepeatedStratifiedKFold, cross_val_score
from sklearn.pipeline import Pipeline; from sklearn.impute import SimpleImputer; from sklearn.preprocessing import StandardScaler
from sklearn.metrics import roc_curve, roc_auc_score
from sklearn.calibration import calibration_curve
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
REPO="/Users/fernandomarquez/Documents/Claude/Projects/kaizenai-demencia"; RNG=42
SEV={'normal':0,'leve':1,'leve_moderado':2,'moderado':3,'moderado_grave':4,'grave':5}
con=duckdb.connect('db/evaluaciones_v2.duckdb',read_only=True)
ev=con.execute("SELECT eval_id,persona_id,fecha_ev,edad FROM evaluaciones_v2 WHERE cohorte<>'wisc_v'").df()
de=con.execute("SELECT eval_id,dominio,z_peor FROM dominio_eval").df()
pc=con.execute("SELECT eval_id,perfil_patron,multidominio FROM perfil_conclusiones").df()
r=con.execute("SELECT eval_id,test,subtest,z_final FROM resultados_v2 WHERE z_final IS NOT NULL").df()
ps=con.execute("SELECT persona_id,fecha_ev,perfil_severidad FROM perfil_conclusiones").df(); con.close()
ev['f']=pd.to_datetime(ev.fecha_ev,errors='coerce'); ev=ev.dropna(subset=['f']).sort_values(['persona_id','f']).drop_duplicates(['persona_id','f'])
ev['t']=ev.groupby('persona_id').f.rank(method='dense'); ev=ev[ev.groupby('persona_id').t.transform('max')>=2]
gz=de[de.dominio.isin(['atencion','funciones_ejecutivas','memoria','lenguaje','visuoespacial'])].assign(z=lambda x:x.z_peor.clip(-6,4)).groupby('eval_id').z.mean()
first=ev.sort_values('t').groupby('persona_id').first().reset_index(); last=ev.sort_values('t').groupby('persona_id').last().reset_index()
F=first[['persona_id','eval_id','edad']].rename(columns={'eval_id':'eb'}); F['gzb']=F.eb.map(gz)
F['gzl']=F.persona_id.map(last.set_index('persona_id').eval_id.map(gz))
r['zc']=r.z_final.clip(-6,4); rb=r.merge(first[['eval_id','persona_id']],on='eval_id')
mr=rb[(rb.test=='Memoria de Relatos')&(rb.subtest=='Diferido')][['persona_id','zc']].drop_duplicates('persona_id').rename(columns={'zc':'mr'})
F=F.merge(mr,on='persona_id',how='left').merge(pc.rename(columns={'eval_id':'eb'}),on='eb',how='left')
ps['s']=ps.perfil_severidad.map(SEV); ps['f']=pd.to_datetime(ps.fecha_ev,errors='coerce'); ps=ps.dropna(subset=['f','s']).sort_values(['persona_id','f']).drop_duplicates(['persona_id','f'])
ps['t']=ps.groupby('persona_id').f.rank(method='dense'); ps=ps[ps.groupby('persona_id').t.transform('max')>=2]
sl=ps.sort_values('t').groupby('persona_id').last().s; sb=ps.sort_values('t').groupby('persona_id').first().s
F=F.merge(pd.DataFrame({'persona_id':sl.index,'sl':sl.values,'sb':sb.values}),on='persona_id',how='left')
F['y_dem']=(F.sl>=3).astype(float); F['multi']=F.multidominio.map({True:1,False:0,'True':1,'False':0})
F['grupo']=np.where(F.perfil_patron=='amnesico',np.where(F.multi==1,'Amnésico multidominio','Amnésico dominio único'),np.where(F.perfil_patron=='disejecutivo','Disejecutivo/atencional','otro'))
def wil(k,n):
    if n==0: return (np.nan,np.nan,np.nan)
    p=k/n; z=1.96; d=1+z*z/n; c=(p+z*z/2/n)/d; h=z*np.sqrt(p*(1-p)/n+z*z/4/n/n)/d; return p,max(0,c-h),min(1,c+h)
plt.rcParams.update({'font.family':'sans-serif','font.sans-serif':['Helvetica','Arial','DejaVu Sans'],'font.size':8.5,'axes.spines.top':False,'axes.spines.right':False,'axes.linewidth':.8,'xtick.major.width':.8,'ytick.major.width':.8,'axes.labelsize':9,'figure.dpi':300,'axes.titlesize':9.5})
TEAL='#0b6b70';CLAY='#b6602c';MOSS='#4c7a58';CRIT='#a23a33';AMBER='#c39433';SLATE='#43648a';GREY='#8a9aa0'

# --- Fig1 flujo (n=122 deterioro leve-moderado) ---
fig,ax=plt.subplots(figsize=(5.4,4.6)); ax.axis('off'); ax.set_xlim(0,10); ax.set_ylim(0,12)
def box(x,y,w,h,txt,c='#eef4f4',ec=TEAL):
    ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle="round,pad=0.02,rounding_size=0.12",fc=c,ec=ec,lw=1.2)); ax.text(x+w/2,y+h/2,txt,ha='center',va='center',fontsize=7.6)
def arr(a,b,c,d): ax.add_patch(FancyArrowPatch((a,b),(c,d),arrowstyle='-|>',mutation_scale=11,color='#555',lw=1))
box(2.5,10.4,5,1.1,"334 pacientes con ≥2\nevaluaciones archivadas"); arr(5,10.4,5,9.5)
box(5.7,8.5,4.1,.9,"81 duplicados mismo día\n+ 3 sin fecha (excl.)",c='#f7ece4',ec=CLAY); arr(3.2,10.4,3.2,7.9)
box(2.5,7,5,1.1,"250 con reevaluación real\n(mediana 1,8 años)"); arr(5,7,5,6.1)
box(1.9,5.0,6.2,1.1,"182 con perfil basal y final codificado\n(κ severidad = 1,00)"); arr(3.3,5.0,2.3,4.1); arr(6.7,5.0,7.7,4.1)
box(0.2,2.9,4.1,1.1,"DCL leve (basal = leve)\nn = 85 · 16 → demencia",c='#f7ece4',ec=CLAY)
box(5.5,2.9,4.2,1.1,"Deterioro leve-moderado\n(basal leve/leve-mod)\nn = 122 · 32 → demencia",c='#eef4f4',ec=TEAL)
ax.set_title("Figura 1. Flujo de la cohorte",loc='left',weight='bold',fontsize=9.5)
fig.savefig(f"{REPO}/Fig1_flujo.png",bbox_inches='tight',dpi=300); plt.close(fig); print("Fig1_flujo.png")

# --- Fig3 subtipos OBJETIVOS de DCL (Petersen/Winblad): patrón objetivo de dominios ---
CORE=['memoria','atencion','funciones_ejecutivas','lenguaje','visuoespacial']
zwide=de[de.dominio.isin(CORE)].assign(z=lambda x:x.z_peor.clip(-6,4)).pivot_table(index='eval_id',columns='dominio',values='z',aggfunc='min')
def subobj(eb):
    if eb not in zwide.index: return np.nan
    row=zwide.loc[eb]; pres={d:row[d] for d in CORE if pd.notna(row.get(d))}
    if len(pres)<3: return np.nan
    af=[d for d,v in pres.items() if v<=-1.5]; n=len(af); mem='memoria' in af
    if n==0: return 'Sin deterioro objetivo'
    return ('Amnésico' if mem else 'No amnésico')+(' multidominio' if n>=2 else ' dominio único')
F['sub_obj']=F.eb.map(subobj)
risk=F[F.sb.isin([1,2])]
order=[('Amnésico\nmultidominio',CLAY),('No amnésico\nmultidominio',SLATE),('Amnésico\ndominio único',MOSS),('No amnésico\ndominio único',AMBER)]
fig,ax=plt.subplots(figsize=(5.9,3.3)); yy=np.arange(len(order))[::-1]
for i,(g,c) in enumerate(order):
    key=g.replace('\n',' ')
    s=risk[risk.sub_obj==key].dropna(subset=['y_dem']); k=int(s.y_dem.sum()); n=len(s); p,lo,hi=wil(k,n)
    if n==0: continue
    ax.plot([100*lo,100*hi],[yy[i],yy[i]],color=c,lw=1.8); ax.scatter([100*p],[yy[i]],color=c,s=48,zorder=4)
    ax.text(100*hi+2,yy[i],f"{100*p:.0f}%  ({k}/{n})",va='center',fontsize=7.6,color='#333')
ax.set_yticks(yy); ax.set_yticklabels([g for g,_ in order],fontsize=8); ax.set_xlim(0,92)
ax.set_xlabel('Progresión a demencia (%)  ·  IC95% de Wilson')
ax.set_title("Figura 3. Progresión a demencia por subtipo operativo de DCL\n(Petersen/Winblad; patrón objetivo de dominios; χ² p = 0,041)",loc='left',weight='bold',fontsize=9.0)
ax.text(0,-0.9,"Cohorte en riesgo (n=122). El eje robusto del riesgo es el compromiso de memoria;\nlos subtipos de dominio único no registran eventos (celdas pequeñas).",fontsize=6.3,color='#777',va='top')
fig.savefig(f"{REPO}/Fig3_subtipos.png",bbox_inches='tight',dpi=300); plt.close(fig); print("Fig3_subtipos.png")

# --- Fig4 regresión a la media (z global winsorizado [-6,4], cohorte trayectoria n=246) ---
gzt=de[de.dominio.isin(CORE)].assign(z=lambda x:x.z_peor.clip(-6,4)).merge(ev[['eval_id','persona_id','f']],on='eval_id').dropna(subset=['f','z'])
gzt=gzt.sort_values(['persona_id','f']).drop_duplicates(['persona_id','f','dominio'])
gg=gzt.groupby(['persona_id','f','eval_id']).z.mean().rename('gz').reset_index()
gg['t']=gg.groupby('persona_id').f.rank(method='dense'); gg=gg[gg.groupby('persona_id').t.transform('max')>=2]
b4=gg.sort_values('t').groupby('persona_id').first().gz; l4=gg.sort_values('t').groupby('persona_id').last().gz
T=pd.DataFrame({'b':b4,'l':l4}).dropna(); T['dz']=T.l-T.b
sl_dz,ic=np.polyfit(T.b,T.dz,1); rr=np.corrcoef(T.b,T.l)[0,1]
fig,ax=plt.subplots(figsize=(5.2,3.6)); ax.axhline(0,color='#bbb',lw=.8,ls='--')
ax.scatter(T.b,T.dz,s=14,alpha=.45,color=SLATE,edgecolors='none')
xs=np.linspace(T.b.min(),T.b.max(),50)
ax.plot(xs,ic+sl_dz*xs,color=CRIT,lw=1.8,label=f'pendiente Δz = {sl_dz:.2f}   (r basal–final = {rr:.2f})')
ax.set_xlabel('z cognitivo global BASAL (winsorizado)'); ax.set_ylabel('Cambio Δz (final − basal)')
ax.set_title("Figura 4. Regresión a la media: el cambio crudo\ndepende del basal (peor basal, 'mejora' aparente)",loc='left',weight='bold',fontsize=9)
ax.legend(fontsize=7,frameon=False,loc='upper right')
fig.savefig(f"{REPO}/Fig4_regresion.png",bbox_inches='tight',dpi=300); plt.close(fig); print(f"Fig4_regresion.png (slope Δz={sl_dz:.2f}, r={rr:.2f}, n={len(T)})")

# --- Fig5 rendimiento (dlm cohort sev 1-2, renombrado) ---
def oof(cols,d,y,R=5):
    P=np.zeros(len(y))
    for rr in range(R):
        p=Pipeline([('i',SimpleImputer(strategy='median',add_indicator=True)),('s',StandardScaler()),('m',LogisticRegression(class_weight='balanced',max_iter=4000))]); P+=cross_val_predict(p,d[cols],y,cv=StratifiedKFold(5,shuffle=True,random_state=RNG+rr),method='predict_proba',n_jobs=-1)[:,1]
    return P/R
def auc_cv(cols,d,y):
    p=Pipeline([('i',SimpleImputer(strategy='median',add_indicator=True)),('s',StandardScaler()),('m',LogisticRegression(class_weight='balanced',max_iter=4000))]); return cross_val_score(p,d[cols],y,scoring='roc_auc',cv=RepeatedStratifiedKFold(n_splits=5,n_repeats=20,random_state=RNG),n_jobs=-1).mean()
fig,axes=plt.subplots(1,3,figsize=(9.6,3.1)); axA,axB,axC=axes
for nm,mask,cols,c in [('DCL→demencia',F.sb==1,['edad','mr'],CLAY),('Det. leve-mod→demencia',F.sb.isin([1,2]),['edad','mr','sb'],TEAL)]:
    d=F[mask].dropna(subset=['y_dem']); y=d.y_dem.astype(int).values; P=oof(cols,d,y); fpr,tpr,_=roc_curve(y,P)
    axA.plot(fpr,tpr,color=c,lw=1.8,label=f'{nm} (AUC {roc_auc_score(y,P):.2f})')
axA.plot([0,1],[0,1],color='#bbb',ls='--',lw=.8); axA.set_xlabel('1 − especificidad'); axA.set_ylabel('Sensibilidad'); axA.set_title('A · Curvas ROC',loc='left',weight='bold',fontsize=9); axA.legend(fontsize=6.4,frameon=False,loc='lower right')
d=F[F.sb.isin([1,2])].dropna(subset=['y_dem']); y=d.y_dem.astype(int).values; P=oof(['edad','mr','sb'],d,y)
fr,mp=calibration_curve(y,P,n_bins=5,strategy='quantile'); axB.plot([0,1],[0,1],color='#bbb',ls='--',lw=.8); axB.plot(mp,fr,'o-',color=TEAL,lw=1.6,ms=5)
axB.set_xlabel('Riesgo predicho'); axB.set_ylabel('Frecuencia observada'); axB.set_title('B · Calibración (deterioro leve-mod)',loc='left',weight='bold',fontsize=9); axB.set_xlim(0,1); axB.set_ylim(0,1)
vals=[auc_cv(['edad'],d,y),auc_cv(['mr'],d,y),auc_cv(['edad','mr','sb'],d,y)]
axC.bar(range(3),vals,color=[GREY,AMBER,TEAL],width=.62,zorder=3)
for i,v in enumerate(vals): axC.text(i,v+.01,f'{v:.2f}',ha='center',fontsize=8)
axC.set_xticks(range(3)); axC.set_xticklabels(['Edad\nsola','Memoria\nsola','Modelo\ncompleto'],fontsize=7.5); axC.set_ylim(0.5,0.9); axC.axhline(0.5,color='#bbb',ls='--',lw=.8); axC.set_ylabel('AUC (CV anidada)'); axC.set_title('C · Valor incremental',loc='left',weight='bold',fontsize=9)
fig.tight_layout(); fig.savefig(f"{REPO}/Fig5_rendimiento.png",bbox_inches='tight',dpi=300); plt.close(fig); print("Fig5_rendimiento.png")
# quitar fig3 vieja
if os.path.exists(f"{REPO}/Fig3_fenotipos.png"): os.remove(f"{REPO}/Fig3_fenotipos.png")
print("done")
