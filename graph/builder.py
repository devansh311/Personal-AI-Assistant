import sqlite3

from langchain_core.messages import ToolMessage

from graph.state import ChatState
from graph.nodes import chat_node, calendar_confirmation_node, tools

from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.checkpoint.sqlite import SqliteSaver


def after_tools_routing(state):
    """
    After ToolNode executes, check which tool ran last.
    If prepare_calendar_event ran → go to HITL confirmation node.
    Otherwise → go back to chat node as usual.
    """
    messages = state["messages"]

    for msg in reversed(messages):
        if isinstance(msg, ToolMessage):
            if msg.name == "prepare_calendar_event":
                return "calendar_confirmation"
            break

    return "chat"


graph = StateGraph(ChatState)

tool_node = ToolNode(tools)

# Add nodes
graph.add_node("chat", chat_node)
graph.add_node("tools", tool_node)
graph.add_node("calendar_confirmation", calendar_confirmation_node)

# Add edges
graph.add_edge(START, "chat")

graph.add_conditional_edges(
    "chat",
    tools_condition
)

# Replace old tools → chat edge with conditional routing
graph.add_conditional_edges(
    "tools",
    after_tools_routing,
    {
        "calendar_confirmation": "calendar_confirmation",
        "chat": "chat"
    }
)

# Calendar confirmation always ends after completing
graph.add_edge("calendar_confirmation", END)

conn = sqlite3.connect("database/chatbot.db", check_same_thread=False)
memory = SqliteSaver(conn)

chatbot = graph.compile(checkpointer=memory)