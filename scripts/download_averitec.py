import os
import certifi
import json

os.environ["SSL_CERT_FILE"] = certifi.where()
os.environ["CURL_CA_BUNDLE"] = certifi.where()

import datasets

def download_averitec():
    print("Downloading AVeriTeC dataset from HuggingFace...")
    ds = datasets.load_dataset('averitec/averitec')
    
    out_dir = "data/raw/averitec"
    os.makedirs(out_dir, exist_ok=True)
    
    print(ds.keys())
    for split in ds.keys():
        print(f"Saving {split}...")
        out_path = os.path.join(out_dir, f"{split}.jsonl")
        # To jsonl
        ds[split].to_json(out_path)
        print(f"Saved {split} with {len(ds[split])} instances.")

if __name__ == "__main__":
    download_averitec()
