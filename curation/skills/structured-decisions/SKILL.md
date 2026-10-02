---
name: structured-decisions
description: Choosing how an application makes small repeated decisions at runtime — routing, classification, moderation, triage, scoring, filtering. Covers the ladder from constants and rules up to typed-output classification models and full LLM calls, with the cost, latency and failure mode of each rung. Use when designing or reviewing any code path that must decide "which one", "how urgent", or "is this allowed" on every request.
---

# Structured decisions at runtime

An application that decides something on every request — which model to route to, whether
a message is abusive, how urgent a ticket is, whether a tool call is safe — needs that
decision to be cheap, fast and predictable. The common mistake is to reach straight for an
LLM call because it is the most familiar tool, and to discover in production that it costs
too much, answers too slowly, and occasionally invents a category that does not exist.

## The ladder

Climb one rung only when the one below has actually failed. Each rung costs more in money,
latency and operational surface than the one under it.

| Rung | Use when | Cost | Fails when |
|---|---|---|---|
| **1. Constant or config** | The answer never varies per request | Free | The answer does vary |
| **2. Rule, regex, lookup table** | The decision is expressible in conditions you can enumerate | Free, microseconds | The rules multiply past readability, or inputs are natural language |
| **3. Deterministic code with a scoring function** | You can define the criteria numerically | Free, microseconds | Criteria are fuzzy or depend on meaning |
| **4. Classification model with typed output** | Natural-language input, bounded output, high volume, latency matters | Orders of magnitude below an LLM call; free per call if you run it yourself | You need generated text, or multi-step reasoning |
| **5. LLM call** | Open-ended output, reasoning, generation | Orders of magnitude above rung 4 | Volume or latency makes it untenable |

**Most decisions belong on rungs 1 to 3.** "Is this file a test file?" is a suffix check,
not a classification problem. Write the rule first and let it fail before spending money.

## Rung 4 in practice — a classification model with typed output

The rung-4 tool is a model that **generates no text**. You hand it a block of state and a set
of typed questions; it returns typed values with probabilities and confidence scores, meant to
be consumed by code rather than read. The question shapes are nearly always the same three:

- a **boolean** — a yes/no statement, answered with a probability from 0 to 1
- a **choice** — pick one option from a set you name
- a **score** — rate against a scale you define

The property that earns the rung is that the model **cannot return a value outside the schema
you supply**. That removes a whole class of parsing and hallucination bugs, and removes all
flexibility along with it.

Such models exist both as hosted APIs and as open-source weights you run yourself. The choice
between those two is the usual one — operational surface against per-call cost and data
residency — and it belongs in the ADR, not in this skill.

### Calling one — Laya as a concrete example

[Laya](https://github.com/NandhaKishorM/laya) (Apache-2.0, `pip install laya`) is one open
source option: multilingual, non-autoregressive, runs locally on CPU or GPU, and ships its own
MCP server. Taken from its documentation:

```python
from laya import Router

router = Router()  # downloads a checkpoint on first use

state = "Hi, we were billed twice for March. Please refund the duplicate today or we will cancel our plan."
questions = {
    "department": {"type": "choice", "instructions": "Which department should handle this?",
                   "criteria": {"billing": "invoices, payments, refunds",
                                "technical": "bugs, outages, system errors",
                                "other": "everything else"}},
    "urgency": {"type": "score", "instructions": "How urgent is this?",
                "criteria": ["not urgent", "soon", "blocking"]},
    "churn_risk": {"type": "noul", "instructions": "Does the user threaten to cancel or leave?"},
}

result = router.predict(state, questions, min_confidence=0.6)
print(result["answers"]["department"]["choice"])   # billing
print(result["answers"]["churn_risk"]["noul"])     # probability the answer is yes
```

`min_confidence` is the part worth copying whatever tool you pick: it marks any answer below
the threshold `low_confidence` and reports an `abstention` state, so the calling code can tell
a check that cleared from a check that never ran. Without it you get a bare probability and
no way to distinguish the two.

The same questions are reachable over MCP as the `laya_predict` and `laya_decide` tools, and
in batch — `decide_batch`, `laya_predict_batch` — which shares one forward pass across
requests with the same question schema. Batch whenever you have more than a couple of items.

### Before committing to a rung-4 model in a plan

Check these, and record the answers in an ADR — they are the reasons a future maintainer
will need:

- **Measure its accuracy on your own decisions, zero-shot, before designing around it.**
  These models are small, and out-of-the-box accuracy on a specific domain is often
  unimpressive: Laya's own typed-decisions benchmark reports 0.362 for the base English
  checkpoint against 0.766 after fine-tuning on the domain. Budget for fine-tuning or for a
  confidence threshold that sends the uncertain cases up a rung.
- **Price the operational surface, not just the per-call cost.** A hosted API costs money per
  request and scales with your traffic. A local model costs nothing per call but has to be
  deployed, given CPU or GPU, and kept alive — Laya's checkpoints are 322M–421M parameters and
  download from Hugging Face on first use, so the first request is slow and the container
  needs room for the weights.
- **Check the licence of the weights, not only of the code.** They are often different, and a
  non-commercial model licence rules out a commercial application however permissive the
  surrounding library is. Laya is Apache-2.0 for both.
- **Design the fallback path.** Any rung-4 model, hosted or local, will be unavailable at some
  point. Decide now whether a failure falls back to rung-2 rules or up to an LLM call, rather
  than discovering it in production.
- **It replaces no LLM.** No text out. If any part of the response must be prose, this is the
  wrong rung.

## Reviewing an existing decision path

When you find an LLM call making a small bounded decision, ask in order: could a rule do
it? could a scoring function? is the volume high enough that the cost difference is real?
Only then propose a classifier. Moving a decision from rung 5 to rung 4 is worth doing at
scale and is pure churn at ten calls a day.

Record whichever rung you land on, and why the one below was insufficient, in `STATE.md`
or an ADR. The next person will otherwise assume the choice was arbitrary.
