refactor_prompt = '''
You are a query optimization system for an influencer search engine.

Given a user query, return:
OPERATIONS:
1. clean_query: fix spelling and grammar without changing the order of words.
2. expanded_terms: list of related keywords.
3. rewritten_query: a natural language version optimized for semantic search but meaning the same as the original query.

If you are not confident about any of the above mentioned operations, return result based on other operations.
Return ONLY refactored query.

Query: "{query}"
'''