# Architecture Research

**Domain:** ADK Workshop - Travel Booking Agent
**Researched:** 2026-01-23
**Confidence:** HIGH

## Standard Architecture

### System Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                    WORKSHOP MATERIALS LAYER                      │
├─────────────────────────────────────────────────────────────────┤
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐        │
│  │Tutorial  │  │ Starter  │  │Solutions │  │Reference │        │
│  │   Docs   │  │   Code   │  │   Code   │  │   Impl   │        │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘        │
│       │             │              │             │              │
│       └─────────────┴──────────────┴─────────────┘              │
│                          │                                       │
├──────────────────────────┼───────────────────────────────────────┤
│                    AGENT APPLICATION LAYER                       │
├──────────────────────────┴───────────────────────────────────────┤
│  ┌───────────────────────────────────────────────────────┐      │
│  │                   Root Agent                           │      │
│  │  (Orchestration + Conversation Management)             │      │
│  └───────────┬──────────────────────────┬─────────────────┘      │
│              │                          │                        │
│  ┌───────────▼──────────┐  ┌───────────▼──────────┐             │
│  │   Tools Layer        │  │   Knowledge Layer    │             │
│  │  (Function Calling)  │  │       (RAG)          │             │
│  ├──────────────────────┤  ├──────────────────────┤             │
│  │ - Search Hotels      │  │ - Destination Corpus │             │
│  │ - Search Flights     │  │ - Embedding Store    │             │
│  │ - Check Availability │  │ - Retrieval Engine   │             │
│  └──────────────────────┘  └──────────────────────┘             │
├─────────────────────────────────────────────────────────────────┤
│                   INFRASTRUCTURE LAYER                           │
├─────────────────────────────────────────────────────────────────┤
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │   Session    │  │    Vertex    │  │   Gemini     │          │
│  │   Service    │  │ RAG Engine   │  │     API      │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
└─────────────────────────────────────────────────────────────────┘
```

### Component Responsibilities

| Component | Responsibility | Typical Implementation |
|-----------|----------------|------------------------|
| Tutorial Docs | Progressive learning material with concept explanations | Markdown files with code snippets, diagrams, ADK concepts |
| Starter Code | Scaffolded boilerplate for participants to build upon | Partial agent.py with TODOs, test stubs, config templates |
| Solutions Code | Complete implementations with detailed comments | Fully working agent.py per exercise, explanation docs |
| Reference Implementation | Production-grade example demonstrating best practices | Complete agent with all features, deployment config, tests |
| Root Agent | Orchestrates tools and RAG, manages conversation flow | ADK LlmAgent with tools list, system prompt, session config |
| Tools Layer | Function calling for real-time data (booking APIs) | ADK Function Tools wrapping mock/real booking APIs |
| Knowledge Layer | RAG for static knowledge (destination info) | Vertex AI RAG Engine with GCS-backed document corpus |
| Session Service | Persists conversation state and user preferences | VertexAiSessionService with state management |
| Vertex RAG Engine | Embedding creation and semantic retrieval | Managed Vertex AI service with pre-indexed documents |
| Gemini API | LLM inference for agent reasoning and responses | Gemini model via Vertex AI integration |

## Recommended Project Structure

### Workshop Materials Organization

```
workshop-root/
├── docs/                          # Tutorial documentation
│   ├── 00-setup.md                # GCP and ADK environment setup
│   ├── 01-basic-agent.md          # Exercise 1: Simple conversational agent
│   ├── 02-function-calling.md     # Exercise 2: Add booking search tools
│   ├── 03-rag-integration.md      # Exercise 3: Add destination knowledge
│   ├── 04-session-management.md   # Exercise 4: Add conversation state
│   ├── 05-deployment.md           # Deploy to Vertex AI
│   └── concepts/                  # Deep-dive concept explanations
│       ├── context-engineering.md
│       ├── tools-vs-rag.md
│       └── agent-architecture.md
├── exercises/                     # Starter code for each exercise
│   ├── exercise-01-basic-agent/
│   │   ├── travel_agent/
│   │   │   ├── agent.py           # Partial implementation with TODOs
│   │   │   ├── prompts.py         # Starter prompts
│   │   │   └── __init__.py
│   │   ├── tests/
│   │   │   └── test_agent.py      # Test cases to validate completion
│   │   ├── .env.example
│   │   └── pyproject.toml
│   ├── exercise-02-function-calling/
│   │   ├── travel_agent/
│   │   │   ├── agent.py           # Builds on ex-01, adds TODO for tools
│   │   │   ├── tools/
│   │   │   │   ├── booking_tools.py  # Stub functions with TODOs
│   │   │   │   └── __init__.py
│   │   │   ├── prompts.py
│   │   │   └── __init__.py
│   │   ├── tests/
│   │   ├── .env.example
│   │   └── pyproject.toml
│   ├── exercise-03-rag-integration/
│   │   ├── travel_agent/
│   │   │   ├── agent.py           # Adds RAG tool integration
│   │   │   ├── tools/
│   │   │   │   ├── booking_tools.py
│   │   │   │   └── __init__.py
│   │   │   ├── data/              # Sample destination documents
│   │   │   │   └── destinations/
│   │   │   ├── prompts.py
│   │   │   └── __init__.py
│   │   ├── scripts/
│   │   │   └── setup_rag.py       # RAG corpus setup script
│   │   ├── tests/
│   │   ├── .env.example
│   │   └── pyproject.toml
│   └── exercise-04-session-management/
│       ├── travel_agent/
│       │   ├── agent.py           # Adds session state management
│       │   ├── tools/
│       │   ├── prompts.py
│       │   └── __init__.py
│       ├── tests/
│       ├── .env.example
│       └── pyproject.toml
├── solutions/                     # Complete implementations with explanations
│   ├── exercise-01-solution/
│   │   ├── travel_agent/
│   │   │   └── agent.py           # Fully working code
│   │   ├── EXPLANATION.md         # Line-by-line walkthrough
│   │   └── pyproject.toml
│   ├── exercise-02-solution/
│   ├── exercise-03-solution/
│   └── exercise-04-solution/
├── reference/                     # Production-grade complete implementation
│   ├── travel_booking_agent/
│   │   ├── agent.py               # Complete agent with all features
│   │   ├── tools/
│   │   │   ├── booking_tools.py   # Full booking API integration
│   │   │   ├── preference_tools.py
│   │   │   └── __init__.py
│   │   ├── data/
│   │   │   └── destinations/      # Full destination corpus
│   │   ├── prompts.py
│   │   ├── config.py
│   │   └── __init__.py
│   ├── deployment/
│   │   ├── deploy.sh              # Vertex AI deployment script
│   │   └── cloudbuild.yaml
│   ├── eval/
│   │   ├── test_cases.json        # Evaluation scenarios
│   │   └── run_eval.py
│   ├── tests/
│   │   ├── test_agent.py
│   │   ├── test_tools.py
│   │   └── test_integration.py
│   ├── .env.example
│   ├── pyproject.toml
│   └── README.md
├── data/                          # Shared data for workshop
│   ├── destinations/              # Destination knowledge documents
│   │   ├── paris.md
│   │   ├── tokyo.md
│   │   └── new-york.md
│   └── mock-data/                 # Mock booking API responses
│       ├── hotels.json
│       └── flights.json
├── scripts/                       # Utility scripts
│   ├── setup_gcp.sh               # GCP project initialization
│   ├── create_rag_corpus.py       # Batch RAG corpus creation
│   └── verify_setup.py            # Pre-workshop validation
└── README.md                      # Workshop overview and structure
```

### Agent Application Structure (Per Exercise)

```
exercise-name/
├── travel_agent/              # Main agent package
│   ├── agent.py               # Root agent definition and orchestration
│   ├── prompts.py             # System prompts and instructions
│   ├── config.py              # Configuration and constants
│   ├── tools/                 # Function calling tools
│   │   ├── booking_tools.py   # Hotel/flight search tools
│   │   ├── preference_tools.py # User preference management
│   │   └── __init__.py
│   ├── data/                  # Static data and RAG documents
│   │   └── destinations/      # Destination knowledge base
│   └── __init__.py
├── tests/                     # Test suite
│   ├── test_agent.py          # Agent behavior tests
│   ├── test_tools.py          # Tool unit tests
│   └── conftest.py            # Pytest fixtures
├── scripts/                   # Helper scripts
│   ├── setup_rag.py           # RAG corpus initialization
│   └── run_local.py           # Local testing interface
├── .env.example               # Environment template
├── pyproject.toml             # Poetry dependencies
└── README.md                  # Exercise-specific instructions
```

### Structure Rationale

- **Progressive Exercises:** Each exercise folder is self-contained with all dependencies, allowing participants to start fresh or continue from previous checkpoints without complex merging
- **Starter Code with TODOs:** Exercise folders include partial implementations marked with TODO comments at strategic points, guiding participants on what to implement without overwhelming them
- **Solutions Separate from Exercises:** Clean separation prevents accidental spoilers while browsing, and EXPLANATION.md files provide educational commentary beyond just working code
- **Reference vs Solutions:** Solutions show "how to complete the exercise" while reference shows "how to build production-grade" - different purposes and quality bars
- **Shared Data Directory:** Central data folder prevents duplication across exercises and makes it easy to update mock data or destination documents once
- **Tools in Package:** Tools live in `tools/` subdirectory rather than separate packages to keep related functionality grouped and simplify imports for beginners
- **Test Co-location:** Tests mirror source structure but stay in separate `tests/` directory following Python conventions, with pytest fixtures for common setup

## Architectural Patterns

### Pattern 1: Progressive Complexity in Workshop Structure

**What:** Each exercise builds incrementally on previous concepts, isolating one new ADK feature per exercise

**When to use:** Workshop learning environments where participants need checkpoints and concept isolation

**Trade-offs:**
- Pros: Accommodates different learning paces, allows skipping ahead, reduces cognitive load
- Cons: More boilerplate duplication across exercises, requires careful dependency management between exercises

**Example:**
```
Exercise 1: Basic agent (just LLM + prompt)
Exercise 2: + Function calling (booking tools)
Exercise 3: + RAG (destination knowledge)
Exercise 4: + Sessions (conversation state)
```

**Progressive feature addition:**
```python
# Exercise 1: Basic agent
agent = LlmAgent(
    model="gemini-2.0-flash",
    system_instruction=TRAVEL_AGENT_PROMPT,
)

# Exercise 2: Add tools
agent = LlmAgent(
    model="gemini-2.0-flash",
    system_instruction=TRAVEL_AGENT_PROMPT,
    tools=[search_hotels, search_flights],  # NEW
)

# Exercise 3: Add RAG
agent = LlmAgent(
    model="gemini-2.0-flash",
    system_instruction=TRAVEL_AGENT_PROMPT,
    tools=[
        search_hotels,
        search_flights,
        VertexAiRagRetrieval(corpus_name="destinations"),  # NEW
    ],
)

# Exercise 4: Add sessions
session_service = VertexAiSessionService(project_id=PROJECT_ID)  # NEW
agent = LlmAgent(
    model="gemini-2.0-flash",
    system_instruction=TRAVEL_AGENT_PROMPT,
    tools=[search_hotels, search_flights, VertexAiRagRetrieval(...)],
)
runner = adk.Runner(agent, session_service=session_service)  # NEW
```

### Pattern 2: Function Tools for Real-Time Data

**What:** ADK Function Tools wrap external APIs for real-time data retrieval (booking availability, pricing)

**When to use:** When agent needs current/dynamic data that changes frequently (inventory, prices, availability)

**Trade-offs:**
- Pros: Always up-to-date, no storage/indexing costs, simple implementation
- Cons: API latency, rate limits, requires error handling, costs per call

**Example:**
```python
from google.adk.tools import FunctionTool

def search_hotels(
    destination: str,
    check_in: str,
    check_out: str,
    guests: int = 2,
) -> list[dict]:
    """
    Search available hotels for specified dates and destination.

    Args:
        destination: City or location name
        check_in: Check-in date (YYYY-MM-DD)
        check_out: Check-out date (YYYY-MM-DD)
        guests: Number of guests

    Returns:
        List of available hotels with pricing
    """
    # In workshop: mock data from JSON file
    # In production: call real booking API
    return booking_api.search_hotels(
        location=destination,
        dates=(check_in, check_out),
        occupancy=guests,
    )

# Register as ADK tool
hotel_search_tool = FunctionTool(search_hotels)
```

### Pattern 3: RAG for Static Knowledge

**What:** Use Vertex AI RAG Engine to retrieve static knowledge from pre-indexed document corpus (destination guides, travel tips, recommendations)

**When to use:** When agent needs factual knowledge that doesn't change frequently and benefits from semantic search

**Trade-offs:**
- Pros: Rich contextual information, semantic retrieval, no per-query API costs, grounding reduces hallucination
- Cons: Requires corpus preparation, indexing time, stale data unless re-indexed, embedding storage costs

**Example:**
```python
from google.adk.tools.google_cloud import VertexAiRagRetrieval

# Corpus prepared ahead of time with destination guides
rag_tool = VertexAiRagRetrieval(
    corpus_name=f"projects/{PROJECT_ID}/locations/{LOCATION}/ragCorpora/{CORPUS_ID}",
    similarity_top_k=3,  # Retrieve top 3 relevant passages
    vector_distance_threshold=0.5,
)

agent = LlmAgent(
    model="gemini-2.0-flash",
    tools=[
        hotel_search_tool,
        flight_search_tool,
        rag_tool,  # Agent can retrieve destination knowledge
    ],
)
```

**Corpus preparation (workshop setup script):**
```python
from google.cloud import aiplatform

# Create RAG corpus
corpus = aiplatform.RagCorpus.create(
    display_name="travel-destinations",
    description="Destination guides and travel information",
)

# Import documents from GCS
corpus.import_files(
    source=f"gs://{BUCKET_NAME}/destinations/*.md",
    chunk_size=512,
    chunk_overlap=100,
)
```

### Pattern 4: Session State for Conversation Context

**What:** Use ADK Session Service to persist conversation history and user preferences across turns

**When to use:** Multi-turn conversations where agent needs to remember previous context (user preferences, search history, booking criteria)

**Trade-offs:**
- Pros: Natural conversation flow, accumulates context, enables personalization
- Cons: State management complexity, costs for storage, privacy/data retention considerations

**Example:**
```python
from google.adk import Runner
from google.adk.services import VertexAiSessionService

# Initialize session service
session_service = VertexAiSessionService(
    project_id=PROJECT_ID,
    location=LOCATION,
)

# Create runner with session management
runner = Runner(
    agent=travel_agent,
    session_service=session_service,
)

# Run with session context
response = await runner.run(
    user_id="user123",
    session_id="session456",  # Resume previous conversation
    prompt="Show me those hotels again but near the beach",
)
```

**Accessing state in tools:**
```python
from google.adk.tools import ToolContext

def search_hotels(
    destination: str = None,
    context: ToolContext = None,
) -> list[dict]:
    """Search hotels using destination or previous search context."""

    # If no destination provided, use from previous conversation
    if not destination and context:
        destination = context.state.get("last_destination")

    # Store for future turns
    if context and destination:
        context.state["last_destination"] = destination

    return booking_api.search_hotels(location=destination)
```

### Pattern 5: Coordinator Pattern for Multi-Agent Orchestration

**What:** Root agent delegates specialized tasks to sub-agents (hotel specialist, flight specialist, destination expert)

**When to use:** Complex workflows benefiting from specialized expertise and parallel execution

**Trade-offs:**
- Pros: Modular, testable, can run sub-agents in parallel, clearer separation of concerns
- Cons: Added complexity (overkill for 90-min workshop), requires coordination logic, harder to debug

**Example (reference implementation, not workshop exercises):**
```python
from google.adk import LlmAgent, CoordinatorAgent

# Specialized sub-agents
hotel_agent = LlmAgent(
    model="gemini-2.0-flash",
    system_instruction="You are a hotel booking specialist...",
    tools=[search_hotels, get_hotel_details],
)

destination_agent = LlmAgent(
    model="gemini-2.0-flash",
    system_instruction="You are a destination expert...",
    tools=[VertexAiRagRetrieval(corpus_name="destinations")],
)

# Root coordinator
travel_coordinator = CoordinatorAgent(
    model="gemini-2.0-flash",
    sub_agents=[hotel_agent, destination_agent],
    system_instruction="Route user requests to appropriate specialist...",
)
```

**Note:** This pattern is mentioned in reference implementation but excluded from workshop exercises due to time constraints and beginner audience.

## Data Flow

### Request Flow (Single-Turn Interaction)

```
[User Message: "Find hotels in Paris"]
    ↓
[Agent receives prompt + conversation history from session]
    ↓
[Gemini LLM analyzes intent] → Decision: Need hotel search tool
    ↓
[Tool Call: search_hotels(destination="Paris")]
    ↓
[Mock/Real API] → Returns hotel data
    ↓
[Tool Response passed back to LLM]
    ↓
[LLM synthesizes natural language response]
    ↓
[Response + tool call events saved to session]
    ↓
[User sees: "Here are top hotels in Paris: ..."]
```

### Multi-Turn Conversation Flow with State

```
Turn 1:
[User: "I want to visit Paris"]
    ↓
[Agent + Destination RAG] → "Paris is beautiful! When are you planning to visit?"
    ↓
[Session State: {destination: "Paris"}]

Turn 2:
[User: "Next month"]
    ↓
[Agent reads session state] → destination="Paris"
    ↓
[Agent + Search Hotels tool] → search_hotels(destination="Paris", check_in="2026-02-01")
    ↓
[Session State: {destination: "Paris", dates: "2026-02-01 to 2026-02-05"}]
    ↓
[Response: "Here are available hotels in Paris for February..."]

Turn 3:
[User: "Show me things to do there"]
    ↓
[Agent reads session state] → destination="Paris"
    ↓
[Agent + Destination RAG] → Retrieves Paris activities from corpus
    ↓
[Response: "In Paris you can visit the Louvre, Eiffel Tower..."]
```

### RAG Retrieval Flow

```
[User query: "Tell me about things to do in Tokyo"]
    ↓
[Agent invokes VertexAiRagRetrieval tool]
    ↓
[Query embedding created] → Vector: [0.23, -0.45, 0.67, ...]
    ↓
[Semantic search in Vertex AI RAG corpus]
    ↓
[Top-K similar passages retrieved]
    │
    ├─ Passage 1: "Tokyo offers incredible cuisine..." (similarity: 0.89)
    ├─ Passage 2: "Popular attractions include Senso-ji..." (similarity: 0.85)
    └─ Passage 3: "Shibuya and Shinjuku districts..." (similarity: 0.78)
    ↓
[Passages returned as tool response]
    ↓
[LLM grounds response using retrieved context]
    ↓
[Natural language response with cited information]
```

### Workshop Exercise Progression Data Flow

```
Exercise 1: Basic Conversation
User ─────→ Agent ─────→ LLM ─────→ Response
            (prompt only)

Exercise 2: + Function Calling
User ─────→ Agent ─────→ LLM ─────→ Tool Call ─────→ Booking API
                           ↑                              │
                           └──────── Tool Response ───────┘
                                          ↓
                                      Response

Exercise 3: + RAG
User ─────→ Agent ─────→ LLM ─────→ Tool Selection
                           ↑              │
                           │              ├─→ Booking API (real-time data)
                           │              └─→ RAG Engine (static knowledge)
                           │                       ↓
                           └─────── Responses ─────┘
                                          ↓
                                      Response

Exercise 4: + Sessions
User ─────→ Agent ─────→ LLM ─────→ Tools (with state context)
   ↑                      ↑              │
   │                      │              │
Session ←─── State ───────┴──────────────┘
Service       Update
```

## Scaling Considerations

| Scale | Architecture Adjustments |
|-------|--------------------------|
| Workshop (10-50 participants) | In-memory session service for exercises, shared Vertex AI project with quota limits, mock booking APIs to avoid rate limits, small RAG corpus (10-20 documents) |
| Small Production (100-1K users) | VertexAiSessionService with TTL cleanup, real booking APIs with caching layer, expanded RAG corpus (100s of documents), simple error handling and retries |
| Medium Production (1K-10K users) | DatabaseSessionService with relational storage, API rate limiting and circuit breakers, partitioned RAG corpora by region, monitoring and observability (Cloud Trace/Logging) |
| Large Production (10K+ users) | Multi-region deployment for latency, session data in distributed cache (Memorystore), CDN for static content, auto-scaling Cloud Run deployment, separate RAG corpus per language/region, advanced caching strategies |

### Scaling Priorities

1. **First bottleneck: LLM API rate limits**
   - Gemini API has per-minute quotas that workshop will hit with 50 concurrent participants
   - Fix: Request quota increase before workshop, implement request queuing, use multiple projects

2. **Second bottleneck: RAG corpus creation time**
   - Creating and indexing corpus can take 10-15 minutes for 100 documents
   - Fix: Pre-create corpus before workshop, provide script in setup docs, use pre-indexed shared corpus

3. **Third bottleneck: Session storage**
   - In-memory sessions clear on restart, not suitable for production
   - Fix: Migrate to VertexAiSessionService or DatabaseSessionService with PostgreSQL/CloudSQL

## Anti-Patterns

### Anti-Pattern 1: Using RAG for Real-Time Data

**What people do:** Try to use RAG corpus for hotel availability, flight prices, or other frequently changing data

**Why it's wrong:** RAG requires re-indexing to update, causing stale data. Embedding/indexing costs waste budget on data that changes hourly.

**Do this instead:** Use Function Tools for real-time data (booking APIs), reserve RAG for static knowledge (destination guides, travel tips, FAQs)

**Example:**
```python
# WRONG: Using RAG for hotel availability
corpus.import_files("gs://bucket/hotel-availability.json")  # Stale within hours!

# RIGHT: Use Function Tool for real-time data
@FunctionTool
def get_hotel_availability(destination: str, date: str) -> list[dict]:
    """Check current hotel availability via API."""
    return booking_api.search(destination, date)

# RAG for static knowledge only
rag_tool = VertexAiRagRetrieval(
    corpus_name="destination-guides",  # Only static travel guides
)
```

### Anti-Pattern 2: Overusing Multi-Agent Patterns for Simple Tasks

**What people do:** Create separate sub-agents for every tool or simple task (hotel agent, flight agent, restaurant agent, etc.)

**Why it's wrong:** Added complexity (orchestration logic, debugging difficulty, latency) without benefit for simple tool delegation. Single agent with tools is simpler and faster.

**Do this instead:** Use single LlmAgent with multiple tools for straightforward workflows. Reserve multi-agent patterns for genuinely complex coordination requiring specialized prompts/models per domain.

**Example:**
```python
# WRONG: Over-engineered for simple booking
hotel_agent = LlmAgent(tools=[search_hotels])
flight_agent = LlmAgent(tools=[search_flights])
coordinator = CoordinatorAgent(sub_agents=[hotel_agent, flight_agent])

# RIGHT: Single agent with multiple tools
travel_agent = LlmAgent(
    tools=[search_hotels, search_flights, get_destination_info],
    system_instruction="You are a travel booking assistant...",
)
```

**When multi-agent IS appropriate:** Complex workflows like travel-concierge sample with distinct pre-booking, planning, booking, and in-trip phases each requiring different context and specialized prompts.

### Anti-Pattern 3: Ignoring Session State Management

**What people do:** Re-ask users for information already provided ("What's your destination again?"), lose context between turns

**Why it's wrong:** Poor user experience, feels robotic rather than conversational, wastes tokens re-providing context in prompts

**Do this instead:** Use Session Service to persist state and access previous context in tools and prompts

**Example:**
```python
# WRONG: Stateless tool requiring repeated input
def search_hotels(destination: str, check_in: str, check_out: str):
    """User must provide all params every time."""
    return api.search(destination, check_in, check_out)

# RIGHT: State-aware tool with defaults
def search_hotels(
    destination: str = None,
    check_in: str = None,
    context: ToolContext = None,
):
    """Falls back to session state if params not provided."""
    destination = destination or context.state.get("destination")
    check_in = check_in or context.state.get("check_in")

    # Update state for next turn
    if context:
        context.state.update({"destination": destination, "check_in": check_in})

    return api.search(destination, check_in)
```

### Anti-Pattern 4: Mixing Exercise Progression Concerns

**What people do:** Have Exercise 2 starter code already include Exercise 3 concepts (RAG setup in function-calling exercise)

**Why it's wrong:** Confuses participants about what's relevant to current exercise, violates single-concept-per-exercise pedagogy, makes it harder to isolate issues

**Do this instead:** Each exercise starter code contains ONLY concepts from current and previous exercises. Future concepts appear only as comments or TODO markers.

**Example:**
```python
# WRONG: Exercise 2 (function calling) includes RAG
agent = LlmAgent(
    tools=[
        search_hotels,  # Exercise 2 concept
        VertexAiRagRetrieval(...),  # Exercise 3 concept - confusing!
    ],
)

# RIGHT: Exercise 2 focuses only on function calling
agent = LlmAgent(
    tools=[search_hotels, search_flights],
)
# TODO Exercise 3: Add RAG tool for destination knowledge

# Exercise 3 starter then introduces RAG
agent = LlmAgent(
    tools=[
        search_hotels,
        search_flights,
        # TODO: Initialize VertexAiRagRetrieval tool here
    ],
)
```

### Anti-Pattern 5: Production Secrets in Workshop Code

**What people do:** Hardcode GCP project IDs, API keys, or corpus IDs directly in code examples

**Why it's wrong:** Security risk if workshop materials published, prevents reuse across different GCP projects/environments, teaches bad practices to beginners

**Do this instead:** Always use environment variables with .env.example template, provide clear setup instructions for participants to configure their own credentials

**Example:**
```python
# WRONG: Hardcoded credentials
PROJECT_ID = "my-workshop-project-12345"
CORPUS_ID = "1234567890"
API_KEY = "AIzaSyABC123..."

# RIGHT: Environment variables
import os
from dotenv import load_dotenv

load_dotenv()

PROJECT_ID = os.getenv("GCP_PROJECT_ID")
LOCATION = os.getenv("GCP_LOCATION", "us-central1")
CORPUS_ID = os.getenv("RAG_CORPUS_ID")

if not PROJECT_ID:
    raise ValueError("GCP_PROJECT_ID environment variable required")
```

**.env.example template:**
```bash
# Google Cloud Configuration
GCP_PROJECT_ID=your-project-id
GCP_LOCATION=us-central1
RAG_CORPUS_ID=your-corpus-id

# Optional: Model Configuration
GEMINI_MODEL=gemini-2.0-flash
```

## Integration Points

### External Services

| Service | Integration Pattern | Notes |
|---------|---------------------|-------|
| Vertex AI Gemini API | Direct via ADK LlmAgent with model parameter | Main LLM inference, use "gemini-2.0-flash" for workshop (fast + cheap) |
| Vertex AI RAG Engine | Via VertexAiRagRetrieval tool | Requires pre-created corpus, 10-15min setup time, corpus ID in env vars |
| Vertex AI Agent Engine Sessions | Via VertexAiSessionService | Managed session storage, automatic TTL cleanup, requires project/location config |
| Google Cloud Storage | Indirect via RAG corpus import | Stores destination documents before indexing, bucket must be in same region |
| Booking APIs (Mock) | Via custom Function Tools | Workshop uses JSON mock data, production would use real APIs (Amadeus, Booking.com) |
| Google Maps/Places API | Optional enhancement (not in core exercises) | Could add location enrichment, travel time calculations |

### Internal Boundaries

| Boundary | Communication | Notes |
|----------|---------------|-------|
| Agent ↔ Tools | Function call protocol via ADK runtime | ADK handles serialization, tool registration, result passing automatically |
| Agent ↔ RAG Engine | Tool interface (VertexAiRagRetrieval) | RAG tool behaves like any other tool from agent's perspective |
| Agent ↔ Session Service | Runner manages session lifecycle | Session state automatically loaded/saved on each turn, transparent to agent code |
| Tools ↔ Session State | ToolContext parameter injection | Optional context parameter gives tools read/write access to session state |
| Tutorial Docs ↔ Code | Markdown references code file paths | Docs should use relative paths, code blocks should be copy-pasteable |
| Exercises ↔ Solutions | Separate directory structure | No cross-references in code, solutions link back to exercises via docs |
| Starter Code ↔ Tests | Tests import from starter package | Tests validate completion without revealing solution |

## Build Order and Dependencies

### Suggested Build Order for Workshop Materials

**Phase 1: Foundation (Build First)**
1. Mock booking data JSON files (no dependencies)
2. Destination knowledge documents (no dependencies)
3. Basic agent scaffold (agent.py with minimal prompt)
4. Exercise 1 starter code (basic conversational agent)

**Phase 2: Tools Layer**
5. Booking tool implementations (depends on mock data)
6. Exercise 2 starter code (depends on #3, #5)
7. Exercise 2 solution (depends on #6)

**Phase 3: Knowledge Layer**
8. RAG corpus setup script (depends on destination docs #2)
9. Exercise 3 starter code (depends on #6, #8)
10. Exercise 3 solution (depends on #9)

**Phase 4: State Management**
11. Session service configuration (depends on Exercise 3)
12. Exercise 4 starter code (depends on #9, #11)
13. Exercise 4 solution (depends on #12)

**Phase 5: Documentation and Reference**
14. Tutorial documentation (can parallel exercises, but validate against working code)
15. Reference implementation (depends on all exercise solutions)
16. Deployment scripts and configuration (depends on reference impl)

**Phase 6: Workshop Logistics**
17. Setup scripts and validation (depends on all infrastructure)
18. GCP project templates and quotas (coordinate with Google)

### Dependency Graph

```
Mock Data (#1) ──────────┐
                         ├──→ Tools (#5) ──────────┐
                         │                         │
Destination Docs (#2) ───┼──→ RAG Setup (#8) ─────┼──→ Ex3 (#9) ──┐
                         │                         │               │
Basic Scaffold (#3) ─────┴──→ Ex1 (#4)             │               │
                                  ↓                │               │
                             Ex2 (#6) ─────────────┘               │
                                  ↓                                │
                             Ex2 Solution (#7)                     │
                                                                   │
Session Config (#11) ──────────────────────────────────────────────┤
                                                                   ↓
                                                              Ex4 (#12)
                                                                   ↓
                                                         All Solutions
                                                                   ↓
Tutorial Docs (#14) ←────────────────────────┐         Reference (#15)
                                             │               ↓
Setup Scripts (#17) ←────────────────────────┴─────── Deployment (#16)
```

### Critical Path

**Must be completed in order:**
1. Mock data and destination docs (blocking tools and RAG)
2. Basic agent scaffold (template for all exercises)
3. Exercise 1 (validates basic setup works)
4. Exercise 2 (tools depend on mock data, exercises are sequential)
5. RAG corpus setup (blocking Exercise 3)
6. Exercise 3 (RAG must work before sessions)
7. Exercise 4 (final exercise builds on all previous)

**Can parallelize:**
- Tutorial docs writing (alongside exercise development, validate after)
- Reference implementation (can develop in parallel with exercises, may inform exercise design)
- Setup scripts (can develop once infrastructure patterns clear)
- Solutions (can write immediately after starter code, before next exercise)

### Pre-Workshop Critical Dependencies

**Must be ready 1 week before workshop:**
- GCP project templates with quotas approved
- RAG corpus pre-created and indexed (avoid 15min setup during workshop)
- Mock data validated and complete
- All exercises tested end-to-end

**Must be ready 1 day before workshop:**
- Participant accounts provisioned
- Setup verification script run on sample account
- Instructor walkthrough completed
- All documentation published and accessible

## Sources

### High Confidence (Official Documentation)

- [Google ADK Official Documentation](https://google.github.io/adk-docs/) - Architecture, agents, tools, sessions
- [ADK Python GitHub Repository](https://github.com/google/adk-python) - Code structure and examples
- [ADK Sample Agents](https://github.com/google/adk-samples) - Travel concierge and 40+ reference implementations
- [Vertex AI Session Management](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/agent-engine/sessions/manage-sessions-adk) - Session service patterns
- [ADK Tools Documentation](https://google.github.io/adk-docs/tools/) - Function calling and RAG integration
- [Adding Sessions and Memory to ADK](https://dev.to/marianocodes/adding-sessions-and-memory-to-your-ai-agent-with-agent-development-kit-adk-31ap) - Session and memory architecture

### Medium Confidence (Verified Secondary Sources)

- [Google's Eight Essential Multi-Agent Design Patterns (InfoQ)](https://www.infoq.com/news/2026/01/multi-agent-design-patterns/) - Multi-agent patterns
- [Developer's Guide to Multi-Agent Patterns in ADK](https://developers.googleblog.com/developers-guide-to-multi-agent-patterns-in-adk/) - Pattern applications
- [Build AI Travel Assistant with ADK (Codecademy)](https://www.codecademy.com/article/build-an-ai-travel-assistant-with-google-agent-development-kit-adk) - Travel agent example
- [Practical Reactor Workshop Structure](https://github.com/schananas/practical-reactor) - Progressive exercise pattern reference

### Workshop Structure Research

- [Best Practices for Project Folder Structure (DEV Community)](https://dev.to/mattqafouri/projects-folder-structures-best-practices-g9d)
- [File and Folder Organization for Web Development (GeeksforGeeks)](https://www.geeksforgeeks.org/javascript/file-and-folder-organization-best-practices-for-web-development/)

---
*Architecture research for: Google ADK Workshop - Travel Booking Agent*
*Researched: 2026-01-23*
