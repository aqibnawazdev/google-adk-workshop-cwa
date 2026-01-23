# Requirements: Google ADK Workshop - Context-Engineered Travel Booking Assistant

**Defined:** 2026-01-23
**Core Value:** Participants learn to build production-ready AI agents with proper context engineering - combining real-time APIs, knowledge bases, and structured data

## v1 Requirements

Requirements for the 90-minute workshop. Each maps to roadmap phases.

### Workshop Materials

- [ ] **WORK-01**: Participant can follow setup guide to configure Python 3.11/3.12, ADK 1.23.0, and GCP credentials
- [ ] **WORK-02**: Participant can complete Exercise 1 (basic agent with Gemini 2.5 Flash)
- [ ] **WORK-03**: Participant can complete Exercise 2 (function calling with flight/hotel search)
- [ ] **WORK-04**: Participant can complete Exercise 3 (RAG integration with destination knowledge)
- [ ] **WORK-05**: Participant can complete Exercise 4 (session management for preferences)
- [ ] **WORK-06**: Participant can reference complete solutions for all exercises
- [ ] **WORK-07**: Participant can use troubleshooting guide to resolve common errors
- [ ] **WORK-08**: Participant can follow deployment guide to publish agent to Vertex AI
- [ ] **WORK-09**: Participant can run reference implementation (complete working agent)
- [ ] **WORK-10**: Participant can understand context engineering module (tools vs RAG vs sessions decision framework)
- [ ] **WORK-11**: Participant can use production readiness checklist to evaluate agent quality
- [ ] **WORK-12**: Pre-workshop validation system verifies participant environment 48h ahead
- [ ] **WORK-13**: Participant can use git branch checkpoints to jump to any exercise

### Agent Capabilities

- [ ] **AGENT-01**: Agent can search flights by destination, dates, and number of passengers
- [ ] **AGENT-02**: Agent can search hotels by location, check-in/out dates, and number of guests
- [ ] **AGENT-03**: Agent can retrieve destination information from knowledge base (visa requirements, attractions, weather)
- [ ] **AGENT-04**: Agent can remember user preferences across conversation (budget, travel style, dietary restrictions)
- [ ] **AGENT-05**: Agent can maintain multi-turn conversations with context retention
- [ ] **AGENT-06**: Agent can handle errors gracefully and provide helpful error messages
- [ ] **AGENT-07**: Agent can provide smart recommendations combining real-time availability with destination knowledge
- [ ] **AGENT-08**: Agent can filter results by user's stated budget
- [ ] **AGENT-09**: Agent can infer unstated preferences from conversation context

### Technical Infrastructure

- [ ] **INFRA-01**: Mock flight API provides search results without rate limits or costs
- [ ] **INFRA-02**: Mock hotel API provides search results without rate limits or costs
- [ ] **INFRA-03**: Destination knowledge corpus with 10-15 PDF guides is pre-indexed in Vertex AI RAG
- [ ] **INFRA-04**: Pre-provisioned GCP accounts have Vertex AI API enabled
- [ ] **INFRA-05**: Workshop materials run in Google Colab for zero-install experience
- [ ] **INFRA-06**: pytest test framework with ADK AgentEvaluator validates agent behavior
- [ ] **INFRA-07**: Agent deploys to Vertex AI Agent Engine with shareable endpoint
- [ ] **INFRA-08**: Cost monitoring dashboard shows token usage and API costs

### Context Engineering

- [ ] **CONTEXT-01**: Workshop explains when to use function calling vs RAG vs session state
- [ ] **CONTEXT-02**: Workshop demonstrates real-time data access pattern (function calling for flights/hotels)
- [ ] **CONTEXT-03**: Workshop demonstrates static knowledge retrieval pattern (RAG for destination guides)
- [ ] **CONTEXT-04**: Workshop demonstrates state management pattern (sessions for user preferences)
- [ ] **CONTEXT-05**: Workshop demonstrates prompt engineering for effective agent instructions
- [ ] **CONTEXT-06**: Workshop demonstrates error handling patterns (errors in context improve behavior)
- [ ] **CONTEXT-07**: Workshop demonstrates cache-friendly patterns (avoid cache-breaking changes)

## v2 Requirements

Deferred to future workshop versions or advanced follow-up sessions.

### Advanced Agent Features

- **AGENT-10**: Agent can plan multi-destination itineraries with optimal routing
- **AGENT-11**: Agent can provide weather-aware recommendations for activities
- **AGENT-12**: Agent can filter hotels by accessibility requirements

### Advanced Infrastructure

- **INFRA-09**: Integration with real travel APIs (Amadeus sandbox) for realistic data
- **INFRA-10**: MCP (Model Context Protocol) tool integration for interoperability
- **INFRA-11**: Production monitoring with alerts and observability dashboard

### Multi-Agent Features

- **MULTI-01**: Multi-agent orchestration with specialized booking, knowledge, and planning agents
- **MULTI-02**: Agent-to-agent communication patterns
- **MULTI-03**: Coordinator agent managing task delegation

## Out of Scope

Explicitly excluded to keep workshop focused and within 90-minute timeline.

| Feature | Reason |
|---------|--------|
| Custom model fine-tuning | Beyond ADK fundamentals, requires ML expertise not in scope |
| Payment processing | Focus on agent capabilities, not business logic integration |
| Real booking system integration | Legal/compliance complexity, use mock data for teaching |
| Advanced RAG techniques | Embedding tuning, hybrid search too advanced for 90-minute beginner workshop |
| Multi-language support | English-only keeps scope manageable |
| Mobile app interface | Web-based Colab and API endpoints sufficient for teaching |
| Production monitoring/observability | Basic deployment only, full monitoring deferred to advanced topics |

## Traceability

Which phases cover which requirements. Updated during roadmap creation.

| Requirement | Phase | Status |
|-------------|-------|--------|
| WORK-01 | Phase 1 | Pending |
| WORK-02 | Phase 5 | Pending |
| WORK-03 | Phase 2 | Pending |
| WORK-04 | Phase 3 | Pending |
| WORK-05 | Phase 4 | Pending |
| WORK-06 | Phase 5 | Pending |
| WORK-07 | Phase 5 | Pending |
| WORK-08 | Phase 4 | Pending |
| WORK-09 | Phase 1 | Pending |
| WORK-10 | Phase 5 | Pending |
| WORK-11 | Phase 5 | Pending |
| WORK-12 | Phase 5 | Pending |
| WORK-13 | Phase 5 | Pending |
| AGENT-01 | Phase 2 | Pending |
| AGENT-02 | Phase 2 | Pending |
| AGENT-03 | Phase 3 | Pending |
| AGENT-04 | Phase 4 | Pending |
| AGENT-05 | Phase 4 | Pending |
| AGENT-06 | Phase 2 | Pending |
| AGENT-07 | Phase 3 | Pending |
| AGENT-08 | Phase 2 | Pending |
| AGENT-09 | Phase 3 | Pending |
| INFRA-01 | Phase 2 | Pending |
| INFRA-02 | Phase 2 | Pending |
| INFRA-03 | Phase 3 | Pending |
| INFRA-04 | Phase 1 | Pending |
| INFRA-05 | Phase 1 | Pending |
| INFRA-06 | Phase 4 | Pending |
| INFRA-07 | Phase 4 | Pending |
| INFRA-08 | Phase 4 | Pending |
| CONTEXT-01 | Phase 2 | Pending |
| CONTEXT-02 | Phase 2 | Pending |
| CONTEXT-03 | Phase 3 | Pending |
| CONTEXT-04 | Phase 4 | Pending |
| CONTEXT-05 | Phase 1 | Pending |
| CONTEXT-06 | Phase 2 | Pending |
| CONTEXT-07 | Phase 2 | Pending |

**Coverage:**
- v1 requirements: 37 total
- Mapped to phases: 37 (100% coverage)
- Unmapped: 0

---
*Requirements defined: 2026-01-23*
*Last updated: 2026-01-23 after roadmap creation*
