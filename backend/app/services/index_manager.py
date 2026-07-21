from app.services.scanner import scan_data_folder

from app.database.file_tracker import (
    is_file_indexed,
    add_indexed_file
)

from app.core.config import settings


def index_files():

    files = scan_data_folder(settings.DATA_FOLDER)

    new_files = []
    skipped_files = 0

    for file in files:

        if is_file_indexed(file["file_path"]):
            skipped_files += 1
            continue

        add_indexed_file(
            file_name=file["file_name"],
            file_path=file["file_path"],
            collection=file["collection"],
            last_modified=file["last_modified"]
        )

        new_files.append(file["file_name"])

    return {
        "total_scanned": len(files),
        "new_files": len(new_files),
        "skipped_files": skipped_files,
        "new_file_names": new_files
    }