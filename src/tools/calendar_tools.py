from autogen_core.tools import FunctionTool
from src.utils.messages import CalendarEvent, EventDateTime
from src.utils.calendar_client import CalendarClient
from src.config import Settings
from datetime import datetime
import tzlocal

def add_event_to_calendar(event: CalendarEvent) -> str:
    # client = CalendarClient();
    print(f"Below is the calendar event:\n{event}")
    return "event added to calendar"

def get_date_and_time() -> str:
    time_zone = tzlocal.get_localzone()
    date_and_time = datetime.now(time_zone)
    return (
        f"Today's date and time: {date_and_time}.\n"
        f"TIME ZONE: {time_zone}.\n"
        f"Today's day of the week: {date_and_time.strftime('%A')}"
    )

def fetch_events(time_max: EventDateTime, time_min: EventDateTime) -> str:
    client = CalendarClient();
    events_list = client.service.events().list(
            calendarId=Settings.CALENDAR_ID,
            timeMin=time_min,
            timeMax=time_max,
            singleEvents=True,
            orderBy="startTime"
    ).execute()

    events = events_result.get("items", [])
    return f"Events:\n {events}"

get_datetime_tool = FunctionTool(get_date_and_time, description="Use to fetch current date and time.")
add_event_to_calendar_tool = FunctionTool(
    add_event_to_calendar, description="Use to add event to calendar."
)
fetch_events_tool = FunctionTool(fetch_events, description="Use to fetch events from the calendar.")