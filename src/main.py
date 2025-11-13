from autogen_ext.models.openai import OpenAIChatCompletionClient
from src.agents.ai_agent import CalendarAssistantAgent
from autogen_core import AgentId, SingleThreadedAgentRuntime
from autogen_core.models import SystemMessage
from src.tools.calendar_tools import (
    get_datetime_tool,
    add_event_to_calendar_tool,
    fetch_events_tool,
    reschedule_event_tool,
    delete_event_tool,
)
from typing import List
from autogen_core.tools import Tool
from src.config import Settings
from src.tools.messages import Message
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from contextlib import asynccontextmanager

tools: List[Tool] = [
    get_datetime_tool,
    add_event_to_calendar_tool,
    fetch_events_tool,
    reschedule_event_tool,
    delete_event_tool
]

app = FastAPI()
# Create a runtime.
runtime = SingleThreadedAgentRuntime()
# Create the model client.
model_client = OpenAIChatCompletionClient(
    model="gpt-4o-mini",
    api_key=Settings.OPENAI_API_KEY,
)

calendar_assistant_agent = AgentId("calendar_assistant_agent", "default")

@asynccontextmanager
async def lifespan(app: FastAPI):
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
    yield
    # Stop the runtime (Stop processing messages).
    await runtime.stop_when_idle()
    await model_client.close() # close the model client session


app = FastAPI(lifespan=lifespan)

class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

manager = ConnectionManager()


@app.get("/")
async def root():
    return {"message": "Server Running"}

@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    await manager.connect(websocket)
    try:
        while True:
            message =  Message(client_id=client_id, content=await websocket.receive_text())
            # Send the message to the calendar assistant agent.
            response = await runtime.send_message(message, calendar_assistant_agent)
            await manager.send_message(f"Assistant: {response.content}", websocket)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
