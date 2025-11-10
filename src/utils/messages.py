from typing import List
from pydantic import BaseModel, Field
from autogen_core.models import LLMMessage
from datetime import datetime

class UserLogin(BaseModel):
    pass


class UserTask(BaseModel):
    context: List[LLMMessage]


class AgentResponse(BaseModel):
    reply_to_topic_type: str
    context: List[LLMMessage]

class EventDateTime(BaseModel):
    dateTime: datetime = Field(..., description="Event start datetime in ISO 8601 format")
    timeZone: str | None = Field(None, description="timezone of event") #. tbd - Make this required.

class CalendarEvent(BaseModel):
    summary: str = Field(..., description="Short title for the event")
    location: str | None = Field(None, description="Location of the event")
    description: str | None = Field(None, description="Description of the event")
    start: EventDateTime
    end: EventDateTime 
    recurrence: List[str] | None = Field(None, description=("Recurrence rules (RRULE)"))