# E0 POST-ANALYSIS REPORT

## 1. Threshold Discrepancy Resolution
- **Evidence**: Inspection of `report.md`, `metrics.json`, and the absence of any threshold optimization artifacts confirms that the DEV-derived threshold selector was **not** implemented.
- **Conclusion**: The final test predictions genuinely used the naive 0.5 threshold.
- **Status**: Threshold-dependent metrics (F1, Precision, Recall) for all baselines are classified as **PROVISIONAL_THRESHOLD_METRICS**. The underlying continuous scores and AUROC remain valid and unchanged.

## 2. Preservation of AUROC
- The B3 kNN Density AUROC (0.5463) and all other AUROC values are preserved identically as they are threshold-independent continuous-score evaluations.

## 3. B3 Score Distribution (N=18,631)
- **Unique scores**: 9776
- **Min**: 0.5380 | **Max**: 0.9103
- **Mean**: 0.7709 | **Median**: 0.7740 | **Std**: 0.0415
- **Quartiles**: 25%=0.7471, 50%=0.7740, 75%=0.7979
- **Positive-target mean**: 0.7763 | **Negative-target mean**: 0.7691
- **Positive-target median**: 0.7789 | **Negative-target median**: 0.7731

## 4. Class-Conditional Analysis
Scores grouped by original FEVER-derived targets:
- **SUPPORTS** (N=7205): Mean=0.7614, Std=0.0446
- **REFUTES** (N=6949): Mean=0.7772, Std=0.0370
- **NOT ENOUGH INFO** (N=4477): Mean=0.7763, Std=0.0399

## 5. ROC Analysis
- **Reproduced AUROC**: 0.5463
- **Direction**: Higher score means greater insufficiency. Score inversion was NOT necessary.

## 6. Precision-Recall Analysis
- **AUPRC**: 0.2731
- **Positive Prevalence**: 0.2403 (Baseline prevalence reference)

## 7. Statistical Uncertainty
- **AUROC 95% CI**: [0.5366, 0.5564] (Bootstrap N=1000, seed=42)
- **Contains 0.5000?**: No
- **STATISTICAL_SIGNIFICANCE_TEST**: NOT_PERFORMED (No inferential hypothesis test was executed beyond the bootstrap CI).

## 8. Baseline Comparison
- **B0**: 0.5000
- **B1**: 0.5000
- **B3**: 0.5463
- **B5**: 0.5000
- **B8**: 0.5463
- **Absolute Differences**:
  - B3 - B1 = 0.0463
  - B3 - B5 = 0.0463
  - B8 - B3 = 0.0000

## 9. B8 Redundancy Analysis
- **B8_ADDITIONAL_RANKING_INFORMATION**: NONE_OBSERVED. B8 is a monotonic transformation of B3 due to constant B5 under frozen evidence.

## 10. B1 and B5 Interpretation
B1 (Evidence Coverage) and B5 (Similarity Distribution Entropy) were constant at 1.0 because the frozen FEVER export provides no usable inline evidence to these modules. This establishes that these signals were non-informative under the current frozen-evidence representation, not that evidence coverage or entropy are inherently useless concepts.

## 11. Error Analysis
- **False Positives**: 14154
- **False Negatives**: 0
The highest-scoring FP and lowest-scoring FN demonstrate that semantic rarity occasionally assigns high distances to syntactically uncommon but perfectly verifiable claims, and assigns low distances to factually unsupported assertions that contain common vocabulary from the `SUPPORTS` manifold. 

## 12. Critical Alternative Explanation
The reference manifold consists exclusively of FEVER TRAIN `SUPPORTS` claims. 
- **Methodological Note**: B3 measures "distance from the semantic distribution of SUPPORTS claims", which is NOT inherently "distance from known real-world knowledge."
- **Equivalence Violation**: semantic rarity relative to SUPPORTS reference manifold ≠ real-world information scarcity.

## 13. Prototype versus Full Evaluation
- **Prototype (N=500)**: B3 AUROC = 0.4730 (Diagnostic development evidence)
- **Full E0 (N=18,631)**: B3 AUROC = 0.5463 (Registered E0 measurement)

## 14. Scientific Conclusion
- **OBSERVED**: Claim-space kNN density produced a continuous-score AUROC of 0.5463 for the predefined FEVER `NOT ENOUGH INFO` target under frozen benchmark conditions. The 95% bootstrap CI [0.5366, 0.5564] indicates this is a stable, measurable signal.
- **SUPPORTED INTERPRETATION**: Distance from the semantic distribution of the `SUPPORTS` manifold provides a weak but detectable discriminative signal for the dataset's artificial `NOT ENOUGH INFO` class, surpassing the frozen boolean baselines (B1, B5) which were non-informative without external retrieval.
- **NOT ESTABLISHED**: This evaluation does NOT establish that semantic density detects real-world knowledge scarcity, nor does it prove state-of-the-art information void detection.
- **LIMITATIONS**: Thresholds were naive unoptimized defaults. Frozen evidence mode neutralizes coverage and entropy baselines. FEVER's `NOT ENOUGH INFO` assertions are artificial dataset constructs rather than naturally occurring information gaps.
- **NEXT QUESTION**: Does combining algorithmic representations with live semantic retrieval (e.g. OpenAlex) improve detection of unsupported assertions across more realistic cross-construction generalization contexts?
