import os
from notion_client import Client
from agent.tools import Tool
from dotenv import load_dotenv

load_dotenv()
notion = Client(auth=os.environ['NOTION_TOKEN'])
DATABASE_ID = os.environ.get('NOTION_DATABASE_ID', '')


class NotionCreatePageTool(Tool):
    def __init__(self):
        super().__init__(
            name='notion_create_page',
            description='Create a new page/task in your Notion database. Provide a title and optional content.',
            parameters={
                'title': {'type': 'string'},
                'content': {'type': 'string', 'default': ''}
            }
        )

    def execute(self, title='', content='', **kwargs) -> str:
        try:
            new_page = {
                'parent': {'database_id': DATABASE_ID},
                'properties': {
                    'Name': {'title': [{'text': {'content': title}}]}
                },
                'children': [{'object': 'block', 'type': 'paragraph', 'paragraph': {'rich_text': [{'text': {'content': content}}]}}] if content else []
            }
            page = notion.pages.create(**new_page)
            return f"Page created: '{title}' | ID: {page['id']}"
        except Exception as e:
            return f'Error creating page: {e}'


class NotionSearchTool(Tool):
    def __init__(self):
        super().__init__(
            name='notion_search',
            description='Search your Notion workspace by keyword. Returns matching page titles and IDs.',
            parameters={'query': {'type': 'string'}}
        )

    def execute(self, query='', **kwargs) -> str:
        try:
            results = notion.search(query=query, filter={'property': 'object', 'value': 'page'}).get('results', [])
            if not results:
                return f'No Notion pages found for: {query}'
            lines = []
            for r in results[:5]:
                title_prop = r.get('properties', {}).get('Name', {}).get('title', [{}])
                title = title_prop[0].get('text', {}).get('content', 'Untitled') if title_prop else 'Untitled'
                lines.append(f"- {title} | {r['id']}")
            return '\n'.join(lines)
        except Exception as e:
            return f'Error searching Notion: {e}'
