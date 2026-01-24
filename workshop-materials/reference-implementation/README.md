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

## File Structure

```
reference-implementation/
├── agent.py          # Agent definition and configuration
├── tools.py          # Tool function implementations (flights, hotels)
├── rag_tools.py      # RAG retrieval tool configuration (Exercise 3)
├── hybrid_agent.py   # Hybrid coordinator pattern (Exercise 3)
├── README.md         # This file
└── .env.template     # Environment configuration
```

## Workshop Progression

| Exercise | What You'll Add | Files Modified |
|----------|-----------------|----------------|
| 1. Hello Agent | Basic agent creation | agent.py (base) |
| 2. Function Calling | search_flights, search_hotels | agent.py (tools) |
| 3. RAG Integration | Destination knowledge base | agent.py (knowledge) |
| 4. Sessions | Preference memory | agent.py (session_config) |

## Testing

Quick test to verify the agent can be created:

```bash
python -c "from agent import create_agent; a = create_agent(); print(f'Agent created: {a.name}')"
```

For full agent testing with conversations, use the workshop notebooks which have the proper async Runner pattern.

## Need Help?

- Workshop troubleshooting guide: [Link]
- ADK documentation: https://google.github.io/adk-docs/
- Instructor contact: [Workshop-specific]
