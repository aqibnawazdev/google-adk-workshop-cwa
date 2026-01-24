"""
Travel Booking Tools - Reference Implementation

Complete implementations of flight and hotel search functions.
These demonstrate proper patterns for ADK function tools:
- Type hints for automatic schema generation
- Google-style docstrings for LLM context
- Error-in-context pattern (return error dicts, don't raise exceptions)
- Budget filtering with optional max_price parameter
- Realistic mock data for deterministic testing
"""

from datetime import datetime
from typing import Optional

# ============================================================
# MOCK DATA (Deterministic for reproducible results)
# ============================================================

MOCK_FLIGHTS = {
    ("SFO", "NRT"): [
        {
            "airline": "United Airlines",
            "flight_number": "UA837",
            "price": 850,
            "departure": "08:30",
            "arrival": "14:30+1",
            "duration": "11h 00m",
            "aircraft": "Boeing 787-9",
        },
        {
            "airline": "ANA",
            "flight_number": "NH7",
            "price": 920,
            "departure": "11:00",
            "arrival": "17:00+1",
            "duration": "11h 00m",
            "aircraft": "Boeing 777-300ER",
        },
        {
            "airline": "JAL",
            "flight_number": "JL2",
            "price": 890,
            "departure": "13:45",
            "arrival": "19:45+1",
            "duration": "11h 00m",
            "aircraft": "Boeing 787-8",
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
        },
        {
            "airline": "Delta",
            "flight_number": "DL79",
            "price": 820,
            "departure": "17:00",
            "arrival": "12:30+1",
            "duration": "10h 30m",
            "aircraft": "Airbus A330-900neo",
        },
    ],
    ("JFK", "LHR"): [
        {
            "airline": "British Airways",
            "flight_number": "BA178",
            "price": 650,
            "departure": "19:00",
            "arrival": "07:00+1",
            "duration": "7h 00m",
            "aircraft": "Airbus A380",
        },
        {
            "airline": "Virgin Atlantic",
            "flight_number": "VS4",
            "price": 720,
            "departure": "21:30",
            "arrival": "09:30+1",
            "duration": "7h 00m",
            "aircraft": "Airbus A350-1000",
        },
    ],
}

MOCK_HOTELS = {
    "tokyo": [
        {
            "name": "Park Hyatt Tokyo",
            "stars": 5,
            "price_per_night": 450,
            "rating": 4.8,
            "amenities": ["Pool", "Spa", "Restaurant", "Gym", "Bar"],
            "location": "Shinjuku",
        },
        {
            "name": "Shinjuku Granbell Hotel",
            "stars": 4,
            "price_per_night": 180,
            "rating": 4.5,
            "amenities": ["Restaurant", "Bar", "Gym"],
            "location": "Shinjuku",
        },
        {
            "name": "MUJI Hotel Ginza",
            "stars": 4,
            "price_per_night": 220,
            "rating": 4.6,
            "amenities": ["Restaurant", "Minimalist design"],
            "location": "Ginza",
        },
        {
            "name": "Hoshinoya Tokyo",
            "stars": 5,
            "price_per_night": 680,
            "rating": 4.9,
            "amenities": ["Onsen", "Restaurant", "Spa", "Traditional"],
            "location": "Otemachi",
        },
    ],
    "paris": [
        {
            "name": "Hotel Plaza Athenee",
            "stars": 5,
            "price_per_night": 850,
            "rating": 4.9,
            "amenities": ["Spa", "Restaurant", "Bar", "Concierge"],
            "location": "Champs-Elysees",
        },
        {
            "name": "Hotel Brighton",
            "stars": 4,
            "price_per_night": 320,
            "rating": 4.6,
            "amenities": ["Restaurant", "Louvre view"],
            "location": "1st Arrondissement",
        },
        {
            "name": "Le Marais Boutique",
            "stars": 3,
            "price_per_night": 180,
            "rating": 4.4,
            "amenities": ["Breakfast", "WiFi"],
            "location": "Le Marais",
        },
    ],
    "london": [
        {
            "name": "The Savoy",
            "stars": 5,
            "price_per_night": 550,
            "rating": 4.8,
            "amenities": ["Spa", "Restaurant", "Bar", "Pool"],
            "location": "Strand",
        },
        {
            "name": "CitizenM Tower of London",
            "stars": 4,
            "price_per_night": 190,
            "rating": 4.5,
            "amenities": ["Bar", "24h Food", "Rooftop"],
            "location": "Tower Hill",
        },
    ],
}


# ============================================================
# FLIGHT SEARCH TOOL
# ============================================================

def search_flights(
    origin: str,
    destination: str,
    departure_date: str,
    passengers: int = 1,
    max_price: Optional[int] = None,
) -> dict:
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
        - flights: List of available flights with pricing
        - error_message: Error details if status is 'error'
    """
    # Debug output for learning
    print(f"search_flights called: {origin} -> {destination}, {departure_date}, {passengers} pax")

    # Validate date format
    try:
        departure_dt = datetime.strptime(departure_date, '%Y-%m-%d')
    except ValueError:
        return {
            "status": "error",
            "error_message": f"Invalid date format: '{departure_date}'. Use YYYY-MM-DD format.",
            "requested_date": departure_date,
            "example": "2026-03-15",
        }

    # Validate date is in future (for realism)
    if departure_dt.date() < datetime.now().date():
        return {
            "status": "error",
            "error_message": f"Departure date {departure_date} is in the past. Please provide a future date.",
            "requested_date": departure_date,
        }

    # Validate passenger count
    if not 1 <= passengers <= 9:
        return {
            "status": "error",
            "error_message": f"Passengers must be between 1 and 9. You requested {passengers}.",
            "requested_passengers": passengers,
        }

    # Lookup route in mock database
    route_key = (origin.upper(), destination.upper())
    flights = MOCK_FLIGHTS.get(route_key)

    if not flights:
        available_routes = ", ".join(f"{o}->{d}" for o, d in MOCK_FLIGHTS.keys())
        return {
            "status": "error",
            "error_message": f"No flights found for route {origin} -> {destination}.",
            "available_routes": available_routes,
            "suggestion": f"Try one of these routes: {available_routes}",
        }

    # Filter by budget if specified
    if max_price is not None:
        original_count = len(flights)
        flights = [f for f in flights if f["price"] <= max_price]
        if not flights:
            all_prices = [f["price"] for f in MOCK_FLIGHTS[route_key]]
            return {
                "status": "error",
                "error_message": f"No flights found under ${max_price}. Lowest price: ${min(all_prices)}.",
                "max_price": max_price,
                "lowest_available": min(all_prices),
                "suggestion": f"Increase budget to ${min(all_prices)} or try a different route.",
            }

    # Success response
    print(f"   Found {len(flights)} flights")
    return {
        "status": "success",
        "flights": flights,
        "currency": "USD",
        "route": f"{origin} -> {destination}",
        "date": departure_date,
        "passengers": passengers,
        "total_results": len(flights),
    }


# ============================================================
# HOTEL SEARCH TOOL
# ============================================================

def search_hotels(
    location: str,
    check_in: str,
    check_out: str,
    guests: int = 1,
    max_price_per_night: Optional[int] = None,
) -> dict:
    """
    Search for available hotels in a destination.

    Args:
        location: City or area name (e.g., 'Tokyo', 'Paris', 'London')
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
    # Debug output for learning
    print(f"search_hotels called: {location}, {check_in} to {check_out}, {guests} guests")

    # Validate date formats
    try:
        checkin_dt = datetime.strptime(check_in, '%Y-%m-%d')
        checkout_dt = datetime.strptime(check_out, '%Y-%m-%d')
    except ValueError:
        return {
            "status": "error",
            "error_message": "Invalid date format. Use YYYY-MM-DD format.",
            "check_in": check_in,
            "check_out": check_out,
            "example": "2026-03-15",
        }

    # Validate date order
    if checkout_dt <= checkin_dt:
        return {
            "status": "error",
            "error_message": f"Check-out date ({check_out}) must be after check-in date ({check_in}).",
            "check_in": check_in,
            "check_out": check_out,
        }

    # Validate check-in is in future
    if checkin_dt.date() < datetime.now().date():
        return {
            "status": "error",
            "error_message": f"Check-in date {check_in} is in the past. Please provide a future date.",
            "check_in": check_in,
        }

    # Calculate nights
    nights = (checkout_dt - checkin_dt).days

    # Lookup location in mock database
    location_key = location.lower().strip()
    hotels = MOCK_HOTELS.get(location_key)

    if not hotels:
        available_locations = ", ".join(MOCK_HOTELS.keys())
        # Check for close matches
        suggestion = None
        for loc in MOCK_HOTELS.keys():
            if loc in location_key or location_key in loc:
                suggestion = loc
                break
        return {
            "status": "error",
            "error_message": f"Location '{location}' not found.",
            "available_locations": available_locations,
            "suggestion": f"Did you mean '{suggestion}'?" if suggestion else f"Try: {available_locations}",
        }

    # Filter by budget if specified
    if max_price_per_night is not None:
        original_count = len(hotels)
        hotels = [h for h in hotels if h["price_per_night"] <= max_price_per_night]
        if not hotels:
            all_prices = [h["price_per_night"] for h in MOCK_HOTELS[location_key]]
            return {
                "status": "error",
                "error_message": f"No hotels found under ${max_price_per_night}/night. Lowest: ${min(all_prices)}/night.",
                "max_price_per_night": max_price_per_night,
                "lowest_available": min(all_prices),
                "suggestion": f"Increase budget to ${min(all_prices)}/night or try a different location.",
            }

    # Add total cost to each hotel
    hotels_with_total = []
    for hotel in hotels:
        hotel_copy = hotel.copy()
        hotel_copy["total_cost"] = hotel["price_per_night"] * nights
        hotel_copy["nights"] = nights
        hotels_with_total.append(hotel_copy)

    # Success response
    print(f"   Found {len(hotels_with_total)} hotels")
    return {
        "status": "success",
        "hotels": hotels_with_total,
        "location": location,
        "check_in": check_in,
        "check_out": check_out,
        "nights": nights,
        "guests": guests,
        "currency": "USD",
        "total_results": len(hotels_with_total),
    }
