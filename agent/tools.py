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
TOOL_REGISTRY = [EchoTool(),
     CreateEventTool(),
      ListEventsTool(),
      DeleteEventTool(),
      FindFreeTimeTool(),
       NotionCreatePageTool(),
      NotionSearchTool(),
      SearchMemoryTool()]