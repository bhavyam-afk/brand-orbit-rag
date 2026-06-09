# Collabrio RAG - Influencer Discovery Search Engine

## Overview

Collabrio RAG is an Information Retrieval (IR) system built for influencer discovery and creator search. The system enables brands, agencies, and marketers to find relevant influencers using natural language queries such as:

* "fitness influencers in india with 1M followers"
* "sports creators in egypt"
* "beauty influencers france high engagement"
* "travel creators thailand for campaign"

The project combines traditional keyword retrieval techniques with modern semantic search and Large Language Models (LLMs) to improve search quality.

---

## Dataset

The search engine is built on a curated influencer dataset containing:

* Influencer Name
* Platform
* Country
* Category / Niche
* Followers
* Engagement Rate
* Potential Reach

Each influencer is assigned a unique ID which is used throughout retrieval, ranking, reranking, and evaluation.

Example:

```json
{
  "id": "ig_123",
  "name": "Mohamed Salah @mosalah",
  "platform": "Instagram",
  "country": "Egypt",
  "category": "Sports",
  "followers": "63.5M",
  "engagement_rate": "1.37%",
  "potential_reach": "19M"
}
```

---

## Retrieval Architecture

The project follows a multi-stage retrieval pipeline.

```text
User Query -> Query Refactoring (LLM) -> Retrieval Pipeline -> Optional Reranking -> Final Results
```

### Query Refactoring

Before retrieval, the user query is passed through an LLM-based query refactoring step to correct spelling and grammar for accurate intention match.

This improves both keyword matching and semantic retrieval.

---

## Search Methods
### 1. Keyword Search (BM25)
### 2. Semantic Search (FAISS + Sentence Transformers)
## Hybrid Retrieval Pipelines

---

## Pipeline 1 — Only Keyword Search

Retrieval Method:

```text
Query -> LLM Refactor -> BM25
```

Purpose:

* Baseline lexical retrieval system.

---

## Pipeline 2 — Only Semantic Search

Retrieval Method:

```text
Query -> LLM Refactor -> Sentence Transformer -> FAISS
```

Purpose:

* Baseline semantic retrieval system.

---

## Pipeline 3 — Hybrid Score Fusion

Combines normalized BM25 and Semantic scores.
Formula:

```text
Final Score =
α × BM25 Score + (1 - α) × Semantic Score
```

Flow:

```text
Query -> LLM Refactor -> BM25 -> Semantic Search -> RRF Fusion -> Weighted Fusion
```

Purpose:

* Combines lexical and semantic relevance.

---

## Pipeline 4 — Hybrid RRF

Uses Reciprocal Rank Fusion (RRF).
Formula:

```text
RRF = Σ 1 / (k + rank)
```

Flow:

```text
Query -> LLM Refactor -> BM25 -> Semantic Search -> RRF Fusion
```

Purpose:

* More robust than score fusion.
* Does not depend on score scales.
* Widely used in production retrieval systems.

---

## Pipeline 5 — Hybrid RRF + LLM Reranker

The most advanced pipeline.

Flow:

```text
Query -> LLM Refactor -> BM25 -> Semantic Search -> RRF Fusion -> LLM Reranker -> Final Results
```

The reranker receives:

* User query
* Retrieved candidates
* Candidate metadata

and assigns relevance scores based on semantic relevance to the query.

Purpose:

* Improve final ranking quality.
* Push the most relevant creators to the top.
* Simulate production-grade retrieval pipelines.

--- 

## Tech Stack

* Python
* BM25 (rank_bm25)
* Sentence Transformers
* FAISS
* Google Gemini / Gemma
* JSON-based Metadata Store

---

## Project Goal

The goal of Collabrio RAG is to explore and evaluate modern retrieval techniques for influencer discovery by comparing traditional lexical search, semantic search, hybrid retrieval, and LLM-powered reranking within a unified evaluation framework.
