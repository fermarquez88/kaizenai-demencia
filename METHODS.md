# Métodos

## 1. Cohorte y saneamiento
- Fuente: reevaluaciones neuropsicológicas del Instituto de Neurociencias San Juan (2020–2026), datos del mundo real.
- Identidad por **DNI** (nunca por nombre → evita homónimos y capta cambios de apellido).
- **Reevaluación real** = ≥2 evaluaciones en **fechas distintas**. Se descartan duplicados del mismo día
  (mismo informe archivado con el nombre en distinto orden).
- Intervalo de seguimiento: mediana ~1.8 años.

## 2. Desenlaces (targets)
Escala de severidad codificada del perfil (de la sección "Conclusiones"):
`normal(0) < DCL/leve(1) < leve-moderado(2) | moderado(3) < moderado-grave(4) < grave(5)`.
- **Progresión a demencia:** severidad final ≥ *moderado* (criterio clínico del instituto).
- **Declive fiable:** cambio z global entre basal y reevaluación que supera el **índice de cambio fiable (RCI)**
  empírico local (RCI ≈ 1.96 · MAD de los pares estables ≈ 0.97 z).

## 3. Variables y **derivaciones** (transparencia)
La app desplegada usa **solo variables leíbles del informe** (no requiere que el clínico derive nada). El
*análisis*, en cambio, exploró variables derivadas; se documentan aquí para reproducibilidad:

| Variable | Origen | Derivación |
|---|---|---|
| z por test (ej. Memoria de Relatos Diferido, Rey Trial-1, WAT, Hayling) | tabla del informe | directo (z impreso) |
| intrusiones | nota/narrativa del informe | conteo directo |
| edad, educación | encabezado | directo |
| severidad basal | sección "Conclusiones" | codificación (ver abajo) |
| z de dominio ("peor-z") | batería | mínimo (peor) z entre los tests del dominio |
| z global | batería | media de los peor-z de 5 dominios core |
| dispersión | batería | desvío estándar entre dominios |
| gap normativo | batería + demografía | residuo de un modelo z ~ edad+educación (HGB) sobre la cohorte completa |
| d′, criterio C | reconocimiento (RAVLT) | teoría de detección de señales: d′ = Φ⁻¹(hits/targets) − Φ⁻¹(FA/foils) |
| perfil (severidad/patrón/almacenamiento/…) | "Conclusiones" | codificación por LLM con codebook; fiabilidad inter-codificador κ (severidad 1.00) validada contra el z objetivo |

> Los **modelos finales** (los desplegados) usan únicamente: Memoria de Relatos Diferido, edad, severidad,
> Rey Trial-1, intrusiones, WAT, Hayling — todo transcribible del informe. Las derivadas anteriores **no** se
> usan en producción (no mejoraron el AUC honesto a este n).

## 4. Feature engineering y selección de variables
- Espacio completo (~40 variables) evaluado con **stability selection** (Meinshausen-Bühlmann): frecuencia de
  selección por L1 sobre 120 bootstraps.
- **Hallazgo clave:** a 16–32 eventos, la selección sobre un espacio grande **sobreajusta**; los mejores modelos
  honestos son **parsimoniosos** (2–5 variables). La stability selection confirmó las variables robustas
  (memoria diferida, edad, criterio C, Hayling) pero ningún modelo grande superó al parsimonioso.
- ⚠️ Nota metodológica: la "mejora" aparente de un modelo cuya selección se hace sobre todo el dataset es
  **fuga de selección**; los AUC reportados provienen de sets fijos a priori o de selección **dentro** de cada fold.

## 5. Entrenamiento y validación
- Modelos: **regresión logística penalizada** (L1 para selección; L2 para el modelo desplegado, coeficientes estables),
  con `class_weight='balanced'`. Comparación con HistGradientBoosting (descartado por sobreajuste en desenlaces con
  no-linealidad débil; AUC aparente 0.97 → honesto ~0.66 en conversión).
- **Validación:** CV anidada `RepeatedStratifiedKFold` 5×20 + tuning interno; **optimismo-corregido (Steyerberg,
  bootstrap)**; **LOOCV** en cohortes chicas; **calibración Platt** (Brier, pendiente/intercepto, ECE).
- **Preprocesamiento** (imputación mediana + indicador de faltante, estandarización) **dentro** de la CV (sin fuga).
- Bandas de incertidumbre por paciente: 200 modelos bootstrap exportados a JSON.

## 6. Despliegue
- Coeficientes + calibración Platt + bootstraps exportados a `models/models_deploy.json`.
- Inferencia **client-side** en JavaScript; **test de paridad** (JS == scikit-learn) en `src/build_deploy_final.py`.
- Sin backend → los datos del paciente no se transmiten.

## 7. Limitaciones
n pequeño (pocos eventos, IC amplios), sin validación externa, sin biomarcadores, sin etiología, sesgo de
selección (quién se reevalúa), y deriva de documentación propia de los datos del mundo real. **Prototipo.**
