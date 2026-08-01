# Critical peer review (self-audit as a *Neurology* reviewer) and point-by-point resolution

> We audited the manuscript as a critical *Neurology* reviewer would, re-ran the analyses the critique demanded
> (with confidence intervals and formal tests), and revised the manuscript accordingly. Below: each concern, the
> evidence, and how it was addressed.

## Major concerns

**M1 — Overstated Classification of Evidence.** The manuscript claimed Class II. This is a single-center,
retrospective study with a **16-event** primary model, internally validated only. *Resolution:* downgraded to
**exploratory (Class IV)**; “prototype requiring external validation” stated throughout; the Classification-of-Evidence
sentence rewritten.

**M2 — Outcome validity (“moderate = dementia”).** Dementia requires functional impairment (DSM-5/NIA-AA); a severity
label from a report is a proxy that conflates severity with syndrome. *Resolution:* outcome reframed as **“progression
to moderate-or-greater cognitive impairment (a dementia-level syndrome by the institute’s clinical criterion)”**; the
absence of an independent functional criterion added as a key limitation; **sensitivity analysis** added (events fall
from 32 at ≥moderate to **9** at ≥moderate-severe and **4** at severe, i.e., stricter thresholds are unestimable here).

**M3 — Unstable phenotype-subgroup estimates.** Re-analysis with 95% CIs showed the phenotype decline rates are
**fragile** across analytic choices and have wide CIs (small subgroups). *Resolution:* Figure 1 now reports **Wilson
95% CIs** and an **omnibus χ² (p=0.030)**; the narrative is tempered to a single robust claim—**the amnestic phenotype
carries the highest reliable-decline rate (47%, 95% CI 35–59)**—with the ordering of the remaining phenotypes described
as uncertain.

**M4 — Mechanism (storage) claim not statistically supported.** Re-computation: impaired vs preserved storage 38% vs
26%, **OR 1.7, p=0.197 (NS)** (the earlier 44% vs 18% did not survive a proper contingency test). *Resolution:* claim
softened to “numerically higher but not statistically significant”; presented with CIs.

**M5 — “No normal→dementia” underpowered.** The denominator is only **n=14** baseline-normal patients (0/14).
*Resolution:* denominator reported explicitly and the claim reframed as “no observed transitions among 14 normals,
consistent with—but underpowered to prove—a staged model.”

**M6 — Low events-per-variable / overfitting.** EPV = 6.8–10.7 (MCI model 8.0; reliable-decline 6.8), below the
conventional ≥10. The MCI model’s CI (0.54–1.0) is nearly uninformative at its lower bound. *Resolution:* EPV reported;
“prototype” framing reinforced; discrimination presented as optimism-corrected with explicit CIs (Figure 2).

**M7 — Method dependency / potential circularity.** Baseline severity (a predictor) and the outcome (final severity)
are coded from the same report section by the same automated process (shared-method variance), though at different
timepoints. *Resolution:* independence-by-timepoint stated; shared-method variance and single-source coding added as a
limitation; construct validity against the independent z-score reference emphasized.

**M8 — Selection/attrition and informative censoring.** Only patients who returned are analyzed; competing risk of
death is unmodeled; a binary outcome ignores variable follow-up time. *Resolution:* strengthened limitation; a
time-to-event (discrete-time survival) analysis flagged as the required next step.

**M9 — Informal superiority claim.** “Outperforms published models” compares across different cohorts. *Resolution:*
changed to **“comparable to”** published neuropsychology-only models.

## Minor concerns
- Missing TRIPOD items (participant flow, full model equation/intercept, missing-data detail) → model coefficients are
  released openly in `models/models_deploy.json`; flow described in Results; imputation specified in Methods.
- No calibration plot → calibration slope/intercept and Brier reported; recalibration (Platt) stated.
- Single center/single coding scheme → added to limitations.
- Multiplicity from model search → addressed by nested CV + bootstrap optimism correction; stated.

## Net effect
The revision **removes over-claims**, adds **inferential statistics and CIs**, corrects two results that did not
survive proper testing (storage mechanism; phenotype ordering), reports the **true denominators**, and repositions the
work as a rigorous **exploratory** study with an openly deployed prototype—strengths that remain: real-world data,
highly reliable profile coding, honest internal validation, and full open code.
