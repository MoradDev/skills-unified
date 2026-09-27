---
name: structured-decisions
description: Choosing how an application makes small repeated decisions at runtime — routing, classification, moderation, triage, scoring, filtering. Covers the ladder from constants and rules up to classifier models such as TypeSafe Jev and full LLM calls, with the cost, latency and failure mode of each rung. Use when designing or reviewing any code path that must decide "which one", "how urgent", or "is this allowed" on every request.
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
| **4. Classifier model** | Natural-language input, bounded output, high volume, latency matters | ~$0.04 per million input tokens | You need generated text, or multi-step reasoning |
| **5. LLM call** | Open-ended output, reasoning, generation | 40–400× rung 4 | Volume or latency makes it untenable |

**Most decisions belong on rungs 1 to 3.** "Is this file a test file?" is a suffix check,
not a classification problem. Write the rule first and let it fail before spending money.

## Rung 4 in practice — Jev

[Jev](https://vercel.com/ai-gateway/models/jev) from TypeSafe AI is a "System One" model:
it generates no text. You hand it a block of state and typed questions; it returns typed
values with probabilities and confidence scores, meant to be consumed by code rather than
read. Three question types:

- `noul` — a yes/no statement, answered with a probability from 0 to 1
- `choice` — pick one option from a set you name
- `score` — rate against a scale you define

It **cannot return a value outside the schema you supply**, which removes a whole class of
parsing and hallucination bugs, and removes all flexibility along with it.

### Calling it

Over Vercel AI Gateway, from any language:

```bash
curl https://ai-gateway.vercel.sh/typesafe/v1/systemone \
  -H "Authorization: Bearer $AI_GATEWAY_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "typesafe-ai/jev",
    "state": "I was charged twice for my subscription.",
    "questions": {
      "refund": { "type": "noul", "instructions": "Is the customer asking for money back?" },
      "team": {
        "type": "choice",
        "instructions": "Which team should handle this?",
        "criteria": { "billing": "Charges and refunds", "technical": "Bugs and outages" }
      }
    }
  }'
```

The response carries `answers` keyed by your question names, plus `usage`. Never hardcode
the key — read it from the environment, as with any credential.

### What it costs and what it bounds

$0.042 per million input tokens, 32,000-token context. The vendor claims 40–200× faster
and 40–400× cheaper than frontier LLMs on comparable classification.

### Before committing to it in a plan

Check these, and record the answers in an ADR — they are the reasons a future maintainer
will need:

- **It is young.** Released 15 September 2026. Vercel's model page reports no rate limits
  and no production-readiness guarantee, and notes its capability metadata is incomplete.
  Treat availability as unproven and design a fallback path — rung 2 rules, or an LLM call —
  rather than a hard dependency.
- **It is paid per call, in your application's runtime.** Unlike a build-time tool, this
  cost scales with your traffic. Estimate it against expected volume before choosing it.
- **Self-hosting is probably not an option.** Open-Jev is 27B parameters, needs roughly an
  80 GB GPU, and is licensed **CC BY-NC 4.0 — non-commercial**. If the application is
  commercial, the hosted API is the only lawful path.
- **It replaces no LLM.** No text out. If any part of the response must be prose, this is
  the wrong rung.

## Reviewing an existing decision path

When you find an LLM call making a small bounded decision, ask in order: could a rule do
it? could a scoring function? is the volume high enough that the cost difference is real?
Only then propose a classifier. Moving a decision from rung 5 to rung 4 is worth doing at
scale and is pure churn at ten calls a day.

Record whichever rung you land on, and why the one below was insufficient, in `STATE.md`
or an ADR. The next person will otherwise assume the choice was arbitrary.
