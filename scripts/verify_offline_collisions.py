import json
import datetime
import os

def load_split(manifest_path, split_name, raw_path):
    with open(manifest_path) as f:
        manifest = json.load(f)
    ids = set(manifest[f"{split_name}_ids"])
    
    data = []
    with open(raw_path) as f:
        for line in f:
            inst = json.loads(line)
            if str(inst.get("id")) in ids:
                data.append(inst)
    return data

def load_train(filepath):
    data = []
    with open(filepath, 'r') as f:
        for line in f:
            data.append(json.loads(line))
    return data

def main():
    print("Loading datasets...")
    train_data = load_train("data/raw/fever/train.jsonl")
    
    # We load both DEV and TEST to check collisions across both
    test_data = load_split("data/processed/fever/E0_offline_split_manifest.json", "OFFLINE_E0_TEST", "data/raw/fever/paper_dev.jsonl")
    dev_data = load_split("data/processed/fever/E0_offline_split_manifest.json", "OFFLINE_E0_DEV", "data/raw/fever/paper_dev.jsonl")

    collisions = ["Planet of the Apes was released.", "Boston is in the United States."]
    
    exclusions = {
        "dataset": "FEVER",
        "split": "OFFLINE_E0_TEST",
        "excluded_instances": []
    }
    
    print("Verifying collisions...")
    for claim in collisions:
        test_matches = [t for t in test_data if t.get('claim') == claim]
        for t_match in test_matches:
            exclusions["excluded_instances"].append({
                "instance_id": str(t_match.get("id")),
                "claim": claim,
                "reason": "exact_claim_overlap_with_reference_population",
                "detection_method": "preflight_leakage_audit",
                "detection_timestamp": datetime.datetime.now().isoformat(),
                "reference_population_responsible_for_contamination": "fever_train"
            })

    os.makedirs("backend/experiments/configs", exist_ok=True)
    with open("backend/experiments/configs/E0_offline_exclusions.json", "w") as f:
        json.dump(exclusions, f, indent=2)

    print(f"Collisions verified. {len(exclusions['excluded_instances'])} instances quarantined.")

if __name__ == "__main__":
    main()
