# Testing Architecture

## Overview
The testing suite enforces the engineering validation of the SyntheticSilence2.0 backend. It ensures that the research primitives behave according to their mathematical definitions and that the pipeline correctly handles edge cases, failures, and isolation boundaries.

## Architecture
- **Unit Tests (`tests/unit/`)**: Verifies isolated component behavior (e.g., temporal edge cases, calibration limits, null semantics).
- **Integration Tests (`tests/integration/`)**: Verifies pipeline orchestration and failure propagation.
- **Scientific Tests (`tests/scientific/` & `tests/regression/`)**: Verifies density leakage boundaries, reproducibility, and qualitative bounds (Cases A-I).
- **Mocks (`tests/mocks/`)**: Provides deterministic `MockLLMProvider` and `MockRetrievalProvider` to isolate the pipeline from external API instability.

## Principles
1. **Behavioral Assertions**: Tests assert specific mathematical and state boundaries (e.g., `coverage == 0.0` or `status == NOT_CALIBRATED`), not arbitrary test results.
2. **Isolation**: Explanation models cannot modify upstream scientific features.
3. **No Leakage**: Density estimators must never fit against test domain queries.

## Running Tests
Run the suite using pytest:
```bash
pytest backend/tests/
```
