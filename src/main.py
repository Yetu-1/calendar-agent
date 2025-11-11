from autogen_ext.models.openai import OpenAIChatCompletionClient
from src.agents.ai_agent import CalendarAssistantAgent
from autogen_core import AgentId, SingleThreadedAgentRuntime
from autogen_core.models import SystemMessage
from src.tools.calendar_tools import (
    get_datetime_tool,
    add_event_to_calendar_tool,
    fetch_events_tool,
)
from src.config import Settings
from src.utils.messages import Message
from fastapi import FastAPI

app = FastAPI()
# Create a runtime.
runtime = SingleThreadedAgentRuntime()
# Create the model client.
model_client = OpenAIChatCompletionClient(
    model="gpt-4o-mini",
    api_key=Settings.OPENAI_API_KEY,
)
calendar_assistant_agent = AgentId("calendar_assistant_agent", "default")

@app.on_event("startup")
async def setupAgent():

    tools: List[Tool] = [
        get_datetime_tool,
        add_event_to_calendar_tool,
        fetch_events_tool
    ]
    # Register the calendar assistant agent
    await CalendarAssistantAgent.register(
        runtime,
        "calendar_assistant_agent",
        lambda: CalendarAssistantAgent(
            model_client=model_client,
            tool_schema=tools,
        ),
    )
    # Start the runtime (Start processing messages).
    runtime.start()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/assistant")
async def root(message: Message):
    # Send a direct message to the calendar assistant agent agent.
    response = await runtime.send_message(Message(content=message.content), calendar_assistant_agent)
    return {"response": response.content}

@app.post("/assistant/exit")
async def root(message: Message):
    # Run until completion (Stop processing messages).
    await runtime.stop_when_idle()
    await model_client.close()