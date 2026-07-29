from langchain_core.messages import SystemMessage, AIMessage
from langchain_core.messages import ToolMessage

from config.llm import llm
from prompts.system_prompt import SYSTEM_PROMPT

from tools.calculator import calculator
from tools.search import search_tool
from tools.stocks import get_stock_price
from tools.weather import get_weather
from tools.rag import ask_documents
from tools.calendar import (
    get_upcoming_events,
    prepare_calendar_event,
    pending_event,
    create_event_direct
)

from langgraph.types import interrupt

tools = [
    calculator,
    search_tool,
    get_stock_price,
    get_weather,
    get_upcoming_events,
    ask_documents,
    prepare_calendar_event
]

llm_with_tools = llm.bind_tools(tools).with_config(
    {"run_name": "chat model"}
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

    return {"messages": [response]}

def calendar_confirmation_node(state):
    if pending_event:
        confirmation_msg = (
            f"📅 Please confirm event creation:\n\n"
            f"Title    : {pending_event['title']}\n"
            f"Date     : {pending_event['date']}\n"
            f"Time     : {pending_event['time']}\n"
            f"Duration : {pending_event['duration_minutes']} minutes\n\n"
            f"Type 'yes' to confirm or 'no' to cancel."
        )
    else:
        confirmation_msg = "No pending event found. Please describe the event again."

    # GRAPH PAUSES HERE
    user_response = interrupt(confirmation_msg)
    # GRAPH RESUMES HERE

    response_lower = user_response.strip().lower()

    # Case 1 — User confirms
    if response_lower in ["yes", "y", "confirm", "ok", "sure", "haan", "ha"]:
        result = create_event_direct(pending_event)
        return {"messages": [AIMessage(content=result)]}

    # Case 2 — User cancels
    elif response_lower in ["no", "n", "cancel", "nahi", "nope"]:
        pending_event.clear()
        return {"messages": [AIMessage(content="❌ Event creation cancelled.")]}

    # Case 3 — User wants to modify duration
    elif "duration" in response_lower or "min" in response_lower or "hour" in response_lower:
        # Extract number from response
        import re
        numbers = re.findall(r'\d+', user_response)
        if numbers:
            new_duration = int(numbers[0])
            # Convert hours to minutes if needed
            if "hour" in response_lower:
                new_duration = new_duration * 60
            pending_event.update({"duration_minutes": new_duration})

        return {
            "messages": [AIMessage(
                content=(
                    f"✏️ Duration updated to {pending_event['duration_minutes']} minutes.\n\n"
                    f"📅 Updated event details:\n"
                    f"Title    : {pending_event['title']}\n"
                    f"Date     : {pending_event['date']}\n"
                    f"Time     : {pending_event['time']}\n"
                    f"Duration : {pending_event['duration_minutes']} minutes\n\n"
                    f"Type 'yes' to confirm or 'no' to cancel."
                )
            )]
        }

    # Case 4 — Anything else unclear
    else:
        return {
            "messages": [AIMessage(
                content=(
                    f"⚠️ I didn't understand that. Please type:\n"
                    f"- 'yes' to confirm the event\n"
                    f"- 'no' to cancel\n"
                    f"- 'duration is X mins' to change duration"
                )
            )]
        }