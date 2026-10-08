from sentence_transformers import SentenceTransformer
import numpy as np

class EmbeddingService:
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        """
        Initializes the sentence transformer model. 
        Using all-MiniLM-L6-v2 as strictly specified for local/efficient execution on M4.
        """
        self.model = SentenceTransformer(model_name)

    def get_embeddings(self, texts: list[str]) -> np.ndarray:
        """
        Returns a numpy array of embeddings for the given texts.
        """
        if not texts:
            return np.array([])
        
        # Output is (num_texts, embedding_dim)
        embeddings = self.model.encode(texts, convert_to_numpy=True)
        return embeddings
