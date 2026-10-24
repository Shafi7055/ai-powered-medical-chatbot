import logging
import secrets
import uuid
from pathlib import Path
from typing import Literal

from fastapi import FastAPI, Header, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from app.agent import graph
from app.config import settings


logger = logging.getLogger(__name__)
BASE_DIR = Path(__file__).resolve().parent.parent

app = FastAPI(title="MedGuide AI")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        *(
            origin.strip()
            for origin in settings.allowed_origins.split(",")
            if origin.strip()
        ),
        "http://localhost:5500",
        "http://127.0.0.1:5500",
    ],
    allow_methods=["*"],
    allow_headers=["*"],
)
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")


class HistoryMessage(BaseModel):
    role: Literal["user", "assistant"]
    content: str


class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=4000)
    history: list[HistoryMessage] = Field(default_factory=list)
    image_data: str | None = None


@app.get("/")
def index():
    return FileResponse(BASE_DIR / "templates" / "index.html")


@app.get("/api/health")
def health():
    return {
        "configured": bool(settings.groq_api_key and settings.pinecone_api_key),
    }


@app.post("/api/chat")
def chat(
    payload: ChatRequest,
    authorization: str | None = Header(default=None),
):
    # Enforce API token only when a token is configured.
    # Allows running locally without a token.
    if settings.api_token:
        if not secrets.compare_digest(
            authorization or "",
            f"Bearer {settings.api_token}",
        ):
            raise HTTPException(status_code=401, detail="Invalid or missing API token.")

    if not settings.groq_api_key or not settings.pinecone_api_key:
        raise HTTPException(
            status_code=503,
            detail="Chat is not configured. Set the Groq and Pinecone API keys.",
        )

    try:
        result = graph.invoke(
            {
                "question": payload.message,
                "history": [message.model_dump() for message in payload.history],
                "image_description": "",
                "kb": [],
                "web": [],
                "answer": "",
                "route": "",
            },
            config={"configurable": {"thread_id": str(uuid.uuid4())}},
        )
    except Exception:
        logger.exception("Chat request failed")
        raise HTTPException(
            status_code=500,
            detail="The chat request failed. Check the server logs for details.",
        ) from None

    sources = [
        {"type": "pdf", "page": item["page"]}
        for item in result.get("kb", [])
        if item.get("page") is not None
    ]
    sources.extend(
        {"type": "web", "url": item["url"]}
        for item in result.get("web", [])
        if item.get("url")
    )
    from fastapi.responses import JSONResponse
    return JSONResponse(content={"answer": result.get("answer", ""), "sources": sources})

@app.options("/api/chat")
def chat_options():
    """CORS preflight response for /api/chat.
    Returns an empty JSON body with status 200.
    """
    from fastapi.responses import JSONResponse
    return JSONResponse(content={})