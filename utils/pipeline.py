from search.hybrid_search import hybrid_rrf_scores
from llms.refactor_query import refactor_query
from llms.rerank_results import rerank_results


def run_pipeline(query: str):
    original_query = query
    # 1. Query refinement
    try:
        query = refactor_query(query)
    except Exception as e:
        print("Refactoration of query failed:", e) 

    # 2. Retrieval of 2 * 10 influencers with hybrid search using reciprocal rank fusion.
    rrf_scores = hybrid_rrf_scores(query, top_k=10, k=60) 

    # 3. Reranking through LLM.
    reranked_results = rerank_results(query, rrf_scores)

    return {
        "original_query": original_query,
        "final_query": query,
        "results": reranked_results
    }
