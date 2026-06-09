import json
import math
import pandas as pd

from pipelines.only_keyword import search as bm25_search
from pipelines.only_semantic import search as semantic_search
from pipelines.hybrid_score import search as hybrid_score_search
from pipelines.hybrid_rrf import search as hybrid_rrf_search
from pipelines.hybrid_rrf_rerank import search as hybrid_rrf_rerank_search


PIPELINES = {
    "bm25": bm25_search,
    "semantic": semantic_search,
    "hybrid_score": hybrid_score_search,
    "hybrid_rrf": hybrid_rrf_search,
    "hybrid_rrf_rerank": hybrid_rrf_rerank_search,
}


with open("data/golden_queries.json", "r") as f:
    evaluation_queries = json.load(f)


# --------------------------------------------------
# NDCG
# --------------------------------------------------

def dcg(relevances):
    score = 0

    for i, rel in enumerate(relevances):
        score += rel / math.log2(i + 2)

    return score


def ndcg_at_k(retrieved_ids, relevance_map, k):

    retrieved_ids = retrieved_ids[:k]

    gains = [
        relevance_map.get(str(doc_id), 0)
        for doc_id in retrieved_ids
    ]

    dcg_score = dcg(gains)

    ideal = sorted(
        relevance_map.values(),
        reverse=True
    )[:k]

    idcg = dcg(ideal)

    if idcg == 0:
        return 0

    return dcg_score / idcg


# --------------------------------------------------
# EVALUATION
# --------------------------------------------------

def evaluate_pipeline(search_fn, top_k=10):

    total_precision = 0
    total_recall = 0
    total_mrr = 0
    total_ndcg = 0

    num_queries = len(evaluation_queries)

    for item in evaluation_queries:

        query = item["query"]
        print(f"running for: {query}")
        relevance_map = item["relevance"]

        relevant_ids = set(
            relevance_map.keys()
        )

        results = search_fn(
            query=query,
            top_k=top_k
        )

        retrieved_ids = [
            str(doc_id)
            for doc_id, _ in results
        ]

        # -------------------------
        # Precision / Recall
        # -------------------------

        hits = len(
            set(retrieved_ids) & relevant_ids
        )

        precision = hits / top_k

        recall = (
            hits / len(relevant_ids)
            if relevant_ids
            else 0
        )

        # -------------------------
        # MRR
        # -------------------------
        highly_relevant_ids = {
            doc_id
            for doc_id, grade in relevance_map.items()
            if grade == 3
        }

        mrr = 0

        for rank, doc_id in enumerate(
            retrieved_ids,
            start=1
        ):
            if doc_id in highly_relevant_ids:
                mrr = 1 / rank
                break

        # -------------------------
        # NDCG
        # -------------------------

        ndcg = ndcg_at_k(
            retrieved_ids,
            relevance_map,
            top_k
        )

        total_precision += precision
        total_recall += recall
        total_mrr += mrr
        total_ndcg += ndcg

    return {
        f"precision@{top_k}":
            round(total_precision / num_queries, 4),

        f"recall@{top_k}":
            round(total_recall / num_queries, 4),

        "mrr":
            round(total_mrr / num_queries, 4),

        f"ndcg@{top_k}":
            round(total_ndcg / num_queries, 4),
    }


# --------------------------------------------------
# RUN
# --------------------------------------------------

def run_evaluation():

    results = {}

    for pipeline_name, search_fn in PIPELINES.items():

        print(f"Running {pipeline_name}...")

        results[pipeline_name] = evaluate_pipeline(
            search_fn,
            top_k=10
        )

    df = pd.DataFrame(results)

    print("\n")
    print("=" * 100)
    print("FINAL RESULTS")
    print("=" * 100)

    print(df)

    print("=" * 100)

    print("\nMarkdown Table:\n")
    print(df.to_markdown())


if __name__ == "__main__":
    run_evaluation()