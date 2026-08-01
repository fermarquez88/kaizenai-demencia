"""Tablas + figuras (estilo Nature) + números para la auditoría del manuscrito."""
import warnings, os; warnings.filterwarnings('ignore')
import duckdb, numpy as np, pandas as pd
from scipy.stats import chi2_contingency, fisher_exact, norm
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
REPO="/Users/fernandomarquez/Documents/Claude/Projects/kaizenai-demencia"
SEV={'normal':0,'leve':1,'leve_moderado':2,'moderado':3,'moderado_grave':4,'grave':5}
LAB={0:'Normal',1:'DCL leve',2:'Leve-mod',3:'Moderado',4:'Mod-grave',5:'Grave'}

con=duckdb.connect('db/evaluaciones_v2.duckdb',read_only=True)
ev=con.execute("SELECT eval_id,persona_id,fecha_ev,edad,educacion,sexo FROM evaluaciones_v2 WHERE cohorte<>'wisc_v'").df()
de=con.execute("SELECT eval_id,dominio,z_peor FROM dominio_eval").df()
perf=con.execute("SELECT eval_id,perfil_patron,mem_almacenamiento,mod_animo FROM perfil_conclusiones").df()
ps=con.execute("SELECT persona_id,fecha_ev,perfil_severidad FROM perfil_conclusiones").df()
con.close()
ev['f']=pd.to_datetime(ev.fecha_ev,errors='coerce')
ev=ev.dropna(subset=['f']).sort_values(['persona_id','f']).drop_duplicates(['persona_id','f'])
ev['t']=ev.groupby('persona_id').f.rank(method='dense'); nt=ev.groupby('persona_id').t.transform('max')
ev['reeval']=nt>=2
CORE=['atencion','funciones_ejecutivas','memoria','lenguaje','visuoespacial']
gz=de[de.dominio.isin(CORE)].assign(z=lambda x:x.z_peor.clip(-6,4)).groupby('eval_id').z.mean().rename('gz')
ev=ev.merge(gz,on='eval_id',how='left')

# ---------- Tabla 1: demografía reeval vs 1-visita ----------
base=ev[ev.t==1].copy(); base['fem']=base.sexo.astype(str).str.upper().str[0]=='F'
def desc(d): return f"{d.edad.mean():.1f}±{d.edad.std():.1f}", f"{d.educacion.mean():.1f}±{d.educacion.std():.1f}", f"{100*d.fem.mean():.0f}%"
r=base[base.reeval]; s=base[~base.reeval]
print("=== TABLA 1: demografía (basal) ===")
print(f"  Reeval (n={len(r)}): edad {desc(r)[0]}, educ {desc(r)[1]}, %fem {desc(r)[2]}")
print(f"  1-visita (n={len(s)}): edad {desc(s)[0]}, educ {desc(s)[1]}, %fem {desc(s)[2]}")
rr=ev[ev.reeval]; span=rr.groupby('persona_id').f.agg(lambda x:(x.max()-x.min()).days/365.25)
ntomas=rr.groupby('persona_id').t.max().value_counts().sort_index()
print(f"  Seguimiento (reeval): mediana {span.median():.2f} a (IQR {span.quantile(.25):.2f}-{span.quantile(.75):.2f})")
print(f"  Nº tomas: {ntomas.to_dict()}")

# ---------- severidad basal + target demencia (longitudinal) ----------
ps['s']=ps.perfil_severidad.map(SEV); ps['f']=pd.to_datetime(ps.fecha_ev,errors='coerce')
ps=ps.dropna(subset=['f','s']).sort_values(['persona_id','f']).drop_duplicates(['persona_id','f'])
ps['t']=ps.groupby('persona_id').f.rank(method='dense'); ps=ps[ps.groupby('persona_id').t.transform('max')>=2]
fb=ps.sort_values('t').groupby('persona_id').first().s; lb=ps.sort_values('t').groupby('persona_id').last().s
D=pd.DataFrame({'sb':fb,'sl':lb}); D['dem']=D.sl>=3
print("\n=== Distribución severidad BASAL (cohorte longitudinal, n=%d) ===" % len(D))
print(D.sb.map(LAB).value_counts().reindex([LAB[i] for i in range(6)]).dropna().to_string())
print("\n=== Denominador 'normal→demencia' (AUDITORÍA) ===")
nrm=D[D.sb==0]; print(f"  Basal NORMAL: n={len(nrm)} → progresaron a demencia: {int(nrm.dem.sum())}")
print("=== Sensibilidad definición de demencia (cohorte pre-demencia sb<=2, n=%d) ===" % int((D.sb<=2).sum()))
pre=D[D.sb<=2]
for thr,nm in [(3,'≥moderado (usado)'),(4,'≥mod-grave'),(5,'=grave')]:
    print(f"  {nm:18s} {int((pre.sl>=thr).sum())} eventos ({100*(pre.sl>=thr).mean():.0f}%)")

# ---------- Figura 1: declive por fenotipo (ajustado por basal) + IC + inferencia ----------
gpair=ev[ev.reeval].copy()
first=gpair.sort_values('t').groupby('persona_id').first(); last=gpair.sort_values('t').groupby('persona_id').last()
T=pd.DataFrame({'gzb':first.gz,'gzl':last.gz,'eb':first.eval_id})
T=T.dropna(subset=['gzb','gzl'])
b,a=np.polyfit(T.gzb,T.gzl,1); T['res']=T.gzl-(a+b*T.gzb); T['dec']=T.res< -0.3
T=T.merge(perf.rename(columns={'eval_id':'eb'}),on='eb',how='left')
def wilson(k,n):
    if n==0: return (0,0,0)
    p=k/n; z=1.96; d=1+z*z/n
    c=(p+z*z/2/n)/d; h=z*np.sqrt(p*(1-p)/n+z*z/4/n/n)/d
    return p, max(0,c-h), min(1,c+h)
print("\n=== FIGURA 1: declive fiable (ajustado) por FENOTIPO basal ===")
order=['multidomain','amnesico','disejecutivo','preservado']
mapn={'multidominio_global':'multidomain','amnesico':'amnesico','disejecutivo':'disejecutivo','preservado':'preservado'}
T['ph']=T.perfil_patron.map(mapn)
rows=[]
for ph in order:
    sub=T[T.ph==ph]; p,lo,hi=wilson(sub.dec.sum(),len(sub)); rows.append((ph,len(sub),p,lo,hi))
    print(f"  {ph:14s} n={len(sub):3d}  declive={100*p:.0f}% [IC95 {100*lo:.0f}-{100*hi:.0f}]")
tab=T[T.ph.isin(order)]; ct=pd.crosstab(tab.ph,tab.dec)
chi,pv,_,_=chi2_contingency(ct); print(f"  Omnibus χ²={chi:.1f}, p={pv:.3f}")
# storage
st=T.dropna(subset=['mem_almacenamiento'])
scomp=st[st.mem_almacenamiento=='comprometido']; scons=st[st.mem_almacenamiento=='conservado']
pc,loc,hic=wilson(scomp.dec.sum(),len(scomp)); pk,lok,hik=wilson(scons.dec.sum(),len(scons))
orv,pf=fisher_exact([[scomp.dec.sum(),len(scomp)-scomp.dec.sum()],[scons.dec.sum(),len(scons)-scons.dec.sum()]])
print(f"  Almacenamiento comprometido {100*pc:.0f}% [{100*loc:.0f}-{100*hic:.0f}] (n={len(scomp)}) vs conservado {100*pk:.0f}% [{100*lok:.0f}-{100*hik:.0f}] (n={len(scons)}); OR={orv:.1f} p={pf:.3f}")
# mood
mm=T.dropna(subset=['mod_animo']); mm['an']=mm.mod_animo.map({True:1,False:0,'True':1,'False':0})
ma=mm[mm.an==1]; mn=mm[mm.an==0]
pa,loa,hia=wilson(ma.dec.sum(),len(ma)); pn,lon,hin=wilson(mn.dec.sum(),len(mn))
print(f"  Ánimo+ {100*pa:.0f}% [{100*loa:.0f}-{100*hia:.0f}] (n={len(ma)}) vs Ánimo- {100*pn:.0f}% [{100*lon:.0f}-{100*hin:.0f}] (n={len(mn)})")

# ---- estilo Nature ----
plt.rcParams.update({'font.family':'sans-serif','font.sans-serif':['Helvetica','Arial','DejaVu Sans'],
 'font.size':8,'axes.spines.top':False,'axes.spines.right':False,'axes.linewidth':.8,
 'xtick.major.width':.8,'ytick.major.width':.8,'axes.labelsize':8.5,'figure.dpi':300})
TEAL='#0b6b70';CLAY='#b6602c';MOSS='#4c7a58';CRIT='#a23a33';AMBER='#c39433';SLATE='#43648a';GREY='#8a9a9a'

# Figura 1
fig,(ax1,ax2)=plt.subplots(1,2,figsize=(7.2,2.8),gridspec_kw={'width_ratios':[1.25,1]})
labs=['Multidomain','Amnestic','Dysexecutive','Preserved']; cols=[CRIT,CLAY,AMBER,MOSS]
ys=np.arange(len(rows))[::-1]
for i,(ph,n,p,lo,hi) in enumerate(rows):
    ax1.barh(ys[i],100*p,color=cols[i],height=.62,zorder=3)
    ax1.plot([100*lo,100*hi],[ys[i],ys[i]],color='#333',lw=1.1,zorder=4)
    ax1.text(100*hi+2,ys[i],f"{100*p:.0f}%  (n={n})",va='center',fontsize=7.3,color='#333')
ax1.set_yticks(ys); ax1.set_yticklabels(labs); ax1.set_xlim(0,72); ax1.set_xlabel('Baseline-adjusted reliable decline (%)')
ax1.set_title(f'Trajectory by baseline phenotype',fontsize=8.5,loc='left',weight='bold')
ax1.text(0,-1.15,f'χ² p = {pv:.3f}',fontsize=7,color='#555',transform=ax1.get_xaxis_transform())
# panel B storage + mood
grp=['Storage\ncompromised','Storage\npreserved','Mood\nmodulated','No mood\nmodulator']
vals=[pc,pk,pa,pn]; los=[loc,lok,loa,lon]; his=[hic,hik,hia,hin]; ns=[len(scomp),len(scons),len(ma),len(mn)]
colsB=[CLAY,MOSS,MOSS,CLAY]; xs=np.arange(4)
for i in range(4):
    ax2.bar(xs[i],100*vals[i],color=colsB[i],width=.66,zorder=3)
    ax2.plot([xs[i],xs[i]],[100*los[i],100*his[i]],color='#333',lw=1.1,zorder=4)
    ax2.text(xs[i],100*his[i]+2,f"{100*vals[i]:.0f}%",ha='center',fontsize=7,color='#333')
ax2.set_xticks(xs); ax2.set_xticklabels(grp,fontsize=6.6); ax2.set_ylim(0,62); ax2.set_ylabel('Reliable decline (%)')
ax2.set_title('Mechanism & modulator',fontsize=8.5,loc='left',weight='bold')
fig.tight_layout(); fig.savefig(f"{REPO}/Figure1.png",bbox_inches='tight',dpi=300); print("\nFigura1.png guardada")

# Figura 2: forest de AUC
fig2,ax=plt.subplots(figsize=(6.4,2.6))
models=[('MCI → dementia',0.84,0.54,1.0,TEAL),('Pre-dementia → dementia',0.81,0.66,0.93,TEAL),
        ('Reliable decline',0.69,0.48,0.88,SLATE),('Band conversion (honest)',0.66,0.53,0.81,GREY)]
yy=np.arange(len(models))[::-1]
for i,(nm,au,lo,hi,c) in enumerate(models):
    ax.plot([lo,hi],[yy[i],yy[i]],color=c,lw=1.6,zorder=3); ax.scatter([au],[yy[i]],color=c,s=34,zorder=4)
    ax.text(hi+0.01,yy[i],f"{au:.2f} [{lo:.2f}–{hi:.2f}]",va='center',fontsize=7.2,color='#333')
ax.scatter([0.97],[yy[3]],facecolors='none',edgecolors=CRIT,s=34,zorder=4)
ax.text(0.97,yy[3]+0.32,'apparent 0.97 (overfit)',fontsize=6.3,color=CRIT,ha='center')
ax.axvline(0.5,color='#bbb',ls='--',lw=.9); ax.set_yticks(yy); ax.set_yticklabels([m[0] for m in models])
ax.set_xlim(0.45,1.12); ax.set_xlabel('AUC (nested CV, optimism-corrected) with 95% CI')
ax.set_title('Discrimination by outcome',fontsize=8.5,loc='left',weight='bold')
fig2.tight_layout(); fig2.savefig(f"{REPO}/Figure2.png",bbox_inches='tight',dpi=300); print("Figura2.png guardada")
print("\nEPV (events per variable):")
for nm,ev_,k in [('MCI→dem',16,2),('pre-dem→dem',32,3),('declive',34,5)]: print(f"  {nm}: {ev_} eventos / {k} vars = {ev_/k:.1f}")
