"""
Workshop Cost Tracking Utility - Reference Implementation

Track token usage and estimate costs for ADK agents during workshop sessions.
Use this to understand API costs and plan for production deployments.

Pricing based on Gemini 2.5 Flash (as of 2026-01):
- Input: $0.30 per 1M tokens  (prompts under 128K tokens)
- Output: $2.50 per 1M tokens (thinking mode)

Exercise 4 Reference - Post-workshop utility for cost awareness
"""

import json
from dataclasses import dataclass, field, asdict
from typing import Optional, List, Any
from datetime import datetime


# ============================================================
# GEMINI 2.5 FLASH PRICING (per 1M tokens)
# ============================================================

PRICING = {
    "gemini-2.5-flash": {
        "input_per_million": 0.30,   # $0.30 per 1M input tokens
        "output_per_million": 2.50,  # $2.50 per 1M output tokens (thinking mode)
    },
    "gemini-2.0-flash": {
        "input_per_million": 0.10,   # $0.10 per 1M input tokens
        "output_per_million": 0.40,  # $0.40 per 1M output tokens
    },
}

# Default model for workshop
DEFAULT_MODEL = "gemini-2.5-flash"


# ============================================================
# DATA CLASSES
# ============================================================

@dataclass
class TokenUsage:
    """Record of a single query's token usage."""
    input_tokens: int
    output_tokens: int
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    model: str = DEFAULT_MODEL
    query_preview: str = ""  # First 50 chars of query for reference


@dataclass
class CostSummary:
    """Aggregated cost summary for a session."""
    total_input_tokens: int
    total_output_tokens: int
    total_queries: int
    input_cost_usd: float
    output_cost_usd: float
    total_cost_usd: float
    model: str


# ============================================================
# COST TRACKER CLASS
# ============================================================

class WorkshopCostTracker:
    """
    Track token usage and costs for workshop sessions.

    Usage:
        tracker = WorkshopCostTracker()

        # Option 1: Log from ADK response with usage_metadata
        tracker.log_query(response, query="Find flights to Tokyo")

        # Option 2: Log tokens directly (if you have counts)
        tracker.log_tokens_directly(input_tokens=150, output_tokens=50)

        # Get summary
        summary = tracker.get_summary()
        print(f"Total cost: ${summary.total_cost_usd:.4f}")

        # Print formatted report
        tracker.print_report()
    """

    def __init__(self, model: str = DEFAULT_MODEL):
        """
        Initialize the cost tracker.

        Args:
            model: Model name for pricing lookup (default: gemini-2.5-flash)
        """
        self.model = model
        self.usage_records: List[TokenUsage] = []

        if model not in PRICING:
            print(f"Warning: Unknown model '{model}'. Using {DEFAULT_MODEL} pricing.")
            self.model = DEFAULT_MODEL

    def log_query(self, response: Any, query: str = "") -> Optional[TokenUsage]:
        """
        Log token usage from an ADK response with usage_metadata.

        Args:
            response: ADK response object with usage_metadata attribute
            query: Optional query text for reference

        Returns:
            TokenUsage record if usage_metadata found, None otherwise

        Example:
            async for event in runner.run_async(...):
                if event.is_final_response():
                    tracker.log_query(event, query="Find flights")
        """
        # Try to extract usage_metadata from response
        usage_metadata = None

        # Handle different response structures
        if hasattr(response, 'usage_metadata'):
            usage_metadata = response.usage_metadata
        elif hasattr(response, 'content') and hasattr(response.content, 'usage_metadata'):
            usage_metadata = response.content.usage_metadata
        elif isinstance(response, dict) and 'usage_metadata' in response:
            usage_metadata = response['usage_metadata']

        if usage_metadata is None:
            # No usage metadata found - can't track
            return None

        # Extract token counts
        input_tokens = getattr(usage_metadata, 'prompt_token_count', 0)
        output_tokens = getattr(usage_metadata, 'candidates_token_count', 0)

        # Handle dict-style access
        if isinstance(usage_metadata, dict):
            input_tokens = usage_metadata.get('prompt_token_count', 0)
            output_tokens = usage_metadata.get('candidates_token_count', 0)

        return self.log_tokens_directly(
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            query=query
        )

    def log_tokens_directly(
        self,
        input_tokens: int,
        output_tokens: int,
        query: str = ""
    ) -> TokenUsage:
        """
        Log token usage directly when you have the counts.

        Args:
            input_tokens: Number of input (prompt) tokens
            output_tokens: Number of output (response) tokens
            query: Optional query text for reference

        Returns:
            TokenUsage record
        """
        record = TokenUsage(
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            model=self.model,
            query_preview=query[:50] if query else ""
        )
        self.usage_records.append(record)
        return record

    def get_summary(self) -> CostSummary:
        """
        Get aggregated cost summary for all logged queries.

        Returns:
            CostSummary with totals and costs
        """
        total_input = sum(r.input_tokens for r in self.usage_records)
        total_output = sum(r.output_tokens for r in self.usage_records)

        pricing = PRICING.get(self.model, PRICING[DEFAULT_MODEL])

        # Calculate costs (tokens / 1M * price per 1M)
        input_cost = (total_input / 1_000_000) * pricing["input_per_million"]
        output_cost = (total_output / 1_000_000) * pricing["output_per_million"]

        return CostSummary(
            total_input_tokens=total_input,
            total_output_tokens=total_output,
            total_queries=len(self.usage_records),
            input_cost_usd=input_cost,
            output_cost_usd=output_cost,
            total_cost_usd=input_cost + output_cost,
            model=self.model
        )

    def print_report(self) -> None:
        """Print a formatted cost report to console."""
        summary = self.get_summary()
        pricing = PRICING.get(self.model, PRICING[DEFAULT_MODEL])

        print("=" * 50)
        print("WORKSHOP COST REPORT")
        print("=" * 50)
        print(f"Model: {summary.model}")
        print(f"Queries: {summary.total_queries}")
        print("-" * 50)
        print("TOKEN USAGE:")
        print(f"  Input tokens:  {summary.total_input_tokens:,}")
        print(f"  Output tokens: {summary.total_output_tokens:,}")
        print("-" * 50)
        print("COSTS:")
        print(f"  Input cost:    ${summary.input_cost_usd:.4f}")
        print(f"  Output cost:   ${summary.output_cost_usd:.4f}")
        print(f"  TOTAL:         ${summary.total_cost_usd:.4f}")
        print("-" * 50)
        print("PRICING (per 1M tokens):")
        print(f"  Input:  ${pricing['input_per_million']:.2f}")
        print(f"  Output: ${pricing['output_per_million']:.2f}")
        print("=" * 50)

    def export_json(self, filepath: str = "cost_report.json") -> str:
        """
        Export cost data to JSON file.

        Args:
            filepath: Output file path

        Returns:
            Path to the exported file
        """
        summary = self.get_summary()

        data = {
            "summary": asdict(summary),
            "records": [asdict(r) for r in self.usage_records],
            "exported_at": datetime.now().isoformat()
        }

        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)

        return filepath

    def reset(self) -> None:
        """Clear all recorded usage data."""
        self.usage_records = []


# ============================================================
# WORKSHOP COST ESTIMATION
# ============================================================

def estimate_workshop_cost(
    participants: int = 25,
    queries_per_participant: int = 20,
    avg_input_tokens: int = 500,
    avg_output_tokens: int = 200,
    model: str = DEFAULT_MODEL
) -> dict:
    """
    Estimate total cost for a workshop session.

    Use this for planning and budgeting workshop resources.

    Args:
        participants: Number of workshop participants
        queries_per_participant: Expected queries per person
        avg_input_tokens: Average input tokens per query
        avg_output_tokens: Average output tokens per query
        model: Model to use for pricing

    Returns:
        Dictionary with cost estimates

    Example:
        estimate = estimate_workshop_cost(participants=30)
        print(f"Expected cost: ${estimate['total_cost']:.2f}")
    """
    pricing = PRICING.get(model, PRICING[DEFAULT_MODEL])

    total_queries = participants * queries_per_participant
    total_input = total_queries * avg_input_tokens
    total_output = total_queries * avg_output_tokens

    input_cost = (total_input / 1_000_000) * pricing["input_per_million"]
    output_cost = (total_output / 1_000_000) * pricing["output_per_million"]

    return {
        "participants": participants,
        "queries_per_participant": queries_per_participant,
        "total_queries": total_queries,
        "total_input_tokens": total_input,
        "total_output_tokens": total_output,
        "input_cost": input_cost,
        "output_cost": output_cost,
        "total_cost": input_cost + output_cost,
        "model": model,
        "pricing": pricing,
        "cost_per_participant": (input_cost + output_cost) / participants,
    }


# ============================================================
# DEMO / CLI
# ============================================================

if __name__ == "__main__":
    print("Workshop Cost Tracker Demo")
    print("=" * 50)
    print()

    # Demo 1: Track individual queries
    print("DEMO 1: Tracking individual queries")
    print("-" * 50)

    tracker = WorkshopCostTracker()

    # Simulate some workshop queries
    tracker.log_tokens_directly(500, 150, "Find flights from SFO to Tokyo")
    tracker.log_tokens_directly(600, 200, "What hotels are available in Tokyo?")
    tracker.log_tokens_directly(400, 100, "What's the visa policy for Japan?")
    tracker.log_tokens_directly(450, 180, "Remember my budget is $1500")
    tracker.log_tokens_directly(550, 220, "Now find hotels within my budget")

    tracker.print_report()
    print()

    # Demo 2: Workshop cost estimation
    print("DEMO 2: Workshop cost estimation")
    print("-" * 50)

    # Estimate for a 25-person workshop
    estimate = estimate_workshop_cost(
        participants=25,
        queries_per_participant=20,
        avg_input_tokens=500,
        avg_output_tokens=200
    )

    print(f"Participants:      {estimate['participants']}")
    print(f"Queries/person:    {estimate['queries_per_participant']}")
    print(f"Total queries:     {estimate['total_queries']:,}")
    print(f"Total input:       {estimate['total_input_tokens']:,} tokens")
    print(f"Total output:      {estimate['total_output_tokens']:,} tokens")
    print(f"Input cost:        ${estimate['input_cost']:.4f}")
    print(f"Output cost:       ${estimate['output_cost']:.4f}")
    print(f"TOTAL COST:        ${estimate['total_cost']:.4f}")
    print(f"Cost/participant:  ${estimate['cost_per_participant']:.4f}")
    print()

    # Export to JSON
    print("DEMO 3: Export to JSON")
    print("-" * 50)
    filepath = tracker.export_json("demo_cost_report.json")
    print(f"Report exported to: {filepath}")
    print()

    print("Done! Use WorkshopCostTracker in your workshop sessions.")
