# 4. RESULTS

## 4.1 Frozen E0 Evaluation
The baseline evaluation was performed on the established FEVER-derived dataset comprising 18,631 instances, utilizing frozen evidence retrievals. The claim-space kNN density metric (B3) achieved an AUROC of 0.5463 (95% CI [0.5366, 0.5564]) and an AUPRC of 0.2731. Under the frozen FEVER-derived evaluation protocol, claim-space kNN density exhibited modest discrimination of the predefined FEVER `NOT ENOUGH INFO` target.

## 4.2 Cross-Construction E1 Evaluation
To test whether the density signal generalized, we evaluated it against AVeriTeC, a naturalistic dataset where claims lack evidence despite active retrieval (`retrieved_insufficient`). The evaluation population utilized a strict 2,384-instance DEV set for threshold calibration and a frozen 500-instance TEST set. A reference manifold of 671 "Supported" AVeriTeC training instances was used. Leakage was prevented by quarantining 6 overlapping claims, ensuring CLEAN isolation. The optimal Youden threshold (0.5656) was derived exclusively from DEV, ensuring no TEST tuning occurred. The experiment yielded PASS for reproducibility.

## 4.3 Construction-Specific Results
On the frozen AVeriTeC TEST set, B3 yielded an overall AUROC of 0.3545 (95% CI [0.2925, 0.4215]), representing a profound reversal of the discriminative direction.
- `retrieved_insufficient`: AUROC = 0.2754.
- `contradictory`: AUROC = 0.4273.
- `rare_valid`: AUROC = 0.4637.

## 4.4 Post-Hoc Failure Attribution
Post-hoc diagnostics indicated strong support for Reference-Manifold Effect (H1), Class-Composition Confounding (H3), and Genuine Construction Dependence (H5). Stylistic/Structural Confounding (H4) and Retrieval/Evidence Artifact (H6) could not be tested directly due to immutability constraints prohibiting instance-level score re-extraction.

## 4.5 Scientific Interpretation
The inversion of the density signal (AUROC 0.2754 for `retrieved_insufficient`) supports the interpretation that the metric strictly measures semantic proximity to the reference manifold. Because naturally occurring "Not Enough Evidence" claims are stylistically closer to "Supported" claims than overtly "Refuted" claims, the density signal erroneously assigns lower distance (higher sufficiency) to them, operating effectively as a generalized anomaly detector rather than a direct evidence-insufficiency measure.
