# state.py

conversation_state = {
    "last_order_id": None,
    "last_payment_id": None,
    "last_return_id": None,
    "last_intent": None,
    "last_user_query": None,
    "history": []
}


# =========================================
# UPDATE FUNCTIONS
# =========================================

def update_order_id(order_id):
    conversation_state["last_order_id"] = order_id


def update_payment_id(payment_id):
    conversation_state["last_payment_id"] = payment_id


def update_return_id(return_id):
    conversation_state["last_return_id"] = return_id


def update_intent(intent):
    conversation_state["last_intent"] = intent


def update_user_query(query):
    conversation_state["last_user_query"] = query


def add_to_history(role, message):
    conversation_state["history"].append({
        "role": role,
        "message": message
    })


# =========================================
# GET FUNCTIONS
# =========================================

def get_last_order_id():
    return conversation_state.get("last_order_id")


def get_last_payment_id():
    return conversation_state.get("last_payment_id")


def get_last_return_id():
    return conversation_state.get("last_return_id")


def get_last_intent():
    return conversation_state.get("last_intent")


def get_last_user_query():
    return conversation_state.get("last_user_query")


def get_history():
    return conversation_state.get("history")


# =========================================
# RESET MEMORY
# =========================================

def reset_state():
    conversation_state["last_order_id"] = None
    conversation_state["last_payment_id"] = None
    conversation_state["last_return_id"] = None
    conversation_state["last_intent"] = None
    conversation_state["last_user_query"] = None
    conversation_state["history"] = []