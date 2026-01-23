# Project Research Summary

**Project:** Google ADK Workshop - Travel Booking Agent with Context Engineering
**Domain:** Technical Workshop / Educational Content
**Researched:** 2026-01-23
**Confidence:** HIGH

## Executive Summary

This project is a 90-minute hands-on workshop teaching Python developers how to build production-quality AI agents using Google's Agent Development Kit (ADK). The workshop uses a travel booking agent as the teaching vehicle, progressively introducing core concepts: function calling for real-time data, RAG for knowledge retrieval, and session management for conversation state. The recommended approach follows Google's official ADK codelabs structure: deliver via Google Colab notebooks to eliminate installation friction, use incremental exercises with clear checkpoints, and culminate in a real deployment to Vertex AI Agent Engine.

The critical success factor is balancing depth with the 90-minute constraint. Research shows that 65% of agentic AI pilots fail to reach production not due to technical limitations, but because developers skip production concerns like error handling, rate limiting, and context management. This workshop must avoid "demo-driven development" by explicitly showing at least one production pattern per module while maintaining beginner accessibility. The architecture follows ADK best practices: single agent with specialized tools (not over-engineered multi-agent), Vertex AI RAG Engine for destination knowledge (not custom vector DB), and proper session state management to prevent context poisoning.

Key risk: Time management. Workshops commonly spend 40+ minutes on setup, leaving critical content rushed. Mitigation: pre-workshop environment validation 48 hours ahead with confirmation required, strict time-boxing per section, and backup shared Colab notebooks if local setup fails. The workshop structure must be resilient to the 3x skill variance typical in beginner audiences, providing catch-up checkpoints via git branches and stretch exercises for advanced participants.

## Key Findings

### Recommended Stack

The stack is optimized for zero-installation workshop delivery while teaching production-ready patterns. Google Colab eliminates local environment setup (saving 15-20 minutes), while the actual agent implementation uses ADK 1.23.0 (latest stable as of Jan 2026), Python 3.11/3.12, and Gemini 2.5 Flash for stability over bleeding-edge Gemini 3.0.

**Core technologies:**
- **Google ADK 1.23.0**: Production-ready v1.0+ framework with code-first approach that makes agent development feel like software development, not prompt engineering
- **Python 3.11/3.12**: Required by ADK (>=3.10), chosen over 3.9 which Google Cloud SDK deprecates Jan 27, 2026; offers 10-60% performance gains
- **Gemini 2.5 Flash**: Stable model for workshop (vs. Gemini 2.0 Flash deprecated, shutdown March 31, 2026; Gemini 3.0 too new)
- **Vertex AI RAG Engine**: Managed RAG service eliminates custom vector DB setup, integrates natively with ADK via VertexAiRagRetrieval tool
- **Google Colab**: Zero-install notebook environment for participants, official ADK tutorials use Colab, free tier with generous compute
- **Vertex AI Agent Engine**: One-command deployment (`adk deploy agent_engine`) with free tier (50 hours vCPU + 100 hours RAM monthly), appropriate for workshop scope

**Critical version compatibility:**
- Python 3.9 or earlier: Avoid (Google Cloud SDK deprecating support)
- google-adk < 1.0: Avoid (pre-production versions)
- Gemini 2.0 Flash: Avoid (deprecated, shutdown March 31, 2026)

### Expected Features

The feature set balances workshop time constraints against demonstrating real-world capabilities. Core value proposition is teaching context engineering patterns: when to use RAG vs. tools vs. structured data, and how to manage context as a scarce resource.

**Must have (table stakes):**
- **Clear setup/installation guide**: Exact steps for GCP project setup, ADK installation, API key config — beginners can't learn if base environment doesn't work
- **Working starter code**: Pre-built scaffolding with comments, tested on clean environment before workshop
- **Step-by-step tutorial with checkpoints**: Each checkpoint = working code, git branches for stragglers to catch up
- **Natural language agent queries**: Core AI capability using Gemini's built-in NLU
- **Function/tool calling**: 2-3 simple tools (search_flights, get_hotel_prices, check_weather) demonstrating real-world capability
- **RAG knowledge base**: Small travel corpus (visa requirements, travel tips, airport codes) showing how to ground agents in custom data
- **Session/conversation memory**: Track preferences across turns ("I prefer window seats" → remember for booking)
- **Troubleshooting guide**: Top 5 errors from dry runs (auth issues, missing dependencies, API limits)

**Should have (competitive differentiators):**
- **Live deployment to Vertex AI**: Most tutorials stop at localhost — this shows real cloud deployment in final 15 minutes
- **Context engineering patterns**: Explicitly teach the "why" not just "how" — when to use RAG vs. tools vs. structured data
- **Real-world API integration**: Use actual travel APIs (free tier: Amadeus, Skyscanner) vs. toy mocks for production skills
- **Interactive debugging session**: Intentionally trigger common issues, debug together — builds participant confidence
- **Cost transparency**: Show GCP billing dashboard, explain free tier limits, estimate workshop costs (~$0.50/participant)
- **Modular architecture**: Separate concerns (tools/, knowledge/, agent/) — teach professional structure from day 1

**Defer (anti-features for 90-min beginner workshop):**
- **Multi-agent orchestration**: Creates complexity explosion, needs 4+ hours to teach properly — use single agent with multiple tools instead
- **Custom fine-tuned models**: Requires ML expertise, orthogonal to context engineering concepts
- **Real payment processing**: PCI compliance nightmares, liability issues — use mock booking confirmation instead
- **Complex UI/frontend**: Insufficient time for React + agent code — terminal interface or simple Streamlit app only
- **Advanced RAG (GraphRAG)**: Requires vector DB setup, embedding concepts, graph theory — use simple semantic search instead

### Architecture Approach

The architecture follows ADK's progressive complexity pattern: each exercise builds incrementally on previous concepts, isolating one new feature per exercise. This accommodates different learning paces and reduces cognitive load while requiring careful dependency management between exercises.

**Major components:**

1. **Workshop Materials Layer** — Tutorial docs (Markdown), starter code (partial implementations with TODOs), solutions (complete with explanations), reference implementation (production-grade example)

2. **Agent Application Layer** — Root agent (orchestration + conversation management), Tools Layer (Function calling for real-time booking data), Knowledge Layer (RAG for destination information), Session State (conversation persistence)

3. **Infrastructure Layer** — Session Service (VertexAiSessionService for state persistence), Vertex RAG Engine (managed semantic search), Gemini API (LLM inference)

**Key patterns:**
- **Progressive Complexity**: Exercise 1 (basic agent), Exercise 2 (+function calling), Exercise 3 (+RAG), Exercise 4 (+sessions)
- **Function Tools for Real-Time Data**: Wrap external APIs for current/dynamic data (booking availability, pricing)
- **RAG for Static Knowledge**: Use Vertex AI RAG Engine for factual knowledge that doesn't change frequently (destination guides, travel tips)
- **Session State for Conversation Context**: Persist conversation history and user preferences across turns, prevent "re-ask" syndrome
- **Avoid Multi-Agent Over-Engineering**: Single LlmAgent with multiple tools for straightforward workflows, reserve multi-agent for genuinely complex coordination

### Critical Pitfalls

Research identified 8 critical pitfalls with high impact on workshop success:

1. **Treating Agents as "Magic" Without Understanding Fundamentals** — Participants copy code without understanding how function calling or RAG works, leave unable to debug. Prevention: Dedicate 10-15 min to core concepts before coding, include "what's happening under the hood" slide for each demo.

2. **"Demo-Driven Development" Instead of Production Readiness** — Examples work in demos but fail in real environments due to missing error handling, rate limiting, monitoring. Prevention: Show at least one production concern per module, include "Production Checklist" slide.

3. **Over-Scoped "God Agents" That Do Everything** — Monolithic agents handling too many unrelated tasks struggle with context switching and are impossible to debug. Prevention: Teach Coordinator Pattern explicitly, show "bad example" of over-scoped agent.

4. **Wrong Embeddings and Context-Destroying Chunking** — Default chunking (split on newlines) destroys semantic meaning, returns irrelevant RAG results. Prevention: Show side-by-side bad vs. good chunking comparison, explain embedding model tradeoffs.

5. **Cache-Breaking Patterns That Kill Performance** — Adding timestamps to prompts, modifying context history breaks Gemini's prompt caching, causing 100x slower responses and 3-5x higher costs. Prevention: Explain prompt caching with performance comparison, provide cache-friendly patterns.

6. **Hiding Errors from Context (Missing "Wrong Turns")** — Hiding error messages from the model prevents learning from mistakes, agents retry same failing approach infinitely. Prevention: Demonstrate error in context → better retry behavior.

7. **Session Management Failures and Context Poisoning** — Stateless agents forget everything, or buggy persistence corrupts context with hallucinated facts that propagate forward. Prevention: Show full session lifecycle with validation, demonstrate context poisoning example.

8. **Time Management Disaster** — Spending 40 minutes on setup leaves critical content rushed in final 20 minutes. Prevention: Pre-workshop environment validation 48h ahead, strict time-boxing, backup Colab notebooks if local setup fails.

## Implications for Roadmap

Based on research, the roadmap should follow a 4-phase progressive workshop structure that mirrors how participants will learn incrementally:

### Phase 1: Foundation and Setup (Setup + Basic Agent)
**Rationale:** Must establish working environment and mental models before any advanced concepts. Research shows setup failures consume first 30 minutes if not handled pre-workshop.

**Delivers:**
- Complete setup documentation (GCP project, ADK installation, API keys)
- Environment verification script
- Basic conversational agent (Hello World equivalent)
- Pre-workshop validation process

**Addresses Features:**
- Clear setup/installation guide (table stakes)
- Working starter code (table stakes)
- Troubleshooting guide foundation

**Avoids Pitfalls:**
- Time management disaster (pre-workshop setup validation)
- Environment setup hell (verification script, backup Colab)
- Treating agents as magic (10-15 min concept intro before coding)

**Research Flag:** Standard patterns for workshop setup, but needs testing on 3 OS (Mac, Windows, Linux). No deep research needed.

### Phase 2: Function Calling and Tools (Real-Time Data Integration)
**Rationale:** Function calling is the first real-world capability that differentiates agents from chatbots. Must come before RAG because it's simpler conceptually and establishes tool pattern.

**Delivers:**
- Booking search tools (search_hotels, search_flights)
- Mock API data structure
- Error handling patterns
- Cache-friendly prompt design

**Addresses Features:**
- Function/tool calling (table stakes)
- Real-world API integration (differentiator - at least mock structure)
- Structured output (table stakes - tool responses as JSON)

**Avoids Pitfalls:**
- Demo-driven development (include error handling in first demo)
- Cache-breaking patterns (explain prompt caching with performance comparison)
- Hiding errors from context (show error → better retry pattern)

**Uses Stack:**
- ADK Function Tools
- Mock booking APIs (with structure for real API upgrade)
- Gemini 2.5 Flash for tool selection

**Research Flag:** Standard ADK patterns well-documented. May need research on specific travel APIs (Amadeus, Skyscanner) if using real integration. Otherwise skip research-phase.

### Phase 3: RAG and Knowledge Integration (Static Knowledge Retrieval)
**Rationale:** RAG builds on tool pattern established in Phase 2 but introduces new complexity (embeddings, chunking, semantic search). Natural progression from real-time tools to static knowledge.

**Delivers:**
- Vertex AI RAG Engine integration
- Destination knowledge corpus (10-20 documents)
- Chunking strategy for travel content
- RAG corpus setup script

**Addresses Features:**
- Knowledge base retrieval/RAG (table stakes)
- Context engineering patterns (differentiator - explicitly teach RAG vs. tools decision)

**Avoids Pitfalls:**
- Wrong embeddings and chunking (side-by-side bad vs. good comparison)
- Over-scoped god agents (show when RAG appropriate vs. when to use tools)

**Uses Stack:**
- Vertex AI RAG Engine
- VertexAiRagRetrieval tool
- Google Cloud Storage (for corpus documents)

**Implements Architecture:**
- Knowledge Layer (RAG for destination guides)

**Research Flag:** RAG chunking strategies for travel content may need research. Corpus preparation patterns are standard but timing (10-15 min indexing) needs testing.

### Phase 4: Session Management and Deployment (State Persistence + Production)
**Rationale:** Sessions tie together all previous concepts (tools, RAG, conversation flow) and represent the final production capability. Deployment is the capstone that gives participants working cloud endpoint.

**Delivers:**
- VertexAiSessionService integration
- Conversation state management
- Deployment to Vertex AI Agent Engine
- Production readiness checklist

**Addresses Features:**
- Session/conversation memory (table stakes)
- Live deployment to Vertex AI (differentiator)
- Cost transparency (differentiator - show billing dashboard)

**Avoids Pitfalls:**
- Session management failures (show full lifecycle with validation)
- Demo-driven development (include "Production Checklist" - what's missing from workshop code)
- Over-scoped god agents (deployment as time for multi-agent discussion)

**Uses Stack:**
- VertexAiSessionService
- Vertex AI Agent Engine deployment
- ADK CLI (`adk deploy agent_engine`)

**Implements Architecture:**
- Session State management
- Infrastructure Layer (deployment config)

**Research Flag:** Standard ADK deployment patterns. May need research on quota limits for workshop (50 concurrent participants hitting Vertex AI). Otherwise skip research-phase.

### Phase Ordering Rationale

**Dependency Chain:**
Setup → Function Calling → RAG → Sessions → Deployment

- **Setup must come first:** Blocking for everything, time-critical to validate pre-workshop
- **Function Calling before RAG:** Simpler concept, establishes tool pattern, RAG is "just another tool" to agent
- **RAG before Sessions:** Sessions manage context from both tools and RAG, so need both working first
- **Deployment last:** Requires all features working, serves as capstone demonstration

**Time Budget Validation:**
- Phase 1: 10 min (setup pre-done) + 10 min (basic agent) = 20 min
- Phase 2: 20 min (function calling demo + exercise)
- Phase 3: 25 min (RAG demo + exercise)
- Phase 4: 20 min (sessions) + 15 min (deployment walkthrough)
- Total: 100 min (allows 10-min buffer for 90-min constraint)

**Architectural Coherence:**
Each phase adds one layer to the architecture diagram, making cumulative complexity visible and manageable.

### Research Flags

**Phases needing deeper research during planning:**
- **Phase 2 (Function Calling):** If using real travel APIs (Amadeus, Skyscanner), need API research for auth, rate limits, response schemas. If using mocks, skip research.
- **Phase 3 (RAG):** Chunking strategies for travel content (destinations, itineraries, tips) may need domain-specific research. Corpus indexing timing needs testing (can't have 15-min wait during workshop).
- **Phase 4 (Deployment):** Quota limits and rate limiting for 50 concurrent participants hitting Vertex AI need research and Google coordination.

**Phases with standard patterns (skip research-phase):**
- **Phase 1 (Setup):** Standard workshop setup patterns, well-documented by Google ADK tutorials and Codelabs
- **Phase 2 (Function Calling - if using mocks):** ADK Function Tools pattern is standard, mock data structure is straightforward
- **Phase 4 (Sessions - API aspects):** VertexAiSessionService patterns well-documented in ADK docs

## Confidence Assessment

| Area | Confidence | Notes |
|------|------------|-------|
| Stack | HIGH | All technologies verified with official Google sources. Version numbers current as of Jan 2026. Compatibility matrix validated against ADK 1.23.0 release notes. |
| Features | HIGH | Feature prioritization based on official ADK Crash Course structure, verified workshop design best practices, and real 2026 AI travel agent capabilities from industry sources (Sabre, Booking.com). |
| Architecture | HIGH | Architecture patterns extracted from official ADK documentation, Google's published multi-agent design patterns, and verified ADK sample repositories (travel-concierge example). |
| Pitfalls | HIGH | Pitfalls sourced from Anthropic context engineering research, Google's ADK guides, and verified 2026 production failure analysis (65% pilot-to-production gap from Composio 2025 AI Agent Report). |

**Overall confidence:** HIGH

All research based on official documentation (Google ADK, Vertex AI), verified with recent 2026 sources, and cross-validated across multiple HIGH confidence references. Stack choices align with Google's recommended patterns from official Codelabs. Feature prioritization matches proven workshop design principles (90-min constraint, beginner audience, hands-on exercises). Architecture follows ADK best practices without custom patterns.

### Gaps to Address

**Travel API Integration Decision:**
Research provides structure for both mock and real API approaches, but final decision needed during Phase 2 planning: use free-tier real APIs (Amadeus, Skyscanner) for production skills, or mocks for consistency/simplicity? Recommendation: Start with mocks in core exercises, provide real API upgrade path in reference implementation.

**Chunking Strategy for Travel Content:**
Generic chunking guidance exists, but travel-specific corpus (destination guides, itineraries, multi-page PDFs) may need experimentation during Phase 3. Plan to test 2-3 chunking strategies on sample travel documents before finalizing exercise.

**Workshop Quota Limits:**
50 concurrent participants hitting Vertex AI (Gemini API, RAG Engine, Agent Engine) will hit default quotas. Need to coordinate with Google for quota increase before workshop, but exact limits depend on final exercise design. Address during Phase 4 planning with quota calculator.

**Participant Skill Variance:**
Research identifies 3x skill variance in beginner workshops but doesn't prescribe exact solution. Decision needed during planning: create "fast track" stretch exercises, split into beginner/intermediate tracks, or use graduated hints system? Recommendation: Git branches for catch-up + optional "going further" sections in docs.

## Sources

### Primary (HIGH confidence)

**Official Google ADK Documentation:**
- [Google ADK Official Documentation](https://google.github.io/adk-docs/) — Complete framework documentation, architecture patterns, tools, sessions
- [google-adk PyPI Package](https://pypi.org/project/google-adk/) — Version 1.23.0 release details (Jan 22, 2026)
- [Vertex AI Agent Builder Overview](https://docs.cloud.google.com/agent-builder/agent-development-kit/overview) — Official Google Cloud docs
- [ADK Python Quickstart](https://google.github.io/adk-docs/get-started/python/) — Setup and installation requirements
- [ADK Tools Documentation](https://google.github.io/adk-docs/tools/) — Function calling and RAG integration patterns
- [ADK Deployment Guide](https://google.github.io/adk-docs/deploy/agent-engine/deploy/) — Vertex AI deployment steps

**Official Google Tutorials:**
- [ADK Crash Course Codelab](https://codelabs.developers.google.com/onramp/instructions) — Official 2-notebook 90-min workshop structure
- [Travel Agent MCP Toolbox Codelab](https://codelabs.developers.google.com/travel-agent-mcp-toolbox-adk) — Travel agent reference example
- [Building AI Agents with ADK Foundation](https://codelabs.developers.google.com/devsite/codelabs/build-agents-with-adk-foundation) — Foundational tutorial

**Google Cloud Platform:**
- [Vertex AI Pricing](https://cloud.google.com/vertex-ai/pricing) — Free tier details and cost estimation
- [Google Cloud SDK Release Notes](https://docs.cloud.google.com/sdk/docs/release-notes) — Python version compatibility tracking

### Secondary (MEDIUM confidence)

**AI Agent Best Practices:**
- [Anthropic: Effective Context Engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) — Context engineering patterns, error visibility
- [Context Engineering - Manus Blog](https://manus.im/blog/Context-Engineering-for-AI-Agents-Lessons-from-Building-Manus) — Production context management lessons
- [Google's Eight Essential Multi-Agent Design Patterns (InfoQ)](https://www.infoq.com/news/2026/01/multi-agent-design-patterns/) — Multi-agent patterns and when to avoid over-engineering

**Production Deployment Research:**
- [The 2025 AI Agent Report - Composio](https://composio.dev/blog/why-ai-agent-pilots-fail-2026-integration-roadmap) — 65% pilot failure rate, production gaps analysis
- [Why Most AI Agents Fail in Production - Data Science Collective](https://medium.com/data-science-collective/why-most-ai-agents-fail-in-production-and-how-to-build-ones-that-dont-f6f604bcd075) — Common production pitfalls

**Workshop Design:**
- [7 Tips for Successful Coding Workshop](https://mercedesbernard.com/blog/7-tips-for-successful-coding-workshop/) — Time management, skill variance, hands-on exercises
- [Microsoft AI Agents for Beginners](https://microsoft.github.io/ai-agents-for-beginners/) — Competitive workshop analysis

**Travel Agent Capabilities:**
- [Sabre AI Travel Demo at CES 2026](https://skift.com/2026/01/06/sabre-ces-agentic-ai-travel-trip-booking-demo/) — 2026 travel agent state-of-the-art
- [Booking.com Agentic AI Innovations](https://news.booking.com/bookingcom-debuts-agentic-ai-innovations-adding-to-its-robust-suite-of-genai-tools-for-customers/) — Production travel agent features

### Tertiary (LOW confidence)

**Community Guides:**
- [Context Engineering Complete Guide 2026 - CodeConductor](https://codeconductor.ai/blog/context-engineering/) — General patterns, needs validation
- [DataCamp: Introduction to AI Agents Course](https://www.datacamp.com/courses/introduction-to-ai-agents) — Competitive analysis reference

---
*Research completed: 2026-01-23*
*Ready for roadmap: yes*
