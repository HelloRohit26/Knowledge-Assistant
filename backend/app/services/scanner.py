from pathlib import Path
import hashlib


SUPPORTED_EXTENSIONS = {
    ".pdf",
    ".docx",
    ".txt",
    ".json",
    ".csv",
    ".xlsx"
}


def calculate_checksum(file_path):

    md5 = hashlib.md5()

    with open(file_path, "rb") as file:

        for chunk in iter(
            lambda: file.read(4096),
            b""
        ):
            md5.update(chunk)

    return md5.hexdigest()


def scan_data_folder(data_path):

    data_folder = Path(data_path)

    files_metadata = []

    for file_path in data_folder.rglob("*"):

        if not file_path.is_file():
            continue

        extension = file_path.suffix.lower()

        if extension not in SUPPORTED_EXTENSIONS:
            continue

        collection = file_path.parent.name

        metadata = {
            "file_name": file_path.name,
            "file_path": str(file_path),
            "collection": collection,
            "extension": extension,
            "last_modified": file_path.stat().st_mtime,
            "checksum": calculate_checksum(file_path)
        }

        files_metadata.append(metadata)

    return files_metadata