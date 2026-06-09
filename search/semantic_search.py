from sentence_transformers import SentenceTransformer
import faiss
import json

def load_resources():
    model = SentenceTransformer("all-MiniLM-L6-v2")
    index = faiss.read_index("data/faiss.index")

    with open("data/metadata.json") as f:
        influencers = json.load(f)

    return model, index, influencers

model, index, influencers = load_resources()

def semantic_search(query, top_k=10):
    query_emb = model.encode([query], normalize_embeddings=True).astype("float32")

    scores, indices = index.search(query_emb, top_k)

    results = []

    for idx, score in zip(indices[0], scores[0]):
        doc_id = influencers[idx]["id"]
        results.append((doc_id, float(score)))

    return results 