# backend/graph.py

from typing import TypedDict

from langgraph.graph import StateGraph, END

# =========================================
# Import Agents
# =========================================

from agents.faq import faq_agent
from agents.cancel_order_agent import cancel_order_agent
from agents.order_tracking_agent import order_tracking_agent
from agents.payment_support_agent import payment_support_agent
from agents.product_recommendation_agent import (
    product_recommendation_agent
)
from agents.refund_return_agent import (
    refund_return_agent
)

# =========================================
# Conversation Memory
# =========================================

LAST_AGENT = {
    "name": None
}

# =========================================
# State
# =========================================

class AgentState(TypedDict):

    user_query: str
    response: str

# =========================================
# Router
# =========================================

def router(state: AgentState):

    query = state["user_query"].lower()

    # =====================================
    # CONTEXT CONTINUATION
    # =====================================

    # If user only sends IDs,
    # continue previous agent

    if (
        query.startswith("ord")
        or query.startswith("pay")
        or query.startswith("ret")
    ):

        if LAST_AGENT["name"]:

            print(
                "USING MEMORY ROUTE:",
                LAST_AGENT["name"]
            )

            return LAST_AGENT["name"]

    # =====================================
    # CANCEL ORDER
    # =====================================

    if any(word in query for word in [

        "cancel",
        "cancel order",
        "stop order"

    ]):

        LAST_AGENT["name"] = "cancel_order"

        print("ROUTER DECISION: cancel_order")

        return "cancel_order"

    # =====================================
    # ORDER TRACKING
    # =====================================

    elif any(word in query for word in [

        "track",
        "tracking",
        "where is my order",
        "delivery status"

    ]):

        LAST_AGENT["name"] = "order_tracking"

        print("ROUTER DECISION: order_tracking")

        return "order_tracking"

    # =====================================
    # PAYMENT SUPPORT
    # =====================================

    elif any(word in query for word in [

        "payment",
        "billing",
        "invoice",
        "transaction",
        "pay"

    ]):

        LAST_AGENT["name"] = "payment_support"

        print("ROUTER DECISION: payment_support")

        return "payment_support"

    # =====================================
    # PRODUCT RECOMMENDATION
    # =====================================

    elif any(word in query for word in [

        "recommend",
        "suggest",
        "product",
        "electronics",
        "laptop",
        "gaming",
        "fashion"

    ]):

        LAST_AGENT["name"] = "product_recommendation"

        print(
            "ROUTER DECISION: "
            "product_recommendation"
        )

        return "product_recommendation"

    # =====================================
    # REFUND / RETURN
    # =====================================

    elif any(word in query for word in [

        "refund",
        "return",
        "replace",
        "exchange"

    ]):

        LAST_AGENT["name"] = "refund_return"

        print("ROUTER DECISION: refund_return")

        return "refund_return"

    # =====================================
    # DEFAULT FAQ
    # =====================================

    LAST_AGENT["name"] = "faq"

    print("ROUTER DECISION: faq")

    return "faq"

# =========================================
# FAQ NODE
# =========================================

def faq_node(state: AgentState):

    response = faq_agent(
        state["user_query"]
    )

    return {
        "response": response
    }

# =========================================
# CANCEL ORDER NODE
# =========================================

def cancel_order_node(state: AgentState):

    response = cancel_order_agent(
        state["user_query"]
    )

    return {
        "response": response
    }

# =========================================
# ORDER TRACKING NODE
# =========================================

def order_tracking_node(state: AgentState):

    response = order_tracking_agent(
        state["user_query"]
    )

    return {
        "response": response
    }

# =========================================
# PAYMENT SUPPORT NODE
# =========================================

def payment_support_node(state: AgentState):

    response = payment_support_agent(
        state["user_query"]
    )

    return {
        "response": response
    }

# =========================================
# PRODUCT RECOMMENDATION NODE
# =========================================

def product_recommendation_node(
    state: AgentState
):

    response = product_recommendation_agent(
        state["user_query"]
    )

    return {
        "response": response
    }

# =========================================
# REFUND RETURN NODE
# =========================================

def refund_return_node(state: AgentState):

    response = refund_return_agent(
        state["user_query"]
    )

    return {
        "response": response
    }

# =========================================
# Build Graph
# =========================================

workflow = StateGraph(AgentState)

# =========================================
# Add Nodes
# =========================================

workflow.add_node("faq", faq_node)

workflow.add_node(
    "cancel_order",
    cancel_order_node
)

workflow.add_node(
    "order_tracking",
    order_tracking_node
)

workflow.add_node(
    "payment_support",
    payment_support_node
)

workflow.add_node(
    "product_recommendation",
    product_recommendation_node
)

workflow.add_node(
    "refund_return",
    refund_return_node
)

# =========================================
# Conditional Routing
# =========================================

workflow.set_conditional_entry_point(
    router
)

# =========================================
# Add Edges
# =========================================

workflow.add_edge("faq", END)

workflow.add_edge(
    "cancel_order",
    END
)

workflow.add_edge(
    "order_tracking",
    END
)

workflow.add_edge(
    "payment_support",
    END
)

workflow.add_edge(
    "product_recommendation",
    END
)

workflow.add_edge(
    "refund_return",
    END
)

# =========================================
# Compile Graph
# =========================================

app = workflow.compile()