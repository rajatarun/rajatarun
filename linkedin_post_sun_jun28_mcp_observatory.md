# LinkedIn Post — Sunday Jun 28, 2026
# Topic: LLM Cost Attribution / mcp-observatory
# Format: Text post ~280 words

---

Your model provider cannot tell a production pipeline from a junior's infinite loop. It bills both as "API usage." Finance forwards you the invoice. No one's mental model matches it — and the dashboard was never built to make it match.

This is the actual problem with LLM cost control: the unit of billing (tokens) doesn't map to the unit of work (agent invocations, pipeline runs, task completions). You get a monthly aggregate. You don't get per-loop spend, per-invocation context-window breakdown, which pipeline is consuming 70% of your budget on repeated payloads, or whether dev environment noise is bleeding into your production line item.

Optimization is impossible when you can't attribute spend to behavior. You're tuning blindfolded.

I built mcp-observatory inside AIWeave (aiweave.org, Apache 2.0) specifically because this gap isn't a reporting problem — it's an instrumentation problem. The billing API gives you what the provider tracks. mcp-observatory instruments at the invocation level: per-loop cost, context-window breakdown per call, compression ratio before and after context compaction, payload repetition across turns. It sits between your agent and the model, not downstream in a dashboard.

The billing dashboard was designed to tell you what you spent. It was never designed to tell you why, or which invocation is the one to fix.

Until you're tracking at that granularity, any budget conversation is a guess dressed up as a number.

What does your per-invocation cost look like right now — and can you actually answer that without a custom instrumentation layer?

#MCPProtocol #AgentObservability #LLMCostControl #AIInfrastructure #AgentArchitecture
