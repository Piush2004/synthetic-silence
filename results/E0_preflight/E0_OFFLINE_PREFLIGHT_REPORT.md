# E0 OFFLINE PREFLIGHT REPORT

**E0_OFFLINE_PREFLIGHT_STATUS: READY**

## Dataset Provenance
- **Source Dataset**: FEVER v1.0
- **Source Splitting**: Derived strictly from `paper_dev.jsonl` (N=37,566).
- **Split Algorithm**: 50/50 Stratified Random on unique instance IDs (Seed=42).

## Population Accounting
- **Original FEVER paper_dev**: N=37,566
- **OFFLINE_E0_DEV**: N=18935
- **OFFLINE_E0_TEST before quarantine**: N=18631 
  - SUPPORTS: 7205
  - REFUTES: 6949
  - NOT ENOUGH INFO: 4477
- **OFFLINE_E0_TEST after quarantine**: N=18631
  - SUPPORTS: 7205
  - REFUTES: 6949
  - NOT ENOUGH INFO: 4477

## Quarantine & Statistical Reporting
- **Excluded N**: 0
- **Exclusion Rate**: 0.0000
- The class distribution was largely unaffected by the quarantine (0 exclusions found in the offline test split against the known collision set).

## Leakage Audit
- **Status**: PASS
- **DEV vs TEST Overlap**: 0 claims.
- **Reference Manifold vs TEST Overlap**: 0 exact claims.
- **Finding**: The INCLUDED evaluation population has no text contamination with the Reference Manifold or the DEV split.

## Threshold-Selection Protocol
- **Status**: Missing formalized optimal selector. The baseline `metrics.py` implements a naive 0.5 threshold for uncalibrated scores. True calibration requires the `OFFLINE_E0_DEV` split. The E0 config proceeds with continuous AUROC and the naive threshold to establish baseline feasibility.

## Frozen-Evidence Confirmation
- **Status**: PASS
- **Verification**: Configured with `mode: FROZEN_EVIDENCE_MODE` in `E0_baseline_offline.yaml`.

## Methodological Note
The official FEVER paper_test population was not used for supervised metric evaluation because the acquired distribution was unlabelled. A deterministic offline development/evaluation split was therefore constructed from the labelled paper_dev population. This derived evaluation population is not the official FEVER test set.
