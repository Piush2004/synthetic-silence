# BENCHMARK INFRASTRUCTURE REPORT

## Dataset Catalog
- **FEVER (Fact Extraction and VERification)**
  - Adapter Status: IMPLEMENTED (`fever_adapter.py`)
  - Target: The `NOT ENOUGH INFO` split is mapped to the internal `is_insufficient=True` target.
- **AVeriTeC**
  - Adapter Status: PENDING. (Requires parsing complex tabular evidence structures).

## Evaluation Protocol
See `docs/EVALUATION_PROTOCOL.md` for full semantics.
Key rule: The benchmark measures whether the engine identifies the dataset's specific NEI condition. It does NOT automatically assert that NEI is equivalent to a real-world knowledge void without empirical justification.

## Reference Manifold Definition
The Reference Manifold represents the "manifold of established knowledge" in the embedding space (e.g., embeddings of known `SUPPORTS` claims from the training set). Distance from this manifold constitutes the Representation Density feature. 
**Crucially, the reference manifold population is strictly isolated from the test evaluation population.**

## Leakage Audit Design
`scripts/run_experiment.py` requires a strict `perform_leakage_audit` pass before execution. It computes exact-text and semantic overlap between the Reference Manifold and the Test Claims. If `overlap_rate > 0`, the experiment is blocked and a `leakage_audit.json` artifact is generated detailing the contamination.

## Baseline Ladder
Experiments (E0) explicitly compare:
- B1: Evidence Coverage-only
- B3: kNN Density-only
- B5: Similarity Distribution Entropy-only
- B6: LLM Verification-only
- B8: Combined Heuristic

## Metric Definitions
Metrics computed via `metrics.py` (scikit-learn):
- **AUROC/AUPRC**: Evaluated directly on the continuous `insufficiency_score`.
- **Precision/Recall/F1**: Evaluated at a naive 0.5 threshold for uncalibrated scores, or using the Conformal Calibrator's bounds if fitted.

## CLI Usage
**Build the Manifold:**
```bash
python3 scripts/build_reference_manifold.py --dataset fever --split train --model all-MiniLM-L6-v2 --output data/manifolds/fever_train.json
```

**Run the Experiment:**
```bash
python3 scripts/run_experiment.py --config backend/experiments/configs/E0_baseline.yaml
```

## Artifact Structure
```
backend/experiments/results/<exp_id>/
  manifest.json
  leakage_audit.json
  metrics.json
  predictions.json
  errors.json
```

## Remaining Blockers / Scientific Limitations
1. **Actual Dataset Files:** We need the literal FEVER `.jsonl` files downloaded to `data/fever/` to execute E0.
2. **NLI Baseline (B7):** We are currently using the LLM Verification Adapter (B6). A true deterministic cross-encoder NLI model is required for B7 comparisons.
3. **AVeriTeC Adapter:** Must be implemented to run Experiment E1 (Cross-Construction Generalization).

## Exact Command for E0
```bash
export PYTHONPATH="$(pwd)/backend"
python3 scripts/run_experiment.py --config backend/experiments/configs/E0_baseline.yaml
```
