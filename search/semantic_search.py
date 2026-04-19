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
    # query embedding made is of shape [1, 384] because passed as a single element in a list. 
    query_emb = model.encode([query], normalize_embeddings=True)
    query_emb = np.array(query_emb).astype("float32")

    scores, indices = index.search(query_emb, top_k) 

    results = []
    for i, idx in enumerate(indices[0]):
        influencer = influencers[idx]
        score = scores[0][i]

        results.append({
            "influencer": influencer,
            "score": float(score)
        })

    return results

   