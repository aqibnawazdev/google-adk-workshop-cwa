"""
Google ADK Workshop - Complete Travel Booking Agent

This is the reference implementation showing what you'll build by the end of the workshop.
Each section is labeled with the exercise where you'll learn to build it.

Run with: adk run agent.py
Or in Colab: import this module and call create_agent()
"""

import os
from google.adk.agents import Agent

# ============================================================
# CONFIGURATION (Exercise 1: Setup)
# ============================================================

PROJECT_ID = os.environ.get('GOOGLE_CLOUD_PROJECT', 'your-project-id')
LOCATION = os.environ.get('GOOGLE_CLOUD_LOCATION', 'us-central1')
MODEL = 'gemini-2.5-flash'

# ============================================================
# TOOL FUNCTIONS (Exercise 2: Function Calling)
# ============================================================

# These functions let the agent search for real-time travel data.
# You'll implement these in Exercise 2.

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
    # TODO (Exercise 2): Implement with mock data or real API
    # For now, return sample data
    return {
        'flights': [
            {'airline': 'United', 'price': 850, 'departure': '08:30', 'arrival': '14:30+1'},
            {'airline': 'ANA', 'price': 920, 'departure': '11:00', 'arrival': '17:00+1'},
            {'airline': 'JAL', 'price': 890, 'departure': '13:45', 'arrival': '19:45+1'},
        ],
        'currency': 'USD',
        'route': f'{origin} → {destination}',
        'date': departure_date,
    }


def search_hotels(location: str, check_in: str, check_out: str,
                  guests: int = 1) -> dict:
    """
    Search for available hotels.

    Args:
        location: City or area name (e.g., 'Tokyo, Japan')
        check_in: Check-in date in YYYY-MM-DD format
        check_out: Check-out date in YYYY-MM-DD format
        guests: Number of guests (default 1)

    Returns:
        Dict with available hotels and rates
    """
    # TODO (Exercise 2): Implement with mock data or real API
    return {
        'hotels': [
            {'name': 'Park Hyatt Tokyo', 'stars': 5, 'price_per_night': 450, 'rating': 4.8},
            {'name': 'Shinjuku Granbell', 'stars': 4, 'price_per_night': 180, 'rating': 4.5},
            {'name': 'MUJI Hotel Ginza', 'stars': 4, 'price_per_night': 220, 'rating': 4.6},
        ],
        'location': location,
        'dates': f'{check_in} to {check_out}',
        'currency': 'USD',
    }


# ============================================================
# KNOWLEDGE BASE (Exercise 3: RAG Integration)
# ============================================================

# The agent can retrieve destination information from a knowledge base.
# You'll set this up with Vertex AI RAG in Exercise 3.

# RAG_CORPUS_ID = os.environ.get('RAG_CORPUS_ID', None)
#
# def get_destination_knowledge():
#     """Configure RAG knowledge base for destination information."""
#     if RAG_CORPUS_ID:
#         from google.adk.tools import VertexAIRag
#         return VertexAIRag(corpus_id=RAG_CORPUS_ID)
#     return None


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
        instruction='''You are an expert travel booking assistant.

YOUR CAPABILITIES:
- Search for flights between any airports worldwide
- Find hotels in any destination
- Provide destination information, visa requirements, and travel tips
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
# MAIN ENTRY POINT
# ============================================================

if __name__ == '__main__':
    # Create and test the agent
    agent = create_agent()

    # Simple test
    print("Travel Booking Assistant initialized!")
    print("Testing with a sample query...\n")

    response = agent.generate_content(
        "I want to plan a trip to Tokyo in March. "
        "Can you help me find flights from San Francisco?"
    )
    print(response.text)
