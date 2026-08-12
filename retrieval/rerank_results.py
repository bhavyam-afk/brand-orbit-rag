import os
import json
import re
from dotenv import load_dotenv
from google import genai
from prompts.reranker import reranker_prompt
from utils.utils import get_audience_tier, load_influencers

load_dotenv()
influencers = load_influencers()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

id_map = {
    inf["id"]: inf
    for inf in influencers
}

def build_rerank_input(results):
    formatted = []

    for doc_id, score in results:
        inf = id_map.get(doc_id)

        if not inf: 
            continue

        country = inf['country']
        formatted.append({
            "id": inf["id"],
            "text": f"""
                Creator: {inf['name']}.
                Location: {country}. Based in {country}. Country: {country}.
                Platform: {inf['platform']}.
                Niche: {inf['category']}.
                Audience: {get_audience_tier(int(inf['followers_count']))}, 
                {inf['followers']} followers, {inf['engagement_rate']} engagement.
                Reach: {inf['potential_reach']}.
            """.strip()
        })

    return formatted

def rerank_results(query, results):

    if not results:
        return []

    influencers = build_rerank_input(results)

    prompt = reranker_prompt.format(
        query=query,
        influencers=json.dumps(influencers, indent=2)
    )

    response = client.models.generate_content(
        model="gemma-4-31b-it",
        contents=[prompt]
    )

    

    try:
        match = re.search(r"\[.*\]", response.text, re.DOTALL)
        if not match:
            return results
        llm_scores = json.loads(match.group(0))

    except Exception:
        return results

    score_map = {
        str(item["id"]): item["score"]
        for item in llm_scores
    }

    reranked = []

    for doc_id, _ in results:
        reranked.append(
            (
                doc_id,
                score_map.get(str(doc_id), 0)
            )
        )

    reranked.sort(
        key=lambda x: x[1],
        reverse=True
    )



    return reranked