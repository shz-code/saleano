import os
from google import genai

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def get_embedding(text: str):
    result = client.models.embed_content(
        model="gemini-embedding-001",
        contents=[text]
    )
    return result.embeddings[0].values