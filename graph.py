from langgraph.graph import StateGraph, START, END

from state import TravelState

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

# Graph Flow
builder.add_edge(START, "extract_information")
builder.add_edge("extract_information", "planner")
builder.add_edge("planner", "executor")
builder.add_edge("executor", "response")
builder.add_edge("response", END)

graph = builder.compile()