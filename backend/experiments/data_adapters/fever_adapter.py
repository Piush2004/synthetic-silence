import json
import uuid
from typing import List
from .base import BenchmarkAdapter, BenchmarkInstance
from app.models.claim import ExtractedClaim
from app.models.schemas import Evidence, ConstructionFamily

class FEVERAdapter(BenchmarkAdapter):
    def load_data(self, file_path: str, split: str = "dev") -> List[BenchmarkInstance]:
        """
        Loads a FEVER JSONL file from HuggingFace export.
        In FEVER, the labels are SUPPORTS, REFUTES, NOT ENOUGH INFO (NEI).
        For our engine, NEI = is_insufficient: True.
        """
        instances = []
        try:
            with open(file_path, 'r') as f:
                for line in f:
                    data = json.loads(line)
                    
                    label = data.get("label")
                    if not label:
                        continue
                        
                    is_insufficient = (label == "NOT ENOUGH INFO")
                    
                    # Original label preserved in metadata mapping outside this core schema, 
                    # or derived back from true_construction_family. 
                    # We map NEI to missing_evidence, REFUTES to contradictory, SUPPORTS to ambiguous_claim (or valid).
                    if label == "NOT ENOUGH INFO":
                        true_family = ConstructionFamily.missing_evidence
                    elif label == "REFUTES":
                        true_family = ConstructionFamily.contradictory
                    else:
                        true_family = ConstructionFamily.ambiguous_claim # Using this as a proxy for valid/supported in this schema

                    claim = ExtractedClaim(
                        id=str(data.get("id", uuid.uuid4())),
                        original_text=data.get("claim", ""),
                        context="FEVER Dataset"
                    )
                    
                    # HF dataset for FEVER has evidence in a strange nested structure or separate strings.
                    # 'evidence_annotation_id', 'evidence_id', 'evidence_url', 'evidence_sentence_id'
                    # Or 'evidence' as a list. We'll leave evidence empty here for E0 because we're focusing on
                    # NEI (missing evidence) and claim-density, but if we need it for B1, we'd mock it.
                    evidence_list = []
                    
                    instance = BenchmarkInstance(
                        claim=claim,
                        evidence=evidence_list,
                        is_insufficient=is_insufficient,
                        true_construction_family=true_family,
                        dataset_name="FEVER"
                    )
                    # Hack to preserve original label explicitly
                    setattr(instance, 'original_label', label)
                    
                    instances.append(instance)
                    
        except FileNotFoundError:
            print(f"Warning: Benchmark file {file_path} not found. Skipping load.")
            
        return instances
