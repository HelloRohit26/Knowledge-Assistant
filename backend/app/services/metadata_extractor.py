from google import genai
from google.genai import types

from app.core.config import settings
from app.models.document_metadata import DocumentMetadata
from app.services.document_rules import apply_document_rules
from app.services.metadata_validator import validate_metadata


client = genai.Client(
    api_key=settings.GEMINI_API_KEY
)


def extract_metadata(text: str) -> DocumentMetadata:

    prompt = f"""
You are an enterprise document classifier.

Extract metadata from this document.

Document:

{text[:8000]}
"""

    response = client.models.generate_content(
        model="gemini-3.5-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            temperature=0,
            response_mime_type="application/json",
            response_schema=DocumentMetadata,
        )
    )

    metadata = response.parsed

    # Apply rule engine
    metadata = apply_document_rules(metadata)

    # Convert to dict, validate, convert back
    metadata_dict = metadata.model_dump()
    metadata_dict = validate_metadata(metadata_dict)

    # Reconstruct validated model
    validated = DocumentMetadata(**metadata_dict)

    return validated