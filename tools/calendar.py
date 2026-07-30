from datetime import datetime, timezone, timedelta
from langchain_core.tools import tool
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import os

SCOPES = ["https://www.googleapis.com/auth/calendar"]

# stores event details between prepare and confirm steps
pending_event = {}


def authenticate():
    creds = None

    if os.path.exists("credentials/token.json"):
        creds = Credentials.from_authorized_user_file(
            "credentials/token.json",
            SCOPES
        )

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials/credentials.json",
                SCOPES
            )
            creds = flow.run_local_server(port=0)

        with open("credentials/token.json", "w") as token:
            token.write(creds.to_json())

    return build("calendar", "v3", credentials=creds)


@tool
def get_upcoming_events():
    """
    Get the next 10 upcoming events from Google Calendar.
    Use this tool whenever the user asks about
    meetings, schedule, events, appointments or calendar.
    """
    service = authenticate()

    now = datetime.now(timezone.utc).isoformat()
    events_result = service.events().list(
        calendarId="primary",
        timeMin=now,
        maxResults=10,
        singleEvents=True,
        orderBy="startTime"
    ).execute()

    events = events_result.get("items", [])

    if not events:
        return {"events": []}

    result = []
    for event in events:
        start = event["start"].get("dateTime", event["start"].get("date"))
        result.append({"title": event["summary"], "start": start})

    return {"events": result}


@tool
def prepare_calendar_event(
    title: str,
    date: str,
    time: str,
    duration_minutes: int = 60
):
    """
    Use this tool when the user wants to CREATE, ADD or SCHEDULE
    a new calendar event. Extract the event title, date (YYYY-MM-DD),
    time (HH:MM in 24hr format) and duration from the user message.
    Always call this BEFORE creating any event.
    """
    global pending_event

   # NEW - updates in place (keeps same object, import reference stays valid)
    pending_event.clear()
    pending_event.update({
    "title": title,
    "date": date,
    "time": time,
    "duration_minutes": duration_minutes
    })

    return {
        "status": "pending_confirmation",
        "title": title,
        "date": date,
        "time": time,
        "duration_minutes": duration_minutes
    }

def create_event_direct(event_data: dict) -> str:
    try:
        service = authenticate()

        # parse datetime
        start_dt = datetime.strptime(
            f"{event_data['date']} {event_data['time']}",
            "%Y-%m-%d %H:%M"
        )
        end_dt = start_dt + timedelta(minutes=event_data["duration_minutes"])

        event = {
            "summary": event_data["title"],
            "start": {
                # explicit IST offset — no ambiguity
                "dateTime": start_dt.strftime("%Y-%m-%dT%H:%M:00+05:30"),
                "timeZone": "Asia/Kolkata"
            },
            "end": {
                "dateTime": end_dt.strftime("%Y-%m-%dT%H:%M:00+05:30"),
                "timeZone": "Asia/Kolkata"
            }
        }

        created = service.events().insert(
            calendarId="primary",
            body=event
        ).execute()

        pending_event.clear()

        return (
            f"✅ Event '{created['summary']}' created successfully!\n"
            f"🔗 Open in Calendar: {created.get('htmlLink', 'N/A')}"
        )

    except ValueError as e:
        return f"❌ Invalid date/time format: {str(e)}"
    except Exception as e:
        return f"❌ Failed to create event: {str(e)}"

