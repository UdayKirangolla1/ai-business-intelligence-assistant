def create_retriever(vectorstore):

    retriever = vectorstore.as_retriever(
        search_kwargs={"k": 2}
    )

    return retriever