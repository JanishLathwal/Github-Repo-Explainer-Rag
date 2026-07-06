import uuid
import requests
import streamlit as st

BACKEND_URL = "http://127.0.0.1:8000"

# --------------------------------------------------
# Page Config
# --------------------------------------------------

st.set_page_config(
    page_title="GitHub Repository Explainer",
    page_icon="📚",
    layout="wide"
)

# --------------------------------------------------
# Session State
# --------------------------------------------------

if "repo_id" not in st.session_state:
    st.session_state.repo_id = None

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

if "documents" not in st.session_state:
    st.session_state.documents = 0

if "chunks" not in st.session_state:
    st.session_state.chunks = 0

# --------------------------------------------------
# Sidebar
# --------------------------------------------------

st.sidebar.title("📚 GitHub Repository Explainer")

st.sidebar.markdown("---")

if st.session_state.repo_id:

    st.sidebar.success("Repository Indexed")

    st.sidebar.write(f"**Repo:**")
    st.sidebar.code(st.session_state.repo_id)

    st.sidebar.metric(
        "Documents",
        st.session_state.documents
    )

    st.sidebar.metric(
        "Chunks",
        st.session_state.chunks
    )

else:

    st.sidebar.warning("No Repository Indexed")

st.sidebar.markdown("---")

if st.sidebar.button("🗑 Clear Chat", use_container_width=True):

    st.session_state.chat_history = []

    st.session_state.session_id = str(uuid.uuid4())

    st.rerun()

st.sidebar.markdown("---")

st.sidebar.caption(
    "Built using\n\nFastAPI\n\nLangChain\n\nQdrant\n\nGemini\n\nTree-sitter\n\nStreamlit"
)

# --------------------------------------------------
# Title
# --------------------------------------------------

st.title("📚 GitHub Repository Explainer")

st.write(
    "Index any GitHub repository and ask questions about its code."
)

st.divider()

# --------------------------------------------------
# Repository Indexing
# --------------------------------------------------

st.subheader("Index Repository")

repo_url = st.text_input(
    "GitHub Repository URL",
    placeholder="https://github.com/owner/repository"
)

if st.button(
    "🚀 Index Repository",
    use_container_width=True
):

    if repo_url.strip() == "":

        st.warning("Please enter a GitHub URL.")

    else:

        try:

            with st.spinner("Cloning repository..."):

                response = requests.post(
                    f"{BACKEND_URL}/repo/index",
                    json={
                        "repo_url": repo_url
                    }
                )

            if response.status_code == 200:

                data = response.json()

                st.session_state.repo_id = data["repo_id"]

                st.session_state.documents = data["documents"]

                st.session_state.chunks = data["chunks"]

                st.success("Repository indexed successfully!")

                c1, c2, c3 = st.columns(3)

                c1.metric(
                    "Documents",
                    data["documents"]
                )

                c2.metric(
                    "Chunks",
                    data["chunks"]
                )

                c3.metric(
                    "Status",
                    "Ready"
                )

            else:

                st.error(response.text)

        except requests.exceptions.ConnectionError:

            st.error(
                "Cannot connect to FastAPI backend."
            )

        except Exception as e:

            st.error(e)

st.divider()

# --------------------------------------------------
# Chat
# --------------------------------------------------

st.subheader("💬 Chat")

if st.session_state.repo_id is None:

    st.info("Please index a repository first.")

else:

    st.info(f"Current Repository: **{st.session_state.repo_id}**")

    # ------------------------
    # Display Chat History
    # ------------------------

    for message in st.session_state.chat_history:

        with st.chat_message(message["role"]):

            st.markdown(message["content"])

            if message["role"] == "assistant":

                sources = message.get("sources", [])

                if sources:

                    st.markdown("#### 📄 Referenced Files")

                    shown = set()

                    for source in sources:

                        path = source["path"]

                        if path not in shown:

                            shown.add(path)

                            st.markdown(f"- `{path}`")

                    if "chunks" in message:

                        st.caption(
                            f"Retrieved {message['chunks']} chunks"
                        )

    # ------------------------
    # User Input
    # ------------------------

    question = st.chat_input(
        "Ask a question..."
    )

    if question:

        # Show user instantly

        st.session_state.chat_history.append(
            {
                "role": "user",
                "content": question
            }
        )

        with st.chat_message("user"):

            st.markdown(question)

        try:

            with st.spinner("Analyzing repository..."):

                response = requests.post(
                    f"{BACKEND_URL}/chat",
                    json={
                        "repo_id": st.session_state.repo_id,
                        "session_id": st.session_state.session_id,
                        "question": question
                    }
                )

            if response.status_code == 200:

                result = response.json()

                answer = result["answer"]

                sources = result.get(
                    "sources",
                    []
                )

                chunks = result.get(
                    "chunks_retrieved",
                    0
                )

                st.session_state.chat_history.append(
                    {
                        "role": "assistant",
                        "content": answer,
                        "sources": sources,
                        "chunks": chunks
                    }
                )

                with st.chat_message("assistant"):

                    st.markdown(answer)

                    if sources:

                        st.markdown(
                            "#### 📄 Referenced Files"
                        )

                        shown = set()

                        for source in sources:

                            path = source["path"]

                            if path not in shown:

                                shown.add(path)

                                st.markdown(
                                    f"- `{path}`"
                                )

                    st.caption(
                        f"Retrieved {chunks} chunks"
                    )

            else:

                st.error(response.text)

        except requests.exceptions.ConnectionError:

            st.error(
                "Cannot connect to FastAPI backend."
            )

        except Exception as e:

            st.error(e)

st.divider()

st.caption(
    "🚀 GitHub Repository Explainer | FastAPI • LangChain • Qdrant • Gemini • Tree-sitter • Streamlit"
)