# AI-Powered Medical Chatbot

An educational medical question-and-answer chatbot built with **FastAPI, LangGraph, Groq, Pinecone, and Tavily**. It retrieves relevant passages from a medical PDF knowledge base and can use web search for current or time-sensitive information.

> **Important:** This project provides general information for educational purposes only. It is not a medical device and does not diagnose, treat, or replace advice from a licensed healthcare professional.

## 📋 Table of Contents

- [Introduction](#-introduction)
- [How It Works](#-how-it-works)
- [Tech Stack](#️-tech-stack)
- [Features](#-features)
- [Project Structure](#-project-structure)
- [Quick Start](#-quick-start)
- [API Usage](#-api-usage)
- [Screenshots](#️-screenshots)
- [Safety Notice](#️-safety-notice)
- [License](#-license)

## 🚀 Introduction

This repository contains a lightweight AI-powered medical chatbot with a web interface and REST API. Users can ask general health questions and receive conversational answers grounded in passages retrieved from a medical PDF. When a question calls for current information, the workflow can search the web and use the results as additional context.

The project also includes short-term conversation memory backed by SQLite and a document-ingestion script for indexing PDF content in Pinecone. It is intended as a learning and experimentation project—not for clinical decision-making.

## 🔄 How It Works

1. A user sends a question through the web interface or chat API.
2. A LangGraph workflow retrieves relevant content from the Pinecone medical knowledge base.
3. The workflow determines whether web evidence may be useful and, when needed, searches with Tavily.
4. Groq generates a response using the retrieved context and conversation state.
5. The application returns the answer and available source information.

## ⚙️ Tech Stack

- **Python** — application and ingestion scripts
- **FastAPI** — web server and REST API
- **LangGraph** — orchestration of retrieval and answer-generation steps
- **LangChain / Groq** — language-model integration
- **Pinecone** — vector search for medical document passages
- **Tavily** — web search for current information
- **SQLite** — short-term conversation checkpoints
- **HTML, CSS, and JavaScript** — chatbot interface

## ⚡ Features

- 💬 Conversational medical Q&A through a web interface
- 📚 Retrieval-augmented answers grounded in an indexed medical PDF
- 🌐 Tavily web-search fallback for current or time-sensitive questions
- 🧠 Short-term conversation state stored with SQLite checkpoints
- 🔌 FastAPI REST endpoints for health checks and chat
- 📄 PDF ingestion script for adding content to the Pinecone index
- ⚙️ Configurable CORS and optional API-token protection
- 🧾 Source metadata returned with answers when available

## 📁 Project Structure

```text
.
├── app/
│   ├── agent.py       # LangGraph workflow and answer generation
│   ├── config.py      # Environment configuration
│   ├── knowledge.py   # Pinecone retrieval and document access
│   └── main.py        # FastAPI application and API routes
├── data/
│   └── Medical_book.pdf
├── docs/
│   └── ai_powered_medical_chatbot_architecture.jpg
├── static/            # Static frontend assets
├── templates/
│   └── index.html     # Chat interface
├── ingest.py          # PDF ingestion and vector indexing
├── requirements.txt
├── test.py
├── test_api.py
└── README.md
```

## 🛠️ Quick Start

### Prerequisites

- Python 3.10 or newer
- pip
- API keys for Groq, Pinecone, and Tavily
- A Pinecone index you can access

### 1. Clone the repository

```bash
git clone https://github.com/Shafi7055/ai-powered-medical-chatbot.git
cd ai-powered-medical-chatbot
```

### 2. Create and activate a virtual environment

```bash
python -m venv .venv
```

Linux/macOS:

```bash
source .venv/bin/activate
```

Windows:

```powershell
.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root and add your credentials and settings:

```env
GROQ_API_KEY=your_groq_api_key
PINECONE_API_KEY=your_pinecone_api_key
TAVILY_API_KEY=your_tavily_api_key
PINECONE_INDEX=medical-chat-bot
API_TOKEN=
ALLOWED_ORIGINS=http://localhost:8000,http://127.0.0.1:8000
```

Keep API keys private. Do not commit your `.env` file.

### 5. Index the medical PDF

Make sure your Pinecone index is ready, then run:

```bash
python ingest.py --pdf data/Medical_book.pdf
```

### 6. Start the application

```bash
uvicorn app.main:app --reload
```

Open [http://localhost:8000/](http://localhost:8000/) in your browser.

## 🔌 API Usage

### Health check

```bash
curl http://127.0.0.1:8000/api/health
```

### Send a chat message

```bash
curl -X POST "http://127.0.0.1:8000/api/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What are common causes of headaches?",
    "history": [],
    "image_data": null
  }'
```

A response includes an answer and may include source metadata, for example:

```json
{
  "answer": "Headaches can have many causes. If your symptoms are severe, unusual, or persistent, seek advice from a healthcare professional.",
  "sources": [
    {"type": "pdf", "page": 12}
  ]
}
```

## 🖼️ Screenshots

The repository includes an architecture diagram at [`docs/ai_powered_medical_chatbot_architecture.jpg`](docs/ai_powered_medical_chatbot_architecture.jpg). Add screenshots of the chat interface here as the UI evolves.

## ⚠️ Safety Notice

This chatbot is for informational and educational use only.

- It does not provide a diagnosis, treatment plan, or prescription.
- It cannot replace a clinician's judgment or a consultation with a qualified healthcare professional.
- Do not use it to make decisions in an emergency.
- If you may be experiencing a medical emergency—including chest pain, difficulty breathing, severe bleeding, stroke symptoms, or suicidal intent—contact your local emergency services immediately.

## 📝 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
