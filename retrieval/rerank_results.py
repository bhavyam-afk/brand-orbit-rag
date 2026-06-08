import os
import json
import re
from dotenv import load_dotenv
from google import genai
from prompts.reranker import reranker_prompt
from utils.utils import idToInfluencer

def build_rerank_input(results):
    formatted = []

    for result in results:
        influencer = idToInfluencer[result["id"]]

        formatted.append({
            "id": influencer["id"],
            "text": f"""
            Name: {influencer['name']}
            Country: {influencer['country']}
            Category: {influencer['category']}
            Followers: {influencer['followers']}
            Engagement Rate: {influencer['engagement_rate']}
            Potential Reach: {influencer['potential_reach']}
            """.strip()
        })

    return formatted


def rerank_results(query, results):
    if not results:
        return []

    load_dotenv()
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

    influencers = build_rerank_input(results)
    prompt = reranker_prompt.format(query=query, influencers=json.dumps(influencers, indent=2))
    response = client.models.generate_content(model="gemma-3-27b-it", contents=[prompt])

    try:
        match = re.search(r"\[.*\]", response.text, re.DOTALL)
        llm_scores = json.loads(match.group(0))

    except Exception:
        return results
    

    reranked = []
    for result in results:
        reranked.append({
            "id": result["id"],
            "score": llm_scores.get(result["id"], 0)
        })

    reranked.sort(key=lambda x: x["score"], reverse=True)
    return reranked