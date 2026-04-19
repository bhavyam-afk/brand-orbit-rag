import os
import json
import re
from dotenv import load_dotenv
from google import genai
from prompts.reranker import reranker_prompt


def rerank_results(query, results):
    if not results:
        return results

    # 1. Setup
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY not set")

    client = genai.Client(api_key=api_key)

    # 2. Clean structured input for LLMs
    formatted_results = []
    for item in results:
        inf = item["influencer"]

        formatted_results.append({
            "id": str(item["id"]),
            "text": f"""
                Name: {inf.get('username')}
                Niche: {inf.get('niche')}
                Description: {inf.get('description')}
                Engagement: {inf.get('engagement_rate')}
                Location: {inf.get('location')}
                """.strip(),
            "hybrid_score": item["score"]
        })

    # 3. Build prompt
    prompt = reranker_prompt.format(
        query=query,
        influencers=json.dumps(formatted_results, indent=2)
    )

    # 4. Call LLM
    response = client.models.generate_content(
        model="gemma-3-27b-it",
        contents=[prompt]
    )

    # 5. SAFE JSON PARSING
    try:
        llm_output = response.text.strip()

        # extract JSON array using regex
        match = re.search(r"\[.*\]", llm_output, re.DOTALL)
        if not match:
            raise ValueError("No JSON array found")

        json_str = match.group(0)
        scores_data = json.loads(json_str)

        # validate structure
        if not isinstance(scores_data, list):
            raise ValueError("Parsed data is not a list")

    except Exception as e:
        print("Failed to parse LLM response:", e)
        print("Raw response:", repr(response.text))

        return [
            {
                "id": str(item["id"]),
                "influencer": item["influencer"],
                "hybrid_score": item["score"],
                "llm_score": 0
            }
            for item in results
        ]

    # 6. Build llm score map
    score_map = {
        str(item["id"]): item.get("score", 0)
        for item in scores_data
    }

    # 7. Merge scores
    reranked = []
    for item in results:
        influencer_id = str(item["id"])

        reranked.append({
            "id": influencer_id,
            "influencer": item["influencer"],
            "hybrid_score": item["score"],
            "llm_score": score_map.get(influencer_id, 0)
        })

    # 8. Sort
    reranked.sort(key=lambda x: x["llm_score"], reverse=True)

    return reranked