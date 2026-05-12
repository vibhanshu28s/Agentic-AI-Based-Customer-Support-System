# backend/agents/order_tracking_agent.py

import os
import re

from dotenv import load_dotenv
from langchain_groq import ChatGroq

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

    "ORD1001": {

        "customer_name": "John Doe",
        "product": "Wireless Headphones",
        "status": "Shipped",
        "location": "Delhi Warehouse",
        "estimated_delivery": "15 May 2026"
    },

    "ORD1002": {

        "customer_name": "Alice Smith",
        "product": "Gaming Laptop",
        "status": "Out for Delivery",
        "location": "Mumbai Delivery Hub",
        "estimated_delivery": "13 May 2026"
    },

    "ORD1003": {

        "customer_name": "Michael Brown",
        "product": "Running Shoes",
        "status": "Delivered",
        "location": "Customer Address",
        "estimated_delivery": "Completed"
    }
}

# =========================================
# Fetch Order
# =========================================

def fetch_order(order_id: str):

    return ORDERS_DB.get(order_id.upper())

# =========================================
# Extract Order ID
# =========================================

def extract_order_id(user_query: str):

    pattern = r"ORD\d+"

    match = re.search(
        pattern,
        user_query.upper()
    )

    if match:

        return match.group()

    return None

# =========================================
# Order Tracking Agent
# =========================================

def order_tracking_agent(user_query: str):

    query = user_query.lower()

    # =====================================
    # GENERAL TRACKING QUERIES
    # =====================================

    tracking_keywords = [

        "track order",
        "track my order",
        "where is my order",
        "order tracking",
        "delivery status",
        "shipment status",
        "package tracking"

    ]

    # =====================================
    # GENERAL TRACKING HELP
    # =====================================

    if any(keyword in query for keyword in tracking_keywords):

        order_id = extract_order_id(
            user_query
        )

        if not order_id:

            return """
I can help you track your order.

Please provide your Order ID.

Examples:
- ORD1001
- ORD1002
- ORD1003
"""

    # =====================================
    # Extract Order ID
    # =====================================

    order_id = extract_order_id(
        user_query
    )

    # =====================================
    # Missing Order ID
    # =====================================

    if not order_id:

        return """
Please provide a valid Order ID.

Examples:
- ORD1001
- ORD1002
- ORD1003
"""

    # =====================================
    # Fetch Order
    # =====================================

    order = fetch_order(order_id)

    # =====================================
    # Order Not Found
    # =====================================

    if not order:

        return f"""
Sorry, I could not find
any order with ID {order_id}.

Please verify your Order ID.
"""

    # =====================================
    # Create Context
    # =====================================

    context = f"""
Order ID: {order_id}

Customer Name: {order['customer_name']}
Product: {order['product']}
Current Status: {order['status']}
Current Location: {order['location']}
Estimated Delivery: {order['estimated_delivery']}
"""

    # =====================================
    # Prompt
    # =====================================

    prompt = f"""
You are an AI-powered Order Tracking Support Agent.

Your responsibilities:
- Help customers track orders
- Explain delivery status clearly
- Be professional and friendly
- Guide customers properly
- Use ONLY provided order information

Order Information:
{context}

Generate a helpful tracking response.
"""

    # =====================================
    # Generate Response
    # =====================================

    try:

        response = llm.invoke(prompt)

        if hasattr(response, "content"):

            return response.content

        return str(response)

    except Exception as e:

        print(
            "ORDER TRACKING ERROR:",
            e
        )

        return (
            "Sorry, order tracking "
            "service is temporarily unavailable."
        )

# =========================================
# Testing
# =========================================

if __name__ == "__main__":

    test_queries = [

        "track order",
        "where is my order",
        "ORD1001",
        "ORD1002",
        "delivery status"

    ]

    for query in test_queries:

        print("\n========================")
        print("QUERY:", query)
        print("========================")

        result = order_tracking_agent(query)

        print(result)