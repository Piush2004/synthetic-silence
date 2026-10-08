import pytest
from app.services.analysis.explanation import ExplanationService, ExplanationOutput
from app.models.schemas import InsufficiencySignal
from tests.mocks.providers import MockLLMProvider

@pytest.mark.asyncio
async def test_explanation_isolation():
    """
    Verify that the explanation layer cannot modify scientific outputs, 
    even if it hallucinates or generates contradictory text.
    """
    mock_llm = MockLLMProvider()
    # Malicious/hallucinated explanation
    mock_llm.set_response(ExplanationOutput, ExplanationOutput(explanation="The evidence strongly contradicts the claim."))
    
    service = ExplanationService(mock_llm)
    
    original_signal = InsufficiencySignal(
        evidence_coverage=1.0,
        semantic_support=0.9, # High support
        contradiction_level=0.1, # Low contradiction
        temporal_coverage=0.5,
        representation_density=0.2,
        uncertainty=0.1,
        retrieval_confidence=0.8,
        insufficiency_signal=0.1,
        construction_family_estimate="rare_valid",
        calibration_status="CALIBRATED_90_PCT"
    )
    
    # Deep copy to ensure we catch mutations
    signal_copy = original_signal.model_copy(deep=True)
    
    explanation = await service.generate_explanation(signal_copy, "Valid claim text")
    
    assert explanation == "The evidence strongly contradicts the claim."
    
    # Assert features are completely unchanged despite the hallucinated text
    assert signal_copy.semantic_support == 0.9
    assert signal_copy.contradiction_level == 0.1
    assert signal_copy.evidence_coverage == 1.0
    assert signal_copy.construction_family_estimate == "rare_valid"
