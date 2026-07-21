from fastapi import APIRouter

from app.services.metadata_extractor import extract_metadata

router = APIRouter(
    prefix="/metadata"
)


@router.get("/test")
def test():

    sample = """
HR Work From Home Policy

Employees may work from home 4 days per week.

Effective Date: 1 July 2026

Version: v4

Status: Active

Department: HR

Author: HR Team
"""

    return extract_metadata(sample)