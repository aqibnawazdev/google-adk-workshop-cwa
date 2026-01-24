# Project State

## Project Reference

See: .planning/PROJECT.md (updated 2026-01-23)

**Core value:** Participants learn to build production-ready AI agents with proper context engineering - combining real-time APIs, knowledge bases, and structured data
**Current focus:** RAG & Knowledge Integration

## Current Position

Phase: 3 of 5 (RAG & Knowledge Integration)
Plan: 1 of 6 in progress (03-02 complete)
Status: In progress - building destination guide corpus
Last activity: 2026-01-24 - Completed 03-02-PLAN.md (5 destination guides created)

Progress: [████████░░] 83%

## Performance Metrics

**Velocity:**
- Total plans completed: 8
- Average duration: 3.5min
- Total execution time: 0.47 hours

**By Phase:**

| Phase | Plans | Total | Avg/Plan |
|-------|-------|-------|----------|
| 1 (Foundation & Setup) | 4 | 12min | 3.0min |
| 2 (Function Calling & Tools) | 3 | 8min | 2.7min |
| 3 (RAG & Knowledge Integration) | 1 | 14min | 14.0min |

**Recent Trend:**
- Last 5 plans: 03-02 (14min), 02-03 (1.5min), 02-02 (2min), 02-01 (4min), 01-04 (2min)
- Trend: Phase 3 content creation slower (expected for detailed guide writing)

*Updated after each plan completion*

## Accumulated Context

### Decisions

Decisions are logged in PROJECT.md Key Decisions table.
Recent decisions affecting current work:

- Roadmap creation: 5-phase progressive workshop structure derived from requirements (setup → function calling → RAG → sessions → support materials)
- Coverage validation: All 37 v1 requirements mapped to phases with no orphans
- Phase 1 execution: Colab-first approach with 48-hour pre-validation pattern established
- Educational structure: TODO-guided hands-on coding with instructor notes and checkpoints
- Reference implementation: Exercise-labeled code sections showing progressive architecture
- 01-01: Colab-only approach eliminates local environment setup (saves 30-40 minutes)
- 01-01: 48-hour pre-validation requirement catches auth/API issues before workshop
- 01-01: Specific troubleshooting per error type (ImportError, CalledProcessError, TimeoutError)
- 01-02: 14-cell notebook structure with timing estimates - supports workshop pacing and instructor facilitation
- 01-02: HTML comment instructor notes - keeps participant view clean while providing facilitation guidance
- 01-02: Embedded troubleshooting in checkpoints - reduces context switching during workshop
- 01-03: Mock data in tool functions - keeps reference simple, focuses on ADK patterns
- 01-03: Exercise labels in code comments - creates clear learning roadmap
- 01-03: Context engineering in instruction - demonstrates proper prompt engineering pattern
- 01-04: Colab as primary path with local as advanced option - reduces setup complexity for 90% of participants
- 01-04: Comprehensive troubleshooting section - addresses auth, dependencies, network, and model access issues
- 01-04: Context engineering explanation in README - makes workshop learning objectives explicit
- 02-01: Mock APIs over real travel APIs - eliminates costs, rate limits, API key management while keeping focus on ADK patterns
- 02-01: Tools vs RAG decision framework upfront - THE key insight participants need before building
- 02-01: Error-in-context pattern demonstrated explicitly - critical for LLM-based error recovery
- 02-01: Debug output in tool functions - makes LLM tool invocation visible to learners
- 02-02: Error-in-context pattern - tools return error dicts instead of raising exceptions for better LLM reasoning
- 02-02: Budget filtering parameters - max_price and max_price_per_night enable budget-aware travel planning
- 02-02: Modular tool architecture - tools.py separate from agent.py for production code organization
- 02-03: Tools vs RAG decision framework documented prominently - enables participants to make correct architectural choices
- 02-03: Parameter tables with complete documentation - type, required status, descriptions prevent usage confusion
- 02-03: Example JSON responses - shows actual tool output structure for transparency
- 02-03: Error-in-context pattern explicitly explained - makes critical pattern visible and teachable
- 03-02: Standardized 10-section destination guide structure - enables consistent RAG retrieval patterns across diverse content
- 03-02: Table format for attractions with booking details - tests layout-aware chunking (Document AI parser must preserve table structure)
- 03-02: Cultural sensitivity emphasized - Dubai Islamic customs, Bangkok monarchy respect, Barcelona Catalan identity
- 03-02: Balanced practical and cultural content - authentic guides serve dual purpose (RAG corpus + educational resource)

### Pending Todos

None yet.

### Blockers/Concerns

**Phase 2 (Function Calling):** ~~Decision needed on mock vs real travel APIs~~ RESOLVED - Using mock APIs for workshop exercises (02-01/02-02). Eliminates costs, rate limits, API key management while keeping ADK patterns authentic.

**Phase 3 (RAG):** Chunking strategy for travel content (destination guides, itineraries) needs testing with sample documents before finalizing exercise.

**Phase 4 (Deployment):** Quota limits for 50 concurrent workshop participants hitting Vertex AI need coordination with Google for quota increases.

**01-01/01-04 Consideration:** Troubleshooting URLs currently show placeholders (`[workshop-repo-url]`, `[instructor contact info]`). Should be replaced when workshop support infrastructure created (Phase 5).

## Session Continuity

Last session: 2026-01-24T07:21:27Z
Stopped at: Completed 03-02-PLAN.md (5 destination guides created)
Resume file: None
