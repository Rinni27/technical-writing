"""
Chunk the Pet API markdown docs and embed them into a persistent ChromaDB collection.

Run this whenever the docs content changes:
    python ingest.py
"""

import re
from pathlib import Path

import chromadb
from chromadb.utils import embedding_functions

DOCS_DIR = Path(__file__).parent.parent / "pet-api-mkdocs-source" / "docs"
CHROMA_DIR = Path(__file__).parent / "chroma_db"
COLLECTION_NAME = "pet_api_docs"

H2_SPLIT_RE = re.compile(r"^## (.+)$", re.MULTILINE)


def slugify(heading: str) -> str:
    slug = heading.lower().strip()
    slug = re.sub(r"[^a-z0-9\s-]", "", slug)
    slug = re.sub(r"\s+", "-", slug)
    return slug


def build_url(relative_path: Path, anchor: str | None) -> str:
    stem_parts = list(relative_path.with_suffix("").parts)
    if stem_parts[-1] == "index":
        stem_parts = stem_parts[:-1]
    url_path = "/".join(stem_parts)
    url = f"/{url_path}/" if url_path else "/"
    if anchor:
        url += f"#{anchor}"
    return url


def chunk_markdown_file(path: Path):
    text = path.read_text(encoding="utf-8")
    relative_path = path.relative_to(DOCS_DIR)

    lines = text.splitlines()
    title = lines[0].lstrip("# ").strip() if lines and lines[0].startswith("# ") else relative_path.stem
    body = "\n".join(lines[1:]) if lines and lines[0].startswith("# ") else text

    matches = list(H2_SPLIT_RE.finditer(body))

    chunks = []

    intro = body[: matches[0].start()].strip() if matches else body.strip()
    if intro:
        chunks.append(
            {
                "id": f"{relative_path}::intro",
                "text": f"# {title}\n\n{intro}",
                "title": title,
                "section": "Overview",
                "url": build_url(relative_path, None),
                "source_file": str(relative_path),
            }
        )

    for i, match in enumerate(matches):
        section_heading = match.group(1).strip()
        start = match.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(body)
        section_body = body[start:end].strip()
        anchor = slugify(section_heading)
        chunks.append(
            {
                "id": f"{relative_path}::{anchor}",
                "text": f"# {title}\n\n## {section_heading}\n\n{section_body}",
                "title": title,
                "section": section_heading,
                "url": build_url(relative_path, anchor),
                "source_file": str(relative_path),
            }
        )

    return chunks


def build_index():
    """Chunk all docs and (re)build the ChromaDB collection from scratch."""
    md_files = sorted(DOCS_DIR.rglob("*.md"))
    print(f"Found {len(md_files)} markdown files under {DOCS_DIR}")

    all_chunks = []
    for path in md_files:
        all_chunks.extend(chunk_markdown_file(path))

    print(f"Produced {len(all_chunks)} chunks")

    client = chromadb.PersistentClient(path=str(CHROMA_DIR))
    embedding_fn = embedding_functions.DefaultEmbeddingFunction()

    try:
        client.delete_collection(COLLECTION_NAME)
    except Exception:
        pass

    collection = client.create_collection(
        name=COLLECTION_NAME,
        embedding_function=embedding_fn,
        metadata={"hnsw:space": "cosine"},
    )

    collection.add(
        ids=[c["id"] for c in all_chunks],
        documents=[c["text"] for c in all_chunks],
        metadatas=[
            {
                "title": c["title"],
                "section": c["section"],
                "url": c["url"],
                "source_file": c["source_file"],
            }
            for c in all_chunks
        ],
    )

    print(f"Indexed {collection.count()} chunks into ChromaDB at {CHROMA_DIR}")
    return collection


if __name__ == "__main__":
    build_index()
