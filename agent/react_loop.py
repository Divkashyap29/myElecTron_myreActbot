import re, os, json, time
from datetime import datetime
from anthropic import Anthropic, APIStatusError
from dotenv import load_dotenv
from agent.tools import TOOL_REGISTRY

load_dotenv()
client = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))

# Model configuration
# Claude is a decoder-only transformer (~80 layers of multi-head attention + FFN)
# Understanding: every API call sends our prompt through these transformer blocks,
# and the decoder generates one token at a time via softmax over the vocabulary
MODEL_NAME = 'claude-sonnet-4-20250514'
MAX_CONTEXT_TOKENS = 200000   # Claude Sonnet's context window
MAX_OUTPUT_TOKENS = 1024       # how many tokens the decoder will generate
MAX_ITERATIONS = 10            # ReAct loop safety limit


def count_tokens(conversation_history: list) -> int:
    return sum(len(msg['content']) for msg in conversation_history) // 4


def trim_history(conversation_history: list, max_tokens: int = 10000, archive_path='memory_archive.json'):
    archive = []
    if count_tokens(conversation_history) <= max_tokens:
        return conversation_history
    if os.path.exists(archive_path):
        with open(archive_path, 'r') as f:
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
        f'- {t.name}: {t.description} | params: {list(t.parameters.keys())}'
        for t in TOOL_REGISTRY
    )

    # Few-shot examples (GPT-3 paper, B2): showing the model 3 real examples
    # of the Thought/Action/Observation pattern so attention heads can learn
    # the exact format from context, not just from abstract instructions.
    # Example 1: tool call (calendar)
    # Example 2: multi-step reasoning (check free time then create event)
    # Example 3: direct answer (no tool needed)
    few_shot_examples = """Here are examples of how to respond:

Example 1 — Using a tool:
User: "What events do I have this week?"
Thought: The user wants to see their upcoming calendar events. I should use calendar_list_events to fetch them.
Action: calendar_list_events
Action Input: {"days_ahead": 7}
Observation: - Team standup @ 2026-04-18T09:00:00Z\n- Lunch with Sanskriti @ 2026-04-19T12:00:00Z
Thought: I have the events. Let me present them clearly to the user.
Action: FINAL_ANSWER
Action Input: {"answer": "Here are your events this week:\\n\\n- Team standup — Friday Apr 18 at 9:00 AM\\n- Lunch with Sanskriti — Saturday Apr 19 at 12:00 PM"}

Example 2 — Multi-step (check then act):
User: "Schedule a study session tomorrow at 4pm for 2 hours"
Thought: I need to create a calendar event. I have the title, start time, and can calculate the end time (4pm + 2 hours = 6pm). Let me create it directly.
Action: calendar_create_event
Action Input: {"title": "Study Session", "start": "2026-04-19T16:00:00", "end": "2026-04-19T18:00:00"}
Observation: Event created: Study Session | ID: abc123
Thought: The event was created successfully. I should confirm with the user.
Action: FINAL_ANSWER
Action Input: {"answer": "Done! I scheduled your Study Session for tomorrow from 4:00 PM to 6:00 PM."}

Example 3 — No tool needed:
User: "Thanks Kaashvi!"
Thought: The user is just saying thanks. No tool is needed, I should respond warmly.
Action: FINAL_ANSWER
Action Input: {"answer": "You're welcome! Let me know if you need anything else."}"""

    today = datetime.now().strftime('%Y-%m-%d (%A)')

    return f"""You are Kaashvi, a personal AI assistant built for Divyanshi Kashyap. You are warm, helpful, and remember context from earlier in the conversation.

Today's date: {today}

Available tools:
{tool_descriptions}

You must ALWAYS respond in this exact format:

Thought: <your reasoning about what to do next>
Action: <tool name from the list above, or FINAL_ANSWER if you are done>
Action Input: <a JSON object with the tool parameters, or your final response as JSON>

CRITICAL RULES:
- Output ONLY ONE Thought/Action/Action Input per response, then STOP.
- Do NOT write "Observation:" yourself. The system will provide it.
- Do NOT plan multiple steps ahead in one response. One action at a time.
- For multi-step tasks (like creating 5 events), do ONE action, wait for the Observation, then do the next.

{few_shot_examples}

When you have the answer, use Action: FINAL_ANSWER and put your reply in Action Input as {{"answer": "your response here"}}.
Do not add any text outside this format."""


def extract_first_json(text: str) -> str:
    """Extract only the first complete JSON object from a string.
    Fixes the bug where re.DOTALL grabs hallucinated observations
    after the real JSON, causing json.loads to fail on the extra text."""
    if not text.startswith('{'):
        return text
    depth = 0
    for i, ch in enumerate(text):
        if ch == '{':
            depth += 1
        elif ch == '}':
            depth -= 1
        if depth == 0:
            return text[:i + 1]
    return text


def parse_action(text: str) -> tuple[str, dict]:
    action_match = re.search(r'Action:\s*(.+)', text)
    input_match = re.search(r'Action Input:\s*(.*)', text, re.DOTALL)
    action = action_match.group(1).strip() if action_match else 'FINAL_ANSWER'
    if not input_match:
        return action, {}
    raw_input = extract_first_json(input_match.group(1).strip())
    try:
        params = json.loads(raw_input)
        if isinstance(params, str):
            params = {'answer': params}
        return action, params
    except json.JSONDecodeError:
        if action == 'FINAL_ANSWER':
            return action, {'answer': raw_input}
        return action, {}


def run_agent(user_message: str, conversation_history: list = None, stream: bool = False) -> tuple[str, list]:
    if conversation_history is None:
        conversation_history = []
    conversation_history.append({'role': 'user', 'content': user_message})
    conversation_history = trim_history(conversation_history)
    messages = list(conversation_history)
    scratchpad = ''

    for iteration in range(MAX_ITERATIONS):
        # 1. Build messages — scratchpad goes FIRST so LLM sees previous reasoning
        if scratchpad:
            current_messages = messages + [{'role': 'user', 'content': scratchpad}]
        else:
            current_messages = messages

        # 2. Call LLM — stream OR non-stream, with retry for transient errors
        llm_output = ''
        for attempt in range(3):
            try:
                if stream:
                    llm_output = ''
                    with client.messages.stream(
                        model=MODEL_NAME,
                        max_tokens=MAX_OUTPUT_TOKENS,
                        system=build_system_prompt(),
                        messages=current_messages
                    ) as response:
                        for token in response.text_stream:
                            print(token, end='', flush=True)
                            llm_output += token
                    print()  # newline after streaming finishes
                else:
                    response = client.messages.create(
                        model=MODEL_NAME,
                        max_tokens=MAX_OUTPUT_TOKENS,
                        system=build_system_prompt(),
                        messages=current_messages
                    )
                    llm_output = response.content[0].text
                break  # success, exit retry loop
            except APIStatusError as e:
                if 'overloaded' in str(e).lower() and attempt < 2:
                    wait = 2 ** (attempt + 1)  # 2s, 4s
                    print(f'\n[API overloaded, retrying in {wait}s...]')
                    time.sleep(wait)
                else:
                    raise

        # 3. Parse the action from LLM output
        action, params = parse_action(llm_output)

        if action == 'FINAL_ANSWER':
            answer = params.get('answer') or params.get('response') or next(iter(params.values()), llm_output)
            conversation_history.append({'role': 'assistant', 'content': answer})
            return answer, conversation_history

        # 4. Execute the tool and add observation to scratchpad
        tool = next((t for t in TOOL_REGISTRY if t.name == action), None)
        observation = tool.execute(**params) if tool else f'Error: tool {action} not found'
        scratchpad += f'\n{llm_output}\nObservation: {observation}\n'

    return 'Max iterations reached without a final answer.', conversation_history
