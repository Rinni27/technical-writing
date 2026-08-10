"""
Core RAG logic: retrieve relevant doc chunks from ChromaDB, score confidence,
and generate a grounded answer with the Claude API.
"""

import os
import re
from pathlib import Path

import chromadb
from anthropic import Anthropic
from chromadb.utils import embedding_functions
from dotenv import load_dotenv

load_dotenv()

CHROMA_DIR = Path(__file__).parent / "chroma_db"
COLLECTION_NAME = "pet_api_docs"
CLAUDE_MODEL = os.environ.get("CLAUDE_MODEL", "claude-sonnet-5")

# Cosine similarity thresholds for labeling retrieval confidence.
# Tuned for all-MiniLM-L6-v2 embeddings on short technical doc chunks.
HIGH_CONFIDENCE_THRESHOLD = 0.5
MEDIUM_CONFIDENCE_THRESHOLD = 0.3

# Questions about error/status/response codes should be answered from each
# endpoint's "Responses" section — but that section is a tiny table, so it
# often loses out on raw semantic similarity to longer, keyword-dense
# overview chunks. When this pattern matches, we explicitly pull from
# Responses-section chunks and put them first, rather than relying purely
# on whole-corpus vector similarity.
CODE_QUESTION_PATTERN = re.compile(r"\b(error|status|response)\s*codes?\b", re.IGNORECASE)
RESPONSES_SECTION_BOOST_COUNT = 3

SYSTEM_PROMPT = """You are a documentation assistant for the Pet API developer portal.
Answer the user's question using ONLY the documentation excerpts provided in their message.

Rules:
- Be concise and accurate. Prefer short, direct answers with concrete details (endpoint paths, \
status codes, field names) drawn from the excerpts.
- If the excerpts don't contain enough information to answer confidently, say so plainly instead \
of guessing or inventing details.
- Never invent endpoints, fields, status codes, or behavior that isn't in the provided excerpts.
- When useful, mention which section of the docs your answer is based on.
"""

_chroma_client = None
_collection = None
_anthropic_client = None


def get_collection():
    global _chroma_client, _collection
    if _collection is None:
        _chroma_client = chromadb.PersistentClient(path=str(CHROMA_DIR))
        embedding_fn = embedding_functions.DefaultEmbeddingFunction()
        _collection = _chroma_client.get_collection(
            name=COLLECTION_NAME,
            embedding_function=embedding_fn,
        )
    return _collection


def get_anthropic_client():
    global _anthropic_client
    if _anthropic_client is None:
        api_key = os.environ.get("ANTHROPIC_API_KEY")
        if not api_key:
            raise RuntimeError(
                "ANTHROPIC_API_KEY is not set. Add it to pet-api-rag-assistant/.env"
            )
        _anthropic_client = Anthropic(api_key=api_key)
    return _anthropic_client


def _run_query(question: str, n_results: int, where: dict | None = None):
    collection = get_collection()
    results = collection.query(query_texts=[question], n_results=n_results, where=where)

    chunks = []
    for chunk_id, doc, meta, distance in zip(
        results["ids"][0], results["documents"][0], results["metadatas"][0], results["distances"][0]
    ):
        similarity = 1 - distance
        chunks.append({"id": chunk_id, "text": doc, "metadata": meta, "similarity": similarity})
    return chunks


def retrieve(question: str, n_results: int = 6):
    chunks = _run_query(question, n_results=n_results)

    if CODE_QUESTION_PATTERN.search(question):
        boosted = _run_query(
            question, n_results=RESPONSES_SECTION_BOOST_COUNT, where={"section": "Responses"}
        )
        boosted_ids = {c["id"] for c in boosted}
        chunks = boosted + [c for c in chunks if c["id"] not in boosted_ids]
        chunks = chunks[:n_results]

    return chunks


def score_confidence(chunks: list[dict]):
    if not chunks:
        return 0.0, "low"

    top_similarity = chunks[0]["similarity"]
    if top_similarity >= HIGH_CONFIDENCE_THRESHOLD:
        label = "high"
    elif top_similarity >= MEDIUM_CONFIDENCE_THRESHOLD:
        label = "medium"
    else:
        label = "low"
    return top_similarity, label


def build_context(chunks: list[dict]) -> str:
    parts = []
    for c in chunks:
        meta = c["metadata"]
        parts.append(f"[Source: {meta['title']} — {meta['section']}]\n{c['text']}")
    return "\n\n---\n\n".join(parts)


def ask(question: str, history: list[dict] | None = None, n_results: int = 6) -> dict:
    """
    history: list of prior {"role": "user"|"assistant", "content": str} turns,
             plain text without retrieved context re-injected.
    """
    chunks = retrieve(question, n_results=n_results)
    top_score, confidence_label = score_confidence(chunks)
    context = build_context(chunks)

    messages = list(history) if history else []
    messages.append(
        {
            "role": "user",
            "content": (
                f"Documentation excerpts:\n\n{context}\n\n"
                f"Question: {question}"
            ),
        }
    )

    client = get_anthropic_client()
    response = client.messages.create(
        model=CLAUDE_MODEL,
        max_tokens=1024,
        system=SYSTEM_PROMPT,
        messages=messages,
    )
    answer = "".join(
        block.text for block in response.content if block.type == "text"
    )

    sources = [
        {
            "title": c["metadata"]["title"],
            "section": c["metadata"]["section"],
            "url": c["metadata"]["url"],
            "similarity": round(c["similarity"], 3),
        }
        for c in chunks
    ]

    return {
        "answer": answer,
        "sources": sources,
        "confidence_score": round(top_score, 3),
        "confidence_label": confidence_label,
    }
