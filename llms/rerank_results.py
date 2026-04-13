import os
import json
import re
from dotenv import load_dotenv
from google import genai
from prompts.reranker import reranker_prompt


def _parse_batch_scores(text):
    """Extract JSON array of scores from LLM response."""
    json_match = re.search(r"\[.*?\]", text, re.DOTALL)
    if not json_match:
        raise ValueError(f"Could not find JSON array in response: {text!r}")
    return json.loads(json_match.group(0))


def rerank_results(query, results):
    if not results:
        return results
    
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY environment variable not set")

    client = genai.Client(api_key=api_key)
    
    # Format all results into the prompt
    influencers_text = "\n".join(
        f"{i+1}. ID: {item['id']}, Influencer: {item['influencer']}, Hybrid score: {item['score']}"
        for i, item in enumerate(results)
    )
    
    prompt = (
        f"{reranker_prompt}\n\n"
        f"Query: {query}\n\n"
        f"Influencers to rank:\n{influencers_text}\n\n"
        "Respond with a JSON array of objects with 'id' and 'score' keys, "
        "e.g., [{\"id\": \"...\", \"score\": 8}, {\"id\": \"...\", \"score\": 7}]\n"
        "Response:"
    )
    
    response = client.models.generate_content(
        model="gemma-3-27b-it",
        contents=[prompt]
    )
    
    scores_data = _parse_batch_scores(response.text)
    score_map = {item["id"]: item["score"] for item in scores_data}
    
    reranked = [
        {**item, "llm_score": score_map.get(item["id"], 0)}
        for item in results
    ]
    reranked.sort(key=lambda row: row["llm_score"], reverse=True)
    return reranked

