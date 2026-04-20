from dataclasses import dataclass
from typing import Any


@dataclass
class Tool:
    name: str
    description: str
    parameters : dict

    def execute( self, **kwargs)-> str:
        raise NotImplementedError

class EchoTool(Tool):
      def __init__(self):
          super().__init__(
              name='echo',
              description='Repeats back whatever you tell it. Use for testing.',
              parameters={'message': {'type':   'string', 'description': 'Text to echo'}}
          )

      def execute(self, message: str = '',**kwargs) -> str:
          return f'Echo: {message}'

from integrations.calendar_tools import CreateEventTool, ListEventsTool, DeleteEventTool, FindFreeTimeTool
from integrations.notion_tools import NotionCreatePageTool, NotionSearchTool
from integrations.memory_tools import SearchMemoryTool
from integrations.gmail_tools import GmailSendTool, GmailReadTool, GmailSearchTool
from integrations.web_search_tools import WebSearchTool
from integrations.weather_tools import WeatherTool
from integrations.file_tools import ReadFileTool, WriteFileTool, ListFilesTool
from integrations.reminder_tools import SetReminderTool, ListRemindersTool, CheckRemindersTool
from integrations.task_tools import AddTaskTool, ListTasksTool, CompleteTaskTool, DeleteTaskTool
from integrations.shell_tools import RunCommandTool

TOOL_REGISTRY = [
    EchoTool(),
    # Calendar
    CreateEventTool(),
    ListEventsTool(),
    DeleteEventTool(),
    FindFreeTimeTool(),
    # Notion
    NotionCreatePageTool(),
    NotionSearchTool(),
    # Memory
    SearchMemoryTool(),
    # Gmail
    GmailSendTool(),
    GmailReadTool(),
    GmailSearchTool(),
    # Web Search
    WebSearchTool(),
    # Weather
    WeatherTool(),
    # File Management
    ReadFileTool(),
    WriteFileTool(),
    ListFilesTool(),
    # Reminders
    SetReminderTool(),
    ListRemindersTool(),
    CheckRemindersTool(),
    # Tasks
    AddTaskTool(),
    ListTasksTool(),
    CompleteTaskTool(),
    DeleteTaskTool(),
    # Shell
    RunCommandTool(),
]
