from retrieval.refactor_query import refactor_query
from retrieval.rerank_results import rerank_results
from search.hybrid_search import hybrid_rrf_scores

def search(query, top_k=10):
    query = refactor_query(query)

    candidates = hybrid_rrf_scores(query=query, top_k=20)

    reranked = rerank_results(query=query, results=candidates)
    return reranked[:top_k]