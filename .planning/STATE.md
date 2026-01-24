# Project State

## Project Reference

See: .planning/PROJECT.md (updated 2026-01-23)

**Core value:** Participants learn to build production-ready AI agents with proper context engineering - combining real-time APIs, knowledge bases, and structured data
**Current focus:** Sessions & Deployment

## Current Position

Phase: 4 of 5 (Sessions & Deployment)
Plan: 0 of TBD (phase planning needed)
Status: Phase 3 complete, ready for Phase 4 planning
Last activity: 2026-01-24 - Completed Phase 3 (RAG & Knowledge Integration) with 6 plans, verified all must-haves

Progress: [██████░░░░] 60%

## Performance Metrics

**Velocity:**
- Total plans completed: 13
- Average duration: 4.5min
- Total execution time: 0.97 hours

**By Phase:**

| Phase | Plans | Total | Avg/Plan |
|-------|-------|-------|----------|
| 1 (Foundation & Setup) | 4 | 12min | 3.0min |
| 2 (Function Calling & Tools) | 3 | 8min | 2.7min |
| 3 (RAG & Knowledge Integration) | 6 | 56min | 9.3min |

**Recent Trend:**
- Last 5 plans: 03-06 (5min), 03-05 (7min), 03-03 (4min), 03-04 (5min), 03-01 (16min)
- Trend: Excellent velocity - documentation plans (03-06: 5min) and notebooks (03-05: 7min) efficient, Phase 3 complete

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
- ASYNC FIX: Top-level await instead of asyncio.run() - Colab/Jupyter has existing event loop, asyncio.run() causes nested loop conflict
- **AUTH DECISION: Switched from Vertex AI to Google AI API key approach** - Simpler participant experience (just get API key from aistudio.google.com/apikey), no GCP project config needed, eliminates vertexai.init() complexity. Vertex AI remains available for deployment topics if covered later.
- **ADK API PATTERN: Use Runner + InMemorySessionService pattern (not agent.generate_content)** - Based on official docs and ADK_Learning_tools.ipynb example. The correct pattern is: genai.configure(api_key), Runner with InMemorySessionService, runner.run_async() with async for loop, event.is_final_response() to extract response. agent.generate_content() does not exist in ADK.
- 03-03: Markdown2 + Weasyprint for PDF conversion - preserves tables, professional formatting, CSS control for Document AI parser input
- 03-03: Document AI layout parser enabled (use_advanced_pdf_parsing) - preserves table/list structure in chunks (Pattern 2 from research)
- 03-03: 1024 token chunk size / 256 overlap - research-recommended defaults, resolves "chunking strategy" blocker from Phase 3 concerns
- 03-03: 48-hour pre-workshop setup timeline - allows indexing completion and validation before workshop (Pattern 1 from research)
- 03-04: Sequential agent coordination pattern - ADK constraint prevents mixing VertexAiRagRetrieval with function tools, workaround uses separate specialized agents with routing logic
- 03-04: Explicit DO/DO NOT tool descriptions - prevents LLM from calling RAG for real-time queries or tools for static knowledge (Pattern 3 from research)
- 03-04: Graceful degradation for missing RAG_CORPUS_ID - all modules work before Exercise 3, error messages guide setup
- 03-05: Progressive exercise structure (explore → configure → create → test → integrate) - matches Exercise 2 format, builds complexity incrementally
- 03-05: Introduce constraint before solution (3C explains limitation, 3E provides workaround) - builds problem-solving mindset, not rote coding
- 03-05: Focus TODOs on RAG concepts only - Phase 2 function calling tools provided, reduces cognitive load for new RAG learning
- 03-06: Tools vs RAG Decision Framework in README - enables participants to make correct architectural choices post-workshop
- 03-06: Hybrid agent pattern documented with architecture diagram - explains ADK constraint workaround

### Pending Todos

None yet.

### Blockers/Concerns

**Phase 2 (Function Calling):** ~~Decision needed on mock vs real travel APIs~~ RESOLVED - Using mock APIs for workshop exercises (02-01/02-02). Eliminates costs, rate limits, API key management while keeping ADK patterns authentic.

**Phase 3 (RAG):** ~~Chunking strategy for travel content needs testing~~ RESOLVED - 1024 tokens / 256 overlap with Document AI layout parser enabled (03-03). Tables preserved in chunks, 13-query validation suite ready for pre-workshop testing.

**Phase 4 (Deployment):** ~~Quota limits for 50 concurrent workshop participants hitting Vertex AI~~ REDUCED CONCERN - Workshop exercises now use Google AI API (no GCP quota needed). Only deployment topics (if covered) would use Vertex AI.

**01-01/01-04 Consideration:** Troubleshooting URLs currently show placeholders (`[workshop-repo-url]`, `[instructor contact info]`). Should be replaced when workshop support infrastructure created (Phase 5).

## Session Continuity

Last session: 2026-01-24T10:45:00Z
Stopped at: Completed Phase 3 (RAG & Knowledge Integration) - all 6 plans executed, verified
Resume file: None
