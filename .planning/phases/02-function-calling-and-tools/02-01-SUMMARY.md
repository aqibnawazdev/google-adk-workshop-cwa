---
phase: 02-function-calling-and-tools
plan: 01
subsystem: workshop-materials
tags: [google-adk, function-calling, tools, jupyter, colab, error-handling, budget-filtering]

# Dependency graph
requires:
  - phase: 01-foundation-and-setup
    provides: Colab notebook structure, setup patterns, instructor notes convention
provides:
  - Exercise 2 notebook teaching function calling and tool use in ADK
  - Tools vs RAG decision framework for participants
  - Error-in-context pattern demonstration
  - Mock flight and hotel search functions
  - Budget filtering implementation examples
affects: [03-rag-and-knowledge, 04-sessions-and-state]

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "TODO-guided function implementation exercises"
    - "Error-in-context pattern (return error dicts, not exceptions)"
    - "Tools vs RAG decision framework (real-time vs static data)"
    - "Type hints + docstrings for automatic ADK schema generation"
    - "Debug output in tool functions for learning visibility"

key-files:
  created:
    - workshop-materials/02-tools-functions.ipynb
  modified: []

key-decisions:
  - "Mock APIs over real travel APIs - eliminates costs, rate limits, API key management while keeping focus on ADK patterns"
  - "Tools vs RAG decision framework upfront - THE key insight participants need before building"
  - "Error-in-context pattern demonstrated explicitly with side-by-side comparison - critical for LLM-based error recovery"
  - "Budget filtering with optional max_price parameter - shows agent reasoning and parameter usage"
  - "Debug output in tool functions - makes LLM tool invocation visible to learners"

patterns-established:
  - "Exercise structure: concept intro → TODO implementation → checkpoint → next concept"
  - "Error handling: return {status: error, error_message, example} not raise exceptions"
  - "Tool docstrings: include parameter examples (e.g., 'SFO', '2026-03-15') for LLM understanding"
  - "Agent instruction: explicit tool usage guidelines, budget awareness, error recovery"

# Metrics
duration: 4min
completed: 2026-01-24
---

# Phase 02 Plan 01: Function Calling & Tools Summary

**Complete Exercise 2 notebook with TODO-guided function calling exercises, tools vs RAG decision framework, error-in-context pattern, and budget filtering - 33 cells teaching participants to build agents with real-time data access**

## Performance

- **Duration:** 4 minutes
- **Started:** 2026-01-24T05:13:00Z
- **Completed:** 2026-01-24T05:17:11Z
- **Tasks:** 1
- **Files modified:** 1

## Accomplishments

- Created 02-tools-functions.ipynb with 33 cells following 01-hello-agent.ipynb patterns
- Tools vs RAG decision framework prominently explained upfront (THE key concept)
- Error-in-context pattern demonstrated with side-by-side comparison (exceptions vs error dicts)
- Mock search_flights and search_hotels functions with realistic data structures
- Budget filtering exercises with max_price parameter and agent reasoning
- Complete solutions provided in collapsible cells

## Task Commits

Each task was committed atomically:

1. **Task 1: Create 02-tools-functions.ipynb with exercise structure** - `3fbde23` (feat)

**Plan metadata:** (pending - to be committed with STATE.md update)

## Files Created/Modified

- `workshop-materials/02-tools-functions.ipynb` - Exercise 2 notebook teaching function calling, error handling, budget filtering with TODO-guided exercises (33 cells, ~30min workshop time)

## Decisions Made

**Mock API approach:** Used mock flight/hotel data instead of real travel APIs (Amadeus, Skyscanner). This eliminates workshop complexity (API keys, rate limits, costs, variable responses) while demonstrating ADK patterns authentically. Mock data structures match real API patterns for post-workshop transition.

**Tools vs RAG decision framework upfront:** Dedicated the first concept section to explaining when to use tools vs RAG, with clear decision matrix and travel-specific examples. This is THE critical distinction participants need before implementing - prevents confusion in Phase 3 when RAG is introduced.

**Error-in-context pattern emphasized:** Demonstrated explicitly with side-by-side comparison showing why exceptions fail (LLM can't see them) vs error dicts succeed (LLM can read and respond). This pattern is where most beginner function calling implementations fail - made it impossible to miss.

**Debug output for learning:** Added `print()` statements in tool functions showing when they're called with what parameters. Makes LLM tool invocation visible to learners, preventing "black box" misunderstanding.

**Budget filtering as parameter:** Added optional `max_price` parameter to demonstrate both parameterization and agent reasoning about budget constraints mentioned in conversation.

## Deviations from Plan

None - plan executed exactly as written.

## Issues Encountered

None - notebook creation was straightforward with clear guidance from research and Exercise 1 patterns.

## User Setup Required

None - no external service configuration required. Notebook runs in Colab with google-adk pip install.

## Next Phase Readiness

**Ready for Phase 2 remaining plans:**
- Exercise 2 complete with function calling foundation
- Participants understand tools vs RAG distinction
- Error-in-context pattern established
- Mock APIs provide consistent, reproducible workshop experience

**For Phase 3 (RAG):**
- Tools vs RAG decision framework already taught - can reference back
- Function calling patterns established - RAG will feel like natural extension
- Error handling patterns apply to RAG as well

**No blockers.** Phase 2 Plan 1 complete, ready for subsequent plans in phase (if any) or Phase 3.

---
*Phase: 02-function-calling-and-tools*
*Completed: 2026-01-24*
