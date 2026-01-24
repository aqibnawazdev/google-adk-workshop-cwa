# Phase 4: Sessions & Deployment - Research

**Researched:** 2026-01-24
**Domain:** ADK Session Management, Vertex AI Deployment, Agent Evaluation, Cost Monitoring
**Confidence:** MEDIUM

## Summary

Phase 4 covers session state management for user preferences, deployment to Vertex AI Agent Engine, automated testing with AgentEvaluator, and cost monitoring. The research reveals that ADK already uses InMemorySessionService throughout Exercises 1-3, so this phase focuses on teaching **state prefixes** for preference persistence, introducing deployment workflows, and establishing evaluation patterns.

**Key architectural insight:** The workshop already uses proper ADK patterns (Runner + InMemorySessionService), so session "introduction" is not needed. The phase should focus on **state management patterns** (user: prefix for cross-session preferences), **deployment mechanics** (Vertex AI Agent Engine), and **testing discipline** (AgentEvaluator for validation).

For a 90-minute workshop with ~15-20 minutes allocated to this phase, the scope must be demonstration-focused rather than hands-on. Deployment requires GCP project setup (billing, APIs, buckets) which is impractical for beginners in 15 minutes. Recommend: demonstrate deployment, provide hands-on state management, document deployment for post-workshop exploration.

**Primary recommendation:** Use state prefixes (user:, temp:) for preference persistence in Exercise 4, demonstrate Agent Engine deployment in instructor walkthrough, provide AgentEvaluator example tests as reference material.

## Standard Stack

The established libraries/tools for this domain:

### Core
| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| google-adk | 1.23.0 | Agent framework with session management | Official Google ADK, includes InMemorySessionService, DatabaseSessionService, session state management |
| google-cloud-aiplatform | >=1.112 | Vertex AI SDK for deployment | Required for agent_engines.create() deployment to Vertex AI Agent Engine |
| pytest | Latest | Testing framework | Standard Python testing, integrates with AgentEvaluator for CI/CD |
| pytest-asyncio | Latest | Async test support | Required for @pytest.mark.asyncio with AgentEvaluator.evaluate() |

### Supporting
| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| vertexai | >=1.112 | Vertex AI client initialization | Alternative import path for agent_engines module |
| google-generativeai | Latest (Gemini SDK) | Token usage tracking | Cost monitoring via model metadata in responses |

### Alternatives Considered
| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| InMemorySessionService | DatabaseSessionService | Requires database setup (PostgreSQL/MySQL/SQLite), overkill for workshop |
| InMemorySessionService | VertexAiSessionService | Requires Reasoning Engine deployment, high complexity barrier |
| Vertex AI Agent Engine | Local deployment only | Misses production deployment learning objective |

**Installation:**
```bash
# Core ADK (already installed in workshop)
pip install google-adk==1.23.0

# For deployment (Exercise 4 / post-workshop)
pip install google-cloud-aiplatform[agent_engines,adk]>=1.112

# For testing (reference material)
pip install pytest pytest-asyncio
```

## Architecture Patterns

### Recommended Session State Structure
```python
# Session state with prefixes for different scopes
session.state = {
    # Session-scoped (current conversation only)
    "current_step": 3,
    "search_results": [...],

    # User-scoped (persists across all user sessions)
    "user:budget": 1000,
    "user:travel_style": "budget",
    "user:dietary_restrictions": ["vegetarian"],

    # App-scoped (shared across all users/sessions)
    "app:version": "1.0.0",
    "app:feature_flags": {"rag_enabled": True},

    # Temporary (current invocation only, never persists)
    "temp:api_response": {...},
    "temp:intermediate_calc": 42
}
```

### Pattern 1: State Prefix Usage for User Preferences
**What:** Use `user:` prefix for cross-session user preferences, no prefix for conversation-specific data
**When to use:** User mentions preferences (budget, style, dietary needs) that should persist
**Example:**
```python
# Source: https://google.github.io/adk-docs/sessions/state/
# In tool function or callback
def remember_preference(context: ToolContext, preference_type: str, value: str):
    """Store user preference across sessions using user: prefix"""
    context.state[f"user:{preference_type}"] = value
    return f"I'll remember that you prefer {value}"

# In agent instruction (state injection)
instruction = """You are a travel assistant.

User preferences (from previous conversations):
- Budget: {user:budget?}
- Travel style: {user:travel_style?}
- Dietary restrictions: {user:dietary_restrictions?}

Use these preferences when making recommendations.
If a preference is mentioned, remember it for future conversations.
"""
```

### Pattern 2: Vertex AI Agent Engine Deployment
**What:** Deploy ADK agent to managed Vertex AI runtime for production access
**When to use:** Moving from development to production, need shareable endpoint, require scaling
**Example:**
```python
# Source: https://docs.cloud.google.com/agent-builder/agent-engine/quickstart-adk
import vertexai
from vertexai import agent_engines
from google.adk.agents import Agent

# 1. Create agent locally
agent = Agent(
    model="gemini-2.5-flash",
    name="travel_booking_assistant",
    tools=[search_flights, search_hotels]
)
app = agent_engines.AdkApp(agent=agent)

# 2. Initialize Vertex AI client
client = vertexai.Client(project="PROJECT_ID", location="us-central1")

# 3. Deploy to Agent Engine (~3 minutes)
remote_agent = client.agent_engines.create(
    agent=app,
    config={
        "requirements": ["google-cloud-aiplatform[agent_engines,adk]"],
        "staging_bucket": "gs://YOUR_BUCKET"  # Required for code staging
    }
)

# 4. Get endpoint URL
print(remote_agent.api_resource.name)
# Output: projects/PROJECT_NUMBER/locations/us-central1/reasoningEngines/RESOURCE_ID

# 5. Test deployed agent (same API as local)
async for event in remote_agent.async_stream_query(
    user_id="user_123",
    message="Find flights from SFO to Tokyo"
):
    print(event)
```

### Pattern 3: AgentEvaluator pytest Integration
**What:** Automated testing with golden datasets and pass/fail criteria
**When to use:** CI/CD pipelines, regression testing, validating agent behavior
**Example:**
```python
# Source: https://codelabs.developers.google.com/adk-eval/instructions
# tests/test_agent_eval.py
from google.adk.evaluation.agent_evaluator import AgentEvaluator
import pytest

@pytest.mark.asyncio
async def test_booking_agent():
    """Test agent's flight search capability"""
    await AgentEvaluator.evaluate(
        agent_module="agent",  # Path to agent.py
        eval_dataset_file_path_or_dir="tests/booking_eval.test.json",
    )

# tests/booking_eval.test.json
{
  "eval_set_id": "booking_tests",
  "name": "Flight and Hotel Booking Tests",
  "eval_cases": [
    {
      "eval_id": "budget_flight_search",
      "session_input": {
        "app_name": "travel_booking_assistant",
        "user_id": "eval_user"
      },
      "conversation": [
        {
          "user_content": {
            "role": "user",
            "parts": [{"text": "Find flights from SFO to NRT under $900"}]
          },
          "intermediate_data": {
            "tool_uses": [
              {
                "name": "search_flights",
                "args": {
                  "origin": "SFO",
                  "destination": "NRT",
                  "max_price": 900
                }
              }
            ]
          }
        }
      ]
    }
  ]
}
```

### Pattern 4: Cost Monitoring with Token Tracking
**What:** Track token usage and API costs for budget management
**When to use:** Production deployments, workshop cost control, billing alerts
**Example:**
```python
# Source: https://ai.google.dev/gemini-api/docs/pricing
# Token tracking in responses (built-in to Gemini API)
import google.generativeai as genai

# After agent response, check usage metadata
response = model.generate_content("Hello")
print(response.usage_metadata)
# Output: prompt_tokens=5, candidates_tokens=10, total_tokens=15

# Calculate cost (Gemini 2.5 Flash pricing)
input_cost = (prompt_tokens / 1_000_000) * 0.30  # $0.30 per 1M input tokens
output_cost = (candidates_tokens / 1_000_000) * 2.50  # $2.50 per 1M output tokens
total_cost = input_cost + output_cost

# Workshop budget monitoring (50 participants, 10 queries each)
estimated_tokens_per_query = 1000  # Conservative estimate
total_queries = 50 * 10
total_tokens = total_queries * estimated_tokens_per_query
workshop_cost = (total_tokens / 1_000_000) * 2.80  # Avg of input/output
print(f"Estimated workshop cost: ${workshop_cost:.2f}")
```

### Anti-Patterns to Avoid
- **Direct session.state modification:** Never modify `session.state` directly outside managed contexts (bypasses event tracking, breaks persistence). Always use `append_event()` with `state_delta` or modify via `ToolContext.state`
- **Missing state key without `?`:** Using `{user:budget}` in instruction without `?` throws error if key missing. Use `{user:budget?}` for optional keys
- **InMemorySessionService in production:** Loses all state on restart, doesn't work in distributed systems. Use DatabaseSessionService or VertexAiSessionService for production
- **Assuming free tier for workshop:** Gemini has free tier, but rate limits may impact 50 concurrent participants. Set billing alerts

## Don't Hand-Roll

Problems that look simple but have existing solutions:

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Session persistence | Custom file/JSON storage | DatabaseSessionService (SQLite for dev) | Built-in event tracking, thread-safe, state prefix support, proper session lifecycle |
| Agent evaluation | Manual test scripts | AgentEvaluator with pytest | Trajectory validation, response matching, LLM-based grading, CI/CD integration |
| Token counting | String length estimates | response.usage_metadata | Exact tokenization (subword, not character), includes all model overhead |
| State injection | String formatting/f-strings | ADK curly-brace templating `{key}` | Automatic type conversion, optional key support `{key?}`, escaping handled |
| Deployment automation | Custom Docker/K8s setup | Vertex AI Agent Engine | Managed runtime, automatic scaling, session/memory GA support, ADK API server included |

**Key insight:** ADK provides complete lifecycle management (sessions, state, deployment, evaluation). Use built-in services rather than implementing custom infrastructure.

## Common Pitfalls

### Pitfall 1: Confusing Session Scope vs User Scope
**What goes wrong:** Developer stores user preferences without `user:` prefix, preferences lost when new session starts
**Why it happens:** Default state (no prefix) is session-scoped by design. State prefixes are "magic" and easy to overlook in documentation
**How to avoid:**
- Use `user:` prefix for any data that should persist across sessions (preferences, profile)
- Use no prefix for conversation-specific data (current search results, step tracking)
- Use `temp:` for invocation-only data (intermediate calculations, API responses)
**Warning signs:** User says "I told you my budget" but agent doesn't remember across sessions

### Pitfall 2: Deployment Prerequisites Not Ready
**What goes wrong:** `agent_engines.create()` fails with errors about missing bucket, APIs not enabled, permissions
**Why it happens:** Vertex AI Agent Engine requires GCP project setup (billing enabled, Vertex AI API, Cloud Storage API, staging bucket, IAM roles)
**How to avoid:**
- Enable Vertex AI and Cloud Storage APIs: `gcloud services enable aiplatform.googleapis.com storage.googleapis.com`
- Create staging bucket: `gsutil mb gs://YOUR_BUCKET`
- Ensure "Vertex AI User" and "Storage Admin" IAM roles
- Verify billing is active (Agent Engine is paid service)
**Warning signs:** InternalServerError 500, "staging_bucket" validation errors, "Revision not ready"

### Pitfall 3: Evaluation Test Data Mismatches Reality
**What goes wrong:** AgentEvaluator tests pass in test dataset but fail with real users
**Why it happens:** Golden dataset doesn't represent actual conversation patterns, edge cases, or tool call variations
**How to avoid:**
- Generate golden datasets from actual agent sessions using `adk web` UI
- Test multiple conversation paths (different user styles, error cases, budget ranges)
- Use appropriate thresholds (tool_trajectory_avg_score: 0.8 allows some variation)
- Include error handling tests (invalid dates, no results found, API failures)
**Warning signs:** 100% test pass rate but users report agent failures

### Pitfall 4: Free Tier Rate Limits in Workshop
**What goes wrong:** 50 concurrent participants hit Gemini API rate limits, agents timeout/fail
**Why it happens:** Free tier has per-minute quotas that don't scale to workshop concurrency
**How to avoid:**
- Enable billing and set budget alerts ($10-20 for typical workshop)
- Calculate expected usage: 50 users × 10 queries × 1000 tokens = 500K tokens (~$1.40)
- Test with 5-10 concurrent users before workshop
- Have backup plan (local InMemorySessionService works offline)
**Warning signs:** "Quota exceeded" errors, 429 status codes during workshop dry-run

### Pitfall 5: Instruction State Injection Without Optional Marker
**What goes wrong:** Agent instruction uses `{user:budget}` but throws error when state key doesn't exist
**Why it happens:** By default, missing keys cause errors. Question mark `?` makes keys optional
**How to avoid:**
- Always use `{user:budget?}` for optional state keys
- Initialize state with defaults: `state.setdefault("user:budget", None)`
- Handle missing values in instruction: "Budget: {user:budget?} (not set if empty)"
**Warning signs:** KeyError exceptions when new users interact with agent

## Code Examples

Verified patterns from official sources:

### Reading and Writing Session State
```python
# Source: https://google.github.io/adk-docs/sessions/state/
from google.adk.context import ToolContext

def save_user_preference(context: ToolContext, budget: int) -> str:
    """Save user's budget preference across sessions"""
    # Write with user: prefix - persists across all user sessions
    context.state["user:budget"] = budget

    # Write session-specific data - lost when session ends
    context.state["last_budget_update"] = "2026-01-24"

    # Write temp data - never persists, only in current invocation
    context.state["temp:validation_passed"] = True

    return f"I'll remember your ${budget} budget for future trips!"

# In agent instruction - inject state with optional marker
instruction = """You are a travel assistant.

User's saved budget: {user:budget?}
Last updated: {last_budget_update?}

If budget is set, apply it to all searches automatically.
If not set, ask for budget when showing prices.
"""
```

### Deploying to Vertex AI Agent Engine (Complete Flow)
```python
# Source: https://docs.cloud.google.com/agent-builder/agent-engine/quickstart-adk
import vertexai
from vertexai import agent_engines
from google.adk.agents import Agent

# 1. Initialize Vertex AI
PROJECT_ID = "your-project-id"
LOCATION = "us-central1"
STAGING_BUCKET = "gs://your-bucket-for-staging"

client = vertexai.Client(project=PROJECT_ID, location=LOCATION)

# 2. Create agent with tools
from tools import search_flights, search_hotels

agent = Agent(
    model="gemini-2.5-flash",
    name="travel_booking_assistant",
    description="Books flights and hotels with budget awareness",
    instruction="...",
    tools=[search_flights, search_hotels]
)

# 3. Wrap in AdkApp
app = agent_engines.AdkApp(agent=agent)

# 4. Deploy (takes ~3 minutes)
print("Deploying agent to Vertex AI Agent Engine...")
remote_agent = client.agent_engines.create(
    agent=app,
    config={
        "requirements": [
            "google-cloud-aiplatform[agent_engines,adk]>=1.112"
        ],
        "staging_bucket": STAGING_BUCKET,
        "display_name": "Travel Booking Workshop Agent"
    }
)

# 5. Get endpoint
endpoint = remote_agent.api_resource.name
print(f"Agent deployed! Endpoint: {endpoint}")
# projects/123456/locations/us-central1/reasoningEngines/789

# 6. Test deployed agent (same API as local)
async for event in remote_agent.async_stream_query(
    user_id="test_user",
    message="Find flights from SFO to Tokyo on March 15"
):
    if event.is_final_response():
        print(event.content.parts[0].text)

# 7. Cleanup (when done)
remote_agent.delete(force=True)
```

### AgentEvaluator Test Suite
```python
# Source: https://codelabs.developers.google.com/adk-eval/instructions
# tests/test_travel_agent.py
import pytest
from google.adk.evaluation.agent_evaluator import AgentEvaluator

@pytest.mark.asyncio
async def test_flight_search_with_budget():
    """Verify agent uses max_price parameter when budget mentioned"""
    await AgentEvaluator.evaluate(
        agent_module="agent",
        eval_dataset_file_path_or_dir="tests/flight_budget.test.json",
    )

@pytest.mark.asyncio
async def test_state_persistence():
    """Verify agent remembers user preferences across turns"""
    await AgentEvaluator.evaluate(
        agent_module="agent",
        eval_dataset_file_path_or_dir="tests/preference_memory.test.json",
    )

# tests/flight_budget.test.json
{
  "eval_set_id": "budget_filtering",
  "name": "Budget-Aware Flight Search",
  "eval_cases": [
    {
      "eval_id": "under_900_budget",
      "session_input": {
        "app_name": "travel_booking_assistant",
        "user_id": "eval_user"
      },
      "conversation": [
        {
          "user_content": {
            "role": "user",
            "parts": [{"text": "Find flights from SFO to Tokyo under $900"}]
          },
          "intermediate_data": {
            "tool_uses": [
              {
                "name": "search_flights",
                "args": {
                  "origin": "SFO",
                  "destination": "NRT",
                  "departure_date": "2026-03-15",
                  "max_price": 900
                }
              }
            ]
          },
          "final_response": {
            "role": "model",
            "parts": [{"text": "I found 1 flight under $900: United Airlines UA837 for $850"}]
          }
        }
      ]
    }
  ]
}

# Run tests
# pytest tests/test_travel_agent.py -v
```

### Cost Monitoring Dashboard (Simple)
```python
# Source: https://ai.google.dev/gemini-api/docs/pricing
import google.generativeai as genai
from dataclasses import dataclass
from typing import List

@dataclass
class TokenUsage:
    user_id: str
    query: str
    input_tokens: int
    output_tokens: int
    cost_usd: float

class WorkshopCostTracker:
    """Track token usage and costs during workshop"""

    def __init__(self):
        self.usage_log: List[TokenUsage] = []
        # Gemini 2.5 Flash pricing (as of 2026-01-24)
        self.input_price_per_1m = 0.30
        self.output_price_per_1m = 2.50

    def log_query(self, user_id: str, query: str, response):
        """Log token usage from agent response"""
        metadata = response.usage_metadata

        input_cost = (metadata.prompt_tokens / 1_000_000) * self.input_price_per_1m
        output_cost = (metadata.candidates_tokens / 1_000_000) * self.output_price_per_1m
        total_cost = input_cost + output_cost

        usage = TokenUsage(
            user_id=user_id,
            query=query,
            input_tokens=metadata.prompt_tokens,
            output_tokens=metadata.candidates_tokens,
            cost_usd=total_cost
        )
        self.usage_log.append(usage)

    def get_summary(self):
        """Get workshop cost summary"""
        total_input = sum(u.input_tokens for u in self.usage_log)
        total_output = sum(u.output_tokens for u in self.usage_log)
        total_cost = sum(u.cost_usd for u in self.usage_log)

        return {
            "total_queries": len(self.usage_log),
            "unique_users": len(set(u.user_id for u in self.usage_log)),
            "total_input_tokens": total_input,
            "total_output_tokens": total_output,
            "total_cost_usd": total_cost,
            "avg_cost_per_query": total_cost / len(self.usage_log) if self.usage_log else 0
        }

# Usage
tracker = WorkshopCostTracker()

# After each agent query
tracker.log_query(
    user_id="participant_1",
    query="Find flights to Tokyo",
    response=agent_response
)

# At end of workshop
summary = tracker.get_summary()
print(f"Workshop cost: ${summary['total_cost_usd']:.2f}")
print(f"Average per query: ${summary['avg_cost_per_query']:.4f}")
```

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| agent.generate_content() | Runner + InMemorySessionService | ADK 1.x (2025) | Proper session management, event streaming, production-ready pattern |
| Manual state in global variables | SessionService with state prefixes | ADK Sessions feature | Cross-session persistence (user:), app-wide config (app:), proper scoping |
| Custom Docker deployment | Vertex AI Agent Engine | GA Jan 2026 | Managed runtime, auto-scaling, no container management |
| Manual test scripts | AgentEvaluator with pytest | ADK Evaluation framework | Trajectory validation, LLM grading, CI/CD integration |
| FirestoreSessionService (community) | DatabaseSessionService official | ADK 1.x | Built-in SQL persistence (PostgreSQL, MySQL, SQLite) |

**Deprecated/outdated:**
- **agent.generate_content()**: Does not exist in ADK. Use Runner.run_async() pattern
- **ReasoningEngine (preview)**: Replaced by Vertex AI Agent Engine (GA as of Jan 2026)
- **Manual state tracking**: Use SessionService.state with prefixes instead of custom persistence

## Open Questions

Things that couldn't be fully resolved:

1. **Workshop Deployment Scope**
   - What we know: Deployment requires GCP project setup (billing, APIs, bucket creation, ~10 minutes setup time)
   - What's unclear: Is 15-20 minute allocation sufficient for hands-on deployment, or should it be demonstration-only?
   - Recommendation: Demonstrate deployment in instructor walkthrough, provide deployment guide for post-workshop. Focus hands-on time on state management (immediately useful, works in Colab)

2. **Cost Monitoring Integration**
   - What we know: Gemini API provides usage_metadata, pricing is $0.30-$2.50 per 1M tokens
   - What's unclear: Should workshop include live cost dashboard, or just document monitoring patterns?
   - Recommendation: Provide simple cost tracker example (code above), document monitoring. Real-time dashboard adds complexity without educational value for beginners

3. **AgentEvaluator Scope**
   - What we know: AgentEvaluator requires test dataset creation, pytest setup, understanding of trajectory vs response evaluation
   - What's unclear: Should workshop include hands-on test writing, or reference material only?
   - Recommendation: Provide reference tests (agent validates booking flow), document evaluation process. Full test suite creation exceeds 15-minute allocation

4. **Session Persistence Choice**
   - What we know: InMemorySessionService already used (Exercises 1-3), DatabaseSessionService requires database setup, VertexAiSessionService requires Agent Engine deployment
   - What's unclear: Should workshop switch to DatabaseSessionService (SQLite) for "real" persistence?
   - Recommendation: Keep InMemorySessionService, teach state prefixes (user:) for cross-session behavior. Database setup distracts from core learning (state management patterns)

## Sources

### Primary (HIGH confidence)
- [ADK Sessions Documentation](https://google.github.io/adk-docs/sessions/) - Session, State, Memory concepts
- [ADK State Management](https://google.github.io/adk-docs/sessions/state/) - State prefixes, injection, persistence
- [Vertex AI Agent Engine Deployment](https://docs.cloud.google.com/agent-builder/agent-engine/deploy) - Deployment methods, configuration
- [ADK Quickstart with Agent Engine](https://docs.cloud.google.com/agent-builder/agent-engine/quickstart-adk) - Complete development to deployment flow
- [ADK Evaluation Documentation](https://google.github.io/adk-docs/evaluate/) - AgentEvaluator overview
- [Evaluating Agents Codelab](https://codelabs.developers.google.com/adk-eval/instructions) - Complete evaluation tutorial with examples
- [Gemini API Pricing](https://ai.google.dev/gemini-api/docs/pricing) - Token costs, free tier limits

### Secondary (MEDIUM confidence)
- [Remember this: Agent state and memory with ADK](https://cloud.google.com/blog/topics/developers-practitioners/remember-this-agent-state-and-memory-with-adk) - Google Cloud Blog post on state management
- [Agent Engine Troubleshooting](https://docs.cloud.google.com/agent-builder/agent-engine/troubleshooting/deploy) - Common deployment errors
- [ADK DatabaseSessionService Guide](https://medium.com/google-cloud/building-persistent-sessions-with-google-adk-a-comprehensive-guide-c3bab191269d) - Community guide on persistent sessions
- [Extending ADK with Firestore](https://medium.com/google-cloud/extending-google-adk-building-a-custom-session-service-with-firestore-0fc4b74354bf) - Custom session service implementation

### Tertiary (LOW confidence)
- Multiple Medium articles on ADK sessions and deployment (2025-2026) - Community perspectives, not official documentation
- GitHub issues/discussions on AgentEvaluator, DatabaseSessionService - Real-world usage patterns

## Metadata

**Confidence breakdown:**
- Standard stack: MEDIUM - Official ADK 1.23.0 verified, Agent Engine pricing started Jan 28 2026 (very recent), pytest integration well-documented
- Architecture: MEDIUM - State prefix patterns from official docs (HIGH), deployment flow verified in quickstart (HIGH), cost monitoring extrapolated from pricing docs (MEDIUM)
- Pitfalls: MEDIUM - State scope confusion from official warnings (HIGH), deployment prerequisites from troubleshooting docs (HIGH), workshop rate limits estimated from pricing/quotas (LOW)

**Research date:** 2026-01-24
**Valid until:** 2026-02-24 (30 days - ADK is stable, but Agent Engine pricing/features may evolve)
