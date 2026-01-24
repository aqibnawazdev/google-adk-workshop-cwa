# Project State

## Project Reference

See: .planning/PROJECT.md (updated 2026-01-23)

**Core value:** Participants learn to build production-ready AI agents with proper context engineering - combining real-time APIs, knowledge bases, and structured data
**Current focus:** PROJECT COMPLETE

## Current Position

Phase: 5 of 5 (Workshop Support Materials) - COMPLETE
Plan: 6 of 6 in current phase - PHASE COMPLETE
Status: All phases complete
Last activity: 2026-01-24 - Completed 05-06-PLAN.md (Solution Audit)

Progress: [##########] 100%

## Performance Metrics

**Velocity:**
- Total plans completed: 24
- Average duration: 3.5min
- Total execution time: 1.43 hours

**By Phase:**

| Phase | Plans | Total | Avg/Plan |
|-------|-------|-------|----------|
| 1 (Foundation & Setup) | 4 | 12min | 3.0min |
| 2 (Function Calling & Tools) | 3 | 8min | 2.7min |
| 3 (RAG & Knowledge Integration) | 6 | 56min | 9.3min |
| 4 (Sessions & Deployment) | 5 | 12min | 2.4min |
| 5 (Workshop Support Materials) | 6 | ~16min | ~2.7min |

**Recent Trend:**
- Last 5 plans: 05-06 (4min), 05-01 (3min), 05-03 (3min), 05-05 (2min), 05-04 (2min)
- Trend: Excellent velocity maintained throughout project

*Updated after each plan completion*

## Accumulated Context

### Decisions

Decisions are logged in PROJECT.md Key Decisions table.
Recent decisions affecting current work:

- Roadmap creation: 5-phase progressive workshop structure derived from requirements (setup -> function calling -> RAG -> sessions -> support materials)
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
- 03-05: Progressive exercise structure (explore -> configure -> create -> test -> integrate) - matches Exercise 2 format, builds complexity incrementally
- 03-05: Introduce constraint before solution (3C explains limitation, 3E provides workaround) - builds problem-solving mindset, not rote coding
- 03-05: Focus TODOs on RAG concepts only - Phase 2 function calling tools provided, reduces cognitive load for new RAG learning
- 03-06: Tools vs RAG Decision Framework in README - enables participants to make correct architectural choices post-workshop
- 03-06: Hybrid agent pattern documented with architecture diagram - explains ADK constraint workaround
- 04-01: State prefix pattern (user:, temp:, app:) for different persistence scopes - core session management concept
- 04-01: State injection syntax {user:key?} with optional marker - prevents errors when key not set
- 04-01: Auto-apply preferences in tool functions - context.state access for preference-aware tools
- 04-02: state_utils.py as reusable module - centralizes preference management for reference implementation
- 04-02: tool_context parameter follows ADK convention - framework-injected context for state access
- 04-02: Helper functions take state dict directly - flexible API for both tool_context.state and session state
- 04-03: Post-workshop deployment focus - impractical for hands-on during 15-minute allocation
- 04-03: Instructor demonstration model - deploy.py enables live demo without participant GCP setup
- 04-03: Cleanup prominence in documentation - cost awareness is critical for participants
- 04-04: AgentEvaluator pattern with eval_dataset_file_path_or_dir for golden dataset testing
- 04-04: Golden datasets with tool_uses in intermediate_data for trajectory validation
- 04-05: Gemini 2.5 Flash pricing ($0.30/$2.50 per 1M tokens) as cost tracking reference
- 04-05: usage_metadata extraction pattern for automatic token counting
- 05-05: Screenshot + email confirmation creates accountability for pre-workshop readiness
- 05-05: 24-hour instructor response window balances promptness with practicality
- 05-05: Tracking table template enables instructor to monitor confirmation status
- 05-02: ASCII flowchart for context engineering decisions - works in all markdown renderers
- 05-02: Quick Reference Card format - printable summary for development use
- 05-02: 5 common mistakes with corrections - prevents architectural errors
- 05-03: Two-tier checklist (MVP Day 1-7, Mature Week 2+) for realistic production timelines
- 05-03: AI-specific focus (evaluation, observability, cost, reliability) not generic software checklist
- 05-03: Each checklist item includes 'why' explanation for informed prioritization
- 05-01: Symptom-first troubleshooting organization - participants find errors by what they see, not by component
- 05-01: 8 error pattern categories covering auth, deps, API, async, network, types, RAG, state
- 05-01: Preserve inline troubleshooting in notebooks - quick help during exercises, link to detailed guide
- 05-06: Three-layer solution format (Implementation + Why This Works + Key Insight) - explains WHY patterns work, not just WHAT

### Pending Todos

None - project complete.

### Blockers/Concerns

All blockers resolved during project execution:

- **Phase 2 (Function Calling):** RESOLVED - Using mock APIs for workshop exercises
- **Phase 3 (RAG):** RESOLVED - 1024 tokens / 256 overlap with Document AI layout parser
- **Phase 4 (Deployment):** RESOLVED - Workshop uses Google AI API (no GCP quota needed)

## Session Continuity

Last session: 2026-01-24T19:36:47Z
Stopped at: PROJECT COMPLETE - All 24 plans executed
Resume file: None

## Project Complete Summary

All 5 phases executed successfully:
- Phase 1: Foundation & Setup (4 plans)
- Phase 2: Function Calling & Tools (3 plans)
- Phase 3: RAG & Knowledge Integration (6 plans)
- Phase 4: Sessions & Deployment (5 plans)
- Phase 5: Workshop Support Materials (6 plans)

Total: 24 plans, ~1.43 hours execution time
