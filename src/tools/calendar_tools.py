from autogen_core.tools import FunctionTool
from src.utils.messages import CalendarEvent, EventDateTime
from src.utils.calendar_client import CalendarClient
from src.config import Settings
from datetime import datetime
import tzlocal

def add_event_to_calendar(event: CalendarEvent) -> str:
    client = CalendarClient();
    result = client.service.events().insert(calendarId=Settings.CALENDAR_ID, body=event.model_dump()).execute()
    return f"Result: {result}"

def get_date_and_time() -> str:
    time_zone = tzlocal.get_localzone()
    date_and_time = datetime.now(time_zone)
    return (
        f"Today's date and time: {date_and_time}.\n"
        f"TIME ZONE: {time_zone}.\n"
        f"Today's day of the week: {date_and_time.strftime('%A')}"
    )

def fetch_events(time_min: EventDateTime, time_max: EventDateTime) -> str:
    client = CalendarClient();
    events_list = client.service.events().list(
            calendarId=Settings.CALENDAR_ID,
            timeMin=time_min.dateTime,
            timeMax=time_max.dateTime,
            timeZone=time_min.timeZone,
            singleEvents=True,
            orderBy="startTime"
    ).execute()
    if not events_list:
        return "No events found in this time range."
    events = events_list.get("items", [])
    return f"Events:\n {events}"

def patch_event(event_id: str, start: EventDateTime, end: EventDateTime) -> str:
    client = CalendarClient();
    result = client.service.events().patch(
            calendarId=Settings.CALENDAR_ID,
            eventId=event_id,
            body={
                "start": start.model_dump(),
                "end": end.model_dump(),   
            }
    ).execute()
    return f"Result: {result}"

get_datetime_tool = FunctionTool(get_date_and_time, description="Use to fetch current date and time.")
add_event_to_calendar_tool = FunctionTool(
    add_event_to_calendar, description="Use to add event to calendar."
)
fetch_events_tool = FunctionTool(fetch_events, description="Use to fetch events from the calendar.")
reschedule_event_tool = FunctionTool(patch_event, description="Use to reschedule and update event in the calendar.")