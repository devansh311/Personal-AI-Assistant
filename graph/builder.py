import psycopg
from langchain_core.messages import ToolMessage

from graph.state import ChatState
from graph.nodes import (
    chat_node,
    calendar_confirmation_node,
    tools
)

from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.checkpoint.postgres import PostgresSaver
from config.settings import DATABASE_URL


def after_tools_routing(state):
    """
    After ToolNode executes, check which tool ran last.
    Routes to appropriate HITL node or back to chat.
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
graph.add_conditional_edges("chat", tools_condition)
graph.add_conditional_edges(
    "tools",
    after_tools_routing,
    {
        "calendar_confirmation": "calendar_confirmation",
        "chat": "chat"
    }
)

graph.add_edge("calendar_confirmation", END)


# PostgreSQL connection — autocommit required for PostgresSaver
conn = psycopg.connect(DATABASE_URL, autocommit=True)
memory = PostgresSaver(conn)
memory.setup()  # creates checkpoint tables if they don't exist

chatbot = graph.compile(
    checkpointer=memory,
    interrupt_before=["calendar_confirmation"]
)