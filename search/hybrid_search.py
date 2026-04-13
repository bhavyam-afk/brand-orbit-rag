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
    keyword_results = keyword_search(query, top_k=100 * top_k)
    semantic_results = semantic_search(query, top_k=100 * top_k)

    rrf_scores = {}

    # keyword contribution
    for rank, (influencer, _) in enumerate(keyword_results):
        doc_id = influencer.get("id")
        if doc_id is None:
            continue

        score = 1 / (k + rank + 1)

        if doc_id not in rrf_scores:
            rrf_scores[doc_id] = {
                "score": 0,
                "influencer": influencer
            }

        rrf_scores[doc_id]["score"] += score

    # semantic contribution
    for rank, item in enumerate(semantic_results):
        influencer = item["influencer"]
        doc_id = influencer.get("id")

        if doc_id is None:
            continue

        score = 1 / (k + rank + 1)

        if doc_id not in rrf_scores:
            rrf_scores[doc_id] = {
                "score": 0,
                "influencer": influencer
            }

        rrf_scores[doc_id]["score"] += score

    results = [
        {
            "id": doc_id,
            "influencer": data["influencer"],
            "score": data["score"]
        }
        for doc_id, data in rrf_scores.items()
    ]

    results.sort(key=lambda x: x["score"], reverse=True)

    return results[:top_k]

def hybrid_score_search(query, top_k=10, alpha=0.75):
    keyword_results = keyword_search(query, top_k=100 * top_k)
    semantic_results = semantic_search(query, top_k=100 * top_k)

    keyword_scores = [score for _, score in keyword_results]
    semantic_scores = [item["score"] for item in semantic_results]

    normalise_scores(keyword_scores)
    normalise_scores(semantic_scores)

    keyword_map = {
        influencer.get("id"): (influencer, keyword_scores[i])
        for i, (influencer, _) in enumerate(keyword_results)
        if influencer.get("id") is not None
    }

    semantic_map = {
        item["influencer"].get("id"): (item["influencer"], semantic_scores[i])
        for i, item in enumerate(semantic_results)
        if item["influencer"].get("id") is not None
    }

    common_ids = set(keyword_map.keys()) & set(semantic_map.keys())
    hybrid_results = []

    for influencer_id in common_ids:
        influencer, kw_score = keyword_map[influencer_id]
        _, sem_score = semantic_map[influencer_id]
        hybrid_score = alpha * kw_score + (1 - alpha) * sem_score
        hybrid_results.append((influencer, hybrid_score))

    hybrid_results.sort(key=lambda x: x[1], reverse=True)

    return hybrid_results[:top_k]


if __name__ == "__main__":
    results = hybrid_rrf_scores("investing for kids in future", top_k=10, k=60)
    print("\nTop 10 Influencers for 'investing for kids in future':")
    print("=" * 50)
    for i, item in enumerate(results, 1):
        influencer = item["influencer"]
        score = item["score"]
        print(f"{i}. Name: {influencer.get('username', 'Unknown')}")
        print(f"   Niche: {influencer.get('niche', 'Unknown')}")
        print(f"   Location: {influencer.get('location', 'Unknown')}")
        print(f"   Engagement Rate: {influencer.get('engagement_rate', 'N/A')}%")
        print(f"   Followers: {influencer.get('followers', 'N/A'):,}")
        print(f"   Hybrid RRF Score: {score:.4f}")
        print(f"   Description: {influencer.get('description', 'N/A')[:100]}...")
        print()