from search.keyword_search import keyword_search
from search.semantic_search import semantic_search  

def normalise_scores(scores):
    # for normalisation to be used in hybrid search.
    if not scores:
        return
    min_score = min(scores)
    max_score = max(scores)
    for i in range(len(scores)):
        scores[i] = (scores[i] - min_score) / (max_score - min_score) if max_score > min_score else 0.0

def hybrid_rrf_scores(query, top_k=10, k=60):

    keyword_results = keyword_search(query, top_k=50 * top_k)
    semantic_results = semantic_search(query, top_k=50 * top_k)
    rrf_scores = {}

    # BM25 contribution
    for rank, result in enumerate(keyword_results):
        doc_id = result["id"]

        rrf_scores[doc_id] = (rrf_scores.get(doc_id, 0) + 1 / (k + rank + 1))

    # Semantic contribution
    for rank, result in enumerate(semantic_results):
        doc_id = result["id"]

        rrf_scores[doc_id] = (rrf_scores.get(doc_id, 0) + 1 / (k + rank + 1))

    results = [{
            "id": doc_id,
            "score": score
        }
        for doc_id, score in rrf_scores.items()
    ]

    results.sort(key=lambda x: x["score"], reverse=True)
    return results[:top_k]



def hybrid_score_search(query, top_k=10, alpha=0.75):
    keyword_results = keyword_search(query, top_k=100 * top_k)
    semantic_results = semantic_search(query, top_k=100 * top_k)

    keyword_scores = [item["score"] for item in keyword_results]
    semantic_scores = [item["score"] for item in semantic_results]

    keyword_scores = normalise_scores(keyword_scores)
    semantic_scores = normalise_scores(semantic_scores)

    keyword_map = {
        item["id"]: keyword_scores[i]
        for i, item in enumerate(keyword_results)
    }

    semantic_map = {
        item["id"]: semantic_scores[i]
        for i, item in enumerate(semantic_results)
    }

    common_ids = keyword_map.keys() & semantic_map.keys()

    results = []
    for influencer_id in common_ids:

        hybrid_score = alpha * keyword_map[influencer_id] + ((1 - alpha) * semantic_map[influencer_id])

        results.append({
            "id": influencer_id,
            "score": hybrid_score
        })

    results.sort(key=lambda x: x["score"], reverse=True)
    return results[:top_k]
 