import os

import streamlit as st

from src.pdf_processor import extract_text_from_pdf, clean_text
from src.chunker import create_chunks
from src.retriever import DocumentRetriever
from src.qa import answer_question
from src.quiz_generator import generate_quiz


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

        # ---------------------------
        # PDF PROCESSING
        # ---------------------------

        raw_text = extract_text_from_pdf(pdf_path)
        text = clean_text(raw_text)

        st.success("PDF processed successfully!")

        st.subheader("Document Information")

        st.write(
            f"**Characters extracted:** {len(text):,}"
        )

        # ---------------------------
        # TEXT PREVIEW
        # ---------------------------

        st.subheader("Extracted Text")

        st.text_area(
            "Preview",
            text[:5000],
            height=400
        )

        # ---------------------------
        # CHUNKING
        # ---------------------------

        chunks = create_chunks(text)

        st.subheader("Document Chunks")

        st.write(
            f"Total chunks: {len(chunks)}"
        )

        for index, chunk in enumerate(
            chunks[:5],
            start=1
        ):
            with st.expander(
                f"Chunk {index}"
            ):
                st.write(chunk)

        # ---------------------------
        # RETRIEVER
        # ---------------------------

        retriever = DocumentRetriever(chunks)

        # ---------------------------
        # Q&A
        # ---------------------------

        st.subheader("Ask LearnQuest AI")

        question = st.text_input(
            "Ask a question about your uploaded document"
        )

        if question:

            with st.spinner(
                "Analyzing your document..."
            ):

                answer, results = answer_question(
                    retriever,
                    question,
                    top_k=2
                )

            st.markdown("### 🤖 Answer")

            st.write(answer)

            with st.expander(
                "View supporting document sections"
            ):

                for index, (chunk, score) in enumerate(
                    results,
                    start=1
                ):

                    st.markdown(
                        f"**Section {index} — "
                        f"Similarity: {score:.3f}**"
                    )

                    st.write(chunk)

        # ---------------------------
        # QUIZ GENERATION
        # ---------------------------

        st.subheader("📝 Generate Quiz")

        quiz_topic = st.text_input(
            "Enter a topic for the quiz",
            placeholder="Example: Mel-scale filter bank"
        )

        num_questions = st.slider(
            "Number of questions",
            min_value=1,
            max_value=5,
            value=3
        )

        if st.button("Generate Quiz"):

            if not quiz_topic.strip():

                st.warning(
                    "Please enter a topic."
                )

            else:

                with st.spinner(
                    "Generating quiz..."
                ):

                    quiz = generate_quiz(
                        retriever,
                        quiz_topic,
                        num_questions
                    )

                if not quiz:

                    st.error(
                        "Unable to generate a valid quiz "
                        "for this topic."
                    )

                else:

                    st.session_state["quiz"] = quiz

                    # Remove old score when generating
                    # a new quiz.
                    st.session_state.pop(
                        "quiz_score",
                        None
                    )

        # ---------------------------
        # DISPLAY QUIZ
        # ---------------------------

        if "quiz" in st.session_state:

            quiz = st.session_state["quiz"]

            st.markdown("### 🎯 Quiz")

            for index, q in enumerate(quiz):

                st.markdown(
                    f"**Question {index + 1}: "
                    f"{q['question']}**"
                )

                st.radio(
                    "Choose an answer:",
                    q["options"],
                    index=None,
                    key=f"quiz_question_{index}"
                )

                st.markdown("---")

            # ---------------------------
            # SUBMIT QUIZ
            # ---------------------------

            if st.button("Submit Quiz"):

                score = 0
                unanswered = 0

                for index, q in enumerate(quiz):

                    selected_answer = st.session_state.get(
                        f"quiz_question_{index}"
                    )

                    if selected_answer is None:

                        unanswered += 1

                        continue

                    correct_answer = q["options"][
                        q["answer"]
                    ]

                    if selected_answer == correct_answer:

                        score += 1

                if unanswered > 0:

                    st.warning(
                        f"Please answer all questions. "
                        f"Unanswered: {unanswered}"
                    )

                else:

                    st.session_state["quiz_score"] = score

            # ---------------------------
            # QUIZ RESULTS
            # ---------------------------

            if "quiz_score" in st.session_state:

                score = st.session_state["quiz_score"]

                st.success(
                    f"Your score: "
                    f"{score}/{len(quiz)}"
                )

                st.markdown(
                    "### 📋 Answer Review"
                )

                for index, q in enumerate(quiz):

                    correct_answer = q["options"][
                        q["answer"]
                    ]

                    selected_answer = st.session_state.get(
                        f"quiz_question_{index}"
                    )

                    if selected_answer == correct_answer:

                        st.markdown(
                            f"**Question {index + 1}: "
                            f"✅ Correct**"
                        )

                    else:

                        st.markdown(
                            f"**Question {index + 1}: "
                            f"❌ Incorrect**"
                        )

                    st.write(
                        f"Correct answer: "
                        f"**{correct_answer}**"
                    )

                    st.write(
                        f"Explanation: "
                        f"{q['explanation']}"
                    )

                    st.markdown("---")

    except Exception as error:

        st.error(
            f"Error processing PDF: {error}"
        )