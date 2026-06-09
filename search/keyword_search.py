from utils.utils import load_influencers
from preprocessing.preprocess import preprocess
from rank_bm25 import BM25Okapi

def get_audience_tier(fc):
    if fc >= 10_000_000:
        return "mega influencer"

    elif fc >= 1_000_000:
        return "macro influencer"

    elif fc >= 100_000:
        return "micro influencer"

    else:
        return "nano influencer"
    
def extract_text_values(inf):
    country = inf['country']
    return f"""
        Creator: {inf['name']}.
        Location: {country}. Based in {country}. Country: {country}.
        Platform: {inf['platform']}.
        Niche: {inf['category']}.
        Audience: {get_audience_tier(int(inf['followers_count']))}, 
        {inf['followers']} followers, {inf['engagement_rate']} engagement.
        Reach: {inf['potential_reach']}.
    """


def keyword_search(query, top_k=10):
    influencers = load_influencers()
    query_tokens = preprocess(query)
    
    docTokens = []
    for influencer in influencers:
        text_string = extract_text_values(influencer)
        tokens = preprocess(text_string)
        docTokens.append(tokens)
    
    # bm25 needs list of list as it uses inner list for tokens and outer list as id to map token to.
    bm25 = BM25Okapi(docTokens)
    scores = bm25.get_scores(query_tokens)
    
    # now returning top k influencers id and keyword match score.
    top_influencers = sorted(zip([inf["id"] for inf in influencers], scores), key=lambda x: x[1], reverse=True)[:top_k]
    return top_influencers 