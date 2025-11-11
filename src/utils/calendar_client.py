from google.oauth2 import service_account
from googleapiclient.discovery import build
from src.config import Settings
from src.utils.messages import CalendarEvent
from pathlib import Path

service_account_file_path = Path(__file__).parent / "service_account.json"
class CalendarClient: 
    def __init__(self):
        self.service = build("calendar", "v3", 
            credentials = service_account.Credentials.from_service_account_file(
                service_account_file_path,
                scopes=["https://www.googleapis.com/auth/calendar"]
            )
        )
        
    def add_event(self, event_data: CalendarEvent) -> str: 
        event = self.service.events().insert(calendarId=Settings.CALENDAR_ID, body=event_data).execute()
        return "---tbd---"

    def list_events(self, time_min : str , time_max: str) -> str:
        print(f"timeMin: {time_min}")
        events_result = self.service.events().list(
            calendarId=Settings.CALENDAR_ID,
            timeMin=time_min,
            timeMax=time_max,
            singleEvents=True,
            orderBy="startTime"
        ).execute()
        events = events_result.get("items", [])
        if not events:
            print("No upcoming events.")
        else:
            for event in events:
                start = event["start"].get("dateTime", event["start"].get("date"))
                print(start, event["summary"])
        return "---tbd---"