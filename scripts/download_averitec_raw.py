import os
import httpx
import json
import hashlib
import pandas as pd
from datetime import datetime, timezone

def calculate_sha256(filepath):
    sha256_hash = hashlib.sha256()
    with open(filepath, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def download_file(url, out_path):
    print(f"Downloading {url} to {out_path}...")
    with httpx.stream("GET", url, verify=False, follow_redirects=True) as r:
        r.raise_for_status()
        with open(out_path, "wb") as f:
            for chunk in r.iter_bytes(chunk_size=8192):
                f.write(chunk)
                
def main():
    base_url = "https://huggingface.co/datasets/pminervini/averitec/resolve/main"
    files = {
        "train": "data/train-00000-of-00001.parquet",
        "dev": "data/dev-00000-of-00001.parquet"
    }
    
    out_dir = "data/raw/averitec"
    os.makedirs(out_dir, exist_ok=True)
    
    manifest = {
        "dataset_name": "AVeriTeC",
        "version": "pminervini/averitec (HuggingFace)",
        "source_url": "https://huggingface.co/datasets/pminervini/averitec",
        "acquisition_timestamp": datetime.now(timezone.utc).isoformat(),
        "license": "Apache 2.0 (assumed from paper)",
        "files": []
    }
    
    for split, path in files.items():
        url = f"{base_url}/{path}"
        parquet_path = os.path.join(out_dir, f"{split}.parquet")
        jsonl_path = os.path.join(out_dir, f"{split}.jsonl")
        
        # Download Parquet
        download_file(url, parquet_path)
        
        # Convert to JSONL
        print(f"Converting {parquet_path} to JSONL...")
        df = pd.read_parquet(parquet_path)
        df.to_json(jsonl_path, orient="records", lines=True)
        
        # Remove parquet to save space
        os.remove(parquet_path)
        
        file_size = os.path.getsize(jsonl_path)
        sha256 = calculate_sha256(jsonl_path)
        
        manifest["files"].append({
            "filename": f"{split}.jsonl",
            "original_parquet_path": path,
            "size_bytes": file_size,
            "sha256": sha256,
            "record_count": len(df)
        })
        
    manifest_path = os.path.join(out_dir, "MANIFEST.json")
    with open(manifest_path, "w") as f:
        json.dump(manifest, f, indent=2)
        
    print(f"Acquisition complete. Manifest saved to {manifest_path}")

if __name__ == "__main__":
    main()
