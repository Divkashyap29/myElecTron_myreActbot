import re, os, json
from anthropic import Anthropic
from dotenv import load_dotenv
from agent.tools import TOOL_REGISTRY

load_dotenv()
client = Anthropic()
MAX_ITERATIONS = 10

def count_tokens(conversation_history: list) -> int:
    return sum(len(msg['content']) for msg in conversation_history) // 4


def trim_history(conversation_history: list, max_tokens: int = 10000, archive_path ='memory_archive.json'):
    archive = [] 
    if count_tokens(conversation_history) <= max_tokens:
        return conversation_history 
    if os.path.exists(archive_path):
        with open( archive_path,'r') as f:
            archive = json.load(f)
    else:
     archive = []
    while count_tokens(conversation_history) > max_tokens and len(conversation_history) > 2:
        archive.extend(conversation_history[:2])
        conversation_history = conversation_history[2:]
    with open(archive_path, 'w') as f:
        json.dump(archive, f)
    return conversation_history


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
    input_match = re.search(r'Action Input:\s*(\{.*\})', text, re.DOTALL)
    action = action_match.group(1).strip() if action_match else 'FINAL_ANSWER'
    try:
        params = json.loads(input_match.group(1)) if input_match else {}
    except Exception:
        params = {}
    return action, params


def run_agent(user_message: str, conversation_history: list = None) -> tuple[str, list]:
    if conversation_history is None:
        conversation_history = []
    conversation_history.append({'role': 'user', 'content': user_message})
    conversation_history = trim_history(conversation_history)
    messages = list(conversation_history)
    scratchpad = ''

    for iteration in range(MAX_ITERATIONS):
        if scratchpad:
            current_messages = messages + [{'role': 'user', 'content': scratchpad}]
        else:
            current_messages = messages

        response = client.messages.create(
            model='claude-sonnet-4-20250514',
            max_tokens=1024,
            system=build_system_prompt(),
            messages=current_messages
        )
        llm_output = response.content[0].text
        action, params = parse_action(llm_output)

        if action == 'FINAL_ANSWER':
            answer = params.get('answer') or params.get('response') or next(iter(params.values()), llm_output)
            conversation_history.append({'role': 'assistant', 'content': answer})
            return answer, conversation_history

        tool = next((t for t in TOOL_REGISTRY if t.name == action), None)
        observation = tool.execute(**params) if tool else f'Error: tool {action} not found'
        scratchpad += f'\n{llm_output}\nObservation: {observation}\n'

    return 'Max iterations reached without a final answer.', conversation_history
