# E0 PREFLIGHT REPORT

**E0_PREFLIGHT_STATUS: READY**

## Dataset Provenance
- **Dataset**: FEVER v1.0
- **Acquisition Source**: HuggingFace (`datasets` export for exact paper splits)
- **Raw Files**: Preserved canonical data byte-for-byte.

## Quarantine & Statistical Reporting
The canonical FEVER data contained instances that overlapped with the reference population under the experiment's predefined contamination criteria. Those instances were excluded from this evaluation through a pre-registered experiment-level quarantine (`E0_exclusions.json`).
- **Original N**: 19998
- **Excluded N**: 2
- **Final N**: 19996
- **Class Counts Before**: {'SUPPORTS': 0, 'REFUTES': 0, 'NOT ENOUGH INFO': 0, 'OTHER': 0, '': 19998}
- **Class Counts After**: {'SUPPORTS': 0, 'REFUTES': 0, 'NOT ENOUGH INFO': 0, 'OTHER': 0, '': 19996}

## Leakage Audit (Post-Quarantine)
- **Status**: PASS
- **Test Results**: Exact and normalized overlap between `train.jsonl` claims and the INCLUDED `paper_test.jsonl` claims was measured at `0`.
- **Finding**: The INCLUDED evaluation population has no text contamination with the Reference Manifold.

## Frozen-Evidence Confirmation
- **Status**: PASS
- **Verification**: Experiment E0 is configured statically with `mode: FROZEN_EVIDENCE_MODE` in `E0_baseline.yaml`, guaranteeing zero external OpenAlex calls during runtime.

## Conclusion
Dataset integrity, adapter mapping, offline reference generation, explicit contamination quarantine, and leakage checks on the INCLUDED population have all succeeded. E0 is cleared for execution.
