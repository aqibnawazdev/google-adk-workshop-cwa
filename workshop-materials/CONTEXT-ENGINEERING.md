# Context Engineering Decision Framework

A practical guide for choosing between function calling, RAG retrieval, and session state when building AI agents with Google ADK.

## What is Context Engineering?

Context engineering is the art of providing your AI agent with the right information at the right time. Unlike prompt engineering (crafting effective instructions), context engineering focuses on **data architecture**: which information sources to connect, how to access them, and when each approach is appropriate.

For AI agents, context comes from three primary sources:

| Source | What It Provides | When It Changes |
|--------|------------------|-----------------|
| **Function Calling (Tools)** | Real-time external data | Every API call |
| **RAG (Knowledge Retrieval)** | Pre-indexed document knowledge | At indexing time |
| **Session State** | User preferences and conversation history | User actions |

**Why this matters:** Choosing the wrong approach leads to stale data, unnecessary API costs, or lost user preferences. The travel booking assistant you build in this workshop demonstrates all three approaches working together.

## The Core Question

When deciding how to provide information to your agent, ask:

> **"What kind of data is this, and when does it change?"**

This single question guides most context engineering decisions.

---

## Quick Decision Table

Use this table for rapid decision-making (under 30 seconds):

| Question | Tool (Function Calling) | RAG (Knowledge Retrieval) | Session State |
|----------|------------------------|---------------------------|---------------|
| Does data change in real-time? | YES | NO | NO |
| Is it external API data? | YES | NO | NO |
| Is it pre-indexed documents? | NO | YES | NO |
| Is it user-specific preference? | NO | NO | YES |
| Requires live calculation? | YES | NO | NO |
| Static knowledge base? | NO | YES | NO |
| Persists across sessions? | NO | NO | YES (with `user:`) |
| **Example: Flight prices** | **Tool** | - | - |
| **Example: Visa requirements** | - | **RAG** | - |
| **Example: User budget** | - | - | **Session** |
| **Example: Hotel availability** | **Tool** | - | - |
| **Example: Cultural customs** | - | **RAG** | - |
| **Example: Preferred airlines** | - | - | **Session** |

---

## Decision Flowchart

Trace through this flowchart for any data source:

```
                            User Query
                                |
                                v
          +---------------------------------------------+
          |     Does this need REAL-TIME data?         |
          |  (prices, availability, current status)     |
          +---------------------------------------------+
                    |                       |
                   YES                      NO
                    |                       |
                    v                       v
    +---------------------------+   +----------------------------------+
    |  Use FUNCTION CALLING     |   |    Is this STATIC KNOWLEDGE?     |
    |         TOOLS             |   | (guides, policies, cultural info)|
    |                           |   +----------------------------------+
    |  Examples:                |           |                    |
    |  - search_flights()       |          YES                   NO
    |  - search_hotels()        |           |                    |
    +---------------------------+           v                    v
                            +----------------------+  +-----------------------+
                            |   Use RAG RETRIEVAL  |  | Is this USER-SPECIFIC |
                            |                      |  |     preference?       |
                            |  Examples:           |  +-----------------------+
                            |  - destination guides|          |           |
                            |  - visa requirements |         YES          NO
                            |  - cultural tips     |          |           |
                            +----------------------+          v           v
                                            +--------------------+  +-------------+
                                            |  Use SESSION STATE |  | LLM general |
                                            |                    |  |  knowledge  |
                                            |  Examples:         |  +-------------+
                                            |  - user:budget     |
                                            |  - user:style      |
                                            +--------------------+
```

---

## Detailed Comparison

| Aspect | Function Calling (Tools) | RAG (Knowledge Retrieval) | Session State |
|--------|-------------------------|---------------------------|---------------|
| **Data freshness** | Real-time (every call) | At indexing time | User sets |
| **Latency** | API call time (100-500ms) | Vector search time (50-200ms) | Instant |
| **Cost** | Per API call | Per query (embeddings) | Free |
| **Setup complexity** | Define tool functions | Index corpus | State prefixes |
| **When to update** | Never (live API) | Re-index corpus | User action |
| **Size limits** | API response limits | Chunk token limits | State storage limits |
| **Best for** | Dynamic external data | Large document knowledge | Personalization |

### When Each Shines

**Function Calling Tools** excel when:
- Data changes frequently (prices, inventory, status)
- You need live API integration
- Results depend on user input (search queries)
- External system interaction is required

**RAG Retrieval** excels when:
- You have large document collections
- Information is relatively stable (guides, policies)
- Semantic search across corpus is needed
- Answers synthesize from multiple sources

**Session State** excels when:
- Personalizing agent behavior
- Remembering user preferences
- Maintaining conversation context
- Avoiding repeated questions

---

## Workshop Examples

Each workshop exercise demonstrates the appropriate approach:

### Exercise 2: Function Calling Tools
**Query:** "Find flights from SFO to Tokyo on March 15"
**Why Tool:** Flight availability and prices change every minute. A RAG corpus would have stale prices immediately.

```python
# tools.py - Real-time data requires function calling
def search_flights(origin: str, destination: str, departure_date: str, ...) -> dict:
    # Returns current flight availability and pricing
```

### Exercise 3: RAG Knowledge Retrieval
**Query:** "What are the visa requirements for Japan?"
**Why RAG:** Visa policies change infrequently (maybe quarterly). Pre-indexed guides provide accurate, consistent answers.

```python
# rag_tools.py - Static knowledge uses RAG
destination_knowledge = create_destination_knowledge_tool(
    corpus_id=RAG_CORPUS_ID,
    # Searches pre-indexed destination guides
)
```

### Exercise 4: Session State
**Query:** "Remember my budget is $2000 and I prefer luxury hotels"
**Why Session:** User preferences persist across the conversation and should be applied to all future searches automatically.

```python
# state_utils.py - User preferences use session state
tool_context.state["user:budget"] = 2000
tool_context.state["user:travel_style"] = "luxury"
# These persist and auto-apply to searches
```

---

## Common Mistakes

Avoid these architectural errors that lead to broken or inefficient agents:

### Mistake 1: Using RAG for Real-Time Data

**What it looks like:**
```python
# WRONG: Indexing flight prices in RAG corpus
"The flight to Tokyo costs $850..."  # In destination guide
```

**Why it fails:**
- Price is stale the moment you index it
- Users get incorrect quotes
- Booking attempts fail due to price mismatch

**Correction:** Use `search_flights()` tool for any pricing or availability data.

---

### Mistake 2: Using Tools for Static Knowledge

**What it looks like:**
```python
# WRONG: Creating a "get_visa_requirements" API tool
def get_visa_requirements(country: str) -> dict:
    # Calls external API every time
```

**Why it's wasteful:**
- Visa rules change infrequently (quarterly at most)
- Unnecessary API calls and latency
- External API may have rate limits

**Correction:** Index visa requirements in RAG corpus. Re-index quarterly or when policies change.

---

### Mistake 3: Storing Real-Time Data in Session State

**What it looks like:**
```python
# WRONG: Caching flight prices in session
tool_context.state["user:last_flight_price"] = 850
# Later: "The Tokyo flight is $850" (but it's now $920)
```

**Why it fails:**
- Prices change, user gets stale data
- Creates inconsistency between quoted and actual price

**Correction:** Always call `search_flights()` for current prices. Only store user preferences (budget, style) in session.

---

### Mistake 4: Forgetting User Preferences

**What it looks like:**
```python
# WRONG: Agent asks for budget every conversation
"What's your budget for this trip?"
# User: "I told you last time - $2000"
```

**Why it frustrates users:**
- Repetitive questioning wastes time
- Feels like the agent doesn't "remember" them
- Reduces personalization value

**Correction:** Store preferences with `user:` prefix for persistence across sessions:
```python
tool_context.state["user:budget"] = 2000  # Persists!
```

---

### Mistake 5: Mixing RAG with Function Tools in Same Agent

**What it looks like:**
```python
# WRONG: ADK constraint violation
agent = Agent(
    tools=[search_flights, search_hotels, destination_knowledge]
    # ^-- Function tools          ^-- RAG tool
    # This combination is NOT allowed!
)
```

**Why it fails:**
- ADK constraint: VertexAiRagRetrieval cannot mix with function calling tools
- Agent creation will fail or behave unpredictably

**Correction:** Use the hybrid coordinator pattern:
```python
# Separate specialized agents
booking_agent = Agent(tools=[search_flights, search_hotels])
knowledge_agent = Agent(tools=[destination_knowledge])
# Coordinator routes queries to appropriate agent
```

See `hybrid_agent.py` in reference implementation for complete pattern.

---

## Post-Workshop: Applying to Your Projects

Use this process when designing your own agents:

### Step 1: List All Data Sources

What information does your agent need? Examples:
- Product catalog
- Pricing database
- User account info
- Company policies
- External APIs
- User preferences

### Step 2: Classify Each Source

For each data source, answer:

| Data Source | Changes while user talks? | Per-user or shared? | Decision |
|-------------|---------------------------|---------------------|----------|
| Product prices | YES | Shared | **Tool** |
| Product descriptions | NO | Shared | **RAG** |
| User's past orders | NO | Per-user | **Tool** (API) |
| User's style preference | NO | Per-user | **Session** |
| Return policy | NO | Shared | **RAG** |
| Inventory count | YES | Shared | **Tool** |

### Step 3: Apply the Decision Framework

- **Real-time + Shared** -> Function calling tool
- **Static + Shared** -> RAG corpus
- **Per-user + Persistent** -> Session state with `user:` prefix
- **Per-user + Real-time** -> Function calling tool with user context

### Step 4: Design Your Architecture

Sketch the flow:

```
User Query
    |
    v
[Intent Detection]
    |
    +---> Real-time query ---> [Function Calling Agent]
    |
    +---> Knowledge query ---> [RAG Agent]
    |
    +---> Preference update --> [Session State]
```

### Example: E-commerce Customer Service Agent

| Component | Approach | Rationale |
|-----------|----------|-----------|
| Order status | Tool | Real-time from order DB |
| Product specs | RAG | Static catalog content |
| Shipping policy | RAG | Rarely changes |
| Customer's address | Session | Per-user, persists |
| Current promotions | Tool | Changes frequently |
| Size recommendations | Session + Tool | Preference + inventory check |

---

## Hybrid Patterns

When your agent needs multiple approaches (like our travel assistant):

### The ADK Constraint

**Important:** Vertex AI RAG retrieval tool (`VertexAiRagRetrieval`) cannot be mixed with function calling tools in the same agent.

This means you cannot do:
```python
# This DOES NOT work
agent = Agent(
    tools=[search_flights, destination_knowledge]  # Mix not allowed
)
```

### Solution: Hybrid Coordinator Pattern

Create specialized agents and coordinate between them:

```
                    User Query
                         |
                         v
              +-------------------+
              |    Coordinator    |
              | (Intent Detection)|
              +-------------------+
                    |       |
         +----------+       +----------+
         |                             |
         v                             v
+------------------+         +------------------+
|  Booking Agent   |         | Knowledge Agent  |
| (Function Tools) |         |   (RAG Tool)     |
+------------------+         +------------------+
| - search_flights |         | - destination_   |
| - search_hotels  |         |   knowledge      |
+------------------+         +------------------+
         |                             |
         v                             v
  Real-time results          Knowledge results
         |                             |
         +-------------+---------------+
                       |
                       v
              Combined Response
```

### When to Consider Hybrid Pattern

Use hybrid coordination when your agent needs:
- Real-time booking/search capabilities
- Knowledge base access for context
- Comprehensive answers combining both

See `reference-implementation/hybrid_agent.py` for the complete implementation.

---

## Quick Reference Card

Print this for reference during development:

```
+------------------------------------------------------------------+
|                CONTEXT ENGINEERING QUICK REFERENCE                |
+------------------------------------------------------------------+
|                                                                  |
|  TOOL (Function Calling)                                         |
|    Use when: Data changes in real-time                           |
|    Examples: search_flights(), search_hotels()                   |
|    Pattern: def my_tool(...) -> dict: return {...}               |
|                                                                  |
+------------------------------------------------------------------+
|                                                                  |
|  RAG (Knowledge Retrieval)                                       |
|    Use when: Static/slow-changing knowledge base                 |
|    Examples: destination_knowledge, policy_docs                  |
|    Pattern: VertexAiRagRetrieval(corpus=...)                     |
|    Constraint: Cannot mix with function tools!                   |
|                                                                  |
+------------------------------------------------------------------+
|                                                                  |
|  SESSION STATE                                                   |
|    Use when: User preferences, personalization                   |
|    Examples: user:budget, user:travel_style                      |
|    Pattern: tool_context.state["user:key"] = value               |
|    Prefixes: user: (persistent), temp: (invocation only)         |
|                                                                  |
+------------------------------------------------------------------+
|                                                                  |
|  THE CORE QUESTION                                               |
|    "What kind of data is this, and when does it change?"         |
|                                                                  |
+------------------------------------------------------------------+
```

---

## Further Reading

- **Reference Implementation:** See `reference-implementation/` for complete code examples
- **ADK Documentation:** https://google.github.io/adk-docs/
- **Vertex AI RAG:** https://cloud.google.com/vertex-ai/docs/rag-overview

---

*This document is part of the Google ADK Workshop materials. The decision framework presented here transfers to any AI agent project, regardless of framework.*
