# backend/agents/refund_return_agent.py

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
# Dummy Refund / Return Database
# Replace with real DB/API later
# =========================================

RETURNS_DB = {

    "RET1001": {

        "customer_name": "John Doe",
        "product": "Wireless Headphones",
        "refund_status": "Approved",
        "refund_amount": "$120",
        "return_status": "Pickup Scheduled",
        "estimated_refund_date": "15 May 2026"
    },

    "RET1002": {

        "customer_name": "Alice Smith",
        "product": "Gaming Laptop",
        "refund_status": "Pending",
        "refund_amount": "$1200",
        "return_status": "Under Review",
        "estimated_refund_date": "18 May 2026"
    },

    "RET1003": {

        "customer_name": "Michael Brown",
        "product": "Running Shoes",
        "refund_status": "Completed",
        "refund_amount": "$90",
        "return_status": "Returned",
        "estimated_refund_date": "Completed"
    }
}

# =========================================
# Fetch Return Request
# =========================================

def fetch_return_request(return_id: str):

    return RETURNS_DB.get(return_id.upper())

# =========================================
# Extract Return ID
# =========================================

def extract_return_id(user_query: str):

    pattern = r"RET\d+"

    match = re.search(
        pattern,
        user_query.upper()
    )

    if match:

        return match.group()

    return None

# =========================================
# Refund / Return Agent
# =========================================

def refund_return_agent(user_query: str):

    query = user_query.lower()

    # =====================================
    # GENERAL RETURN / REFUND QUERIES
    # =====================================

    general_keywords = [

        "return",
        "refund",
        "replace",
        "exchange",
        "cancel return",
        "refund status",
        "return status",
        "product damaged",
        "wrong item",
        "return order"

    ]

    # =====================================
    # GENERAL SUPPORT
    # =====================================

    if any(keyword in query for keyword in general_keywords):

        return """
To check an existing return/refund,
please provide your Return ID.

Examples:
- RET1001
- RET1002
"""

    # =====================================
    # Extract Return ID
    # =====================================

    return_id = extract_return_id(
        user_query
    )

    # =====================================
    # Missing Return ID
    # =====================================

    if not return_id:

        return """
Please provide a valid Return ID.

Examples:
- RET1001
- RET1002
- RET1003
"""

    # =====================================
    # Fetch Return Request
    # =====================================

    return_request = fetch_return_request(
        return_id
    )

    # =====================================
    # Return Request Not Found
    # =====================================

    if not return_request:

        return f"""
Sorry, I could not find
any return request with ID {return_id}.

Please verify your Return ID.
"""

    # =====================================
    # Create Context
    # =====================================

    context = f"""
Return ID: {return_id}

Customer Name: {return_request['customer_name']}
Product: {return_request['product']}
Refund Status: {return_request['refund_status']}
Refund Amount: {return_request['refund_amount']}
Return Status: {return_request['return_status']}
Estimated Refund Date: {return_request['estimated_refund_date']}
"""

    # =====================================
    # Prompt
    # =====================================

    prompt = f"""
You are an AI-powered Refund and Return Support Agent.

Your responsibilities:
- Help customers with return requests
- Explain refund and return status
- Be professional and friendly
- Guide customers properly
- Use ONLY provided information

Return Information:
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

        print(
            "REFUND RETURN ERROR:",
            e
        )

        return (
            "Sorry, refund and return "
            "service is temporarily unavailable."
        )

# =========================================
# Testing
# =========================================

if __name__ == "__main__":

    test_queries = [

        "i want refund",
        "return order",
        "wrong item delivered",
        "RET1001",
        "refund status",
        "damaged product"

    ]

    for query in test_queries:

        print("\n========================")
        print("QUERY:", query)
        print("========================")

        result = refund_return_agent(query)

        print(result)