import json
import datetime
import os

def load_data(filepath):
    data = []
    with open(filepath, 'r') as f:
        for line in f:
            data.append(json.loads(line))
    return data

def main():
    train_data = load_data("data/raw/fever/train.jsonl")
    test_data = load_data("data/raw/fever/paper_test.jsonl")

    collisions = ["Planet of the Apes was released.", "Boston is in the United States."]
    
    details = []
    exclusions = {
        "dataset": "FEVER",
        "split": "paper_test",
        "excluded_instances": []
    }
    
    for claim in collisions:
        train_matches = [t for t in train_data if t.get('claim') == claim]
        test_matches = [t for t in test_data if t.get('claim') == claim]
        
        details.append({
            "claim": claim,
            "train_matches": train_matches,
            "paper_test_matches": test_matches
        })
        
        for t_match in test_matches:
            exclusions["excluded_instances"].append({
                "instance_id": str(t_match.get("id")),
                "claim": claim,
                "reason": "exact_claim_overlap_with_reference_population",
                "detection_method": "preflight_leakage_audit",
                "detection_timestamp": datetime.datetime.now().isoformat(),
                "reference_population_responsible_for_contamination": "fever_train"
            })

    os.makedirs("results/E0_preflight", exist_ok=True)
    with open("results/E0_preflight/contamination_details.json", "w") as f:
        json.dump(details, f, indent=2)
        
    os.makedirs("backend/experiments/configs", exist_ok=True)
    with open("backend/experiments/configs/E0_exclusions.json", "w") as f:
        json.dump(exclusions, f, indent=2)

    print("Collisions verified and exclusion manifest generated.")

if __name__ == "__main__":
    main()
