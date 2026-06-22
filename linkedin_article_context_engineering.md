# Context Engineering: The 4-Operation Pattern That Replaced Prompt Engineering

*Tarun Raja — Founder/Architect, AIWeave (independent applied research, aiweave.org)*

---

Prompt engineering is dead. Everyone agrees. Almost no one has noticed that "context engineering" is just four operations — write, select, compress, isolate — and that three of them belong to a router, not a human.

This article codifies the pattern. It's the design we implemented in ContextWeave/ExpertiseRAG (part of AIWeave, Apache 2.0), and it produced a 91% token reduction on production agent loops. The pattern is not proprietary. The implementation is open. I'm writing it down here because most teams are still doing all four operations by hand, expensively and incorrectly.

---

## Why "Context Engineering" Is the Right Frame

The term "prompt engineering" was always a proxy for a deeper problem: getting the right information into the model's context window at the right time. We called it prompt engineering because, for most teams, the only lever they had was the prompt itself.

Context engineering is the correct name for what actually matters. The context window — the full block of text a model can see on any given call — is the only input that determines output quality. Everything else is downstream of it.

The shift from "prompt" to "context" is not cosmetic. It changes what you build, what you measure, and where the efficiency gains live.

---

## The Four Operations

Context engineering, properly understood, decomposes into four distinct operations. Every team performing context management is doing some version of these — most just don't have names for them, which means they can't reason about which ones to automate.

### Operation 1: WRITE

WRITE is the operation that stays human. It's the authoring of the system message, the user query framing, the instruction structure, the few-shot examples. This is *intent capture* — you're encoding what the model should care about and how it should behave.

WRITE cannot be fully automated because it requires semantic intent that only a human who understands the domain and the goal can provide. You can template it, scaffold it, and assist it with tooling — but the core intent-encoding step demands a human author.

This is where most teams stop. They write a prompt, ship it, and call it done. They've completed one of four operations.

### Operation 2: SELECT

SELECT is where the router wakes up. Given a query and an available corpus — documents, code, conversation history, knowledge bases — SELECT picks the *minimal set* of context that is relevant to this specific turn.

This is RAG. This is semantic search. This is graph traversal and tool-call routing. Any operation that asks "what from our available information does the model actually need right now?" is SELECT.

Most teams who build RAG pipelines call SELECT "done." The model still sees bloat from over-retrieval. Latency still scales with corpus size rather than query specificity. SELECT is necessary, but it is not sufficient.

### Operation 3: COMPRESS

COMPRESS is the operation that most teams skip entirely — and it's where the most significant efficiency gains live.

After SELECT gives you the relevant chunks, COMPRESS removes redundancy *within* those chunks. Strip boilerplate. Summarize repeated patterns. Extract the signal rather than sending the full container: "line 247 is the function signature you need" instead of the entire 500-line file.

In AIWeave's ContextWeave module, compression ratios on typical document and code sets run between 3:1 and 8:1. The 91% token reduction we measured on production agent loops is primarily attributable to the SELECT + COMPRESS combination. Teams running without COMPRESS are paying full freight to feed the model noise.

The response to this is usually: "LLMs are cheap now." They are cheaper than they were. They are not cheap enough to waste 80% of every context window on irrelevant tokens, multiplied by every agent invocation, at production scale.

### Operation 4: ISOLATE

ISOLATE is the guard rail that almost no one builds — and the absence of it is behind a significant portion of confabulation errors in multi-context RAG systems.

After COMPRESS, you have a lean, relevant context payload. ISOLATE injects metadata barriers so the model cannot conflate contexts from different sources. If you're providing "best practices from documentation set A" and "your specific codebase from repository B," those need explicit namespace tags. Without them, the model will hallucinate applications of best-practice A to codebase B that don't apply.

ISOLATE is semantic namespace enforcement. It costs nearly nothing to implement once you have the schema. In our testing, it catches 60% or more of confabulation errors in multi-context settings. It is consistently underrated and almost never built.

---

## The Automation Boundary

The critical insight — the one that changes how you architect your context pipeline — is that these four operations have different automation profiles.

**WRITE stays human.** Intent is domain-specific and goal-specific. You can support the WRITE operation with templates and scaffolding, but you cannot replace it. The model cannot write its own system message without knowing what you want it to do.

**SELECT, COMPRESS, and ISOLATE automate.**

SELECT is deterministic: semantic relevance is measurable. COMPRESS is algorithmic: redundancy detection and summarization are solved problems. ISOLATE is rule-based: you define the tagging schema once and apply it systematically.

When you treat SELECT, COMPRESS, and ISOLATE as router responsibilities rather than human authoring tasks, several things happen:

- Cost per invocation drops because token volume drops
- Hallucination rates drop because context quality goes up
- Latency becomes predictable because you control what enters the window
- You can version, audit, and meter your context pipeline the same way you version and meter any other infrastructure component

Context engineering stops being a "write better prompts" guessing game and becomes a system you can reason about, monitor, and optimize.

---

## What We Built

ContextWeave and ExpertiseRAG (modules within AIWeave, aiweave.org — Apache 2.0, independent applied research) implement the SELECT, COMPRESS, and ISOLATE operations as first-class architectural components.

ContextWeave handles compression and isolation: it takes a retrieved context payload, strips redundancy, and enforces semantic namespace boundaries before the payload reaches the model. ExpertiseRAG handles selection: domain-specific retrieval that operates at the chunk level, not the document level, so selection precision increases as corpus size increases rather than degrading.

The 91% token reduction figure is from production agent loops running ContextWeave — not a benchmark, not a synthetic test. The loops involve multi-turn conversations with retrieval from both structured and unstructured sources. The reduction comes from eliminating redundant context at the COMPRESS stage and from precision retrieval at the SELECT stage. ISOLATE contributes to quality rather than cost, but quality and cost are the same signal at the final-merits level: a confabulating agent is an expensive agent.

---

## How to Apply This in Your Own Stack

You don't need ContextWeave to implement the four-operation pattern. The pattern is the contribution; the implementation is one instance of it.

A rough migration path for teams currently running a single-stage RAG pipeline:

1. **Audit your SELECT operation.** How precise is your retrieval? Are you retrieving whole documents when you need paragraphs? Are you retrieving all matches above a similarity threshold when you need only the top-k most specific? Add retrieval precision as a metric you track.

2. **Add a COMPRESS stage.** Before injecting retrieved chunks into the prompt, run a compression pass. Even a simple extractive summarization step — pulling the most relevant sentences from each chunk — will reduce token volume meaningfully. Measure the before/after at the token level.

3. **Add namespace tags to your ISOLATE stage.** If you're retrieving from more than one source in a single prompt, tag each source explicitly. `[SOURCE: internal-docs]` and `[SOURCE: codebase]` before their respective context blocks is sufficient to reduce cross-source confabulation significantly.

4. **Track token spend per operation, per invocation.** Not just the monthly total — per invocation, and broken down by which context block is consuming which tokens. You cannot optimize what you cannot attribute.

---

## The Measurement Problem

Most teams I talk to know their monthly LLM bill. Almost none of them know their token spend per agent invocation. Fewer still can tell you what percentage of their context window is noise on an average call.

This is the gap that mcp-observatory (another AIWeave module) is built to close — per-invocation observability at the context level, not just the API level. But the measurement problem is separable from the instrumentation solution. Even a manual audit of your current prompts — literally pasting one into a token counter and identifying what's irrelevant to the current turn — will reveal the problem.

The question to ask your team this week: what is our token spend per agent invocation, and are we tracking compression ratios at all?

If you can't answer the first part, you don't have an optimization problem. You have a measurement problem wearing an optimization problem's clothes.

---

## The EB1A-Adjacent Note (Skip If You're Here for the Technical Content)

This article is also part of a deliberate public record. AIWeave is independent applied research — I build it outside of my day job. The four-operation taxonomy of context engineering is my independent crystallization of a pattern I've implemented and measured. I'm writing it down here, with a byline and a timestamp, because the field benefits from named, attributable frameworks — and because establishing a public record of original technical contributions is something I believe every engineer building genuinely novel infrastructure should do.

If you're building something real, write it down. Name the pattern. Own the framing.

---

## Summary

Context engineering is not prompt engineering with better branding. It is a four-operation decomposition of a problem that was always more complex than a single prompt:

| Operation | Who owns it | Automatable? |
|---|---|---|
| WRITE | Human | No — intent is human-defined |
| SELECT | Router | Yes — relevance is measurable |
| COMPRESS | Router | Yes — redundancy is algorithmic |
| ISOLATE | Router | Yes — namespacing is rule-based |

Three of the four operations belong to your infrastructure, not your prompt author. Building them as infrastructure — versionable, auditable, meterable — is the difference between a demo and a production agent system.

ContextWeave / ExpertiseRAG (aiweave.org, Apache 2.0) implements SELECT, COMPRESS, and ISOLATE as open-source modules. The four-operation pattern is free to implement in any stack.

What's your current compression ratio? Are you tracking it?

---

*Tarun Raja is the founder and architect of AIWeave (aiweave.org), an Apache 2.0 AWS-native AI infrastructure ecosystem built as independent applied research. He is a Senior Lead Engineer / SVP at JPMorgan Chase (CIB). The views and work described in this article are his own and are not attributable to JPMorgan Chase.*

---

**Tags:** AI Infrastructure · Agent Architecture · Context Engineering · LLM Optimization · Token Efficiency · ContextWeave · ExpertiseRAG · AIWeave
