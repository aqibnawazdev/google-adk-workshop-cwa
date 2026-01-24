---
phase: 02-function-calling-and-tools
plan: 02
subsystem: tools
tags: [python, google-adk, function-calling, validation, error-handling]

# Dependency graph
requires:
  - phase: 01-foundation-and-setup
    provides: Reference implementation structure and workshop materials foundation
provides:
  - Complete tool implementations with validation and error handling
  - Budget filtering capability for both flights and hotels
  - Error-in-context pattern demonstration
  - Modular tool architecture (tools.py separate from agent.py)
affects: [02-function-calling-and-tools, workshop-exercises]

# Tech tracking
tech-stack:
  added: [typing.Optional]
  patterns: [error-in-context, budget-filtering, modular-tools, google-style-docstrings]

key-files:
  created: [workshop-materials/reference-implementation/tools.py]
  modified: [workshop-materials/reference-implementation/agent.py]

key-decisions:
  - "Error-in-context pattern: tools return error dicts with status field instead of raising exceptions"
  - "Budget filtering: max_price and max_price_per_night as optional parameters for user budget awareness"
  - "Modular architecture: tools.py separate from agent.py for better code organization and reusability"

patterns-established:
  - "Error-in-context pattern: All tool functions return dict with 'status' field ('success' or 'error') and descriptive error_message when validation fails"
  - "Budget filtering pattern: Optional max_price parameters filter results and provide helpful suggestions when budget too low"
  - "Debug output pattern: Print statements show when tools are called for learning visibility"

# Metrics
duration: 2min
completed: 2026-01-24
---

# Phase 02 Plan 02: Complete Tool Implementation Summary

**Production-quality search_flights and search_hotels with full validation, error handling, budget filtering, and modular architecture**

## Performance

- **Duration:** 2 min 20 sec
- **Started:** 2026-01-24T06:39:45Z
- **Completed:** 2026-01-24T06:42:05Z
- **Tasks:** 2
- **Files modified:** 2

## Accomplishments
- Created tools.py with complete search_flights and search_hotels implementations (387 lines)
- Implemented comprehensive input validation with error-in-context pattern
- Added budget filtering via max_price and max_price_per_night optional parameters
- Refactored agent.py to import tools from separate module
- Added BUDGET AWARENESS section to agent instruction

## Task Commits

Each task was committed atomically:

1. **Task 1: Create tools.py with complete implementations** - `b786563` (feat)
2. **Task 2: Update agent.py to import from tools.py** - `0986342` (refactor)

## Files Created/Modified
- `workshop-materials/reference-implementation/tools.py` - Complete tool implementations with validation, error handling, budget filtering, and realistic mock data
- `workshop-materials/reference-implementation/agent.py` - Updated to import tools from tools.py, removed inline definitions, added budget awareness to instruction

## Decisions Made

**1. Error-in-context pattern for tool functions**
- Tools return dicts with "status": "success" or "status": "error" instead of raising exceptions
- Error responses include descriptive error_message and helpful suggestions
- This pattern keeps errors in LLM context for better agent reasoning

**2. Budget filtering as optional parameters**
- search_flights accepts max_price parameter
- search_hotels accepts max_price_per_night parameter
- When budget filters out all results, tools suggest lowest available price
- Enables budget-aware travel planning

**3. Modular tool architecture**
- Separated tools into tools.py instead of inline definitions in agent.py
- Improves code organization and reusability
- Demonstrates production patterns for workshop participants

## Deviations from Plan

None - plan executed exactly as written.

## Issues Encountered

None - all tasks completed without issues. Verification tests confirmed:
- Date format validation works correctly
- Past date validation catches invalid dates
- Budget filtering correctly filters results
- Error-in-context pattern returns proper error dicts
- Mock data covers 3 flight routes (SFO->NRT, LAX->CDG, JFK->LHR) and 3 hotel locations (Tokyo, Paris, London)

## Next Phase Readiness

Ready for Exercise 2 implementation. Reference implementation now provides:
- Complete tool functions participants can examine
- Error-in-context pattern to teach
- Budget filtering capability to demonstrate
- Modular architecture to follow

**Next:** Create hands-on exercise notebook for participants to build these tools step-by-step (plan 02-03).

---
*Phase: 02-function-calling-and-tools*
*Completed: 2026-01-24*
