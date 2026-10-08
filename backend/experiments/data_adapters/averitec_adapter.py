import json
import uuid
from typing import List
from .base import BenchmarkAdapter, BenchmarkInstance
from app.models.claim import ExtractedClaim
from app.models.schemas import Evidence, ConstructionFamily

class AVeriTeCAdapter(BenchmarkAdapter):
    def load_data(self, file_path: str, split: str = "dev") -> List[BenchmarkInstance]:
        """
        Loads an AVeriTeC JSONL file.
        In AVeriTeC, the labels are Supported, Refuted, Not Enough Evidence, Conflicting Evidence/Cherrypicking.
        """
        instances = []
        try:
            with open(file_path, 'r') as f:
                for idx, line in enumerate(f):
                    data = json.loads(line)
                    
                    label = data.get("label")
                    if not label:
                        continue
                        
                    # Map to true construction family
                    if label == "Not Enough Evidence":
                        true_family = ConstructionFamily.retrieved_insufficient
                        is_insufficient = True
                    elif label == "Conflicting Evidence/Cherrypicking":
                        true_family = ConstructionFamily.contradictory
                        is_insufficient = True
                    elif label == "Supported":
                        true_family = ConstructionFamily.rare_valid
                        is_insufficient = False
                    elif label == "Refuted":
                        true_family = ConstructionFamily.ambiguous_claim # or valid/sufficient
                        is_insufficient = False
                    else:
                        continue

                    claim_text = data.get("claim", "")
                    # AVeriTeC records don't naturally have a unique ID at the root level, so we generate one deterministically
                    instance_id = str(uuid.uuid5(uuid.NAMESPACE_URL, f"averitec_{split}_{idx}_{claim_text}"))
                    
                    claim = ExtractedClaim(
                        id=instance_id,
                        original_text=claim_text,
                        context="AVeriTeC Dataset"
                    )
                    
                    evidence_list = []
                    questions = data.get("questions", [])
                    for q_idx, q in enumerate(questions):
                        answers = q.get("answers", [])
                        for a_idx, ans in enumerate(answers):
                            ans_text = ans.get("answer", "")
                            if not ans_text:
                                continue
                            ev_id = str(uuid.uuid5(uuid.NAMESPACE_URL, f"ev_{instance_id}_{q_idx}_{a_idx}"))
                            ev = Evidence(
                                id=ev_id,
                                text=ans_text,
                                source_url=ans.get("source_url"),
                                construction_family=true_family
                            )
                            evidence_list.append(ev)
                    
                    instance = BenchmarkInstance(
                        claim=claim,
                        evidence=evidence_list,
                        is_insufficient=is_insufficient,
                        true_construction_family=true_family,
                        dataset_name="AVeriTeC",
                        original_label=label
                    )
                    
                    instances.append(instance)
                    
        except FileNotFoundError:
            print(f"Warning: Benchmark file {file_path} not found. Skipping load.")
            
        return instances
