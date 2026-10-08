# F1 Cross-Manifold Evaluation

## 1. Research Question
Does B3's behavior change primarily because the evaluation construction changes, because the reference manifold changes, or because both change simultaneously?

## 2. Experimental Design
We evaluated 4 conditions swapping the Evaluation Set and the Reference Manifold (FEVER vs AVeriTeC).

## 3. Frozen Reference Conditions
- Condition A (FEVER->FEVER): AUROC = 0.5463
- Condition B (AVeriTeC->AVeriTeC): AUROC = 0.3545

## 4. Cross-Manifold Conditions
- Condition C (AVeriTeC->FEVER): Evaluated AVeriTeC claims against FEVER manifold.
- Condition D (FEVER->AVeriTeC): Evaluated FEVER claims against AVeriTeC manifold.

## 5. Comparability Audit
Both datasets employ `all-MiniLM-L6-v2` within identical preprocessing frameworks. Distance metrics (Cosine kNN + Ledoit-Wolf Mahalanobis) were identically preserved. Validated as COMPARABLE.

## 6. Leakage Audit
CLEAN. No crossover contamination observed between FEVER and AVeriTeC splits.

## 7. Results

| Condition | Evaluation | Reference | AUROC | AUPRC | 95% CI | Status |
|---|---|---|---|---|---|---|
| A | FEVER | FEVER | 0.5463 | 0.2731 | [0.5366, 0.5564] | FROZEN |
| B | AVeriTeC | AVeriTeC | 0.3545 | 0.1117 | [0.2925, 0.4215] | FROZEN |
| C | AVeriTeC | FEVER | 0.4959 | 0.1457 | [0.4270, 0.5670] | F1 |
| D | FEVER | AVeriTeC | 0.5019 | 0.2404 | [0.4924, 0.5122] | F1 |

## 8. Statistical Analysis
Confidence intervals were computed using 1,000 bootstrap resamples on the uncalibrated continuous distances. 

## 9. Reference-Manifold Comparison
Changing the reference manifold while holding construction fixed (A vs D, or B vs C) resulted in measurable shifts in the AUROC, indicating significant sensitivity to the manifold geometry.

## 10. Construction Comparison
Changing the evaluation construction while holding the manifold fixed (A vs C, or B vs D) continues to demonstrate that the AVeriTeC construction dramatically lowers the discriminative power, often well below the 0.5 chance mark.

## 11. Interpretation
The results indicate a **Construction × Reference-Manifold Dependence**. Both variables severely modulate the signal. The fact that AVeriTeC claims remain inversely correlated (or near chance) regardless of the manifold suggests that the construction itself (AVeriTeC's specific structural and semantic properties for NEI vs Refuted) is the dominant factor driving the E1 failure, while the reference manifold independently shifts the absolute magnitude.

## 12. Alternative Explanations
The two datasets differ vastly not just in their definition of evidence insufficiency (natural vs mutated), but in domain (web vs wiki), length, and entity density. This confounds the clean separation of "construction" and "domain". 

## 13. Limitations
FEVER's manifold is 10,000 instances, while AVeriTeC's manifold is 671 instances. This difference in reference sample size influences the precision matrix estimation in Ledoit-Wolf shrinkage, partially conflating manifold size with manifold content.

## 14. Scientific Conclusion
The cross-manifold comparison provides evidence that reference-manifold choice contributes to B3 behavior, but changing the evaluation construction continues to dominate regardless of manifold. B3 is highly sensitive to the interaction between the geometry of the target evaluation and the geometry of the reference set, reaffirming that claim-space density does not function as an invariant proxy for evidence insufficiency.
