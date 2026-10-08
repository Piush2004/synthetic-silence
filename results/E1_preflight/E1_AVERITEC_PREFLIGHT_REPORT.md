# E1 AVeriTeC Preflight Report

## 1. Acquisition Provenance
- **Dataset**: AVeriTeC (`pminervini/averitec` via HuggingFace hub mirror)
- **Acquisition Script**: `scripts/download_averitec_raw.py`
- **License**: Apache 2.0 (assumed from paper origin, publicly hosted on HF).
- **Manifest**: `data/raw/averitec/MANIFEST.json`
- **Files Acquired**:
  - `train.jsonl` (Size: ~10MB, Records: ~3,500+)
  - `dev.jsonl` (Size: ~1MB, Records: ~500)

## 2. Schema Audit
- **Total Records (Dev+Train)**: 3,568 (Note: This is the exact number of records retrieved from the `pminervini/averitec` distribution).
- **Field Names**: `claim`, `justification`, `label`, `original_claim_url`, `fact_checking_article`, `location_ISO_code`, `questions`, `fact_checking_strategies`, `reporting_source`, `claim_types`, `cached_original_claim_url`, `required_reannotation`, `speaker`, `claim_date`.
- **Missing Values**: Frequent nulls in metadata (`speaker`, `location_ISO_code`, `original_claim_url`). Core fields (`claim`, `label`, `questions`) are robustly populated.
- **Label Distribution**:
  - `Refuted`: 2047
  - `Supported`: 971
  - `Not Enough Evidence`: 317
  - `Conflicting Evidence/Cherrypicking`: 233

## 3. Label & Evidence Semantics
- **Evidence Formatting**: Evidence is not provided as inline sentences (like FEVER), but as Question-Answer pairs under the `questions` array. Each question contains `answers`, which contain `answer` strings and `source_url`.
- **Construction-Family Mapping**:
  - `Not Enough Evidence` → `retrieved_insufficient`
  - `Conflicting Evidence/Cherrypicking` → `contradictory`
  - `Supported` → `rare_valid` (if long-tail filtered)

## 4. FEVER Comparability
- FEVER (`missing_evidence`) relies on artificially mutated Wikipedia sentences. AVeriTeC involves real-world claims backed by complex web reasoning paths. They are **not directly comparable**, making AVeriTeC an excellent out-of-distribution test for E0's density signal.

## 5. Leakage & Contamination Audit
- **Exact Claim Overlap with FEVER**: 0
- **Normalized Claim Overlap with FEVER**: 0
- **Cross-Dataset Contamination**: None detected. AVeriTeC claims are entirely disjoint from FEVER's train/dev/test populations.

## 6. Split Structure
- Official `train` and `dev` splits are provided by the dataset. We will preserve these official boundaries for density embedding (Train) and threshold selection/evaluation (Dev). If a true Test set is required (as HF `test` is often unlabelled), we will apply the formal E1 deterministic split protocol to the combined Train+Dev sets or use Dev as the evaluation proxy depending on sample size requirements.

## 7. Reference-Manifold Eligibility
- **Eligibility**: HIGH. The 971 `Supported` claims in AVeriTeC provide a robust, domain-aligned population to construct the E1-B Construction-Specific Reference Manifold (`averitec_train_v1`).

## 8. Adapter Status
- The semantic mapping and schema audits are complete. The `AVeriTeCAdapter` is now authorized to be implemented in the next phase, translating `questions/answers` into `Document` structures.

## 9. Negative-Control Status
- **Status**: SUPPORTED. The `Supported` class can be filtered for rare/uncommon entities (relative to the training manifold) to test if low density merely captures "rarity" rather than "insufficiency."

## 10. Conclusion
The dataset is clean, untainted by FEVER contamination, and perfectly supports the target construction families (`retrieved_insufficient`, `contradictory`).

**E1_AVERITEC_PREFLIGHT_STATUS: READY**
