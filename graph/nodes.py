from langchain_core.messages import SystemMessage

from config.llm import llm
from prompts.system_prompt import SYSTEM_PROMPT

from tools.calculator import calculator
from tools.search import search_tool
from tools.stocks import get_stock_price

from tools.weather import get_weather

from tools.calendar import get_upcoming_events

from tools.rag import ask_documents

tools = [
    calculator,
    search_tool,
    get_stock_price,
    get_weather,
    get_upcoming_events,
    ask_documents
]

llm_with_tools = llm.bind_tools(tools).with_config(
    {
        "run_name":"chat model"
    }
)


def chat_node(state):

    print("=" * 50)
    print("Entered chat node")

    messages = state["messages"]

    print(messages)

    response = llm_with_tools.invoke(
        [SystemMessage(content=SYSTEM_PROMPT)] + messages
    )

    print("LLM responded:", repr(response.content))

    return {
        "messages": [response]
    }