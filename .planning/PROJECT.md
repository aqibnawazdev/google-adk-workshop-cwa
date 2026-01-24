# Google ADK Workshop - Context-Engineered Travel Booking Assistant

## What This Is

A comprehensive 90-minute hands-on workshop teaching Google Agent Development Kit (ADK) through building a travel booking assistant agent. The workshop demonstrates context engineering by combining real-time booking APIs, travel knowledge retrieval, and intelligent conversation management. Deliverables include step-by-step tutorials, starter code, complete reference implementation, and progressive hands-on exercises for developers new to AI agents.

## Core Value

Participants learn to build production-ready AI agents with proper context engineering - specifically how to combine real-time APIs with structured data and knowledge bases to create intelligent, stateful booking assistants that can search hotels/flights, remember user preferences, and provide expert travel guidance.

## Current State

**Status:** v1.0 Shipped (2026-01-24)

Complete 90-minute workshop with 4 progressive exercises, reference implementation, and comprehensive support materials.

For milestone history, see: `.planning/MILESTONES.md`

## Requirements

### Validated (v1.0)

**Workshop Materials (13):**
- [x] Step-by-step tutorial documentation with clear explanations for AI beginners
- [x] Starter code project (boilerplate) participants build upon
- [x] Complete reference implementation demonstrating all concepts
- [x] 4 progressive exercises building from simple to complete agent
- [x] Exercise solutions with detailed three-layer explanations
- [x] GCP and ADK setup instructions for pre-provisioned accounts
- [x] Troubleshooting guide with symptom-based navigation
- [x] Deployment guide for Vertex AI Agent Engine
- [x] Context engineering decision framework
- [x] Production readiness checklist
- [x] Pre-workshop validation system (48-hour ahead)
- [x] Git checkpoint branches for catch-up

**Core ADK Concepts (4):**
- [x] Function calling/tools - booking search APIs for real-time availability
- [x] RAG integration - travel knowledge base for destination info and recommendations
- [x] Session management - stateful conversations that remember user preferences
- [x] Deployment to Vertex AI - publishing the agent to production

**Context Engineering Demonstrations (7):**
- [x] Real-time + static data fusion (live booking data + destination knowledge)
- [x] Structured data grounding (inventory, pricing, availability constraints)
- [x] Prompt engineering patterns (effective agent instruction design)
- [x] Tools vs RAG vs Sessions decision framework
- [x] Error-in-context pattern (graceful degradation)
- [x] Cache-friendly patterns
- [x] State prefix pattern (user:, temp:, app:)

**Travel Booking Agent Capabilities (9):**
- [x] Search hotels with user preferences and constraints
- [x] Search flights with date/destination filters
- [x] Budget filtering in search results
- [x] Retrieve destination information from knowledge base
- [x] Remember user preferences across conversation turns
- [x] Infer unstated preferences from context
- [x] Provide booking recommendations based on context
- [x] Multi-turn conversation support
- [x] Graceful error handling

**Technical Infrastructure (8):**
- [x] Mock flight API (no rate limits or costs)
- [x] Mock hotel API (no rate limits or costs)
- [x] 10 destination knowledge guides (pre-indexed)
- [x] Colab-first environment (zero-install)
- [x] pytest + AgentEvaluator tests
- [x] Cost monitoring utilities

### Active

(No active requirements - v1.0 complete)

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

- **Timeline**: Workshop must complete in 90 minutes including setup, 4 exercises, and deployment
- **Audience Level**: Beginners to AI agents - need conceptual explanations, not just code
- **Cost**: Keep minimal - use free tier, avoid expensive Vertex AI operations, use small RAG corpus
- **Tech Stack**: Google ADK, Vertex AI, Python 3, Flask - maintain consistency with reference project
- **GCP Region**: Participants use pre-provisioned accounts (specific region TBD by organizers)
- **Complexity**: Balance depth vs time - cover all 4 concepts but keep implementations simple

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| Travel booking domain instead of sales | More relatable for workshop audience, demonstrates similar ADK patterns in different context | ✓ Good |
| Progressive exercises (4) vs single build | Allows checkpoints, accommodates different pace learners, clearer concept isolation | ✓ Good |
| Mock booking data vs real APIs | Keeps costs minimal, avoids API rate limits, simplifies setup, focuses on ADK concepts | ✓ Good |
| Include deployment despite time constraint | Critical for production-ready understanding, distinguishes ADK from toy examples | ✓ Good |
| Colab-first approach | Eliminates local environment setup for 90% of participants | ✓ Good |
| Google AI API key (not Vertex AI) | Simpler participant experience, no GCP project config needed | ✓ Good |
| Hybrid agent for RAG constraint | ADK can't mix RAG with function tools in single agent | ✓ Good |
| State prefixes (user:, temp:, app:) | Clear persistence scope semantics | ✓ Good |
| Three-layer solution format | Explains WHY patterns work, not just WHAT | ✓ Good |
| 48-hour pre-validation | Catches setup issues before workshop day | ✓ Good |

---
*Last updated: 2026-01-24 after v1.0 milestone completion*
