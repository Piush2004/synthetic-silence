import json
from app.models.schemas import ConstructionFamily
from experiments.data_adapters.fever_adapter import FEVERAdapter

def main():
    adapter = FEVERAdapter()
    
    splits = ["data/raw/fever/train.jsonl", "data/raw/fever/paper_dev.jsonl", "data/raw/fever/paper_test.jsonl"]
    
    results = {}
    
    for split in splits:
        print(f"Validating {split}...")
        instances = adapter.load_data(split)
        
        valid = True
        for inst in instances:
            original_label = getattr(inst, 'original_label', None)
            if original_label == "SUPPORTS":
                if inst.is_insufficient is not False: valid = False
            elif original_label == "REFUTES":
                if inst.is_insufficient is not False: valid = False
            elif original_label == "NOT ENOUGH INFO":
                if inst.is_insufficient is not True: valid = False
                
        results[split] = {
            "instances_parsed": len(instances),
            "mapping_valid": valid
        }
        print(f"  Passed: {valid}")
        
    with open("artifacts/fever_adapter_validation.json", "w") as f:
        json.dump(results, f, indent=2)

if __name__ == "__main__":
    main()
