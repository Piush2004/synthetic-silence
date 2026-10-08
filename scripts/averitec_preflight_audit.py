import os
import json
from collections import Counter
import hashlib

def get_hash(text):
    return hashlib.md5(text.encode("utf-8")).hexdigest()

def normalize_claim(claim):
    return " ".join(claim.lower().strip().split())

def main():
    preflight_dir = "results/E1_preflight"
    os.makedirs(preflight_dir, exist_ok=True)
    
    averitec_files = ["data/raw/averitec/train.jsonl", "data/raw/averitec/dev.jsonl"]
    
    all_claims = []
    all_records = []
    
    schema_stats = {
        "number_of_records": 0,
        "field_names": set(),
        "missing_values": {},
        "label_distribution": Counter()
    }
    
    evidence_stats = {
        "total_evidence_blocks": 0,
        "evidence_fields": set(),
        "source_urls": 0
    }
    
    for fpath in averitec_files:
        with open(fpath) as f:
            for line in f:
                record = json.loads(line)
                all_records.append(record)
                schema_stats["number_of_records"] += 1
                
                for k, v in record.items():
                    schema_stats["field_names"].add(k)
                    if v is None or v == "":
                        schema_stats["missing_values"][k] = schema_stats["missing_values"].get(k, 0) + 1
                        
                schema_stats["label_distribution"][record.get("label", "MISSING")] += 1
                
                if "claim" in record:
                    all_claims.append(record["claim"])
                    
                # Audit evidence
                if "evidence" in record:
                    ev_list = record["evidence"]
                    if isinstance(ev_list, list):
                        for ev in ev_list:
                            evidence_stats["total_evidence_blocks"] += 1
                            if isinstance(ev, dict):
                                for ek in ev.keys():
                                    evidence_stats["evidence_fields"].add(ek)
                                if "url" in ev:
                                    evidence_stats["source_urls"] += 1
                                    
    schema_stats["field_names"] = list(schema_stats["field_names"])
    schema_stats["label_distribution"] = dict(schema_stats["label_distribution"])
    evidence_stats["evidence_fields"] = list(evidence_stats["evidence_fields"])
    
    with open(os.path.join(preflight_dir, "averitec_schema_audit.json"), "w") as f:
        json.dump(schema_stats, f, indent=2)
        
    with open(os.path.join(preflight_dir, "averitec_evidence_audit.json"), "w") as f:
        json.dump(evidence_stats, f, indent=2)
        
    # Leakage Audit against FEVER
    fever_files = ["data/raw/fever/train.jsonl", "data/raw/fever/paper_dev.jsonl", "data/raw/fever/paper_test.jsonl"]
    fever_claims_exact = set()
    fever_claims_norm = set()
    
    for ff in fever_files:
        if os.path.exists(ff):
            with open(ff) as f:
                for line in f:
                    rec = json.loads(line)
                    if "claim" in rec:
                        c = rec["claim"]
                        fever_claims_exact.add(c)
                        fever_claims_norm.add(normalize_claim(c))
                        
    leakage = {
        "exact_claim_overlap": 0,
        "normalized_claim_overlap": 0,
        "overlapping_claims": []
    }
    
    for c in all_claims:
        if c in fever_claims_exact:
            leakage["exact_claim_overlap"] += 1
            leakage["overlapping_claims"].append(c)
        elif normalize_claim(c) in fever_claims_norm:
            leakage["normalized_claim_overlap"] += 1
            leakage["overlapping_claims"].append(c)
            
    with open(os.path.join(preflight_dir, "leakage_audit.json"), "w") as f:
        json.dump(leakage, f, indent=2)
        
    print("Schema audit:", json.dumps(schema_stats, indent=2))
    print("Evidence audit:", json.dumps(evidence_stats, indent=2))
    print("Leakage audit overlap:", leakage["exact_claim_overlap"] + leakage["normalized_claim_overlap"])

if __name__ == "__main__":
    main()
