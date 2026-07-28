from datetime import datetime, timezone

from langchain_core.tools import tool
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

import os

SCOPES = [
    "https://www.googleapis.com/auth/calendar"
]


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

    service = build(
        "calendar",
        "v3",
        credentials=creds
    )

    return service


@tool
def get_upcoming_events():

    """
    Get the next 10 upcoming events from Google Calendar.
    Use this tool whenever the user asks about
    meetings, schedule, events, appointments or calendar.
    """

    service = authenticate()
    calendar_list = service.calendarList().list().execute()

    print("Available calendars:")

    for cal in calendar_list["items"]:
     print(cal["summary"], "->", cal["id"])

    now = datetime.now(timezone.utc).isoformat()

    events_result = service.events().list(
        calendarId="primary",
        timeMin=now,
        maxResults=10,
        singleEvents=True,
        orderBy="startTime"
    ).execute()

    events = events_result.get("items", [])
    print("=" * 50)
    print("Total events:", len(events))

    for event in events:
     print(event["summary"])

    if not events:
        return {
            "events": []
        }

    result = []

    for event in events:

        start = event["start"].get(
            "dateTime",
            event["start"].get("date")
        )

        result.append(
            {
                "title": event["summary"],
                "start": start
            }
        )

    return {
        "events": result
    }