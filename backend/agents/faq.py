import os

from dotenv import load_dotenv
from langchain_groq import ChatGroq

from rag.retriever import search_docs

# =========================================
# Load Environment Variables
# =========================================

load_dotenv()

# =========================================
# Initialize LLM
# =========================================

llm = ChatGroq(
    groq_api_key=os.getenv("GROQ_API_KEY"),
    model_name="llama-3.3-70b-versatile"
)

# =========================================
# FAQ Agent
# =========================================

def faq_agent(query: str):

    # -------------------------------------
    # Retrieve relevant documents
    # -------------------------------------

    docs = search_docs(query)

    # -------------------------------------
    # Combine retrieved document chunks
    # -------------------------------------

    context = "\n".join([
        doc.page_content for doc in docs
    ])

    # -------------------------------------
    # Create prompt
    # -------------------------------------

    prompt = f"""
You are a professional AI FAQ support agent.

Your responsibilities:
- Answer customer questions
- Use ONLY the provided context
- Be concise and professional
- If answer is not available in context, say:
  "I could not find that information."

Context:
{context}

User Question:
{query}
"""

    # -------------------------------------
    # Generate response
    # -------------------------------------

    response = llm.invoke(prompt)

    # -------------------------------------
    # Return final answer
    # -------------------------------------

    return response.content