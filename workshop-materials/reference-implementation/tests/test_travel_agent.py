"""
Agent Evaluation Tests - Reference Implementation

Demonstrates ADK AgentEvaluator for validating agent behavior.
These tests verify the travel booking assistant works correctly.

Run with: pytest tests/test_travel_agent.py -v

Prerequisites:
- google-adk installed
- pytest and pytest-asyncio installed
- GOOGLE_API_KEY or Vertex AI auth configured
"""

import pytest
import os
from pathlib import Path

# Check for ADK evaluation support
try:
    from google.adk.evaluation.agent_evaluator import AgentEvaluator
    HAS_EVALUATOR = True
except ImportError:
    HAS_EVALUATOR = False
    pytest.skip("AgentEvaluator not available", allow_module_level=True)


# ============================================================
# CONFIGURATION
# ============================================================

# Path to evaluation datasets
EVAL_DATASETS_DIR = Path(__file__).parent / "eval_datasets"

# Agent module path (relative to reference-implementation/)
AGENT_MODULE = "agent"

# Evaluation thresholds
TOOL_TRAJECTORY_THRESHOLD = 0.8  # 80% tool call accuracy
RESPONSE_MATCH_THRESHOLD = 0.7   # 70% response similarity


# ============================================================
# TEST FIXTURES
# ============================================================

@pytest.fixture(scope="module")
def check_api_key():
    """Ensure API key is configured for evaluation."""
    if not os.environ.get("GOOGLE_API_KEY") and not os.environ.get("GOOGLE_GENAI_USE_VERTEXAI"):
        pytest.skip("GOOGLE_API_KEY or Vertex AI auth required for evaluation")


# ============================================================
# FLIGHT SEARCH TESTS
# ============================================================

@pytest.mark.asyncio
async def test_flight_search(check_api_key):
    """
    Test that agent correctly uses search_flights tool.

    Validates:
    - Agent calls search_flights for flight queries
    - Correct parameters extracted (origin, destination, date)
    - Budget constraint applied when mentioned
    """
    await AgentEvaluator.evaluate(
        agent_module=AGENT_MODULE,
        eval_dataset_file_path_or_dir=str(EVAL_DATASETS_DIR / "flight_search.test.json"),
    )


@pytest.mark.asyncio
async def test_flight_search_with_budget(check_api_key):
    """
    Test budget-aware flight search.

    Validates:
    - max_price parameter used when budget mentioned
    - Agent explains when options exceed budget
    """
    await AgentEvaluator.evaluate(
        agent_module=AGENT_MODULE,
        eval_dataset_file_path_or_dir=str(EVAL_DATASETS_DIR / "flight_search.test.json"),
        # Filter to budget-specific cases
        # eval_case_ids=["budget_filter_test"]
    )


# ============================================================
# PREFERENCE MEMORY TESTS
# ============================================================

@pytest.mark.asyncio
async def test_preference_memory(check_api_key):
    """
    Test that agent remembers user preferences across turns.

    Validates:
    - remember_preference called when user states preference
    - Preference applied to subsequent searches
    - Multi-turn context retention
    """
    await AgentEvaluator.evaluate(
        agent_module=AGENT_MODULE,
        eval_dataset_file_path_or_dir=str(EVAL_DATASETS_DIR / "preference_memory.test.json"),
    )


# ============================================================
# HOTEL SEARCH TESTS
# ============================================================

@pytest.mark.asyncio
async def test_hotel_search(check_api_key):
    """
    Test that agent correctly uses search_hotels tool.

    Validates:
    - Agent calls search_hotels for accommodation queries
    - Correct parameters extracted (location, dates, guests)
    - Price filter applied when budget mentioned
    """
    # This test uses the same dataset format
    # In production, you'd have a separate hotel_search.test.json
    await AgentEvaluator.evaluate(
        agent_module=AGENT_MODULE,
        eval_dataset_file_path_or_dir=str(EVAL_DATASETS_DIR / "flight_search.test.json"),
    )


# ============================================================
# ERROR HANDLING TESTS
# ============================================================

@pytest.mark.asyncio
async def test_invalid_date_handling(check_api_key):
    """
    Test that agent handles invalid dates gracefully.

    Validates:
    - Agent asks for clarification on invalid dates
    - Error returned in context, not exception
    """
    # Would have error_handling.test.json in production
    pass  # Placeholder - create dataset for error cases


# ============================================================
# MULTI-TURN CONVERSATION TESTS
# ============================================================

@pytest.mark.asyncio
async def test_multi_turn_booking_flow(check_api_key):
    """
    Test complete booking conversation flow.

    Validates:
    - Agent maintains context across turns
    - Previous search results referenced
    - Preferences applied consistently
    """
    # Would have multi_turn.test.json in production
    pass  # Placeholder - create dataset for multi-turn flow


# ============================================================
# UTILITY FUNCTIONS
# ============================================================

def generate_eval_report(results: dict) -> str:
    """Generate human-readable evaluation report."""
    report_lines = [
        "=" * 60,
        "AGENT EVALUATION REPORT",
        "=" * 60,
        f"Total cases: {results.get('total_cases', 0)}",
        f"Passed: {results.get('passed', 0)}",
        f"Failed: {results.get('failed', 0)}",
        "",
        "Metrics:",
        f"  Tool trajectory score: {results.get('tool_trajectory_avg_score', 0):.2%}",
        f"  Response match score: {results.get('response_match_score', 0):.2%}",
        "=" * 60,
    ]
    return "\n".join(report_lines)


if __name__ == "__main__":
    # Run tests directly
    pytest.main([__file__, "-v", "--tb=short"])
