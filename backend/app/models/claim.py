from pydantic import BaseModel, Field

class ExtractedClaim(BaseModel):
    id: str = Field(description="Unique identifier for the extracted claim")
    original_text: str = Field(description="The exact text of the claim as found in the source")
    context: str = Field(description="The surrounding text or context where the claim was found")

class NormalizedClaim(BaseModel):
    id: str
    extracted_claim_id: str
    normalized_text: str = Field(description="The canonical, standardized surface form of the claim")
    core_entity: str = Field(description="The primary subject or entity of the claim")
    core_predicate: str = Field(description="The primary action or relationship asserted in the claim")
