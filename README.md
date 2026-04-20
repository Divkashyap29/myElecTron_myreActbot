# Kaashvi

A personal AI agent built from scratch using Python and the Anthropic API. No frameworks. Each capability comes from reading, understanding, and implementing a research paper. 25 papers total (and growing), from Transformers to multi-agent coordination, with a benchmark suite that measures improvement after every paper.

**24 tools** across 9 categories: Calendar, Gmail, Notion, Memory, Web Search, Weather, File System, Tasks/Reminders, and Shell.

For detailed explanations of how each component works, see [docs/project-notes.md](docs/project-notes.md). For deep dives into individual papers, see [docs/react-paper.md](docs/react-paper.md) and [docs/memgpt-paper.md](docs/memgpt-paper.md).

## Current Capabilities

| Category | Tools | Description |
|----------|-------|-------------|
| Google Calendar | `calendar_create_event`, `calendar_list_events`, `calendar_delete_event`, `calendar_find_free_time` | Full calendar management |
| Gmail | `gmail_send`, `gmail_read`, `gmail_search` | Send, read inbox, search emails |
| Notion | `notion_create_page`, `notion_search` | Create pages, search workspace |
| Memory | `search_memory` | Search archived conversations (MemGPT) |
| Web Search | `web_search` | DuckDuckGo search (no API key needed) |
| Weather | `get_weather` | Current weather via wttr.in (no API key needed) |
| File System | `read_file`, `write_file`, `list_files` | File ops with path traversal protection |
| Reminders | `set_reminder`, `list_reminders`, `check_reminders` | Persistent reminders (JSON storage) |
| Tasks | `add_task`, `list_tasks`, `complete_task`, `delete_task` | Persistent to-do list (JSON storage) |
| Shell | `run_command` | Execute commands with safety blocklist |
| Testing | `echo` | Echo tool for testing |

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
| 19 | SMALLBENCH / AgentBench | Various 2023 | M1 | Agent evaluation methodology, benchmark design | 50-task benchmark suite that measures Kaashvi before and after each paper |
| 20 | Prompt Injection Attacks | Perez 2022 | C5 | Adversarial attacks on LLMs, input sanitization | Guardrails so Kaashvi cannot be hijacked through calendar titles or Notion pages |
| 21 | Constitutional AI | Bai 2022 | C6 | Self-supervised safety, harmlessness training | Kaashvi self-checks outputs for harmful or biased content |
| 22 | Whisper | Radford 2022 | P2 | Speech-to-text, audio processing | Voice input so you can talk to Kaashvi instead of typing |
| 23 | LLaVA | Liu 2023 | P3 | Vision-language models, image understanding | Kaashvi can understand screenshots, photos, diagrams |
| 24 | MediaPipe | Lugaresi 2019 | R1 | Real-time face mesh, hand tracking, pose estimation | Face detection + head pose for gaze tracking in invigilate mode |
| 25 | YOLOv8 | Jocher 2023 | R3 | Real-time object detection | Detect phone in webcam frame during focus sessions |

## Roadmap

```
PHASE 0 — FOUNDATION (DONE)
|
|   Phase 1: ReAct Loop ................................. DONE
|   Phase 2: Google Calendar (4 tools) .................. DONE
|   Phase 3: Notion (2 tools) ........................... DONE
|   Phase 4: Electron Desktop App ....................... DONE
|   Phase A1: MemGPT Conversation Memory ................ DONE
|   Phase A2: Tool Expansion (8 → 24 tools) ............. DONE
|       Gmail (3), Web Search (1), Weather (1),
|       File System (3), Reminders (3), Tasks (4), Shell (1)
|
v
PHASE B — PROMPT ENGINEERING AND THEORY
|
|   B1: Attention Is All You Need ..... understand transformers .........DONE 
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
|   C5: Prompt Injection Defense ..... sanitize tool inputs and outputs,
|                                      prevent hijacking through calendar
|                                      event titles, Notion page content,
|                                      or crafted user messages
|   C6: Constitutional AI ............ self-check outputs for harmful,
|                                      biased, or hallucinated content
|                                      before returning to user
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
|   F4: Hugging Face Ecosystem ....... Hub, Transformers library, Inference
|                                      SDK, open source model hosting,
|                                      practical tooling for all embedding
|                                      and fine-tuning work
|   F5: Chunking Strategies .......... how to split documents for RAG,
|                                      fixed-size vs semantic vs recursive
|                                      splitting, overlap tuning
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
|   H7: Fine-Tuning .................. train a model on your own data,
|                                      required for H3 task classifier,
|                                      learn LoRA and full fine-tuning
|                                      using Hugging Face Transformers
|
v
PHASE P — MULTIMODAL AI
|
|   P1: Image Generation ............. DALL-E or Stable Diffusion, Kaashvi
|                                      can generate visuals on request
|   P2: Speech-to-Text ............... Whisper integration, voice input
|                                      so you can talk to Kaashvi
|   P3: Image Understanding .......... LLaVA or OpenAI Vision, Kaashvi
|                                      can read screenshots, photos,
|                                      diagrams and reason about them
|   P4: Text-to-Speech ............... Kaashvi speaks responses aloud,
|                                      hands-free interaction mode
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
|   I6: Local LLM Fallback ........... Ollama integration so Kaashvi runs
|                                      100% offline, zero cloud dependency,
|                                      automatic fallback when API is down
|
v
PHASE J — MULTI-AGENT COORDINATION
|
|   J1: Generative Agents ............ two Kaashvi instances negotiate meeting
|                                      times, surface shared context, identify
|                                      dependency conflicts between users
|
v
PHASE K — STREAMING AND VISUALIZATION
|
|   K1: Streaming Thought Visualizer .. render Thought/Action/Observation loop
|                                       live in the Electron UI as it happens,
|                                       real-time token-by-token display with
|                                       collapsible reasoning trace
|
v
PHASE Q — 3D COMPANION AND DESKTOP WIDGET
|
|   Q1: Desktop Overlay ............... transparent, frameless, always-on-top
|                                       Electron window that floats over the
|                                       desktop like a widget, not a full app
|                                       window, click-through background,
|                                       draggable mascot
|   Q2: 3D Mascot with Three.js ....... replace static cat image with a 3D
|                                       model using Three.js or React Three
|                                       Fiber, rendered live in Electron,
|                                       idle animations (breathing, blinking,
|                                       floating)
|   Q3: Emotion State Machine ......... mascot changes expression based on
|                                       agent state: thinking (eyes closed),
|                                       happy (solved a task), confused (tool
|                                       error), listening (user typing),
|                                       excited (greeting), sleeping (idle),
|                                       uses blend shapes / morph targets
|                                       for smooth transitions
|   Q4: Framer Motion Animations ...... spring-based physics animations for
|                                       all UI elements, chat bubbles slide
|                                       in, mascot bounces on interaction,
|                                       gesture support (drag, tap, hover)
|   Q5: Spline or Rive Integration .... design the 3D mascot in Spline (3D
|                                       design tool) or Rive (animation
|                                       engine), export directly to web,
|                                       interactive triggers tied to agent
|                                       events
|   Q6: Mini Mode ..................... collapsed state where only the mascot
|                                       floats on screen, expands into full
|                                       chat on click, system tray icon,
|                                       notification badges
|
v
PHASE R — INVIGILATE MODE (FOCUS GUARDIAN)
|
|   R1: Face Detection + Head Pose .... MediaPipe face mesh through webcam,
|                                       detect if user is facing the screen
|                                       or turned away, head angle estimation
|   R2: Gaze Tracking ................ estimate where the user is looking,
|                                       screen vs away vs phone vs window,
|                                       uses MediaPipe iris landmarks
|   R3: Phone Detection (YOLO) ....... YOLOv8 object detection on webcam
|                                       feed, detect phone in hand or on
|                                       desk being used, trained on custom
|                                       dataset if needed
|   R4: Distraction Classifier ....... combines head pose + gaze + phone
|                                       detection + app switching into a
|                                       single focus score (0 to 100),
|                                       threshold triggers alert
|   R5: Alert System ................. mascot reacts (angry/concerned face),
|                                       plays notification sound, shows
|                                       message like "Hey, you said you
|                                       wanted to study until 6pm. Get
|                                       back to it!", customizable tone
|                                       (gentle, firm, playful)
|   R6: Focus Session Manager ........ user starts invigilate mode with a
|                                       timer ("Study for 2 hours"), Kaashvi
|                                       tracks focus percentage over the
|                                       session, shows summary at the end
|                                       ("You were focused 78% of the time,
|                                       distracted 3 times by phone")
|   R7: Privacy Controls ............. camera only active when user enables
|                                       invigilate mode, no frames saved to
|                                       disk, no data leaves the machine,
|                                       all processing happens locally with
|                                       MediaPipe and YOLO, clear indicator
|                                       light when camera is active
|   R8: Focus Analytics .............. over time builds a profile of when
|                                       you focus best, what distracts you
|                                       most, feeds into H1 cognitive load
|                                       model and H2 productivity predictor
|
v
PHASE L — RESEARCH AND PUBLICATION
|
|   L1: Study Design ................. controlled study, 50 UNB students,
|                                      25 use Kaashvi vs 25 manual planning
|   L2: Data Collection .............. measure tasks completed, deadline misses,
|                                      deep work hours, stress levels
|   L3: Analysis and Paper ........... statistical analysis, write findings
|   L4: CHI Submission ............... submit to Conference on Human Factors
|                                      in Computing Systems
|   L5: Cognitive Load Paper ......... behavioral proxy measurement published
|                                      as a separate methodology paper
|   L6: arXiv-Style Writeup .......... 4-page PDF in /paper/kaashvi.pdf
|                                      describing methodology, architecture,
|                                      and evaluation results, signals research
|                                      maturity even before formal publication
|
v
PHASE M — EVALUATION AND BENCHMARKS
|
|   M1: Evaluation Harness ........... 50 real tasks (calendar management,
|                                      Notion queries, multi-step planning),
|                                      automated test runner that measures
|                                      success rate before and after each
|                                      paper implementation
|   M2: Memory Benchmark ............. controlled comparison of MemGPT-style
|                                      tiered memory vs baseline (no memory)
|                                      on recall tasks, numbers not claims
|   M3: Progress Graphs .............. "ReAct loop: 67% -> Reflexion: 89%
|                                      task completion" visualized over time,
|                                      this is a research contribution
|
v
PHASE N — PRODUCTION
|
|   N1: Installers ................... .dmg / .exe / .AppImage
|   N2: Auto-Update System ........... seamless updates
|   N3: Open Source ................... public repo with plugin documentation
|   N4: Sentry Crash Reporting ........ production error tracking
```

## System Architecture

This is the full architecture of Kaashvi when all phases are complete. Today it is a Python script calling an API. By the end it is a multi-process, multi-layer system with real-time streaming, 3D rendering, ML inference, and inter-agent communication.

### Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│                        ELECTRON APP (Renderer)                      │
│                                                                     │
│  ┌─────────────────┐  ┌──────────────────┐  ┌───────────────────┐  │
│  │    Chat UI       │  │  3D Companion    │  │  Thought Stream   │  │
│  │    React +       │  │  Three.js /      │  │  Live Thought /   │  │
│  │    Framer Motion │  │  React Three     │  │  Action / Obs     │  │
│  │                  │  │  Fiber + Spline  │  │  visualizer       │  │
│  └────────┬─────────┘  └────────┬─────────┘  └────────┬──────────┘  │
│           │                     │                      │             │
│  ┌────────▼─────────────────────▼──────────────────────▼──────────┐  │
│  │              WebSocket (real-time streaming)                    │  │
│  └────────────────────────────┬───────────────────────────────────┘  │
└───────────────────────────────┼──────────────────────────────────────┘
                                │
┌───────────────────────────────▼──────────────────────────────────────┐
│                      LOCALHOST REST API + WebSocket Server            │
│                                                                      │
│  ┌────────────┐  ┌────────────┐  ┌──────────────┐  ┌─────────────┐  │
│  │ Rate       │  │ Auth +     │  │ Circuit      │  │ Request     │  │
│  │ Limiter    │  │ CORS       │  │ Breaker      │  │ Router      │  │
│  │            │  │ Headers    │  │              │  │             │  │
│  │ Budget per │  │ localhost  │  │ Anthropic    │  │ /agent      │  │
│  │ API (hourly│  │ only, no   │  │ down? route  │  │ /calendar   │  │
│  │ + daily)   │  │ external   │  │ to Ollama    │  │ /notion     │  │
│  │            │  │ access     │  │ fallback     │  │ /memory     │  │
│  └────────────┘  └────────────┘  └──────────────┘  │ /ml         │  │
│                                                     │ /status     │  │
│                                                     └─────────────┘  │
└──────────────┬──────────────┬──────────────┬─────────────────────────┘
               │              │              │
     ┌─────────▼────┐  ┌─────▼──────┐  ┌────▼─────────────┐
     │ AGENT CORE   │  │ ML WORKERS │  │ RUST DAEMON      │
     │ (Python)     │  │ (Python)   │  │ (Background)     │
     │              │  │            │  │                  │
     │ ReAct Loop   │  │ Cognitive  │  │ Calendar Sync    │
     │ Tool Registry│  │ Load Model │  │ Notion Sync      │
     │ Memory Mgr   │  │ Productiv- │  │ Plugin Sync      │
     │ Plan-and-    │  │ ity Pred   │  │ (Slack, Linear,  │
     │ Solve        │  │ Task Class │  │  GitHub Issues)   │
     │ Reflexion    │  │ Anomaly    │  │                  │
     │ Tree of      │  │ Detection  │  │ Runs every 5 min │
     │ Thoughts     │  │ Intervent- │  │ Feeds new data   │
     │ Voyager      │  │ ion Timing │  │ into ML pipeline │
     │ Safety       │  │            │  │                  │
     │ Checks       │  │ Runs on    │  │ IPC: stdin/stdout│
     │              │  │ separate   │  │ or Unix socket   │
     │              │  │ threads,   │  │                  │
     │              │  │ never      │  │                  │
     │              │  │ blocks UI  │  │                  │
     └──────┬───────┘  └─────┬──────┘  └────┬─────────────┘
            │                │              │
┌───────────▼────────────────▼──────────────▼──────────────────────────┐
│                          DATA LAYER                                  │
│                                                                      │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐               │
│  │   SQLite     │  │   ChromaDB   │  │   Redis /    │               │
│  │              │  │              │  │   In-Memory   │               │
│  │ Users        │  │ Embeddings   │  │   Cache       │               │
│  │ Tasks        │  │ Vectors      │  │              │               │
│  │ Events       │  │ Semantic     │  │ Calendar     │               │
│  │ Preferences  │  │ Search       │  │ results      │               │
│  │ Archived     │  │ Collections  │  │ Frequent     │               │
│  │ Conversations│  │              │  │ embeddings   │               │
│  │ Skill Library│  │              │  │ LLM response │               │
│  │ Benchmark    │  │              │  │ cache        │               │
│  │ Results      │  │              │  │              │               │
│  └──────────────┘  └──────────────┘  └──────────────┘               │
│                                                                      │
│  All encrypted with AES-256 at rest                                  │
│  All local, zero cloud storage                                       │
└──────────────────────────────────────────────────────────────────────┘
            │                │              │
┌───────────▼────────────────▼──────────────▼──────────────────────────┐
│                      EXTERNAL SERVICES                               │
│                                                                      │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐               │
│  │ LLM Layer    │  │ APIs         │  │ Asset CDN    │               │
│  │              │  │              │  │              │               │
│  │ Anthropic    │  │ Google       │  │ 3D Models    │               │
│  │ (primary)    │  │ Calendar     │  │ (.glb/.gltf) │               │
│  │      |       │  │              │  │              │               │
│  │      v       │  │ Notion       │  │ Textures     │               │
│  │ Ollama       │  │              │  │ (.webp)      │               │
│  │ (offline     │  │ Slack        │  │              │               │
│  │  fallback)   │  │ Linear       │  │ Audio Files  │               │
│  │      |       │  │ GitHub       │  │ (.mp3/.wav)  │               │
│  │      v       │  │ Issues       │  │              │               │
│  │ Hugging Face │  │              │  │ Mascot Anim  │               │
│  │ (embeddings  │  │              │  │ (.rive/.json)│               │
│  │  + fine-tune)│  │              │  │              │               │
│  │              │  │              │  │ Lazy loaded   │               │
│  │              │  │              │  │ + cached      │               │
│  └──────────────┘  └──────────────┘  └──────────────┘               │
└──────────────────────────────────────────────────────────────────────┘
```

### How Processes Communicate

```
┌──────────────┐    IPC (preload.js)     ┌──────────────┐
│ Electron     │◄───────────────────────►│ Node.js      │
│ Renderer     │    contextBridge        │ Main Process │
│ (UI, 3D)     │                         │              │
└──────────────┘                         └──────┬───────┘
                                                │
                          spawn / WebSocket     │
                                                │
                                         ┌──────▼───────┐
                                         │ Python       │
                                         │ Agent Server │
                                         │              │
                                         │ REST API on  │
                                         │ localhost:    │
                                         │ 8420         │
                                         └──────┬───────┘
                                                │
                              Unix socket /     │
                              stdin-stdout      │
                                                │
                                         ┌──────▼───────┐
                                         │ Rust Daemon  │
                                         │              │
                                         │ Background   │
                                         │ sync + ML    │
                                         │ data feed    │
                                         └──────────────┘
```

### Multi-Agent Communication

```
┌──────────────────┐                    ┌──────────────────┐
│ Kaashvi           │    Message Queue   │ Kaashvi           │
│ Instance A        │◄──(Pub/Sub)──────►│ Instance B        │
│ (User 1)          │                    │ (User 2)          │
│                   │                    │                   │
│ "User 1 needs     │   Negotiation     │ "User 2 is free   │
│  a meeting at 3pm"│──────────────────►│  at 3pm, confirm" │
│                   │                    │                   │
│ "Conflict: User 1 │   Dependency      │ "Task X depends   │
│  blocked on Task X"│◄─────────────────│  on User 1"       │
│                   │                    │                   │
│ Shared context:   │   Context Sync    │ Shared context:   │
│ Project deadline  │◄────────────────►│ Project deadline  │
│ is Friday         │                    │ is Friday         │
└──────────────────┘                    └──────────────────┘
         │                                       │
         └──────────┐               ┌────────────┘
                    │               │
              ┌─────▼───────────────▼─────┐
              │    Shared State Store      │
              │    (encrypted, synced)     │
              │                           │
              │    Meeting proposals      │
              │    Dependency graph        │
              │    Shared project context  │
              └───────────────────────────┘
```

### Data Flow: User Message to Response

```
User types message
       │
       ▼
[1] Electron Renderer sends via WebSocket
       │
       ▼
[2] API Gateway validates, rate checks
       │
       ▼
[3] Agent Core receives message
       │
       ├──► Append to conversation_history
       ├──► trim_history() if over token limit (archive to SQLite)
       ├──► count_tokens() for budget awareness
       │
       ▼
[4] ReAct Loop begins
       │
       ├──► LLM call (Anthropic → Ollama fallback → cached response)
       ├──► Stream tokens via WebSocket to UI (thought visualizer)
       ├──► Update mascot emotion state (thinking)
       │
       ├──► If Action == tool call:
       │       ├──► Safety check (prompt injection scan)
       │       ├──► Execute tool (Calendar / Notion / Memory / ML)
       │       ├──► Cache result if cacheable
       │       ├──► Observation back to scratchpad
       │       └──► Update mascot emotion (working)
       │
       ├──► If Action == FINAL_ANSWER:
       │       ├──► Safety check output (Constitutional AI)
       │       ├──► Append to conversation_history
       │       ├──► Save to SQLite
       │       ├──► Update mascot emotion (happy)
       │       └──► Stream response to UI
       │
       ▼
[5] Response displayed in chat, mascot reacts
```

### Asset Pipeline (3D Models + Multimodal)

```
Design Phase                    Build Phase                  Runtime

Spline / Blender               Export Pipeline               Electron App
┌────────────┐                ┌────────────────┐           ┌─────────────┐
│ 3D Mascot  │───export──────►│ .glb optimizer │──────────►│ Three.js    │
│ Model      │                │ Draco compress │           │ Renderer    │
│            │                │ Texture to     │           │             │
│ Blend      │                │ .webp          │           │ Lazy load   │
│ shapes for │                │                │           │ from local  │
│ emotions   │                │ Bundle size    │           │ cache or    │
│            │                │ target: <5MB   │           │ CDN         │
└────────────┘                └────────────────┘           └─────────────┘

Rive / After Effects          Audio Pipeline               Whisper
┌────────────┐                ┌────────────────┐           ┌─────────────┐
│ Animations │───export──────►│ .riv / Lottie  │──────────►│ Load into   │
│ Idle       │                │ files          │           │ renderer    │
│ Thinking   │                └────────────────┘           └─────────────┘
│ Happy      │
│ Confused   │                ┌────────────────┐           ┌─────────────┐
│ Sleeping   │                │ Whisper model  │──────────►│ Voice input │
└────────────┘                │ (~150MB, local)│           │ processing  │
                              └────────────────┘           └─────────────┘

                              ┌────────────────┐           ┌─────────────┐
                              │ TTS model      │──────────►│ Voice output│
                              │ (local)        │           │ processing  │
                              └────────────────┘           └─────────────┘
```

### System Design Concepts Used

| Concept | Where It Applies | Why |
|---------|-----------------|-----|
| WebSocket | Thought streaming, mascot state, chat | Real-time bidirectional, no polling |
| Circuit Breaker | LLM layer | Anthropic down? Ollama fallback. Ollama down? Cached response. |
| Rate Limiter | API Gateway | Budget control per API (Anthropic hourly/daily, Google quota) |
| Pub/Sub Message Queue | Multi-agent | Two Kaashvi instances communicate asynchronously |
| Worker Threads | ML inference | Heavy computation off main thread, UI never blocks |
| CDN / Local Cache | 3D assets, audio | Large files lazy-loaded and cached, not bundled in app |
| Event-Driven Architecture | Agent core | Agent only runs on events (user message, timer, calendar change, sync) |
| IPC (Inter-Process Comm) | Electron to Python to Rust | Three separate processes, each doing what its language is best at |
| CQRS | Data layer | Reads (search, list) and writes (create, update) through different paths |
| Cache-Aside Pattern | Calendar, embeddings | Check cache first, fetch from API on miss, store in cache |
| Encryption at Rest | SQLite, ChromaDB, archives | AES-256 on all local files, keys derived from user passphrase |
| Asset Pipeline | 3D models, textures | Draco compression, .webp textures, target <5MB total bundle |
| Graceful Degradation | Entire system | No API? Use Ollama. No GPU? CPU inference. No network? Cached data. |

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

AgentBench / SMALLBENCH (evaluation methodology)
    |
    +---> Evaluation Harness, 50 real tasks (M1)
    +---> Memory Benchmark, tiered vs baseline (M2)
    +---> Progress Graphs over time (M3)

Prompt Injection Attacks + Constitutional AI (safety)
    |
    +---> Input sanitization, output self-checking (C5, C6)
    +---> Prevents hijacking through tool inputs

Whisper (audio)
    |
    +---> Speech-to-Text, voice input (P2)
    +---> Text-to-Speech, spoken responses (P4)

LLaVA (vision-language)
    |
    +---> Image Understanding (P3)
    +---> Uses: BERT embeddings for visual grounding

Hugging Face (practical tooling)
    |
    +---> Hub + Transformers + Inference SDK (F4)
    +---> Enables: Fine-tuning (H7), Sentence-BERT (F2)
    +---> Enables: Chunking strategies for RAG (F5)

MediaPipe (real-time perception)
    |
    +---> Face Detection + Head Pose (R1)
    +---> Gaze Tracking via iris landmarks (R2)
    +---> Feeds into: Distraction Classifier (R4)
    +---> Feeds into: Cognitive Load Model (H1)

YOLOv8 (object detection)
    |
    +---> Phone Detection in webcam (R3)
    +---> Feeds into: Distraction Classifier (R4)

Distraction Classifier (R4)
    |
    +---> Combines: head pose + gaze + phone + app switching
    +---> Triggers: Alert System (R5)
    +---> Logs to: Focus Analytics (R8)
    +---> Feeds into: Productivity Predictor (H2)
```

## Final Vision

When all phases are complete, Kaashvi is a personal AI agent with:

### Intelligence

1. ReAct reasoning loop with planning, self-evaluation, and learning from experience
2. Tree of Thoughts exploration for complex decisions
3. Skill library that remembers successful strategies and reuses them

### Integrations

4. Google Calendar management (create, list, delete events, find free time)
5. Gmail (send, read, search emails)
6. Notion integration (create pages, search, auto-classify tasks by urgency and cognitive demand)
7. Web search (DuckDuckGo), weather (wttr.in), file management, tasks, reminders, shell
8. Plugin system for Slack, Linear, GitHub Issues, and anything else

### Memory

7. Semantic memory search powered by embeddings and ChromaDB vectors
8. Recursive summarization of old conversations
9. Semantic task matching that surfaces related past work when you start something new

### ML Models

10. Cognitive load measurement from behavioral signals (no wearables needed)
11. Personal productivity predictor trained on your own patterns (deep work windows, burnout risk)
12. Anomaly detection on schedule health
13. Intervention timing model that learns when you are most receptive

### Safety

14. Prompt injection defense, input and output sanitization across all tools
15. Constitutional AI self-checking for harmful, biased, or hallucinated content

### Architecture

16. Local-first, zero cloud dependency (SQLite + ChromaDB)
17. AES-256 encrypted storage for all personal data
18. Rust background daemon syncing data and running ML pipeline silently
19. localhost REST API so other tools can query your state
20. Local LLM fallback via Ollama, runs 100% offline when API is down
21. Hugging Face Transformers integration for fine-tuning and open source models

### Multimodal

22. Voice input via Whisper speech-to-text
23. Text-to-speech for hands-free spoken responses
24. Image understanding via LLaVA, reads screenshots, photos, diagrams
25. Image generation via DALL-E or Stable Diffusion

### Visualization

26. Streaming thought visualizer that renders Thought/Action/Observation live in the Electron UI as it happens

### 3D Companion

27. Floating desktop widget that hovers over all windows, draggable, always accessible
28. 3D animated mascot with idle animations (breathing, blinking, floating)
29. Emotion system that changes expression based on agent state (thinking, happy, confused, listening, sleeping)
30. Spring-based Framer Motion animations on all UI elements
31. Mini mode where only the mascot floats on screen, expands to full chat on click

### Invigilate Mode (Focus Guardian)

32. Webcam-based focus monitoring using MediaPipe face mesh and gaze tracking
33. Phone detection via YOLOv8 object detection on live webcam feed
34. Distraction classifier that combines head pose, gaze, phone, and app switching into a real-time focus score
35. Kaashvi mascot reacts with concerned expression and plays alert when you get distracted
36. Focus session manager with timer, focus percentage tracking, and end-of-session summary
37. Focus analytics that builds a profile of when you focus best and what distracts you most
38. All processing local, no frames saved to disk, camera only active when user enables it

### Multi-Agent

39. Two Kaashvi instances coordinate between users (negotiate meetings, surface shared context, detect dependency conflicts)

### Evaluation

40. 50-task benchmark suite measuring success rate before and after each paper implementation
41. Memory benchmark comparing tiered memory vs baseline on recall tasks
42. Progress graphs showing measurable improvement over time

### Research

43. Controlled study with 50 UNB students, published results
44. Behavioral cognitive load measurement published as methodology paper
45. Submitted to CHI (Conference on Human Factors in Computing Systems)
46. arXiv-style 4-page PDF describing methodology and evaluation results

### Production

47. Desktop app with .dmg / .exe / .AppImage installers
48. Auto-update system
49. Open source with plugin documentation
50. Sentry crash reporting

## Setup

Requires Python 3.10+, an Anthropic API key, Google Calendar API credentials, and a Notion integration token.

```bash
pip install anthropic python-dotenv google-auth-oauthlib google-api-python-client duckduckgo-search requests
```

Create a `.env` file with your API keys and run `python main.py` to start the CLI, or `cd desktop/ && npm start` for the Electron app.
