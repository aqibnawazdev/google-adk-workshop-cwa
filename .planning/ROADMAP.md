# Roadmap: Google ADK Workshop - Context-Engineered Travel Booking Assistant

## Overview

This roadmap delivers a complete 90-minute hands-on workshop teaching AI agent development through progressive exercises. Participants start with environment setup and basic agents, then build complexity through function calling for real-time booking searches, RAG integration for destination knowledge, and session management for stateful conversations. The journey culminates in deploying a production-ready travel assistant to Vertex AI, with comprehensive support materials ensuring workshop success.

## Phases

**Phase Numbering:**
- Integer phases (1, 2, 3): Planned milestone work
- Decimal phases (2.1, 2.2): Urgent insertions (marked with INSERTED)

Decimal phases appear between their surrounding integers in numeric order.

- [x] **Phase 1: Foundation & Setup** - Environment setup, basic agent, and reference implementation
- [ ] **Phase 2: Function Calling & Tools** - Real-time booking search with flight/hotel APIs
- [ ] **Phase 3: RAG & Knowledge Integration** - Destination knowledge retrieval and recommendations
- [ ] **Phase 4: Sessions & Deployment** - State management, conversation persistence, and Vertex AI deployment
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
- [ ] 01-01-PLAN.md — Environment verification notebook (00-setup-verification.ipynb)
- [ ] 01-02-PLAN.md — Basic hello agent notebook (01-hello-agent.ipynb)
- [ ] 01-03-PLAN.md — Reference implementation (agent.py, README, .env.template)
- [ ] 01-04-PLAN.md — Setup documentation (SETUP.md, workshop README.md)

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
- [ ] 02-01-PLAN.md — Function calling exercise notebook (02-tools-functions.ipynb)
- [ ] 02-02-PLAN.md — Reference implementation tools (tools.py with search_flights, search_hotels)
- [ ] 02-03-PLAN.md — Reference implementation README update (decision framework, tool docs)

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
**Plans**: TBD

Plans:
- [ ] 03-01: TBD during phase planning

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
**Plans**: TBD

Plans:
- [ ] 04-01: TBD during phase planning

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
**Plans**: TBD

Plans:
- [ ] 05-01: TBD during phase planning

## Progress

**Execution Order:**
Phases execute in numeric order: 1 → 2 → 3 → 4 → 5

| Phase | Plans Complete | Status | Completed |
|-------|----------------|--------|-----------|
| 1. Foundation & Setup | 4/4 | Complete | 2026-01-23 |
| 2. Function Calling & Tools | 0/3 | In progress | - |
| 3. RAG & Knowledge Integration | 0/TBD | Not started | - |
| 4. Sessions & Deployment | 0/TBD | Not started | - |
| 5. Workshop Support Materials | 0/TBD | Not started | - |
