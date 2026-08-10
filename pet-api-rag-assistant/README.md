# Ask the Pet API Docs — RAG-Powered Documentation Assistant

A retrieval-augmented generation (RAG) assistant that answers developer questions about the [Pet API documentation](https://rinni27.github.io/technical-writing/pet-api-docs/) — grounded strictly in the docs, with confidence scoring, cited sources, and a feedback loop. Built end-to-end: ingestion pipeline, vector search, LLM answer generation, UI, and cloud deployment.

**Try it live:**
- Embedded in the docs: [pet-api-docs/ask-the-docs](https://rinni27.github.io/technical-writing/pet-api-docs/ask-the-docs/)
- Standalone app: [technical-writing-rinni27.streamlit.app](https://technical-writing-rinni27.streamlit.app/)

---

## Why this exists

Static documentation is searchable but not *answerable*. A developer integrating with an API usually has a specific question ("what status code do I get if a pet isn't found?") and has to hunt across multiple pages for it. This project turns the docs into a system that can be asked directly — while staying strictly grounded in what the documentation actually says, rather than guessing.

## What it does

| Feature | Description |
|---|---|
| **Grounded Q&A** | Answers are generated only from retrieved doc content — the assistant explicitly declines to answer when the docs don't cover something, instead of hallucinating. |
| **Confidence scoring** | Every answer shows a 🟢/🟡/🔴 confidence badge based on how well the retrieved content actually matched the question, so users know when to double-check. |
| **Source citations** | Each answer links back to the exact documentation section it came from, on the live docs site. |
| **Conversation memory** | Follow-up questions ("what about its status codes?") work naturally within a session. |
| **Feedback loop** | 👍/👎 on every answer, logged to CSV with the question, answer, and confidence score — a real signal for which docs need improvement. |
| **Auto-generated FAQ** | A one-click button has Claude scan the entire doc set and produce a organized, grounded FAQ page — regenerable any time the docs change. |
| **Embedded in the docs site** | Lives natively inside the MkDocs portal via iframe, not a separate tab a visitor has to go find. |

## How it works

```
Pet API docs (Markdown)
        │
        ▼
  ingest.py  ──  chunk by section, embed locally (MiniLM), store in ChromaDB
        │
        ▼
   rag.py   ──  embed the question → vector search → retrieve top chunks
        │        → score confidence (cosine similarity)
        │        → call Claude with the retrieved context
        ▼
Claude API  ──  generates an answer grounded only in the retrieved excerpts
        │
        ▼
   app.py   ──  Streamlit UI: chat, confidence badge, sources, feedback, FAQ tab
```

**Retrieval design decisions worth noting:**
- Docs are chunked by markdown section (H1/H2), not fixed-size windows — each chunk is a coherent unit (e.g. one endpoint's "Responses" section), which produces much cleaner citations than arbitrary text splitting.
- Questions about error/status/response codes get a targeted second search restricted to each endpoint's "Responses" section specifically. Those sections are small tables that were losing out to longer, keyword-dense overview chunks on raw semantic similarity alone — this fix made retrieval reliably correct for one of the most common question types developers ask.
- The vector index isn't committed to git (it's regenerated output); the app detects a missing index and builds it automatically on first run, which is what makes a from-scratch cloud deployment work without any manual setup step.

## Tech stack

- **Embeddings**: `all-MiniLM-L6-v2`, run locally via ChromaDB's built-in ONNX runtime — no external embedding API, no cost.
- **Vector store**: ChromaDB (persistent, local, cosine similarity).
- **LLM**: Claude (Anthropic API) — generates the final answer and the auto-generated FAQ.
- **UI**: Streamlit.
- **Deployment**: Streamlit Community Cloud, secrets managed outside the repo.

## File structure

```
pet-api-rag-assistant/
├── ingest.py            # Chunks the docs and builds the ChromaDB vector index
├── rag.py               # Core RAG logic: retrieval, confidence scoring, Claude calls
├── app.py               # Streamlit UI — chat tab + FAQ tab
├── generate_faq.py      # Standalone + in-app FAQ generator (Claude scans docs → FAQ markdown)
├── requirements.txt     # chromadb, anthropic, streamlit, python-dotenv
├── .env.example         # Template for the required ANTHROPIC_API_KEY (real key never committed)
├── .gitignore
├── chroma_db/           # Generated vector index (gitignored — rebuilt automatically)
├── feedback/
│   └── feedback.csv     # Thumbs up/down log (gitignored — user-generated data)
└── generated/
    └── faq.md           # Latest auto-generated FAQ output
```

## Running it locally

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Add your Anthropic API key
cp .env.example .env   # then paste your key into .env

python3 ingest.py       # builds the vector index (one-time, or after doc changes)
streamlit run app.py
```

## Status: MVP complete

Everything above is built, tested end-to-end (including against the live cloud deployment), and shipped:
ingestion → retrieval → confidence scoring → grounded answers → sources → conversation memory → feedback logging → auto-generated FAQ → cloud deployment → native embedding in the docs site.

**Future Updates:** multi-doc RAG (searching across more than one API's documentation with a source selector) — deferred until a second real documentation set exists to index against.

---

Built by Rinni Mahajan as part of the [Mkdocs Pet API Documentation Portal project](https://rinni27.github.io/technical-writing/pet-api-docs/).
