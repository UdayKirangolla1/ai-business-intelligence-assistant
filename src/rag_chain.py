import os

def generate_answer(question, retriever):

    # Step 1: Retrieve relevant chunks
    relevant_docs = retriever.invoke(question)

    # Step 2: Deduplicate chunks
    unique_docs = []
    seen_texts = set()

    for doc in relevant_docs:
        text = doc.page_content.strip()
        if text not in seen_texts:
            unique_docs.append(doc)
            seen_texts.add(text)

    # Step 3: Build context string from chunks
    context = ""
    for i, doc in enumerate(unique_docs, start=1):
        context += f"\nSource {i}:\n"
        context += doc.page_content
        context += "\n"

    # Step 4: Try Claude API if key is available
    api_key = os.environ.get("ANTHROPIC_API_KEY")

    if api_key:
        try:
            import anthropic
            client = anthropic.Anthropic(api_key=api_key)

            message = client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=1024,
                messages=[
                    {
                        "role": "user",
                        "content": f"""You are a helpful business intelligence assistant.
Answer the user's question using ONLY the context provided below.
If the context does not contain enough information to answer fully, say so clearly.
Always mention which source(s) your answer is based on.

Context:
{context}

Question: {question}

Answer:"""
                    }
                ]
            )

            answer = message.content[0].text
            return answer, unique_docs

        except Exception:
            pass  # Fall through to formatted retrieval answer

    # Step 5: Fallback — format retrieved chunks as a clean readable answer
    answer = f"Based on the most relevant sections found in the document:\n\n"

    for i, doc in enumerate(unique_docs, start=1):
        answer += f"📄 Source {i}:\n{doc.page_content.strip()}\n\n"

    answer += "---\n💡 Tip: Add an Anthropic API key in the sidebar to get AI-synthesized answers."

    return answer, unique_docs