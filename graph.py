from langgraph.graph import StateGraph, START, END

from state import TravelState


def route_after_extract(state):
    if state.get("error"):
        return END
    return "planner"


def route_after_planner(state):
    if state.get("error"):
        return END
    return "executor"


def route_after_executor(state):
    if state.get("error"):
        return END
    return "response"
from nodes import (
    extract_information,
    planner,
    executor_node,
    response_node,
)

builder = StateGraph(TravelState)

# Nodes
builder.add_node("extract_information", extract_information)
builder.add_node("planner", planner)
builder.add_node("executor", executor_node)
builder.add_node("response", response_node)

builder.add_edge(START, "extract_information")

builder.add_conditional_edges(
    "extract_information",
    route_after_extract,
    {
        "planner": "planner",
        END: END,
    },
)

builder.add_conditional_edges(
    "planner",
    route_after_planner,
    {
        "executor": "executor",
        END: END,
    },
)

builder.add_conditional_edges(
    "executor",
    route_after_executor,
    {
        "response": "response",
        END: END,
    },
)

builder.add_edge("response", END)

graph = builder.compile()