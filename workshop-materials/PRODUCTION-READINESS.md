# Production Readiness Checklist for AI Agents

A checklist specifically designed for AI agents built with Google ADK - not generic software.

---

## Why This Exists

The workshop teaches you how to **build** an AI agent. Production requires additional considerations that are specific to AI systems:

- **Evaluation:** How do you know your agent is giving good answers?
- **Observability:** How do you debug when things go wrong at 2 AM?
- **Cost Management:** LLM API calls cost money - how do you track and control this?
- **Reliability:** What happens when external APIs fail?

This checklist bridges the gap between "workshop complete" and "ready for real users."

---

## Two Tiers: MVP vs Mature Production

| Tier | Timeline | Goal |
|------|----------|------|
| **MVP** | Day 1-7 | Launch internally with confidence |
| **Mature** | Week 2-4 | Scale to production traffic |

Start with MVP. Every item has a reason. Skip items only if you understand the risk.

---

## Workshop vs Production Comparison

| Aspect | Workshop | Production |
|--------|----------|------------|
| Traffic | 1 user testing | 100-10,000+ users |
| Uptime | None required | 99%+ SLA |
| Errors | Debug manually | Alert and triage |
| Costs | Free tier / minimal | Budget tracking required |
| Testing | Manual verification | Automated evaluation |
| Monitoring | Print statements | Observability platform |
| Sessions | Ephemeral | Persistent across days |
| Secrets | Environment variables | Secret manager |

---

## MVP Production Checklist (Day 1-7)

Items needed to launch with confidence. Complete these before your first internal users.

### Evaluation (CRITICAL)

Without evaluation, you don't know if your agent is working correctly.

- [ ] **Golden dataset with 20+ test cases covering main user intents**
  - Why: Regression testing - know immediately if a change breaks something
  - How: See `tests/eval_datasets/` for format with `tool_uses` in `intermediate_data`
  - Workshop reference: `tests/README.md` explains AgentEvaluator patterns

- [ ] **Response quality baseline measured (AgentEvaluator)**
  - Why: Need a number to compare against after changes
  - How: Run `pytest tests/ -v` and record `tool_trajectory_avg_score`
  - Target: `tool_trajectory_avg_score >= 0.8`

- [ ] **Tool trajectory accuracy >= 80%**
  - Why: Agent must call correct tools with correct parameters
  - How: Golden datasets specify expected tool calls, evaluator compares actual
  - Workshop reference: `tests/eval_datasets/flight_search.test.json`

- [ ] **Manual review of 10 edge case conversations**
  - Why: LLM-as-judge misses nuance humans catch
  - How: Collect 10 real conversations, manually score appropriateness
  - Edge cases: Ambiguous requests, multi-tool scenarios, error recovery

### Observability (CRITICAL)

Without observability, debugging production issues is impossible.

- [ ] **Logging enabled for all LLM calls**
  - Why: Know what prompts were sent and what responses came back
  - How: Enable Cloud Logging, capture request/response
  - Include: Session ID, user ID, timestamp, latency

- [ ] **Tool success/failure tracking**
  - Why: Know which tools fail most often
  - How: Log tool name, parameters, result status, duration
  - Workshop reference: Error-in-context pattern returns `{"status": "error", ...}`

- [ ] **Basic latency monitoring**
  - Why: Know if agent is getting slower
  - How: Track end-to-end response time per query
  - Alert if: p95 latency > 5 seconds

- [ ] **Error alerting configured**
  - Why: Know about failures before users complain
  - How: Cloud Monitoring alerts on error rate > 5%
  - Include: PagerDuty/Slack integration for on-call

### Cost Management

LLM APIs are not free. Track usage or get surprised by bills.

- [ ] **Token usage tracking per session**
  - Why: Know which queries cost most
  - How: Use `cost_tracker.py` pattern to log `usage_metadata`
  - Workshop reference: `WorkshopCostTracker` in `cost_tracker.py`

- [ ] **Daily cost alerts configured**
  - Why: Catch runaway costs before month-end
  - How: GCP Budget Alerts with 50%, 80%, 100% thresholds
  - Action: Alert on-call if daily spend exceeds expected

- [ ] **Model selection documented (Flash vs Pro)**
  - Why: Pro costs 10x+ more than Flash
  - How: Document which model for which use case
  - Recommendation: Flash for most queries, Pro only when needed
  - Current pricing: Gemini 2.5 Flash at $0.30/$2.50 per 1M tokens

### Reliability

Handle failures gracefully so users have a good experience.

- [ ] **Graceful error handling (error-in-context pattern)**
  - Why: Agent can explain and recover from errors
  - How: Tools return `{"status": "error", "error_message": "..."}` instead of raising
  - Workshop reference: All tools in `tools.py` use this pattern

- [ ] **Timeout configuration for external APIs**
  - Why: Prevent hanging on slow external services
  - How: 30-second timeout on all external calls
  - Action: Return helpful error message on timeout

- [ ] **Basic rate limiting**
  - Why: Prevent single user from exhausting quota
  - How: 10 requests/minute/user initially
  - Track: Cloud Endpoints or application-level limiting

### Security

Protect user data and prevent abuse.

- [ ] **API keys in environment variables (not code)**
  - Why: Keys in code get committed to git
  - How: Use `.env` files locally, Secret Manager in production
  - Verify: `grep -r "GOOGLE_API_KEY" --include="*.py"` returns nothing

- [ ] **Input validation on user queries**
  - Why: Prevent prompt injection, filter malicious input
  - How: Length limits, character filtering, pattern detection
  - Maximum query length: 2000 characters

- [ ] **No PII logging without consent**
  - Why: GDPR, CCPA, and other privacy regulations
  - How: Redact emails, phone numbers, addresses from logs
  - Review: Audit logs monthly for PII leakage

---

## Mature Production Checklist (Week 2+)

Items for scale, confidence, and continuous improvement. Build on MVP foundation.

### Evaluation (ADVANCED)

Production evaluation is more than one-time testing.

- [ ] **Golden dataset with 50+ examples covering all tool combinations**
  - Why: More coverage means fewer edge case surprises
  - Include: Multi-tool sequences, error paths, preference usage
  - Maintain: Update dataset as you discover new failure modes

- [ ] **Session-level evaluation (multi-turn conversation quality)**
  - Why: Individual responses can be good but conversation flow bad
  - How: Rate complete sessions on goal completion
  - Metric: % of sessions where user achieved their intent

- [ ] **Trace-level evaluation (reasoning chain validity)**
  - Why: Right answer via wrong reasoning breaks eventually
  - How: Review tool call sequences for logical correctness
  - Pattern: Did agent gather info before making recommendations?

- [ ] **Human evaluation loop for tone and appropriateness**
  - Why: LLM judges miss cultural nuance, brand voice, edge cases
  - How: Sample 5% of conversations for human review weekly
  - Score: Helpfulness, accuracy, appropriateness (1-5 scale)

- [ ] **Regression testing on prompt changes**
  - Why: Prompt changes can break things you didn't expect
  - How: Run full golden dataset before every prompt deployment
  - Block deploy if: Accuracy drops > 5%

### Observability (ADVANCED)

See everything happening in production.

- [ ] **Distributed tracing across all LLM calls and tools**
  - Why: Debug multi-step agent behavior
  - How: Cloud Trace with span IDs linking LLM calls + tool executions
  - Include: Context propagation across tool calls

- [ ] **Token consumption dashboards**
  - Why: Visualize trends, catch anomalies
  - How: Grafana/Cloud Monitoring dashboard
  - Dimensions: By user, by session, by query type

- [ ] **Latency percentiles (p50, p95, p99)**
  - Why: Average hides tail latency
  - How: Track distribution, not just mean
  - Alert if: p99 > 10 seconds

- [ ] **Error rate by error type**
  - Why: Different errors need different fixes
  - How: Categorize errors (tool failure, timeout, model error, validation)
  - Dashboard: Error breakdown pie chart

- [ ] **User satisfaction signals**
  - Why: Technical metrics don't capture user happiness
  - How: Thumbs up/down on responses, session abandonment rate
  - Track: Correlation between metrics and satisfaction

### Cost Management (ADVANCED)

Optimize spend without sacrificing quality.

- [ ] **Cost attribution by user/session**
  - Why: Find expensive users or use cases
  - How: Aggregate token usage by user ID and session ID
  - Action: Investigate sessions that cost > $0.10

- [ ] **Budget alerts with automatic throttling**
  - Why: Prevent runaway costs automatically
  - How: Rate limit or queue requests when daily budget 80% consumed
  - Notify: User sees "high demand, responses may be delayed"

- [ ] **Cost optimization analysis (which queries cost most?)**
  - Why: 20% of queries may cost 80% of budget
  - How: Analyze token usage by query pattern
  - Optimize: Caching, model routing, prompt compression

- [ ] **Model routing (Flash for simple, Pro for complex)**
  - Why: Use cheaper model when possible
  - How: Classify query complexity, route to appropriate model
  - Pattern: Flash for factual queries, Pro for complex reasoning

### Reliability (ADVANCED)

Handle failures at scale.

- [ ] **Multi-provider failover strategy**
  - Why: Single provider outage shouldn't take down your agent
  - How: Fallback to alternative model if primary fails
  - Pattern: Gemini primary, OpenAI fallback (or vice versa)

- [ ] **Graceful degradation when tools fail**
  - Why: Partial answer better than no answer
  - How: Continue conversation even if one tool fails
  - Example: "I couldn't search flights, but here's destination info..."

- [ ] **Circuit breaker for external APIs**
  - Why: Stop cascading failures
  - How: Open circuit after 5 consecutive failures, retry after 30 seconds
  - Pattern: Circuit breaker pattern from distributed systems

- [ ] **Rollback procedure for prompt/tool changes**
  - Why: Bad deploy needs quick recovery
  - How: Version control prompts, one-click rollback
  - Test: Practice rollback quarterly

### Configuration and Governance

Manage change safely and comply with regulations.

- [ ] **Prompts version-controlled in git**
  - Why: Treat prompts like code - review, track, rollback
  - How: Store in `.txt` or `.yaml` files, not inline strings
  - Pattern: `prompts/v1/travel_assistant.txt`

- [ ] **Tool schemas version-controlled**
  - Why: Tool changes affect agent behavior
  - How: Track tool function signatures and docstrings
  - Review: Require review for tool changes

- [ ] **Change review process for prompts**
  - Why: Prompt changes can break things subtly
  - How: PR review + golden dataset test required
  - Checklist: Does this change affect safety? Accuracy? Costs?

- [ ] **Audit trail for regulatory compliance**
  - Why: May need to explain agent decisions to regulators
  - How: Log all model inputs/outputs with timestamps
  - Retention: Keep logs for required period (check regulations)

---

## Workshop Components That Help

The workshop reference implementation demonstrates many production patterns:

### Evaluation

| Workshop Component | Production Pattern |
|-------------------|-------------------|
| `tests/README.md` | AgentEvaluator framework overview |
| `tests/eval_datasets/` | Golden dataset format with `tool_uses` |
| `tests/test_travel_agent.py` | pytest integration for CI/CD |

**Key pattern:** Golden datasets include `intermediate_data.tool_uses` to validate tool call trajectories, not just final responses.

### Cost Tracking

| Workshop Component | Production Pattern |
|-------------------|-------------------|
| `cost_tracker.py` | Token usage tracking and cost calculation |
| `WorkshopCostTracker` class | Session-level cost aggregation |
| `estimate_workshop_cost()` | Capacity planning function |

**Key pattern:** Extract `usage_metadata` from responses to track `prompt_token_count` and `candidates_token_count`.

### Error Handling

| Workshop Component | Production Pattern |
|-------------------|-------------------|
| `tools.py` | Error-in-context pattern (return error dict) |
| Tool functions | Validation before processing |
| Error messages | Include examples for user correction |

**Key pattern:** Return `{"status": "error", "error_message": "...", "example": "..."}` instead of raising exceptions. LLM can see and help user fix the issue.

### Deployment

| Workshop Component | Production Pattern |
|-------------------|-------------------|
| `DEPLOYMENT.md` | Vertex AI Agent Engine deployment |
| `deploy.py` | Automated deploy/test/cleanup script |
| Prerequisites section | Required IAM roles and APIs |

**Key pattern:** Always clean up test deployments to prevent ongoing billing.

---

## Estimated Timeline

| Milestone | Typical Time | What's Complete |
|-----------|--------------|-----------------|
| Workshop complete | Day 0 | Concepts understood, agent working locally |
| MVP checklist done | Day 3-7 | Safe to launch to internal users |
| Mature checklist done | Week 2-4 | Ready for production traffic |
| Production-hardened | Month 2+ | Handling edge cases, optimized costs |

### Realistic Expectations

| Activity | Estimated Time |
|----------|----------------|
| Set up monitoring/logging | 2-4 hours |
| Create 20-case golden dataset | 4-8 hours |
| Configure cost tracking | 1-2 hours |
| Implement rate limiting | 2-4 hours |
| Set up CI/CD with tests | 4-8 hours |
| Total MVP | 15-30 hours |

---

## Common Mistakes to Avoid

### 1. Skipping Evaluation

**Mistake:** "It works in testing, ship it."

**Reality:** Without golden datasets, you can't:
- Know if a change broke something
- Compare model versions objectively
- Debug "it feels worse" complaints

**Fix:** Spend 4-8 hours creating 20+ test cases before launch.

### 2. No Cost Tracking

**Mistake:** "Gemini is cheap, don't worry about it."

**Reality:**
- Runaway loops can burn hundreds of dollars
- Token costs compound with user growth
- No visibility = surprise bills

**Fix:** Implement `cost_tracker.py` pattern on day one.

### 3. Logging Everything

**Mistake:** "Log all conversations for debugging."

**Reality:**
- User queries contain PII
- GDPR/CCPA require consent
- Storage costs add up

**Fix:** Log metadata (latency, token counts, error types) always. Log content only with consent and redaction.

### 4. Ignoring Tool Failures

**Mistake:** "Tools either work or throw exceptions."

**Reality:**
- External APIs fail silently
- Partial data is common
- Agent should handle gracefully

**Fix:** Use error-in-context pattern. Test with intentionally failing tools.

### 5. Prompt Changes Without Testing

**Mistake:** "I just tweaked the wording, it's fine."

**Reality:**
- Small changes can break edge cases
- Effects are often invisible until production
- Rollback is painful without version control

**Fix:** Version control prompts. Run golden dataset tests before every change.

---

## Resources

### ADK Documentation
- [ADK Overview](https://google.github.io/adk-docs/)
- [Evaluation Guide](https://google.github.io/adk-docs/evaluate/)
- [Deployment Guide](https://google.github.io/adk-docs/deploy/)

### Vertex AI
- [Vertex AI Agent Engine](https://cloud.google.com/vertex-ai/docs/reasoning-engine/overview)
- [Vertex AI Pricing](https://cloud.google.com/vertex-ai/pricing)
- [Cloud Monitoring](https://cloud.google.com/monitoring/docs)

### Workshop Reference Implementation
- `reference-implementation/` - Complete working example
- `tests/` - AgentEvaluator test patterns
- `cost_tracker.py` - Token tracking implementation
- `DEPLOYMENT.md` - Deployment guide

### Industry Best Practices
- [State of AI Agents 2026](https://www.langchain.com/state-of-agent-engineering) - 89% have observability, 52% have evaluation
- [AI Agent Production Checklist](https://www.getmaxim.ai/articles/the-ultimate-checklist-for-rapidly-deploying-ai-agents-in-production/)

---

## Quick Reference: Day 1 Priorities

If you can only do 5 things before launch:

1. **Create 10-case golden dataset** - Know if it breaks
2. **Enable logging** - Debug production issues
3. **Track token costs** - Avoid bill shock
4. **Error-in-context pattern** - Graceful failures
5. **Daily cost alerts** - Catch runaway usage

Everything else can wait until you have real users providing real feedback.

---

*This checklist is part of the Google ADK Workshop materials. For workshop support, contact your instructor.*
