from autogen_core.tools import FunctionTool
from src.utils.messages import CalendarEvent
from src.utils.calendar_client import CalendarClient
from datetime import datetime
import tzlocal

def add_event_to_calendar(event: CalendarEvent) -> str:
    # client = CalendarClient();
    print(f"Below is the calendar event:\n{event}")
    return "event added to calendar"

def get_date_and_time() -> str:
    time_zone = tzlocal.get_localzone()
    date_and_time = datetime.now(time_zone)
    return f"Current date and time: {datetime.now(time_zone)}. TIME ZONE: {time_zone}"

get_datetime_tool = FunctionTool(get_date_and_time, description="Use to fetch current date and time.")
add_event_to_calendar_tool = FunctionTool(
    add_event_to_calendar, description="Use to add event to calendar."
)
