reranker_prompt = f"""Rate how well this influencer matches the search query.
hybrid result provides us : (top influencers who have potential to match)
- id 
- influencer (has main data to judge upon)
- hybrid search score.

Consider:
- Direct relevance to content needs.
- User intent (what niche they're looking for in influencer).
- Engagement rates and past collaborations.

Rank them on the basis of which one is better than the other influencers considering the above factors. 
output ONLY a list of dictionaries with rank, influencer and id without any explanation. 
"""