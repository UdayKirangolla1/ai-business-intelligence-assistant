from langchain_community.document_loaders import (
    PyPDFLoader,
    TextLoader,
    Docx2txtLoader
)

import tempfile
import os


def load_document(uploaded_file):

    suffix = uploaded_file.name.split(".")[-1]

    with tempfile.NamedTemporaryFile(delete=False, suffix=f".{suffix}") as tmp:
        tmp.write(uploaded_file.read())
        temp_path = tmp.name

    if suffix == "pdf":
        loader = PyPDFLoader(temp_path)

    elif suffix == "docx":
        loader = Docx2txtLoader(temp_path)

    elif suffix == "txt":
        loader = TextLoader(temp_path)

    else:
        raise ValueError("Unsupported file format")

    documents = loader.load()

    os.remove(temp_path)

    return documents