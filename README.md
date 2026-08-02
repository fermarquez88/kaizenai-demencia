# Kaizen·AI — Riesgo de progresión a demencia y declive cognitivo

## ▶️ [**ABRIR LA APP**](https://fermarquez88.github.io/kaizenai-demencia/)
### 🔗 https://fermarquez88.github.io/kaizenai-demencia/

> Calculadora de riesgo individualizada a ~2 años a partir de la evaluación neuropsicológica **basal**,
> entrenada con datos longitudinales reales del **Instituto de Neurociencias San Juan (Clínica El Castaño)**
> y normada localmente. **Prototipo de investigación — NO es un dispositivo médico.**

**Idiomas:** Español / English · **100% client-side** (los datos no salen del navegador)

---

## Qué hace

Dada la severidad del perfil basal, la app muestra **un** modelo pronóstico y pide **solo los puntajes que se
leen del informe** (z de la tabla + intrusiones de la nota + edad). Devuelve la **probabilidad de empeoramiento**
con su **banda de incertidumbre (IC95%)** y el respaldo científico.

| Severidad basal | Modelo | Variables | AUC (CV anidada, optimismo-corregido) |
|---|---|---|---|
| Leve-moderado (primario) | Progresión a demencia (severidad clínica) | Memoria de Relatos Diferido (z) + edad | **0.74** [0.63–0.83] |
| DCL (sensibilidad) | Progresión a demencia (severidad clínica) | Memoria de Relatos Diferido (z) + edad | **0.76** [0.59–0.88] |
| Normal / Moderado+ | Declive cognitivo fiable | edad, Rey Trial-1, intrusiones, CI premórbido, Hayling | 0.68 [0.58–0.77] |

> **Desenlace = progresión a demencia** (severidad clínica ≥ moderada, **corroborada funcionalmente** por el ADLQ del informante; sin biomarcadores). IC95% bootstrap. El modelo estratifica riesgo relativo (terciles 9%/26%/45%; VPN 92%). Detalle y análisis exploratorios en [material suplementario](suplementario/SUPLEMENTARIO.md).

Desenlace = **progresión a demencia** definido como severidad del perfil ≥ *moderado* en la reevaluación
(criterio clínico del instituto). *Declive fiable* = cambio z que supera el índice de cambio fiable (RCI) local.

## Cómo funciona (arquitectura)

- **100% client-side.** Los modelos son **regresiones logísticas**; sus coeficientes viven en
  [`models/models_deploy.json`](models/models_deploy.json) y el cálculo se hace en el navegador (JavaScript).
- **Privacidad por diseño:** ningún dato del paciente sale del dispositivo — no hay backend.
- **Incertidumbre por paciente:** la banda IC95% se computa con **200 modelos bootstrap** exportados.
- **Auditable:** los coeficientes son inspeccionables; la matemática del JS reproduce exactamente a
  `scikit-learn` (test de paridad en `src/build_deploy_final.py`).

## Rigor científico (resumen)

- **Cohorte:** reevaluaciones reales (≥2 fechas, dedup mismo-día), adulto. n≈85–250 según modelo.
- **Selección de variables:** *stability selection* (Meinshausen-Bühlmann) + comparación de sets fijos a priori.
  A este tamaño muestral, **la parsimonia gana**: los mejores modelos usan 2–5 variables.
- **Validación:** CV anidada 5×20 + **optimismo-corregido (Steyerberg)** + LOOCV + **calibración Platt**.
- **Honestidad:** se reportan AUC optimismo-corregidos, IC95%, y las limitaciones (pocos eventos, sin validación externa).
  Un modelo previo con Random Forest fue descartado por sobreajuste (AUC aparente 0.97 → honesto ~0.66).

Ver [`MODEL_CARD.md`](MODEL_CARD.md) y [`METHODS.md`](METHODS.md).

## Estructura

```
index.html                app autónoma (calculadora + respaldo científico)
models/models_deploy.json  coeficientes + calibración + 200 bootstrap por modelo
src/                       código de análisis y modelado (reproducible)
MODEL_CARD.md              tarjeta del modelo
METHODS.md                 metodología y derivación de variables
```

⚠️ **Los datos de pacientes NO se incluyen** (contienen PII). El código lee de `data/`/`db/` que están en
`.gitignore`. Para reproducir hay que tener acceso autorizado a la base del instituto.

## Advertencia

Herramienta **investigacional/educativa**. Predice **trayectoria cognitiva**, no enfermedad, y **no asigna
diagnóstico etiológico**. Las cifras son exploratorias e hipótesis-generadoras. **No debe usarse para decisiones
clínicas.** Requiere validación externa antes de cualquier uso asistencial.

## Cita

Kaizen·AI — Instituto de Neurociencias San Juan (Clínica El Castaño), 2026. Prototipo v1.

## Licencia

Código bajo licencia MIT (ver [`LICENSE`](LICENSE)). Los datos clínicos NO están licenciados ni incluidos.
