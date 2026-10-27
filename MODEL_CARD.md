# Model card: dementia progression risk calculator

Version 1 (coefficients frozen in August 2026). Research prototype. Not a medical device.

## 1. Model details

- **Developer:** Fernando Márquez (Memory and Brain Health Unit, Hospital Dr. Guillermo Rawson, San Juan, Argentina), with the neuropsychology team of Instituto de Neurociencias San Juan and colleagues from Universidad Católica de Cuyo and Hospital Dr. Guillermo Rawson.
- **Type:** three L2-penalised logistic regression models with class weighting, each followed by Platt recalibration. Inference is implemented in JavaScript inside `index.html`; the coefficients, standardisation constants, Platt parameters and 200 bootstrap coefficient sets per model are embedded in that file and can be inspected directly.
- **Status:** internally validated only; not externally validated; the underlying analysis has not been peer reviewed.

## 2. Intended use

- **Purpose:** to support research and teaching on prognosis after a baseline neuropsychological assessment, by placing a patient in a relative risk band (low, intermediate, high) for cognitive worsening over about two years.
- **Users:** neurologists, neuropsychologists and trainees, in a research or teaching context.
- **Out of scope:** diagnostic or treatment decisions; eligibility for any therapy; use as a medical device; people under 18; patients whose scores fall outside the range of the development cohort (the page flags such inputs); populations assessed with other batteries or norms.

## 3. Inputs

All inputs are values that can be read from a standard neuropsychological report:

| Input | Unit | Used by |
|---|---|---|
| Baseline severity band stated in the report conclusion | ordinal (normal, MCI, mild to moderate, moderate, moderate to severe, severe) | model selection |
| Delayed story recall (logical memory, delayed) | z score | progression models |
| Age | years | all models |
| Rey auditory verbal learning test, trial 1 | z score | reliable decline model |
| Intrusions on the Rey list | count | reliable decline model |
| Premorbid IQ estimate (word accentuation test) | z score | reliable decline model |
| Hayling test | z score | reliable decline model |

Missing inputs are replaced by the development-cohort median of that variable, as was done during model development.

## 4. Outputs

A calibrated probability of the outcome over the follow-up horizon of the development cohort (median about 1.8 years), a 95% uncertainty band from the bootstrap models, a risk band (below 20%, 20% to 40%, above 40%) and the event rate of the development cohort for reference. Because the number of events is small, the output should be read as a relative risk stratum rather than as an exact individual probability.

## 5. Development data

- **Setting:** outpatient neuropsychology service of Instituto de Neurociencias San Juan, a private institution in San Juan, Argentina.
- **Period:** assessments performed between 2020 and 2026.
- **Population:** adults with at least two assessments on different dates. Same-day duplicate reports were removed. Median interval between baseline and reassessment 1.8 years (interquartile range 1.25 to 2.97).
- **Cohorts:** 96 patients with a baseline band of mild cognitive impairment (18 events); 140 patients with a baseline band of mild or mild to moderate impairment (37 events); 250 patients for the reliable decline model (47 events).
- **Missing data:** the memory predictor was missing in 13 of 140 patients (9%) of the main cohort and was imputed with the median inside each cross-validation fold; the complete-case analysis gave a concordant AUC.

## 6. Outcome definitions

- **Progression:** a severity band of "moderate" or worse written in the reassessment report. The bands were extracted from the conclusions of each signed report with a language model constrained by a closed codebook. Two blind extraction runs agreed perfectly on the severity band, but this measures the consistency of the extraction, not agreement with an independent clinician, which has not yet been assessed. The outcome is therefore a severity band, not a clinical diagnosis of dementia. Informant-rated functional status, available for about half of the reassessed patients, was consistent with the bands at the group level only.
- **Reliable decline:** a change in the global z composite between baseline and reassessment that exceeds an empirically derived reliable change index (about 0.97 z).

## 7. Modelling and validation

- Standardisation of predictors, median imputation with missingness indicators and model fitting were all performed inside the cross-validation loop.
- Discrimination was estimated with repeated nested cross-validation (5 folds, 20 repeats) and corrected for optimism by bootstrap; the confidence intervals are bootstrap intervals on out-of-sample predictions. The spread of AUC across folds was wider and is not a confidence interval.
- Calibration: Platt recalibration applied to the deployed models. For the main progression model, calibration slope 0.88 and Brier score 0.21 before recalibration. Observed progression by tercile of predicted risk: about 9%, 26% and 45% (about 47 patients per tercile); negative predictive value about 92%.
- Predictor sets were fixed in advance (delayed story recall and age for progression). Larger variable sets selected by stability selection did not improve optimism-corrected discrimination at this sample size. A gradient boosting model with an apparent AUC of 0.97 fell to about 0.66 after optimism correction and was discarded.

## 8. Full model specification

Predictors are standardised as (value minus mean) divided by SD, using the development-cohort constants below; the linear predictor is intercept plus the sum of coefficient times standardised value; the Platt step applies the sigmoid of A times the linear predictor plus B.

| Model | Predictor | Mean (SD) of development cohort | Coefficient (standardised) |
|---|---|---|---|
| Progression, MCI band (intercept -0.374; Platt A 1.226, B -1.466) | Delayed story recall z | -1.28 (1.29) | -1.069 |
|  | Age, years | 67.1 (13.3) | 0.252 |
| Progression, mild to moderate band (intercept -0.231; Platt A 1.093, B -1.026) | Delayed story recall z | -1.57 (1.26) | -0.946 |
|  | Age, years | 67.8 (12.3) | 0.346 |
| Reliable decline (intercept -0.173; Platt A 1.000, B -1.459) | Age, years | 67.0 (14.3) | 0.197 |
|  | Rey list trial 1 z | -1.07 (1.25) | -0.358 |
|  | Intrusions, count | 4.16 (3.61) | 0.465 |
|  | Premorbid IQ estimate z | -0.12 (0.65) | 0.369 |
|  | Hayling test z | -1.05 (1.42) | -0.238 |

## 9. Performance summary

| Model | Patients / events | AUC, optimism-corrected (95% CI) |
|---|---|---|
| Progression, MCI band | 96 / 18 | 0.76 (0.59 to 0.88) |
| Progression, mild to moderate band | 140 / 37 | 0.74 (0.63 to 0.83) |
| Reliable decline | 250 / 47 | 0.68 (0.58 to 0.77) |

## 10. Limitations and sources of bias

- Single centre; few events, so the intervals are wide, especially for the MCI model.
- Selection: only patients who returned for reassessment are included, and memory clinics tend to re-call those who worsen; the direction of the resulting bias is uncertain. Vital status was not available, so death as a competing risk was not modelled.
- Outcome: a report severity band coded by a language model, not an adjudicated clinical diagnosis; no biomarkers; no aetiology. The models describe a trajectory, not a disease.
- Shared source: the baseline band used for model selection and the outcome band come from the same type of report text, at different time points.
- Documentation drift across years of routine practice (for example in how intrusions are recorded).
- No external validation. Performance in other services, batteries or populations is unknown.

## 11. Data provenance, ethics and conflict of interest

The model coefficients were estimated from a retrospective analysis of routine neuropsychological reassessments held by Instituto de Neurociencias San Juan, a private institution that the developer co-directs. This is declared as a potential conflict of interest.

The analysis used a person-level code in place of names and national identity numbers. This repository contains no individual-level data, identifiers or report text: the only published artefacts are aggregate coefficients, standardisation constants and bootstrap coefficient sets.

The analysis was carried out as internal, retrospective use of routine clinical records under the institution's own data governance. It has no documented review by an independent research ethics committee; that review, together with the institution's written authorisation, will be obtained before the analysis is published or the records are used further. The tool has not been assessed by any regulatory body and must not be used to inform decisions about individual patients.

## 12. Maintenance

The coefficients of version 1 are frozen. Any refit with new data, any change in the outcome definition or any external validation will be released as a new version with its own model card.

## 13. Citation and licence

Márquez F, with the neuropsychology team of Instituto de Neurociencias San Juan. Dementia progression risk calculator from a baseline neuropsychological assessment (research prototype, version 1). 2026. https://github.com/fermarquez88/kaizenai-demencia

Code under the MIT licence. No clinical data are included or licensed.
