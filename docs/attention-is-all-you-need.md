# Attention Is All You Need (Vaswani, Shazeer et al., 2017)

Paper that introduced the Transformer — the architecture behind every modern LLM including Claude, GPT, LLaMA, and Gemini. This is the reason Kaashvi works.

---

## The Problem: Why We Needed Something New

### Recurrent Neural Networks (RNNs)
Neural networks designed for sequential data — text, audio, stock prices. They process one word at a time, left to right, passing a hidden state forward. Weights and biases are shared across all time steps.

Good for sequences, but two massive problems:

### Vanishing / Exploding Gradients
![Vanishing](RNN_gradient_explode.png)

When the model gets something wrong, it computes a loss and sends correction signals (gradients) backward through every step. These gradients get **multiplied** at each step as they travel back.

**Exploding gradients** — corrections grow exponentially. Weights get massive updates, loss becomes NaN, model goes haywire. You can partially fix this with gradient clipping (cap the gradient at a max value) but it's a bandaid.

**Vanishing gradients** — corrections shrink to basically zero. Early words in a long sentence never get meaningful updates. The model literally cannot learn long-range dependencies. Word 1 has no influence on how word 100 is interpreted.

### LSTMs (Long Short-Term Memory)
LSTMs added gates — forget gate, input gate, output gate — that control what information to keep and what to throw away.

```
RNN:  information must pass through every step (gets degraded)
LSTM: information has a highway lane that can skip steps (preserved)
```

LSTMs helped with vanishing gradients, but they're still **sequential**. Word 5 still waits for word 4. You cannot parallelize this on a GPU. Training is slow.

### Types of RNN Architectures
1. **Vector -> Sequence** — fixed input, sequence output (e.g., image captioning)
2. **Sequence -> Vector** — sequence input, fixed output (e.g., sentiment analysis)
3. **Sequence -> Sequence** — both sides are sequences (e.g., translation, which is what this paper tackles)

### The Core Question
Can we handle sequences WITHOUT recurrence? Can every word see every other word at the same time, so we can parallelize everything?

Yes. That's what the Transformer does.

---

## The Solution: Self-Attention

Instead of processing words one by one in order, let every word **look at every other word simultaneously**. This is called self-attention.

```
RNN way (reading a book one word at a time):
"The cat sat on the mat"
  1 -> 2 -> 3 -> 4 -> 5 -> 6
  Word 6 only "remembers" word 1 through a chain. Long chain = degraded info.

Attention way (seeing the whole sentence at once):
"The cat sat on the mat"
  Every word can directly look at every other word.
  "mat" looks directly at "cat" — no chain, no degradation.
```

This solves both problems:
1. **Parallelization** — all words processed at the same time (GPU loves this)
2. **Long-range dependencies** — word 100 can directly attend to word 1, no chain

### Query, Key, Value (Q, K, V)

Every word gets transformed into three vectors through learned weight matrices:

| Vector | Role | Analogy |
|--------|------|---------|
| **Query (Q)** | "What am I looking for?" | Your search question at a library |
| **Key (K)** | "What do I contain?" | Book titles / index cards |
| **Value (V)** | "What info do I give if matched?" | The actual book contents |

**Example:** "The animal didn't cross the street because **it** was too tired"

What does "it" refer to? Here's what self-attention does:
1. "it" creates a Query: "What noun am I referring to?"
2. Every word creates a Key: "animal" says "I'm a living noun"; "street" says "I'm a place"
3. Q * K^T = dot product = similarity score. "it" scores high with "animal", low with "street"
4. Softmax normalizes scores to probabilities (animal=0.85, street=0.05, ...)
5. Multiply by V = "it" now carries mostly "animal"'s information

The formula:
```
Attention(Q, K, V) = softmax(Q * K^T / sqrt(d_k)) * V
```

The `/ sqrt(d_k)` is just scaling — without it, dot products get too large and softmax becomes too sharp (puts all attention on one word, ignoring everything else).

**Why three projections instead of one?** Because a word needs to play different roles at the same time. When "it" is ASKING (Q) it behaves differently than when "animal" is BEING MATCHED (K) or PROVIDING information (V). These are different jobs — separating them lets the model learn each role independently.

---

## Multi-Head Attention

One attention head learns ONE type of relationship. But language has many:
- Grammar: subject <-> verb agreement
- Meaning: "cat" and "animal" are related
- Position: adjacent words matter
- Coreference: "it" -> "cat"

Solution: run **8 attention heads in parallel**, each with its own Q, K, V weight matrices.

```
Head 1: learns grammar relationships
Head 2: learns semantic similarity
Head 3: learns positional patterns
Head 4: learns coreference ("it" -> "cat")
... (8 total in the paper)
```

Then concatenate all 8 outputs and project back down:
```
MultiHead(Q, K, V) = Concat(head_1, ..., head_8) * W_O
where head_i = Attention(Q * W_Qi, K * W_Ki, V * W_Vi)
```

It's like having 8 specialists vs 1 generalist. Each head specializes in one type of pattern. Together they see the full picture.

If embedding dimension is 512 and you have 8 heads, each head works with 512/8 = **64 dimensions**.

---

## Positional Encoding

Attention sees all words at once, so it has **no idea about word order**. "Dog bites man" and "Man bites dog" would look identical. RNNs knew order from sequential processing. Transformers need something else.

Solution: add a unique position signal to each word's embedding using sine and cosine functions:
```
PE(pos, 2i)   = sin(pos / 10000^(2i/d_model))
PE(pos, 2i+1) = cos(pos / 10000^(2i/d_model))
```

Don't memorize the formula. The intuition:
- Each position gets a **unique fingerprint**
- Nearby positions have **similar patterns** (model knows "these words are close")
- The pattern is **added** to the word embedding (not concatenated)

```
final_input = word_embedding + positional_encoding
```

**Why add instead of concatenate?** Concatenation would double the size (512 -> 1024), making everything downstream bigger and slower. Addition keeps the same size. The embedding space is high-dimensional enough that position info and word meaning coexist without interfering.

---

## The Transformer Block

Each layer stacks these components:

### Encoder Block (x6 in the paper)
```
Input
  |
[Multi-Head Self-Attention]
  |
[Add & Normalize]    <- residual connection + layer norm
  |
[Feed-Forward Network]    <- two linear layers with ReLU: FFN(x) = max(0, xW1+b1)W2+b2
  |
[Add & Normalize]    <- another residual connection + layer norm
  |
Output
```

### Decoder Block (x6 in the paper)
```
Input (previously generated words)
  |
[MASKED Self-Attention]     <- can't see future words
  |
[Add & Normalize]
  |
[Cross-Attention]           <- Q from decoder, K+V from encoder
  |
[Add & Normalize]
  |
[Feed-Forward Network]
  |
[Add & Normalize]
  |
Output
```

**Residual connections** (the "Add" part): input is added back to the output: `output = layer(x) + x`. Borrowed from ResNet. Helps gradients flow during training — another solution to the vanishing gradient problem.

**Layer Normalization**: normalizes values to prevent them from blowing up or collapsing. Stabilizes training.

---

## Masked Self-Attention (Decoder Only)

When generating word 5, the model should NOT see words 6, 7, 8... — that would be cheating (looking at the future). So future positions are **masked** by setting their attention scores to negative infinity before softmax. This forces them to zero probability.

```
"I love cats and ___"

Predicting the blank:
  "I"     -> visible
  "love"  -> visible
  "cats"  -> visible
  "and"   -> visible
  "___"   -> MASKED (this is what we're predicting)
```

---

## Cross-Attention (Decoder Only)

The decoder needs to read the encoder's output — the "understanding" of the input. Cross-attention is like self-attention but:
- **Q** comes from the decoder ("what am I looking for?")
- **K and V** come from the encoder ("what does the input contain?")

This is how a translation model reads the English input while generating the French output.

---

## Final Output: How Words Are Chosen

```
Decoder output (a vector for each position)
    |
[Linear layer]    -> projects to vocabulary size (e.g., 50,000 words)
    |
[Softmax]         -> probability distribution over all possible words
    |
Pick the highest probability word (or sample from distribution)
```

The output is literally: "73% chance the next word is 'dogs', 12% 'puppies', 3% 'animals'..."

---

## Paper Stats
- **Model dimension (d_model):** 512
- **Attention heads:** 8
- **Head dimension:** 64 (512 / 8)
- **Encoder layers:** 6
- **Decoder layers:** 6
- **Feed-forward inner dimension:** 2048
- **Training:** 8 NVIDIA P100 GPUs, 3.5 days
- **Result:** Beat all existing translation models while training faster

---

## How This Connects to Kaashvi

Every time Kaashvi calls the Anthropic API in `react_loop.py` (line 75), here's what happens inside Claude:

```
System prompt + conversation history + scratchpad
    |
Tokenized into numbers
    |
Word embeddings + positional encodings
    |
Through ~80 decoder-only transformer blocks
(each block: masked self-attention -> feed-forward -> residual + norm)
    |
Softmax over vocabulary
    |
"Thought: I need to check the calendar..." <- generated one token at a time
```

Claude is a **decoder-only** transformer — no separate encoder. Input and output share the same stack. This is the GPT-style architecture.

**Things in Kaashvi that exist because of this paper:**
- The `max_tokens=1024` parameter — this controls how many tokens the decoder generates
- The `system` prompt works because of how attention processes the full context
- The conversation history format (`messages` list) is what gets tokenized and fed through attention layers
- The scratchpad trick works because self-attention lets the model attend to its own previous reasoning
- Kaashvi's ability to understand "schedule a meeting with her" (referencing a name from 3 messages ago) is literally self-attention resolving a long-range dependency

**Understanding transformers means understanding WHY Kaashvi works, not just THAT she works.**

---

## What I'd Improve With This Knowledge
- **Better prompt engineering** — knowing how attention works, I can structure prompts so important information is easier for the model to attend to
- **Token awareness** — understanding the tokenizer and context window limitations leads to smarter `trim_history()` in Phase D2
- **Model routing (Phase D3)** — smaller transformers (Haiku) for simple tasks, bigger ones (Sonnet/Opus) for complex reasoning
