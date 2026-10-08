# Evaluation Protocol

## 1. Semantics and Concept Separation
**Dataset Ground Truth vs. SyntheticSilence Target**
- `dataset_ground_truth`: The literal label provided by the external benchmark (e.g., `NOT ENOUGH INFO` in FEVER).
- `syntheticsilence_target`: The internal classification target (`is_insufficient=True`).
*Rule:* The benchmark tests whether the engine can identify the dataset's specific insufficient-evidence condition. It does NOT automatically prove the claim is a real-world "knowledge void".

## 2. The Evaluation Unit
- **Sample/Instance**: A single benchmark tuple containing a `claim` and its `evidence` list.
- **Claim**: The frozen text assertion provided by the dataset. (Do NOT pass this through LLM Extraction unless explicitly testing extraction).
- **Evidence**: The frozen list of text strings provided by the dataset (NO LIVE RETRIEVAL during E0).
- **Ground Truth**: Binary `is_insufficient` mapping.
- **Prediction**: A continuous `insufficiency_score` and a discrete `construction_family_estimate`.
- **Positive Class**: `is_insufficient == True`.
- **Negative Class**: `is_insufficient == False`.

## 3. Data Population Strictness
The pipeline explicitly separates three data streams:
1. **Supplied Evidence**: Evidence attached to the test instance.
2. **Live Retrieved Evidence**: OpenAlex (Disabled during benchmark evaluation).
3. **Reference Manifold (Validity Corpus)**: The unsupervised corpus of known claims/evidence used purely to fit the `DensityEstimator`.

**The Reference Manifold MUST NOT OVERLAP WITH TEST CLAIMS.**

### What does the Reference Manifold represent scientifically?
The reference manifold is defined as the embedding distribution of **known-supported claims** from the training split (e.g., claims verified as `SUPPORTS` in FEVER). 
- *Why is distance from this informative?* It measures whether a new assertion structurally and stylistically resembles established valid knowledge.
- *Critical Distinction*: Semantic rarity (low density) in the reference corpus is **NOT** synonymous with real-world knowledge scarcity. A perfectly valid, novel scientific discovery may sit in a sparse region of the embedding space simply because the training corpus lacked similar topics. Density is a feature, not an absolute proof of a knowledge void.

### Representation Space
- **Density Calculation Space:** The current `DensityEstimator` explicitly computes density in **Claim Embedding Space**. 
- The pipeline embeds the `NormalizedClaim` text and queries this single vector against the `kNN` / `Mahalanobis` estimators fitted on the reference claim embeddings. 
- It does **not** jointly embed claim+evidence for density, nor does it compute evidence-space density.

## 4. The Baseline Ladder
Experiments must step through these baselines before evaluating the full combined heuristic:
- **B0**: Majority Baseline
- **B1**: Evidence Coverage-only
- **B2**: Similarity-only
- **B3**: kNN Density-only
- **B4**: Mahalanobis Density-only
- **B5**: Similarity Distribution Entropy-only
- **B6**: LLM Verification-only (Current Adapter)
- **B7**: True NLI Baseline (Pending separate implementation)
- **B8**: Combined Heuristic (Current implementation in `pipeline.py`)

## 5. Experiment Artifacts
Every run generates a persistent artifact directory `backend/experiments/results/<experiment_id>/` containing:
- `manifest.json`: Complete provenance of data, model, and git state.
- `leakage_audit.json`: Proof of no contamination between the reference manifold and the test set.
- `metrics.json`: AUROC, AUPRC, Precision, Recall, F1.
- `predictions.json`: Raw continuous scores and binary outputs.
- `errors.json`: TP/TN/FP/FN slices for error analysis.
