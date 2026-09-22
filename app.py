import os

import streamlit as st

from src.pdf_processor import extract_text_from_pdf, clean_text
from src.chunker import create_chunks
from src.retriever import DocumentRetriever


st.set_page_config(
    page_title="LearnQuest AI",
    page_icon="🎓",
    layout="wide"
)

st.title("🎓 LearnQuest AI")

st.write(
    "Transform your study material into an interactive learning experience."
)

uploaded_file = st.file_uploader(
    "Upload your study PDF",
    type=["pdf"]
)


if uploaded_file is not None:

    os.makedirs("data/processed", exist_ok=True)

    pdf_path = "data/processed/uploaded.pdf"

    with open(pdf_path, "wb") as file:
        file.write(uploaded_file.getbuffer())

    try:
        raw_text = extract_text_from_pdf(pdf_path)
        text = clean_text(raw_text)

        st.success("PDF processed successfully!")

        st.subheader("Document Information")

        st.write(f"**Characters extracted:** {len(text):,}")

        st.subheader("Extracted Text")

        st.text_area(
            "Preview",
            text[:5000],
            height=400
        )

        chunks = create_chunks(text)

        st.subheader("Document Chunks")

        st.write(f"Total chunks: {len(chunks)}")

        for index, chunk in enumerate(chunks[:5], start=1):
            with st.expander(f"Chunk {index}"):
                st.write(chunk)

        retriever = DocumentRetriever(chunks)

        st.subheader("Test Document Retrieval")

        question = st.text_input(
            "Ask a question about your document"
        )

        if question:
            results = retriever.search(
                question,
                top_k=3
            )

            st.write("Most relevant sections:")

            for index, (chunk, score) in enumerate(results, start=1):
                with st.expander(
                    f"Result {index} — Similarity: {score:.3f}"
                ):
                    st.write(chunk)

    except Exception as error:
        st.error(f"Error processing PDF: {error}")