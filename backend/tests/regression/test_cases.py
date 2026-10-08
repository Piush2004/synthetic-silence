import pytest
import numpy as np
from app.models.schemas import Evidence, ConstructionFamily
from app.models.claim import NormalizedClaim
from app.services.algo.engine import CoreResearchEngine
from app.services.algo.embeddings import EmbeddingService
from app.services.algo.density import DensityEstimator
from app.services.algo.uncertainty import SimilarityDistributionEntropy
from app.services.algo.nli import LLMNLIAdapter, NLIPrediction
from tests.mocks.providers import MockLLMProvider

@pytest.fixture
def core_engine():
    # We use a real embedder but mock NLI for speed/determinism
    embedder = EmbeddingService() # uses all-MiniLM-L6-v2 locally
    density = DensityEstimator(n_neighbors=2)
    # Fit density with dummy data to avoid NotFitted errors in tests
    dummy_refs = embedder.get_embeddings(["reference one", "reference two", "reference three"])
    density.fit(dummy_refs)
    
    uncertainty = SimilarityDistributionEntropy()
    
    mock_llm = MockLLMProvider()
    nli = LLMNLIAdapter(mock_llm)
    
    return CoreResearchEngine(embedder, density, uncertainty, nli), mock_llm

@pytest.mark.asyncio
async def test_case_a_strongly_supported_claim(core_engine):
    """Case A: Strongly supported claim. Expected: high NLI entailment, low contradiction, high coverage."""
    engine, mock_llm = core_engine
    
    claim = NormalizedClaim(id="1", extracted_claim_id="1", normalized_text="The sky is blue.", core_entity="sky", core_predicate="is blue")
    ev1 = Evidence(id="e1", text="The sky is very blue today.", construction_family=ConstructionFamily.ambiguous_claim)
    
    # Mock NLI to return high entailment
    mock_llm.set_response(NLIPrediction, NLIPrediction(entailment_score=0.95, contradiction_score=0.01, neutral_score=0.04, explanation="Matches"))
    
    signal = await engine.compute_signals(claim, [ev1])
    
    assert signal.evidence_coverage == 1.0
    assert signal.semantic_support == 0.95
    assert signal.contradiction_level == 0.01

@pytest.mark.asyncio
async def test_case_b_no_retrieved_evidence(core_engine):
    """Case B: No retrieved evidence. Expected: zero coverage, None density/confidence."""
    engine, mock_llm = core_engine
    
    claim = NormalizedClaim(id="2", extracted_claim_id="2", normalized_text="Ghosts exist.", core_entity="Ghosts", core_predicate="exist")
    
    # Mock NLI
    mock_llm.set_response(NLIPrediction, NLIPrediction(entailment_score=0.0, contradiction_score=0.0, neutral_score=1.0, explanation="No evidence"))
    
    signal = await engine.compute_signals(claim, [])
    
    assert signal.evidence_coverage == 0.0
    assert signal.representation_density is not None # Computed against reference manifold
    assert signal.retrieval_confidence is not None
    assert signal.uncertainty == 1.0 # Max uncertainty when no evidence

@pytest.mark.asyncio
async def test_case_d_contradictory_evidence(core_engine):
    """Case D: Contradictory evidence. Expected: High contradiction."""
    engine, mock_llm = core_engine
    
    claim = NormalizedClaim(id="3", extracted_claim_id="3", normalized_text="Earth is flat.", core_entity="Earth", core_predicate="is flat")
    ev1 = Evidence(id="e1", text="The Earth is a sphere.", construction_family=ConstructionFamily.ambiguous_claim)
    
    # Mock NLI to return high contradiction
    mock_llm.set_response(NLIPrediction, NLIPrediction(entailment_score=0.01, contradiction_score=0.98, neutral_score=0.01, explanation="Contradicts"))
    
    signal = await engine.compute_signals(claim, [ev1])
    
    assert signal.contradiction_level == 0.98
    assert signal.semantic_support == 0.01
