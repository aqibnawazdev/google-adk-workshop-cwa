---
phase: 03-rag-and-knowledge-integration
plan: 05
type: execution
wave: 3
subsystem: workshop-materials
tags: [RAG, workshop-notebook, VertexAiRagRetrieval, hybrid-agents, exercise-structure]
requires: ["03-01:destination-guides", "03-02:corpus-setup", "03-03:corpus-automation", "03-04:reference-implementation", "02-03:exercise-2-notebook"]
provides: ["exercise-3-notebook", "rag-workshop-materials", "hybrid-pattern-teaching"]
affects: ["04-01:session-management"]
tech-stack:
  added: []
  patterns: [do-not-description-pattern, rag-only-agent, hybrid-coordination, intent-based-routing]
key-files:
  created:
    - workshop-materials/03-rag-knowledge.ipynb
  modified: []
decisions:
  - context: "Notebook structure for teaching RAG concepts"
    choice: "Follow Exercise 2 format with progressive complexity (concept → configure → test → hybrid)"
    rationale: "Consistent workshop experience, participants familiar with pattern from Phase 2"
    alternatives: ["All-at-once approach", "Separate notebooks per exercise"]
  - context: "How to handle ADK single-tool constraint in teaching"
    choice: "Introduce constraint in 3C, solve in 3E with clear architectural diagram"
    rationale: "Participants understand the 'why' before learning the 'how', builds problem-solving mindset"
    alternatives: ["Hide constraint", "Start with hybrid pattern"]
  - context: "Level of code provided vs TODO placeholders"
    choice: "Provide booking tool implementations, TODOs for RAG configuration only"
    rationale: "Focus on RAG concepts (new in Phase 3), not repeating Phase 2 patterns"
    alternatives: ["All TODOs", "All complete code"]
metrics:
  duration: 7m
  completed: 2026-01-24
---

# Phase 03 Plan 05: Exercise 3 Notebook (RAG & Knowledge Integration) Summary

**One-liner:** Complete Exercise 3 notebook teaching RAG integration through 5 progressive exercises with Tools vs RAG decision framework, DO/DO NOT descriptions, and hybrid agent coordination pattern

## Objective Completed

Created comprehensive Exercise 3 notebook (03-rag-knowledge.ipynb) with all exercises 3A-3E plus optional challenge. The notebook teaches RAG concepts through hands-on coding, emphasizing the Tools vs RAG decision framework and demonstrating the hybrid agent pattern for combining function calling with knowledge retrieval.

Total: 36 cells, 443 lines, estimated 40-minute completion time.

## What Was Built

### Exercise 3A: Explore Pre-Indexed RAG Corpus (5 min)
**Purpose:** Introduce RAG corpus structure and layout-aware chunking

**Key content:**
- Pre-indexed corpus explanation (saves 15-20 min setup time)
- 10 destination guides with standardized 10-section structure
- Chunking strategy: 1024 tokens / 256 overlap
- Document AI layout parser importance (preserves tables/lists)
- Corpus ID configuration

**Teaching moment:** Why pre-indexing for workshops (Pattern 1 from research)

### Exercise 3B: Configure RAG Retrieval Tool (7 min)
**Purpose:** Teach VertexAiRagRetrieval configuration with explicit descriptions

**Key content:**
- Parameter table explaining name, description, rag_resources, similarity_top_k, threshold
- DO/DO NOT description pattern (Pattern 3 from research, prevents Pitfall 5)
- Bad vs Good description comparison
- TODO placeholders for participant completion
- Solution cell (collapsed) with complete configuration

**Teaching moment:** Tool descriptions are critical for LLM tool selection

**Code pattern:**
```python
destination_knowledge = VertexAiRagRetrieval(
    name='retrieve_destination_info',
    description='''
    USE THIS TOOL to answer questions about:
    - Visa requirements, attractions, weather, culture...

    DO NOT use this tool for:
    - Real-time flight availability → use search_flights()
    ''',
    rag_resources=[rag.RagResource(rag_corpus=...)],
    similarity_top_k=5,
    vector_distance_threshold=0.6,
)
```

### Exercise 3C: Create RAG-Only Agent (5 min)
**Purpose:** Introduce ADK single-tool constraint

**Key content:**
- ⚠️ Important constraint explanation (cannot mix RAG with function tools)
- Visual comparison: ❌ mixed tools vs ✅ RAG-only
- Agent instruction pattern for RAG-only agent
- TODO placeholders for agent configuration
- Solution cell with complete agent

**Teaching moment:** Understanding constraint before learning workaround builds problem-solving mindset

**Code pattern:**
```python
destination_expert = Agent(
    model='gemini-2.5-flash',
    tools=[destination_knowledge],  # ONLY RAG tool
    instruction='''
    YOUR CAPABILITIES:
    - Retrieve from destination guides

    YOUR LIMITATIONS:
    - Cannot search flights/hotels (no real-time data)

    HOW TO HELP:
    1. Use retrieve_destination_info tool
    2. Combine multiple guide sections
    3. Cite specific details
    '''
)
```

### Exercise 3D: Test RAG Retrieval (8 min)
**Purpose:** Validate retrieval quality and observe RAG in action

**Key content:**
- Helper function using Runner + Sessions pattern (consistent with Phase 2)
- 4 test queries covering different destinations and guide sections:
  1. Visa requirements (Tokyo)
  2. Best time to visit (Paris)
  3. Cultural customs (Tokyo)
  4. Top attractions (NYC)
- Debug output showing tool calls
- Checkpoint explaining what happened (semantic search, chunk retrieval)

**Teaching moment:** Semantic search retrieves relevant chunks even with different wording

### Exercise 3E: Hybrid Agent Pattern (10 min)
**Purpose:** Solve ADK constraint with sequential coordination

**Key content:**
- Architecture diagram showing coordinator routing to specialized agents
- How it works (3-step process):
  1. Intent detection (keyword-based)
  2. Route to agent (booking vs knowledge)
  3. Combine results (enrichment)
- Booking tools provided (from Phase 2)
- Booking agent creation (tools-only)
- Hybrid coordinator function with TODO guidance
- 3 test cases:
  1. Booking with enrichment (flight + tips)
  2. Knowledge-only (culture)
  3. Mixed query (hotel + weather)

**Teaching moment:** Pattern scales to production with NER/classification and orchestration frameworks

**Code pattern:**
```python
async def hybrid_travel_assistant(query):
    # Detect intent
    needs_booking = any(kw in query for kw in BOOKING_KEYWORDS)
    needs_knowledge = any(kw in query for kw in KNOWLEDGE_KEYWORDS)

    # Route
    if needs_knowledge and not needs_booking:
        return await run_agent(destination_expert, query)
    elif needs_booking:
        result = await run_agent(booking_agent, query)
        # Enrich with tips if destination detected
        if destination:
            tips = await run_agent(destination_expert, tip_query)
            return f"{result}\n\n**Tips:**\n{tips}"
    # ...
```

### Challenge (Optional)
**Purpose:** Encourage experimentation and deeper learning

**4 challenges:**
1. Tune retrieval quality (adjust top_k and threshold)
2. Multi-destination query (compare Tokyo vs Paris visas)
3. Edge case handling (query for Mars)
4. Improve intent detection (add destinations, logging)

### Wrap-Up
**Purpose:** Consolidate learning and point to next steps

**Key content:**
- 7 key concepts checklist (RAG vs Tools, constraint, hybrid pattern, etc.)
- Architecture patterns built (RAG-only, function-only, coordinator)
- Production considerations (NER, caching, monitoring)
- What's next (Exercise 4: session management)
- Advanced topics (corpus creation, chunking optimization, metrics)
- Resource links

## Technical Details

### Notebook Structure

Total: 36 cells
- **Markdown cells:** 17 (concept explanations, instructions, checkpoints)
- **Code cells:** 19 (setup, exercises, solutions, tests)

**Cell breakdown:**
- Cells 0-7: Concept + Setup + Exercise 3A (corpus exploration)
- Cells 8-12: Exercise 3B (RAG tool configuration)
- Cells 13-17: Exercise 3C (RAG-only agent)
- Cells 18-24: Exercise 3D (retrieval testing)
- Cells 25-33: Exercise 3E (hybrid pattern)
- Cells 34-35: Challenge
- Cell 36: Wrap-up

### Teaching Patterns Applied

**1. Progressive complexity:**
- 3A: Explore (read-only, no coding)
- 3B: Configure (simple parameter filling)
- 3C: Create agent (familiar pattern from Phase 2)
- 3D: Test (run and observe)
- 3E: Coordinate (complex integration)

**2. TODO-guided coding:**
- Clear TODO comments with hints
- Example structures provided
- Solutions available but collapsed

**3. Instructor notes:**
- HTML comments in markdown cells
- Key teaching moments flagged
- Common pitfalls addressed

**4. Checkpoints:**
- Expected output described
- Troubleshooting guidance
- Verification steps

**5. Visual aids:**
- Decision flowchart (Tools vs RAG)
- Architecture diagram (hybrid coordinator)
- Table comparisons (parameters, patterns)
- Code comparison (❌ bad vs ✅ good)

### Key Patterns Demonstrated

**Pattern 1: Pre-Indexed Corpus** (Research Pattern 1)
- Saves workshop time
- Focuses on usage, not infrastructure
- Instructor setup documented in comments

**Pattern 2: DO/DO NOT Descriptions** (Research Pattern 3, prevents Pitfall 5)
- Explicit tool capabilities
- Clear exclusions
- Critical for LLM tool selection

**Pattern 3: RAG-Only Agent** (Research Pattern 4)
- Single-tool constraint compliance
- Demonstrates limitation before solution

**Pattern 4: Hybrid Coordination** (Research Pattern 5)
- Intent-based routing
- Sequential agent execution
- Result enrichment

**Pattern 5: Async Runner Pattern** (Phase 2 consistency)
- Runner + InMemorySessionService
- runner.run_async() with async for
- event.is_final_response() extraction

## Files Created/Modified

### Created
1. **workshop-materials/03-rag-knowledge.ipynb** (443 lines)
   - 36 cells total
   - 21 TODO placeholders for participant coding
   - 3 solution cells (collapsed)
   - Estimated 40 minutes completion time

### Key Content Metrics
- **Concept introduction:** 2 cells (Tools vs RAG framework)
- **Exercise instructions:** 5 markdown cells (3A-3E)
- **Code exercises:** 5 cells with TODOs
- **Solution cells:** 3 (collapsed, expandable)
- **Test/demo cells:** 8 (retrieval tests, hybrid tests)
- **Checkpoints:** 5 (verification and troubleshooting)
- **Challenge:** 1 cell with 4 challenges
- **Wrap-up:** 1 comprehensive summary

## Decisions Made

### 1. Progressive Exercise Structure Over All-at-Once
**Context:** How to structure RAG teaching in notebook

**Decision:** 5 separate exercises (3A-3E) with increasing complexity

**Rationale:**
- Matches Exercise 2 format (participants familiar with pattern)
- Allows checkpoints between concepts
- Each exercise builds on previous (corpus → tool → agent → test → hybrid)
- Instructor can pace based on participant progress

**Alternatives considered:**
- Single comprehensive exercise: Too overwhelming, no checkpoints
- Separate notebooks: Context switching overhead, harder to reference
- Reverse order (hybrid first): Confusing without understanding constraint

### 2. Introduce Constraint Before Solution
**Context:** When to explain ADK single-tool constraint

**Decision:** Exercise 3C introduces constraint, 3E provides solution

**Rationale:**
- Participants understand the "why" (constraint) before "how" (workaround)
- Builds problem-solving mindset (not just rote coding)
- Makes hybrid pattern feel like a solution, not arbitrary complexity
- Research Pattern 5 explicitly addresses this constraint

**Alternatives considered:**
- Hide constraint: Dishonest, participants discover later in production
- Start with hybrid: Doesn't explain why complexity needed
- Defer to advanced topics: Leaves participants with incomplete solution

### 3. Focus TODOs on RAG, Not Booking Tools
**Context:** What code to provide vs participant-written

**Decision:** Provide complete booking tool implementations, TODOs only for RAG configuration

**Rationale:**
- Phase 3 focus is RAG, not function calling (covered in Phase 2)
- Reduces cognitive load (one new concept at a time)
- Participants already implemented tools in Exercise 2
- More time for RAG-specific learning

**Alternatives considered:**
- All TODOs: Repeats Phase 2, wastes time
- All provided: No hands-on RAG practice
- Import from reference: Participants haven't seen reference yet

## Patterns Demonstrated

### 1. DO/DO NOT Tool Description
**File:** Cell 9 (Exercise 3B)

**Pattern:**
```python
description='''
USE THIS TOOL to answer questions about:
- [explicit list of capabilities]

DO NOT use this tool for:
- [explicit list of exclusions with alternatives]
'''
```

**Benefits:**
- Prevents LLM from calling RAG for real-time queries
- Prevents LLM from calling tools for static knowledge
- Clear boundary between tools and RAG
- Production-ready pattern

### 2. Hybrid Coordinator with Intent Detection
**File:** Cell 28 (Exercise 3E)

**Pattern:**
```python
def hybrid_assistant(query):
    # Keyword-based intent detection
    needs_booking = any(kw in query for kw in BOOKING_KW)
    needs_knowledge = any(kw in query for kw in KNOWLEDGE_KW)

    # Route to specialized agent
    if needs_knowledge and not needs_booking:
        return destination_agent(query)
    elif needs_booking:
        result = booking_agent(query)
        # Optional enrichment
        if destination:
            tips = destination_agent(tip_query)
            return combine(result, tips)
```

**Benefits:**
- Workshop-appropriate complexity (keyword matching)
- Demonstrates routing concept
- Shows result enrichment pattern
- Scales to NER/classification in production

### 3. Test-Driven RAG Validation
**File:** Cells 19-23 (Exercise 3D)

**Pattern:**
```python
test_queries = [
    "Visa requirements for Japan",
    "Best time to visit Paris",
    "Cultural customs in Tokyo",
    "Top attractions NYC"
]

for query in test_queries:
    response = agent(query)
    # Verify tool call, relevance, citations
```

**Benefits:**
- Validates retrieval quality
- Covers multiple destinations and guide sections
- Teaches evaluation thinking
- Production pattern (test suite for RAG)

## Testing Evidence

### Verification Completed
1. ✅ 36 cells total (exceeds 26+ target)
2. ✅ 443 lines (exceeds 400 minimum from must_haves)
3. ✅ 21 TODO placeholders for participant coding
4. ✅ 3 solution cells (collapsed, expandable)
5. ✅ All required terms present:
   - VertexAiRagRetrieval ✓
   - hybrid ✓
   - DO NOT use this tool for ✓
   - single-tool constraint ✓
   - Tools vs RAG ✓

### Content Quality Checks
- **Concept introduction:** Tools vs RAG decision framework with flowchart
- **Exercise 3A:** Corpus structure, layout parsing, pre-indexing rationale
- **Exercise 3B:** DO/DO NOT pattern with bad vs good comparison
- **Exercise 3C:** Single-tool constraint explanation and workaround preview
- **Exercise 3D:** 4 test queries across destinations and guide sections
- **Exercise 3E:** Hybrid pattern with architecture diagram and 3 tests
- **Instructor notes:** HTML comments in 5 cells flagging teaching moments
- **Checkpoints:** 5 verification sections with troubleshooting
- **Challenge:** 4 optional extensions encouraging experimentation

### Structure Verification
- Follows Exercise 2 format (consistent participant experience)
- Progressive complexity (explore → configure → create → test → integrate)
- Each exercise has introduction, code, checkpoint
- Solutions collapsed (available but not distracting)
- Estimated time: 40 minutes (within 45-minute target)

## Deviations from Plan

None - plan executed exactly as written.

All specified components delivered:
- Exercise 3A: Corpus exploration ✓
- Exercise 3B: RAG tool configuration with TODOs ✓
- Exercise 3C: RAG-only agent with constraint explanation ✓
- Exercise 3D: Testing with 4+ test queries ✓
- Exercise 3E: Hybrid pattern with coordinator ✓
- Challenge: Optional extensions ✓
- Wrap-up: Summary and next steps ✓

## Next Phase Readiness

### Prerequisites for 03-06
✅ **Complete:** Exercise 3 notebook provides full RAG teaching materials

**What's delivered for next plan:**
- Complete notebook ready for workshop delivery
- All exercises follow established format
- TODO placeholders guide participant coding
- Solutions available for instructor reference
- Checkpoints enable pacing and troubleshooting

### Integration with Other Plans
- **03-01/03-02:** Destination guides referenced in corpus exploration (3A)
- **03-03:** Corpus setup automation enables pre-workshop indexing (3A)
- **03-04:** Reference implementation patterns demonstrated in solutions
- **02-03:** Exercise 2 format consistency, booking tools reused (3E)

### Workshop Delivery Readiness
✅ **Instructor materials:**
- HTML comments flag teaching moments
- Checkpoints describe expected output
- Troubleshooting guidance for common issues
- Time estimates per exercise (40 min total)

✅ **Participant materials:**
- Clear learning objectives
- Progressive exercise structure
- TODO placeholders with hints
- Solutions for self-check
- Challenge extensions for fast finishers

### Documentation Needs
- **README update:** Add Exercise 3 to workshop sequence (Phase 5)
- **Instructor guide:** Timing, key concepts, common questions (Phase 5)
- **Troubleshooting:** RAG-specific errors (corpus ID, retrieval failures) (Phase 5)

## Workshop Teaching Points

### Key Concepts to Emphasize

1. **Tools vs RAG Decision Framework** (Exercise 3A)
   - Real-time data (changes while talking) → tools
   - Static knowledge (guides, policies) → RAG
   - Show flowchart, give examples

2. **DO/DO NOT Description Pattern** (Exercise 3B)
   - LLM reads description to select tool
   - Vague descriptions cause confusion
   - Explicit boundaries critical

3. **Single-Tool Constraint** (Exercise 3C)
   - ADK limitation, not design choice
   - Solution in 3E (hybrid pattern)
   - Production pattern: specialized agents

4. **Semantic Search** (Exercise 3D)
   - Retrieval by meaning, not keywords
   - Similarity threshold filters quality
   - Chunks provide context for answer

5. **Hybrid Coordination** (Exercise 3E)
   - Intent detection routes queries
   - Sequential execution of specialized agents
   - Result enrichment combines capabilities

### Common Questions to Address

**Q:** Why can't we just add RAG to tools list?
**A:** ADK architecture constraint. Show error if attempted. Solution is hybrid pattern with specialized agents.

**Q:** How does semantic search work?
**A:** Query → embedding vector, compare with chunk embeddings, cosine similarity, top K results above threshold.

**Q:** When should we use RAG vs fine-tuning?
**A:** RAG for dynamic knowledge (frequent updates), fine-tuning for behavior/style. Often combine both.

**Q:** What if retrieval returns wrong chunks?
**A:** Tune similarity_top_k and threshold (Challenge 1), improve chunking strategy, add metadata filtering.

**Q:** How do we test retrieval quality?
**A:** Manual validation (Exercise 3D), automated metrics (faithfulness, relevance - Advanced Topics), A/B testing in production.

### Instructor Facilitation Tips

**Exercise 3A (5 min):**
- Show corpus in Google Cloud Console if possible
- Explain why pre-indexing (saves 15-20 min)
- Preview destination guide structure

**Exercise 3B (7 min):**
- Live-code the description together
- Show bad vs good examples
- Ask participants to suggest DO/DO NOT items

**Exercise 3C (5 min):**
- Emphasize constraint before revealing solution
- Ask: "How would you solve this?"
- Preview 3E as the answer

**Exercise 3D (8 min):**
- Run first query together, explain output
- Participants run remaining queries
- Discuss retrieval quality observations

**Exercise 3E (10 min):**
- Draw architecture diagram on whiteboard
- Walk through intent detection logic
- Run Test 1 together (booking + enrichment)
- Participants complete Tests 2-3

**Pacing:**
- Fast finishers: Challenge exercises
- Struggling participants: Provide more hints, pair programming
- Time buffer: Wrap-up discussion, preview Exercise 4

## Production Considerations

### Workshop Simplifications

**What we used:**
- Keyword-based intent detection
- Dictionary-based destination extraction
- Sequential agent execution
- Single RAG corpus (all guides together)

**Production needs:**
- NER or classification model for intent
- Entity recognition for destinations
- Parallel agent execution (async)
- Multiple corpora (guides, policies, FAQs)
- Caching for repeated queries
- Monitoring: retrieval latency, quality metrics

### Scaling the Patterns

**Hybrid coordinator:**
- Workshop: 2 agents (booking, destination)
- Production: N specialized agents (visa, transport, events)
- Orchestration framework (LangGraph, custom router)

**RAG retrieval:**
- Workshop: Single corpus, default params
- Production: Multi-corpus with metadata filtering
- Tuned chunk size per content type
- A/B testing retrieval params

**Intent detection:**
- Workshop: Keyword matching
- Production: Fine-tuned classifier
- Confidence scores for routing
- Fallback to human escalation

### Evaluation and Monitoring

**Workshop teaches:**
- Manual validation (Exercise 3D)
- Observing tool calls
- Checking answer relevance

**Production requires:**
- Automated RAG metrics (faithfulness, relevance, citation coverage)
- Latency monitoring (retrieval + generation)
- User feedback loops
- A/B testing coordinator strategies

## Links to Research

### Patterns from 03-RESEARCH.md Implemented

- **Pattern 1:** Pre-indexed corpus (Exercise 3A) - saves workshop time
- **Pattern 2:** Layout-aware chunking (Exercise 3A explanation)
- **Pattern 3:** VertexAiRagRetrieval configuration (Exercise 3B)
- **Pattern 4:** RAG-only agent (Exercise 3C)
- **Pattern 5:** Hybrid agent coordination (Exercise 3E)
- **Pattern 6:** Destination guide structure (Exercise 3A content)

### Pitfalls Addressed

- **Pitfall 1:** Single-tool constraint explained in Exercise 3C
- **Pitfall 2:** Layout parser importance in Exercise 3A
- **Pitfall 3:** Pre-indexing in Exercise 3A (not during workshop)
- **Pitfall 4:** Threshold filtering in Exercise 3B parameters
- **Pitfall 5:** DO/DO NOT descriptions in Exercise 3B
- **Pitfall 6:** Test queries in Exercise 3D
- **Pitfall 7:** Tools vs RAG flowchart in Exercise 3A

## Commits

| Task | Commit | Files |
|------|--------|-------|
| 1. Create Exercise 3 Concept Introduction and Setup | 263da45 | workshop-materials/03-rag-knowledge.ipynb |
| 2. Add Exercise 3B-3C (RAG Tool Configuration and Agent) | 22e574a | workshop-materials/03-rag-knowledge.ipynb |
| 3. Add Exercise 3D-3E, Challenge, and Wrap-up | 2464a52 | workshop-materials/03-rag-knowledge.ipynb |

**Total commits:** 3 (one per task, atomic and revertable)

## Success Metrics

✅ All success criteria met:
- [x] Notebook follows existing format from 02-tools-functions.ipynb
- [x] All 5 exercises (3A-3E) plus challenge included
- [x] Clear TODO placeholders for participant coding (21 found)
- [x] Complete solutions in collapsed cells (3 solution cells)
- [x] Instructor notes in HTML comments (5 cells)
- [x] Decision flowchart for Tools vs RAG (Exercise 3A)
- [x] Test queries cover multiple destinations (Tokyo, Paris, NYC, Singapore)
- [x] Hybrid pattern fully demonstrated (Exercise 3E)
- [x] Total estimated time ~40 minutes (within 45-minute target)

## Time Investment

**Duration:** 7 minutes (403 seconds)
**Breakdown:**
- Task 1 (Concept + setup + 3A): 2 minutes
- Task 2 (3B-3C RAG configuration): 2 minutes
- Task 3 (3D-3E testing + hybrid + wrap-up): 2 minutes
- Verification & summary: 1 minute

**Efficiency:** Excellent - autonomous execution with no blockers
