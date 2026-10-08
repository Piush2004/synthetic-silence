# E1 Master Protocol: Cross-Construction Generalization

This protocol is the authoritative blueprint for the E1 experiment phase. It dictates the transition from E0's baseline feasibility observation to E1's cross-construction generalization evaluation.

## 1. Objective
Test whether the representation-density signal (B3) observed in E0 generalizes across distinct semantic constructions of "insufficient evidence" (e.g., missing evidence vs. retrieved insufficient vs. contradictory).

## 2. Prerequisite Documents
The protocol is supported by the following pre-registered documents:
- `E1_RESEARCH_QUESTION.md`: The core hypothesis and failure conditions.
- `E1_CONSTRUCTION_MATRIX.md`: The mapping of datasets to valid insufficiency constructions.
- `E1_REFERENCE_MANIFOLD_PROTOCOL.md`: The dual-manifold (Common vs. Specific) design.
- `E1_LEAKAGE_PROTOCOL.md`: Cryptographic provenance and contamination prevention.
- `E1_STATISTICAL_PROTOCOL.md`: Thresholding (Youden's J) and evaluation strictness.

## 3. The E1 Experiment Matrix
The evaluation matrix will cross Construction Families (Rows) against Baselines (Columns).

**Rows (Implementable Constructions):**
- `missing_evidence` (FEVER)
- `retrieved_insufficient` (AVeriTeC)
- `contradictory` (AVeriTeC)
- `rare_valid` (Negative Control)

**Columns (Baseline Ladder):**
- **B0**: Majority
- **B1**: Evidence Coverage
- **B3**: kNN Density (Primary signal of interest)
- **B5**: Similarity Distribution Entropy
- **B8**: Combined Heuristic

**Output per cell**: N, target prevalence, AUROC, AUPRC, bootstrapped CI, frozen threshold-dependent metrics (P/R/F1).

## 4. Cross-Construction Generalization Test
If sufficient datasets are acquired, E1 will perform a generalization rotation:
- Evaluate AVeriTeC (`retrieved_insufficient`) against the `fever_train_v1` manifold.
- Evaluate FEVER (`missing_evidence`) against the `averitec_train_v1` manifold.

## 5. Required Implementation Steps
Before dataset acquisition can commence, the scientific gate must pass:
1. Identify missing dataset components (AVeriTeC).
2. Authorize acquisition via `E1_GATE_REPORT.md`.
3. Implement `averitec_adapter.py`.
4. Perform Dataset Isolation Audits.
5. Create DEV/TEST splits.
6. Calculate DEV thresholds.
7. Execute final frozen evaluation.
