from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import json

model = SentenceTransformer('all-MiniLM-L6-v2')

# load index once (basically pre-built vector database)
index = faiss.read_index("data/faiss.index")

# load metadata once
with open("data/metadata.json") as f:
    influencers = json.load(f)

def verify_model():
    print(f"Model loaded: {model}")
    print(f"Max sequence length: {model.max_seq_length}")

def semantic_search(query, top_k=10):
    query_emb = model.encode([query], normalize_embeddings=True).astype("float32")

    scores, indices = index.search(query_emb, top_k)

    results = []
    for idx, score in zip(indices[0], scores[0]):
        results.append({
            "id": influencers[idx]["id"],
            "score": float(score)
        })

    return results

   