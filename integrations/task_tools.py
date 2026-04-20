import os, json, uuid
from datetime import datetime
from agent.tools import Tool

TASKS_FILE = 'tasks.json'


def _load_tasks():
    if os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, 'r') as f:
            return json.load(f)
    return []


def _save_tasks(tasks):
    with open(TASKS_FILE, 'w') as f:
        json.dump(tasks, f, indent=2)


class AddTaskTool(Tool):
    def __init__(self):
        super().__init__(
            name='add_task',
            description='Add a new task to your to-do list.',
            parameters={
                'title': {'type': 'string', 'description': 'Task title'},
                'priority': {'type': 'string', 'description': 'Priority: high, medium, or low', 'default': 'medium'},
                'due_date': {'type': 'string', 'description': 'Due date (ISO format, optional)', 'default': ''},
            }
        )

    def execute(self, title='', priority='medium', due_date='', **kwargs) -> str:
        if priority not in ('high', 'medium', 'low'):
            priority = 'medium'
        tasks = _load_tasks()
        task = {
            'id': str(uuid.uuid4())[:8],
            'title': title,
            'priority': priority,
            'due_date': due_date,
            'status': 'pending',
            'created_at': datetime.now().isoformat(),
        }
        tasks.append(task)
        _save_tasks(tasks)
        return f"Task added: \"{title}\" [{priority}] (ID: {task['id']})"


class ListTasksTool(Tool):
    def __init__(self):
        super().__init__(
            name='list_tasks',
            description='List tasks, optionally filtered by status or priority.',
            parameters={
                'status': {'type': 'string', 'description': 'Filter: pending, done, or all', 'default': 'pending'},
                'priority': {'type': 'string', 'description': 'Filter: high, medium, low, or all', 'default': 'all'},
            }
        )

    def execute(self, status='pending', priority='all', **kwargs) -> str:
        tasks = _load_tasks()
        if status != 'all':
            tasks = [t for t in tasks if t['status'] == status]
        if priority != 'all':
            tasks = [t for t in tasks if t['priority'] == priority]
        if not tasks:
            return 'No tasks found matching filters.'
        priority_order = {'high': 0, 'medium': 1, 'low': 2}
        tasks.sort(key=lambda t: priority_order.get(t['priority'], 1))
        lines = []
        for t in tasks:
            due = f" | due: {t['due_date']}" if t.get('due_date') else ''
            lines.append(f"- [{t['id']}] {t['title']} ({t['priority']}{due}) [{t['status']}]")
        return f"Tasks ({len(lines)}):\n" + '\n'.join(lines)


class CompleteTaskTool(Tool):
    def __init__(self):
        super().__init__(
            name='complete_task',
            description='Mark a task as done by its ID.',
            parameters={
                'task_id': {'type': 'string', 'description': 'Task ID to complete'},
            }
        )

    def execute(self, task_id='', **kwargs) -> str:
        tasks = _load_tasks()
        for t in tasks:
            if t['id'] == task_id:
                t['status'] = 'done'
                t['completed_at'] = datetime.now().isoformat()
                _save_tasks(tasks)
                return f"Task \"{t['title']}\" marked as done."
        return f"Task with ID '{task_id}' not found."


class DeleteTaskTool(Tool):
    def __init__(self):
        super().__init__(
            name='delete_task',
            description='Delete a task by its ID.',
            parameters={
                'task_id': {'type': 'string', 'description': 'Task ID to delete'},
            }
        )

    def execute(self, task_id='', **kwargs) -> str:
        tasks = _load_tasks()
        original_len = len(tasks)
        tasks = [t for t in tasks if t['id'] != task_id]
        if len(tasks) == original_len:
            return f"Task with ID '{task_id}' not found."
        _save_tasks(tasks)
        return f"Task '{task_id}' deleted."
