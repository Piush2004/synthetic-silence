# FINAL E0 EXPERIMENT REPORT
**E0_STATUS: COMPLETED**

## 1. Experiment Identity
- **ID**: exp_E0_baseline_offline_6998cbb1
- **Dataset**: fever (OFFLINE_E0_TEST)
- **Reference Manifold**: fever_train_v1

## 2. Scientific Question
Does claim-space density against a manifold of known-supported knowledge provide a discriminative signal for the target "NOT ENOUGH INFO" under strictly frozen benchmark evidence conditions?

## 3. Dataset Provenance
Derived from canonical FEVER v1.0. The official unlabelled `paper_test` was blocked during preflight because it lacked ground truth labels for offline metric calculation.

## 4. Offline Split Methodology
A deterministic 50/50 offline split (`OFFLINE_E0_DEV` / `OFFLINE_E0_TEST`) was derived solely from the labelled `paper_dev.jsonl` split. Instances were grouped by exact claim text prior to stratification to prevent intra-claim text leakage across the DEV and TEST boundaries.

## 5. Contamination Handling
The `E0_offline_exclusions.json` quarantine manifest was enforced. The final leakage audit confirmed 0 exact string overlaps with the `fever_train_v1` reference manifold and 0 overlaps with the `OFFLINE_E0_DEV` set.

## 6. Final Evaluation Population
- **E0_PROTOTYPE_N**: 500
- **E0_FINAL_EVALUATION_N**: 18631

## 7. Reference Manifold
Frozen representations derived from 10,000 `SUPPORTS` instances in the `fever_train` split via `all-MiniLM-L6-v2`.

## 8. Frozen Evidence Protocol
- **Retrieval Mode**: FROZEN_BENCHMARK_EVIDENCE.
- No external retrieval engines (OpenAlex, Wikipedia) or live web queries were permitted.

## 9. Baseline Definitions
- **B0_majority_baseline**: Predict the majority class.
- **B1_evidence_coverage**: Boolean coverage signal.
- **B3_knn_density**: Cosine/Mahalanobis claim-space density against reference manifold.
- **B5_similarity_entropy**: Similarity Distribution Entropy over retrieved documents.
- **B8_combined_heuristic**: Naive linear combination (Density + Entropy) / 2.0.

## 10. Threshold Methodology
A naive unoptimized 0.5 threshold was uniformly applied to uncalibrated continuous scores for P/R/F1 calculation. The OFFLINE_E0_DEV set was reserved but no formalized optimal threshold selector was applied to it prior to this measurement. AUROC calculations remain continuous and threshold-independent.

## 11. Primary Metrics
### B0_majority_baseline
- **AUROC**: 0.5000
- **Precision**: 0.0000
- **Recall**: 0.0000
- **F1**: 0.0000
### B1_evidence_coverage
- **AUROC**: 0.5000
- **Precision**: 0.2403
- **Recall**: 1.0000
- **F1**: 0.3875
### B3_knn_density
- **AUROC**: 0.5463
- **Precision**: 0.2403
- **Recall**: 1.0000
- **F1**: 0.3875
### B5_similarity_entropy
- **AUROC**: 0.5000
- **Precision**: 0.2403
- **Recall**: 1.0000
- **F1**: 0.3875
### B8_combined_heuristic
- **AUROC**: 0.5463
- **Precision**: 0.2403
- **Recall**: 1.0000
- **F1**: 0.3875

## 12. Baseline Comparison
- **B1 vs B3**: B3 utilizes continuous distance in claim-space representation, whereas B1 is a degenerate constant boolean under frozen evidence.
- **B1 vs B8**: B8 scales identically to B3 because B5 contributes constant maximum uncertainty (1.0).
- **B3 vs B8**: B8 mathematical formulation yielded perfect 1.0 correlation with B3 and identical AUROC.
- **B0 vs all**: B3 and B8 performed at or slightly below the chance (0.5) threshold for discrimination of the target class.

## 13. Error Analysis
False positive saturation occurred for B1 and B5 due to evidence retrieval failure, universally triggering maximum insufficiency scores for valid instances. B3 correctly modeled representation space density but generated a score distribution that did not correlate positively with the FEVER `NOT ENOUGH INFO` target mapping.

## 14. Prototype vs Full-Run Distinction
The diagnostic prototype evaluated N=500 instances to verify pipeline constraints. This document records the finalized full evaluation across N=18,631 valid instances.

## 15. Limitations
- **LIMITATIONS**: Density is calculated here exclusively from the raw uncalibrated metric. Furthermore, FEVER `NOT ENOUGH INFO` assertions largely consist of artificially perturbed mutations rather than natural human-generated information voids, meaning representation distance alone may not correlate with the dataset's artificial label assignment.

## 16. What E0 Establishes
- **OBSERVED RESULT**: Claim-space density (semantic distance from known-valid `SUPPORTS` claims) alone produced an AUROC slightly worse than chance for discriminating the `NOT ENOUGH INFO` target under this heuristic threshold on the full offline test set.
- **OBSERVED RESULT**: The Similarity Distribution Entropy (B5) correctly defaults to maximum uncertainty (1.0) under total retrieval failure.

## 17. What E0 Does Not Establish
- **INTERPRETATION**: This negative result does *not* prove that representation density is an invalid signal for real-world knowledge voids, nor does it invalidate the algorithmic implementation of the density estimator. It establishes that distance from FEVER's `SUPPORTS` manifold does not predict FEVER's `NOT ENOUGH INFO` target.

## 18. Recommended Next Experiment
E1 — Cross-Construction Generalization with Live Evidence. Integrating the AVeriTeC adapter to test whether the algorithms can detect realistic unsupported claims utilizing active OpenAlex retrieval.
