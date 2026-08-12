from utils.utils import load_resources 

model, index, influencers = load_resources()

def semantic_search(query, top_k=10):
    query_emb = model.encode([query], normalize_embeddings=True).astype("float32")

    scores, indices = index.search(query_emb, top_k)

    results = []
    for idx, score in zip(indices[0], scores[0]):
        doc_id = influencers[idx]["id"]
        results.append((doc_id, float(score)))

    return results 