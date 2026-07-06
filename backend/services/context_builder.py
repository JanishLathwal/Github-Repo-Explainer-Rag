from langchain_core.documents import Document


def build_context(documents: list[Document]) -> str:

    context_parts = []

    for document in documents:

        metadata = document.metadata

        context_parts.append(
            f"""
File: {metadata.get("path")}

Type: {metadata.get("chunk_type")}

Language: {metadata.get("language")}

-----------------------
{document.page_content}
"""
        )

    return "\n\n=====================================\n\n".join(context_parts)