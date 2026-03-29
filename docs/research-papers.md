# Research Papers — Overview

This document tracks all the research papers I studied while building Kaashvi, and how each paper's concepts were implemented in the codebase.

## Completed Papers

| # | Paper | Year | Key Concept | Implemented In |
|---|-------|------|-------------|----------------|
| 1 | [ReAct](react-paper.md) | Yao 2023 | Reasoning + Acting loop (Thought/Action/Observation) | `agent/react_loop.py` |
| 2 | [MemGPT](memgpt-paper.md) | Packer 2023 | Memory tiers — RAM + hard drive for LLM context management | `agent/react_loop.py`, `integrations/memory_tools.py`, `main.py` |

## Upcoming Papers

| # | Paper | Phase | What I'll Learn |
|---|-------|-------|-----------------|
| 3 | Attention Is All You Need (Vaswani 2017) | B1 | Transformer architecture, self-attention |
| 4 | GPT-3: Few-Shot Learners (Brown 2020) | B2 | In-context learning, few-shot examples |
| 5 | Chain-of-Thought (Wei 2022) | B3 | Step-by-step reasoning |
| 6 | InstructGPT (Ouyang 2022) | B4 | RLHF, why system prompts work |
| 7 | BERT (Devlin 2018) | B5 | Embeddings, semantic understanding |
| 8 | Plan-and-Solve (Wang 2023) | C2 | Planning before acting |
| 9 | Toolformer (Schick 2023) | C4 | Better tool selection |
| 10 | Reflexion (Shinn 2023) | E2 | Self-evaluation and improvement |
| 11 | RAG (Lewis 2020) | F1 | Retrieval Augmented Generation |
| 12 | Tree of Thoughts (Yao 2023) | G1 | Multiple reasoning paths |
| 13 | Voyager (Wang 2023) | G2 | Learning from experience |

## How Papers Connect

```
Attention Is All You Need (foundation)
    └── GPT-3 (scaling + few-shot)
         ├── InstructGPT (RLHF + instruction following)
         ├── Chain-of-Thought (step-by-step reasoning)
         │    └── ReAct (reasoning + tool use) ← IMPLEMENTED
         │         └── Plan-and-Solve (planning before acting)
         │              └── Tree of Thoughts (multiple plans)
         └── BERT (embeddings)
              └── RAG (retrieval with embeddings)

MemGPT (memory management) ← IMPLEMENTED
    ├── Uses: ReAct loop for control flow
    ├── Uses: RAG concepts for memory search
    └── Future: Recursive summarization, semantic search
```
