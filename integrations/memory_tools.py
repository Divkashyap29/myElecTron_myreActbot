import os, json 
from agent.tools import Tool

class SearchMemoryTool(Tool):
    def __init__(self):
        super().__init__(
            name='search_memory',
            description='Search through past archived conversations to find forgotten information. Use when the user asks about something from a previous conversation.',
            parameters={'query':{'type':'string','description':'keyword to search for in past conversations'}})
        
    def execute(self,query='', **kwargs) -> str:
        archive_path='memory_archive.json'
        if not os.path.exists(archive_path):
            return 'No archived memories found.'
        with open(archive_path,'r') as f:
            archive = json.load(f)
        matches =[]
        for msg in archive:
            if query.lower() in msg['content'].lower():
                matches.append(f"{msg['role']}:{msg['content']}")
            
        if not matches:
            return f'No memories found matching "{query}".'
        return '\n'.join(matches[-10:])
    