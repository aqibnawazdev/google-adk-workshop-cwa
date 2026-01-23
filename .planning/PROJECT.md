# Google ADK Workshop - Context-Engineered Travel Booking Assistant

## What This Is

A comprehensive 90-minute hands-on workshop teaching Google Agent Development Kit (ADK) through building a travel booking assistant agent. The workshop demonstrates context engineering by combining real-time booking APIs, travel knowledge retrieval, and intelligent conversation management. Deliverables include step-by-step tutorials, starter code, complete reference implementation, and progressive hands-on exercises for developers new to AI agents.

## Core Value

Participants learn to build production-ready AI agents with proper context engineering - specifically how to combine real-time APIs with structured data and knowledge bases to create intelligent, stateful booking assistants that can search hotels/flights, remember user preferences, and provide expert travel guidance.

## Requirements

### Validated

(None yet — ship to validate)

### Active

**Workshop Materials:**
- [ ] Step-by-step tutorial documentation with clear explanations for AI beginners
- [ ] Starter code project (boilerplate) participants build upon
- [ ] Complete reference implementation demonstrating all concepts
- [ ] 3-4 progressive exercises building from simple to complete agent
- [ ] Exercise solutions with detailed explanations
- [ ] GCP and ADK setup instructions for pre-provisioned accounts

**Core ADK Concepts (must be demonstrated):**
- [ ] Function calling/tools - booking search APIs for real-time availability
- [ ] RAG integration - travel knowledge base for destination info and recommendations
- [ ] Session management - stateful conversations that remember user preferences
- [ ] Deployment to Vertex AI - publishing the agent to production

**Context Engineering Demonstrations:**
- [ ] Real-time + static data fusion (live booking data + destination knowledge)
- [ ] Structured data grounding (inventory, pricing, availability constraints)
- [ ] Prompt engineering patterns (effective agent instruction design)

**Travel Booking Agent Capabilities:**
- [ ] Search hotels with user preferences and constraints
- [ ] Search flights with date/destination filters
- [ ] Retrieve destination information from knowledge base
- [ ] Remember user preferences across conversation turns
- [ ] Provide booking recommendations based on context

### Out of Scope

- Multi-agent orchestration - too advanced for 90-minute beginner workshop
- Custom model fine-tuning - beyond ADK fundamentals
- Advanced RAG techniques - chunking strategies, hybrid search, embeddings tuning
- Production monitoring/observability - basic deployment only
- Payment processing integration - keep focus on agent capabilities
- Real booking system integration - use mock/demo data for simplicity

## Context

**Reference Project:**
The adk-sales-api project demonstrates ADK patterns with function calling and RAG for a sales assistant. This workshop adapts these patterns to a travel booking domain with booking search APIs and destination knowledge retrieval.

**Target Audience:**
Developers familiar with Python and REST APIs, but new to LLMs and AI agent frameworks. Workshop needs clear conceptual explanations of how agents work, when to use tools vs RAG, and how context engineering improves agent responses.

**Workshop Format:**
Guided exercises where participants code independently with checkpoints and instructor guidance. Not live coding - participants build at their own pace with step-by-step instructions and reference solutions available.

**Technical Environment:**
Participants have pre-provisioned Google Cloud accounts with Vertex AI access. Workshop uses Google ADK framework, Python, and Flask (consistent with reference project patterns).

**Context Engineering Focus:**
Demonstrate how combining different context sources (real-time APIs, knowledge bases, conversation history, structured business logic) creates more capable and reliable agents than LLM alone.

## Constraints

- **Timeline**: Workshop must complete in 90 minutes including setup, 3-4 exercises, and deployment
- **Audience Level**: Beginners to AI agents - need conceptual explanations, not just code
- **Cost**: Keep minimal - use free tier, avoid expensive Vertex AI operations, use small RAG corpus
- **Tech Stack**: Google ADK, Vertex AI, Python 3, Flask - maintain consistency with reference project
- **GCP Region**: Participants use pre-provisioned accounts (specific region TBD by organizers)
- **Complexity**: Balance depth vs time - cover all 4 concepts but keep implementations simple

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| Travel booking domain instead of sales | More relatable for workshop audience, demonstrates similar ADK patterns in different context | — Pending |
| Progressive exercises (3-4) vs single build | Allows checkpoints, accommodates different pace learners, clearer concept isolation | — Pending |
| Mock booking data vs real APIs | Keeps costs minimal, avoids API rate limits, simplifies setup, focuses on ADK concepts | — Pending |
| Include deployment despite time constraint | Critical for production-ready understanding, distinguishes ADK from toy examples | — Pending |

---
*Last updated: 2026-01-23 after initialization*
