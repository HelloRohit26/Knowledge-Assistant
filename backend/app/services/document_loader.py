from llama_index.core import SimpleDirectoryReader


def load_multiple_files(files_metadata):

    file_paths = [
        file["file_path"]
        for file in files_metadata
    ]

    documents = SimpleDirectoryReader(
        input_files=file_paths
    ).load_data()

    for doc, file_info in zip(
        documents,
        files_metadata
    ):

        doc.metadata = {
            "file_name": file_info["file_name"],
            "collection": file_info["collection"],
            "file_path": file_info["file_path"]
        }

    return documents