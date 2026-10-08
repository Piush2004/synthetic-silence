# E0 EXECUTION BLOCKED

## Detected Issue
The selected final evaluation population (`data/raw/fever/paper_test.jsonl`) contains no ground-truth labels (the `label` field is an empty string `""` for all instances). This split is provided by HuggingFace as the `unlabelled_test` split, which corresponds to the hidden test set used by the original FEVER shared task organizers.

## Affected Component
- `fever_adapter.py` (which correctly skipped unlabelled instances to prevent fabricating target variables).
- `run_experiment.py` (which executed the pipeline on an empty array).
- `metrics.py` (which legitimately returned empty metrics).

## Scientific Consequence
Without ground-truth labels for the evaluation population, the AUROC, Precision, Recall, and F1 metrics cannot be computed. The experiment cannot measure the discriminative capability of the density signals against the dataset's NEI target because the target is missing.

## Proposed Correction
The split policy must be revised. In FEVER, the true hidden test set is unavailable for offline metric calculation. The standard methodological correction is to:
1. Divide `paper_dev.jsonl` (which contains 18,999 *labelled* instances) into two new offline splits:
   - `paper_dev_offline` (for threshold selection/development)
   - `paper_test_offline` (for final E0 evaluation)
2. Update the E0 Configuration and Preflight Audit to target `paper_test_offline`.

## Invalidation Status
The current E0 run (`exp_E0_baseline_80364ea8`) is **INVALIDATED** because it evaluated 0 instances. 

We must not proceed until the split policy is updated to use a labelled evaluation set and the preflight gate is rerun.
