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
├── agent.py      # Agent definition and configuration
├── tools.py      # Tool function implementations
├── README.md     # This file
└── .env.template # Environment configuration
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
