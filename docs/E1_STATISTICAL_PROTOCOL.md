# E1 Statistical and Threshold Protocol

## 1. No Test-Set Tuning
All thresholds and model-selection decisions must be made exclusively using development data.
- **NEVER** use E1 test labels or test error patterns to adjust parameters.
- Use a strictly frozen threshold for the final evaluation step.

## 2. Formal Threshold Protocol
Unlike E0, E1 **MUST** implement a formal threshold protocol prior to test evaluation.
- **Method**: Youden's J statistic (Maximize Sensitivity + Specificity - 1).
- **Procedure**:
  1. Generate continuous scores on the designated `DEV` split.
  2. Calculate Youden's J across the ROC curve to select the optimal cutoff.
  3. Freeze the selected threshold.
  4. Apply the frozen threshold to the `TEST` split to calculate Precision, Recall, and F1.

*Note: AUROC and AUPRC remain threshold-independent continuous evaluations.*

## 3. Statistical Analysis Requirements
E1 must not rely solely on point estimates. For every construction evaluation, calculate and report:
- **AUROC**
- **AUPRC**
- **Positive Prevalence** (Base rate)
- **Sample Size (N)**
- **Bootstrap Confidence Interval**: 95% CI for AUROC using empirical bootstrapping (e.g., N=1000, fixed seed=42).

## 4. Primary E1 Generalization Metric
To prevent narrative optimization, the primary generalization metric is pre-registered as:
**Median AUROC across all held-out constructions evaluated on the target reference manifold.**

## 5. Statistical Discipline
- Do **NOT** call AUROC differences "statistically significant" unless a formal inferential test (e.g., DeLong's test or a paired permutation test) is successfully executed. 
- If a formal test is absent, the report must state: `STATISTICAL_SIGNIFICANCE_TEST: NOT_PERFORMED`.
- Cross-construction comparisons will report heterogeneity descriptively. We will not invent a universal significance threshold.
