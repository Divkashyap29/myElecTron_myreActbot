from datetime import datetime, timedelta
from integrations.google_auth import get_calendar_service
from agent.tools import Tool


class CreateEventTool(Tool):
    def __init__(self):
        super().__init__(
            name='calendar_create_event',
            description='Create a Google Calendar event. Provide title, start time (ISO format), end time, and optional attendee emails.',
            parameters={
                'title': {'type': 'string'},
                'start': {'type': 'string', 'description': 'ISO 8601 e.g. 2026-03-25T14:00:00'},
                'end': {'type': 'string'},
                'attendees': {'type': 'array', 'items': {'type': 'string'}, 'default': []}
            }
        )

    def execute(self, title='', start='', end='', attendees=None, **kwargs) -> str:
        service = get_calendar_service()
        event = {
            'summary': title,
            'start': {'dateTime': start, 'timeZone': 'UTC'},
            'end': {'dateTime': end, 'timeZone': 'UTC'},
            'attendees': [{'email': e} for e in (attendees or [])],
        }
        created = service.events().insert(calendarId='primary', body=event).execute()
        return f"Event created: {created.get('summary')} | ID: {created.get('id')}"


class ListEventsTool(Tool):
    def __init__(self):
        super().__init__(
            name='calendar_list_events',
            description='List upcoming Google Calendar events within a number of days from now.',
            parameters={'days_ahead': {'type': 'integer', 'default': 7}}
        )

    def execute(self, days_ahead=7, **kwargs) -> str:
        service = get_calendar_service()
        now = datetime.utcnow().isoformat() + 'Z'
        end = (datetime.utcnow() + timedelta(days=days_ahead)).isoformat() + 'Z'
        result = service.events().list(
            calendarId='primary', timeMin=now, timeMax=end,
            maxResults=10, singleEvents=True, orderBy='startTime'
        ).execute()
        events = result.get('items', [])
        if not events:
            return 'No upcoming events found.'
        lines = [f"- {e['summary']} @ {e['start'].get('dateTime', e['start'].get('date'))}" for e in events]
        return '\n'.join(lines)


class DeleteEventTool(Tool):
    def __init__(self):
        super().__init__(
            name='calendar_delete_event',
            description='Delete a Google Calendar event by its event ID.',
            parameters={'event_id': {'type': 'string', 'description': 'The event ID to delete'}}
        )

    def execute(self, event_id='', **kwargs) -> str:
        try:
            service = get_calendar_service()
            service.events().delete(calendarId='primary', eventId=event_id).execute()
            return f'Event {event_id} deleted successfully.'
        except Exception as e:
            return f'Error deleting event: {e}'


class FindFreeTimeTool(Tool):
    def __init__(self):
        super().__init__(
            name='calendar_find_free_time',
            description='Find free time slots in your calendar. Provide days ahead and minimum slot duration in minutes.',
            parameters={
                'days_ahead': {'type': 'integer', 'default': 7},
                'duration_minutes': {'type': 'integer', 'default': 30}
            }
        )

    def execute(self, days_ahead=7, duration_minutes=30, **kwargs) -> str:
        service = get_calendar_service()
        now = datetime.utcnow()
        end = now + timedelta(days=days_ahead)

        result = service.events().list(
            calendarId='primary',
            timeMin=now.isoformat() + 'Z',
            timeMax=end.isoformat() + 'Z',
            singleEvents=True, orderBy='startTime'
        ).execute()
        events = result.get('items', [])

        # Find gaps between events
        free_slots = []
        current = now

        for event in events:
            event_start_str = event['start'].get('dateTime', event['start'].get('date'))
            event_end_str = event['end'].get('dateTime', event['end'].get('date'))
            event_start = datetime.fromisoformat(event_start_str.replace('Z', '+00:00')).replace(tzinfo=None)
            event_end = datetime.fromisoformat(event_end_str.replace('Z', '+00:00')).replace(tzinfo=None)

            gap = (event_start - current).total_seconds() / 60
            if gap >= duration_minutes:
                free_slots.append(f"- {current.strftime('%b %d %I:%M%p')} to {event_start.strftime('%I:%M%p')} ({int(gap)} min)")
                current = max(current, event_end)
        final_gap = (end - current).total_seconds() / 60
        if final_gap >= duration_minutes:
            free_slots.append(f"- {current.strftime('%b %d %I:%M%p')} to {end.strftime('%b %d %I:%M%p')} ({int(final_gap)} min)")
        if not free_slots:
            return 'No free slots found in the given range.'
        return 'Free time slots:\n' + '\n'.join(free_slots)
