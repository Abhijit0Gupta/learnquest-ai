import os
import streamlit as st

from src.pdf_processor import extract_text_from_pdf, clean_text

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

        st.write(f"**Pages:** {len(text.split(chr(12))) + 1}")
        st.write(f"**Characters extracted:** {len(text):,}")

        st.subheader("Extracted Text")

        st.text_area(
            "Preview",
            text[:5000],
            height=400
        )

    except Exception as error:
        st.error(f"Error processing PDF: {error}")