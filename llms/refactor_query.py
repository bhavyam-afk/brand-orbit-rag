from google import genai
import os
from dotenv import load_dotenv
from typer import prompt
from prompts.refactor_query import refactor_prompt 

def refactor_query():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY environment variable not set")

    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model="gemma-3-27b-it",
        contents=[refactor_prompt]
    )
    return response.text
