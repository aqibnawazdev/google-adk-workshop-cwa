# Roadmap: Google ADK Workshop - Context-Engineered Travel Booking Assistant

## Overview

This roadmap delivers a complete 90-minute hands-on workshop teaching AI agent development through progressive exercises. Participants start with environment setup and basic agents, then build complexity through function calling for real-time booking searches, RAG integration for destination knowledge, and session management for stateful conversations. The journey culminates in deploying a production-ready travel assistant to Vertex AI, with comprehensive support materials ensuring workshop success.

## Phases

**Phase Numbering:**
- Integer phases (1, 2, 3): Planned milestone work
- Decimal phases (2.1, 2.2): Urgent insertions (marked with INSERTED)

Decimal phases appear between their surrounding integers in numeric order.

- [x] **Phase 1: Foundation & Setup** - Environment setup, basic agent, and reference implementation
- [x] **Phase 2: Function Calling & Tools** - Real-time booking search with flight/hotel APIs
- [x] **Phase 3: RAG & Knowledge Integration** - Destination knowledge retrieval and recommendations
- [x] **Phase 4: Sessions & Deployment** - State management, conversation persistence, and Vertex AI deployment
- [ ] **Phase 5: Workshop Support Materials** - Exercises, solutions, troubleshooting, and validation systems

## Phase Details

### Phase 1: Foundation & Setup
**Goal**: Participants can set up their development environment and run a basic conversational agent
**Depends on**: Nothing (first phase)
**Requirements**: WORK-01, WORK-09, INFRA-04, INFRA-05, CONTEXT-05
**Success Criteria** (what must be TRUE):
  1. Participant can install Python 3.11/3.12, ADK 1.23.0, and configure GCP credentials following setup guide
  2. Participant can run basic conversational agent with Gemini 2.5 Flash in Google Colab or local environment
  3. Participant can examine reference implementation to understand target architecture
  4. Environment verification script confirms all dependencies and API access work correctly
**Plans**: 4 plans

Plans:
- [x] 01-01-PLAN.md — Environment verification notebook (00-setup-verification.ipynb)
- [x] 01-02-PLAN.md — Basic hello agent notebook (01-hello-agent.ipynb)
- [x] 01-03-PLAN.md — Reference implementation (agent.py, README, .env.template)
- [x] 01-04-PLAN.md — Setup documentation (SETUP.md, workshop README.md)

### Phase 2: Function Calling & Tools
**Goal**: Agent can search real-time booking data using function calling for flights and hotels
**Depends on**: Phase 1
**Requirements**: WORK-03, AGENT-01, AGENT-02, AGENT-06, AGENT-08, INFRA-01, INFRA-02, CONTEXT-01, CONTEXT-02, CONTEXT-06, CONTEXT-07
**Success Criteria** (what must be TRUE):
  1. Agent can search flights by destination, dates, and passenger count returning available options
  2. Agent can search hotels by location, check-in/out dates, and guest count returning available properties
  3. Agent handles API errors gracefully with helpful error messages when searches fail
  4. Agent filters search results by user's stated budget constraints
  5. Workshop materials explain when to use function calling vs RAG vs session state with decision framework
**Plans**: 3 plans

Plans:
- [x] 02-01-PLAN.md — Function calling exercise notebook (02-tools-functions.ipynb)
- [x] 02-02-PLAN.md — Reference implementation tools (tools.py with search_flights, search_hotels)
- [x] 02-03-PLAN.md — Reference implementation README update (decision framework, tool docs)

### Phase 3: RAG & Knowledge Integration
**Goal**: Agent retrieves destination information from knowledge base and provides smart recommendations
**Depends on**: Phase 2
**Requirements**: WORK-04, AGENT-03, AGENT-07, AGENT-09, INFRA-03, CONTEXT-03
**Success Criteria** (what must be TRUE):
  1. Agent retrieves destination information from Vertex AI RAG knowledge base including visa requirements, attractions, and weather
  2. Agent provides smart recommendations combining real-time availability with destination knowledge
  3. Agent infers unstated preferences from conversation context to personalize suggestions
  4. Destination knowledge corpus with 10-15 PDF guides is pre-indexed and searchable
  5. Workshop materials demonstrate static knowledge retrieval pattern and RAG integration
**Plans**: 6 plans

Plans:
- [x] 03-01-PLAN.md — Destination guides batch 1 (Tokyo, Paris, NYC, Singapore, London)
- [x] 03-02-PLAN.md — Destination guides batch 2 (Rome, Bangkok, Sydney, Barcelona, Dubai)
- [x] 03-03-PLAN.md — Corpus setup scripts (PDF conversion, RAG corpus creation, validation)
- [x] 03-04-PLAN.md — Reference implementation RAG (rag_tools.py, hybrid_agent.py)
- [x] 03-05-PLAN.md — Exercise 3 notebook (03-rag-knowledge.ipynb)
- [x] 03-06-PLAN.md — README update with RAG documentation

### Phase 4: Sessions & Deployment
**Goal**: Agent maintains conversation state across turns and deploys to production Vertex AI endpoint
**Depends on**: Phase 3
**Requirements**: WORK-05, WORK-08, AGENT-04, AGENT-05, INFRA-06, INFRA-07, INFRA-08, CONTEXT-04
**Success Criteria** (what must be TRUE):
  1. Agent remembers user preferences across conversation turns including budget, travel style, and dietary restrictions
  2. Agent maintains multi-turn conversations with full context retention using Vertex AI Session Service
  3. Agent deploys to Vertex AI Agent Engine with shareable endpoint accessible via API
  4. pytest tests with ADK AgentEvaluator validate agent behavior and conversation flows
  5. Cost monitoring dashboard shows token usage and API costs for workshop usage
  6. Workshop materials demonstrate state management pattern and deployment process
**Plans**: 5 plans

Plans:
- [x] 04-01-PLAN.md — Exercise 4 notebook for state management (04-sessions-state.ipynb)
- [x] 04-02-PLAN.md — Reference implementation state utilities (state_utils.py, agent.py updates)
- [x] 04-03-PLAN.md — Deployment guide and script (DEPLOYMENT.md, deploy.py)
- [x] 04-04-PLAN.md — AgentEvaluator reference tests (tests/, eval datasets)
- [x] 04-05-PLAN.md — Cost monitoring and README update (cost_tracker.py, README.md)

### Phase 5: Workshop Support Materials
**Goal**: Participants can complete all exercises with solutions, troubleshooting, and validation support
**Depends on**: Phase 4
**Requirements**: WORK-02, WORK-06, WORK-07, WORK-10, WORK-11, WORK-12, WORK-13
**Success Criteria** (what must be TRUE):
  1. Participant can complete Exercise 1 (basic agent), Exercise 2 (function calling), Exercise 3 (RAG), and Exercise 4 (sessions) with step-by-step instructions
  2. Participant can reference complete solutions for all exercises with detailed explanations
  3. Participant can use troubleshooting guide to resolve common errors including auth issues, missing dependencies, and API limits
  4. Participant can understand context engineering decision framework for choosing tools vs RAG vs sessions
  5. Pre-workshop validation system verifies participant environment 48 hours ahead with confirmation required
  6. Participant can use git branch checkpoints to jump to any exercise for catch-up
  7. Production readiness checklist helps participants evaluate agent quality beyond workshop scope
**Plans**: 6 plans

Plans:
- [ ] 05-01-PLAN.md — Centralized troubleshooting guide (TROUBLESHOOTING.md)
- [ ] 05-02-PLAN.md — Context engineering decision framework (CONTEXT-ENGINEERING.md)
- [ ] 05-03-PLAN.md — Production readiness checklist (PRODUCTION-READINESS.md)
- [ ] 05-04-PLAN.md — Git checkpoint branches and documentation (create-checkpoints.sh, CHECKPOINTS.md)
- [ ] 05-05-PLAN.md — Pre-validation confirmation mechanism (00-setup-verification.ipynb updates)
- [ ] 05-06-PLAN.md — Solutions audit and enhancement (all exercise notebooks)

## Progress

**Execution Order:**
Phases execute in numeric order: 1 → 2 → 3 → 4 → 5

| Phase | Plans Complete | Status | Completed |
|-------|----------------|--------|-----------|
| 1. Foundation & Setup | 4/4 | Complete | 2026-01-23 |
| 2. Function Calling & Tools | 3/3 | Complete | 2026-01-24 |
| 3. RAG & Knowledge Integration | 6/6 | Complete | 2026-01-24 |
| 4. Sessions & Deployment | 5/5 | Complete | 2026-01-24 |
| 5. Workshop Support Materials | 0/6 | Not started | - |
