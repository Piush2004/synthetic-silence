# E1 Construction Matrix

This matrix explicitly maps distinct semantic constructions of "insufficiency" to valid dataset representations. Arbitrary label remapping is forbidden.

| Construction Family | Dataset/Source | Original Task | Original Label | SyntheticSilence Target | Evidence State | Construction Mechanism | Validity Justification |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `missing_evidence` | FEVER v1.0 | Fact Verification | `NOT ENOUGH INFO` | `is_insufficient=True` | `FROZEN_BENCHMARK_EVIDENCE` (Empty) | Artificial mutation of `SUPPORTS` claims (e.g., entity swapping, specific detail removal) so the claim cannot be proven by Wikipedia. | Highly valid for benchmarking artificial claim manipulation. Does *not* represent real-world scarcity. |
| `retrieved_insufficient` | AVeriTeC | Real-World Fact Verification | `Not Enough Evidence` | `is_insufficient=True` | LIVE / RETAINED | Real-world naturally occurring claims where extensive web search fails to yield sufficient proving/refuting evidence. | Valid representation of real-world knowledge voids and verification failures. |
| `contradictory` | AVeriTeC | Real-World Fact Verification | `Conflicting Evidence/Cherry-picking` | `is_insufficient=True` | LIVE / RETAINED | Claims where retrieved evidence contains valid, trusted contradictions. | Valid for testing if the representation collapses contradiction and insufficiency. |
| `rare_valid` (Negative Control) | AVeriTeC (Subset) | Fact Verification | `Supported` (Rare entities) | `is_insufficient=False` | LIVE / RETAINED | True claims featuring long-tail/rare entities with low frequency in the training corpus. | Critical negative control: tests if low semantic density merely identifies "rarity" instead of "insufficiency". |

## Critical Semantic Rules Enforced
- `NOT ENOUGH INFO` ≠ knowledge void
- retrieval failure ≠ evidence insufficiency
- contradiction ≠ lack of evidence
- low density ≠ knowledge scarcity

*Note: The negative control (`rare_valid`) is mandatory to isolate semantic rarity relative to the reference manifold from genuine information scarcity.*
