from google import genai
from google.genai import types

from app.core.config import settings
from app.models.document_metadata import DocumentMetadata
from app.services.document_rules import apply_document_rules
from app.services.metadata_validator import validate_metadata
from app.core.logger import logger


def get_client():
    if settings.GEMINI_API_KEY:
        return genai.Client(api_key=settings.GEMINI_API_KEY)
    return None


def extract_metadata(text: str) -> DocumentMetadata:
    metadata = None
    try:
        client = get_client()
        if client:
            prompt = f"""
You are an enterprise document classifier.

Extract metadata from this document.

Document:

{text[:8000]}
"""
            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=0,
                    response_mime_type="application/json",
                    response_schema=DocumentMetadata,
                )
            )
            metadata = response.parsed
    except Exception as e:
        logger.warning(f"Gemini metadata extraction fallback triggered: {e}")

    if not metadata:
        metadata = DocumentMetadata(summary=text[:200] if text else "Document content")

    # Apply rule engine
    metadata = apply_document_rules(metadata)

    # Convert to dict, validate, convert back
    metadata_dict = metadata.model_dump()
    metadata_dict = validate_metadata(metadata_dict)

    # Reconstruct validated model
    validated = DocumentMetadata(**metadata_dict)

    return validated