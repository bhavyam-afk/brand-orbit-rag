from sentence_transformers import SentenceTransformer
from pathlib import Path
import json
import faiss

ROOT_DIR = Path(__file__).resolve().parent.parent

def load_stopwords() -> list:
    stopwords_path = ROOT_DIR / 'data' / 'stopwords.txt'
    with open(stopwords_path, 'r') as f:
        return f.read().splitlines()

def load_influencers() -> list[dict]:
    influencers_path = ROOT_DIR / 'data' / 'influencers_data_v2.json'
    with open(influencers_path, 'r') as f:
        return json.load(f)

def idToInfluencer(id):
    influencers = load_influencers()
    for influencer in influencers:
        if influencer['id'] == id:
            return influencer
    return None

def load_resources():
    model = SentenceTransformer("all-MiniLM-L6-v2")
    index = faiss.read_index("data/faiss.index")
    influencers = load_influencers()

    return model, index, influencers 

def get_audience_tier(fc):
    if fc >= 10_000_000:
        return "mega influencer"

    elif fc >= 1_000_000:
        return "macro influencer"

    elif fc >= 100_000:
        return "micro influencer"

    else:
        return "nano influencer"
    