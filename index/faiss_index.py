import faiss
import numpy as np
import json 
from sentence_transformers import SentenceTransformer
from utils.utils import load_influencers

model = SentenceTransformer('all-MiniLM-L6-v2')

def get_audience_tier(fc):
    if fc >= 10_000_000:
        return "mega influencer"

    elif fc >= 1_000_000:
        return "macro influencer"

    elif fc >= 100_000:
        return "micro influencer"

    else:
        return "nano influencer"
    
def create_embedding_text(inf):
    country = inf['country']
    return f"""
            Creator Name is {inf['name']}.
            works on {inf['platform']}.
            Location: {country}. Based in {country}. Country: {country}.
            niche or category is {inf['category']}.
            has an audience size of {(inf['followers_count'])}.
            with {inf['followers']} followers.
            with engagement rate of {inf['engagement_rate']} and has 
            potential reach of {inf['potential_reach']}.
            and belongs to {get_audience_tier(int(inf['followers_count']))} tier.
            """

def build_faiss_index():
    influencers = load_influencers()

    texts = []
    for influencer in influencers:
        text = create_embedding_text(influencer)
        # store inside influencer
        influencer["embedding_text"] = text
        texts.append(text)
    
    embeddings = model.encode(texts, normalize_embeddings=True, show_progress_bar=True)

    # [5900, 384] dimension array
    embeddings = np.array(embeddings).astype("float32") 
    # 384
    dim = embeddings.shape[1] 
    # cosine similarity (since normalized) {IP = inner product}
    index = faiss.IndexFlatIP(dim)  
    # storage of indexes 
    index.add(embeddings)
    # save index
    faiss.write_index(index, "data/faiss.index")
    # save metadata
    with open("data/metadata.json", "w") as f:
        json.dump(influencers, f)
    print("FAISS index built and saved.") 

if __name__ == "__main__":
    build_faiss_index()