# Agent Evaluation Tests

This directory contains reference tests for the travel booking assistant using ADK's AgentEvaluator framework.

## Overview

AgentEvaluator validates agent behavior by:
1. Running conversations from golden datasets
2. Comparing actual tool calls to expected calls
3. Evaluating response quality with LLM grading
4. Calculating trajectory and response scores

## Test Structure

```
tests/
├── README.md                       # This file
├── test_travel_agent.py            # pytest test file
├── conftest.py                     # pytest configuration
└── eval_datasets/                  # Golden test data
    ├── flight_search.test.json     # Flight search scenarios
    └── preference_memory.test.json # Preference persistence scenarios
```

## Running Tests

```bash
# Install test dependencies
pip install pytest pytest-asyncio

# Run all tests
pytest tests/ -v

# Run specific test
pytest tests/test_travel_agent.py::test_flight_search -v

# Run with verbose output
pytest tests/ -v --tb=short
```

## Writing Golden Datasets

Each `.test.json` file contains evaluation cases:

```json
{
  "eval_set_id": "unique_id",
  "name": "Human-readable name",
  "eval_cases": [
    {
      "eval_id": "case_1",
      "session_input": {
        "app_name": "agent_name",
        "user_id": "test_user"
      },
      "conversation": [
        {
          "user_content": {
            "role": "user",
            "parts": [{"text": "User message"}]
          },
          "intermediate_data": {
            "tool_uses": [
              {
                "name": "expected_tool",
                "args": {"arg1": "value1"}
              }
            ]
          },
          "final_response": {
            "role": "model",
            "parts": [{"text": "Expected response pattern"}]
          }
        }
      ]
    }
  ]
}
```

## Evaluation Metrics

AgentEvaluator calculates:

| Metric | Description |
|--------|-------------|
| `tool_trajectory_avg_score` | How well actual tool calls match expected |
| `response_match_score` | Semantic similarity of responses |
| `overall_score` | Combined evaluation score |

Default thresholds (configurable):
- `tool_trajectory_avg_score >= 0.8`
- `response_match_score >= 0.7`

## Tips

1. **Tool args don't need exact match**: AgentEvaluator allows variations in argument values
2. **Response matching is semantic**: Exact text match not required
3. **Multiple turns supported**: Test multi-turn conversations
4. **Error cases matter**: Include tests for invalid inputs

## Resources

- [ADK Evaluation Docs](https://google.github.io/adk-docs/evaluate/)
- [AgentEvaluator Codelab](https://codelabs.developers.google.com/adk-eval/instructions)
