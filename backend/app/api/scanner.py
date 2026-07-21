from fastapi import APIRouter

from app.services.scanner import scan_data_folder
from app.core.config import settings

router = APIRouter()


@router.get("/scan")
def scan_files():

    files = scan_data_folder(settings.DATA_FOLDER)

    return {
        "total_files": len(files),
        "files": files
    }