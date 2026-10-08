import os
import json
import hashlib
from collections import defaultdict
import random

def normalize_claim(claim):
    return " ".join(claim.lower().strip().split())

def main():
    seed = 42
    random.seed(seed)
    
    out_dir = "data/processed/e1_population"
    os.makedirs(out_dir, exist_ok=True)
    
    averitec_train_path = "data/raw/averitec/train.jsonl"
    averitec_dev_path = "data/raw/averitec/dev.jsonl"
    
    # Load all test claims to ensure they are quarantined from train
    e1_test = []
    test_claims_norm = set()
    with open(averitec_dev_path) as f:
        for line in f:
            rec = json.loads(line)
            e1_test.append(rec)
            test_claims_norm.add(normalize_claim(rec["claim"]))
            
    all_train = []
    with open(averitec_train_path) as f:
        for line in f:
            all_train.append(json.loads(line))
            
    # Group train by normalized claim
    claim_groups = defaultdict(list)
    for rec in all_train:
        claim_groups[normalize_claim(rec["claim"])].append(rec)
        
    manifold = []
    dev_set = []
    
    sorted_claims = sorted(claim_groups.keys())
    
    for c in sorted_claims:
        if c in test_claims_norm:
            # QUARANTINE! This train claim overlaps with TEST.
            continue
            
        group = claim_groups[c]
        is_supported = any(r.get("label") == "Supported" for r in group)
        if is_supported:
            if random.random() < 0.8:
                manifold.extend(group)
            else:
                dev_set.extend(group)
        else:
            dev_set.extend(group)
            
    manifold_path = os.path.join(out_dir, "averitec_train_supported_v1.jsonl")
    with open(manifold_path, "w") as f:
        for rec in manifold:
            if rec.get("label") == "Supported":
                f.write(json.dumps(rec) + "\n")
                
    dev_path = os.path.join(out_dir, "averitec_E1_DEV.jsonl")
    with open(dev_path, "w") as f:
        for rec in dev_set:
            f.write(json.dumps(rec) + "\n")
            
    test_path = os.path.join(out_dir, "averitec_E1_TEST.jsonl")
    with open(test_path, "w") as f:
        for rec in e1_test:
            f.write(json.dumps(rec) + "\n")
            
    manifest = {
        "averitec_train_supported_v1_N": len([r for r in manifold if r.get("label") == "Supported"]),
        "averitec_E1_DEV_N": len(dev_set),
        "averitec_E1_TEST_N": len(e1_test),
        "quarantined_from_train_N": len(all_train) - (len(manifold) + len(dev_set))
    }
    with open(os.path.join(out_dir, "manifest.json"), "w") as f:
        json.dump(manifest, f, indent=2)
        
    print("Rebuilt E1 population successfully with leakage isolation.")
    print(json.dumps(manifest, indent=2))

if __name__ == "__main__":
    main()
