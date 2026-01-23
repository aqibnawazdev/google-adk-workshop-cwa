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

## Quick Start

### In Google Colab (Recommended)

1. Upload this folder to Colab or clone from workshop repo
2. Run the setup cell (authentication + install)
3. Import and test:

```python
from agent import create_agent

agent = create_agent()
response = agent.generate_content("Plan a trip to Japan for me")
print(response.text)
```

### Locally

1. Copy `.env.template` to `.env` and fill in your project ID
2. Authenticate: `gcloud auth application-default login`
3. Run: `python agent.py` or `adk run agent.py`

## File Structure

```
reference-implementation/
├── agent.py          # Main agent implementation
├── .env.template     # Configuration template
└── README.md         # This file
```

## Workshop Progression

| Exercise | What You'll Add | Files Modified |
|----------|-----------------|----------------|
| 1. Hello Agent | Basic agent creation | agent.py (base) |
| 2. Function Calling | search_flights, search_hotels | agent.py (tools) |
| 3. RAG Integration | Destination knowledge base | agent.py (knowledge) |
| 4. Sessions | Preference memory | agent.py (session_config) |

## Testing

Quick test to verify the agent works:

```bash
python -c "from agent import create_agent; a = create_agent(); print(a.generate_content('Hello').text)"
```

## Need Help?

- Workshop troubleshooting guide: [Link]
- ADK documentation: https://google.github.io/adk-docs/
- Instructor contact: [Workshop-specific]
