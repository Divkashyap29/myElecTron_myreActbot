# ReAct — "Reasoning and Acting" (Yao 2023)

## What the paper is about
ReAct introduces the idea of combining reasoning (thinking) and acting (using tools) in a single interleaved loop. Most AI systems either think without doing anything, or use tools without explaining why. ReAct proves that doing both together — Thought, Action, Observation, repeat — produces more accurate and interpretable results than either approach alone.

## Key concepts I learned

- **Thought:** The LLM explains its reasoning before taking an action. This makes the agent transparent — you can see WHY it chose a specific tool.
- **Action:** The LLM picks a tool to call and provides the parameters. This is the "acting" part — actually doing something in the real world.
- **Observation:** The result that comes back from the tool. The LLM reads this and decides what to do next.
- **Scratchpad / Trace:** The full history of Thought/Action/Observation steps accumulated during one task. The LLM sees its own reasoning history so it can build on previous steps.
- **Grounding:** By interacting with real tools (APIs, databases), the LLM stays grounded in reality instead of hallucinating answers.

## How I implemented it in Kaashvi

### Core files:
- `agent/react_loop.py` — The main ReAct loop engine
- `agent/tools.py` — Tool base class, tool registry

### Key functions:
- `run_agent()` — Contains the ReAct loop. Iterates up to MAX_ITERATIONS (10), each iteration the LLM produces a Thought/Action/Observation.
- `parse_action()` — Regex parser that extracts the Action name and Action Input (JSON parameters) from the LLM's raw text output.
- `build_system_prompt()` — System instructions that tell the LLM to follow the Thought/Action/Observation format and lists available tools.
- `TOOL_REGISTRY` — A list of all available tool instances. The loop searches this registry to find and execute the requested tool.

### How the loop works:
```
User sends message
  → LLM produces: Thought + Action + Action Input
  → parse_action() extracts the action name and params
  → If Action == FINAL_ANSWER → return the answer to user
  → Otherwise → find the tool in TOOL_REGISTRY, execute it
  → Append Thought + Action + Observation to scratchpad
  → Send scratchpad back to LLM for next iteration
  → Repeat until FINAL_ANSWER or MAX_ITERATIONS
```

## Before vs After

**Without ReAct (just an LLM):**
- User: "Am I free tomorrow at 3pm?"
- LLM: "I don't have access to your calendar." (or worse, hallucinated answer)

**With ReAct (Kaashvi):**
- Thought: "The user wants to know if they're free. I should check their calendar."
- Action: find_free_time
- Observation: "You have a meeting 2-4pm"
- Thought: "They have a meeting during that time. I should tell them."
- Action: FINAL_ANSWER
- Answer: "You're not free at 3pm — you have a meeting from 2-4pm."

## What I would improve next
- **Phase C1:** Re-audit the ReAct loop against the paper. Fix parse_action regex for edge cases, add error retry when a tool fails.
- **Phase C2:** Add a planning step — for complex queries, generate a plan first, then execute step by step (Plan-and-Solve paper).
- **Phase C4:** Improve tool descriptions so the LLM picks the right tool more often (Toolformer paper).
