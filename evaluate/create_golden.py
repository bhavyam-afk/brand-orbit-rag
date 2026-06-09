from search.keyword_search import keyword_search
from search.semantic_search import semantic_search
from search.hybrid_search import (
    hybrid_rrf_scores,
    hybrid_score_search
)
from utils.utils import load_influencers

influencers = load_influencers()

from utils.evaluation_queries import QUERIES
import json

TOP_K = 20

id_map = {
    inf["id"]: inf
    for inf in influencers
}

evaluation_data = []

for query in QUERIES:

    evaluation_data.append({
    "query": query,

    "bm25": [
        {
            "id": id_map[doc_id]["id"],
            "name": id_map[doc_id]["name"],
            "country": id_map[doc_id]["country"],
            "category": id_map[doc_id]["category"],
            "followers": id_map[doc_id]["followers"]
        }
        for doc_id, _ in keyword_search(query, TOP_K)
    ],

    "semantic": [
        {
            "id": id_map[doc_id]["id"],
            "name": id_map[doc_id]["name"],
            "country": id_map[doc_id]["country"],
            "category": id_map[doc_id]["category"],
            "followers": id_map[doc_id]["followers"]
        }
        for doc_id, _ in semantic_search(query, TOP_K)
    ],

    "hybrid_score": [
        {
            "id": id_map[doc_id]["id"],
            "name": id_map[doc_id]["name"],
            "country": id_map[doc_id]["country"],
            "category": id_map[doc_id]["category"],
            "followers": id_map[doc_id]["followers"]
        }
        for doc_id, _ in hybrid_score_search(query, TOP_K)
    ],

    "hybrid_rrf": [
        {
            "id": id_map[doc_id]["id"],
            "name": id_map[doc_id]["name"],
            "country": id_map[doc_id]["country"],
            "category": id_map[doc_id]["category"],
            "followers": id_map[doc_id]["followers"]
        }
        for doc_id, _ in hybrid_rrf_scores(query, TOP_K)
    ],

    "relevant_ids": []
})

with open(
    "data/manual_find.json",
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        evaluation_data,
        f,
        indent=2,
        ensure_ascii=False
    )

print(f"Saved {len(evaluation_data)} queries")