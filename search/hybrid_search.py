from search.keyword_search import keyword_search
from search.semantic_search import semantic_search  

def normalise_scores(scores):
    # for normalisation to be used in hybrid search.
    if not scores:
        return []
    min_score = min(scores)
    max_score = max(scores)
    for i in range(len(scores)):

        scores[i] = (scores[i] - min_score) / (max_score - min_score) if max_score > min_score else 0.0

    return scores

def hybrid_rrf_scores(query, top_k=10, k=60):

    keyword_results = keyword_search(query, top_k=50 * top_k)
    semantic_results = semantic_search(query, top_k=50 * top_k)

    rrf_scores = {}

    for rank, (doc_id, _) in enumerate(keyword_results):
        rrf_scores[doc_id] = (
            rrf_scores.get(doc_id, 0)
            + 1 / (k + rank + 1)
        )

    for rank, (doc_id, _) in enumerate(semantic_results):
        rrf_scores[doc_id] = (
            rrf_scores.get(doc_id, 0)
            + 1 / (k + rank + 1)
        )

    results = sorted(
        rrf_scores.items(),
        key=lambda x: x[1],
        reverse=True
    )

    return results[:top_k]

def hybrid_score_search(query, top_k=10, alpha=0.7):

    keyword_results = keyword_search(query, top_k=50 * top_k)
    semantic_results = semantic_search(query, top_k=50 * top_k)

    keyword_scores = [score for _, score in keyword_results]
    semantic_scores = [score for _, score in semantic_results]

    keyword_scores = normalise_scores(keyword_scores)
    semantic_scores = normalise_scores(semantic_scores)

    keyword_map = {
        doc_id: keyword_scores[i]
        for i, (doc_id, _) in enumerate(keyword_results)
    }

    semantic_map = {
        doc_id: semantic_scores[i]
        for i, (doc_id, _) in enumerate(semantic_results)
    }

    common_ids = keyword_map.keys() | semantic_map.keys()

    results = []

    for doc_id in common_ids:

        score = ((1 - alpha) * keyword_map.get(doc_id, 0)) + ((alpha) * semantic_map.get(doc_id, 0))

        results.append((doc_id, score))

    results.sort(
        key=lambda x: x[1],
        reverse=True
    )

    return results[:top_k]
 