# backend/agents/cancel_order_agent.py

import os
import re

from dotenv import load_dotenv
from langchain_groq import ChatGroq

from state import (
    get_last_order_id,
    update_order_id,
    update_intent
)

# =========================================
# Load Environment Variables
# =========================================

load_dotenv()

# =========================================
# Initialize Groq LLM
# =========================================

llm = ChatGroq(
    groq_api_key=os.getenv("GROQ_API_KEY"),
    model_name="llama-3.3-70b-versatile"
)

# =========================================
# Dummy Orders Database
# Replace with real DB/API later
# =========================================

ORDERS_DB = {

    "ORD001": {
        "customer_name": "John Doe",
        "product": "Wireless Headphones",
        "status": "Shipped"
    },

    "ORD002": {
        "customer_name": "Alice Smith",
        "product": "Gaming Laptop",
        "status": "Processing"
    },

    "ORD003": {
        "customer_name": "Michael Brown",
        "product": "Smart Watch",
        "status": "Delivered"
    }
}

# =========================================
# Extract Order ID From Query
# =========================================

def extract_order_id(query: str):

    match = re.search(r'ORD\d+', query.upper())

    if match:
        return match.group()

    return None

# =========================================
# Fetch Order Details
# =========================================

def fetch_order(order_id: str):

    return ORDERS_DB.get(order_id.upper())

# =========================================
# Cancel Order Agent
# =========================================

def cancel_order_agent(query: str):

    # -------------------------------------
    # Extract Order ID From Query
    # -------------------------------------

    order_id = extract_order_id(query)

    # -------------------------------------
    # If No Order ID → Use Memory
    # -------------------------------------

    if not order_id:

        order_id = get_last_order_id()

        print("\nUSING MEMORY ORDER ID:", order_id)

    # -------------------------------------
    # Still No Order ID
    # -------------------------------------

    if not order_id:

        return "Please provide a valid Order ID."

    # =====================================
    # SAVE MEMORY
    # =====================================

    update_order_id(order_id)
    update_intent("cancel_order")

    # -------------------------------------
    # Fetch Order
    # -------------------------------------

    order = fetch_order(order_id)

    # -------------------------------------
    # Order Not Found
    # -------------------------------------

    if not order:

        return "Sorry, I could not find any order with this Order ID."

    # -------------------------------------
    # Extract Details
    # -------------------------------------

    customer_name = order["customer_name"]

    product = order["product"]

    status = order["status"]

    # -------------------------------------
    # Cancellation Rules
    # -------------------------------------

    if status == "Delivered":

        return (
            f"Order {order_id} for {product} "
            "has already been delivered and "
            "cannot be cancelled."
        )

    elif status == "Shipped":

        return (
            f"Order {order_id} for {product} "
            "has already been shipped. "
            "Cancellation may not be possible."
        )

    elif status == "Processing":

        # ---------------------------------
        # Create Context
        # ---------------------------------

        context = f"""
Order ID: {order_id}

Customer Name: {customer_name}
Product: {product}
Order Status: {status}
"""

        # ---------------------------------
        # Prompt
        # ---------------------------------

        prompt = f"""
You are an AI-powered Order Cancellation Support Agent.

Your responsibilities:
- Help customers cancel orders
- Explain cancellation status professionally
- Be concise and customer-friendly
- Use ONLY provided order information

Order Information:
{context}

Generate a professional cancellation response.
"""

        # ---------------------------------
        # Generate Response
        # ---------------------------------

        response = llm.invoke(prompt)

        return response.content

    # -------------------------------------
    # Fallback
    # -------------------------------------

    return "Unable to process cancellation request."


# =========================================
# Testing
# =========================================

if __name__ == "__main__":

    result = cancel_order_agent("cancel my order ORD002")

    print("\nAI RESPONSE:\n")

    print(result)