"""
Scan the Pet API docs and have Claude generate a grounded FAQ page.

Run with:
    python generate_faq.py

Writes the result to generated/faq.md — review it before manually copying
any of it into pet-api-mkdocs-source/docs/. This script never touches the
docs source itself.
"""

import os
from pathlib import Path

from anthropic import Anthropic
from dotenv import load_dotenv

from ingest import DOCS_DIR

load_dotenv()

OUTPUT_DIR = Path(__file__).parent / "generated"
OUTPUT_FILE = OUTPUT_DIR / "faq.md"
CLAUDE_MODEL = os.environ.get("CLAUDE_MODEL", "claude-sonnet-5")

SYSTEM_PROMPT = """You are a technical documentation editor. You will be given the full \
contents of an API documentation site. Generate a Frequently Asked Questions (FAQ) page \
for developers integrating with this API.

Rules:
- Ground every question and answer strictly in the provided documentation. Never invent \
endpoints, fields, status codes, or behavior that isn't present in the source content.
- Cover the questions a developer would actually ask while integrating: authentication, \
request/response formats, common error/status codes, and the most-used endpoints.
- Organize the FAQ into topic sections with H2 headings (## Getting Started, ## Endpoints, \
## Errors & Status Codes, etc.), matching MkDocs Material markdown conventions.
- Each question should be a bolded line or H3 heading, followed by a concise answer (2-4 \
sentences, using inline code formatting for endpoints/fields/status codes).
- Produce 10-15 Q&A pairs total. Prefer breadth over depth.
- Do not include markdown links to other doc pages (e.g. "[Overview](getting-started/overview.md)"). \
Those relative paths won't resolve outside the MkDocs site. Reference other pages by name in plain \
text instead, with no link syntax.
- Output ONLY the markdown for the FAQ page, starting with "# Frequently Asked Questions". \
No preamble or explanation outside the markdown.
"""


def load_all_docs() -> str:
    parts = []
    for path in sorted(DOCS_DIR.rglob("*.md")):
        relative_path = path.relative_to(DOCS_DIR)
        parts.append(f"--- {relative_path} ---\n{path.read_text(encoding='utf-8')}")
    return "\n\n".join(parts)


def generate_faq() -> str:
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise RuntimeError("ANTHROPIC_API_KEY is not set. Add it to pet-api-rag-assistant/.env")

    client = Anthropic(api_key=api_key)
    docs_content = load_all_docs()

    response = client.messages.create(
        model=CLAUDE_MODEL,
        max_tokens=4096,
        system=SYSTEM_PROMPT,
        messages=[
            {
                "role": "user",
                "content": f"Documentation source files:\n\n{docs_content}",
            }
        ],
    )

    return "".join(block.text for block in response.content if block.type == "text")


def main():
    faq_markdown = generate_faq()

    OUTPUT_DIR.mkdir(exist_ok=True)
    OUTPUT_FILE.write_text(faq_markdown, encoding="utf-8")

    print(f"FAQ generated: {OUTPUT_FILE}")
    print()
    print(faq_markdown)


if __name__ == "__main__":
    main()
