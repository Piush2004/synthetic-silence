# E1 Evaluation Population Construction Report

## 1. Adapter Implementation
The `AVeriTeCAdapter` has been implemented in `backend/experiments/data_adapters/averitec_adapter.py`. 
- It accurately preserves original semantics and dynamically maps AVeriTeC QA-based evidence strings into uniform `Evidence` instances.
- The 4-way semantic mapping to `is_insufficient` and the respective Construction Families has been integrated.

## 2. Deterministic E1 Evaluation Splits
A deterministic dataset splitting strategy was executed via `scripts/e1_build_population.py` (seed=42). 

### E1-B Construction-Specific Reference Manifold
- **Source**: AVeriTeC `train.jsonl`
- **Population**: 674 `Supported` instances (80% of training supported claims).
- **Location**: `data/processed/e1_population/averitec_train_supported_v1.jsonl`

### E1 Development Set (Threshold Calibration)
- **Source**: AVeriTeC `train.jsonl` (Remainder)
- **Population**: 2,379 instances (Contains the remaining 20% of `Supported` claims, plus all `Refuted`, `Not Enough Evidence`, and `Conflicting Evidence` claims).
- **Location**: `data/processed/e1_population/averitec_E1_DEV.jsonl`
- **Purpose**: Strictly reserved for calculating Youden's J threshold prior to final evaluation.

### E1 Test Set (Final Measurement)
- **Source**: AVeriTeC `dev.jsonl` (Official Dev Split)
- **Population**: 500 instances.
- **Location**: `data/processed/e1_population/averitec_E1_TEST.jsonl`
- **Purpose**: Strictly reserved for the final, frozen, threshold-locked E1 evaluation.

## 3. Protocol Readiness
The E1 cross-construction evaluation populations are completely constructed, physically isolated, and mapped.

**E1_POPULATION_STATUS: READY**
