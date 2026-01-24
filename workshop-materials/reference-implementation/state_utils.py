"""
State Management Utilities - Reference Implementation

Demonstrates ADK state prefix patterns for preference persistence.
Used by agents to remember user preferences across sessions.

State Prefixes:
- No prefix: session-scoped (current conversation only)
- user: prefix: persists across all user sessions
- temp: prefix: current invocation only (never persists)
- app: prefix: shared across all users/sessions (app-wide config)

Exercise 4 Reference
"""

from typing import Optional, Any, List


# ============================================================
# PREFERENCE CONSTANTS (Exercise 4)
# ============================================================

# Supported preference types with their state keys
PREFERENCE_KEYS = {
    "budget": "user:budget",
    "travel_style": "user:travel_style",
    "dietary_restrictions": "user:dietary_restrictions",
    "preferred_airlines": "user:preferred_airlines",
    "hotel_rating_min": "user:hotel_rating_min",
}

# Default values for preferences (used when not set)
PREFERENCE_DEFAULTS = {
    "budget": None,  # No budget filter
    "travel_style": "balanced",  # Options: budget, balanced, luxury
    "dietary_restrictions": [],
    "preferred_airlines": [],
    "hotel_rating_min": 3,
}


# ============================================================
# TOOL FUNCTIONS (for agent use)
# ============================================================

def remember_preference(
    preference_type: str,
    value: str,
    tool_context: Any = None
) -> str:
    """
    Store user preference with user: prefix for cross-session persistence.

    Args:
        preference_type: Type of preference (budget, travel_style, dietary_restrictions)
        value: Value to store (will be converted appropriately)
        tool_context: ADK tool context with state access (injected by ADK)

    Returns:
        Confirmation message

    Example:
        remember_preference("budget", "1500", tool_context)
        # Stores as tool_context.state["user:budget"] = 1500
    """
    if preference_type not in PREFERENCE_KEYS:
        return f"Unknown preference type: {preference_type}. Valid types: {list(PREFERENCE_KEYS.keys())}"

    state_key = PREFERENCE_KEYS[preference_type]

    # If no tool_context provided, return instruction (for testing/demo)
    if tool_context is None:
        return f"Would store {preference_type}={value} at key '{state_key}'"

    # Parse value based on type
    if preference_type == "budget":
        # Extract numeric value (handle "$1500" -> 1500)
        numeric_value = ''.join(c for c in value if c.isdigit())
        if numeric_value:
            tool_context.state[state_key] = int(numeric_value)
        else:
            return f"Could not parse budget from: {value}"
    elif preference_type == "dietary_restrictions":
        # Store as list
        if isinstance(value, str):
            restrictions = [r.strip() for r in value.split(",")]
            tool_context.state[state_key] = restrictions
        else:
            tool_context.state[state_key] = value
    elif preference_type == "preferred_airlines":
        # Store as list
        if isinstance(value, str):
            airlines = [a.strip() for a in value.split(",")]
            tool_context.state[state_key] = airlines
        else:
            tool_context.state[state_key] = value
    else:
        tool_context.state[state_key] = value

    return f"Got it! I'll remember that your {preference_type} is {value}."


def get_preference(
    preference_type: str,
    tool_context: Any = None
) -> str:
    """
    Retrieve stored preference.

    Args:
        preference_type: Type of preference to retrieve
        tool_context: ADK tool context with state access (injected by ADK)

    Returns:
        Preference value or message if not set
    """
    if preference_type not in PREFERENCE_KEYS:
        return f"Unknown preference type: {preference_type}"

    state_key = PREFERENCE_KEYS[preference_type]

    # If no tool_context provided, return instruction (for testing/demo)
    if tool_context is None:
        default = PREFERENCE_DEFAULTS.get(preference_type)
        return f"Would retrieve from key '{state_key}'. Default: {default}"

    value = tool_context.state.get(state_key)

    if value is not None:
        return f"Your {preference_type} is set to: {value}"
    else:
        default = PREFERENCE_DEFAULTS.get(preference_type)
        return f"No {preference_type} preference set. Default: {default}"


def clear_preference(
    preference_type: str,
    tool_context: Any = None
) -> str:
    """
    Clear a stored preference.

    Args:
        preference_type: Type of preference to clear
        tool_context: ADK tool context (injected by ADK)

    Returns:
        Confirmation message
    """
    if preference_type not in PREFERENCE_KEYS:
        return f"Unknown preference type: {preference_type}"

    state_key = PREFERENCE_KEYS[preference_type]

    # If no tool_context provided, return instruction (for testing/demo)
    if tool_context is None:
        return f"Would clear preference at key '{state_key}'"

    if state_key in tool_context.state:
        del tool_context.state[state_key]
        return f"Cleared your {preference_type} preference."
    else:
        return f"No {preference_type} preference was set."


# ============================================================
# HELPER FUNCTIONS (for internal use)
# ============================================================

def get_budget_from_state(state: dict) -> Optional[int]:
    """
    Get budget from state dictionary, or None if not set.

    Args:
        state: State dictionary (from session or tool_context.state)

    Returns:
        Budget as integer, or None if not set
    """
    return state.get("user:budget")


def get_travel_style(state: dict) -> str:
    """
    Get travel style from state, with default.

    Args:
        state: State dictionary

    Returns:
        Travel style string (budget, balanced, or luxury)
    """
    return state.get("user:travel_style", "balanced")


def get_dietary_restrictions(state: dict) -> List[str]:
    """
    Get dietary restrictions from state, as list.

    Args:
        state: State dictionary

    Returns:
        List of dietary restriction strings
    """
    restrictions = state.get("user:dietary_restrictions", [])
    if isinstance(restrictions, str):
        return [r.strip() for r in restrictions.split(",")]
    return restrictions


def get_preferred_airlines(state: dict) -> List[str]:
    """
    Get preferred airlines from state, as list.

    Args:
        state: State dictionary

    Returns:
        List of airline names/codes
    """
    airlines = state.get("user:preferred_airlines", [])
    if isinstance(airlines, str):
        return [a.strip() for a in airlines.split(",")]
    return airlines


def get_hotel_rating_min(state: dict) -> int:
    """
    Get minimum hotel rating from state, with default.

    Args:
        state: State dictionary

    Returns:
        Minimum hotel star rating (1-5)
    """
    return state.get("user:hotel_rating_min", 3)


# ============================================================
# STATE INJECTION TEMPLATE
# ============================================================

def get_preference_injection_block() -> str:
    """
    Get the state injection block for agent instructions.

    Use this in your agent's instruction to inject saved preferences.
    The {key?} syntax means "optional" - won't error if key missing.

    Returns:
        Multi-line string for instruction template
    """
    return '''
Current user preferences (from previous conversations):
- Budget: ${user:budget?} (empty if not set)
- Travel style: {user:travel_style?}
- Dietary restrictions: {user:dietary_restrictions?}
- Preferred airlines: {user:preferred_airlines?}
- Minimum hotel rating: {user:hotel_rating_min?} stars

If a preference is set, apply it automatically to searches.
If not set (empty above), ask the user when relevant.
'''


# ============================================================
# STATE UTILITY DOCUMENTATION
# ============================================================

STATE_PREFIX_DOCUMENTATION = """
ADK State Prefixes - Quick Reference
====================================

1. No Prefix (Session-Scoped)
   - Example: state["conversation_count"] = 5
   - Persists: Current session only
   - Use for: Temporary conversation context

2. user: Prefix (User-Scoped)
   - Example: state["user:budget"] = 1500
   - Persists: Across all sessions for this user
   - Use for: User preferences, settings, history

3. temp: Prefix (Invocation-Scoped)
   - Example: state["temp:search_results"] = [...]
   - Persists: Current tool invocation only
   - Use for: Intermediate calculations, caching

4. app: Prefix (App-Scoped)
   - Example: state["app:exchange_rate"] = 1.05
   - Persists: Shared across all users/sessions
   - Use for: Global config, shared data

State Injection in Instructions
===============================

Use {key?} syntax for optional state injection:
- {user:budget?} - inserts user's budget, empty if not set
- {user:name?} - inserts user's name, empty if not set

The ? makes it optional (no error if missing).
"""
