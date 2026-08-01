"""
BLOQUE 2 — Reoperacionalización de subtipos de DCL con criterios OPERATIVOS de
Petersen (1999) / Winblad (2004), no desde la etiqueta narrativa dominante.

Motivación (auditoría de revisor):
  La Figura 3 actual clasificaba por `perfil_patron` (etiqueta dominante) × flag
  `multidominio`, lo que (a) fuerza cada caso a UN fenotipo y (b) excluye a
  `multidominio_global`, `mixto`, `preservado`... mandándolos a 'otro'. Eso NO es
  la operacionalización de Petersen/Winblad, que se define por el PATRÓN OBJETIVO
  de dominios afectados: memoria (sí/no) × nº de dominios (único/múltiple).

Operacionalización (dos lentes, triangulación):
  A) OBJETIVA (z): dominio afectado si z_peor <= -1.5 (≥1 test); memoria afectada
     define amnésico; nº dominios afectados (entre los 5 core) define único/múltiple.
     -> aMCI-DU, aMCI-DM, naMCI-DU, naMCI-DM, y "sin deterioro objetivo" (posible
        falso positivo tipo Petersen/Winblad, cf. Jak-Bondi 2014).
  B) NARRATIVA por dominios: usa los flags dom_* explícitos del informe (no la
     etiqueta única) -> misma grilla. Sirve de concordancia clínica.

Cohorte en riesgo: reevaluados, basal DCL/leve-moderado (sev basal ∈ {leve, leve-mod}),
  excluyendo normales (no en riesgo a corto plazo) y ya-demencia (basal ≥ moderado).
Desenlace: progresión a demencia = severidad final ≥ moderado.
"""
import warnings, os; warnings.filterwarnings('ignore')
import duckdb, numpy as np, pandas as pd
from scipy.stats import chi2_contingency, fisher_exact

SEV = {'normal':0,'leve':1,'leve_moderado':2,'moderado':3,'moderado_grave':4,'grave':5}
CORE = ['memoria','atencion','funciones_ejecutivas','lenguaje','visuoespacial']
UMBRAL = -1.5

con = duckdb.connect('db/evaluaciones_v2.duckdb', read_only=True)
ev = con.execute("SELECT eval_id,persona_id,fecha_ev,edad FROM evaluaciones_v2 WHERE cohorte<>'wisc_v'").df()
de = con.execute("SELECT eval_id,dominio,z_peor FROM dominio_eval").df()
pc = con.execute("""SELECT eval_id,persona_id,fecha_ev,perfil_severidad,perfil_patron,multidominio,
                    dom_memoria,dom_atencion,dom_funciones_ejecutivas,dom_lenguaje,
                    dom_visuoespacial_construccional,mem_almacenamiento FROM perfil_conclusiones""").df()
con.close()

# --- orden temporal por persona (primera vs última fecha) ---
ev['f'] = pd.to_datetime(ev.fecha_ev, errors='coerce')
ev = ev.dropna(subset=['f']).sort_values(['persona_id','f']).drop_duplicates(['persona_id','f'])
ev['t'] = ev.groupby('persona_id').f.rank(method='dense')
ev = ev[ev.groupby('persona_id').t.transform('max') >= 2]          # reevaluados reales
first = ev.sort_values('t').groupby('persona_id').first().reset_index()
last  = ev.sort_values('t').groupby('persona_id').last().reset_index()

# severidad basal y final (desde perfil_conclusiones, alineado por persona+fecha)
pc['f'] = pd.to_datetime(pc.fecha_ev, errors='coerce')
pc['s'] = pc.perfil_severidad.map(SEV)
psev = pc.dropna(subset=['f','s']).sort_values(['persona_id','f']).drop_duplicates(['persona_id','f'])
psev['t'] = psev.groupby('persona_id').f.rank(method='dense')
psev = psev[psev.groupby('persona_id').t.transform('max') >= 2]
sb = psev.sort_values('t').groupby('persona_id').first().s          # basal
sl = psev.sort_values('t').groupby('persona_id').last().s           # final

# --- perfil objetivo por dominio en el BASAL ---
zw = de.assign(z=lambda x: x.z_peor.clip(-6,4))
zwide = zw[zw.dominio.isin(CORE)].pivot_table(index='eval_id', columns='dominio', values='z', aggfunc='min')
# base = eval basal de cada persona
base = first[['persona_id','eval_id','edad']].rename(columns={'eval_id':'eb'})
base = base.merge(zwide, left_on='eb', right_index=True, how='left')
# flags narrativos + almacenamiento del basal
pcb = pc.drop_duplicates('eval_id').set_index('eval_id')
for col in ['dom_memoria','dom_atencion','dom_funciones_ejecutivas','dom_lenguaje',
            'dom_visuoespacial_construccional','mem_almacenamiento','perfil_patron','multidominio']:
    base[col] = base.eb.map(pcb[col])
base['sb'] = base.persona_id.map(sb); base['sl'] = base.persona_id.map(sl)
base['y_dem'] = (base.sl >= 3).astype('float')

def tobool(x):
    if pd.isna(x): return np.nan
    if isinstance(x,(bool,np.bool_)): return bool(x)
    return str(x).strip().lower() in ('true','1','si','sí','t')

# ---------- A) subtipo OBJETIVO (z <= -1.5) ----------
def subtipo_objetivo(row, umbral=UMBRAL):
    zs = {d: row.get(d) for d in CORE}
    presentes = {d:v for d,v in zs.items() if pd.notna(v)}
    if len(presentes) < 3:               # cobertura insuficiente
        return np.nan, np.nan, np.nan
    afectados = [d for d,v in presentes.items() if v <= umbral]
    n = len(afectados); mem = 'memoria' in afectados
    if n == 0: return 'Sin deterioro objetivo', mem, n
    perfil = 'a' if mem else 'na'
    dom = 'DU' if n == 1 else 'DM'
    lab = {'a':'Amnésico','na':'No amnésico'}[perfil] + (' dominio único' if dom=='DU' else ' multidominio')
    return lab, mem, n

res = base.apply(lambda r: pd.Series(subtipo_objetivo(r), index=['sub_obj','mem_obj','n_obj']), axis=1)
base = pd.concat([base, res], axis=1)

# ---------- B) subtipo NARRATIVO por dominios (flags dom_*) ----------
domflags = {'memoria':'dom_memoria','atencion':'dom_atencion','funciones_ejecutivas':'dom_funciones_ejecutivas',
            'lenguaje':'dom_lenguaje','visuoespacial':'dom_visuoespacial_construccional'}
def subtipo_narrativo(row):
    fl = {d: tobool(row.get(c)) for d,c in domflags.items()}
    if all(pd.isna(v) for v in fl.values()): return np.nan
    af = [d for d,v in fl.items() if v is True]
    n = len(af); mem = 'memoria' in af
    if n == 0: return 'Sin dominios (narrativa)'
    perfil = 'Amnésico' if mem else 'No amnésico'
    return perfil + (' dominio único' if n==1 else ' multidominio')
base['sub_nar'] = base.apply(subtipo_narrativo, axis=1)

def wilson(k,n):
    if n==0: return (np.nan,np.nan,np.nan)
    p=k/n; z=1.96; d=1+z*z/n; c=(p+z*z/2/n)/d; h=z*np.sqrt(p*(1-p)/n+z*z/4/n/n)/d
    return p,max(0,c-h),min(1,c+h)

def tabla(df, col, titulo, order=None):
    print(f"\n{'='*74}\n{titulo}\n{'='*74}")
    d = df.dropna(subset=[col,'y_dem'])
    cats = order or sorted(d[col].unique())
    rows=[]
    for c in cats:
        s = d[d[col]==c]; k=int(s.y_dem.sum()); n=len(s); p,lo,hi=wilson(k,n)
        if n>0:
            print(f"  {c:32s} {k:3d}/{n:3d}  {100*p:5.1f}%  [{100*lo:4.0f}–{100*hi:4.0f}]")
            rows.append((c,k,n,p))
    # chi2 sobre las categorías de deterioro (excluye 'Sin...') con celdas suficientes
    det = [r for r in rows if not str(r[0]).startswith('Sin')]
    if len(det)>=2:
        tab = np.array([[r[1], r[2]-r[1]] for r in det])
        try:
            chi2,pp,_,_ = chi2_contingency(tab)
            print(f"  --> χ²={chi2:.2f}, p={pp:.3f}  (categorías con deterioro: {[r[0] for r in det]})")
        except Exception as e:
            print("  chi2 n/a", e)
    return d

# ---------- Cohorte en riesgo: basal DCL/leve-moderado ----------
riesgo = base[base.sb.isin([1,2])].copy()
print(f"\nCohorte reevaluada total: {base.persona_id.nunique()}")
print(f"En riesgo (basal leve/leve-mod, sb∈{{1,2}}): n={len(riesgo)}  eventos demencia={int(riesgo.y_dem.sum())}")
print(f"Cobertura subtipo objetivo: {riesgo.sub_obj.notna().sum()}/{len(riesgo)}")

ORD_OBJ = ['Amnésico multidominio','No amnésico multidominio','Amnésico dominio único',
           'No amnésico dominio único','Sin deterioro objetivo']
ORD_NAR = ['Amnésico multidominio','No amnésico multidominio','Amnésico dominio único',
           'No amnésico dominio único','Sin dominios (narrativa)']

tabla(riesgo, 'sub_obj', "A) SUBTIPO OBJETIVO (z≤−1.5, batería) — cohorte basal leve/leve-mod", ORD_OBJ)
tabla(riesgo, 'sub_nar', "B) SUBTIPO NARRATIVO por dominios (flags dom_*) — misma cohorte", ORD_NAR)

# ---------- C) reproducir la versión ACTUAL (perfil_patron × multidominio) ----------
riesgo['multi'] = riesgo.multidominio.map(lambda x: tobool(x))
def grupo_actual(r):
    if r.perfil_patron=='amnesico': return 'Amnésico multidominio' if r.multi else 'Amnésico dominio único'
    if r.perfil_patron=='disejecutivo': return 'Disejecutivo/atencional'
    return 'otro (excluido)'
riesgo['sub_actual'] = riesgo.apply(grupo_actual, axis=1)
tabla(riesgo, 'sub_actual', "C) VERSIÓN ACTUAL del manuscrito (etiqueta perfil_patron) — para contraste",
      ['Amnésico multidominio','Disejecutivo/atencional','Amnésico dominio único','otro (excluido)'])

# ---------- D) Concordancia objetivo vs narrativa (amnésico sí/no) ----------
c = riesgo.dropna(subset=['mem_obj'])
mem_nar = c.dom_memoria.map(tobool)
ok = (c.mem_obj == mem_nar)
print(f"\nConcordancia 'memoria afectada' objetivo(z) vs narrativa(dom_memoria): "
      f"{ok.mean()*100:.0f}% (n={ok.notna().sum()})")

# ---------- E) Almacenamiento comprometido dentro del amnésico OBJETIVO ----------
amn = riesgo[riesgo.mem_obj==True]
alm = amn.mem_almacenamiento.map(tobool)
print(f"Almacenamiento comprometido entre amnésicos OBJETIVOS: "
      f"{int(alm.sum())}/{alm.notna().sum()} = {100*alm.mean():.0f}%")

# ---------- F) Sensibilidad umbral z≤−1.0 ----------
res10 = base.apply(lambda r: pd.Series(subtipo_objetivo(r,-1.0), index=['s10','m10','n10']), axis=1)
riesgo10 = pd.concat([base, res10], axis=1)
riesgo10 = riesgo10[riesgo10.sb.isin([1,2])]
tabla(riesgo10, 's10', "F) SENSIBILIDAD umbral z≤−1.0 (objetivo)", ORD_OBJ)

# guardar dataset por si se necesita
riesgo.to_csv('data/interim/subtipos_petersen_reanalisis.csv', index=False)
print("\n[guardado] data/interim/subtipos_petersen_reanalisis.csv")
