from fastapi import FastAPI
from search.hybrid_search import hybrid_rrf_scores
from llms.rerank_results import rerank_results

app = FastAPI()

@app.get("/search")
def search(q: str, top_k: int = 10, rerank: bool = False):
    results = hybrid_rrf_scores(q, top_k=top_k)
    if rerank:
        results = rerank_results(q, results)
    return {"query": q, "results": results}