# Model Card — Kaizen·AI (progresión a demencia / declive cognitivo)

## Uso previsto
- **Propósito:** estimar el riesgo individual de empeoramiento cognitivo a ~2 años desde la evaluación
  neuropsicológica basal, como apoyo a la **investigación** y a la reflexión clínica.
- **Usuarios:** neurólogos/as y neuropsicólogos/as (contexto de investigación).
- **NO previsto:** decisiones diagnósticas o terapéuticas; uso como dispositivo médico; poblaciones pediátricas
  (excluidas); pacientes fuera del rango de entrenamiento.

## Modelos
Tres modelos logísticos, condicionados por la severidad basal del perfil:

| Modelo | Cohorte | Variables | n / eventos | AUC (optimismo-corr.) | IC95% |
|---|---|---|---|---|---|
| Demencia · DCL leve | severidad basal = DCL leve | Memoria de Relatos Diferido (z), edad | 85 / 16 | 0.84 | 0.54–1.0 |
| Demencia · pre-demencia | basal normal/leve/leve-mod | Memoria de Relatos Diferido (z), edad, severidad | 136 / 32 | 0.81 | 0.66–0.93 |
| Declive fiable | todos los reevaluados | edad, Rey Trial-1 (z), intrusiones, WAT (z), Hayling (z) | 182 / 34 | 0.69 | 0.48–0.88 |

- **Desenlace demencia:** severidad del perfil ≥ *moderado* en la reevaluación (criterio clínico del instituto).
- **Desenlace declive:** cambio z global que supera el índice de cambio fiable (RCI) empírico local (≈0.97 z).
- **Calibración:** Platt/sigmoid; se reporta banda de incertidumbre por 200 bootstraps.

## Datos de entrenamiento
- Reevaluaciones neuropsicológicas reales (RWD) del Instituto de Neurociencias San Juan, 2020–2026.
- Cohorte longitudinal saneada: pacientes con ≥2 evaluaciones en fechas distintas (dedup de duplicados
  del mismo día). Perfil codificado desde la sección "Conclusiones" (fiabilidad inter-codificador κ: severidad 1.00).
- **PII:** no incluida en este repositorio.

## Evaluación
- **Discriminación:** AUC por CV anidada (5×20) + optimismo-corregido (Steyerberg) + LOOCV.
- **Calibración:** curva de calibración, Brier, pendiente/intercepto; recalibración Platt.
- **Selección de variables:** stability selection + comparación de sets fijos; parsimonia favorecida por el n.

## Factores y limitaciones
- **Tamaño muestral pequeño** (16–34 eventos) → intervalos de confianza amplios; el modelo de DCL leve es un
  **prototipo** con IC muy ancho.
- **Sesgo de selección:** generaliza a la población que **se reevalúa** (más añosa; gradiente de acceso).
- **Sin validación externa.** Sin biomarcadores. Sin etiología (predice trayectoria, no enfermedad).
- **Deriva de documentación** en RWD (p.ej. cambios en el reporte de confabulaciones entre épocas).
- **Definición del desenlace** ("moderado = demencia") asume criterio clínico del instituto; el compromiso
  funcional no se verifica de forma independiente.

## Consideraciones éticas
- Herramienta de investigación; **no** debe guiar decisiones clínicas sin validación prospectiva y externa.
- Cómputo local (sin transmisión de datos) para proteger la privacidad.
- La recalibración periódica ("norma viva") y la validación en ReDLat son pasos necesarios antes de cualquier uso real.
