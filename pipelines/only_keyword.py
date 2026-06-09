from search.keyword_search import keyword_search
from retrieval.refactor_query import refactor_query

def search(query, top_k=10):
    # query = refactor_query(query)

    return keyword_search(query=query, top_k=top_k)