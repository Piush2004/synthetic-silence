from abc import ABC, abstractmethod
from typing import List, Tuple, Optional
from pydantic import BaseModel
from app.models.claim import ExtractedClaim
from app.models.schemas import Evidence, ConstructionFamily

class BenchmarkInstance(BaseModel):
    claim: ExtractedClaim
    evidence: List[Evidence]
    # Ground truth label representing whether evidence is insufficient
    is_insufficient: bool
    # Ground truth construction family if available in the dataset
    true_construction_family: Optional[ConstructionFamily] = None
    dataset_name: str
    original_label: Optional[str] = None

class BenchmarkAdapter(ABC):
    @abstractmethod
    def load_data(self, file_path: str, split: str = "dev") -> List[BenchmarkInstance]:
        """
        Loads the dataset and transforms it into uniform BenchmarkInstance objects
        that can be fed directly into the CoreResearchEngine.
        """
        pass
