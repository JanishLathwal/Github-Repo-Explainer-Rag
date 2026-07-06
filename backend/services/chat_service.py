from core.retriever import get_retriever
from core.llm import llm
from langchain_core.messages import HumanMessage, AIMessage
from services.chat_memory import get_history
from services.context_builder import build_context

from prompts.qa_prompt import QA_PROMPT


def ask_repository(repo_id: str,session_id: str, question: str):

    history = get_history(session_id)

    history_text = ""

    for message in history:

        if isinstance(message, HumanMessage):
            history_text += f"User: {message.content}\n"

        elif isinstance(message, AIMessage):
            history_text += f"Assistant: {message.content}\n"

    retriever = get_retriever(repo_id)

    documents = retriever.invoke(question)

    context = build_context(documents)

    prompt = QA_PROMPT.format(
        history=history_text,
        context=context,
        question=question
    )

    response = llm.invoke(prompt)

    history.append(
        HumanMessage(content=question)
    )
    history.append(
        AIMessage(content=response.content)
    )

    return {
        "answer": response.content,
        "sources": [
            {
                "path": doc.metadata["path"],
                "chunk_type": doc.metadata["chunk_type"],
                "language": doc.metadata["language"]
            }
            for doc in documents
        ],
        "chunks_retrieved": len(documents)
    }