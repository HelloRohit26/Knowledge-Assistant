from google import genai
from google.genai import types

from app.core.config import settings


client = genai.Client(
    api_key=settings.GEMINI_API_KEY
)


def extract_topic(chunk: str) -> str:

    prompt = f"""
You are an enterprise knowledge classifier.

Read the following chunk.

Return ONLY the main topic.

Maximum 5 words.

Chunk:

{chunk[:3000]}
"""

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            temperature=0
        )
    )

    return response.text.strip()