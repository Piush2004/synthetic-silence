# E1 Leakage and Provenance Protocol

Every new dataset (e.g., AVeriTeC) integrated into E1 must undergo strict leakage prevention and cryptographic provenance auditing.

## Dataset Isolation Audit
Before any E1 execution, the dataset must pass the following checks:
1. **Exact Claim Overlap Audit**: Claim string exact match against all reference manifolds (`fever_train_v1`, `averitec_train_v1`).
2. **Normalized Claim Overlap Audit**: Lowercase/whitespace-stripped match against reference manifolds.
3. **Semantic Near-Duplicate Audit**: (If computationally feasible) cosine similarity > 0.95 detection to prevent trivially identical test claims.
4. **Document/Evidence ID Overlap**: Verification that test evidence IDs do not exist in the training reference.
5. **URL Overlap**: Validation that real-world URLs in the test set were not used to build the reference manifold.

*Note: The audit must distinguish lexical similarity from true contamination.*

## Quarantine Mechanism
Any material contamination detected during the isolation audit must produce:
- **E1_PREFLIGHT_STATUS: BLOCKED**
- An explicitly registered experiment-level quarantine manifest (e.g., `E1_averitec_exclusions.json`) containing the colliding instance IDs.

## Scientific Provenance Log
Every E1 execution must immutably log the following to the `manifest.json`:
- `experiment_id`
- `dataset/version`
- `dataset_file_hashes` (SHA-256)
- `construction_family`
- `reference_manifold_id`
- `reference_population`
- `embedding_model/version`
- `preprocessing`
- `algorithm_version`
- `configuration_hash`
- `seed`
- `Git SHA`
- `software environment`
- `hardware`
- `timestamp`
- `threshold-selection method` (e.g., Youden's J on DEV)
- `cutoff` if applicable

Failure to log these parameters mathematically invalidates the run.
