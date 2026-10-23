from functools import lru_cache
import httpx
from pinecone import Pinecone
import sys
import time
from app.config import settings

NAMESPACE = "__default__"

@lru_cache()
def clients():
    if not settings.pinecone_api_key:
        raise ValueError("Pinecone API key must be set in the environment variables.")
    return (
        Pinecone(api_key=settings.pinecone_api_key),
        httpx.Client(
            headers={
                "Api-Key": settings.pinecone_api_key,
                "X-Pinecone-Api-Version": "2026-07",
            },
            timeout=30.0,
        ),
    )


def ensure_index():
    pc, _ = clients()
    if not pc.has_index(settings.pinecone_index):
        raise ValueError(
            f"Pinecone document index '{settings.pinecone_index}' does not exist."
        )
    return pc.describe_index(settings.pinecone_index).host


def _documents_request(index_host, operation, payload):
    _, client = clients()
    url = f"https://{index_host}/namespaces/{NAMESPACE}/documents/{operation}"
    for attempt in range(6):
        response = client.post(url, json=payload)
        if response.status_code != 429:
            response.raise_for_status()
            return response.json()
        if attempt == 5:
            response.raise_for_status()

        retry_after = response.headers.get("Retry-After")
        try:
            delay = float(retry_after) if retry_after else min(2**attempt, 60)
        except ValueError:
            delay = min(2**attempt, 60)
        print(
            f"Pinecone rate limit reached; retrying in {delay:g}s "
            f"({attempt + 1}/5).",
            file=sys.stderr,
            flush=True,
        )
        time.sleep(delay)


def upsert_documents(index_host, documents):
    return _documents_request(index_host, "upsert", {"documents": documents})


def search_kb(query, top_k=5):
    index_host = ensure_index()
    result = _documents_request(
        index_host,
        "search",
        {
            "top_k": top_k,
            "score_by": [
                {"type": "embed", "fields": ["chunk_text"], "query": query}
            ],
            "include_fields": ["page", "text", "file"],
        },
    )
    matches = []
    for match in result["matches"]:
        fields = match.get("fields", match)
        matches.append(
            {
                "page": fields.get("page"),
                "text": fields.get("text", ""),
                "score": round(match.get("_score", match.get("score", 0)), 3),
                "source": fields.get("file", ""),
            }
        )
    return matches