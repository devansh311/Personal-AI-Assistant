import sqlite3

from graph.state import ChatState
from graph.nodes import chat_node
from graph.nodes import tools

from langgraph.graph import StateGraph
from langgraph.graph import START

from langgraph.prebuilt import ToolNode
from langgraph.prebuilt import tools_condition

from langgraph.checkpoint.sqlite import SqliteSaver


graph = StateGraph(ChatState)

tool_node = ToolNode(tools)

graph.add_node("chat", chat_node)
graph.add_node("tools", tool_node)

graph.add_edge(START,"chat")

graph.add_conditional_edges("chat",tools_condition)

graph.add_edge("tools", "chat")

conn = sqlite3.connect("database/chatbot.db",check_same_thread=False)

memory = SqliteSaver(conn)

chatbot = graph.compile(checkpointer=memory)