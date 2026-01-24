"""
Google ADK Workshop - Complete Travel Booking Agent

This is the reference implementation showing what you'll build by the end of the workshop.
Each section is labeled with the exercise where you'll learn to build it.

Run with: adk run agent.py
Or in Colab: import this module and call create_agent()
"""

import os
import asyncio
from google.adk.agents import Agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai.types import Content, Part
from tools import search_flights, search_hotels

# ============================================================
# CONFIGURATION (Exercise 1: Setup)
# ============================================================

PROJECT_ID = os.environ.get('GOOGLE_CLOUD_PROJECT', 'your-project-id')
LOCATION = os.environ.get('GOOGLE_CLOUD_LOCATION', 'us-central1')
MODEL = 'gemini-2.5-flash'

# ============================================================
# TOOL FUNCTIONS (Exercise 2: Function Calling)
# ============================================================

# Tool functions are now imported from tools.py (see import at top).
# The tools.py file contains complete implementations with:
# - Full validation and error handling
# - Budget filtering (max_price parameters)
# - Realistic mock data
# - Error-in-context pattern (returns error dicts, doesn't raise exceptions)
#
# You'll implement these patterns in Exercise 2.


# ============================================================
# KNOWLEDGE BASE (Exercise 3: RAG Integration)
# ============================================================

# The agent can retrieve destination information from a pre-indexed
# knowledge base using Vertex AI RAG Engine.
#
# IMPORTANT: Due to ADK constraints, RAG tools cannot be mixed with
# function calling tools in the same agent. For hybrid capabilities,
# see hybrid_agent.py which coordinates separate specialized agents.
#
# To enable RAG-only destination expert:
#   1. Set RAG_CORPUS_ID environment variable
#   2. Use create_destination_agent() from hybrid_agent.py
#
# For hybrid travel assistant (tools + RAG):
#   from hybrid_agent import HybridTravelAssistant
#   assistant = HybridTravelAssistant()
#   response = await assistant.assist("your query")

RAG_CORPUS_ID = os.environ.get('RAG_CORPUS_ID')

# Uncomment for Exercise 3 RAG-only agent:
# from rag_tools import create_destination_knowledge_tool
# destination_knowledge = create_destination_knowledge_tool()


# ============================================================
# AGENT DEFINITION (Exercise 1: Basic Agent)
# ============================================================

def create_agent() -> Agent:
    """
    Create the travel booking assistant agent.

    This agent combines:
    - Conversational ability (Exercise 1)
    - Function calling for bookings (Exercise 2)
    - Knowledge retrieval for destinations (Exercise 3)
    - Session memory for preferences (Exercise 4)
    """

    agent = Agent(
        model=MODEL,
        name='travel_booking_assistant',
        description='A helpful travel booking assistant that can search flights, '
                    'find hotels, and provide destination information.',

        # The instruction is where context engineering happens
        rag_capability = ("- Provide destination information from knowledge base (visa, attractions, culture)"
                         if RAG_CORPUS_ID else "# Knowledge base access coming in Exercise 3")

        instruction=f'''You are an expert travel booking assistant.

YOUR CAPABILITIES:
- Search for flights between any airports worldwide
- Find hotels in any destination
{rag_capability}
- Remember user preferences (budget, travel style, dietary needs)

HOW TO HELP:
1. When users ask about trips, gather key details:
   - Destination and dates
   - Number of travelers
   - Budget range (if not stated, ask)
   - Any special requirements

2. Use your tools to find real options:
   - search_flights() for flight options
   - search_hotels() for accommodation
   - Knowledge base for destination info

3. Present options clearly:
   - Show 2-3 best matches for their criteria
   - Explain why you're recommending each option
   - Include prices and key details

4. Remember preferences across the conversation:
   - If they mention budget once, apply it to all searches
   - Note dietary restrictions for restaurant suggestions
   - Track their preferred travel style (luxury, budget, adventure)

BUDGET AWARENESS:
- If user mentions a budget, use max_price parameter for flights and max_price_per_night for hotels
- When options are excluded due to budget constraints, explain this clearly
- If nothing fits their budget, suggest the lowest available price or alternative options
- Be proactive about budget - if they say "under $800", filter aggressively

TONE:
- Friendly and enthusiastic about travel
- Concise but informative
- Proactive in suggesting improvements

If you can't find what they need, suggest alternatives or ask clarifying questions.
''',

        # Tools: Functions the agent can call (Exercise 2)
        tools=[
            search_flights,
            search_hotels,
            # get_destination_knowledge(),  # Uncomment in Exercise 3
        ],

        # Session config would go here (Exercise 4)
        # session_config=SessionConfig(...)
    )

    return agent


# ============================================================
# HYBRID ASSISTANT (Exercise 3 Complete)
# ============================================================

# For the complete travel assistant with both booking tools AND
# destination knowledge, use the hybrid assistant:
#
# from hybrid_agent import HybridTravelAssistant
# assistant = HybridTravelAssistant()
# response = await assistant.assist("Find flights to Tokyo and visa requirements")
#
# This coordinates two specialized agents to provide comprehensive answers.


# ============================================================
# MAIN ENTRY POINT
# ============================================================

async def test_agent():
    """
    Test the agent using the proper Runner + Sessions pattern.

    This demonstrates the CORRECT way to use ADK agents:
    1. Create a session service
    2. Create a session for the conversation
    3. Create a runner
    4. Run queries with async event handling
    """
    # Create agent
    agent = create_agent()

    print("Travel Booking Assistant initialized!")
    print("Testing with a sample query...\n")

    # Create session service and session
    session_service = InMemorySessionService()
    session = await session_service.create_session(
        app_name=agent.name,
        user_id='test_user'
    )

    # Create runner
    runner = Runner(
        agent=agent,
        session_service=session_service,
        app_name=agent.name
    )

    # Run query
    query = "I want to plan a trip to Tokyo in March. Can you help me find flights from San Francisco?"
    print(f"Query: {query}\n")

    final_response = ""
    async for event in runner.run_async(
        user_id='test_user',
        session_id=session.id,
        new_message=Content(parts=[Part(text=query)], role="user")
    ):
        # Show when tools are called
        if hasattr(event.content, 'parts'):
            for part in event.content.parts:
                if hasattr(part, 'function_call') and part.function_call:
                    print(f"🔧 Tool called: {part.function_call.name}")

        if event.is_final_response():
            final_response = event.content.parts[0].text
            break

    print(f"\nResponse:\n{final_response}")

if __name__ == '__main__':
    # Run the test with proper async pattern
    asyncio.run(test_agent())
