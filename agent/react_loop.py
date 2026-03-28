import re, os, json
from anthropic import Anthropic
from dotenv import load_dotenv
from agent.tools import TOOL_REGISTRY

load_dotenv()
client = Anthropic()
MAX_ITERATIONS = 10


def build_system_prompt() -> str:
    tool_descriptions = '\n'.join(
        f'- {t.name}: {t.description}  |  params: {list(t.parameters.keys())}'
        for t in TOOL_REGISTRY
    )
    return f'''You are Kaashvi, a helpful AI assistant build specially for you user that is divyanshi kashyap and with access to tools.
Always respond in this exact format:

Thought: (your reasoning about what to do next)
Action: (tool name, or FINAL_ANSWER if done)
Action Input: (a JSON object with the tool parameters)

Available tools:
{tool_descriptions}

When you are done, set Action to FINAL_ANSWER and put your reply in Action Input.
'''


def parse_action(text: str) -> tuple[str, dict]:
    """Extract Action and Action Input from LLM response."""
    action_match = re.search(r'Action:\s*(.+)', text)
    input_match = re.search(r'Action Input:\s*(\{.*?\})', text, re.DOTALL)
    action = action_match.group(1).strip() if action_match else 'FINAL_ANSWER'
    try:
        params = json.loads(input_match.group(1)) if input_match else {}
    except Exception:
        params = {}
    return action, params


def run_agent(user_message: str) -> str:
    messages = [{'role': 'user', 'content': user_message}]
    scratchpad = ''

    for iteration in range(MAX_ITERATIONS):
        response = client.messages.create(
            model='claude-sonnet-4-20250514',
            max_tokens=1024,
            system=build_system_prompt(),
            messages=messages + [{'role': 'user', 'content': scratchpad}] if scratchpad else messages
        )
        llm_output = response.content[0].text
        action, params = parse_action(llm_output)

        if action == 'FINAL_ANSWER':
            return params.get('answer', llm_output)

        # Find and execute the tool
        tool = next((t for t in TOOL_REGISTRY if t.name == action), None)
        observation = tool.execute(**params) if tool else f'Error: tool {action} not found'

        # Append to scratchpad so the LLM sees what happened
        scratchpad += f'\n{llm_output}\nObservation: {observation}\n'

    return 'Max iterations reached without a final answer.'
