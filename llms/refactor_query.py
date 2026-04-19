from google import genai
import os
from dotenv import load_dotenv
from prompts.refactor_prompt import refactor_prompt 

def refactor_query(query):
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY environment variable not set")

    formatted_prompt = refactor_prompt.format(query=query)     

    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model="gemma-3-27b-it",
        contents=[formatted_prompt]
    )
    return response.text
