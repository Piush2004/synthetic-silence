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
