# backend/agents/product_recommendation_agent.py

import os
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
# Product Database
# =========================================

PRODUCTS_DB = [

    {
        "name": "Wireless Headphones",
        "category": "electronics",
        "price": "$120",
        "description": (
            "Noise-cancelling wireless headphones "
            "with long battery life."
        ),
        "keywords": [
            "headphones",
            "music",
            "audio",
            "wireless",
            "electronics"
        ]
    },

    {
        "name": "Gaming Laptop",
        "category": "electronics",
        "price": "$1200",
        "description": (
            "High-performance laptop for gaming "
            "and heavy workloads."
        ),
        "keywords": [
            "gaming",
            "laptop",
            "computer",
            "electronics"
        ]
    },

    {
        "name": "Smart Watch",
        "category": "electronics",
        "price": "$250",
        "description": (
            "Fitness tracking smartwatch with "
            "heart-rate monitoring."
        ),
        "keywords": [
            "watch",
            "fitness",
            "smartwatch",
            "electronics"
        ]
    },

    {
        "name": "Running Shoes",
        "category": "fashion",
        "price": "$90",
        "description": (
            "Comfortable lightweight running shoes "
            "for daily workouts."
        ),
        "keywords": [
            "shoes",
            "sports",
            "fitness",
            "fashion"
        ]
    },

    {
        "name": "Leather Backpack",
        "category": "fashion",
        "price": "$75",
        "description": (
            "Premium leather backpack "
            "for office and travel."
        ),
        "keywords": [
            "bag",
            "travel",
            "office",
            "fashion"
        ]
    }
]

# =========================================
# Search Products
# =========================================

def search_products(user_query: str):

    user_query = user_query.lower()

    matched_products = []

    # -------------------------------------
    # Split user query into keywords
    # -------------------------------------

    query_words = user_query.split()

    # -------------------------------------
    # Match products
    # -------------------------------------

    for product in PRODUCTS_DB:

        searchable_text = " ".join([
            product["name"],
            product["category"],
            product["description"],
            " ".join(product["keywords"])
        ]).lower()

        # ---------------------------------
        # Match ANY query word
        # ---------------------------------

        if any(word in searchable_text for word in query_words):

            matched_products.append(product)

    return matched_products

# =========================================
# Product Recommendation Agent
# =========================================

def product_recommendation_agent(user_query: str):

    try:

        # ---------------------------------
        # Search Products
        # ---------------------------------

        products = search_products(user_query)

        # ---------------------------------
        # No Product Found
        # ---------------------------------

        if not products:

            return (
                "I could not find exact products for your request.\n\n"
                "Try categories like:\n"
                "- electronics\n"
                "- gaming\n"
                "- fashion\n"
                "- laptops\n"
                "- fitness"
            )

        # ---------------------------------
        # Create Product Context
        # ---------------------------------

        context = ""

        for index, product in enumerate(products, start=1):

            context += f"""
Product {index}

Name: {product['name']}
Category: {product['category']}
Price: {product['price']}
Description: {product['description']}

"""

        # ---------------------------------
        # Prompt
        # ---------------------------------

        prompt = f"""
You are an AI Product Recommendation Assistant.

Your tasks:
- Recommend products professionally
- Explain why each product is useful
- Mention pricing
- Keep response friendly and concise
- Use bullet points
- Use ONLY provided products

Customer Query:
{user_query}

Available Products:
{context}

Generate a helpful recommendation response.
"""

        # ---------------------------------
        # Generate Response
        # ---------------------------------

        response = llm.invoke(prompt)

        # ---------------------------------
        # Handle Response Types
        # ---------------------------------

        if hasattr(response, "content"):

            return response.content

        return str(response)

    except Exception as e:

        print("PRODUCT RECOMMENDATION ERROR:", e)

        return (
            "Sorry, product recommendation "
            "service is temporarily unavailable."
        )

# =========================================
# Testing
# =========================================

if __name__ == "__main__":

    queries = [
        "electronics",
        "gaming laptop",
        "fitness products",
        "smartwatch",
        "fashion"
    ]

    for query in queries:

        print("\n==============================")
        print("QUERY:", query)
        print("==============================")

        result = product_recommendation_agent(query)

        print(result)