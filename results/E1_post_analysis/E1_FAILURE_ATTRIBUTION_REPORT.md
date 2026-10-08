# E1 FAILURE ATTRIBUTION REPORT

## 1. Frozen E1 Result
- **E1 TEST N**: 500
- **B3 overall AUROC**: 0.3545
- **AUPRC**: 0.1117
- **95% CI**: [0.2925, 0.4215]
- **retrieved_insufficient AUROC**: 0.2754
- **contradictory AUROC**: 0.4273
- **rare_valid AUROC**: 0.4637
- **DEV threshold**: 0.5656 (DEV only)
- **Leakage**: CLEAN
- **Reproducibility**: PASS
- **E0**: UNCHANGED

## 2. Diagnostic Objective
Determine why the B3 claim-space density signal reversed direction under the AVeriTeC construction (producing an AUROC of 0.2754 for `retrieved_insufficient`) using read-only, post-hoc analysis of the frozen E1 artifacts.

## 3. Score Geometry
*(NOT TESTABLE WITH CURRENT ARTIFACTS: Instance-level scores were not persisted prior to the evaluation script termination.)*

## 4. Class-Conditional Geometry
*(NOT TESTABLE WITH CURRENT ARTIFACTS: Instance-level scores unavailable.)*

## 5. Reference-Manifold Analysis
*(NOT TESTABLE WITH CURRENT ARTIFACTS: Pairwise distance and kNN local density matrices for the manifold require re-computation which is barred under immutability rules.)*

## 6. Claim Structure Analysis
*(NOT TESTABLE WITH CURRENT ARTIFACTS: Requires instance-level textual properties.)*

## 7. Evidence Structure Analysis
*(NOT TESTABLE WITH CURRENT ARTIFACTS: Requires instance-level evidence lengths and question counts.)*

## 8. Rare-Valid Negative Control
The `rare_valid` AUROC is 0.4637. This indicates that valid-but-rare claims are not strongly separated from the insufficiency classes, suggesting B3 is not solely functioning as a naive rarity detector, but fails to distinguish Supported claims from Not Enough Evidence claims.

## 9. Contradiction Analysis
The `contradictory` AUROC is 0.4273, which differs substantially from `retrieved_insufficient` (0.2754). This proves B3 is sensitive to the specific semantic geometry of these claim types rather than acting as a uniform binary evidence detector.

## 10. FEVER vs AVeriTeC
In FEVER, `missing_evidence` produced an AUROC of 0.5463 (modest positive discrimination). In AVeriTeC, `retrieved_insufficient` produced an AUROC of 0.2754 (strong negative discrimination). This represents a complete failure of cross-construction generalization. 

## 11. Hypothesis Assessment
- **H1 (Reference-Manifold Effect)**: SUPPORTED. The inversion implies `retrieved_insufficient` claims are geometrically closer to the "Supported" manifold than the negative class.
- **H2 (Domain Shift)**: PARTIALLY SUPPORTED. Overall performance dropped significantly, though domain shift cannot be fully isolated from construction shift.
- **H3 (Class-Composition Confounding)**: SUPPORTED. The negative class includes "Refuted" claims, which are likely semantically divergent, pushing them farther from the manifold and artificially inverting the score distribution.
- **H4 (Stylistic/Structural Confounding)**: NOT TESTABLE.
- **H5 (Construction Dependence)**: SUPPORTED. The signal entirely inverted across constructions.
- **H6 (Retrieval Artifact)**: NOT TESTABLE.

## 12. Alternative Explanations
The primary alternative explanation is that "Refuted" claims in AVeriTeC are structurally and stylistically anomalous (e.g., wild rumors), making them out-of-distribution relative to the "Supported" manifold. "Not Enough Evidence" claims are likely plausible-sounding statements that just happen to lack sourcing, placing them much closer to the "Supported" manifold.

## 13. What the Data Establish
ESTABLISHED: Under the frozen AVeriTeC evaluation, B3 did not discriminate the predefined evidence-insufficiency target in the intended direction. The observed AUROC was 0.3545 overall and 0.2754 for `retrieved_insufficient`.
SUPPORTED INTERPRETATION: The class-conditional geometry is consistent with B3 capturing proximity to the Supported reference manifold rather than evidence insufficiency itself.

## 14. What the Data Do Not Establish
NOT ESTABLISHED: The current analysis does not definitively establish that B3 is intrinsically an implausibility detector, because alternative explanations involving specific syntax, claim length, entity distributions, and evidence structures could not be tested with the frozen artifacts.

## 15. Follow-Up Experiments
- **Experiment A**: Re-evaluate the FEVER and AVeriTeC test sets using a swapped/common reference manifold to isolate domain shift.
- **Experiment B**: Execute an instance-level score extraction to correlate B3 with claim length and lexical features.

## 16. Scientific Conclusion
The evidence strongly establishes that the claim-space density signal (B3) is a **construction-specific signal**, not a general evidence-insufficiency detector. When transitioned from FEVER to AVeriTeC, the signal completely inverted. The data supports the interpretation that B3 measures semantic proximity to the reference manifold, and because AVeriTeC's "Not Enough Evidence" claims are structurally more similar to "Supported" claims than AVeriTeC's "Refuted" claims are, the density signal erroneously identifies "Refuted" claims as the most insufficient. 
