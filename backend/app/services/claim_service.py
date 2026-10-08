import uuid
from pydantic import BaseModel
from app.models.claim import ExtractedClaim, NormalizedClaim
from app.services.llm_provider import LLMProvider

class ClaimList(BaseModel):
    claims: list[ExtractedClaim]

class NormalizedResponse(BaseModel):
    normalized_text: str
    core_entity: str
    core_predicate: str

class ClaimService:
    def __init__(self, llm_provider: LLMProvider):
        self.llm_provider = llm_provider

    async def extract_claims(self, source_text: str) -> list[ExtractedClaim]:
        """
        Extracts claims from raw source text using a structured LLM call.
        """
        prompt = (
            "Extract the core factual claims from the following text. "
            f"Text: {source_text}"
        )
        result = await self.llm_provider.generate_structured_output(prompt, ClaimList)
        return result.claims

    async def normalize_claim(self, claim: ExtractedClaim) -> NormalizedClaim:
        """
        Normalizes a claim's surface form to ensure cross-construction testing 
        compares identical underlying semantic units.
        """
        prompt = (
            "Normalize the following claim to its simplest, most canonical form. "
            "Identify the core entity and core predicate. "
            f"Original Claim: {claim.original_text}"
        )
        
        llm_response = await self.llm_provider.generate_structured_output(prompt, NormalizedResponse)
        
        return NormalizedClaim(
            id=str(uuid.uuid4()),
            extracted_claim_id=claim.id,
            normalized_text=llm_response.normalized_text,
            core_entity=llm_response.core_entity,
            core_predicate=llm_response.core_predicate
        )
