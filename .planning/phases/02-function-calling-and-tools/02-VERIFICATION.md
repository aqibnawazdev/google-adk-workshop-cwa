---
phase: 02-function-calling-and-tools
verified: 2026-01-24T12:00:00Z
status: passed
score: 5/5 must-haves verified
re_verification: false
---

# Phase 2: Function Calling & Tools Verification Report

**Phase Goal:** Agent can search real-time booking data using function calling for flights and hotels

**Verified:** 2026-01-24T12:00:00Z

**Status:** PASSED

**Re-verification:** No — initial verification

## Goal Achievement

### Observable Truths

| # | Truth | Status | Evidence |
|---|-------|--------|----------|
| 1 | Agent can search flights by destination, dates, and passenger count returning available options | ✓ VERIFIED | tools.py implements search_flights() with origin, destination, departure_date, passengers parameters. Returns flights array with airline, price, times. Tested successfully. |
| 2 | Agent can search hotels by location, check-in/out dates, and guest count returning available properties | ✓ VERIFIED | tools.py implements search_hotels() with location, check_in, check_out, guests parameters. Returns hotels array with name, stars, price_per_night. Tested successfully. |
| 3 | Agent handles API errors gracefully with helpful error messages when searches fail | ✓ VERIFIED | Error-in-context pattern implemented. Returns {status: "error", error_message: ...} dicts instead of raising exceptions. Validated for invalid dates, past dates, budget constraints, unknown routes/locations. |
| 4 | Agent filters search results by user's stated budget constraints | ✓ VERIFIED | max_price parameter in search_flights filters results. max_price_per_night in search_hotels filters results. Budget filtering tested and working - returns error with helpful suggestions when budget too low. |
| 5 | Workshop materials explain when to use function calling vs RAG vs session state with decision framework | ✓ VERIFIED | 02-tools-functions.ipynb has dedicated "Tools vs RAG: The Decision Framework" section. README.md has decision table. Both use "key question" pattern. Decision framework prominent in both materials. |

**Score:** 5/5 truths verified

### Required Artifacts

| Artifact | Expected | Status | Details |
|----------|----------|--------|---------|
| `workshop-materials/02-tools-functions.ipynb` | Exercise 2 notebook with function calling exercises | ✓ VERIFIED | Exists, 33 cells, 1128 lines. Contains search_flights/search_hotels TODOs, decision framework, error-in-context pattern, budget filtering exercises. |
| `workshop-materials/reference-implementation/tools.py` | Complete tool implementations | ✓ VERIFIED | Exists, 387 lines. Implements search_flights and search_hotels with full validation, error handling, budget filtering, mock data for 3 flight routes and 3 hotel cities. |
| `workshop-materials/reference-implementation/agent.py` | Agent with tools integrated | ✓ VERIFIED | Exists, 151 lines. Imports tools from tools.py, agent configured with tools=[search_flights, search_hotels], instruction includes budget awareness section. |
| `workshop-materials/reference-implementation/README.md` | Documentation with decision framework | ✓ VERIFIED | Exists, 182 lines. Contains "Tools vs RAG: Decision Framework" section with table, parameter documentation for both tools, error handling pattern explanation. |

### Key Link Verification

| From | To | Via | Status | Details |
|------|----|----|--------|---------|
| agent.py | tools.py | import statement | ✓ WIRED | Line 13: `from tools import search_flights, search_hotels` |
| Agent instance | search_flights | tools parameter | ✓ WIRED | Line 121-123: tools=[search_flights, search_hotels] passed to Agent() |
| Agent instance | search_hotels | tools parameter | ✓ WIRED | Same as above - both tools registered |
| Agent instruction | budget awareness | instruction text | ✓ WIRED | Lines 106-110: BUDGET AWARENESS section with max_price guidance |
| search_flights | budget filtering | max_price parameter | ✓ WIRED | Line 183: max_price parameter. Lines 245-256: budget filtering logic with error handling |
| search_hotels | budget filtering | max_price_per_night parameter | ✓ WIRED | Line 280: max_price_per_night parameter. Lines 354-365: budget filtering logic |
| Notebook | decision framework | markdown cells | ✓ WIRED | Cell 1: "Tools vs RAG: The Decision Framework" section with decision table and key question |
| Notebook | TODO exercises | code cells | ✓ WIRED | Cells 5, 10, 14, 19, 25: TODO-guided exercises for implementing functions |

### Requirements Coverage

| Requirement | Status | Supporting Evidence |
|-------------|--------|---------------------|
| WORK-03: Exercise 2 (function calling) | ✓ SATISFIED | 02-tools-functions.ipynb exists with 33 cells, complete TODO-guided exercises |
| AGENT-01: Agent can search flights | ✓ SATISFIED | search_flights() implemented and tested |
| AGENT-02: Agent can search hotels | ✓ SATISFIED | search_hotels() implemented and tested |
| AGENT-06: Graceful error handling | ✓ SATISFIED | Error-in-context pattern implemented, returns error dicts with helpful messages |
| AGENT-08: Budget filtering | ✓ SATISFIED | max_price and max_price_per_night parameters implemented and working |
| INFRA-01: Mock flight API | ✓ SATISFIED | MOCK_FLIGHTS dict with 3 routes (SFO->NRT, LAX->CDG, JFK->LHR) |
| INFRA-02: Mock hotel API | ✓ SATISFIED | MOCK_HOTELS dict with 3 cities (Tokyo, Paris, London) |
| CONTEXT-01: Tools vs RAG framework | ✓ SATISFIED | Decision framework in both notebook and README with decision table |
| CONTEXT-02: Real-time data pattern | ✓ SATISFIED | Function calling demonstrated for flights/hotels as real-time data |
| CONTEXT-06: Error-in-context pattern | ✓ SATISFIED | Explicitly taught in notebook cell 13, implemented in all tools |
| CONTEXT-07: Cache-friendly patterns | ✓ SATISFIED | Deterministic mock data, no random values, same inputs yield same outputs |

### Anti-Patterns Found

| File | Line | Pattern | Severity | Impact |
|------|------|---------|----------|--------|
| None | - | - | - | No anti-patterns detected |

**Anti-pattern scan results:**
- No TODO/FIXME comments in production code (only in exercise TODOs - intentional)
- No placeholder content in implementations
- No empty returns or stub patterns
- No console.log-only implementations
- Error handling uses proper error-in-context pattern throughout

### Functional Testing Results

All core functionality verified through testing:

**Test 1: Valid flight search**
```
Input: search_flights('SFO', 'NRT', '2026-03-15', passengers=2)
Result: ✓ Success - 3 flights returned
```

**Test 2: Budget filtering**
```
Input: search_flights('SFO', 'NRT', '2026-03-15', max_price=800)
Result: ✓ Error handling works - "No flights found under $800. Lowest price: $850."
```

**Test 3: Invalid date error handling**
```
Input: search_flights('SFO', 'NRT', 'March 15')
Result: ✓ Error caught - "Invalid date format: 'March 15'. Use YYYY-MM-DD format."
```

**Test 4: Hotel budget filtering**
```
Input: search_hotels('Tokyo', '2026-03-15', '2026-03-20', max_price_per_night=200)
Result: ✓ Success - 1 hotel returned (filtered from 4)
```

### Quality Metrics

**Code Quality:**
- Type hints: ✓ Present on all function parameters and returns
- Docstrings: ✓ Google-style docstrings with Args and Returns sections
- Error handling: ✓ Comprehensive validation with helpful error messages
- Mock data: ✓ Realistic and deterministic
- Code organization: ✓ Modular (tools.py separate from agent.py)

**Workshop Materials Quality:**
- Notebook cell count: 33 cells (exceeds 18-20 minimum)
- Decision framework: ✓ Prominent and clear
- TODO exercises: ✓ Progressive and guided
- Solutions: ✓ Provided in collapsible cell
- Checkpoints: ✓ After each exercise

**Documentation Quality:**
- Decision framework table: ✓ Clear and actionable
- Parameter tables: ✓ Complete with types and descriptions
- Example responses: ✓ Realistic JSON examples
- Error pattern: ✓ Explicitly documented

## Overall Assessment

**All Phase 2 success criteria VERIFIED:**

1. ✓ Agent can search flights by destination, dates, and passenger count returning available options
2. ✓ Agent can search hotels by location, check-in/out dates, and guest count returning available properties
3. ✓ Agent handles API errors gracefully with helpful error messages when searches fail
4. ✓ Agent filters search results by user's stated budget constraints
5. ✓ Workshop materials explain when to use function calling vs RAG vs session state with decision framework

**Phase Goal ACHIEVED:** Agent can search real-time booking data using function calling for flights and hotels

**Phase Status:** COMPLETE and ready for Phase 3 (RAG & Knowledge Integration)

## Strengths

1. **Error-in-context pattern properly implemented** - This is the critical pattern beginners miss. It's demonstrated explicitly with side-by-side comparison in the notebook and implemented correctly throughout.

2. **Decision framework prominent** - "Tools vs RAG" is positioned upfront in both notebook and README, teaching the KEY conceptual distinction before implementation.

3. **Budget filtering working** - Both tools support budget constraints with helpful error messages when nothing fits budget.

4. **Mock data quality** - Realistic data structures matching real travel APIs, deterministic for reproducible workshop experience.

5. **Comprehensive validation** - Date format, date order, past dates, passenger counts, unknown routes all validated with helpful error messages.

6. **Modular architecture** - tools.py separate from agent.py demonstrates production patterns.

7. **Type hints + docstrings** - Proper ADK schema generation setup with examples in docstrings.

## No Gaps Found

All required functionality is present, substantive, and wired correctly. No blockers to proceeding with Phase 3.

---

_Verified: 2026-01-24T12:00:00Z_
_Verifier: Claude (gsd-verifier)_
