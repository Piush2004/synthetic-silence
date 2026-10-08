# E1 Reference Manifold Protocol

## Scientific Dilemma
E0 utilized the `FEVER TRAIN SUPPORTS` manifold. If we evaluate AVeriTeC claims against the FEVER manifold, we are measuring *distance from FEVER's distribution*, not necessarily distance from *all supported knowledge*. 

To test whether the density signal generalizes, we must isolate cross-construction robustness from manifold-specific tuning.

## Protocol Decision: Design C (Both)
E1 will utilize **BOTH** a common reference manifold and construction-specific reference manifolds to decouple these variables.

### E1-A: Common Reference Manifold
- **Manifold**: `fever_train_v1` (The E0 FEVER `SUPPORTS` manifold).
- **Purpose**: Tests cross-construction robustness. Does a density estimator fitted strictly on FEVER knowledge generalize to detecting insufficiency in real-world AVeriTeC claims?
- **Implication**: If this fails, it suggests the E0 signal is heavily tied to the specific vocabulary/topics of the FEVER corpus.

### E1-B: Construction-Specific Reference Manifold
- **Manifold**: `averitec_train_supported_v1` (A new manifold built exclusively from AVeriTeC `Supported` claims).
- **Purpose**: Tests within-construction discrimination. If we build a manifold native to the AVeriTeC domain, does the density signal differentiate `Not Enough Evidence` claims from `Supported` claims within that same domain?
- **Implication**: If this succeeds but E1-A fails, the density hypothesis holds but requires domain-aligned reference manifolds. If this fails, claim-space density may fundamentally fail on real-world constructions regardless of the manifold.

## Implementation Rules
- Density must remain strictly in **Claim Embedding Space**.
- Do not mix the manifolds into a single heterogeneous vector space unless designated as a separate experiment (`E1-C: Combined Manifold`).
- Embedding model: `all-MiniLM-L6-v2` (Must remain identical to E0 to isolate the construction variable).
