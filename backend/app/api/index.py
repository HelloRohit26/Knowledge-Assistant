from fastapi import APIRouter

from app.services.index_manager import index_files

router = APIRouter(
    tags=["Indexing"]
)


@router.get("/index-files")
def run_indexing():

    result = index_files()

    return result