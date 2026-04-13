from utils.utils import load_influencers
from preprocessing.preprocess import preprocess
from rank_bm25 import BM25Okapi


def extract_text_values(item):
    if isinstance(item, dict):
        return " ".join(extract_text_values(value) for value in item.values())
    if isinstance(item, list):
        return " ".join(extract_text_values(value) for value in item)
    return str(item)


def keyword_search(query, top_k=10):
    influencers = load_influencers()
    query_tokens = preprocess(query)
    docTokens = []
    for influencer in influencers:
        text_string = extract_text_values(influencer)
        tokens = preprocess(text_string)
        docTokens.append(tokens)
    bm25 = BM25Okapi(docTokens)
    scores = bm25.get_scores(query_tokens)
    top_influencers = sorted(zip(influencers, scores), key=lambda x: x[1], reverse=True)[:top_k]
    return top_influencers


if __name__ == "__main__":
    # Pretty print the results
    results = keyword_search("investing for kids in future", 5)
    print("\nTop 5 Influencers for 'investing for kids in future':")
    print("=" * 50)
    for i, (influencer, score) in enumerate(results, 1):
        print(f"{i}. Name: {influencer.get('name', 'Unknown')}")
        print(f"   Niche: {influencer.get('niche', 'Unknown')}")
        print(f"   Location: {influencer.get('location', 'Unknown')}")
        print(f"   Engagement Rate: {influencer.get('engagement_rate', 'N/A')}%")
        print(f"   Followers: {influencer.get('followers', 'N/A'):,}")
        print(f"   BM25 Score: {score:.4f}")
        print(f"   Description: {influencer.get('description', 'N/A')[:100]}...")
        print()