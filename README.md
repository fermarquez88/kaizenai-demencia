# Dementia progression risk calculator

Open the calculator: https://fermarquez88.github.io/kaizenai-demencia/

A browser-based calculator that estimates the risk of cognitive worsening over about two years from a baseline neuropsychological assessment. It is a single static file (`index.html`): nothing is sent or stored, and the arithmetic runs entirely in the browser. The page opens in English and has a button to switch to Spanish.

**Research prototype.** This is not a medical device, it has not been externally validated and it has not been peer reviewed. It must not be used to make decisions about individual patients.

## What it does

The user selects the severity band stated in the conclusion of the baseline report and enters a small number of scores that can be read directly from that report. Depending on the band, one of three logistic regression models applies:

| Baseline severity band | Outcome modelled | Inputs | Patients / events | AUC (95% CI) |
|---|---|---|---|---|
| Mild cognitive impairment | Progression to the moderate-or-worse band at reassessment | Delayed story recall (z), age | 96 / 18 | 0.76 (0.59 to 0.88) |
| Mild to moderate impairment | Progression to the moderate-or-worse band at reassessment | Delayed story recall (z), age | 140 / 37 | 0.74 (0.63 to 0.83) |
| Normal, or already in the dementia range | Reliable cognitive decline at the next reassessment | Age, Rey list trial 1 (z), intrusions, premorbid IQ estimate (z), Hayling test (z) | 250 / 47 | 0.68 (0.58 to 0.77) |

AUC values are optimism-corrected estimates from repeated nested cross-validation; the intervals are bootstrap 95% confidence intervals on out-of-sample predictions. The output is a Platt-calibrated probability with a per-patient uncertainty band computed from 200 bootstrap models. Given the small number of events, the tool should be read as a relative risk stratifier rather than as an exact individual probability.

The outcome of the two progression models is the severity band written in the reassessment report, not a clinical diagnosis of dementia. Details of the outcome definitions, the modelling and the limitations are in [`MODEL_CARD.md`](MODEL_CARD.md).

## Data provenance, ethics and conflict of interest

The model coefficients were estimated from a retrospective analysis of routine neuropsychological reassessments (2020 to 2026) held by Instituto de Neurociencias San Juan, a private institution in San Juan, Argentina, that the author co-directs. This is declared as a potential conflict of interest.

The analysis used a person-level code in place of names and national identity numbers. This repository contains no individual-level data, identifiers or report text: the only published artefacts are aggregate model coefficients, standardisation constants and bootstrap coefficient sets, all embedded in `index.html`.

The analysis was carried out as internal, retrospective use of routine clinical records under the institution's own data governance. It has no documented review by an independent research ethics committee; that review, together with the institution's written authorisation, will be obtained before the analysis is published or the records are used further. The tool has not been assessed by any regulatory body.

## Limitations

- Single centre, few events per model, wide confidence intervals, no external validation.
- The cohort is made of patients who returned for reassessment, so the estimates apply to that population and not to everyone assessed once.
- The severity bands were extracted from the written conclusions of signed reports with a codebook-constrained language model; agreement with independent clinician adjudication has not yet been assessed.
- No biomarkers and no aetiological information: the models describe a cognitive trajectory, not a disease.

## What is in this repository

```
index.html      the calculator, with the model coefficients embedded
MODEL_CARD.md   model card: data, outcome definitions, validation, limitations, ethics
LICENSE         MIT licence for the code
```

The analysis code reads the institution's internal database and is not published. Patient data are not published and are not available on request from this repository.

## Credit

Fernando Márquez (neurologist, Memory and Brain Health Unit, Hospital Dr. Guillermo Rawson, San Juan, Argentina) wrote the calculator and fitted the models. The assessments and reports from which the models were derived were performed by the neuropsychology team of Instituto de Neurociencias San Juan. The analysis was carried out with colleagues from Universidad Católica de Cuyo, Hospital Dr. Guillermo Rawson and the institute, and has not yet been peer reviewed.

## How to cite

Márquez F, with the neuropsychology team of Instituto de Neurociencias San Juan. Dementia progression risk calculator from a baseline neuropsychological assessment (research prototype, version 1). 2026. https://github.com/fermarquez88/kaizenai-demencia

## Licence

The code is released under the MIT licence (see `LICENSE`). The licence covers the code only; no clinical data are included or licensed.

---

*Calculadora del riesgo de progresión a demencia a partir de la evaluación neuropsicológica basal. Prototipo de investigación, no es un dispositivo médico; no incluye datos de pacientes. La página abre en inglés y tiene un botón para pasar al español.*
