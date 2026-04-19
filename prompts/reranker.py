reranker_prompt = """
You are a ranking system for an influencer search engine.

TASK:
Given a user query and a list of influencers, assign a relevance score (0–10) to each influencer.

SCORING GUIDELINES:
- 10 = perfect match to brand's intent.
- 7-9 = strong match
- 4-6 = moderate match
- 1-3 = weak match
- 0 = irrelevant

CONSIDER:
- relevance to query intent
- niche and audience alignment
- engagement rate and content quality
- already assigned score from hybrid search (use as a reference, but adjust based on your judgment)

IMPORTANT RULES:
- Return ONLY valid JSON
- No explanation, no text outside JSON
- Output must be a list of objects with EXACT keys: "id" and "score"
- Keep ALL ids from input (do not drop any)

QUERY: {query}
INFLUENCERS with hybrid search scoes: {influencers}

EXAMPLE FORMAT:
[
  {{"id": "123", "score": 9}},
  {{"id": "456", "score": 7}}
]
"""