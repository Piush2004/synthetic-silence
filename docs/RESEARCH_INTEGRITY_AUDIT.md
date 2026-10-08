# SYNTHETICSILENCE2.0 RESEARCH INTEGRITY REPORT

## Executive Summary
This report documents the formal Research Integrity Audit of the SyntheticSilence2.0 backend engine. The objective is to verify that the existing implementation is scientifically well-defined, reproducible, non-leaky, correctly named, and safe to build upon prior to exposing it via product APIs. The audit resulted in critical terminology corrections (InfoNCE, NLI, Null vs Zero) to ensure mathematical and scientific precision.

## Files Inspected
- `backend/app/services/analysis/temporal.py`
- `backend/app/services/analysis/calibration.py`
- `backend/app/services/analysis/explanation.py`
- `backend/app/services/algo/uncertainty.py`
- `backend/app/services/algo/nli.py`
- `backend/app/services/algo/density.py`
- `backend/app/services/retrieval_service.py`
- `backend/app/services/ranking_service.py`
- `backend/app/services/pipeline.py`
- `backend/app/models/schemas.py`

---

## Scientific Issues Discovered & Corrections Made

### 1. InfoNCE Misnomer (NEEDS_CORRECTION -> PASS)
- **Finding:** The uncertainty module computed cosine similarities, softmax, and entropy. This was incorrectly labeled "InfoNCE" (which strictly requires contrastive logits/loss).
- **Correction:** Renamed `InfoNCEUncertainty` to `SimilarityDistributionEntropy`. The mathematical definition is now correctly documented as the entropy of a softmax distribution over cosine similarities.

### 2. NLI Misrepresentation (NEEDS_CORRECTION -> PASS)
- **Finding:** The `nli.py` file was named `NLIService` but utilized an LLM provider to generate structured judgments. Presenting this as an off-the-shelf NLI baseline is scientifically inaccurate.
- **Correction:** Renamed class to `LLMNLIAdapter` to explicitly denote that it is an LLM-generated structured judgment prototype, not a pretrained sequence-classification NLI model.

### 3. Null vs Zero Leakage (NEEDS_CORRECTION -> PASS)
- **Finding:** The `InsufficiencySignal` schema and `engine.py` defaulted uncomputed values (like `insufficiency_signal` and `temporal_coverage`) to `0.0`. This conflates "not computed/calibrated" with a mathematical value of zero.
- **Correction:** Updated `schemas.py` to `Optional[float] = None` and modified `engine.py` to assign `None` when a value is not calculated or not applicable. 

### 4. Classification Heuristic Transparency (NEEDS_CORRECTION -> PASS)
- **Finding:** `pipeline.py` contained arbitrary hardcoded thresholds (e.g., `contradiction_level > 0.7`) to assign construction families, which could be misconstrued as learned parameters.
- **Correction:** Explicitly documented these thresholds in `pipeline.py` as a "Baseline Prototype Heuristic" and arbitrary architectural placeholders, NOT learned optimal weights.

### 5. Temporal Feature Terminology (NEEDS_CORRECTION -> PASS)
- **Finding:** `temporal.py` called its ratio computation a "temporal novelty estimator".
- **Correction:** Renamed the method to `extract_temporal_feature_ratio` to distinguish a simple statistical feature (post-cutoff evidence ratio) from a complete temporal novelty detector.

---

## Component Scientific Status Matrix

| Component | Implemented | Tested | Scientifically Defined | Validated | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| Claim Extraction | Yes | Yes (Mocked) | Yes (LLM Structured) | No | NOT_VALIDATED |
| Normalization | Yes | Yes (Mocked) | Yes (LLM Canonical) | No | NOT_VALIDATED |
| Retrieval | Yes | Yes (Mocked) | Yes (OpenAlex Live) | No | PASS_WITH_CAVEAT |
| Deduplication | Yes | No | Yes (Exact-text) | No | PARTIAL |
| Ranking | No | No | No | No | NOT_IMPLEMENTED |
| Embedding | Yes | Yes | Yes (MiniLM-L6) | No | NOT_VALIDATED |
| kNN | Yes | Yes | Yes (Cosine) | No | NOT_VALIDATED |
| Mahalanobis | Yes | Yes | Yes (Ledoit-Wolf) | No | NOT_VALIDATED |
| Similarity Entropy | Yes | Yes | Yes (Sim. Entropy) | No | NOT_VALIDATED |
| LLM Verification | Yes | Yes | Yes (LLM Adapter) | No | PROTOTYPE |
| True NLI Baseline | No | No | No | No | NOT_IMPLEMENTED |
| Contradiction | Yes | Yes | Yes (LLM Adapter) | No | PROTOTYPE |
| Temporal | Yes | Yes | Yes (Cutoff Ratio) | No | NOT_VALIDATED |
| Heuristic Score | Yes | Yes | Yes (Composite) | No | NOT_VALIDATED |
| Calibration | Yes | Yes | Yes (Split-Conformal) | No | NOT_CALIBRATED |
| Explanation | Yes | Yes | Yes (LLM Downstream) | No | NOT_VALIDATED |

*Note: Validation requires empirical benchmark experiments (e.g., FEVER/AVeriTeC) which are pending.*

---

## Mathematical Definitions & Data Leakage Findings

### Calibration (`calibration.py`)
- **q_hat:** Calculated as `np.quantile(calibration_scores, q_level, method='higher')` where `q_level = np.ceil((n + 1) * (1 - alpha)) / n`.
- **Status:** The system defaults to `NOT_CALIBRATED`. It correctly requires a `fit()` call with a held-out array of `calibration_signals` to calculate `q_hat`. 

### Density / Leakage (`density.py`)
- **Ledoit-Wolf Shrinkage:** The `cov_estimator` and `knn` rely strictly on `reference_embeddings` provided via `fit()`. 
- **Finding:** No target domain data is currently leaked into the fitting process, provided the orchestrator passes a clean reference corpus. *Action item: Add rigorous pytest leakage assertions.*

### Explanation Isolation (`explanation.py`)
- **Finding:** The explanation layer strictly receives a finalized `InsufficiencySignal` object (downstream). It generates natural language but does not mutate the input signal. Isolation is preserved.

---

## Remaining Risks & Recommended Next Phase

### Remaining Research Risks
- **Ranking System:** Currently stubbed as pass-through.
- **NLI Adapter:** LLM-based NLI is slow and potentially uncalibrated compared to dedicated cross-encoders.
- **Retrieval Semantics:** Live OpenAlex retrieval complicates strict benchmarking against static datasets like FEVER. 

### Remaining Engineering Risks
- **Test Suite Absence:** Unit tests (pytest), synthetic regression suites (Cases A-I), and leakage tests are required before serious experimentation.
- **Error Handling:** Pipeline currently lacks granular fallback handling (e.g., converting OpenAlex timeouts to distinct `RETRIEVAL_FAILED` states rather than empty lists).

### Recommended Next Phase
The backend engine is now **SCIENTIFICALLY DEFINED**, **RESEARCH-TRACEABLE**, and stripped of hallucinated terminology. 

**Next Steps:**
1. Generate the rigorous **Test & Synthetic Regression Suite** (pytest) as mandated by the audit to cover cases A-I, temporal edge cases, and leakage assertions.
2. Only after tests pass, proceed to exposing the API and developing the Chrome UI.
