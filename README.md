# Kaashvi

A personal AI agent built from scratch using Python and the Anthropic API. No frameworks. Each capability comes from reading, understanding, and implementing a research paper. 18 papers total, from Transformers to multi-agent coordination.

For detailed explanations of how each component works, see [docs/project-notes.md](docs/project-notes.md). For deep dives into individual papers, see [docs/react-paper.md](docs/react-paper.md) and [docs/memgpt-paper.md](docs/memgpt-paper.md).

## Completed Papers

| # | Paper | Year | Key Concept | Implemented In |
|---|-------|------|-------------|----------------|
| 1 | [ReAct](docs/react-paper.md) | Yao 2023 | Reasoning + Acting loop (Thought/Action/Observation) | `agent/react_loop.py` |
| 2 | [MemGPT](docs/memgpt-paper.md) | Packer 2023 | Memory tiers — RAM + hard drive for LLM context management | `agent/react_loop.py`, `integrations/memory_tools.py`, `main.py` |

## Upcoming Papers

| # | Paper | Year | Phase | What I'll Learn | What It Adds to Kaashvi |
|---|-------|------|-------|-----------------|-------------------------|
| 3 | Attention Is All You Need | Vaswani 2017 | B1 | Transformer architecture, self-attention | Foundational understanding of how every LLM works |
| 4 | GPT-3: Few-Shot Learners | Brown 2020 | B2 | In-context learning, few-shot examples | Better prompt engineering with few-shot examples |
| 5 | Chain-of-Thought | Wei 2022 | B3 | Step-by-step reasoning | Improved reasoning quality in the ReAct loop |
| 6 | InstructGPT | Ouyang 2022 | B4 | RLHF, why system prompts work | Understanding why Kaashvi follows instructions |
| 7 | BERT | Devlin 2018 | B5 | Embeddings, semantic understanding | Foundation for all embedding-based features |
| 8 | Sentence-BERT | Reimers 2019 | F2 | Sentence-level embeddings, semantic similarity | Semantic task matching, smarter memory search |
| 9 | Plan-and-Solve | Wang 2023 | C2 | Planning before acting | Kaashvi plans multi-step tasks before executing |
| 10 | Toolformer | Schick 2023 | C4 | Self-taught tool selection | Kaashvi picks the right tool more often |
| 11 | Reflexion | Shinn 2023 | E2 | Self-evaluation and retry | Kaashvi detects its own mistakes and corrects them |
| 12 | RAG | Lewis 2020 | F1 | Retrieval Augmented Generation | Semantic memory search replaces keyword search |
| 13 | Tree of Thoughts | Yao 2023 | G1 | Multiple reasoning paths | Kaashvi explores several plans and picks the best one |
| 14 | Voyager | Wang 2023 | G2 | Learning from experience, skill library | Kaashvi remembers successful strategies and reuses them |
| 15 | Isolation Forest | Liu 2008 | H4 | Unsupervised anomaly detection | Detects when schedule deviates from healthy patterns |
| 16 | Generative Agents | Park 2023 | J1 | Multi-agent simulation, agent-to-agent communication | Two Kaashvi instances coordinate between users |
| 17 | Cognitive Load Theory | Sweller 1988 | H1 | Mental effort measurement, intrinsic vs extraneous load | Behavioral proxy model for cognitive load without wearables |
| 18 | Contextual Bandits | Li 2010 | H5 | Online learning, exploration vs exploitation | Learns the best moment to send notifications |

## Roadmap

```
PHASE 0 — FOUNDATION (DONE)
|
|   Phase 1: ReAct Loop ................................. DONE
|   Phase 2: Google Calendar (4 tools) .................. DONE
|   Phase 3: Notion (2 tools) ........................... DONE
|   Phase 4: Electron Desktop App ....................... DONE
|   Phase A1: MemGPT Conversation Memory ................ DONE
|
v
PHASE B — PROMPT ENGINEERING AND THEORY
|
|   B1: Attention Is All You Need ..... understand transformers
|   B2: GPT-3 Few-Shot ............... few-shot prompt examples
|   B3: Chain-of-Thought ............. step-by-step reasoning
|   B4: InstructGPT .................. RLHF, instruction tuning
|   B5: BERT ......................... embeddings foundation
|
v
PHASE C — AGENT INTELLIGENCE
|
|   C1: ReAct audit .................. fix edge cases, error retry
|   C2: Plan-and-Solve ............... plan before acting
|   C4: Toolformer ................... smarter tool selection
|
v
PHASE D — MEMORY UPGRADES
|
|   D1: Recursive Summarization ...... summarize old messages before archiving
|   D2: Accurate Token Counting ...... replace char/4 with real tokenizer
|   D3: Model Routing ................ Haiku for simple tasks, Sonnet for reasoning
|
v
PHASE E — SELF-IMPROVEMENT
|
|   E2: Reflexion .................... detect and fix own mistakes
|
v
PHASE F — SEMANTIC UNDERSTANDING
|
|   F1: RAG .......................... embedding-based memory retrieval
|   F2: Sentence-BERT ................ semantic similarity for task matching
|   F3: ChromaDB Vector Store ........ replace JSON files with vector database
|
v
PHASE G — ADVANCED REASONING
|
|   G1: Tree of Thoughts ............. explore multiple reasoning paths
|   G2: Voyager ...................... learn from experience, skill library
|
v
PHASE H — ML PIPELINE
|
|   H1: Cognitive Load Model ......... typing cadence + task switching + calendar
|                                      density as behavioral proxies, real-time
|                                      score without wearables
|   H2: Productivity Predictor ....... trains on calendar + completion patterns,
|                                      predicts optimal deep work windows and
|                                      burnout risk 2 weeks ahead
|   H3: NLP Task Classifier .......... fine-tuned BERT reads Notion notes,
|                                      classifies by urgency, project, and
|                                      cognitive demand automatically
|   H4: Anomaly Detection ............ Isolation Forest detects schedule
|                                      deviations from healthy patterns,
|                                      proactively suggests restructuring
|   H5: Intervention Timing .......... contextual bandits learn the exact
|                                      moment you are most receptive to a
|                                      notification based on behavioral signals
|   H6: Semantic Task Matching ....... embedding model surfaces related past
|                                      tasks and relevant context when you
|                                      start something new
|
v
PHASE I — SYSTEM ARCHITECTURE
|
|   I1: SQLite + ChromaDB ............ local-first storage, zero cloud dependency
|   I2: Encrypted Storage ............ AES-256, all personal data stays private
|   I3: localhost REST API ............ other tools can query schedule and task state
|   I4: Rust Background Daemon ........ syncs Calendar and Notion every 5 minutes,
|                                      processes new data through ML pipeline silently
|   I5: Plugin System ................ extensible architecture, anyone can add
|                                      Slack, Linear, GitHub Issues via plugins
|
v
PHASE J — MULTI-AGENT COORDINATION
|
|   J1: Generative Agents ............ two Kaashvi instances negotiate meeting
|                                      times, surface shared context, identify
|                                      dependency conflicts between users
|
v
PHASE K — RESEARCH AND PUBLICATION
|
|   K1: Study Design ................. controlled study, 50 UNB students,
|                                      25 use Kaashvi vs 25 manual planning
|   K2: Data Collection .............. measure tasks completed, deadline misses,
|                                      deep work hours, stress levels
|   K3: Analysis and Paper ........... statistical analysis, write findings
|   K4: CHI Submission ............... submit to Conference on Human Factors
|                                      in Computing Systems
|   K5: Cognitive Load Paper ......... behavioral proxy measurement published
|                                      as a separate methodology paper
|
v
PHASE L — PRODUCTION
|
|   L1: Installers ................... .dmg / .exe / .AppImage
|   L2: Auto-Update System ........... seamless updates
|   L3: Open Source ................... public repo with plugin documentation
|   L4: Sentry Crash Reporting ........ production error tracking
```

## How Papers Connect

```
Attention Is All You Need (foundation)
    |
    v
GPT-3 (scaling + few-shot)
    |
    +---> InstructGPT (RLHF + instruction following)
    |
    +---> Chain-of-Thought (step-by-step reasoning)
    |         |
    |         v
    |     ReAct (reasoning + tool use) <--- IMPLEMENTED
    |         |
    |         +---> Plan-and-Solve (planning before acting)
    |         |         |
    |         |         v
    |         |     Tree of Thoughts (multiple plans)
    |         |
    |         +---> Reflexion (self-evaluation + retry)
    |         |
    |         +---> Voyager (learning from experience)
    |
    +---> BERT (embeddings)
              |
              +---> Sentence-BERT (sentence-level similarity)
              |         |
              |         v
              |     Semantic Task Matching (H6)
              |
              +---> RAG (retrieval with embeddings)
                        |
                        v
                    ChromaDB Vector Store (F3)

MemGPT (memory management) <--- IMPLEMENTED
    |
    +---> Uses: ReAct loop for control flow
    +---> Uses: RAG for semantic memory search
    +---> Future: Recursive summarization (D1)
    +---> Future: ChromaDB replaces JSON archive (F3)

Cognitive Load Theory (behavioral science)
    |
    +---> Cognitive Load Model (H1)
    +---> Productivity Predictor (H2)
    +---> Intervention Timing via Contextual Bandits (H5)

Isolation Forest (unsupervised ML)
    |
    +---> Anomaly Detection on schedule patterns (H4)

Generative Agents (multi-agent systems)
    |
    +---> Multi-Agent Coordination (J1)
```

## Final Vision

When all phases are complete, Kaashvi is a personal AI agent with:

**Intelligence**
1. ReAct reasoning loop with planning, self-evaluation, and learning from experience
2. Tree of Thoughts exploration for complex decisions
3. Skill library that remembers successful strategies and reuses them

**Integrations**
4. Google Calendar management (create, list, delete events, find free time)
5. Notion integration (create pages, search, auto-classify tasks by urgency and cognitive demand)
6. Plugin system for Slack, Linear, GitHub Issues, and anything else

**Memory**
7. Semantic memory search powered by embeddings and ChromaDB vectors
8. Recursive summarization of old conversations
9. Semantic task matching that surfaces related past work when you start something new

**ML Models**
10. Cognitive load measurement from behavioral signals (no wearables needed)
11. Personal productivity predictor trained on your own patterns (deep work windows, burnout risk)
12. Anomaly detection on schedule health
13. Intervention timing model that learns when you are most receptive

**Architecture**
14. Local-first, zero cloud dependency (SQLite + ChromaDB)
15. AES-256 encrypted storage for all personal data
16. Rust background daemon syncing data and running ML pipeline silently
17. localhost REST API so other tools can query your state

**Multi-Agent**
18. Two Kaashvi instances coordinate between users (negotiate meetings, surface shared context, detect dependency conflicts)

**Research**
19. Controlled study with 50 UNB students, published results
20. Behavioral cognitive load measurement published as methodology paper
21. Submitted to CHI (Conference on Human Factors in Computing Systems)

**Production**
22. Desktop app with .dmg / .exe / .AppImage installers
23. Auto-update system
24. Open source with plugin documentation
25. Sentry crash reporting

## Setup

Requires Python 3.10+, an Anthropic API key, Google Calendar API credentials, and a Notion integration token. Create a .env file with your API keys and run main.py to start the CLI, or cd into desktop/ and run npm start for the Electron app.
