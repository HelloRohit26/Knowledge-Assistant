from fastapi import APIRouter

from app.database.file_tracker import (
    add_indexed_file,
    get_all_indexed_files
)

router = APIRouter(
    prefix="/db-test",
    tags=["Database Test"]
)


@router.get("/add")
def add_test_record():

    add_indexed_file(
        file_name="test.pdf",
        file_path="data/hr/test.pdf",
        collection="hr",
        last_modified=123456789
    )

    return {
        "message": "Test record inserted successfully"
    }


@router.get("/list")
def list_records():

    rows = get_all_indexed_files()

    return {
        "total_records": len(rows),
        "records": rows
    }