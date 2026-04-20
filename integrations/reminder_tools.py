import os, json, uuid
from datetime import datetime
from agent.tools import Tool

REMINDERS_FILE = 'reminders.json'


def _load_reminders():
    if os.path.exists(REMINDERS_FILE):
        with open(REMINDERS_FILE, 'r') as f:
            return json.load(f)
    return []


def _save_reminders(reminders):
    with open(REMINDERS_FILE, 'w') as f:
        json.dump(reminders, f, indent=2)


class SetReminderTool(Tool):
    def __init__(self):
        super().__init__(
            name='set_reminder',
            description='Set a reminder with a message and trigger time (ISO format or natural like "2026-04-20T17:00:00").',
            parameters={
                'message': {'type': 'string', 'description': 'Reminder message'},
                'trigger_time': {'type': 'string', 'description': 'When to trigger (ISO 8601 format)'},
            }
        )

    def execute(self, message='', trigger_time='', **kwargs) -> str:
        try:
            # Validate the time is parseable
            dt = datetime.fromisoformat(trigger_time)
            reminders = _load_reminders()
            reminder = {
                'id': str(uuid.uuid4())[:8],
                'message': message,
                'trigger_time': trigger_time,
                'created_at': datetime.now().isoformat(),
                'done': False,
            }
            reminders.append(reminder)
            _save_reminders(reminders)
            return f"Reminder set: \"{message}\" at {dt.strftime('%b %d %I:%M %p')} (ID: {reminder['id']})"
        except ValueError:
            return f"Invalid time format: {trigger_time}. Use ISO format like 2026-04-20T17:00:00"
        except Exception as e:
            return f"Error setting reminder: {e}"


class ListRemindersTool(Tool):
    def __init__(self):
        super().__init__(
            name='list_reminders',
            description='List all pending (not yet fired) reminders.',
            parameters={}
        )

    def execute(self, **kwargs) -> str:
        reminders = _load_reminders()
        pending = [r for r in reminders if not r['done']]
        if not pending:
            return 'No pending reminders.'
        lines = []
        for r in sorted(pending, key=lambda x: x['trigger_time']):
            lines.append(f"- [{r['id']}] {r['message']} @ {r['trigger_time']}")
        return f"Pending reminders ({len(lines)}):\n" + '\n'.join(lines)


class CheckRemindersTool(Tool):
    def __init__(self):
        super().__init__(
            name='check_reminders',
            description='Check for due reminders and mark them as done. Returns any reminders that have fired.',
            parameters={}
        )

    def execute(self, **kwargs) -> str:
        reminders = _load_reminders()
        now = datetime.now()
        fired = []
        for r in reminders:
            if r['done']:
                continue
            try:
                trigger = datetime.fromisoformat(r['trigger_time'])
                if trigger <= now:
                    r['done'] = True
                    fired.append(r)
            except ValueError:
                continue
        _save_reminders(reminders)
        if not fired:
            return 'No reminders due right now.'
        lines = [f"- REMINDER: {r['message']} (was due {r['trigger_time']})" for r in fired]
        return f"🔔 {len(fired)} reminder(s) fired:\n" + '\n'.join(lines)
