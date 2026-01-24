# Phase 2: Function Calling & Tools - Research

**Researched:** 2026-01-24
**Domain:** Google ADK Function Calling, Mock Travel APIs, Error Handling, Workshop Education
**Confidence:** HIGH

## Summary

Phase 2 teaches function calling in Google ADK by implementing realistic flight and hotel search tools for the travel agent. The research confirms that ADK 1.23.0 provides robust, automatic function calling with schema generation from Python function signatures, making it ideal for teaching beginners without overwhelming them with JSON schema complexity.

The critical insight for workshop success is the decision framework: **use function calling for real-time data** (flights, hotels, availability) and **RAG for static knowledge** (destination guides, visa info). This distinction must be crystal clear to participants. The mock API approach is superior to real travel APIs for workshops - it eliminates rate limits, costs, API key management, and variable response times while keeping focus on ADK patterns rather than third-party API quirks.

Error handling is where most beginner function calling implementations fail. The key pattern is **errors-in-context**: return descriptive error dictionaries to the LLM rather than raising exceptions, allowing the agent to learn from failures and suggest alternatives. This pattern must be demonstrated explicitly, not just mentioned.

**Primary recommendation:** Implement mock flight/hotel functions returning realistic JSON structures, use ADK's automatic schema generation from type-hinted Python functions, demonstrate error-in-context pattern with specific examples (invalid dates, no availability), and provide a clear decision matrix for tools vs RAG with travel-specific examples.

## Standard Stack

The established stack for ADK function calling:

### Core
| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| google-adk | 1.23.0 | Agent framework with tools | Automatic schema generation, built-in function dispatch |
| Python type hints | 3.11+ | Parameter schema definition | ADK inspects signatures to generate tool schemas |
| Docstrings (Google style) | Standard | Tool descriptions for LLM | LLM reads these to decide when/how to use tools |

### Supporting
| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| typing.Optional | stdlib | Optional parameters | Make parameters optional without complex Union types |
| datetime | stdlib | Date validation/parsing | Validate date formats in mock APIs |
| dataclasses | stdlib | Structured return types | Complex response objects (not strictly required) |

### Alternatives Considered
| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| Mock APIs in functions | Real Amadeus/Skyscanner APIs | Real APIs add cost, rate limits, API key complexity; mocks keep focus on ADK patterns |
| Type-hinted functions | Explicit FunctionTool schemas | Manual schemas give more control but much more verbose, harder for beginners |
| Errors-in-context | Raising exceptions | Exceptions hide errors from LLM, preventing learning; error dicts teach agent |

**Implementation Pattern:**
```python
# ADK automatically generates schema from this
def search_flights(origin: str, destination: str, departure_date: str,
                   passengers: int = 1) -> dict:
    """
    Search for available flights.

    Args:
        origin: Departure airport code (e.g., 'SFO')
        destination: Arrival airport code (e.g., 'NRT')
        departure_date: Date in YYYY-MM-DD format
        passengers: Number of passengers (default 1)

    Returns:
        Dict with available flights and prices
    """
    # Mock implementation
    return {"flights": [...], "currency": "USD"}
```

## Architecture Patterns

### Recommended Exercise Structure
```
02-function-calling-and-tools.ipynb
├── Concept: What is function calling? (5 min)
│   └── Tools vs RAG decision framework
├── Exercise 2A: Implement search_flights (7 min)
│   ├── TODO: Fill in function signature
│   ├── TODO: Add docstring
│   └── TODO: Return mock flight data
├── Exercise 2B: Implement search_hotels (7 min)
│   └── Similar structure to 2A
├── Exercise 2C: Add tools to agent (3 min)
│   └── tools=[search_flights, search_hotels]
├── Exercise 2D: Test function calling (5 min)
│   └── Multi-turn conversation invoking tools
└── Exercise 2E: Error handling (8 min)
    ├── Invalid dates
    ├── No availability
    └── Budget filtering
```

### Pattern 1: Type-Hinted Function Tool
**What:** Python function with type hints and docstring automatically converted to tool
**When to use:** All function tools in ADK (standard approach)
**Example:**
```python
# Source: https://google.github.io/adk-docs/tools-custom/function-tools/
def search_flights(origin: str, destination: str, departure_date: str,
                   passengers: int = 1) -> dict:
    """
    Search for available flights.

    Args:
        origin: Departure airport code (e.g., 'SFO')
        destination: Arrival airport code (e.g., 'NRT')
        departure_date: Date in YYYY-MM-DD format
        passengers: Number of passengers (default 1)

    Returns:
        Dict with available flights and prices or error information
    """
    # Validate date format
    try:
        datetime.strptime(departure_date, '%Y-%m-%d')
    except ValueError:
        return {
            "status": "error",
            "error_message": f"Invalid date format: {departure_date}. Use YYYY-MM-DD.",
            "requested_date": departure_date
        }

    # Return mock data
    return {
        "status": "success",
        "flights": [
            {"airline": "United", "price": 850, "departure": "08:30", "arrival": "14:30+1"},
            {"airline": "ANA", "price": 920, "departure": "11:00", "arrival": "17:00+1"},
            {"airline": "JAL", "price": 890, "departure": "13:45", "arrival": "19:45+1"},
        ],
        "currency": "USD",
        "route": f"{origin} → {destination}",
        "date": departure_date,
    }
```

### Pattern 2: Error-in-Context (Critical for Learning)
**What:** Return error information to LLM rather than raising exceptions
**When to use:** All error conditions in function tools
**Why critical:** LLM cannot learn from exceptions it never sees; error dicts enable agent to retry, clarify, or suggest alternatives
**Example:**
```python
# Source: https://google.github.io/adk-docs/tools-custom/function-tools/
# GOOD: Error in context
def search_hotels(location: str, check_in: str, check_out: str,
                  guests: int = 1) -> dict:
    """Search for available hotels."""

    # Validate dates
    try:
        checkin_dt = datetime.strptime(check_in, '%Y-%m-%d')
        checkout_dt = datetime.strptime(check_out, '%Y-%m-%d')
    except ValueError:
        return {
            "status": "error",
            "error_message": "Invalid date format. Use YYYY-MM-DD.",
            "check_in": check_in,
            "check_out": check_out
        }

    # Validate date order
    if checkout_dt <= checkin_dt:
        return {
            "status": "error",
            "error_message": "Check-out date must be after check-in date.",
            "check_in": check_in,
            "check_out": check_out
        }

    # Mock: No availability
    if location.lower() == "atlantis":
        return {
            "status": "error",
            "error_message": f"Location '{location}' not found in database. Did you mean 'Atlanta'?",
            "location": location,
            "suggestion": "Atlanta"
        }

    # Success case
    return {
        "status": "success",
        "hotels": [...],
        "location": location,
        "dates": f"{check_in} to {check_out}",
    }

# BAD: Raising exceptions (anti-pattern)
def bad_search_hotels(location: str, check_in: str, check_out: str) -> dict:
    if location == "Atlantis":
        raise ValueError("Location not found")  # ❌ LLM never sees this!
```

### Pattern 3: Realistic Mock Data Structure
**What:** Mock data that matches real travel API patterns but with deterministic results
**When to use:** Workshop exercises to avoid API costs/complexity
**Example:**
```python
# Source: Inspired by https://datamock.dev/api-explorer/flight
MOCK_FLIGHT_DATABASE = {
    ("SFO", "NRT"): [
        {
            "airline": "United Airlines",
            "flight_number": "UA837",
            "price": 850,
            "departure": "08:30",
            "arrival": "14:30+1",
            "duration": "11h 00m",
            "aircraft": "Boeing 787-9",
            "class": "Economy"
        },
        {
            "airline": "ANA",
            "flight_number": "NH7",
            "price": 920,
            "departure": "11:00",
            "arrival": "17:00+1",
            "duration": "11h 00m",
            "aircraft": "Boeing 777-300ER",
            "class": "Economy"
        },
    ],
    ("LAX", "CDG"): [
        {
            "airline": "Air France",
            "flight_number": "AF65",
            "price": 780,
            "departure": "15:30",
            "arrival": "11:00+1",
            "duration": "10h 30m",
            "aircraft": "Airbus A350-900",
            "class": "Economy"
        },
    ],
}

def search_flights(origin: str, destination: str, departure_date: str,
                   passengers: int = 1) -> dict:
    """Search for available flights."""

    # Lookup in mock database
    route_key = (origin.upper(), destination.upper())
    flights = MOCK_FLIGHT_DATABASE.get(route_key)

    if not flights:
        return {
            "status": "error",
            "error_message": f"No flights found for route {origin} → {destination}. Available routes: SFO→NRT, LAX→CDG.",
            "origin": origin,
            "destination": destination
        }

    return {
        "status": "success",
        "flights": flights,
        "currency": "USD",
        "route": f"{origin} → {destination}",
        "date": departure_date,
        "passengers": passengers
    }
```

### Pattern 4: Agent with Tools Configuration
**What:** Adding function tools to agent via tools parameter
**When to use:** After implementing individual tool functions
**Example:**
```python
# Source: https://google.github.io/adk-docs/agents/llm-agents/
from google.adk.agents import Agent

agent = Agent(
    model='gemini-2.5-flash',
    name='travel_booking_assistant',
    description='A helpful travel booking assistant.',

    instruction='''You are an expert travel booking assistant.

YOUR TOOLS:
- search_flights(): Find available flights between airports
- search_hotels(): Find accommodation options

HOW TO USE TOOLS:
1. When users ask about trips, gather key details first
2. Use tools to find real options
3. Present 2-3 best matches with prices and details
4. If a tool returns an error, help the user fix the request

BUDGET FILTERING:
- If user mentions budget, filter results to show only options within range
- Explain why you're recommending each option

Be friendly, concise, and proactive.''',

    # Add function tools here
    tools=[
        search_flights,
        search_hotels,
    ],
)

# Test with tool-requiring query
response = agent.generate_content(
    "I need to fly from San Francisco to Tokyo in March. "
    "My budget is $900. Can you help?"
)
print(response.text)
```

### Pattern 5: Tools vs RAG Decision Framework
**What:** Clear criteria for when to use function calling vs RAG
**When to use:** Teaching participants architectural decisions
**Decision Matrix:**
```python
"""
TOOLS (Function Calling) vs RAG Decision Framework

Use FUNCTION CALLING when:
✓ Data changes frequently (real-time)
✓ Requires external API calls
✓ Involves calculations or transformations
✓ Data is structured (database queries)

Examples in Travel Agent:
- search_flights() → availability changes minute-to-minute
- search_hotels() → pricing and inventory updates constantly
- calculate_trip_cost() → computation based on user selections

Use RAG (Retrieval-Augmented Generation) when:
✓ Data is static or slow-changing
✓ Information already in documents
✓ Need semantic search across large corpus
✓ Educational/reference content

Examples in Travel Agent:
- Destination guides (best time to visit Tokyo)
- Visa requirements (US citizens need visa for Brazil)
- Cultural tips (business etiquette in Japan)
- Packing lists for different climates

HYBRID APPROACH (both):
- Use search_flights() to get availability
- Use RAG to retrieve destination guide for that city
- Combine in agent response: "Here are flights to Tokyo,
  and by the way, March is cherry blossom season!"
"""
```

### Anti-Patterns to Avoid
- **Exceptions instead of error dicts**: Don't raise exceptions in tools - LLM needs to see errors in context
- **Complex parameter schemas**: Don't use nested Pydantic models in beginner exercises - stick to primitives (str, int, float)
- **Missing docstrings**: Don't skip docstrings - they're critical for LLM tool selection
- **Vague error messages**: Don't return "Error" - return specific, actionable messages like "Invalid date format: use YYYY-MM-DD"
- **Real APIs in workshop**: Don't use Amadeus/Skyscanner in exercises - rate limits and costs distract from learning
- **Ignoring budget constraints**: Don't forget to demonstrate filtering results by user's stated budget (AGENT-08 requirement)

## Don't Hand-Roll

Problems that look simple but have existing solutions:

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| JSON schema from functions | Manual OpenAPI schema definitions | ADK automatic schema generation | ADK inspects type hints and docstrings automatically, less error-prone |
| Function parameter validation | Custom validation logic | Type hints + optional defaults | Python's type system + ADK handles this, raise issues early |
| Mock API responses | Random/hardcoded per call | Deterministic lookup tables | Reproducible for debugging, realistic data structure |
| Error handling in tools | try/except with generic messages | Descriptive error dicts with suggestions | LLM learns from specific errors, can retry intelligently |
| Tool selection logic | Manual if/elif chains | ADK automatic dispatch | LLM decides which tool based on descriptions, handles multi-tool scenarios |
| Date parsing | Custom regex/split | datetime.strptime() | Handles edge cases, validates properly, standard library |

**Key insight:** ADK's automatic schema generation from Python functions is its superpower. Don't fight it by writing manual schemas. Instead, invest time in clear docstrings and proper type hints - this is where beginners should focus energy.

## Common Pitfalls

### Pitfall 1: Raising Exceptions in Tools Instead of Returning Errors
**What goes wrong:** Function tools raise exceptions when inputs are invalid, LLM never sees the error, agent can't recover
**Why it happens:**
- Standard Python error handling uses exceptions
- Beginners don't realize LLM needs errors in response content
- Examples from other frameworks use try/except
**How to avoid:**
- Demonstrate error-in-context pattern explicitly in first tool
- Show side-by-side: exception (bad) vs error dict (good)
- Include validation in every exercise solution (dates, locations, etc.)
- In instruction, tell agent: "If tool returns error status, help user fix the request"
**Warning signs:**
- Agent says "I encountered an error" without details
- Agent doesn't retry or ask for clarification
- Exceptions appear in Colab output but agent ignores them
**Code example:**
```python
# ❌ BAD: Exception hidden from LLM
def bad_tool(date: str) -> dict:
    datetime.strptime(date, '%Y-%m-%d')  # Raises ValueError
    return {"result": "..."}

# ✅ GOOD: Error in context
def good_tool(date: str) -> dict:
    try:
        datetime.strptime(date, '%Y-%m-%d')
    except ValueError:
        return {
            "status": "error",
            "error_message": f"Invalid date '{date}'. Use YYYY-MM-DD format (e.g., 2026-03-15).",
            "example": "2026-03-15"
        }
    return {"status": "success", "result": "..."}
```

### Pitfall 2: Poor Docstrings Leading to Wrong Tool Selection
**What goes wrong:** LLM calls wrong tool or fails to call tools when appropriate
**Why it happens:**
- Vague docstrings: "Search for flights" without parameter details
- Missing parameter descriptions (no Args: section)
- No examples in descriptions
- Copy-paste docstrings between similar functions
**How to avoid:**
- Require Google-style docstrings in all exercises (Args, Returns sections)
- Include examples in parameter descriptions: "origin: Departure airport code (e.g., 'SFO')"
- Make function names very specific: search_flights not search
- Test with ambiguous queries: "Find me a trip to Paris" should trigger right tool
**Warning signs:**
- Agent says "I can't help with that" despite having relevant tool
- Agent calls hotel search when user asks about flights
- Agent doesn't use tools even when user asks for search
**Code example:**
```python
# ❌ BAD: Vague docstring
def search_flights(origin, destination, date):
    """Search for flights."""
    pass

# ✅ GOOD: Detailed docstring with examples
def search_flights(origin: str, destination: str, departure_date: str,
                   passengers: int = 1) -> dict:
    """
    Search for available flights between two airports.

    Args:
        origin: Departure airport code (e.g., 'SFO', 'LAX', 'JFK')
        destination: Arrival airport code (e.g., 'NRT', 'CDG', 'LHR')
        departure_date: Departure date in YYYY-MM-DD format (e.g., '2026-03-15')
        passengers: Number of passengers (default 1, maximum 9)

    Returns:
        Dictionary with 'status' ('success' or 'error'), 'flights' list with airline,
        price, times, or 'error_message' if search fails.
    """
    pass
```

### Pitfall 3: Mock Data Too Simple or Unrealistic
**What goes wrong:** Mock data doesn't match real API structures, participants surprised when integrating real APIs later
**Why it happens:**
- Return single flight instead of list
- Omit important fields (currency, dates, status)
- Use unrealistic values (flight price: $10)
- No variation in results (always same 3 flights)
**How to avoid:**
- Study real travel API responses (Amadeus, Skyscanner docs)
- Return data structures matching industry patterns (see Pattern 3)
- Include 3-5 options per search with varied prices
- Add realistic details: flight numbers, aircraft types, durations
**Warning signs:**
- Participants confused by real API structure in Phase 5
- Agent responses feel artificial: "Here is THE flight" (singular)
- Missing obvious fields: no currency, no booking availability
**Good mock structure:**
```python
{
    "status": "success",
    "flights": [  # ✓ List of options, not single result
        {
            "airline": "United Airlines",  # ✓ Full name, not just "United"
            "flight_number": "UA837",  # ✓ Realistic flight number
            "price": 850,  # ✓ Realistic price ($800-1000 for SFO→NRT)
            "currency": "USD",  # ✓ Explicit currency
            "departure": "08:30",
            "arrival": "14:30+1",  # ✓ +1 indicates next day arrival
            "duration": "11h 00m",
            "aircraft": "Boeing 787-9",  # ✓ Real aircraft type
            "class": "Economy",
            "available_seats": 42,  # ✓ Availability info
        },
        # ... more options
    ],
    "route": "SFO → NRT",
    "date": "2026-03-15",
    "passengers": 2,
}
```

### Pitfall 4: Not Demonstrating Budget Filtering (AGENT-08)
**What goes wrong:** Agent finds flights but ignores user's budget constraint mentioned earlier
**Why it happens:**
- Tool returns all results without filtering
- Agent instruction doesn't emphasize budget tracking
- No example showing budget-based filtering
**How to avoid:**
- Add budget parameter to tool signature: `max_price: Optional[int] = None`
- In agent instruction, explicitly: "Filter results by user's stated budget"
- Show example: "My budget is $800" → only show flights ≤$800
- Demonstrate filtering in tool logic or in agent's response formatting
**Warning signs:**
- Agent shows $1500 flights when user said "$800 budget"
- Agent finds hotels then ignores "under $200/night" constraint
- No explanation why expensive options are excluded
**Code example:**
```python
def search_flights(origin: str, destination: str, departure_date: str,
                   passengers: int = 1, max_price: Optional[int] = None) -> dict:
    """
    Search for available flights.

    Args:
        origin: Departure airport code
        destination: Arrival airport code
        departure_date: Date in YYYY-MM-DD format
        passengers: Number of passengers (default 1)
        max_price: Maximum price per person in USD (optional)

    Returns:
        Dict with filtered flight results
    """
    flights = get_all_flights(origin, destination, departure_date)

    # Filter by budget if specified
    if max_price is not None:
        flights = [f for f in flights if f["price"] <= max_price]
        if not flights:
            return {
                "status": "error",
                "error_message": f"No flights found under ${max_price}. Lowest available: ${min(f['price'] for f in get_all_flights(...))}",
                "max_price": max_price
            }

    return {"status": "success", "flights": flights, "currency": "USD"}
```

### Pitfall 5: Confusing Tools vs RAG for Beginners
**What goes wrong:** Participants don't understand when to use function calling vs RAG, try to put real-time data in RAG
**Why it happens:**
- No explicit decision framework presented
- Phase 2 (tools) and Phase 3 (RAG) taught separately without contrast
- Examples don't clearly distinguish use cases
**How to avoid:**
- In Phase 2 introduction, preview the distinction (show decision matrix)
- Use clear examples: "Flights = tools (real-time), Destination guides = RAG (static)"
- In agent instruction template, show both: "Use search_flights() for availability, search knowledge base for travel tips"
- Reserve 3 minutes in Phase 2 for "What's coming in Phase 3" contrast
**Warning signs:**
- Participant asks: "Why not just put flight data in a document?"
- Confusion about when to create tools vs add documents to RAG
- Attempt to use tools for static info: `get_visa_requirements()` instead of RAG
**Teaching moment:**
```markdown
## Tools vs RAG: When to Use Each

**This Phase (Tools/Function Calling):**
✓ Real-time flight availability ← Changes every minute
✓ Hotel pricing and inventory ← Updates constantly
✓ Trip cost calculations ← Depends on user selections

**Next Phase (RAG/Knowledge Base):**
✓ Destination guides ← Static content
✓ Visa requirements ← Changes rarely
✓ Cultural tips ← Educational content

**The Key Question:** "Does this data change while the user is talking to the agent?"
- YES → Tool (function calling)
- NO → RAG (knowledge retrieval)
```

### Pitfall 6: Tool Invocation Not Visible to Learners
**What goes wrong:** Beginners don't see that LLM is calling their functions, think "it just works" without understanding
**Why it happens:**
- ADK abstracts tool calling completely
- No visibility into LLM's decision process
- Participants see only final response, not intermediate steps
**How to avoid:**
- Add debug output in tools: `print(f"🔧 search_flights called: {origin} → {destination}")`
- Show agent logs if available: tool selection, arguments, results
- Walk through manually: "Let's trace what happens when agent gets this request"
- Exercise: predict which tool will be called before running
**Warning signs:**
- Participant says: "How does it know to use search_flights?"
- Surprise when tool function executes
- Doesn't understand why tool wasn't called for certain queries
**Teaching enhancement:**
```python
def search_flights(origin: str, destination: str, departure_date: str,
                   passengers: int = 1) -> dict:
    """Search for available flights."""

    # ✓ Add visibility for learning
    print(f"🔧 Tool called: search_flights")
    print(f"   Parameters: {origin} → {destination}, {departure_date}, {passengers} pax")

    # ... implementation

    result = {"status": "success", "flights": [...]}
    print(f"   Result: Found {len(result['flights'])} flights")
    return result
```

## Code Examples

Verified patterns from official sources and workshop best practices:

### Complete Flight Search Tool
```python
# Source: https://google.github.io/adk-docs/tools-custom/function-tools/
from datetime import datetime
from typing import Optional

def search_flights(origin: str, destination: str, departure_date: str,
                   passengers: int = 1, max_price: Optional[int] = None) -> dict:
    """
    Search for available flights between airports.

    Args:
        origin: Departure airport code (e.g., 'SFO', 'LAX', 'JFK')
        destination: Arrival airport code (e.g., 'NRT', 'CDG', 'LHR')
        departure_date: Departure date in YYYY-MM-DD format (e.g., '2026-03-15')
        passengers: Number of passengers, 1-9 (default 1)
        max_price: Maximum price per person in USD (optional)

    Returns:
        Dictionary with:
        - status: 'success' or 'error'
        - flights: List of available flights with pricing and schedule
        - error_message: Error details if status is 'error'
    """
    # Validate date format
    try:
        departure_dt = datetime.strptime(departure_date, '%Y-%m-%d')
    except ValueError:
        return {
            "status": "error",
            "error_message": f"Invalid date format: '{departure_date}'. Please use YYYY-MM-DD (e.g., '2026-03-15').",
            "requested_date": departure_date,
            "example": "2026-03-15"
        }

    # Validate date is in future
    if departure_dt.date() < datetime.now().date():
        return {
            "status": "error",
            "error_message": f"Departure date {departure_date} is in the past. Please provide a future date.",
            "requested_date": departure_date
        }

    # Validate passenger count
    if not 1 <= passengers <= 9:
        return {
            "status": "error",
            "error_message": f"Passengers must be between 1 and 9. You requested {passengers}.",
            "requested_passengers": passengers
        }

    # Mock flight database (route-based lookup)
    MOCK_FLIGHTS = {
        ("SFO", "NRT"): [
            {"airline": "United Airlines", "flight_number": "UA837", "price": 850,
             "departure": "08:30", "arrival": "14:30+1", "duration": "11h 00m",
             "aircraft": "Boeing 787-9"},
            {"airline": "ANA", "flight_number": "NH7", "price": 920,
             "departure": "11:00", "arrival": "17:00+1", "duration": "11h 00m",
             "aircraft": "Boeing 777-300ER"},
            {"airline": "JAL", "flight_number": "JL2", "price": 890,
             "departure": "13:45", "arrival": "19:45+1", "duration": "11h 00m",
             "aircraft": "Boeing 787-8"},
        ],
        ("LAX", "CDG"): [
            {"airline": "Air France", "flight_number": "AF65", "price": 780,
             "departure": "15:30", "arrival": "11:00+1", "duration": "10h 30m",
             "aircraft": "Airbus A350-900"},
            {"airline": "Delta", "flight_number": "DL79", "price": 820,
             "departure": "17:00", "arrival": "12:30+1", "duration": "10h 30m",
             "aircraft": "Airbus A330-900neo"},
        ],
    }

    # Lookup route
    route_key = (origin.upper(), destination.upper())
    flights = MOCK_FLIGHTS.get(route_key)

    if not flights:
        available_routes = ", ".join(f"{o}→{d}" for o, d in MOCK_FLIGHTS.keys())
        return {
            "status": "error",
            "error_message": f"No flights found for route {origin} → {destination}. Available routes: {available_routes}.",
            "origin": origin,
            "destination": destination,
            "available_routes": available_routes
        }

    # Filter by budget if specified
    if max_price is not None:
        flights = [f for f in flights if f["price"] <= max_price]
        if not flights:
            all_prices = [f["price"] for f in MOCK_FLIGHTS[route_key]]
            return {
                "status": "error",
                "error_message": f"No flights found under ${max_price} per person. Lowest available price: ${min(all_prices)}.",
                "max_price": max_price,
                "lowest_price": min(all_prices)
            }

    # Success response
    return {
        "status": "success",
        "flights": flights,
        "currency": "USD",
        "route": f"{origin} → {destination}",
        "date": departure_date,
        "passengers": passengers,
        "total_results": len(flights)
    }
```

### Complete Hotel Search Tool
```python
# Source: Workshop best practices
from datetime import datetime
from typing import Optional

def search_hotels(location: str, check_in: str, check_out: str,
                  guests: int = 1, max_price_per_night: Optional[int] = None) -> dict:
    """
    Search for available hotels in a destination.

    Args:
        location: City or area name (e.g., 'Tokyo', 'Paris', 'New York')
        check_in: Check-in date in YYYY-MM-DD format
        check_out: Check-out date in YYYY-MM-DD format
        guests: Number of guests, 1-8 (default 1)
        max_price_per_night: Maximum price per night in USD (optional)

    Returns:
        Dictionary with:
        - status: 'success' or 'error'
        - hotels: List of available hotels with pricing and ratings
        - error_message: Error details if status is 'error'
    """
    # Validate date formats
    try:
        checkin_dt = datetime.strptime(check_in, '%Y-%m-%d')
        checkout_dt = datetime.strptime(check_out, '%Y-%m-%d')
    except ValueError:
        return {
            "status": "error",
            "error_message": f"Invalid date format. Use YYYY-MM-DD.",
            "check_in": check_in,
            "check_out": check_out,
            "example": "2026-03-15"
        }

    # Validate date order
    if checkout_dt <= checkin_dt:
        return {
            "status": "error",
            "error_message": f"Check-out date ({check_out}) must be after check-in date ({check_in}).",
            "check_in": check_in,
            "check_out": check_out
        }

    # Validate dates in future
    if checkin_dt.date() < datetime.now().date():
        return {
            "status": "error",
            "error_message": f"Check-in date {check_in} is in the past. Please provide a future date.",
            "check_in": check_in
        }

    # Calculate nights
    nights = (checkout_dt - checkin_dt).days

    # Mock hotel database
    MOCK_HOTELS = {
        "tokyo": [
            {"name": "Park Hyatt Tokyo", "stars": 5, "price_per_night": 450, "rating": 4.8,
             "amenities": ["Pool", "Spa", "Restaurant", "Gym"]},
            {"name": "Shinjuku Granbell Hotel", "stars": 4, "price_per_night": 180, "rating": 4.5,
             "amenities": ["Restaurant", "Bar", "Gym"]},
            {"name": "MUJI Hotel Ginza", "stars": 4, "price_per_night": 220, "rating": 4.6,
             "amenities": ["Restaurant", "Minimalist design"]},
        ],
        "paris": [
            {"name": "Hotel Plaza Athénée", "stars": 5, "price_per_night": 850, "rating": 4.9,
             "amenities": ["Spa", "Restaurant", "Bar", "Concierge"]},
            {"name": "Hotel Brighton", "stars": 4, "price_per_night": 320, "rating": 4.6,
             "amenities": ["Restaurant", "Louvre view"]},
        ],
    }

    # Lookup location
    location_key = location.lower()
    hotels = MOCK_HOTELS.get(location_key)

    if not hotels:
        available_locations = ", ".join(MOCK_HOTELS.keys())
        return {
            "status": "error",
            "error_message": f"Location '{location}' not found in database. Available locations: {available_locations}.",
            "location": location,
            "available_locations": available_locations,
            "suggestion": f"Did you mean '{available_locations.split(',')[0]}'?"
        }

    # Filter by budget if specified
    if max_price_per_night is not None:
        hotels = [h for h in hotels if h["price_per_night"] <= max_price_per_night]
        if not hotels:
            all_prices = [h["price_per_night"] for h in MOCK_HOTELS[location_key]]
            return {
                "status": "error",
                "error_message": f"No hotels found under ${max_price_per_night} per night in {location}. Lowest available: ${min(all_prices)}/night.",
                "max_price_per_night": max_price_per_night,
                "lowest_price": min(all_prices)
            }

    # Add total cost to each hotel
    hotels_with_total = []
    for hotel in hotels:
        hotel_copy = hotel.copy()
        hotel_copy["total_cost"] = hotel["price_per_night"] * nights
        hotels_with_total.append(hotel_copy)

    # Success response
    return {
        "status": "success",
        "hotels": hotels_with_total,
        "location": location,
        "check_in": check_in,
        "check_out": check_out,
        "nights": nights,
        "guests": guests,
        "currency": "USD",
        "total_results": len(hotels_with_total)
    }
```

### Agent Configuration with Tools
```python
# Source: https://google.github.io/adk-docs/agents/llm-agents/
from google.adk.agents import Agent

# Create agent with function tools
agent = Agent(
    model='gemini-2.5-flash',
    name='travel_booking_assistant',
    description='A helpful travel booking assistant with real-time search.',

    instruction='''You are an expert travel booking assistant.

YOUR TOOLS:
- search_flights(): Search for available flights between airports
- search_hotels(): Find accommodation in destinations

HOW TO HELP:
1. When users ask about trips, gather key details:
   - Destination and dates
   - Number of travelers
   - Budget range (if not stated, ask)
   - Any special requirements

2. Use your tools to find real options:
   - Call search_flights() with proper airport codes (e.g., 'SFO' not 'San Francisco')
   - Call search_hotels() with city names
   - Pass budget constraints in max_price parameters

3. Present options clearly:
   - Show 2-3 best matches within their budget
   - Include prices and key details
   - Explain why you're recommending each option

4. Handle errors gracefully:
   - If tool returns error status, read the error_message
   - Help user correct the request (e.g., fix date format)
   - Suggest alternatives if no results found

5. Budget awareness:
   - If user states budget, ALWAYS filter to show only affordable options
   - Mention when excluding expensive options
   - Suggest how to adjust if nothing fits budget

TONE:
- Friendly and enthusiastic about travel
- Concise but informative
- Proactive in suggesting improvements

IMPORTANT: When calling tools, use proper formats:
- Airport codes: 3 letters uppercase (SFO, NRT, LAX, CDG)
- Dates: YYYY-MM-DD format (2026-03-15)
''',

    tools=[
        search_flights,
        search_hotels,
    ],
)

# Test multi-turn conversation with tool usage
print("=" * 60)
print("Travel Booking Assistant - Tool Calling Demo")
print("=" * 60)

test_queries = [
    "I want to fly from San Francisco to Tokyo in March",
    "My budget is $900 per person",
    "Great! Now find me a hotel in Tokyo for March 15-20",
]

for query in test_queries:
    print(f"\nYou: {query}")
    response = agent.generate_content(query)
    print(f"Agent: {response.text}")
```

### Exercise Structure (Notebook Cells)
```python
# Cell 1: Concept Introduction
"""
# Exercise 2: Function Calling & Tools

## What is Function Calling?

Function calling (also called "tool use") lets your agent take actions by calling
Python functions you provide. This is how agents access real-time data, perform
calculations, or interact with external systems.

**Tools vs RAG - The Decision Framework:**

Use TOOLS (this exercise) when:
✓ Data changes frequently (flight availability, hotel pricing)
✓ Requires API calls or calculations
✓ Need real-time information

Use RAG (Exercise 3) when:
✓ Data is static (destination guides, visa requirements)
✓ Information is in documents
✓ Need to search large knowledge base

**Example:**
- Flight search → TOOL (prices change every minute)
- "Best time to visit Japan" → RAG (static travel guide content)

⏱️ Estimated time: 30 minutes
"""

# Cell 2: Exercise 2A - Implement search_flights
"""
## Exercise 2A: Implement Flight Search Tool

Complete the `search_flights` function below. This is a mock API - it returns
sample data instead of calling a real travel API (avoiding costs and rate limits).

**Your tasks:**
1. Fill in the function signature with type hints
2. Write a descriptive docstring (Args and Returns sections)
3. Return mock flight data in the specified structure

**Hints:**
- Use type hints: `origin: str, destination: str`
- Include example airport codes in docstring: 'SFO', 'NRT'
- Return a dict with 'status', 'flights', 'currency', 'route', 'date'
"""

from typing import Optional

def search_flights(
    # TODO: Add parameters with type hints
    # origin: str
    # destination: str
    # departure_date: str
    # passengers: int = 1
    # max_price: Optional[int] = None
) -> dict:
    """
    TODO: Write docstring

    Args:
        TODO: Document each parameter

    Returns:
        TODO: Describe return structure
    """
    # TODO: Return mock flight data
    # Structure:
    # {
    #     "status": "success",
    #     "flights": [
    #         {"airline": "...", "price": ..., "departure": "...", "arrival": "..."},
    #     ],
    #     "currency": "USD",
    #     "route": f"{origin} → {destination}",
    #     "date": departure_date,
    # }
    pass

# Cell 3: Solution Check
"""
✅ Checkpoint: Test your function

Run this cell to test if your function works correctly.
"""
# Test the function
result = search_flights("SFO", "NRT", "2026-03-15", passengers=2)
print(result)

# Expected: Dictionary with 'status': 'success' and flight data

# Cell 4: Exercise 2B - Implement search_hotels
# (Similar structure to 2A)

# Cell 5: Exercise 2C - Add Error Handling
"""
## Exercise 2C: Add Error Handling

Real tools need to handle errors gracefully. Modify your `search_flights` function
to validate inputs and return error information.

**Key pattern: Errors in Context**
❌ DON'T raise exceptions - the LLM won't see them
✅ DO return error dicts - the LLM can read and respond

**Add these validations:**
1. Check date format (YYYY-MM-DD)
2. Ensure date is in the future
3. Return helpful error_message if validation fails
"""

# Cell 6: Exercise 2D - Add Tools to Agent
"""
## Exercise 2D: Create Agent with Tools

Now add your functions to the agent's `tools` parameter.
"""

from google.adk.agents import Agent

agent = Agent(
    model='gemini-2.5-flash',
    name='travel_assistant',
    description='Travel booking assistant with flight and hotel search',

    instruction='''You are a travel booking assistant.

    Use search_flights() and search_hotels() to help users plan trips.
    When a user mentions budget, filter results using max_price parameters.
    If a tool returns an error, help the user fix their request.
    ''',

    tools=[
        # TODO: Add your functions here
        # search_flights,
        # search_hotels,
    ],
)

# Cell 7: Test Tool Calling
"""
## Test Your Agent

Try these queries and watch your tools get called!
"""

test_queries = [
    "Find me flights from SFO to Tokyo on March 15",
    "My budget is $900",
    "Now find a hotel in Tokyo for March 15-20",
]

for query in test_queries:
    print(f"\n🧑 You: {query}")
    response = agent.generate_content(query)
    print(f"🤖 Agent: {response.text}")

# Cell 8: Challenge (Optional)
"""
## Challenge: Budget Filtering

The agent should remember budget from conversation context and filter results.

Test: Say "My budget is $800" then ask "Show me flights to Tokyo"
Expected: Only flights ≤$800 should appear
"""
```

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| Manual JSON schemas for tools | Type hints + docstrings → auto schema | ADK 1.0 | Less boilerplate, fewer schema errors |
| Exceptions in tool functions | Error dicts returned to LLM | Best practice 2024+ | LLM learns from errors, better recovery |
| Hard-coded tool logic | LLM-driven tool selection | GPT-4 function calling (2023) | Agent decides when to use tools contextually |
| Real APIs in workshops | Mock APIs with realistic data | Workshop best practice | Eliminates costs, rate limits, API key management |
| Single tool per task | Multiple tools, LLM orchestrates | Multi-tool agents (2024+) | More flexible, handles complex workflows |
| Tool results only | Errors-in-context pattern | ADK best practices (2025+) | Agent can retry, clarify, suggest alternatives |

**Deprecated/outdated:**
- **Manual OpenAPI schema definitions**: ADK generates these automatically from Python type hints
- **Pydantic models for simple tools**: Overkill for beginner exercises; primitives (str, int) sufficient
- **Real travel APIs in workshops**: Use mocks unless specifically teaching API integration
- **Generic error messages**: "Error occurred" → use specific "Invalid date format: use YYYY-MM-DD"

## Open Questions

Things that couldn't be fully resolved:

1. **Mock Data Realism vs Simplicity Tradeoff**
   - What we know: Mock data should match real API structures but be simple enough for beginners
   - What's unclear: Exact level of detail - include flight numbers? Aircraft types? Layovers?
   - Recommendation: Include realistic fields (airline, price, times, aircraft) but limit to 3-5 flights per route. No layovers/connections in basic exercises (add in optional challenge). Deterministic lookups (SFO→NRT always returns same flights) for reproducibility.

2. **When to Introduce Pydantic Models**
   - What we know: Pydantic provides structured outputs, better validation
   - What's unclear: Is Phase 2 too early? Will it overwhelm beginners?
   - Recommendation: Skip Pydantic in Phase 2 exercises. Use simple dicts with type hints. Mention Pydantic in "What's Next" for advanced learners. Focus on core concepts (docstrings, error handling) first.

3. **Budget Filtering: Tool Parameter vs Agent Logic**
   - What we know: AGENT-08 requires filtering by budget
   - What's unclear: Should max_price be tool parameter, or should agent filter results in instruction?
   - Recommendation: Add max_price as optional parameter to tools (shows parameterization), AND mention budget filtering in agent instruction (shows agent reasoning). This demonstrates both approaches: tool-level filtering (efficient) and agent-level reasoning (flexible).

4. **Error Handling Depth for Beginners**
   - What we know: Error-in-context is critical pattern
   - What's unclear: How many validation scenarios to show? Date format, future dates, route availability, budget... could overwhelm.
   - Recommendation: Start with one validation (date format) in Exercise 2C. Add more in optional challenges. Provide complete examples in reference implementation. Key is demonstrating the pattern, not exhaustive coverage.

5. **Real API Upgrade Path**
   - What we know: Participants may want to use real APIs post-workshop
   - What's unclear: Should we provide guidance on migrating from mock to real Amadeus/Skyscanner APIs?
   - Recommendation: Add "Next Steps" section in notebook: brief guide on real travel APIs (Amadeus Self-Service, Skyscanner, links to docs), note that function signature stays same (just swap implementation). Consider optional "bonus exercise" using real API for advanced participants.

## Sources

### Primary (HIGH confidence)
- [Google ADK Function Tools Documentation](https://google.github.io/adk-docs/tools-custom/function-tools/) - Official docs on type hints, docstrings, schema generation
- [Google ADK LLM Agents Documentation](https://google.github.io/adk-docs/agents/llm-agents/) - Agent configuration and tool integration
- [ADK Quickstart Multi-tool Agent](https://google.github.io/adk-docs/get-started/quickstart/) - Official examples of tools parameter
- [DataMock Flight API Explorer](https://datamock.dev/api-explorer/flight) - Realistic flight data schema structure

### Secondary (MEDIUM confidence)
- [RAG vs Function Calling - Stream Blog](https://getstream.io/blog/rag-function-calling/) - Decision framework for tools vs RAG
- [The Anatomy of Tool Calling in LLMs](https://martinuke0.github.io/posts/2026-01-07-the-anatomy-of-tool-calling-in-llms-a-deep-dive/) - Deep dive on function calling mechanics (Jan 2026)
- [Prompt Caching and LLM Costs - Medium](https://medium.com/beyond-localhost/prompt-caching-and-why-your-llm-bill-just-exploded-70e2c2a439c2) - Cache-friendly patterns (Jan 2026)
- [Designing Long-Running LLM Agent Workflows](https://palospublishing.com/designing-long-running-llm-agent-workflows/) - Error handling and retry patterns
- [Function Calling in AI Agents - Prompt Engineering Guide](https://www.promptingguide.ai/agents/function-calling) - General best practices

### Tertiary (LOW confidence)
- [GitHub: microservices-api/flight-booking](https://github.com/microservices-api/flight-booking) - Mock flight booking API structure
- [GitHub: Lemoncode/simple-hotels-mock-rest-api](https://github.com/Lemoncode/simple-hotels-mock-rest-api) - Simple mock hotel API for teaching
- [CodeRefinery Jupyter Exercises](https://coderefinery.github.io/jupyter/exercises/) - Workshop exercise patterns for Jupyter notebooks
- [Programming Workshop For Beginners](https://uwpyb.github.io/) - Workshop structure and mentoring approaches

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH - ADK docs confirm automatic schema generation from type hints, tested in official examples
- Architecture: HIGH - Function tool patterns verified in official docs, error-in-context widely documented
- Pitfalls: MEDIUM - Based on function calling best practices across frameworks, some ADK-specific insights from recent blog posts
- Mock data design: MEDIUM - Travel API structure verified from multiple sources (Amadeus, DataMock), but workshop-specific recommendations based on education best practices

**Research date:** 2026-01-24
**Valid until:** 2026-02-24 (30 days - ADK stable, but function calling patterns evolving)
**Recommended re-validation:** Check for ADK updates before workshop delivery, verify Gemini 2.5 Flash function calling behavior
