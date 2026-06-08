import faiss
import numpy as np
import json 
from sentence_transformers import SentenceTransformer
from utils.utils import load_influencers

model = SentenceTransformer('all-MiniLM-L6-v2')

def getSize(fc): 
    if fc >= 10_000_000:
        return "mega"
    elif fc >= 1_000_000:
        return "macro"
    elif fc >= 100_000:
        return "mid tier"
    else:
        return "micro"
    
def create_embedding_text(inf):
    return f"""
            Creator Name: {inf['name']}
            Platform: {inf['platform']}
            Country: {inf['country']}
            Category: {inf['category']}
            Audience Size: {getSize(inf['followers_count'])}
            Followers: {inf['followers']}
            Engagement Rate: {inf['engagement_rate']}
            Potential Reach: {inf['potential_reach']}
            """

def build_faiss_index():
    influencers = load_influencers()

    texts = []
    for influencer in influencers:
        text = create_embedding_text(influencer)
        # store inside influencer
        influencer["embedding_text"] = text
        texts.append(text)
    
    embeddings = model.encode(
        texts,
        normalize_embeddings=True,
        show_progress_bar=True
    )

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