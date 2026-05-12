# Agentic AI Based Customer Support System

An intelligent multi-agent AI customer support system built using **FastAPI**, **LangGraph**, **LLMs**, and **React**.
This project simulates an autonomous AI support team for an eCommerce or SaaS platform instead of a basic chatbot.

---

# Features

* Multi-Agent Architecture
* AI-Powered Customer Support
* LangGraph Workflow Orchestration
* Product Recommendation Agent
* Payment Support Agent
* Order Cancellation Agent
* FAQ Retrieval Agent (RAG)
* ChromaDB Vector Database
* Async FastAPI Backend
* React Frontend UI
* Real-time API Communication
* Scalable & Modular Design

---

# Tech Stack

## Backend

* Python
* FastAPI
* LangGraph
* LangChain
*  Groq LLM
* ChromaDB
* Sentence Transformers

## Frontend

* React.js
* Axios
* Tailwind CSS

---

# Project Architecture

```bash id="0p6gpf"
Agentic-AI-Customer-Support/
│
├── backend/
│   ├── agents/
│   │   ├── faq_agent.py
│   │   ├── payment_agent.py
│   │   ├── recommendation_agent.py
│   │   └── order_agent.py
│   │
│   ├── rag/
│   │   ├── retriever.py
│   │   ├── ingest.py
│   │   └── chroma_db/
│   │
│   ├── graph/
│   │   └── support_graph.py
│   │
│   ├── main.py
│   ├── requirements.txt
│   └── .env
│
├── frontend/
│   ├── src/
│   ├── public/
│   └── package.json
│
└── README.md
```

---

# System Workflow

1. User sends a query.
2. LangGraph detects user intent.
3. Query is routed to the correct AI agent.
4. FAQ agent retrieves knowledge from ChromaDB.
5. Selected AI agent processes the request.
6. AI generates autonomous support response.
7. Response is returned to frontend UI.

---

# Supported Queries

## FAQ Queries

```text id="m5x7gt"
What is your refund policy?
How long is shipping?
```

## Payment Support

```text id="m0gv2n"
Payment failed for my order
Refund not received
```

## Product Recommendation

```text id="8i9d4m"
Suggest gaming laptops under ₹80,000
Best wireless headphones
```

## Order Management

```text id="k5m86v"
Cancel order ORD12345
Track my order
```

---

# Installation

## 1. Clone Repository

```bash id="t3jvfr"
git clone https://github.com/your-username/agentic-ai-customer-support.git

cd agentic-ai-customer-support
```

---

# Backend Setup

## 2. Create Virtual Environment

### Mac/Linux

```bash id="wbr0pc"
python3 -m venv .venv

source .venv/bin/activate
```

### Windows

```bash id="owm7vz"
python -m venv .venv

.venv\Scripts\activate
```

---

## 3. Install Dependencies

```bash id="mkh9rb"
pip install -r requirements.txt
```

---

## 4. Create `.env`

```env id="7f5t12"
GROQ_API_KEY=your_groq_key
```

---

## 5. Run ChromaDB Ingestion

```bash id="x7ybht"
python rag/ingest.py
```

This script:

* Loads FAQ/support documents
* Creates embeddings
* Stores vectors in ChromaDB

---

## 6. Run Backend

```bash id="6eq7ce"
uvicorn main:app --reload
```

Backend will run on:

```bash id="mbc10c"
http://127.0.0.1:8000
```

---

# Frontend Setup

## 7. Install Frontend Dependencies

```bash id="jlwmxh"
cd frontend

npm install
```

---

## 8. Run Frontend

```bash id="pxn2a7"
npm run dev
```

Frontend will run on:

```bash id="jfej1z"
http://localhost:5173
```

---

# API Endpoint

## POST `/chat`

### Request

```json id="e4v2se"
{
  "message": "Cancel order ORD123"
}
```

### Response

```json id="5qzcq1"
{
  "agent": "order_agent",
  "response": "Your order ORD123 has been cancelled successfully."
}
```

---

# ChromaDB Integration

The system uses **ChromaDB** for Retrieval-Augmented Generation (RAG).

## Benefits

* Fast semantic search
* Persistent vector storage
* Efficient FAQ retrieval
* Context-aware AI responses

## Workflow

```text id="x1u5g9"
User Query
    ↓
Embedding Generation
    ↓
ChromaDB Similarity Search
    ↓
Relevant Context Retrieved
    ↓
LLM Generates Response
```

---

# LangGraph Flow

```text id="j30tbq"
                User Query
                     |
                     v
              Intent Detection
                     |
     --------------------------------
     |              |              |
     v              v              v
 FAQ Agent   Payment Agent   Order Agent
     |
     v
 ChromaDB Retrieval
     |
     v
Recommendation Agent
     |
     v
 Final AI Response
```

---

# Example UI

## Landing Screen

```text id="3pm4k3"
How can I help you today?
```

## Example Prompts

```text id="sngnvs"
Cancel order ORD1001
Recommend smartphones under ₹30,000
Payment failed during checkout
What is your return policy?
```

---

# Future Improvements

* Memory-enabled conversations
* Voice support
* Multi-language support
* Ticket escalation system
* Database integration
* Real-time order tracking
* Authentication & User Accounts
* Deployment on AWS/GCP

---

# Deployment

## Backend Deployment

* Render
* Railway
* AWS Lambda
* GCP Cloud Functions

## Frontend Deployment

* Vercel
* Netlify

---

# Why This Project is Agentic AI?

This system is not a simple chatbot because:

* Multiple specialized AI agents exist
* AI autonomously routes tasks
* LangGraph manages workflows
* ChromaDB enables intelligent retrieval
* Agents independently process queries
* Retrieval-Augmented Generation (RAG)
* Autonomous decision-making pipeline

---

# Requirements.txt Example

```txt id="rm0l0m"
fastapi
uvicorn
langchain
langgraph
openai
groq
chromadb
sentence-transformers
python-dotenv
pydantic
httpx
```

---

# Author

**Vibhanshu K. Singh**

Data Science & AI Developer

---

# License

MIT License