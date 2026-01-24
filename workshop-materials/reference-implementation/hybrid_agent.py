"""
Hybrid Travel Assistant - Reference Implementation

Demonstrates combining function calling tools (flights, hotels) with
RAG knowledge retrieval (destination guides) using coordinated agents.

KEY CONSTRAINT:
ADK's VertexAiRagRetrieval tool CANNOT be mixed with other tools in the
same agent. This module shows the workaround: separate specialized agents
with routing/coordination logic.

Pattern: Sequential Agent Coordination
1. Analyze user query
2. Route to appropriate agent (booking or knowledge)
3. Optionally enrich results with complementary agent
4. Return combined response
"""

import os
import asyncio
from typing import Optional
from google.adk.agents import Agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai.types import Content, Part

from tools import search_flights, search_hotels
from rag_tools import create_destination_knowledge_tool
from state_utils import (
    remember_preference,
    get_preference,
    get_preference_injection_block,
    get_budget_from_state,
)


# ============================================================
# CONFIGURATION
# ============================================================

MODEL = os.environ.get('MODEL', 'gemini-2.5-flash')
RAG_CORPUS_ID = os.environ.get('RAG_CORPUS_ID')


# ============================================================
# SPECIALIZED AGENTS
# ============================================================

def create_booking_agent() -> Agent:
    """
    Create agent for real-time booking searches with preference awareness.
    Uses function calling tools (flights, hotels) and preference tools.
    """
    # Get preference injection block for state-aware instruction
    preference_block = get_preference_injection_block()

    return Agent(
        model=MODEL,
        name='booking_agent',
        description='Search for flights and hotels with real-time availability and preference awareness.',

        instruction=f'''You search for travel bookings using real-time data.

{preference_block}

YOUR CAPABILITIES:
- Search for flights between airports worldwide
- Search for hotels in any destination
- Filter by dates, passengers/guests, and budget
- Remember and apply user preferences automatically

HOW TO HELP:
1. Use search_flights() for flight queries
2. Use search_hotels() for accommodation queries
3. Apply saved budget automatically (from preferences above)
4. If no budget set, ask when showing prices
5. Present 2-3 best options with clear pricing
6. Use remember_preference() when user mentions a budget or preference

You CANNOT provide destination information (visa, culture, weather).
For that, users should ask the destination expert.''',

        tools=[search_flights, search_hotels, remember_preference, get_preference],
    )


def create_destination_agent() -> Optional[Agent]:
    """
    Create agent for destination knowledge retrieval.
    Uses RAG tool ONLY (single-tool constraint).

    Returns None if RAG corpus not configured.
    """
    if not RAG_CORPUS_ID:
        print("Warning: RAG_CORPUS_ID not set, destination agent unavailable")
        return None

    destination_tool = create_destination_knowledge_tool()

    return Agent(
        model=MODEL,
        name='destination_expert',
        description='Provide destination information from travel guide knowledge base.',

        instruction='''You are a travel destination expert with access to comprehensive guides.

YOUR CAPABILITIES:
- Retrieve information from destination guides
- Answer questions about visa requirements, attractions, weather
- Provide cultural tips, safety info, transportation advice
- Share food and dining recommendations

YOUR LIMITATIONS:
- You CANNOT search for flights or hotels (no real-time data)
- You CANNOT provide current prices or booking availability
- Your knowledge comes from static travel guides

HOW TO HELP:
1. Use retrieve_destination_info tool for all destination queries
2. Combine information from multiple guide sections
3. Cite specific details when available
4. Recommend booking tools for real-time availability''',

        tools=[destination_tool],  # ONLY RAG tool (constraint)
    )


# ============================================================
# HYBRID COORDINATOR
# ============================================================

class HybridTravelAssistant:
    """
    Coordinates booking and destination agents for comprehensive travel assistance.

    Routes queries to appropriate agent and optionally enriches responses
    with complementary information.
    """

    # Keywords for routing
    BOOKING_KEYWORDS = {
        'flight', 'hotel', 'book', 'reserve', 'search', 'find',
        'availability', 'price', 'cost', 'dates', 'passengers'
    }

    KNOWLEDGE_KEYWORDS = {
        'visa', 'require', 'weather', 'season', 'attraction', 'visit',
        'culture', 'custom', 'tip', 'safety', 'transport', 'food', 'eat'
    }

    # Destination extraction (simplified - production would use NER)
    DESTINATIONS = {
        'tokyo': 'Tokyo', 'japan': 'Tokyo',
        'paris': 'Paris', 'france': 'Paris',
        'new york': 'New York', 'nyc': 'New York',
        'singapore': 'Singapore',
        'london': 'London', 'uk': 'London',
        'rome': 'Rome', 'italy': 'Rome',
        'bangkok': 'Bangkok', 'thailand': 'Bangkok',
        'sydney': 'Sydney', 'australia': 'Sydney',
        'barcelona': 'Barcelona', 'spain': 'Barcelona',
        'dubai': 'Dubai', 'uae': 'Dubai',
    }

    def __init__(self):
        self.booking_agent = create_booking_agent()
        self.destination_agent = create_destination_agent()
        self.session_service = InMemorySessionService()

    def _detect_intent(self, query: str) -> tuple[bool, bool]:
        """Detect if query needs booking and/or knowledge agents."""
        query_lower = query.lower()

        needs_booking = any(kw in query_lower for kw in self.BOOKING_KEYWORDS)
        needs_knowledge = any(kw in query_lower for kw in self.KNOWLEDGE_KEYWORDS)

        return needs_booking, needs_knowledge

    def _extract_destination(self, query: str) -> Optional[str]:
        """Extract destination from query."""
        query_lower = query.lower()
        for keyword, city in self.DESTINATIONS.items():
            if keyword in query_lower:
                return city
        return None

    async def _run_agent(self, agent: Agent, query: str) -> str:
        """Run an agent and get response."""
        session = await self.session_service.create_session(
            app_name=agent.name,
            user_id='hybrid_user'
        )

        runner = Runner(
            agent=agent,
            session_service=self.session_service,
            app_name=agent.name
        )

        response_text = ""
        async for event in runner.run_async(
            user_id='hybrid_user',
            session_id=session.id,
            new_message=Content(parts=[Part(text=query)], role="user")
        ):
            if event.is_final_response():
                response_text = event.content.parts[0].text
                break

        return response_text

    async def assist(self, user_query: str) -> str:
        """
        Process user query with appropriate agent(s).

        Routing logic:
        1. Booking-only query -> booking agent
        2. Knowledge-only query -> destination agent
        3. Mixed query -> booking agent + enrich with destination tips
        4. Ambiguous -> booking agent as default
        """
        needs_booking, needs_knowledge = self._detect_intent(user_query)
        destination = self._extract_destination(user_query)

        # Knowledge-only query
        if needs_knowledge and not needs_booking:
            if self.destination_agent:
                print("Routing to destination expert...")
                return await self._run_agent(self.destination_agent, user_query)
            else:
                return "Destination knowledge unavailable. Please configure RAG_CORPUS_ID."

        # Booking query (with optional enrichment)
        if needs_booking:
            print("Routing to booking agent...")
            booking_response = await self._run_agent(self.booking_agent, user_query)

            # Enrich with destination tips if destination detected
            if destination and self.destination_agent:
                print(f"Enriching with {destination} tips...")
                tip_query = f"What are the top 3 tips for visiting {destination}?"
                tips = await self._run_agent(self.destination_agent, tip_query)

                booking_response = (
                    f"{booking_response}\n\n"
                    f"**{destination} Travel Tips:**\n{tips}"
                )

            # After booking response, offer to save preferences if budget mentioned
            query_lower = user_query.lower()
            if "budget" in query_lower or "$" in user_query or "under" in query_lower:
                if "remember" not in booking_response.lower() and "saved" not in booking_response.lower():
                    booking_response += "\n\n_Tip: I can remember your budget for future searches. Just say 'remember my budget is $X'._"

            return booking_response

        # Default to booking agent
        print("Routing to booking agent (default)...")
        return await self._run_agent(self.booking_agent, user_query)


# ============================================================
# CONVENIENCE FUNCTION
# ============================================================

async def hybrid_travel_assistant(query: str) -> str:
    """
    One-call function for hybrid travel assistance.

    Example:
        response = await hybrid_travel_assistant(
            "Find flights from SFO to Tokyo and tell me about visa requirements"
        )
    """
    assistant = HybridTravelAssistant()
    return await assistant.assist(query)


# ============================================================
# DEMO
# ============================================================

async def demo():
    """Demonstrate hybrid assistant capabilities."""
    assistant = HybridTravelAssistant()

    test_queries = [
        "Find me flights from SFO to Tokyo on March 15, budget $900",
        "What are the visa requirements for US citizens visiting Japan?",
        "Search for hotels in Paris, March 20-25, under $300/night",
        "What cultural customs should I know before visiting Tokyo?",
    ]

    print("=" * 60)
    print("Hybrid Travel Assistant Demo")
    print("=" * 60)

    for query in test_queries:
        print(f"\nUser: {query}")
        print("-" * 40)
        response = await assistant.assist(query)
        print(f"Assistant: {response[:500]}...")  # Truncate for demo
        print()


if __name__ == "__main__":
    asyncio.run(demo())
