# 5. DISCUSSION

The experimental findings underscore several critical dimensions in evaluating embedding-space metrics for fact-verification tasks:

- **Representation-space density is not automatically evidence sufficiency**: While a modest association existed under FEVER's conditions, density fundamentally captures distributional geometry. It does not inherently correspond to real-world knowledge scarcity.
- **Benchmark construction matters**: Artificial mutations (such as FEVER's missing evidence) and naturalistic knowledge gaps (AVeriTeC) generate vastly different semantic representations, highlighting the necessity of cross-construction validation.
- **Reference-manifold choice matters**: The geometry of the chosen "Supported" corpus critically dictates the resulting density landscape.
- **Negative controls are important**: Utilizing `rare_valid` and contrasting `retrieved_insufficient` against heterogeneous negative classes (`Refuted`) illuminated the confounding role of class composition in metric performance.
- **Naturalistic evaluation can reverse benchmark-derived conclusions**: What appears as a functional signal on a highly controlled benchmark can completely invert when exposed to the diverse structural variance of in-the-wild claims.
