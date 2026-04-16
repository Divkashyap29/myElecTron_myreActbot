# MemGPT — "Towards LLMs as Operating Systems" (Packer 2023)

## What the paper is about
MemGPT treats an LLM like an operating system, giving it the ability to manage its own memory. Just like a computer uses RAM (fast, limited) and a hard drive (slow, unlimited) together, MemGPT creates a memory hierarchy where the LLM's context window acts as RAM and external storage acts as the hard drive. The LLM decides what to keep in context, what to archive, and what to retrieve — enabling unlimited conversation length without losing important information.

## Key concepts I learned

### Three Types of Context
1. **System Instructions (Read Only):** The base prompt telling the LLM who it is, what tools it has, and how to behave. Never changes during a conversation.
2. **Conversational Context (Read Only, FIFO eviction):** The history of recent messages. When it gets too long, the oldest messages are evicted first (First In, First Out). Evicted messages can be summarized before removal.
3. **Working Context (Writable):** A scratchpad the agent writes to during a task. The LLM can update this via function calls.

### Memory Tiers
| Tier | Computer Analogy | Speed | Size | Kaashvi Implementation |
|------|-----------------|-------|------|----------------------|
| Main Context | RAM | Fast (directly visible to LLM) | Limited by token window | `conversation_history` list |
| External Context | Hard Drive | Slow (must be searched/loaded) | Unlimited | `memory_archive.json` file |

### Control Flow
- **Events trigger inference:** The LLM only runs when something happens (user message, timer, system notification).
- **Function chaining:** The LLM can call multiple tools in sequence without returning to the user, building up context through each call.
- **Yield/Return control:** The LLM uses a flag (like FINAL_ANSWER) to signal "I'm done, give the response back to the user."

### Evaluation Criteria
1. **Consistency:** Can the agent remember facts, preferences, and events from past conversations? Tested with the Deep Memory Retrieval (DMR) task — ask about something from 5 conversations ago.
2. **Engagingness:** Does the agent use memory to personalize responses? Tested with the Conversation Opener task — does the agent reference things it learned about the user?

### Nested Key-Value Retrieval
MemGPT can chain multiple memory lookups together (multi-hop retrieval). If searching for key A returns key B, and key B returns key C, MemGPT keeps searching until it finds the final answer. Regular GPT-4 fails after 2-3 hops, but MemGPT with GPT-4 handles unlimited nesting.

## How I implemented it in Kaashvi

### Core files:
- `agent/react_loop.py` — Token counting, history trimming, archive management
- `integrations/memory_tools.py` — SearchMemoryTool for searching archived conversations
- `main.py` — Conversation history persistence (RAM for CLI, JSON file for Electron)

### Key functions:

**`count_tokens(conversation_history)`**
Estimates the token count of the conversation history using the approximation: 1 token = 4 characters. This tells us when the context window is getting full.

**`trim_history(conversation_history, max_tokens=10000, archive_path='memory_archive.json')`**
The FIFO eviction policy. When conversation history exceeds the token limit:
1. Loads the existing archive from disk
2. Removes the oldest user-assistant message pair
3. Saves the removed messages to the archive file
4. Repeats until under the limit
5. Returns the trimmed history

This ensures old messages are never lost — they move from main context (RAM) to external context (hard drive).

**`SearchMemoryTool.execute(query)`**
A tool Kaashvi can call to search through archived conversations:
1. Loads `memory_archive.json`
2. Searches each message for the query keyword (case-insensitive)
3. Returns the last 10 matching messages
4. Returns "No memories found" if nothing matches

This enables multi-hop retrieval — Kaashvi can search, get a result, search again based on that result, and chain lookups together using the ReAct loop.

### Conversation persistence:

**CLI mode (`main.py`):**
- History lives in a Python list variable (`history = []`)
- Persists during the session (while the program runs)
- Lost when the user quits — this is RAM behavior

**Electron mode (`main.py`):**
- History is saved to `conversation_history.json` after every turn
- Loaded from the file at the start of every turn
- Persists across app restarts — this is hard drive behavior

### Architecture diagram:
```
User sends message
     |
     v
[Load conversation_history]  ← from RAM (CLI) or JSON file (Electron)
     |
     v
[Append new user message]
     |
     v
[trim_history()]  ← if too long, evict oldest to memory_archive.json
     |
     v
[run_agent() / ReAct loop]
     |
     ├── LLM calls search_memory tool → searches memory_archive.json
     ├── LLM calls calendar/notion tools → external APIs
     └── LLM says FINAL_ANSWER → return response
     |
     v
[Append assistant response to history]
     |
     v
[Save updated history]  ← to RAM (CLI) or JSON file (Electron)
```



## What I would improve next
- **Phase D1 (Recursive Summarization):** Instead of just archiving old messages raw, summarize them first. "Turns 1-10 summary: User lives in Fredericton, has a friend named Sanskriti, likes butter chicken." This saves even more tokens.
- **Phase D2 (Accurate Token Counting):** Replace the character/4 approximation with Anthropic's actual token counter for precise measurements.
- **Phase D3 (Model Routing):** Use a smaller/cheaper model (Haiku) for simple tasks like echo and memory search, save the expensive model (Sonnet) for complex reasoning.
- **Phase F1 (RAG):** Replace keyword search with semantic/embedding-based search, so "What does my buddy like to eat?" matches "My friend Sanskriti loves painting" even without exact keyword overlap.
