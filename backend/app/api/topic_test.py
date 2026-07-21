from fastapi import APIRouter

from app.services.topic_extractor import extract_topic

router = APIRouter(
    prefix="/topic"
)


@router.get("/test")
def test():

    chunk = """
Employees may work from home
4 days every week.

The policy is effective
from July 2026.
"""

    return {
        "topic": extract_topic(chunk)
    }