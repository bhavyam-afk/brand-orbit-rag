# api/routes.py
# api/routes.py

from fastapi import APIRouter
from pydantic import BaseModel

from pipelines.only_keyword import search as bm25_search
from pipelines.only_semantic import search as semantic_search
from pipelines.hybrid_score import search as hybrid_score_search
from pipelines.hybrid_rrf import search as hybrid_rrf_search
from pipelines.hybrid_rrf_rerank import search as hybrid_rrf_rerank_search


router = APIRouter()


class SearchRequest(BaseModel):
    query: str
    pipeline: str = "hybrid_rrf_rerank"
    top_k: int = 10


@router.post("/search")
def search(request: SearchRequest):

    if request.pipeline == "bm25":
        results = bm25_search(
            query=request.query,
            top_k=request.top_k
        )

    elif request.pipeline == "semantic":
        results = semantic_search(
            query=request.query,
            top_k=request.top_k
        )

    elif request.pipeline == "hybrid_score":
        results = hybrid_score_search(
            query=request.query,
            top_k=request.top_k
        )

    elif request.pipeline == "hybrid_rrf":
        results = hybrid_rrf_search(
            query=request.query,
            top_k=request.top_k
        )

    else:
        results = hybrid_rrf_rerank_search(
            query=request.query,
            top_k=request.top_k
        )

    return {
        "query": request.query,
        "pipeline": request.pipeline,
        "results": results
    }