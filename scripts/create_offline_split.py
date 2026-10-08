import json
import random
import os
import hashlib
from collections import defaultdict

def get_file_hash(filepath: str) -> str:
    h = hashlib.sha256()
    with open(filepath, 'rb') as file:
        while chunk := file.read(8192):
            h.update(chunk)
    return h.hexdigest()

def main():
    SEED = 42
    random.seed(SEED)
    
    input_file = "data/raw/fever/paper_dev.jsonl"
    print(f"Reading {input_file}...")
    
    instances = []
    classes = defaultdict(list)
    with open(input_file, 'r') as f:
        for line in f:
            data = json.loads(line)
            label = data.get("label")
            if not label:
                continue
            inst_id = str(data.get("id"))
            classes[label].append(inst_id)
            instances.append(data)
            
    # Group by claim text first to prevent DEV/TEST claim leakage
    claim_to_ids = defaultdict(list)
    claim_to_label = {}
    for inst in instances:
        claim_text = inst.get("claim", "")
        claim_to_ids[claim_text].append(str(inst.get("id")))
        if claim_text not in claim_to_label:
            claim_to_label[claim_text] = inst.get("label")
            
    # Stratify the unique claims
    stratified_claims = defaultdict(list)
    for claim, label in claim_to_label.items():
        stratified_claims[label].append(claim)
        
    dev_ids = []
    test_ids = []
    
    for label, claims in stratified_claims.items():
        random.shuffle(claims)
        mid = len(claims) // 2
        for claim in claims[:mid]:
            dev_ids.extend(claim_to_ids[claim])
        for claim in claims[mid:]:
            test_ids.extend(claim_to_ids[claim])
            
    dev_set = set(dev_ids)
    test_set = set(test_ids)
    
    assert len(dev_set.intersection(test_set)) == 0, "Leakage between DEV and TEST instance IDs!"
    
    dev_instances = [inst for inst in instances if str(inst.get("id")) in dev_set]
    test_instances = [inst for inst in instances if str(inst.get("id")) in test_set]
    
    dev_classes = defaultdict(int)
    for inst in dev_instances: dev_classes[inst["label"]] += 1
        
    test_classes = defaultdict(int)
    for inst in test_instances: test_classes[inst["label"]] += 1
        
    manifest = {
        "source_dataset": "FEVER",
        "source_split": "paper_dev",
        "source_file_hash": get_file_hash(input_file),
        "random_seed": SEED,
        "split_algorithm": "50/50_stratified_random",
        "normalization_version": "raw",
        "OFFLINE_E0_DEV_counts": {
            "total": len(dev_instances),
            "distribution": dict(dev_classes)
        },
        "OFFLINE_E0_TEST_counts": {
            "total": len(test_instances),
            "distribution": dict(test_classes)
        },
        "OFFLINE_E0_DEV_ids": dev_ids,
        "OFFLINE_E0_TEST_ids": test_ids
    }
    
    out_file = "data/processed/fever/E0_offline_split_manifest.json"
    with open(out_file, 'w') as f:
        json.dump(manifest, f, indent=2)
        
    print(f"Manifest written to {out_file}")

if __name__ == "__main__":
    main()
