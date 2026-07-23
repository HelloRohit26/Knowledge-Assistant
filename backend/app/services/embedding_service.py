try:
    from llama_index.embeddings.google_genai import GoogleGenAIEmbedding
except ModuleNotFoundError:
    try:
        from llama_index.embeddings.google import GoogleEmbedding as GoogleGenAIEmbedding
    except ModuleNotFoundError:
        from llama_index.embeddings.gemini import GeminiEmbedding as GoogleGenAIEmbedding

from app.core.config import settings


embed_model = GoogleGenAIEmbedding(
    model_name="models/gemini-embedding-2",
    api_key=settings.GEMINI_API_KEY
)


def get_embedding(text):

    embedding = embed_model.get_text_embedding(
        text
    )

    return embedding