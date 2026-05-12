import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from state import (
    add_to_history,
    get_history
)

# =========================================
# Disable Tokenizers Parallelism Warning
# =========================================

os.environ["TOKENIZERS_PARALLELISM"] = "false"

# =========================================
# Import LangGraph App
# =========================================

from graph import app

# =========================================
# Initialize FastAPI
# =========================================

api = FastAPI(
    title="Agentic AI Customer Support System"
)

# =========================================
# Enable CORS
# =========================================

api.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change later for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================================
# Request Schema
# =========================================

class ChatRequest(BaseModel):

    message: str

# =========================================
# Root Endpoint
# =========================================

@api.get("/")
async def home():

    return {
        "message": "Agentic AI Customer Support System Running"
    }

# =========================================
# Chat Endpoint
# =========================================

@api.post("/chat")
async def chat(request: ChatRequest):

    user_query = request.message.strip()

    # -------------------------------------
    # Empty Input Handling
    # -------------------------------------

    if not user_query:

        return {
            "response": "Please enter your query."
        }

    # =====================================
    # SAVE USER MESSAGE TO HISTORY
    # =====================================

    add_to_history("user", user_query)

    try:

        # =================================
        # Async LangGraph Invocation
        # =================================

        result = await app.ainvoke({
            "user_query": user_query
        })

        ai_response = result["response"]

        # =================================
        # SAVE AI RESPONSE TO HISTORY
        # =================================

        add_to_history("assistant", ai_response)

        # =================================
        # Return Response
        # =================================

        return {
            "response": ai_response,
            "history": get_history()
        }

    except Exception as e:

        return {
            "response": "Something went wrong.",
            "error": str(e)
        }

# =========================================
# Chat History Endpoint
# =========================================

@api.get("/history")
async def history():

    return {
        "history": get_history()
    }