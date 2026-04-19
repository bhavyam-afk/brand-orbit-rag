import json
from search.hybrid_search import hybrid_rrf_scores
from utils.pipeline import run_pipeline
from utils.utils import load_influencers


# -------------------------------
# 🔹 Heuristic relevance scoring
# -------------------------------

def heuristic_score(query, influencer):
    score = 0

    query = query.lower()

    niche = influencer.get("niche", "").lower()
    name = influencer.get("name", "").lower()
    desc = influencer.get("description", "").lower()

    # Strong signal: niche match
    if niche and niche in query:
        score += 5

    # Keyword overlap (better)
    query_words = set(query.split())
    text = f"{name} {desc}".lower()
    text_words = set(text.split())

    overlap = query_words & text_words
    score += len(overlap) * 2

    # Engagement boost
    if influencer.get("engagement_rate", 0) > 5:
        score += 1

    return score


# -------------------------------
# 🔹 Generate labels
# -------------------------------

def generate_golden_dataset(queries, top_k=20, threshold=3):
    influencers = load_influencers()

    golden = []

    for query in queries:
        print(f"\nProcessing query: {query}")

        results = hybrid_rrf_scores(query, top_k=20)
        candidates = results[:20]

        relevant_ids = []

        for item in candidates:
            influencer = item["influencer"]
            score = heuristic_score(query, influencer)

            scored = []

            for item in candidates:
                influencer = item["influencer"]
                score = heuristic_score(query, influencer)
                scored.append((item["id"], score))

            # sort
            scored.sort(key=lambda x: x[1], reverse=True)

            # take top 6 ONLY
            relevant_ids = [doc_id for doc_id, _ in scored[:6]]

        golden.append({
            "query": query,
            "relevant_ids": relevant_ids,
            "candidates": [item["id"] for item in candidates]
        })

    return golden


# -------------------------------
# 🔹 Save
# -------------------------------

def save_golden(golden, path="data/golden_auto.json"):
    with open(path, "w") as f:
        json.dump(golden, f, indent=2)


# -------------------------------
# 🔹 Run
# -------------------------------

if __name__ == "__main__":
    queries = [
        "fitness influencers for weight loss",
        "funny comedy creators",
        "travel influencers for luxury trips",
        "food bloggers for recipes",
        "finance influencers for investing",
        "tech influencers for AI and coding",
        "gaming streamers",
        "fashion influencers for streetwear",
    ]

    golden = generate_golden_dataset(queries)
    save_golden(golden)

    print("\nSaved auto-labeled golden dataset.")
