from llama_index.core.node_parser import SentenceSplitter


splitter = SentenceSplitter(
    chunk_size=300,
    chunk_overlap=50
)


def create_chunks(documents):

    nodes = splitter.get_nodes_from_documents(
        documents
    )

    return nodes