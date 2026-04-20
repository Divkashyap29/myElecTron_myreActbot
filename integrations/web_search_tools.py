from agent.tools import Tool


class WebSearchTool(Tool):
    def __init__(self):
        super().__init__(
            name='web_search',
            description='Search the web using DuckDuckGo. Returns titles, snippets, and URLs.',
            parameters={
                'query': {'type': 'string', 'description': 'Search query'},
                'max_results': {'type': 'integer', 'default': 5},
            }
        )

    def execute(self, query='', max_results=5, **kwargs) -> str:
        try:
            from duckduckgo_search import DDGS
            with DDGS() as ddgs:
                results = list(ddgs.text(query, max_results=max_results))
            if not results:
                return f'No results found for "{query}".'
            lines = []
            for r in results:
                lines.append(
                    f"- **{r['title']}**\n  {r['body']}\n  {r['href']}"
                )
            return '\n'.join(lines)
        except Exception as e:
            return f"Error searching web: {e}"
