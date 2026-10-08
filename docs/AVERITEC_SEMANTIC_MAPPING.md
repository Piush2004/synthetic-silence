# AVeriTeC Semantic Mapping

This document establishes the precise semantic mapping of AVeriTeC source labels to SyntheticSilence target states.

## Source Label Semantics
The AVeriTeC dataset annotates real-world claims based on web-retrieved QA-driven evidence.

1. **`Supported`**
   - **Original Task Definition**: The claim is demonstrably true based on the retrieved evidence.
   - **SyntheticSilence Target**: `is_insufficient=False`.
   - **Notes**: Represents verified, non-scarce knowledge. Can serve as a negative control (`rare_valid`) if sub-selected for low-frequency entities.

2. **`Refuted`**
   - **Original Task Definition**: The claim is demonstrably false based on the retrieved evidence.
   - **SyntheticSilence Target**: `is_insufficient=False`.
   - **Notes**: Evidence *is* sufficient to disprove the claim. Retrieval succeeded in finding disconfirming facts.

3. **`Not Enough Evidence`**
   - **Original Task Definition**: Extensive web search fails to yield sufficient proving or refuting evidence.
   - **SyntheticSilence Target**: `is_insufficient=True`.
   - **Notes**: Represents genuine real-world information scarcity (the `retrieved_insufficient` construction). Unlike FEVER's artificial mutations, these are natural claims lacking web verification.

4. **`Conflicting Evidence/Cherrypicking`**
   - **Original Task Definition**: The retrieved evidence contains valid, trusted contradictions or the claim cherry-picks facts out of context.
   - **SyntheticSilence Target**: `is_insufficient=True`.
   - **Notes**: Represents the `contradictory` construction family. It is a form of insufficiency because the claim cannot be definitively resolved as universally True or False.

## Label Distribution (Train + Dev)
- `Supported`: 971
- `Refuted`: 2047
- `Not Enough Evidence`: 317
- `Conflicting Evidence/Cherrypicking`: 233
