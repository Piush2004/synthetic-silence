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
