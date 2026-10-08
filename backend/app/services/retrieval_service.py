import httpx
from typing import List, Optional
from app.models.claim import NormalizedClaim
from app.models.schemas import Evidence, ConstructionFamily

class OpenAlexRetrievalService:
    def __init__(self, base_url: str = "https://api.openalex.org"):
        self.base_url = base_url
        self.client = httpx.AsyncClient(base_url=self.base_url)

    async def retrieve_evidence(self, claim: NormalizedClaim, max_results: int = 10) -> List[Evidence]:
        """
        Retrieves evidence strictly from OpenAlex using the normalized claim.
        """
        # Construct a search query based on the core entity and predicate.
        query = f"{claim.core_entity} {claim.core_predicate}"
        
        # OpenAlex Works API: search across title, abstract, and fulltext
        params = {
            "search": query,
            "per-page": max_results,
            "select": "id,title,abstract_inverted_index,doi,publication_year,primary_location"
        }

        response = await self.client.get("/works", params=params)
        response.raise_for_status()
        data = response.json()

        evidence_list = []
        for work in data.get("results", []):
            # Reconstruct the abstract from the inverted index, fallback to title
            abstract_text = self._reconstruct_abstract(work.get("abstract_inverted_index"))
            text = abstract_text if abstract_text else work.get("title", "")
            
            if not text:
                continue

            source_url = work.get("doi")
            if not source_url and work.get("primary_location"):
                source_url = work.get("primary_location", {}).get("landing_page_url")

            # Defaulting to a baseline construction family; will be updated by later pipeline stages
            evidence = Evidence(
                id=work["id"],
                text=text,
                source_url=source_url,
                construction_family=ConstructionFamily.ambiguous_claim 
            )
            evidence_list.append(evidence)

        return evidence_list

    def _reconstruct_abstract(self, inverted_index: Optional[dict]) -> str:
        if not inverted_index:
            return ""
        
        # Inverted index format: {"word1": [pos1, pos2], "word2": [pos3]}
        words = []
        for word, positions in inverted_index.items():
            for pos in positions:
                words.append((pos, word))
        
        words.sort(key=lambda x: x[0])
        return " ".join([word for pos, word in words])
