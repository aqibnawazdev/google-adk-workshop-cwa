# Pitfalls Research

**Domain:** ADK Workshop for Python Developers
**Researched:** 2026-01-23
**Confidence:** HIGH

## Critical Pitfalls

### Pitfall 1: Treating Agents as "Magic" Without Understanding Fundamentals

**What goes wrong:**
Participants copy code examples without understanding how function calling, context management, or RAG actually works. They leave the workshop able to run demos but unable to debug or extend agents in production.

**Why it happens:**
Python developers new to AI skip fundamentals (how LLMs work, what embeddings are, how context windows function) and jump straight to frameworks like ADK. The 90-minute time constraint pressures instructors to show working code rather than explain concepts.

**How to avoid:**
- Dedicate 10-15 minutes to core concepts before any coding (what agents ARE, how function calling works at the protocol level)
- Include a "what's happening under the hood" slide for each major demo
- Provide a "fundamentals quiz" at the start to identify knowledge gaps
- Create a pre-workshop reading list covering LLM basics

**Warning signs:**
- Participants ask "why didn't it work?" without checking logs or understanding error messages
- Questions like "can I just add more tools?" without understanding tool selection challenges
- Inability to explain what their agent is doing when asked to walk through the code

**Phase to address:**
Phase 1 (Introduction) - Set proper mental models before writing code

---

### Pitfall 2: "Demo-Driven Development" Instead of Production Readiness

**What goes wrong:**
Workshop examples work perfectly in controlled demos but fail immediately in real environments. Participants don't learn about error handling, rate limiting, authentication, or monitoring - then their deployed agents break in production.

**Why it happens:**
90-minute time constraints force instructors to skip "boring" production concerns in favor of impressive demos. According to 2026 data, 65% of organizations pilot agentic AI but only 11% achieve full deployment - this 6x gap exists because pilots don't address production realities.

**How to avoid:**
- Show at least ONE production concern in each module (e.g., add retry logic to function calling demo)
- Include a "Production Checklist" slide covering what's missing from workshop code
- Use a "works in demo, fails in production" example early to set expectations
- Provide post-workshop resources for production hardening

**Warning signs:**
- Participants think their workshop code is production-ready
- No questions about error handling, rate limits, or monitoring
- Surprise when agents fail on unexpected inputs or API errors

**Phase to address:**
Phase 4 (Deployment) - Explicitly contrast workshop demos with production requirements

---

### Pitfall 3: Over-Scoped "God Agents" That Do Everything

**What goes wrong:**
Participants build monolithic agents that handle too many unrelated tasks (support, sales, data analysis, code generation). These agents struggle with context switching, give inconsistent results, and are impossible to debug or improve.

**Why it happens:**
Beginners assume "one agent = one project." They don't understand that specialized agents with focused responsibilities outperform general-purpose agents. The ADK's power makes it easy to add more tools without considering architectural consequences.

**How to avoid:**
- Teach the Coordinator Pattern explicitly (one router agent, multiple specialized agents)
- Show a "bad example" of an over-scoped agent that gives poor results
- Provide a "tool count threshold" rule (>5-7 tools = consider splitting)
- Demonstrate agent-to-agent communication in at least one example

**Warning signs:**
- Participants add 10+ tools to a single agent
- Agent descriptions like "handles all customer needs"
- Inability to explain which agent does what in their architecture

**Phase to address:**
Phase 2 (Function Calling) - Introduce specialization concept when adding tools
Phase 3 (RAG) - Show multi-agent pattern for complex workflows

---

### Pitfall 4: Wrong Embeddings and Context-Destroying Chunking

**What goes wrong:**
RAG implementations return irrelevant results because participants use default chunking (splitting on newlines or character counts) that destroys semantic meaning. They choose embedding models without understanding domain fit or dimensionality tradeoffs.

**Why it happens:**
Most tutorials show "just use text-embedding-004" without explaining why. Beginners don't understand that chunking is a critical design decision, not an implementation detail. They treat RAG as "dump everything in a vector DB" rather than as information retrieval engineering.

**How to avoid:**
- Show a side-by-side comparison: bad chunking vs. semantic chunking (same query, different results)
- Explain embedding model tradeoffs (speed vs. quality, general vs. domain-specific)
- Provide chunking strategies for common content types (code, documentation, conversations)
- Demonstrate why "retrieve and rerank" outperforms pure vector search

**Warning signs:**
- Participants chunk text arbitrarily (every 500 characters) without considering content structure
- No discussion of chunk overlap or boundary considerations
- Expecting RAG to work perfectly on first try without iteration

**Phase to address:**
Phase 3 (RAG) - Deep dive on chunking strategies and embedding selection before implementation

---

### Pitfall 5: Cache-Breaking Patterns That Kill Performance

**What goes wrong:**
Participants add timestamps to system prompts, frequently modify context history, or design prompts that change on every request. This breaks Gemini's prompt caching, causing 100x slower responses and 3-5x higher costs in production.

**Why it happens:**
Developers coming from traditional software expect to include timestamps for logging. They don't understand that LLM context is append-only for performance reasons, and even single-token changes invalidate caches from that point forward.

**How to avoid:**
- Explain prompt caching explicitly and why it matters (show cost/latency math)
- Provide "cache-friendly patterns" (stable prefix, append-only context)
- Show the performance difference: cached vs. uncached request
- Give examples of cache-breaking patterns to avoid (timestamps in system prompt, context reordering)

**Warning signs:**
- Participants add current timestamp to every prompt
- Modifying previous messages in conversation history
- No awareness of why some requests are slow and others instant

**Phase to address:**
Phase 2 (Function Calling) and Phase 3 (RAG) - Address when introducing multi-turn conversations

---

### Pitfall 6: Hiding Errors from Context (Missing "Wrong Turns")

**What goes wrong:**
Participants build agents that retry failed actions infinitely or hide error messages from the model. The agent can't learn from mistakes, repeatedly attempts the same failing approach, and provides no useful debugging information.

**Why it happens:**
Traditional programming teaches "catch exceptions and hide them from users." Developers don't realize that showing failed attempts and error messages to the LLM dramatically improves behavior through implicit belief updating.

**How to avoid:**
- Demonstrate an agent that learns from failures (show failed tool call + error → successful retry with different approach)
- Explain "leave the wrong turns in" as a core pattern
- Show explicit comparison: error hidden vs. error in context
- Teach structured error handling that preserves errors for model but formats them clearly

**Warning signs:**
- Agents retry the same failing action without modification
- Participants catch exceptions and return generic "error occurred" messages
- No conversation history showing failed attempts

**Phase to address:**
Phase 2 (Function Calling) - Demonstrate error handling that includes failure context

---

### Pitfall 7: Session Management Failures and Context Poisoning

**What goes wrong:**
Participants build stateless agents that forget everything between requests, or implement buggy session persistence that corrupts context with hallucinated facts. "Context poisoning" occurs when a bad fact enters the summary and propagates forward, contaminating all future responses.

**Why it happens:**
Session management is complex (storage format conversion, message history validation, summarization quality control) but gets minimal workshop coverage. Beginners treat it as "just store the chat history" without understanding state persistence challenges.

**How to avoid:**
- Show the full session lifecycle: creation → persistence → retrieval → resumption
- Demonstrate context poisoning with an example (bad fact in summary → wrong future answers)
- Provide session validation patterns (message history format checks, tool call/result matching)
- Teach summarization quality control (LLM-as-judge evaluation)

**Warning signs:**
- Agents that restart conversation context on every request
- No validation that retrieved session state is well-formed
- Summarization without quality checks

**Phase to address:**
Phase 3 (RAG) or Phase 4 (Sessions) - Dedicated section on state persistence

---

### Pitfall 8: Time Management Disaster - Running Out of Time for Critical Content

**What goes wrong:**
Instructors spend 40 minutes on setup and basic function calling, then rush through RAG and deployment in the final 20 minutes. Participants leave without understanding the most valuable concepts because they were squeezed into a frantic final section.

**Why it happens:**
Technical workshops commonly fail on time management. Participants have varying setup times, demos encounter unexpected issues, and questions derail the schedule. The 90-minute constraint is unforgiving.

**How to avoid:**
- Pre-workshop environment validation (send setup instructions 48h ahead, confirm all participants have working environments)
- Time-box each section strictly (use visible timer)
- Prepare "quick path" versions of each demo in case of time pressure
- Have backup plan: if setup takes >15min, switch to shared Colab notebook
- Build in 5-minute buffer between major sections

**Warning signs:**
- Participants still installing dependencies at 20 minutes in
- Instructor skipping planned examples "due to time"
- Final section feels rushed or incomplete

**Phase to address:**
Workshop Planning Phase - Create detailed timing breakdown with buffers

---

## Technical Debt Patterns

Shortcuts that seem reasonable but create long-term problems.

| Shortcut | Immediate Benefit | Long-term Cost | When Acceptable |
|----------|-------------------|----------------|-----------------|
| Hardcoded API keys in code | Quick setup | Security vulnerability, hard to rotate | Never (use environment variables always) |
| Using default chunking (split on \n) | Simple implementation | Poor retrieval accuracy | Only for text with clear line boundaries |
| Single monolithic agent | Easier to understand initially | Unmaintainable, poor performance | Only for MVP with <5 tools |
| No error handling in tools | Faster coding during workshop | Production failures, no debugging info | Only in intro examples (add it by phase 2) |
| Synchronous tool execution | Simpler code | Slow responses when tools could run in parallel | When tools have dependencies |
| Using example data instead of real data | Consistent demo results | False sense of working system | During initial concept explanation only |
| Skipping session persistence | Stateless = simpler | Can't maintain multi-turn conversations | Only for single-request agents |
| No logging or monitoring | Faster initial development | Impossible to debug production issues | Never (add basic logging from start) |

## Integration Gotchas

Common mistakes when connecting to external services.

| Integration | Common Mistake | Correct Approach |
|-------------|----------------|------------------|
| Gemini API | Not handling rate limits (429 errors) | Implement exponential backoff, request quotas |
| Vector databases | Storing entire documents as single vectors | Chunk appropriately, store metadata, enable filtering |
| Function calling | Expecting model to execute functions directly | Understand model generates structured data, YOU execute |
| Firebase/Firestore | Assuming real-time updates in workshop timeframe | Use async patterns, handle connection failures |
| External APIs | No timeout configuration | Set reasonable timeouts (5-10s), handle timeout errors |
| Cloud Run | Assuming unlimited cold start patience | Configure min instances or warn about cold starts |
| Vertex AI | Mixing regional endpoints inconsistently | Stick to one region, document which one |

## Performance Traps

Patterns that work at small scale but fail as usage grows.

| Trap | Symptoms | Prevention | When It Breaks |
|------|----------|------------|----------------|
| Loading 50+ tool definitions in prompt | Slow responses, poor tool selection | Use tool routing/filtering, specialized agents | >15-20 tools |
| No prompt caching strategy | Every request slow, high costs | Stable prompt prefix, append-only context | Production scale |
| Synchronous serial tool execution | Agents feel slow for multi-tool tasks | Use ParallelAgent for independent operations | 3+ independent tools needed |
| Retrieving 50 chunks from vector DB | Irrelevant context floods prompt | Retrieve top-k=5-10, use reranking | Context window fills up |
| Full conversation history every request | Token costs spike, latency increases | Implement summarization after N turns | >10-15 conversation turns |
| Eager evaluation of all tools | Wasted API calls, slow startup | Lazy tool loading, evaluate only when needed | >20 tools defined |
| No streaming for long responses | User sees nothing until completion | Stream responses for better UX | Responses >3-4 seconds |

## Security Mistakes

Domain-specific security issues beyond general web security.

| Mistake | Risk | Prevention |
|---------|------|------------|
| Granting agents unrestricted API access | Data loss, unauthorized actions via prompt injection | Scope permissions narrowly, use principle of least privilege |
| No input validation on tool parameters | Agent calls tools with malicious/malformed data | Validate tool inputs before execution, use strong typing |
| Exposing system prompts to users | Attackers learn to manipulate agent behavior | Don't return full conversation history to client |
| No rate limiting per user | DoS via expensive agent operations | Implement per-user rate limits, cost caps |
| Storing PII in vector databases without encryption | Data breach from vector DB compromise | Encrypt sensitive data, consider anonymization |
| Trusting model output for authorization | "The agent said it's okay" = security bypass | Never use model output for authz decisions |
| No audit logging of agent actions | Can't detect or investigate abuse | Log all tool executions with user context |
| Returning sensitive data in function results | Data leakage through conversation history | Filter sensitive fields before passing to model |

## UX Pitfalls

Common user experience mistakes in this domain.

| Pitfall | User Impact | Better Approach |
|---------|-------------|-----------------|
| No indication agent is "thinking" | User assumes it's broken, refreshes page | Show loading states, stream thinking indicators |
| Agent gives different answers to same question | Users lose trust, think agent is broken | Explain probabilistic nature, show confidence levels |
| No way to correct agent mistakes | Frustration when agent misunderstands | Allow explicit corrections, show what agent understood |
| Hiding sources/reasoning | "Where did this come from?" | Cite sources for RAG results, show reasoning chain |
| No fallback when agent is unsure | Hallucinations presented as facts | Detect low confidence, escalate to human or say "I don't know" |
| Long first response (cold start) | Users abandon before seeing results | Explain cold starts, show progress, optimize with min instances |
| No clear scope communication | Users ask out-of-scope questions, get confused | State what agent CAN and CANNOT do upfront |

## "Looks Done But Isn't" Checklist

Things that appear complete but are missing critical pieces.

- [ ] **Function calling demo:** Often missing error handling for API failures — verify tool calls have try/catch and return meaningful errors
- [ ] **RAG implementation:** Often missing reranking step — verify not just retrieving vectors but scoring relevance
- [ ] **Session persistence:** Often missing format validation on restore — verify session loads are checked for well-formed structure
- [ ] **Multi-agent system:** Often missing timeout handling for agent communication — verify agents don't wait forever for responses
- [ ] **Deployment example:** Often missing environment variable configuration — verify API keys aren't hardcoded
- [ ] **Cost monitoring:** Often missing usage tracking — verify can detect runaway costs before $1000 bill arrives
- [ ] **Tool definitions:** Often missing parameter validation schemas — verify tools define types, not just free-form strings
- [ ] **Conversation history:** Often missing size management — verify context doesn't grow unbounded

## Recovery Strategies

When pitfalls occur despite prevention, how to recover.

| Pitfall | Recovery Cost | Recovery Steps |
|---------|---------------|----------------|
| Over-scoped monolithic agent | HIGH | Rewrite as multi-agent system, extract specialized agents, add coordinator |
| Poor chunking strategy | MEDIUM | Re-chunk documents with better strategy, rebuild vector index, evaluate improvement |
| Cache-breaking patterns | LOW | Refactor prompts to stable prefix, stop modifying history, redeploy |
| No error handling | LOW | Add try/catch to tool executions, return errors to model, redeploy |
| Context poisoning in sessions | MEDIUM | Clear affected sessions, add validation on restore, implement summary quality checks |
| Security gaps (unrestricted access) | HIGH | Audit all tool permissions, scope down to minimum required, add authz checks |
| Time management failure (workshop) | MEDIUM | Skip to summary slides, provide recording/materials for skipped content, offer follow-up session |
| Wrong embedding model | MEDIUM | Test alternatives on sample queries, measure retrieval accuracy, switch if >20% improvement |

## Pitfall-to-Phase Mapping

How roadmap phases should address these pitfalls.

| Pitfall | Prevention Phase | Verification |
|---------|------------------|--------------|
| Treating agents as magic | Phase 1: Introduction | Participants can explain how function calling works at protocol level |
| Demo-driven development | Phase 4: Deployment | Workshop includes at least one production concern per module |
| Over-scoped god agents | Phase 2: Function Calling | Examples demonstrate specialized agents, not monoliths |
| Wrong embeddings/chunking | Phase 3: RAG | Show bad vs. good chunking side-by-side comparison |
| Cache-breaking patterns | Phase 2: Function Calling | Explain prompt caching with performance comparison |
| Hiding errors from context | Phase 2: Function Calling | Demo shows error in context → better retry behavior |
| Session management failures | Phase 3: RAG or Sessions | Show full session lifecycle with validation |
| Time management disaster | Workshop Planning | Pre-workshop setup validation, strict time-boxing, backup plans ready |

## Workshop-Specific Gotchas

### Environment Setup Hell

**What happens:**
First 30 minutes consumed by participants struggling with Python versions, API key configuration, dependency conflicts, firewall issues, or missing credentials.

**Prevention:**
- Send setup instructions 48 hours before workshop with verification script
- Require participants to confirm working environment 24h ahead
- Have backup: pre-configured Colab notebooks as fallback
- Test instructions on fresh machine (Mac, Windows, Linux) before workshop
- Provide "environment check" script that validates everything

### The "It Works on My Machine" Demo

**What happens:**
Instructor's carefully crafted demo fails during live workshop due to different API version, rate limiting, network latency, or cached state.

**Prevention:**
- Test ALL demos on fresh environment day-of workshop
- Have pre-recorded backup for critical demos
- Use example data that gives consistent results (not live API calls for core concepts)
- Build in failure demonstrations ("let's see what happens when the API is down")

### Skill Level Variance Chaos

**What happens:**
Half the participants are bored (already know function calling), half are lost (never used async Python). Pacing impossible.

**Prevention:**
- Pre-workshop survey to assess skill levels
- State prerequisites clearly in registration (Python 3.10+, basic async/await knowledge)
- Provide "catch-up" links for participants behind
- Have stretch exercises for participants ahead
- Consider splitting into beginner/intermediate tracks if possible

### Question Avalanche Derailment

**What happens:**
Well-intentioned questions take workshop off track. 45 minutes in, you're debugging a participant's personal project instead of teaching the curriculum.

**Prevention:**
- Set ground rules: "questions on current topic only, sidebar personal issues for breaks"
- Use parking lot technique: capture off-topic questions for end
- Time-box Q&A sections (5 minutes max between major sections)
- Have assistant/TA handle 1-on-1 debugging while workshop continues

### Copy-Paste Without Understanding Syndrome

**What happens:**
Participants copy code from slides without reading it, then can't debug or modify. They leave with a working example they don't understand.

**Prevention:**
- Don't provide complete code upfront (use fill-in-the-blank exercises)
- Ask participants to explain what code does before running it
- Include intentional bugs they must find and fix
- Use "think-pair-share" for code review

## Beginner-Specific AI/Python Mistakes

### Assuming LLM API Calls Are Deterministic

**What happens:**
Participants run same prompt twice, get different results, think their code is broken. They don't understand temperature, sampling, or probabilistic nature of LLMs.

**Prevention:**
- Explain non-determinism upfront with live demonstration
- Show temperature parameter and its effects
- Set expectations: "your output may differ slightly from mine"

### Not Understanding Async/Await in Python

**What happens:**
ADK uses async patterns. Participants unfamiliar with async Python get confused by `await`, event loops, and async function calls.

**Prevention:**
- Include 5-minute async crash course if not prerequisite
- Provide cheat sheet: when to use `await`, what `async def` means
- Use consistent async patterns throughout workshop

### Confusing Model Capabilities (Thinking Models Execute Code)

**What happens:**
Participants think Gemini executes their Python functions directly. They don't understand the model only generates structured data describing what to call.

**Prevention:**
- Draw clear diagram: Model generates JSON → Your code executes → Results go back to model
- Show the JSON function call explicitly (not hidden by SDK)
- Explain "function calling" is a misnomer (should be "function recommendation")

## Sources

### Context Engineering & Agent Development
- [Effective context engineering for AI agents - Anthropic](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)
- [Context Engineering for AI Agents - Manus](https://manus.im/blog/Context-Engineering-for-AI-Agents-Lessons-from-Building-Manus)
- [Common AI Agent Development Mistakes and How to Avoid Them - WildNet Edge](https://www.wildnetedge.com/blogs/common-ai-agent-development-mistakes-and-how-to-avoid-them)
- [Why Most AI Agents Fail in Production - Data Science Collective](https://medium.com/data-science-collective/why-most-ai-agents-fail-in-production-and-how-to-build-ones-that-dont-f6f604bcd075)

### Function Calling & Tool Usage
- [Tool Calling Explained: The Core of AI Agents (2026 Guide) - Composio](https://composio.dev/blog/ai-agent-tool-calling-guide)
- [Malformed Function Call Errors in Multi-Agentic Systems - Medium](https://medium.com/@mukrimenurgumus/malformed-function-call-errors-in-multi-agentic-systems-d7462a33b91b)
- [Function Calling in AI Agents - Prompt Engineering Guide](https://www.promptingguide.ai/agents/function-calling)

### RAG Implementation
- [The Complete Guide to RAG and Vector Databases in 2026 - SolvedByCode](https://solvedbycode.ai/blog/complete-guide-rag-vector-databases-2026)
- [Why you shouldn't use vector databases for RAG - Meilisearch](https://www.meilisearch.com/blog/vector-dbs-rag)
- [RAG vector database limitations - Writer](https://writer.com/engineering/rag-vector-database/)

### Session Management & State
- [Context Engineering - Short-Term Memory Management with Sessions - OpenAI Cookbook](https://cookbook.openai.com/examples/agents_sdk/session_memory)
- [Memory and State in LLM Applications - Arize AI](https://arize.com/blog/memory-and-state-in-llm-applications/)
- [A Field Guide to LLM Failure Modes - Medium](https://medium.com/@adnanmasood/a-field-guide-to-llm-failure-modes-5ffaeeb08e80)

### Production & Deployment
- [The 2025 AI Agent Report: Why AI Pilots Fail in Production - Composio](https://composio.dev/blog/why-ai-agent-pilots-fail-2026-integration-roadmap)
- [AI Agent Deployment: Steps and Challenges in 2026 - AIM Multiple](https://research.aimultiple.com/agent-deployment/)
- [Best Practices for AI Agent Implementations: Enterprise Guide 2026 - OneReach](https://onereach.ai/blog/best-practices-for-ai-agent-implementations/)

### Google ADK Specific
- [Building Collaborative AI: A Developer's Guide to Multi-Agent Systems with ADK - Google Cloud Blog](https://cloud.google.com/blog/topics/developers-practitioners/building-collaborative-ai-a-developers-guide-to-multi-agent-systems-with-adk)
- [Function calling with the Gemini API - Google AI for Developers](https://ai.google.dev/gemini-api/docs/function-calling)
- [Building agents with the ADK and the new Interactions API - Google Developers Blog](https://developers.googleblog.com/building-agents-with-the-adk-and-the-new-interactions-api/)

### Learning & Skill Development
- [7 Biggest Mistakes Freshers Make When Learning AI for Development - TalentSprint](https://talentsprint.com/blog/7-biggest-mistakes-freshers-make-when-learning-AI-for-development)
- [The Realistic Guide to Mastering AI Agents in 2026 - Decoding AI](https://www.decodingai.com/p/realistic-guide-to-ai-agents-in-2026)

---
*Pitfalls research for: ADK Workshop for Python Developers*
*Researched: 2026-01-23*
*Confidence: HIGH (based on official documentation, recent 2026 sources, and established best practices)*
