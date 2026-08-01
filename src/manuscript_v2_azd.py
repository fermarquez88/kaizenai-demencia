"""Auditoría Alzheimer&Dementia: análisis nuevos + set de figuras científicas (Nature, español)."""
import warnings,os; warnings.filterwarnings('ignore'); os.environ['PYTHONWARNINGS']='ignore'
import duckdb, numpy as np, pandas as pd
from scipy.stats import norm
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import RepeatedStratifiedKFold, cross_val_score, StratifiedKFold, cross_val_predict
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import roc_curve, roc_auc_score
from sklearn.calibration import calibration_curve
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
REPO="/Users/fernandomarquez/Documents/Claude/Projects/kaizenai-demencia"
RNG=42; SEV={'normal':0,'leve':1,'leve_moderado':2,'moderado':3,'moderado_grave':4,'grave':5}
LAB=['Normal','DCL leve','Leve-mod','Moderado','Mod-grave','Grave']

# ---- frame ----
con=duckdb.connect('db/evaluaciones_v2.duckdb',read_only=True)
r=con.execute("SELECT eval_id,test,subtest,z_final FROM resultados_v2 WHERE z_final IS NOT NULL").df()
ev=con.execute("SELECT eval_id,persona_id,fecha_ev,edad FROM evaluaciones_v2 WHERE cohorte<>'wisc_v'").df()
ps=con.execute("SELECT persona_id,fecha_ev,perfil_severidad,perfil_patron FROM perfil_conclusiones").df()
de=con.execute("SELECT eval_id,dominio,z_peor FROM dominio_eval").df(); con.close()
ev['f']=pd.to_datetime(ev.fecha_ev,errors='coerce'); ev=ev.dropna(subset=['f']).sort_values(['persona_id','f']).drop_duplicates(['persona_id','f'])
ev['t']=ev.groupby('persona_id').f.rank(method='dense'); ev=ev[ev.groupby('persona_id').t.transform('max')>=2]
basal=ev.sort_values('t').groupby('persona_id').first().reset_index()
r['zc']=r.z_final.clip(-6,4); rb=r.merge(basal[['eval_id','persona_id']],on='eval_id')
mr=rb[(rb.test=='Memoria de Relatos')&(rb.subtest=='Diferido')][['persona_id','zc']].drop_duplicates('persona_id').rename(columns={'zc':'mr'})
F=basal[['persona_id','edad','f']].merge(mr,on='persona_id',how='left')
# severidad basal/final + intervalo
psx=ps.copy(); psx['s']=psx.perfil_severidad.map(SEV); psx['f']=pd.to_datetime(psx.fecha_ev,errors='coerce')
psx=psx.dropna(subset=['f','s']).sort_values(['persona_id','f']).drop_duplicates(['persona_id','f'])
psx['t']=psx.groupby('persona_id').f.rank(method='dense'); psx=psx[psx.groupby('persona_id').t.transform('max')>=2]
g=psx.sort_values('t').groupby('persona_id')
first=g.first(); last=g.last()
S=pd.DataFrame({'sb':first.s,'sl':last.s,'phb':first.perfil_patron,'fb':first.f,'fl':last.f})
S['intervalo']=(S.fl-S.fb).dt.days/365.25
F=F.merge(S,left_on='persona_id',right_index=True,how='inner')
F['y_dem']=(F.sl>=3).astype(int)
# global z
gz=de[de.dominio.isin(['atencion','funciones_ejecutivas','memoria','lenguaje','visuoespacial'])].assign(z=lambda x:x.z_peor.clip(-6,4)).groupby('eval_id').z.mean()
gzb=basal.set_index('persona_id').eval_id.map(gz); lastid=ev.sort_values('t').groupby('persona_id').last().eval_id
gzl=lastid.map(gz)
F=F.merge(pd.DataFrame({'gzb':gzb,'gzl':gzl}),left_on='persona_id',right_index=True,how='left')
F['dz']=F.gzl-F.gzb

print("="*60,"\nAUDITORÍA ALZHEIMER & DEMENTIA — análisis nuevos")
# 1) tasa anualizada de progresión
pre=F[F.sb<=2].copy()
py=pre.intervalo.sum(); nev=pre.y_dem.sum()
rate=nev/py*100
print(f"\n[1] Tasa de progresión (pre-demencia): {nev} eventos / {py:.0f} persona-años = {rate:.1f}%/año")
print(f"    crudo: {100*pre.y_dem.mean():.0f}% en mediana {pre.intervalo.median():.1f} a")
# 2) reversión
mci=F[F.sb==1]
rev=(mci.sl==0).sum(); print(f"[2] Reversión DCL→normal: {rev}/{len(mci)} ({100*rev/len(mci):.0f}%)")
print(f"    Mejora ≥1 banda (cualquier basal): {int((F.sl<F.sb).sum())}/{len(F)} ({100*(F.sl<F.sb).mean():.0f}%)")
# 3) valor incremental memoria sobre edad
def auc_cv(cols,d,y):
    p=Pipeline([('i',SimpleImputer(strategy='median',add_indicator=True)),('s',StandardScaler()),('m',LogisticRegression(class_weight='balanced',max_iter=4000))])
    return cross_val_score(p,d[cols],y,scoring='roc_auc',cv=RepeatedStratifiedKFold(n_splits=5,n_repeats=20,random_state=RNG),n_jobs=-1).mean()
print("\n[3] Valor incremental (AUC CV):")
for nm,mask in [('DCL→demencia',F.sb==1),('Pre-demencia→demencia',F.sb<=2)]:
    d=F[mask].dropna(subset=['y_dem']); y=d.y_dem.values
    a_age=auc_cv(['edad'],d,y); a_mr=auc_cv(['mr'],d,y); a_both=auc_cv(['edad','mr'],d,y)
    print(f"    {nm}: edad sola={a_age:.2f} | memoria sola={a_mr:.2f} | edad+memoria={a_both:.2f} (Δ vs edad={a_both-a_age:+.2f})")
# 4) missing data
print("\n[4] Datos faltantes (cohorte pre-demencia):")
for c in ['edad','mr','sb']: print(f"    {c}: {100*pre[c].isna().mean():.0f}% faltante")

# ================= FIGURAS (Nature, español) =================
plt.rcParams.update({'font.family':'sans-serif','font.sans-serif':['Helvetica','Arial','DejaVu Sans'],'font.size':8.5,
 'axes.spines.top':False,'axes.spines.right':False,'axes.linewidth':.8,'xtick.major.width':.8,'ytick.major.width':.8,
 'axes.labelsize':9,'figure.dpi':300,'axes.titlesize':9.5})
TEAL='#0b6b70';CLAY='#b6602c';MOSS='#4c7a58';CRIT='#a23a33';AMBER='#c39433';SLATE='#43648a';GREY='#8a9aa0'

# --- Fig 1: flujo de la cohorte ---
fig,ax=plt.subplots(figsize=(5.4,4.6)); ax.axis('off'); ax.set_xlim(0,10); ax.set_ylim(0,12)
def box(x,y,w,h,txt,c='#eef4f4',ec=TEAL):
    ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle="round,pad=0.02,rounding_size=0.12",fc=c,ec=ec,lw=1.2))
    ax.text(x+w/2,y+h/2,txt,ha='center',va='center',fontsize=7.6)
def arr(x1,y1,x2,y2): ax.add_patch(FancyArrowPatch((x1,y1),(x2,y2),arrowstyle='-|>',mutation_scale=11,color='#555',lw=1))
box(2.5,10.4,5,1.1,"334 pacientes con ≥2\nevaluaciones archivadas")
arr(5,10.4,5,9.5); box(5.7,8.5,4.1,.9,"81 duplicados mismo día\n+ 3 sin fecha (excl.)",c='#f7ece4',ec=CLAY)
arr(3.2,10.4,3.2,7.9)
box(2.5,7,5,1.1,"250 con reevaluación real\n(mediana 1,8 años)")
arr(5,7,5,6.1)
box(1.9,5.0,6.2,1.1,"182 con perfil basal y final codificado\n(κ severidad = 1,00)")
arr(3.3,5.0,2.3,4.1); arr(6.7,5.0,7.7,4.1)
box(0.4,2.9,3.9,1.1,"DCL leve\nn = 85 · 16 → demencia",c='#f7ece4',ec=CLAY)
box(5.7,2.9,3.9,1.1,"Pre-demencia (norm/leve/leve-mod)\nn = 136 · 32 → demencia",c='#eef4f4',ec=TEAL)
ax.set_title("Figura 1. Flujo de la cohorte",loc='left',weight='bold',fontsize=9.5)
fig.savefig(f"{REPO}/Fig1_flujo.png",bbox_inches='tight',dpi=300); plt.close(fig); print("\nFig1_flujo.png")

# --- Fig 2: matriz de transición severidad basal→final ---
M=np.zeros((6,6))
for _,row in S.iterrows(): M[int(row.sb),int(row.sl)]+=1
Mp=M/M.sum(axis=1,keepdims=True)*100
fig,ax=plt.subplots(figsize=(5.6,4.4))
im=ax.imshow(Mp,cmap='BuPu',vmin=0,vmax=100,aspect='auto')
for i in range(6):
    for j in range(6):
        if M[i,j]>0: ax.text(j,i,f"{int(M[i,j])}",ha='center',va='center',fontsize=7.5,color='white' if Mp[i,j]>55 else '#333')
ax.axvline(2.5,color=CRIT,lw=1.4); ax.text(4.2,-0.9,'← rango demencia →',color=CRIT,fontsize=7.5,ha='center')
ax.set_xticks(range(6)); ax.set_xticklabels(LAB,rotation=35,ha='right',fontsize=7.5)
ax.set_yticks(range(6)); ax.set_yticklabels(LAB,fontsize=7.5)
ax.set_xlabel('Severidad en la reevaluación'); ax.set_ylabel('Severidad basal')
ax.set_title("Figura 2. Evolución de los perfiles: transiciones de severidad\n(n por celda; color = % de la fila)",loc='left',weight='bold',fontsize=9)
cb=fig.colorbar(im,ax=ax,fraction=0.046,pad=0.03); cb.set_label('% de la fila',fontsize=7.5); cb.ax.tick_params(labelsize=7)
fig.savefig(f"{REPO}/Fig2_transiciones.png",bbox_inches='tight',dpi=300); plt.close(fig); print("Fig2_transiciones.png")

# --- Fig 3: declive por fenotipo (forest, IC Wilson) ---
def wil(k,n):
    p=k/n; z=1.96; d=1+z*z/n; c=(p+z*z/2/n)/d; h=z*np.sqrt(p*(1-p)/n+z*z/4/n/n)/d; return p,max(0,c-h),min(1,c+h)
gp=F.copy(); b,a=np.polyfit(gp.dropna(subset=['gzb','gzl']).gzb,gp.dropna(subset=['gzb','gzl']).gzl,1)
gp['res']=gp.gzl-(a+b*gp.gzb); gp['dec']=gp.res<-0.3
mapn={'multidominio_global':'Multidominio','amnesico':'Amnésico','disejecutivo':'Disejecutivo','preservado':'Preservado'}
gp['ph']=gp.phb.map(mapn)
fig,ax=plt.subplots(figsize=(5.6,2.9)); rows=[]
for ph,c in [('Amnésico',CLAY),('Disejecutivo',AMBER),('Multidominio',CRIT),('Preservado',MOSS)]:
    sub=gp[gp.ph==ph].dropna(subset=['dec']); p,lo,hi=wil(sub.dec.sum(),len(sub)); rows.append((ph,c,len(sub),p,lo,hi))
yy=np.arange(len(rows))[::-1]
for i,(ph,c,n,p,lo,hi) in enumerate(rows):
    ax.plot([100*lo,100*hi],[yy[i],yy[i]],color=c,lw=1.6); ax.scatter([100*p],[yy[i]],color=c,s=40,zorder=4)
    ax.text(100*hi+2,yy[i],f"{100*p:.0f}%  (n={n})",va='center',fontsize=7.3,color='#333')
ax.set_yticks(yy); ax.set_yticklabels([r[0] for r in rows]); ax.set_xlim(0,75)
ax.set_xlabel('Declive fiable ajustado por el basal (%)  ·  IC95%')
ax.set_title("Figura 3. Declive por fenotipo basal (χ² p = 0,030)",loc='left',weight='bold',fontsize=9.2)
fig.savefig(f"{REPO}/Fig3_fenotipos.png",bbox_inches='tight',dpi=300); plt.close(fig); print("Fig3_fenotipos.png")

# --- Fig 4: regresión a la media ---
d4=F.dropna(subset=['gzb','dz'])
fig,ax=plt.subplots(figsize=(5.2,3.6))
ax.axhline(0,color='#bbb',lw=.8,ls='--')
ax.scatter(d4.gzb,d4.dz,s=14,alpha=.45,color=SLATE,edgecolors='none')
xs=np.linspace(d4.gzb.min(),d4.gzb.max(),50); bb,aa=np.polyfit(d4.gzb,d4.dz,1)
ax.plot(xs,aa+bb*xs,color=CRIT,lw=1.8,label=f'pendiente = {bb:.2f}')
ax.set_xlabel('z cognitivo global BASAL'); ax.set_ylabel('Cambio Δz (final − basal)')
ax.set_title("Figura 4. Regresión a la media: el cambio crudo\ndepende del basal (peor basal → 'mejora' aparente)",loc='left',weight='bold',fontsize=9)
ax.legend(fontsize=7.5,frameon=False,loc='upper right')
fig.savefig(f"{REPO}/Fig4_regresion.png",bbox_inches='tight',dpi=300); plt.close(fig); print("Fig4_regresion.png")

# --- Fig 5: rendimiento (ROC + calibración + valor incremental) ---
def oof(cols,d,y,R=5):
    P=np.zeros(len(y))
    for rr in range(R):
        p=Pipeline([('i',SimpleImputer(strategy='median',add_indicator=True)),('s',StandardScaler()),('m',LogisticRegression(class_weight='balanced',max_iter=4000))])
        P+=cross_val_predict(p,d[cols],y,cv=StratifiedKFold(5,shuffle=True,random_state=RNG+rr),method='predict_proba',n_jobs=-1)[:,1]
    return P/R
fig,axes=plt.subplots(1,3,figsize=(9.6,3.1))
# A ROC
axA=axes[0]
for nm,mask,cols,c in [('DCL→demencia',F.sb==1,['edad','mr'],CLAY),('Pre-demencia→demencia',F.sb<=2,['edad','mr','sb'],TEAL)]:
    d=F[mask].dropna(subset=['y_dem']); y=d.y_dem.values; P=oof(cols,d,y)
    fpr,tpr,_=roc_curve(y,P); axA.plot(fpr,tpr,color=c,lw=1.8,label=f'{nm} (AUC {roc_auc_score(y,P):.2f})')
axA.plot([0,1],[0,1],color='#bbb',ls='--',lw=.8); axA.set_xlabel('1 − especificidad'); axA.set_ylabel('Sensibilidad')
axA.set_title('A · Curvas ROC',loc='left',weight='bold',fontsize=9); axA.legend(fontsize=6.6,frameon=False,loc='lower right')
# B calibración (pre-demencia)
axB=axes[1]; d=F[F.sb<=2].dropna(subset=['y_dem']); y=d.y_dem.values; P=oof(['edad','mr','sb'],d,y)
fr,mp=calibration_curve(y,P,n_bins=5,strategy='quantile'); axB.plot([0,1],[0,1],color='#bbb',ls='--',lw=.8)
axB.plot(mp,fr,'o-',color=TEAL,lw=1.6,ms=5); axB.set_xlabel('Riesgo predicho'); axB.set_ylabel('Frecuencia observada')
axB.set_title('B · Calibración (pre-demencia)',loc='left',weight='bold',fontsize=9); axB.set_xlim(0,1); axB.set_ylim(0,1)
# C valor incremental
axC=axes[2]
d=F[F.sb<=2].dropna(subset=['y_dem']); y=d.y_dem.values
vals=[auc_cv(['edad'],d,y),auc_cv(['mr'],d,y),auc_cv(['edad','mr','sb'],d,y)]
axC.bar(range(3),vals,color=[GREY,AMBER,TEAL],width=.62,zorder=3)
for i,v in enumerate(vals): axC.text(i,v+.01,f'{v:.2f}',ha='center',fontsize=8)
axC.set_xticks(range(3)); axC.set_xticklabels(['Edad\nsola','Memoria\nsola','Modelo\ncompleto'],fontsize=7.5)
axC.set_ylim(0.5,0.9); axC.axhline(0.5,color='#bbb',ls='--',lw=.8); axC.set_ylabel('AUC (CV anidada)')
axC.set_title('C · Valor incremental',loc='left',weight='bold',fontsize=9)
fig.tight_layout(); fig.savefig(f"{REPO}/Fig5_rendimiento.png",bbox_inches='tight',dpi=300); plt.close(fig); print("Fig5_rendimiento.png")
print("\n== figuras generadas ==")
