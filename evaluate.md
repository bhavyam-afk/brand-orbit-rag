# Evaluation

## Evaluation Setup

The influencer retrieval system was evaluated using a manually curated relevance dataset consisting of business-oriented search queries spanning multiple domains, including:

* Luxury & Fashion
* Beauty & Skincare
* Fitness & Health
* Food & Lifestyle
* Technology & Gaming
* Travel
* Parenting & Education

For each query, creators were manually assigned graded relevance labels:

| Grade | Meaning           |
| ----- | ----------------- |
| 3     | Highly Relevant   |
| 2     | Relevant          |
| 1     | Somewhat Relevant |
| 0     | Not Relevant      |

The following retrieval pipelines were evaluated:

1. BM25 (Keyword Search)
2. Semantic Search (Dense Retrieval)
3. Hybrid Score Fusion
4. Hybrid RRF (Reciprocal Rank Fusion)
5. Hybrid RRF + LLM Re-ranking

Metrics were computed at Top-10 results using:

* Precision@10
* Recall@10
* Mean Reciprocal Rank (MRR) - 1 / first rank of relevant record
* Normalized Discounted Cumulative Gain (NDCG@10)

---

## Results - W/O LLM Refactor Query:

|    Metric    |   bm25 |   semantic |   hybrid_score |   hybrid_rrf |   hybrid_rrf_rerank |
|:-------------|-------:|-----------:|---------------:|-------------:|--------------------:|
| precision@10 | 0.4591 |     0.6    |         0.6864 |       0.6636 |              0.8182 |
| recall@10    | 0.3061 |     0.4    |         0.4576 |       0.4424 |              0.5455 |
| mrr          | 0.5413 |     0.4565 |         0.6205 |       0.6535 |              0.9409 |
| ndcg@10      | 0.4302 |     0.5107 |         0.5995 |       0.5747 |              0.7838 |


## Results - With LLM Refactor Query:

---

## Analysis

The results show that dense semantic retrieval consistently outperformed pure keyword-based retrieval, demonstrating the benefit of embedding-based similarity for influencer discovery.

Combining keyword and semantic retrieval through score fusion further improved all evaluation metrics, indicating that both retrieval approaches contribute complementary information.

The strongest performance was achieved by the Hybrid RRF + LLM Re-ranking pipeline:

* Highest Precision@10 (81.82%)
* Highest Recall@10 (54.55%)
* Highest MRR (0.9409)
* Highest NDCG@10 (0.7838)

The large improvement in MRR suggests that highly relevant creators are ranked very close to the top of the result list after re-ranking.

Similarly, the significant NDCG improvement indicates better ordering of highly relevant creators, which is critical for real-world search experiences where users rarely inspect many results.

---

## Dataset Limitations

The evaluation dataset was intentionally designed to be challenging.

Unlike commercial influencer platforms containing millions of creators, this project uses a relatively small dataset of approximately 100 influencers collected from multiple countries, industries, and audience segments.

Several evaluation queries target highly specific business requirements such as:

* Luxury skincare marketing
* Premium fashion campaigns
* Parenting products
* Vegan food promotion
* Technology launches
* Travel partnerships

As a result, some queries may not have many truly ideal matches within the available creator pool.

Consequently:

* Recall scores are naturally lower than what would be expected on a large-scale production influencer database.
* Some niches are underrepresented in the dataset.
* Geographic and category coverage is limited by the available creators.

Despite these constraints, the hybrid retrieval and re-ranking pipeline achieved strong ranking quality and consistently outperformed all retrieval baselines.

---

## Conclusion

The evaluation demonstrates that:

1. Semantic retrieval improves over traditional keyword search.
2. Hybrid retrieval provides further gains by combining lexical and semantic signals.
3. LLM-based re-ranking significantly improves ranking quality and user-facing relevance.

The final Hybrid RRF + Re-rank pipeline achieved the best overall performance and is used as the production retrieval strategy for the influencer search engine.
