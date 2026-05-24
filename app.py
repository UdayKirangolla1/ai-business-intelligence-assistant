import os
import streamlit as st

from src.document_loader import load_document
from src.text_splitter import split_documents
from src.embeddings import load_embeddings
from src.vector_store import create_vector_store
from src.retriever import create_retriever
from src.rag_chain import generate_answer


st.set_page_config(
    page_title="AI Business Intelligence Assistant",
    layout="wide"
)

st.title("AI Business Intelligence Assistant")
st.write("Upload a business document and ask questions about it using RAG + Claude AI.")

# ── API Key Input ──────────────────────────────────────────────────────────────
with st.sidebar:
    st.header("Configuration")
    api_key = st.text_input(
        "Anthropic API Key",
        type="password",
        placeholder="sk-ant-..."
    )
    if api_key:
        os.environ["ANTHROPIC_API_KEY"] = api_key
        st.success("API key set!")
    else:
        st.warning("Enter your Anthropic API key to enable AI answers.")

# ── File Upload ────────────────────────────────────────────────────────────────
uploaded_file = st.file_uploader(
    "Upload PDF, TXT, or DOCX file",
    type=["pdf", "txt", "docx"]
)

question = st.text_input("Ask a question about the uploaded document")

if uploaded_file is not None:

    with st.spinner("Processing document..."):
        documents = load_document(uploaded_file)
        chunks = split_documents(documents)
        embeddings = load_embeddings()
        vectorstore = create_vector_store(chunks, embeddings)
        retriever = create_retriever(vectorstore)

    st.success(f"Document processed! {len(chunks)} chunks created.")

    if question:
        if not os.environ.get("ANTHROPIC_API_KEY"):
            st.error("Please enter your Anthropic API key in the sidebar first.")
        else:
            with st.spinner("Generating answer..."):
                answer, relevant_docs = generate_answer(question, retriever)

            st.subheader("Answer")
            st.write(answer)

            with st.expander("Retrieved Source Chunks"):
                for i, doc in enumerate(relevant_docs, start=1):
                    st.markdown(f"**Source {i}**")
                    st.write(doc.page_content)
                    st.divider()