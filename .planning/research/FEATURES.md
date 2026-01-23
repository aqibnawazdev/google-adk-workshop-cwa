# Feature Research

**Domain:** Beginner-friendly AI Agent Workshop (Google ADK)
**Researched:** 2026-01-23
**Confidence:** HIGH

## Feature Landscape

### Table Stakes (Users Expect These)

Features participants assume exist. Missing these = workshop fails.

#### Workshop Materials Features

| Feature | Why Expected | Complexity | Notes |
|---------|--------------|------------|-------|
| Clear setup/installation guide | Beginners need exact steps to get environment working | LOW | Must cover: GCP project setup, ADK installation, API key config. Document prerequisites clearly. |
| Working starter code | Can't learn if base code doesn't run | LOW | Pre-built scaffolding with comments. Test on clean environment before workshop. |
| Step-by-step tutorial with checkpoints | 90 minutes = no time for debugging mysteries | MEDIUM | Each checkpoint = working code. Create git branches for each step so stragglers can catch up. |
| Hands-on exercises (not just demos) | "Best learning is done by doing" - workshop design best practice | MEDIUM | Short exercises after each concept. 5-10 min each max. |
| Solutions/reference implementation | Participants need to compare when stuck | LOW | Complete working solution in separate branch/folder. |
| Troubleshooting guide | Common errors will happen with 20+ participants | LOW | Document top 5 errors from dry runs: auth issues, missing dependencies, API limits, etc. |
| Post-workshop resources | Learning continues after 90 minutes | LOW | Links to official ADK docs, next steps, community resources. |

#### Agent Features (What the Demo Agent Must Do)

| Feature | Why Expected | Complexity | Notes |
|---------|--------------|------------|-------|
| Natural language queries | Core AI agent capability - participants expect to "talk" to agent | LOW | Use Gemini's built-in NLU. Example: "Find flights to Tokyo next week" |
| Function/tool calling | Table stakes for production agents - demonstrates real-world capability | MEDIUM | 2-3 simple tools: search_flights, get_hotel_prices, check_weather |
| Knowledge base retrieval (RAG) | Shows how to ground agents in custom data vs hallucinating | MEDIUM | Small travel knowledge base: visa requirements, travel tips, airport codes |
| Session/conversation memory | Agents must remember context within conversation | MEDIUM | Track preferences mentioned earlier: "I prefer window seats" → remember for booking |
| Structured output | Real systems need parseable responses, not just chat | LOW | Return booking details as JSON, not just text descriptions |
| Error handling basics | Production agents must handle API failures gracefully | LOW | Show try/catch pattern for tool calls, fallback messages |

### Differentiators (Competitive Advantage)

Features that make this workshop exceptional. Not required, but valuable.

| Feature | Value Proposition | Complexity | Notes |
|---------|-------------------|------------|-------|
| Live deployment to Vertex AI | Most tutorials stop at localhost - show real deployment | MEDIUM | Deploy final agent to Vertex AI Agent Engine in last 15 minutes. Gives participants working cloud endpoint. |
| Context engineering patterns | This is the workshop's CORE VALUE - teach the "why" not just "how" | MEDIUM | Explicitly demonstrate: when to use RAG vs tools vs structured data. Show context window as scarce resource. |
| Real-world API integration | Mock APIs feel toy-ish. Real APIs = production skills | MEDIUM | Use actual travel APIs (free tier): Amadeus, Skyscanner, OpenWeatherMap. Shows auth, rate limits, response parsing. |
| Interactive debugging session | Most workshops hide failures. Show how to debug agent failures live. | LOW | Intentionally trigger common issues, debug together. Builds confidence. |
| Cost transparency | Participants worry about surprise bills | LOW | Show GCP billing dashboard, explain free tier limits, estimate workshop costs (~$0.50/participant). |
| Modular architecture | Teach clean code, not spaghetti | MEDIUM | Separate concerns: tools/functions.py, knowledge/kb.py, agent/agent.py. Professional structure from day 1. |
| Template for next project | Give participants headstart on their own agents | LOW | Provide "agent-starter-template" with auth, config, logging already set up. |

### Anti-Features (Commonly Requested, Often Problematic)

Features that seem good but create problems in 90-minute beginner workshop.

| Feature | Why Requested | Why Problematic | Alternative |
|---------|---------------|-----------------|-------------|
| Multi-agent orchestration | Sounds sophisticated, is trendy | Creates complexity explosion. Debugging agent handoffs with beginners = disaster. Needs 4+ hours to teach properly. | Single agent with multiple tools. Explain pattern, provide post-workshop tutorial link. |
| Custom fine-tuned models | Sounds "production-ready" | Requires ML expertise, training time, costs. Completely orthogonal to context engineering concepts. | Use Gemini out-of-box. Mention fine-tuning in "advanced topics" slide. |
| Real payment processing | "Make it realistic" | PCI compliance, security nightmares, liability. Participants might accidentally charge real cards. | Mock booking confirmation with booking reference IDs. Show where Stripe/payment would integrate. |
| Complex UI/frontend | "Agents need interfaces" | 90 minutes insufficient for React + agent code. Frontend debugging distracts from agent concepts. | Terminal interface or simple Streamlit app. Focus on agent, not CSS. |
| Advanced RAG (GraphRAG, hierarchical search) | "Teach cutting edge" | Requires vector DB setup, embedding concepts, graph theory. Too much for beginners. | Simple semantic search with small knowledge base. Mention GraphRAG as advanced topic. |
| Production monitoring/observability | "Production-ready" buzzword | Requires understanding of metrics, logging infra, dashboards. Workshop would become monitoring tutorial. | Basic print statements for visibility. Link to Cloud Logging docs for post-workshop. |
| Custom tool frameworks | "Learn tool building" | Time sink. Many edge cases. Not ADK-specific knowledge. | Use ADK's built-in tool decorator. Show pattern, provide working examples. |

## Feature Dependencies

```
WORKSHOP FLOW DEPENDENCIES:

[Setup Guide]
    └──enables──> [Starter Code]
                      └──enables──> [Function Calling Exercise]
                                        └──enables──> [RAG Exercise]
                                                          └──enables──> [Session Memory Exercise]
                                                                            └──enables──> [Deployment Exercise]

[Troubleshooting Guide] ──supports──> [All Exercises] (parallel, not blocking)

AGENT CAPABILITY DEPENDENCIES:

[Natural Language Queries]
    └──requires──> [Gemini API Setup]

[Function Calling]
    └──requires──> [Tool Definitions]
                       └──optional──> [Real API Keys] (can use mocks)

[RAG/Knowledge Base]
    └──requires──> [Vector Embedding] (can use ADK's built-in)
                       └──requires──> [Knowledge Documents]

[Session Memory]
    └──requires──> [State Management Pattern]
                       └──enhances──> [Function Calling] (remember preferences)

[Deployment]
    └──requires──> [GCP Project]
    └──requires──> [All Core Features Working Locally]
```

### Dependency Notes

- **Exercises must be sequential:** Each builds on previous. Can't teach RAG before participants understand function calling.
- **Setup is critical path:** If setup fails, everything fails. Needs most robust documentation + testing.
- **Real APIs are optional:** Workshop works with mocks, but real APIs increase engagement. Provide both paths.
- **Deployment is final capstone:** Can be skipped if time runs short. Local agent is still valuable outcome.

## MVP Definition

### Launch With (v1 - Minimum Viable Workshop)

Minimum viable workshop — what's needed to deliver core value proposition.

- [x] **Installation guide (GCP + ADK)** — Workshop literally can't start without this. Test on 3 different OS.
- [x] **Starter code that runs** — Hello-world agent that responds to basic query. Proves environment works.
- [x] **Function calling exercise** — Teach tool use with 2 simple functions (search_flights, get_hotels). Core ADK capability.
- [x] **RAG/knowledge base exercise** — Load 5-10 travel documents, query them. Shows context engineering in action.
- [x] **Session memory exercise** — Track user preferences across conversation. Demonstrates state management.
- [x] **Hands-on exercises (3-4 short ones)** — After each concept, 5-min "now you try" exercise.
- [x] **Working solution code** — Complete reference implementation. Participants can compare.
- [x] **Troubleshooting FAQ** — Top 5 errors with fixes. Based on dry run learnings.

**Time budget check:** 90 minutes
- Setup/intro: 10 min
- Function calling: 20 min (demo 10 + exercise 10)
- RAG: 25 min (demo 15 + exercise 10)
- Session memory: 20 min (demo 10 + exercise 10)
- Wrap-up: 15 min (recap, next steps, Q&A)

### Add After Validation (v1.x)

Features to add once core workshop is working and time-tested.

- [ ] **Deployment to Vertex AI** — Add as optional "bonus section" if workshop runs fast. 15-min deployment walkthrough.
- [ ] **Real API integration** — Upgrade from mocks to Amadeus/Skyscanner APIs. Requires API key distribution strategy.
- [ ] **Interactive debugging demo** — Show common failure modes + how to debug. Builds troubleshooting confidence.
- [ ] **Cost dashboard walkthrough** — 5-min GCP billing overview. Reduces anxiety about costs.
- [ ] **Agent starter template** — Polished template repo participants can clone for next project.

### Future Consideration (v2+)

Features to defer until workshop format is battle-tested.

- [ ] **Advanced RAG patterns** — GraphRAG, hierarchical search. Requires separate 2-hour workshop.
- [ ] **Multi-agent patterns** — After participants master single agents (workshop 2 in series).
- [ ] **Production monitoring** — Logging, metrics, observability. Separate ops-focused workshop.
- [ ] **Fine-tuning walkthrough** — Custom models. Requires ML background, 3+ hour workshop.
- [ ] **Security deep-dive** — Auth, secrets management, PII handling. Separate security-focused workshop.

## Feature Prioritization Matrix

| Feature | User Value | Implementation Cost | Priority |
|---------|------------|---------------------|----------|
| Installation guide | HIGH | LOW | P1 |
| Starter code | HIGH | LOW | P1 |
| Function calling exercise | HIGH | MEDIUM | P1 |
| RAG exercise | HIGH | MEDIUM | P1 |
| Session memory exercise | HIGH | MEDIUM | P1 |
| Hands-on exercises | HIGH | LOW | P1 |
| Solution code | HIGH | LOW | P1 |
| Troubleshooting FAQ | HIGH | LOW | P1 |
| Deployment to Vertex AI | MEDIUM | MEDIUM | P2 |
| Real API integration | MEDIUM | MEDIUM | P2 |
| Debugging demo | MEDIUM | LOW | P2 |
| Cost dashboard | MEDIUM | LOW | P2 |
| Starter template | MEDIUM | MEDIUM | P2 |
| Advanced RAG | LOW | HIGH | P3 |
| Multi-agent patterns | LOW | HIGH | P3 |
| Production monitoring | LOW | MEDIUM | P3 |
| Fine-tuning | LOW | HIGH | P3 |

**Priority key:**
- P1: Must have for launch (core 90-min workshop)
- P2: Should have, add when core is stable
- P3: Nice to have, separate advanced workshops

## Workshop Design Best Practices Applied

Based on research into 90-minute coding workshop design:

### Time Management
- **Practice runs finish faster:** Dry run in 60 min, real workshop takes 80-90 min due to questions/delays
- **Small runnable steps:** Each code change should compile/run. No multi-slide debugging sessions.
- **Checkpoints via git branches:** Create branch after each major concept so stragglers can `git checkout step-2` and catch up

### Supporting Skill Levels
- **Participants vary widely:** Expect 3x skill range. Provide "fast track" extensions for experienced devs.
- **Documentation for every step:** Don't assume knowledge. Type everything participants need into tutorial.
- **Start with deploy/demo:** Show working agent first, then build it. Motivates participants.

### Code Design
- **Big fonts everywhere:** Code blocks, terminal output. Workshop screens are far from back row.
- **Short, focused code:** Each concept = <20 lines new code. Not 200-line files.
- **Comments everywhere:** Assume participants skim, don't read carefully.

### Exercise Structure
- **Each lesson = hands-on challenge:** No passive lectures. Demo → Exercise → Solution pattern.
- **5-10 minute exercises max:** Longer = participants get stuck, workshop derails.
- **Immediate feedback:** Exercises have clear success criteria ("Agent should return flight options")

## Context Engineering Teaching Strategy

This is the differentiator. How we teach context engineering to beginners:

### 1. Context Window as Scarce Resource (Concept)
**When:** Introduction (5 min)
**How:** Visual diagram showing LLM context window. "Imagine 100-page limit for agent's memory"
**Why matters:** Sets up all future decisions about RAG vs tools vs prompts

### 2. Function Calling = External Capability (Pattern)
**When:** Exercise 1 (20 min)
**How:** Show agent with vs without flight search tool. "Context window holds question, tool gives fresh data"
**Demonstrates:** Real-time data access without context pollution

### 3. RAG = Domain Knowledge (Pattern)
**When:** Exercise 2 (25 min)
**How:** Query knowledge base for visa requirements. "Can't fit all travel rules in context, retrieve relevant docs"
**Demonstrates:** Selective context loading, grounding in facts

### 4. Session Memory = State Management (Pattern)
**When:** Exercise 3 (20 min)
**How:** Remember "I'm vegetarian" across conversation. "Store preferences outside context, load when relevant"
**Demonstrates:** Context budget optimization, personalization

### 5. Structured Data = Reliable Integration (Pattern)
**When:** Woven throughout
**How:** All tool outputs return JSON/Pydantic models. "Systems need parseable data, not prose"
**Demonstrates:** Production-ready agent design

## Competitor Workshop Analysis

| Feature | DataCamp "Intro to AI Agents" (90 min) | Microsoft "AI Agents for Beginners" | Our ADK Workshop |
|---------|--------------------------------------|-------------------------------------|-----------------|
| Duration | 90 min | 12 lessons (self-paced) | 90 min (matches sweet spot) |
| Hands-on coding | No ("without writing code") | Yes | Yes (core focus) |
| Real deployment | No | No | Yes (Vertex AI - unique!) |
| Context engineering focus | No | Partial | Yes (our differentiator) |
| Cloud platform | Agnostic | Azure-leaning | GCP/Vertex AI |
| Travel agent demo | Generic examples | Generic examples | Travel booking (relatable, practical) |
| Cost to learner | Free trial then paid | Free | Free (GCP free tier) |

**Our competitive advantages:**
1. **Only workshop with real cloud deployment** - Participants leave with live agent URL
2. **Context engineering as first-class concept** - Not hidden implementation detail
3. **Real APIs** - Not toy examples, actual Amadeus/Skyscanner integration
4. **GCP/Vertex AI native** - Participants learn Google's production stack

## Sources

### Official Documentation & Tutorials
- [Google ADK Documentation](https://google.github.io/adk-docs/)
- [ADK Overview - Vertex AI](https://docs.cloud.google.com/agent-builder/agent-development-kit/overview)
- [ADK Crash Course - Google Codelabs](https://codelabs.developers.google.com/onramp/instructions)
- [Deploy to Vertex AI Agent Engine](https://google.github.io/adk-docs/deploy/agent-engine/)
- [Quickstart with ADK](https://docs.cloud.google.com/agent-builder/agent-engine/memory-bank/quickstart-adk)

### AI Agent Best Practices
- [Microsoft AI Agents for Beginners](https://microsoft.github.io/ai-agents-for-beginners/)
- [Anthropic: Effective Context Engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)
- [Weaviate: Context Engineering for AI Agents](https://weaviate.io/blog/context-engineering)
- [LlamaIndex: Context Engineering Techniques](https://www.llamaindex.ai/blog/context-engineering-what-it-is-and-techniques-to-consider)
- [InfoWorld: Anatomy of AI Agent Knowledge Base](https://www.infoworld.com/article/4091400/anatomy-of-an-ai-agent-knowledge-base.html)

### Travel Agent Examples & Capabilities
- [Sabre AI Travel Demo at CES 2026](https://skift.com/2026/01/06/sabre-ces-agentic-ai-travel-trip-booking-demo/)
- [Booking.com Agentic AI Innovations](https://news.booking.com/bookingcom-debuts-agentic-ai-innovations-adding-to-its-robust-suite-of-genai-tools-for-customers/)
- [AI Agent Use Cases for Travel Industry](https://anglara.com/blog/ai-agent-use-cases-for-travel-industry/)
- [Best AI Booking Agents 2026](https://cognitivefuture.ai/ai-booking-agents/)

### Workshop Design Best Practices
- [7 Tips for Successful Coding Workshop](https://mercedesbernard.com/blog/7-tips-for-successful-coding-workshop/)
- [How to Run a Coding Workshop](https://codefol.io/posts/how-do-i-run-a-ruby-workshop/)
- [DataCamp: Introduction to AI Agents Course](https://www.datacamp.com/courses/introduction-to-ai-agents)

### Context Engineering & Data Systems
- [2026 Data Engineering Roadmap for Agentic AI](https://medium.com/@sanjeebmeister/the-2026-data-engineering-roadmap-building-data-systems-for-the-agentic-ai-era-8e7064c2cf55)
- [CodeConductor: Context Engineering Complete Guide 2026](https://codeconductor.ai/blog/context-engineering/)
- [Context Engineering Lessons from Building Manus](https://manus.im/blog/Context-Engineering-for-AI-Agents-Lessons-from-Building-Manus)

---
*Feature research for: Google ADK Workshop (Travel Booking Agent)*
*Researched: 2026-01-23*
*Confidence: HIGH - Based on official ADK documentation, verified workshop design best practices, and real-world 2026 AI travel agent capabilities*
