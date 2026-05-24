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
st.write("Upload a business document and ask questions about it using RAG.")

# File Upload
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
        with st.spinner("Searching document..."):
            answer, relevant_docs = generate_answer(question, retriever)

        st.subheader("Answer")
        st.write(answer)

        with st.expander("Retrieved Source Chunks"):
            for i, doc in enumerate(relevant_docs, start=1):
                st.markdown(f"**Source {i}**")
                st.write(doc.page_content)
                st.divider()