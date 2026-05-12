# backend/agents/payment_support_agent.py

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
# Dummy Payment Database
# Replace with real DB/API later
# =========================================

PAYMENTS_DB = {

    "PAY1001": {
        "customer_name": "John Doe",
        "amount": "$120",
        "status": "Successful",
        "payment_method": "Credit Card",
        "transaction_date": "11 May 2026"
    },

    "PAY1002": {
        "customer_name": "Alice Smith",
        "amount": "$450",
        "status": "Pending",
        "payment_method": "UPI",
        "transaction_date": "12 May 2026"
    },

    "PAY1003": {
        "customer_name": "Michael Brown",
        "amount": "$89",
        "status": "Failed",
        "payment_method": "Debit Card",
        "transaction_date": "12 May 2026"
    }
}

# =========================================
# Fetch Payment Details
# =========================================

def fetch_payment(payment_id: str):

    return PAYMENTS_DB.get(payment_id.upper())

# =========================================
# Extract Payment ID From Query
# =========================================

def extract_payment_id(user_query: str):

    pattern = r"PAY\d+"

    match = re.search(
        pattern,
        user_query.upper()
    )

    if match:
        return match.group()

    return None

# =========================================
# Payment Support Agent
# =========================================

def payment_support_agent(user_query: str):

    query = user_query.lower()

    # =====================================
    # GENERAL PAYMENT SUPPORT
    # =====================================

    general_keywords = [

        "payment",
        "billing",
        "invoice",
        "transaction",
        "refund",
        "upi",
        "credit card",
        "debit card",
        "paypal",
        "payment issue",
        "payment statement",
        "payment methods",
        "payment status"

    ]

    # =====================================
    # Detect Generic Payment Questions
    # =====================================

    if (
        any(keyword in query for keyword in general_keywords)
        and "pay" not in query.upper()
    ):

        return """

To check a specific payment,
please provide your Payment ID.

Example:
- PAY1001
- PAY1002
"""

    # =====================================
    # Extract Payment ID
    # =====================================

    payment_id = extract_payment_id(user_query)

    # =====================================
    # Missing Payment ID
    # =====================================

    if not payment_id:

        return """
Please provide a valid Payment ID.

Example:
- PAY1001
- PAY1002
- PAY1003
"""

    # =====================================
    # Fetch Payment
    # =====================================

    payment = fetch_payment(payment_id)

    # =====================================
    # Payment Not Found
    # =====================================

    if not payment:

        return (
            f"Sorry, I could not find any "
            f"payment with ID {payment_id}."
        )

    # =====================================
    # Create Context
    # =====================================

    context = f"""
Payment ID: {payment_id}

Customer Name: {payment['customer_name']}
Amount: {payment['amount']}
Payment Status: {payment['status']}
Payment Method: {payment['payment_method']}
Transaction Date: {payment['transaction_date']}
"""

    # =====================================
    # Prompt
    # =====================================

    prompt = f"""
You are an AI-powered Payment Support Agent.

Your responsibilities:
- Help customers understand payment details
- Explain payment status clearly
- Be professional and friendly
- Help resolve payment confusion
- Use ONLY provided information

Payment Information:
{context}

Generate a helpful support response.
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

        print("PAYMENT SUPPORT ERROR:", e)

        return (
            "Sorry, payment support service "
            "is temporarily unavailable."
        )

# =========================================
# Testing
# =========================================

if __name__ == "__main__":

    queries = [

        "payment statement",
        "billing issue",
        "PAY1001",
        "PAY1002",
        "refund payment",
        "transaction failed"

    ]

    for query in queries:

        print("\n============================")
        print("QUERY:", query)
        print("============================")

        result = payment_support_agent(query)

        print(result)