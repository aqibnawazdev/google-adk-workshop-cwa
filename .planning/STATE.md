# Project State

## Project Reference

See: .planning/PROJECT.md (updated 2026-01-23)

**Core value:** Participants learn to build production-ready AI agents with proper context engineering - combining real-time APIs, knowledge bases, and structured data
**Current focus:** RAG & Knowledge Integration

## Current Position

Phase: 3 of 5 (RAG & Knowledge Integration)
Plan: 2 of 6 (03-01, 03-02 complete)
Status: In progress - destination guide corpus complete (10 guides total), ALL notebook blocking issues resolved (asyncio + Vertex AI init)
Last activity: 2026-01-24 - Fixed asyncio conflicts + Vertex AI initialization across all notebooks (00, 01, 02) - workshops now fully functional

Progress: [████████░░] 85%

## Performance Metrics

**Velocity:**
- Total plans completed: 9
- Average duration: 3.3min
- Total execution time: 0.50 hours

**By Phase:**

| Phase | Plans | Total | Avg/Plan |
|-------|-------|-------|----------|
| 1 (Foundation & Setup) | 4 | 12min | 3.0min |
| 2 (Function Calling & Tools) | 3 | 8min | 2.7min |
| 3 (RAG & Knowledge Integration) | 2 | 30min | 15.0min |

**Recent Trend:**
- Last 5 plans: 03-01 (16min), 03-02 (14min), 02-03 (1.5min), 02-02 (2min), 02-01 (4min)
- Trend: Phase 3 content creation slower (expected for detailed guide writing), excellent quality output

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
- 03-01: Table format for Top Attractions section - enables layout-aware chunking validation (Document AI parser must preserve table structure)
- 03-01: 300-600 line guides balance comprehensive content with manageable chunk counts (15-25 chunks per guide at 1024 tokens)
- 03-01: Diverse destinations (Tokyo, Paris, NYC, Singapore, London) test multicultural RAG patterns across Asia, Europe, North America
- 03-01: Standardized 10-section structure ensures consistent retrieval quality ("Visa Requirements" returns same format from any guide)
- 03-02: Standardized 10-section destination guide structure - enables consistent RAG retrieval patterns across diverse content
- 03-02: Table format for attractions with booking details - tests layout-aware chunking (Document AI parser must preserve table structure)
- 03-02: Cultural sensitivity emphasized - Dubai Islamic customs, Bangkok monarchy respect, Barcelona Catalan identity
- 03-02: Balanced practical and cultural content - authentic guides serve dual purpose (RAG corpus + educational resource)
- 00-setup-verification FIX: Top-level await instead of asyncio.run() - Colab/Jupyter has existing event loop, asyncio.run() causes nested loop conflict
- 01-hello-agent FIX: Top-level await in Cells 7, 11 - same asyncio.run() issue blocked Exercise 1
- 02-tools-functions FIX: Top-level await in Cells 21, 27 - same asyncio.run() issue blocked Exercise 2
- ALL NOTEBOOKS FIX: Added vertexai.init() before Agent creation - ADK defaults to Google AI API without it, requires api_key parameter instead of using Vertex AI with GCP auth

### Pending Todos

None yet.

### Blockers/Concerns

**Phase 2 (Function Calling):** ~~Decision needed on mock vs real travel APIs~~ RESOLVED - Using mock APIs for workshop exercises (02-01/02-02). Eliminates costs, rate limits, API key management while keeping ADK patterns authentic.

**Phase 3 (RAG):** Chunking strategy for travel content (destination guides, itineraries) needs testing with sample documents before finalizing exercise.

**Phase 4 (Deployment):** Quota limits for 50 concurrent workshop participants hitting Vertex AI need coordination with Google for quota increases.

**01-01/01-04 Consideration:** Troubleshooting URLs currently show placeholders (`[workshop-repo-url]`, `[instructor contact info]`). Should be replaced when workshop support infrastructure created (Phase 5).

## Session Continuity

Last session: 2026-01-24T07:23:19Z
Stopped at: Completed 03-01-PLAN.md (Tokyo, Paris, New York, Singapore, London guides)
Resume file: None
