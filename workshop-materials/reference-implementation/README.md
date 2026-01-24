# Travel Booking Assistant - Reference Implementation

This is the complete implementation you'll build throughout the workshop.
Each section of the code is labeled with the exercise where you'll learn to build it.

## What This Agent Does

The Travel Booking Assistant can:
- **Search flights** between any airports (Exercise 2: Function Calling)
- **Find hotels** in any destination (Exercise 2: Function Calling)
- **Provide destination knowledge** like visa requirements, attractions, weather (Exercise 3: RAG)
- **Remember your preferences** across the conversation (Exercise 4: Sessions)

## Architecture Overview

```
┌─────────────────────────────────────────────────────┐
│                    ADK Agent                         │
│  ┌───────────────────────────────────────────────┐  │
│  │              Gemini 2.5 Flash                 │  │
│  │         (Conversational Intelligence)         │  │
│  └───────────────────────────────────────────────┘  │
│                         │                           │
│    ┌────────────────────┼────────────────────┐     │
│    ▼                    ▼                    ▼     │
│ ┌──────┐          ┌──────────┐        ┌──────────┐ │
│ │Tools │          │ Knowledge│        │ Session  │ │
│ │(Ex 2)│          │  (Ex 3)  │        │  (Ex 4)  │ │
│ └──────┘          └──────────┘        └──────────┘ │
│    │                    │                    │     │
│    ▼                    ▼                    ▼     │
│ ┌──────┐          ┌──────────┐        ┌──────────┐ │
│ │Flight│          │ Vertex AI│        │ Vertex AI│ │
│ │Hotel │          │   RAG    │        │ Sessions │ │
│ │ APIs │          │          │        │          │ │
│ └──────┘          └──────────┘        └──────────┘ │
└─────────────────────────────────────────────────────┘
```

## Tools vs RAG: Decision Framework

This agent demonstrates the key decision: **when to use function calling vs knowledge retrieval**.

| Use Case | Approach | Why |
|----------|----------|-----|
| Flight availability | **Tool** (search_flights) | Data changes every minute |
| Hotel pricing | **Tool** (search_hotels) | Inventory updates constantly |
| Destination guides | **RAG** (Exercise 3) | Static content, rarely changes |
| Visa requirements | **RAG** (Exercise 3) | Updated infrequently |

**The Key Question:** Does this data change while the user is talking to the agent?
- **YES** -> Use a Tool (function calling)
- **NO** -> Use RAG (knowledge retrieval)

For a comprehensive decision framework with flowcharts and common mistakes, see [Context Engineering Guide](../CONTEXT-ENGINEERING.md).

## Available Tools

### search_flights

Search for available flights between airports.

**Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| origin | str | Yes | Departure airport code (SFO, LAX, JFK) |
| destination | str | Yes | Arrival airport code (NRT, CDG, LHR) |
| departure_date | str | Yes | Date in YYYY-MM-DD format |
| passengers | int | No | Number of passengers (default: 1) |
| max_price | int | No | Maximum price per person in USD |

**Available Routes:** SFO->NRT, LAX->CDG, JFK->LHR

**Example Response:**
```json
{
  "status": "success",
  "flights": [
    {"airline": "United Airlines", "flight_number": "UA837", "price": 850, ...}
  ],
  "route": "SFO -> NRT",
  "currency": "USD"
}
```

### search_hotels

Search for available hotels in a destination.

**Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| location | str | Yes | City name (Tokyo, Paris, London) |
| check_in | str | Yes | Check-in date in YYYY-MM-DD format |
| check_out | str | Yes | Check-out date in YYYY-MM-DD format |
| guests | int | No | Number of guests (default: 1) |
| max_price_per_night | int | No | Maximum price per night in USD |

**Available Locations:** Tokyo, Paris, London

**Example Response:**
```json
{
  "status": "success",
  "hotels": [
    {"name": "Park Hyatt Tokyo", "stars": 5, "price_per_night": 450, ...}
  ],
  "location": "Tokyo",
  "nights": 5
}
```

## Error Handling Pattern

Tools return error information in the response (not exceptions) so the LLM can help users fix issues:

```json
{
  "status": "error",
  "error_message": "Invalid date format: 'march 15'. Use YYYY-MM-DD format.",
  "example": "2026-03-15"
}
```

This "errors-in-context" pattern lets the agent:
- Explain what went wrong
- Suggest how to fix it
- Offer alternatives

## RAG Knowledge Integration

### Overview

Starting in Exercise 3, you'll add a knowledge base of destination guides using Vertex AI RAG Engine. This gives your agent access to static information like visa requirements, attractions, weather, and cultural tips.

### Why RAG Complements Tools

The key decision: **Does this data change while the user is talking to the agent?**

**Use Tools (Function Calling) when:**
- Data changes every minute (flight availability, hotel pricing)
- Requires real-time API calls
- Need current status or live calculations

**Use RAG (Knowledge Retrieval) when:**
- Data is static or slow-changing (destination guides, visa policies)
- Information already exists in documents
- Need semantic search across large corpus

**Example queries:**
```
"Find flights to Tokyo on March 15"           → Tool (search_flights)
"What's the best time to visit Tokyo?"        → RAG (seasonal guide)
"Show hotels in Shibuya under $200/night"     → Tool (search_hotels)
"What are visa requirements for Japan?"       → RAG (policy document)
"What cultural customs should I know?"        → RAG (destination guide)
```

### Tools vs RAG Decision Framework

```
User Query
    ↓
Does this need REAL-TIME data?
(prices, availability, current status)
    ↓
   YES → Use FUNCTION CALLING TOOLS
         (search_flights, search_hotels)
    ↓
    NO → Is this STATIC KNOWLEDGE?
          (guides, policies, cultural info)
    ↓
   YES → Use RAG RETRIEVAL
         (destination_knowledge)
    ↓
    NO → General knowledge
          LLM can answer directly
```

### Files Added in Exercise 3

```
reference-implementation/
├── rag_tools.py          # RAG retrieval tool configuration
├── hybrid_agent.py       # Combines tools + RAG (workaround pattern)
└── agent.py             # Updated with RAG integration
```

### Quick Start with RAG

**1. Set up environment:**
```bash
# Add to your .env file (workshop corpus pre-indexed with 10 destination guides)
RAG_CORPUS_ID=projects/674082857580/locations/europe-west1/ragCorpora/7493989779944505344
```

The corpus ID above is pre-configured for the workshop. If running your own corpus, replace with your ID.

**2. Configure RAG tool:**
```python
from rag_tools import destination_knowledge

# Pre-configured RAG retrieval tool
# - Searches destination guide corpus
# - Returns top 5 most relevant chunks
# - Filters by similarity threshold (0.6)
```

**3. Create RAG-only agent:**
```python
from google.adk.agents import Agent
from rag_tools import destination_knowledge

destination_expert = Agent(
    model='gemini-2.5-flash',
    name='destination_expert',
    tools=[destination_knowledge],  # ONLY RAG tool
)
```

**Important constraint:** Vertex AI RAG retrieval tool cannot be mixed with function calling tools in the same agent. See hybrid pattern below.

### Hybrid Agent Pattern

To provide both real-time booking AND destination knowledge, use the hybrid coordination pattern:

```python
from hybrid_agent import HybridTravelAssistant

# Creates two specialized agents:
# - booking_agent: Has search_flights and search_hotels tools
# - destination_agent: Has RAG retrieval tool only
#
# Coordinator routes queries based on intent:
# - "Find flights..." → booking agent
# - "What are visa requirements..." → destination agent
# - "Find flights to Tokyo..." → booking agent + destination enrichment

assistant = HybridTravelAssistant()
response = assistant.assist("Find flights to Tokyo and tell me about the culture")
# Returns: Flight results + Tokyo cultural tips from knowledge base
```

**Why this pattern?**
- ADK constraint: RAG tool cannot mix with function calling tools
- Solution: Separate specialized agents with coordination logic
- Intent detection routes to appropriate agent
- Results can be combined for comprehensive answers

**Pattern comparison:**

| Pattern | Capabilities | When to Use |
|---------|-------------|-------------|
| Tools-only agent | Real-time search | Phase 2, before RAG |
| RAG-only agent | Static knowledge | Testing RAG, knowledge-focused queries |
| Hybrid coordinator | Tools + RAG | Production use, comprehensive assistance |

See `hybrid_agent.py` for full implementation with intent detection, routing logic, and result enrichment.

### RAG Tool Description Pattern

Critical for correct tool selection: use explicit DO/DO NOT sections in RAG tool descriptions.

**Bad (vague):**
```python
description='Get information about travel destinations.'
```

**Good (explicit):**
```python
description='''Retrieve destination information from travel guide knowledge base.

USE THIS TOOL to answer questions about:
- Visa requirements and entry rules
- Top attractions and landmarks
- Weather and best time to visit
- Cultural tips and local customs
- Safety information
- Transportation within city

DO NOT use this tool for:
- Real-time flight or hotel availability → use search_flights/search_hotels
- Current pricing or booking status → use search tools
- Live event schedules → real-time data not in guides
'''
```

Without DO/DO NOT boundaries, the LLM may call RAG for real-time queries or call tools for static knowledge.

### Environment Variables

```bash
# Required for RAG integration (workshop corpus)
RAG_CORPUS_ID=projects/674082857580/locations/europe-west1/ragCorpora/7493989779944505344

# Optional tuning parameters (defaults shown)
RAG_SIMILARITY_TOP_K=5          # Number of chunks to retrieve
RAG_VECTOR_THRESHOLD=0.6        # Minimum similarity score (0.0-1.0)
```

### Troubleshooting RAG

**Issue: "RAG_CORPUS_ID not set"**
- Cause: Environment variable missing
- Fix: Add `RAG_CORPUS_ID=projects/.../ragCorpora/...` to .env file
- Get corpus ID from instructor or workshop materials

**Issue: "No relevant information found"**
- Cause: Query doesn't match any destination guides
- Fix: Check corpus contains guide for that destination
- Or: Lower `RAG_VECTOR_THRESHOLD` to be more permissive

**Issue: "Retrieved chunks seem irrelevant"**
- Cause: Similarity threshold too low
- Fix: Increase `RAG_VECTOR_THRESHOLD` (try 0.7 or 0.8)
- Or: Reduce `RAG_SIMILARITY_TOP_K` to return fewer chunks

**Issue: "Agent calls RAG for real-time queries"**
- Cause: Vague RAG tool description
- Fix: Add explicit DO/DO NOT sections (see pattern above)
- Ensure tool description clearly states "static guides, not live data"

**Issue: "Cannot mix RAG with function calling tools"**
- Cause: Tried to add destination_knowledge to tools list with search_flights/search_hotels
- Fix: Use hybrid pattern (see `hybrid_agent.py`)
- Create separate agents: one for tools, one for RAG

## Quick Start

### In Google Colab (Recommended)

1. Upload this folder to Colab or clone from workshop repo
2. Run the setup cell (authentication + install)
3. Use the workshop notebooks (01-hello-agent.ipynb, 02-tools-functions.ipynb) which have the proper async Runner pattern for testing agents

### Locally

1. Copy `.env.template` to `.env` and fill in your project ID
2. Authenticate: `gcloud auth application-default login`
3. Run: `python agent.py` or `adk run agent.py`

## State Management

Exercise 4 introduces persistent state using ADK's state prefix system. This allows the agent to remember user preferences across conversations.

### State Prefixes

| Prefix | Scope | Persistence | Use Case |
|--------|-------|-------------|----------|
| (none) | Session | Current conversation only | Temp data, context |
| `user:` | User | Across all user sessions | Preferences, settings |
| `temp:` | Invocation | Single tool call | Intermediate calculations |
| `app:` | Application | All users, all sessions | Global config |

### Preference Storage

The agent can remember and apply user preferences:

```python
from state_utils import remember_preference, get_preference

# In agent tools list:
tools=[search_flights, search_hotels, remember_preference, get_preference, clear_preference]

# User says: "Remember my budget is $1500"
# Agent calls: remember_preference("budget", "1500", tool_context)
# Stored as: tool_context.state["user:budget"] = 1500
```

### State Injection

Inject saved preferences into agent instructions using `{key?}` syntax:

```python
instruction='''You are a travel assistant.

Current user preferences:
- Budget: ${user:budget?} (empty if not set)
- Travel style: {user:travel_style?}

If a preference is set, apply it automatically to searches.
'''
```

The `?` makes injection optional - no error if key is missing.

### Supported Preferences

| Preference | State Key | Example Value |
|------------|-----------|---------------|
| Budget | `user:budget` | 1500 |
| Travel style | `user:travel_style` | "luxury" |
| Dietary restrictions | `user:dietary_restrictions` | ["vegetarian", "halal"] |
| Preferred airlines | `user:preferred_airlines` | ["United", "ANA"] |
| Min hotel rating | `user:hotel_rating_min` | 4 |

See `state_utils.py` for complete implementation.

---

## Deployment

Deploy your agent to Vertex AI Agent Engine for production use.

### Quick Deployment

```bash
# Set environment
export GOOGLE_CLOUD_PROJECT="your-project-id"
export STAGING_BUCKET="gs://your-bucket-adk-staging"

# Deploy
python deploy.py --action deploy

# Test deployed agent
python deploy.py --action test --endpoint "projects/.../reasoningEngines/..."

# Cleanup (important - stops billing!)
python deploy.py --action cleanup --endpoint "projects/.../reasoningEngines/..."
```

### Prerequisites

1. GCP project with Vertex AI enabled
2. Cloud Storage bucket for staging
3. IAM roles: `aiplatform.user`, `storage.objectCreator`
4. Python packages: `google-cloud-aiplatform>=1.60.0`, `google-adk`

### What Deployment Provides

- Managed infrastructure (no servers to maintain)
- Built-in session management
- Secure HTTPS endpoints with IAM auth
- Integrated monitoring and logging
- Automatic scaling

See [DEPLOYMENT.md](../DEPLOYMENT.md) for complete documentation.

---

## Testing with AgentEvaluator

The `tests/` directory contains reference tests using ADK's AgentEvaluator framework.

### Running Tests

```bash
# Install test dependencies
pip install pytest pytest-asyncio

# Run all tests
pytest tests/ -v

# Run specific test
pytest tests/test_travel_agent.py::test_flight_search -v
```

### Test Structure

```
tests/
├── README.md                       # Test documentation
├── test_travel_agent.py            # pytest test file
├── conftest.py                     # pytest configuration
└── eval_datasets/                  # Golden test data
    ├── flight_search.test.json     # Flight search scenarios
    └── preference_memory.test.json # Preference persistence scenarios
```

### What AgentEvaluator Tests

| Metric | Description | Default Threshold |
|--------|-------------|-------------------|
| `tool_trajectory_avg_score` | Tool call accuracy | >= 0.8 |
| `response_match_score` | Response quality | >= 0.7 |

Golden datasets define expected tool calls in `intermediate_data.tool_uses` and expected response patterns in `final_response`.

See `tests/README.md` for writing custom test scenarios.

---

## Cost Monitoring

Track API costs during workshop sessions and estimate production budgets.

### Using the Cost Tracker

```python
from cost_tracker import WorkshopCostTracker, estimate_workshop_cost

# Track individual queries
tracker = WorkshopCostTracker()

# Option 1: From ADK response with usage_metadata
tracker.log_query(response, query="Find flights to Tokyo")

# Option 2: Log tokens directly
tracker.log_tokens_directly(input_tokens=500, output_tokens=200)

# Get summary
summary = tracker.get_summary()
print(f"Total cost: ${summary.total_cost_usd:.4f}")

# Print formatted report
tracker.print_report()
```

### Gemini 2.5 Flash Pricing

| Token Type | Price per 1M Tokens |
|------------|---------------------|
| Input | $0.30 |
| Output (thinking mode) | $2.50 |

### Workshop Cost Estimation

```python
estimate = estimate_workshop_cost(
    participants=25,
    queries_per_participant=20,
    avg_input_tokens=500,
    avg_output_tokens=200
)
print(f"Estimated workshop cost: ${estimate['total_cost']:.2f}")
# ~$0.33 for a 25-person workshop
```

See `cost_tracker.py` for complete implementation.

---

## File Structure

```
reference-implementation/
├── agent.py          # Agent definition and configuration
├── tools.py          # Tool function implementations (flights, hotels)
├── rag_tools.py      # RAG retrieval tool configuration (Exercise 3)
├── hybrid_agent.py   # Hybrid coordinator pattern (Exercise 3)
├── state_utils.py    # State management utilities (Exercise 4)
├── deploy.py         # Vertex AI Agent Engine deployment script
├── cost_tracker.py   # Token usage and cost tracking utility
├── tests/            # AgentEvaluator test suite
│   ├── test_travel_agent.py
│   ├── conftest.py
│   └── eval_datasets/
├── README.md         # This file
└── .env.template     # Environment configuration
```

## Workshop Progression

| Exercise | What You'll Add | Files Modified |
|----------|-----------------|----------------|
| 1. Hello Agent | Basic agent creation | agent.py (base) |
| 2. Function Calling | search_flights, search_hotels | agent.py, tools.py |
| 3. RAG Integration | Destination knowledge base | agent.py, rag_tools.py, hybrid_agent.py |
| 4. Sessions | Preference memory | agent.py, state_utils.py |

### Post-Workshop Exploration

| Topic | Files | Documentation |
|-------|-------|---------------|
| Deployment | deploy.py | [DEPLOYMENT.md](../DEPLOYMENT.md) |
| Testing | tests/ | tests/README.md |
| Cost tracking | cost_tracker.py | This file |

## Testing

Quick test to verify the agent can be created:

```bash
python -c "from agent import create_agent; a = create_agent(); print(f'Agent created: {a.name}')"
```

For full agent testing with conversations, use the workshop notebooks which have the proper async Runner pattern.

For automated testing with golden datasets, see the Testing section above.

---

## Beyond the Workshop

Ready to take your agent to production? Use our AI-agent-specific production readiness checklist:

**[Production Readiness Checklist](../PRODUCTION-READINESS.md)**

Covers:
- **Evaluation:** Golden datasets, AgentEvaluator, human review loops
- **Observability:** Logging, tracing, alerting for LLM systems
- **Cost Management:** Token tracking, budget alerts, model routing
- **Reliability:** Error handling, failover, rollback procedures

Start with the MVP checklist (Day 1-7), then progress to Mature production (Week 2+).

---

## Need Help?

- Workshop troubleshooting guide: [Link]
- ADK documentation: https://google.github.io/adk-docs/
- Instructor contact: [Workshop-specific]
