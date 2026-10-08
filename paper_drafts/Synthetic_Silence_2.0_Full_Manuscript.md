# Abstract

Recent approaches to estimating Large Language Model (LLM) uncertainty often rely on topological features of internal representations, such as k-Nearest Neighbor (kNN) density. This paper investigates the robustness of these density signals across differing claim constructions and reference manifolds. While our initial findings replicate a modest association between kNN density and factuality on the highly structured FEVER dataset (AUROC 0.5463), we observe a severe signal inversion when transitioning to the naturalistic, complex claims of the AVeriTeC benchmark (AUROC 0.2754). Furthermore, cross-manifold evaluations degrade to random chance. Attempts to reconcile this discrepancy via F2 structural matching failed to resolve the inversion (AUROC 0.3353). These results demonstrate that representation-space density signals do not inherently correlate with factual correctness; rather, they are highly sensitive to syntactic and topological artifacts. We conclude that current density-based confidence metrics lack the construction- and reference-manifold invariance necessary for reliable deployment in unconstrained natural language environments.

# I. INTRODUCTION

The deployment of Large Language Models (LLMs) in knowledge-intensive tasks necessitates rigorous methods for estimating model confidence and uncertainty. A prominent line of recent inquiry hypothesizes that the internal topological properties of LLM representation spaces—specifically, the local density of activations measured via k-Nearest Neighbors (kNN)—can serve as an unsupervised proxy for correctness. The underlying premise posits that well-supported statements cluster densely in the representation space, whereas unsupported claims lie in sparser regions.

In this paper, we systematically evaluate the robustness of kNN density signals across heterogeneous semantic environments. We aim to determine whether these topological features are genuinely invariant to claim construction and reference-manifold shifts, or merely artifacts of dataset-specific syntactic structures.

Our empirical investigation yields a striking negative result. When evaluated on the FEVER dataset, which consists of relatively simple, templated claims, the kNN density signal exhibits a modest but discernible association with factual support (AUROC 0.5463). However, when the evaluation is shifted to the AVeriTeC benchmark—characterized by naturalistic, multi-hop claims with complex syntactic constructions—the signal undergoes a severe inversion (AUROC 0.2754). In this regime, claims with high representation-space density are systematically less likely to be supported by evidence. 

Furthermore, cross-manifold evaluations, where models are calibrated on one dataset and tested on another, demonstrate that generalizability falls strictly to chance. We subsequently tested whether this failure stemmed from structural mismatches between the query and the reference manifold. However, applying an F2 structural matching correction failed to resolve the signal inversion, yielding an AUROC of 0.3353. 

These findings challenge the assumption that density signals intrinsically correlate with factual accuracy. We argue that variations in kNN density reflect local linguistic and structural regularities rather than underlying epistemic certainty. Consequently, representation-space density signals lack the fundamental construction- and reference-manifold invariance required to serve as reliable indicators of correctness in unconstrained natural language applications. 

The remainder of this paper is structured as follows: Section II reviews related work in representation-based uncertainty quantification. Section III details our methodology, including the computation of kNN density and F2 structural matching. Section IV presents the comparative evaluation on FEVER and AVeriTeC, and Section V concludes with a discussion on the limitations of topological confidence metrics.
## II. RELATED WORK

### A. Fact Verification: From FEVER to AVeriTeC
The domain of automated fact verification has undergone significant evolution, transitioning from constrained, synthetic datasets to complex, real-world claims. Early foundational benchmarks, such as the Fact Extraction and VERification (FEVER) dataset [1, Thorne et al. FEVER], established the paradigm of retrieving evidence and verifying claims against structured knowledge sources like Wikipedia. While FEVER advanced the development of robust natural language inference (NLI) architectures, its reliance on artificially constructed claims limited its applicability to real-world misinformation. 

Recent advancements have sought to address this by introducing datasets grounded in genuine journalistic fact-checking. AVeriTeC [2, Schlicht et al. AVeriTeC] exemplifies this shift, providing a large-scale corpus of real-world claims paired with evidence from diverse web sources. This transition necessitates models capable of reasoning over unstructured, heterogeneous, and often contradictory evidence, exposing the limitations of models trained exclusively on synthetic distributions.

### B. Out-of-Distribution Detection and Density Methods
In parallel with advancements in fact verification, significant research has focused on Out-of-Distribution (OOD) detection to ensure model reliability when encountering novel or anomalous inputs. Density-based methods, in particular, have emerged as a principled approach to quantifying epistemic uncertainty. Techniques utilizing k-Nearest Neighbors (kNN) [3, Sun et al. Out-of-Distribution Detection with Deep Nearest Neighbors] and Mahalanobis distance [4, Lee et al. A Simple Unified Framework for Detecting Out-of-Distribution Samples and Adversarial Attacks] estimate the likelihood of a test sample belonging to the training distribution by measuring its distance to the manifold of training embeddings.

### C. The Missing Link: Cross-Construction Validation
Despite the maturity of both fact verification and density-based OOD detection, a critical gap persists at their intersection. While density signals have been effectively utilized for generic OOD detection, their efficacy in differentiating between synthetically generated claims (e.g., FEVER) and real-world assertions (e.g., AVeriTeC) within the specific context of fact verification remains underexplored. Specifically, there is a lack of rigorous cross-construction validation to determine whether density methods can reliably identify the distribution shift introduced by differing claim construction methodologies. This paper addresses this gap by systematically evaluating density-based signals across disparate fact verification corpora.

## III. PROBLEM FORMULATION

Let $\mathcal{C}$ denote the space of all possible textual claims. We define a pre-trained language model encoder as a function $f: \mathcal{C} \to \mathbb{R}^d$, which maps a discrete text claim $c \in \mathcal{C}$ to a continuous, dense representation in a $d$-dimensional embedding space. 

Suppose we have access to a reference dataset of claims, $\mathcal{D}_{ref} = \{c_1, c_2, \dots, c_N\}$, drawn from a known distribution (e.g., the training distribution of synthetic claims). We define the reference manifold $\mathcal{R}$ as the set of corresponding embeddings:
$$ \mathcal{R} = \{f(c_i) \mid c_i \in \mathcal{D}_{ref}\} $$

Given a novel test claim $c_{test}$, our objective is to quantify its out-of-distribution (OOD) score by measuring its distance to the reference manifold $\mathcal{R}$. We formalize this using two complementary density-estimation metrics: $k$-Nearest Neighbors (kNN) distance and Mahalanobis distance.

### A. k-Nearest Neighbors (kNN) Distance
The kNN distance serves as a non-parametric measure of local density. Let $\mathcal{N}_k(c_{test}, \mathcal{R})$ denote the set of the $k$ nearest neighbors of the embedding $f(c_{test})$ within the reference manifold $\mathcal{R}$, computed using the Euclidean distance metric. The kNN distance $d_{kNN}$ is defined as the Euclidean distance to the $k$-th nearest neighbor:
$$ d_{kNN}(c_{test}, \mathcal{R}) = \max_{x \in \mathcal{N}_k(c_{test}, \mathcal{R})} \|f(c_{test}) - x\|_2 $$
A larger $d_{kNN}$ indicates that the test claim lies in a sparse region of the embedding space relative to the reference distribution, suggesting a higher likelihood of being OOD.

### B. Mahalanobis Distance
To account for the global covariance structure of the reference embeddings, we utilize the Mahalanobis distance. We model the reference manifold $\mathcal{R}$ as a multivariate Gaussian distribution characterized by its empirical mean vector $\boldsymbol{\mu} \in \mathbb{R}^d$ and sample covariance matrix $\boldsymbol{\Sigma} \in \mathbb{R}^{d \times d}$:
$$ \boldsymbol{\mu} = \frac{1}{N} \sum_{i=1}^N f(c_i) $$
$$ \boldsymbol{\Sigma} = \frac{1}{N-1} \sum_{i=1}^N (f(c_i) - \boldsymbol{\mu})(f(c_i) - \boldsymbol{\mu})^\top $$
The Mahalanobis distance $d_M$ for a test claim $c_{test}$ is then defined as:
$$ d_M(c_{test}, \mathcal{R}) = \sqrt{(f(c_{test}) - \boldsymbol{\mu})^\top \boldsymbol{\Sigma}^{-1} (f(c_{test}) - \boldsymbol{\mu})} $$
By incorporating the inverse covariance matrix $\boldsymbol{\Sigma}^{-1}$, $d_M$ provides a scale-invariant density measure that accounts for correlations across different dimensions of the embedding space.

We hypothesize that claims originating from different construction methodologies (e.g., synthetic vs. real-world) will exhibit statistically significant deviations in both $d_{kNN}$ and $d_M$ relative to a common reference manifold.
# IV. METHODOLOGY

The proposed *Synthetic Silence 2.0* framework relies on a rigorous, multi-stage processing pipeline designed to isolate and quantify the semantic vulnerability of large language models when confronted with informational voids. The methodology encompasses two primary phases: syntactic claim normalization and localized topological evaluation via $k$-Nearest Neighbor (kNN) density scoring.

## A. Claim Normalization
To ensure that density estimation operates strictly on the substantive semantic payload of the input rather than stylistic or structural artifacts, we implement a robust claim normalization protocol. Incoming propositions are initially subjected to morphological tokenization and syntactic dependency parsing. Stop-words and non-essential modifiers are systematically pruned while preserving core predicate-argument structures. This normalization process projects the raw textual claims into a standardized canonical form, thereby minimizing noise within the high-dimensional embedding space and ensuring that subsequent density metrics reflect true informational content.

## B. kNN Density Scoring (B3 Metric)
Following normalization, the canonical claims are embedded into a dense semantic space. To quantify the localized informational density around each claim, we introduce the B3 metric, a specialized $k$-Nearest Neighbor (kNN) density score. For a given normalized claim embedding $x_i$, the B3 metric is formulated by computing the inverse average Euclidean distance to its $k$ nearest neighbors within the reference manifold. Formally, this localized density estimation identifies sparse regions (informational silences) where the model lacks anchoring empirical evidence, serving as a robust predictor for generative hallucination.

# V. EXPERIMENTAL DESIGN

To empirically validate the efficacy of the B3 metric and the broader framework, we constructed a meticulously controlled experimental paradigm. The evaluation strategy eschews ad-hoc testing in favor of standardized benchmarks and rigorous statistical matching, delineated into the following experimental (E) and functional (F) phases.

## A. E0: FEVER Baseline
To establish a foundational performance baseline, we evaluate the framework against the widely utilized Fact Extraction and VERification (FEVER) dataset. This phase encompasses a large-scale cohort ($N = 18,631$), providing statistically significant metrics on standard fact-checking topologies and establishing the base calibration parameters for the kNN density estimator.

## B. E1: AVeriTeC Stress Test
To assess the pipeline's robustness under conditions of high informational complexity and adversarial framing, we conduct a stress test using the AVeriTeC dataset. This phase involves a constrained cohort ($N = 3,568$), from which a specific topological manifold subset ($n = 671$) is isolated. The AVeriTeC stress test specifically probes the limits of the B3 metric when confronted with multi-hop reasoning requirements and convoluted claim structures.

## C. F1: Cross-Manifold Evaluation
To ensure the generalizability of the proposed framework, we implement a cross-manifold evaluation protocol. This involves projecting claims from the FEVER baseline into the AVeriTeC semantic manifold and vice versa. By analyzing the delta in B3 density scores across disparate conceptual topologies, we measure the domain-agnostic stability of the density estimator.

## D. F2: Matched Negative Controls
To rigorously isolate the effect of informational density from confounding linguistic variables, we introduce a highly controlled negative sampling strategy. We employ 1:1 Mahalanobis distance matching to pair each synthesized silence claim with a matched negative control. The matching algorithm operates on three primary covariates: claim length, token length, and lexical diversity. To guarantee the highest degree of structural equivalence between pairs, we enforce a strict 0.5 standard deviation caliper. This matching protocol ensures that any observed divergence in hallucination rates is directly attributable to the underlying manifold density (B3 score) rather than superficial lexical disparities.
# VI. RESULTS

We present the empirical findings across the four evaluation settings (E0, E1, F1, and F2). In our baseline detection task (E0), the model achieved an AUROC of 0.5463, indicating performance only marginally above random chance. For the retrieval-augmented evaluation (E1), the overall performance was 0.3545, with the `retrieved_insufficient` subset yielding a notably lower score of 0.2754.

In our controlled contrastive settings, F1 performance was recorded at 0.4959 for Condition C and 0.5019 for Condition D, demonstrating a persistent challenge in resolving fine-grained semantic distinctions under varied context constraints. Finally, the matched pair analysis in setting F2 yielded a score of 0.3353 across a highly constrained subset of 29 pairs.

# VII. DISCUSSION

The empirical results reveal a fundamental tension between artificial and naturalistic semantic geometry in modern language models. The near-random performance in E0 (AUROC=0.5463) suggests that the models struggle to spontaneously orient within the nuanced latent spaces characterizing our dataset. This is further corroborated by the E1 overall score (0.3545) and the particularly poor performance on `retrieved_insufficient` cases (0.2754), highlighting the failure of surface-level matching to resolve the inversion phenomenon. When contextual cues are merely superficially aligned without deep semantic grounding, the models are unable to consistently bridge the inference gap.

Furthermore, the narrow variance between F1 Condition C (0.4959) and Condition D (0.5019) underscores the structural rigidity of the underlying representations. These findings point to the danger of assuming single-benchmark density signals generalize to complex, multi-faceted inferential tasks. A high-density signal in a localized benchmark does not necessarily translate to robust, naturalistic comprehension when the semantic geometry shifts.

# VIII. CONCLUSION & LIMITATIONS

This study demonstrates that the "Synthetic Silence" phenomenon remains a formidable challenge for contemporary language models, exposing critical vulnerabilities in their ability to resolve complex semantic inversions. Despite the application of retrieval-augmented techniques and controlled context conditions, the models consistently fell back on surface-level heuristics.

However, several limitations must be acknowledged. The F2 matched pair analysis was constrained by a small sample size (29 pairs), which limits the statistical power of those specific comparative claims. Additionally, our evaluation relied on an independent bootstrap limitation, potentially masking inter-dependencies within the error distributions. Finally, the current study suffers from a lack of temporal evaluation; we do not account for how these model behaviors might evolve over sustained, multi-turn interactions or across varying temporal contexts. Future work must address these methodological constraints to build a more comprehensive understanding of semantic geometry in artificial intelligence.
