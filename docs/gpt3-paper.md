# GPT-3 — "Language Models are Few-Shot Learners" (Brown et al., 2020)

The paper that proved you don't need to train a model for every task. Just show it a few examples in the prompt and it figures it out. This is why Kaashvi can do calendar management, Notion search, and memory recall with just a system prompt — no fine-tuning, no custom training.

---

## The World Before GPT-3

Before this paper, if you wanted an AI to do sentiment analysis, you collected 10,000 labeled reviews, fine-tuned BERT on them, deployed it. If you then wanted it to also do translation? Collect ANOTHER dataset, fine-tune ANOTHER model. Every task = new data + new training.

GPT-3 said: what if one model could do everything, and you just tell it what you want in plain English?

This idea is called **prompt programming** — instead of writing code to teach the model, you write a prompt. That's literally what `build_system_prompt()` in Kaashvi is. I'm programming Claude's behavior through text, not through training.

---

## Architecture, Data, Compute

GPT-3 is a **decoder-only transformer** — the exact same architecture from "Attention Is All You Need" (B1), just scaled up to an insane degree.

```
Original Transformer (2017):     GPT-3 (2020):
- 6 layers                       - 96 layers
- 8 attention heads              - 96 attention heads
- 512 embedding dim              - 12,288 embedding dim
- 65M parameters                 - 175 BILLION parameters
```

The architecture didn't change. They literally just made it bigger. The Transformer design from Vaswani was so good that scaling it 1000x kept making it better.

### Training Data
Basically the entire internet:
- Common Crawl (filtered web pages) — 410 billion tokens
- WebText2 (Reddit links with 3+ karma)
- Books1 + Books2
- All of English Wikipedia

Total: ~300 billion tokens. The model saw more text during training than any human could read in a thousand lifetimes.

### Cost
- Trained on NVIDIA V100 GPU clusters
- Estimated cost: **$4.6 million** for one training run
- Took weeks

This is why we use APIs instead of training our own models. Claude (what Kaashvi uses) was even more expensive to train, but we just pay per API call.

---

## Zero-Shot, One-Shot, and Few-Shot Learning

This is THE most important section. This is what we're adding to Kaashvi.

### Zero-Shot (what Kaashvi does right now)
You describe the task but show no examples:
```
Translate English to French:
cheese =>
```

The model has to figure out what you want from the instruction alone. It works sometimes, but it can misunderstand the format or the task.

### One-Shot
You show ONE example before the real input:
```
Translate English to French:
sea otter => loutre de mer
cheese =>
```

Now the model sees a concrete example of the exact format. Input, arrow, output. It clicks.

### Few-Shot (2-5 examples)
You show a FEW examples:
```
Translate English to French:
sea otter => loutre de mer
peppermint => menthe poivrée
plush giraffe => girafe en peluche
cheese =>
```

Multiple examples reinforce the pattern. The model becomes very confident about what you want.

### Why does this work? (attention explanation)

The model's weights don't change. No training happens. So what's going on?

Remember self-attention from B1 — every token can attend to every other token. When the model generates the answer for "cheese =>":

1. Attention heads look BACK at the examples in the prompt
2. Head X notices: every line follows "English => French"
3. Head Y notices: words before `=>` are English, words after are French
4. Head Z notices: "cheese" is English, so it needs French after `=>`
5. Model generates "fromage"

The examples are **context for attention**, not training data. More examples = more evidence for the pattern = more reliable output. The transformer reads the examples the same way it reads any other text — through self-attention — but the examples happen to demonstrate exactly what you want.

### How this applies to Kaashvi

My system prompt right now is zero-shot. I tell the model the format:
```
Thought: <reasoning>
Action: <tool name>
Action Input: <JSON>
```

But I show ZERO examples of this being done correctly. The model sometimes picks the wrong tool, writes bad JSON, or forgets FINAL_ANSWER. Adding 2-3 real examples of Thought/Action/Observation traces will fix most of these problems because the model will have seen the pattern executed, not just described.

---

## Scaling Laws (The Power-Law Chart)

One of the most famous charts in AI history. It shows: as you increase model size, performance improves on a **smooth, predictable curve**. It doesn't plateau — it just keeps going.

Key findings:
- 175B parameters crushes 1.3B on almost every task
- Few-shot performance scales BETTER than zero-shot with model size
- Small models can't do few-shot well — they don't have enough capacity to "learn from context"

This is why Kaashvi uses Claude Sonnet (a large model) instead of a tiny one. A tiny model wouldn't be able to follow the ReAct format reliably even with few-shot examples. With a large model, the few-shot examples make it almost perfect.

This is also relevant for Phase D3 on my roadmap (Model Routing) — use a smaller model like Haiku for simple tasks (echo, memory search) and save the expensive Sonnet for complex multi-step reasoning. The scaling law tells us that simple tasks don't NEED the big model.

---

## Results: Machine Translation

GPT-3 with few-shot prompting matched or beat supervised translation models on English to French — despite NEVER being trained for translation specifically. It learned translation patterns from internet text that happened to contain multilingual content.

On other language pairs (German, Romanian) it was weaker because the training data was mostly English.

The lesson: a general-purpose model with the right prompt can compete with specialists. This is why Kaashvi doesn't need a specialized "calendar scheduling model" — Claude with the right prompt handles it.

---

## Natural Language Inference (Reasoning is Hard)

NLI = given a premise and hypothesis, decide if the hypothesis is true, false, or neutral.

```
Premise: "A man is eating pizza"
Hypothesis: "A man is eating food"
Answer: Entailment (true — pizza is food)
```

GPT-3 struggled here. It could pattern-match but had trouble with multi-step logical reasoning. This was the weakest area.

This is exactly why Chain-of-Thought (B3, my next paper) matters. GPT-3 proved that raw pattern matching isn't enough for reasoning — you need to explicitly force the model to think step by step. The "Thought:" step in Kaashvi's ReAct loop is literally this fix. The ReAct paper came AFTER GPT-3 specifically to address this weakness.

---

## Arithmetic

GPT-3 on simple math:
- 2-digit addition: ~100% accuracy
- 3-digit addition: ~80%
- 4-5 digit addition: drops off hard

GPT-3 doesn't do math. It pattern-matches from seeing math in training data. For small numbers it's seen enough examples. For large numbers, it hasn't.

This is why Kaashvi uses **tools**. If someone asks "what time is my next meeting?" the LLM shouldn't guess — it should call `calendar_list_events` and get the real answer. The ReAct architecture (LLM for reasoning, tools for actions) exists because LLMs are fundamentally unreliable at factual lookups and computation. They're good at deciding WHAT to do, not at doing it.

---

## Word Unscrambling and SAT Analogies

**Word unscrambling:** GPT-3 was decent at "eealpl" => "appeal" with few-shot examples. Shows it has some understanding of word structure.

**SAT analogies:** GPT-3 scored 65% on SAT analogy questions. Average college applicant scores ~57%. This made headlines — "AI is smarter than college students!" But it's really just pattern matching from having read millions of texts that contain analogical reasoning.

Not directly relevant to Kaashvi, but shows how broad in-context learning is. The same mechanism that lets GPT-3 solve SAT analogies is what lets Kaashvi's ReAct loop choose the right tool.

---

## Fake News Generation

GPT-3 can generate news articles that humans can't distinguish from real ones:
- Small GPT-3 (125M params): humans detected fakes ~60% of the time
- Full GPT-3 (175B params): humans detected fakes only ~52% (basically coin flip)

The paper included this to be transparent about misuse. OpenAI was saying "this is powerful and potentially dangerous."

This is relevant to my roadmap:
- Phase C5 (Prompt Injection Defense) — if someone puts malicious text in a calendar event title, Kaashvi could be tricked
- Phase C6 (Constitutional AI) — self-check outputs before returning them to the user
- The more capable the model, the more important safety becomes

---

## Data Contamination

Big concern: did GPT-3 cheat by memorizing test questions?

If SAT questions or translation benchmarks were in Common Crawl (GPT-3's training data), then the "few-shot" results might be memorization, not learning. The paper checked for overlap and found some contamination existed, but performance was similar even on clean data.

Lesson for me: when I build Kaashvi's evaluation suite (Phase M1), I need to use my OWN personal test cases — real calendar queries, real Notion searches, real multi-step tasks. These are guaranteed to be unseen by Claude, so the benchmarks will be honest.

---

## Limitations (The Paper's Own Admission)

1. **Long coherent text** — starts strong, loses coherence after a few paragraphs
2. **Reasoning** — struggles with multi-step logical deduction → Chain-of-Thought (B3) fixes this
3. **Common sense physics** — "is cheese cold after being in the fridge?" sometimes fails
4. **Self-contradiction** — can assert X and then assert not-X → Reflexion (E2) catches this
5. **Sample efficiency** — humans learn from 1-2 examples, GPT-3 sometimes needs 50
6. **No learning after deployment** — weights frozen, can't learn from mistakes → Voyager (G2) saves successful strategies

Every limitation maps to a paper on my roadmap. GPT-3 showed the problems, and the next 5 years of research solved them one by one.

---

## Bias, Fairness, Broader Impact

GPT-3 learned from internet text, so it absorbed the internet's biases:

**Gender:** "He was a nurse" gets lower probability than "She was a nurse." "She was a CEO" gets lower probability than "He was a CEO." The model learned stereotypes from the data.

**Race:** Certain races associated with more negative sentiment words in model outputs.

**Religion:** Islam more frequently associated with violence in completions.

The paper didn't hide from this. They measured bias explicitly and published results, which was unusual and set a standard for responsible AI research.

For Kaashvi: this is why Phase C6 (Constitutional AI) is on the roadmap. When Kaashvi generates responses about people, scheduling, or priorities, bias from the underlying model could creep in. The system needs to self-check for harmful or biased content before showing it to the user.

---

## Final Thoughts: Are We Moving Toward AGI?

The paper's answer: no, but the scaling trend is interesting.

GPT-3 showed that bigger models + more data = emergent capabilities nobody designed. Translation, arithmetic, code generation — none of these were explicitly taught. They just appeared as the model got bigger.

What actually happened after this paper:
- GPT-4 confirmed scaling keeps working (way better at reasoning)
- Claude, Gemini, LLaMA followed the same decoder-only transformer playbook
- Chain-of-Thought (B3) partially fixed the reasoning weakness
- RLHF/InstructGPT (B4) made models follow instructions reliably
- The whole field of "AI agents" (including Kaashvi) became possible because models got good enough at following structured formats through in-context learning

---

## What I'm Taking from This Paper into Kaashvi

| GPT-3 Finding | What I'm Doing |
|---|---|
| Few-shot > zero-shot | Adding 2-3 examples to my system prompt for reliable tool selection |
| Bigger model = better in-context learning | Using Claude Sonnet, not a tiny model |
| LLMs can't do real math/lookups | Tools (calendar API, Notion API) for actions, LLM for reasoning only |
| Reasoning is the weakest area | Chain-of-Thought (B3) is my next paper |
| Bias exists in all outputs | Constitutional AI (C6) on the roadmap |
| Data contamination skews benchmarks | Using personal test cases for evaluation (M1) |
| Prompt format matters enormously | Structured ReAct format + few-shot = reliable agent |

The biggest practical change: **few-shot examples in `build_system_prompt()`** so Kaashvi picks the right tool, formats JSON correctly, and follows the Thought/Action/Observation pattern reliably.
