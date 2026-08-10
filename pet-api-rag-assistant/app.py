"""
Streamlit UI for the Pet API "Ask the Docs" RAG assistant.

Run with:
    streamlit run app.py
"""

import csv
from datetime import datetime, timezone
from pathlib import Path

import streamlit as st

from generate_faq import OUTPUT_FILE as FAQ_FILE
from generate_faq import generate_faq
from rag import ask

LIVE_DOCS_BASE_URL = "https://rinni27.github.io/technical-writing/pet-api-docs"

FEEDBACK_DIR = Path(__file__).parent / "feedback"
FEEDBACK_FILE = FEEDBACK_DIR / "feedback.csv"

CONFIDENCE_STYLE = {
    "high": ("🟢", "High confidence"),
    "medium": ("🟡", "Medium confidence"),
    "low": ("🔴", "Low confidence"),
}

st.set_page_config(page_title="Ask the Pet API Docs", page_icon="🐾", layout="centered")


def log_feedback(question, answer, rating, confidence_label, confidence_score):
    FEEDBACK_DIR.mkdir(exist_ok=True)
    file_exists = FEEDBACK_FILE.exists()
    with open(FEEDBACK_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(
                ["timestamp_utc", "question", "answer", "rating", "confidence_label", "confidence_score"]
            )
        writer.writerow(
            [
                datetime.now(timezone.utc).isoformat(),
                question,
                answer,
                rating,
                confidence_label,
                confidence_score,
            ]
        )


st.title("🐾 Ask the Pet API Docs")
st.caption(
    "A RAG-powered assistant that answers questions using the "
    "[Pet API documentation](%s)." % LIVE_DOCS_BASE_URL
)

chat_tab, faq_tab = st.tabs(["💬 Ask the Docs", "❓ FAQ"])

with chat_tab:
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "turns" not in st.session_state:
        st.session_state.turns = []

    for i, turn in enumerate(st.session_state.turns):
        with st.chat_message("user"):
            st.markdown(turn["question"])

        with st.chat_message("assistant"):
            st.markdown(turn["answer"])

            icon, label = CONFIDENCE_STYLE[turn["confidence_label"]]
            st.caption(f"{icon} {label} · retrieval score {turn['confidence_score']}")

            if turn["confidence_label"] == "low":
                st.warning(
                    "I couldn't find a strong match for this in the docs — treat this answer with caution."
                )

            with st.expander("Sources"):
                for s in turn["sources"]:
                    st.markdown(
                        f"- [{s['title']} — {s['section']}]({LIVE_DOCS_BASE_URL}{s['url']}) "
                        f"(similarity: {s['similarity']})"
                    )

            col1, col2, _ = st.columns([1, 1, 8])
            feedback_given = turn.get("feedback") is not None
            with col1:
                if st.button("👍", key=f"up_{i}", disabled=feedback_given):
                    turn["feedback"] = "up"
                    log_feedback(
                        turn["question"], turn["answer"], "up",
                        turn["confidence_label"], turn["confidence_score"],
                    )
                    st.rerun()
            with col2:
                if st.button("👎", key=f"down_{i}", disabled=feedback_given):
                    turn["feedback"] = "down"
                    log_feedback(
                        turn["question"], turn["answer"], "down",
                        turn["confidence_label"], turn["confidence_score"],
                    )
                    st.rerun()
            if feedback_given:
                st.caption("Feedback recorded — thank you.")

    question = st.chat_input("Ask a question about the Pet API...")
    if question:
        with st.spinner("Searching the docs..."):
            result = ask(question, history=st.session_state.messages)

        st.session_state.messages.append({"role": "user", "content": question})
        st.session_state.messages.append({"role": "assistant", "content": result["answer"]})
        st.session_state.turns.append(
            {
                "question": question,
                "answer": result["answer"],
                "sources": result["sources"],
                "confidence_score": result["confidence_score"],
                "confidence_label": result["confidence_label"],
                "feedback": None,
            }
        )
        st.rerun()

with faq_tab:
    st.caption("Regenerate any time the docs change.")

    if st.button("🔄 Regenerate FAQ"):
        with st.spinner("Scanning the docs and generating a fresh FAQ..."):
            faq_markdown = generate_faq()
            FAQ_FILE.parent.mkdir(exist_ok=True)
            FAQ_FILE.write_text(faq_markdown, encoding="utf-8")
        st.rerun()

    if FAQ_FILE.exists():
        last_generated = datetime.fromtimestamp(
            FAQ_FILE.stat().st_mtime, tz=timezone.utc
        ).strftime("%Y-%m-%d %H:%M UTC")
        st.caption(f"Last generated: {last_generated}")
        st.markdown(FAQ_FILE.read_text(encoding="utf-8"))
    else:
        st.info("No FAQ generated yet — click the button above to create one.")
