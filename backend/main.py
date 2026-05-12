
import os

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
# Welcome Banner
# =========================================

print("\n==========================================")
print("   AI Customer Support System")
print("==========================================")

print("\nHow can I help you today?\n")

print("Example Queries:\n")

print("1. Track my order ORD001")
print("2. Cancel order ORD002")
print("3. Payment issue with PAY1003")
print("4. Refund status for RET1002")
print("5. Recommend electronics products")
print("6. What is your refund policy?")

print("\nType 'exit' to quit.\n")

# =========================================
# Chat Loop
# =========================================

while True:

    # -------------------------------------
    # User Input
    # -------------------------------------

    user_query = input("User: ").strip()

    # -------------------------------------
    # Exit Condition
    # -------------------------------------

    if user_query.lower() == "exit":

        print("\nAI Support: Thank you for using our support system!")

        break

    # -------------------------------------
    # Empty Input Handling
    # -------------------------------------

    if not user_query:

        print("\nAI Support: Please enter your query.\n")

        continue

    # =====================================
    # SAVE USER MESSAGE TO HISTORY
    # =====================================

    add_to_history("user", user_query)

    # -------------------------------------
    # Invoke LangGraph App
    # -------------------------------------

    try:

        result = app.invoke({
            "user_query": user_query
        })

        ai_response = result["response"]

        # =================================
        # SAVE AI RESPONSE TO HISTORY
        # =================================

        add_to_history("assistant", ai_response)

        # ---------------------------------
        # Print AI Response
        # ---------------------------------

        print("\nAI Support:", ai_response)

        # =================================
        # OPTIONAL DEBUG MEMORY
        # =================================

        # print("\nCHAT HISTORY:")
        # print(get_history())

    # -------------------------------------
    # Error Handling
    # -------------------------------------

    except Exception as e:

        print("\nAI Support: Something went wrong.")

        print("Error:", str(e))

    print()