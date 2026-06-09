from retrieval.refactor_query import refactor_query
from search.hybrid_search import hybrid_rrf_scores

def search(query, top_k=10):
    # query = refactor_query(query)

    return hybrid_rrf_scores(query=query, top_k=top_k)