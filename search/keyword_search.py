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