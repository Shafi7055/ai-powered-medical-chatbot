# AI-Powered Medical Chatbot

A medical Q&A assistant built with FastAPI, LangGraph, Groq, Pinecone, and Tavily. The app allows users to ask medical questions and receive conversational answers grounded in a medical knowledge base and optional live web results.

## Overview

This project provides a lightweight medical chatbot interface for:

- answering general health and medical information questions
- retrieving relevant passages from a local medical PDF knowledge base
- using web search as a fallback for current or time-sensitive guidance
- maintaining short-term conversation memory with SQLite checkpoints
- exposing a REST API for integration with other frontends or services

The application is designed as an educational and triage-support tool, not a replacement for a licensed clinician.

## Features

- FastAPI backend and web UI
- LangGraph workflow for retrieval, routing, and answer generation
- Groq LLM integration for answer synthesis
- Pinecone vector database for document retrieval
- Tavily-powered web search fallback
- SQLite-backed memory for conversation state
- configurable CORS and optional API token protection
- simple ingestion pipeline for PDF medical content

## Project Structure

```text
.
├── app/
│   ├── __init__.py
│   ├── agent.py          # LangGraph orchestration and answer generation
│   ├── config.py         # Environment configuration and settings
│   ├── knowledge.py      # Pinecone document access and retrieval layer
│   └── main.py           # FastAPI app and API routes
├── data/
│   └── Medical_book.pdf  # Medical PDF used for knowledge ingestion
├── docs/
│   └── ai_powered_medical_chatbot_architecture.jpg
├── static/
├── templates/
│   └── index.html        # Frontend interface
├── .gitignore
├── .vscode/
├── ingest.py             # PDF ingestion script for vector indexing
├── LICENSE
├── medical_memory.db     # SQLite memory database
├── requirements.txt
├── run_ingest.py
├── test.py
├── test_api.py
├── README.md
└── .env.example          # if present in your environment, add your secrets here
```

## Tech Stack

- Python
- FastAPI
- LangGraph
- LangChain / Groq
- Pinecone
- Tavily
- SQLite
- HTML/CSS/JavaScript frontend

## Prerequisites

Before running the app, make sure you have:

- Python 3.10+ recommended
- pip and virtual environment support
- API keys for:
  - Groq
  - Pinecone
  - Tavily

## Setup

1. Clone the repository:

```bash
git clone https://github.com/Shafi7055/ai-powered-medical-chatbot.git
cd ai-powered-medical-chatbot
```

2. Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate   # Linux/macOS
# or
.venv\Scripts\activate     # Windows
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the project root with the required variables:

```env
GROQ_API_KEY=your_groq_api_key
PINECONE_API_KEY=your_pinecone_api_key
TAVILY_API_KEY=your_tavily_api_key
PINECONE_INDEX=medical-chat-bot
API_TOKEN=
ALLOWED_ORIGINS=http://localhost:8000,http://127.0.0.1:8000
```

5. Ensure your Pinecone index exists and is accessible.

6. Ingest the medical PDF into the vector database:

```bash
python ingest.py --pdf data/Medical_book.pdf
```

## Run the Application

Start the backend server:

```bash
uvicorn app.main:app --reload
```

Open the browser at:

```text
http://localhost:8000/
```

## API Usage

### Health Check

```bash
curl http://127.0.0.1:8000/api/health
```

### Chat Endpoint

```bash
curl -X POST "http://127.0.0.1:8000/api/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What are common causes of headaches?",
    "history": [],
    "image_data": null
  }'
```

Example response:

```json
{
  "answer": "Headaches can be caused by stress, dehydration, poor sleep, migraine triggers, or tension. If symptoms are severe or unusual, please seek medical advice.",
  "sources": [
    {"type": "pdf", "page": 12}
  ]
}
```

## How It Works

The app uses a LangGraph state machine to:

1. retrieve relevant passages from the Pinecone knowledge base
2. decide whether the question needs web-based evidence
3. query Tavily for current information if needed
4. generate a final answer with GroqLLM using the retrieved context and conversation memory

## Important Safety Notice

This project is intended for informational and educational use only.

- It is not a substitute for professional medical judgment.
- It is not designed to diagnose, treat, or prescribe care.
- Users with severe symptoms should contact emergency services or seek urgent medical help immediately.
- For emergency situations such as chest pain, difficulty breathing, severe bleeding, stroke symptoms, or suicidal intent, contact local emergency services without delay.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Contributing

Contributions are welcome. If you would like to improve the chatbot, add safeguards, improve medical prompts, or refine the frontend, please open a pull request with a clear description of the change.

## Project Status

This repository is a functional prototype for an AI-assisted medical chatbot and is suitable for experimentation, learning, and extension into a production-grade clinical support application with stronger validation and safety controls.
