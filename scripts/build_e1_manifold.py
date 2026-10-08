import os
import json
import numpy as np
from sentence_transformers import SentenceTransformer

def build_manifold():
    manifold_dir = "data/manifolds"
    os.makedirs(manifold_dir, exist_ok=True)
    
    input_path = "data/processed/e1_population/averitec_train_supported_v1.jsonl"
    output_path = os.path.join(manifold_dir, "averitec_train_supported_v1.npy")
    
    claims = []
    with open(input_path) as f:
        for line in f:
            rec = json.loads(line)
            claims.append(rec["claim"])
            
    print(f"Loaded {len(claims)} claims for manifold.")
    
    # We must use the exact same embedding model as E0
    model = SentenceTransformer('all-MiniLM-L6-v2')
    
    print("Encoding...")
    embeddings = model.encode(claims, show_progress_bar=True, convert_to_numpy=True)
    
    np.save(output_path, embeddings)
    print(f"Saved {embeddings.shape} to {output_path}")

if __name__ == "__main__":
    build_manifold()
