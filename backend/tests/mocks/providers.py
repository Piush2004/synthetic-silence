from typing import Any, Type, List, Optional
from app.services.llm_provider import LLMProvider
from app.models.schemas import Evidence, ConstructionFamily
from app.models.claim import NormalizedClaim

class MockLLMProvider(LLMProvider):
    def __init__(self):
        # We can map specific prompts or schema types to deterministic outputs
        self.responses = {}
        self.default_response = None
        self.call_history = []

    def set_response(self, schema_class: Type, response: Any):
        self.responses[schema_class] = response

    async def generate_structured_output(self, prompt: str, schema_class: Type) -> Any:
        self.call_history.append((prompt, schema_class))
        if schema_class in self.responses:
            return self.responses[schema_class]
        if self.default_response:
            return self.default_response
        raise ValueError(f"No mock response configured for {schema_class}")

class MockRetrievalProvider:
    def __init__(self):
        self.evidence_to_return = []
        self.should_timeout = False
        self.should_fail = False

    def set_returns(self, evidence_list: List[Evidence]):
        self.evidence_to_return = evidence_list

    async def retrieve_evidence(self, claim: NormalizedClaim, max_results: int = 10) -> List[Evidence]:
        if self.should_timeout:
            raise TimeoutError("Mock retrieval timeout")
        if self.should_fail:
            raise Exception("Mock retrieval failure")
        return self.evidence_to_return
