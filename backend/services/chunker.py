import os
import traceback
from tree_sitter_language_pack import get_parser
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from config import SEMANTIC_NODES
# this helps when we are chunking the texts files like readme 
def recursive_chunk(document:Document)-> list[Document]:

    content=document.page_content

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    chunks = splitter.split_text(content)
    result = []

    for index, chunk in enumerate(chunks):

        metadata = document.metadata.copy()

        metadata["chunk_type"] = "text"
        metadata["chunk_index"] = index

        result.append(
            Document(
                page_content=chunk,
                metadata=metadata
            )
        )
        
    return result


# for code bases and all
# traversing the tree recursively 
def traverse_tree(current_node,source: str,document: Document,chunks: list[Document],semantic_nodes,):
    
    if current_node.kind() in semantic_nodes:

        chunk_content = source[
            current_node.start_byte(): current_node.end_byte()
        ]

        metadata = document.metadata.copy()

        metadata["chunk_type"] = current_node.kind()
        metadata["chunk_index"] = len(chunks)

        chunks.append(
            Document(
                page_content=chunk_content,
                metadata=metadata,
            )
        )

        return 

    for i in range(current_node.child_count()):
        traverse_tree(
            current_node.child(i),
            source,
            document,
            chunks,
            semantic_nodes,
        )


# semantic chunking on the basis of the nodes : {"class_definition","function_definition","method_definition"}
def semantic_chunk(document: Document) -> list[Document]:

    language = document.metadata.get("language", "text")

    parser = get_parser(language)

    source = document.page_content

    tree = parser.parse(source)

    semantic_nodes = SEMANTIC_NODES.get(language, set())

    chunks = []

    traverse_tree(
        tree.root_node(),
        source,
        document,
        chunks,
        semantic_nodes,
    )
    
    return chunks


# chunking all the files 
def chunk_document(document: Document) -> list[Document]:

    language = document.metadata.get("language", "text")

    try:

        if language in SEMANTIC_NODES:

            chunks = semantic_chunk(document)

            if chunks:
                return chunks

        return recursive_chunk(document)

    except Exception:
        traceback.print_exc()
        return recursive_chunk(document)

def chunk_documents(documents: list[Document]) -> list[Document]:

    chunked_documents = []

    for document in documents:
    #     chunked_documents.extend(
    #         chunk_document(document)
    #     )
        chunks = chunk_document(document)
        chunked_documents.extend(chunks)

    return chunked_documents
    