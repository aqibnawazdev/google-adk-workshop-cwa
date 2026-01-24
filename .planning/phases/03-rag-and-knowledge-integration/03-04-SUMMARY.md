---
phase: 03-rag-and-knowledge-integration
plan: 04
type: execution
wave: 2
subsystem: reference-implementation
tags: [RAG, VertexAiRagRetrieval, hybrid-agents, coordination, ADK-constraints]
requires: ["03-01:destination-guides", "03-02:corpus-setup", "02-02:async-tools"]
provides: ["rag-tools-module", "hybrid-agent-pattern", "rag-integration-reference"]
affects: ["03-05:workshop-notebook"]
tech-stack:
  added: []
  patterns: [sequential-agent-coordination, single-tool-constraint-workaround, intent-based-routing]
key-files:
  created:
    - workshop-materials/reference-implementation/rag_tools.py
    - workshop-materials/reference-implementation/hybrid_agent.py
  modified:
    - workshop-materials/reference-implementation/agent.py
decisions:
  - context: "ADK constraint: VertexAiRagRetrieval cannot be mixed with function calling tools"
    choice: "Implement sequential coordination pattern with separate specialized agents"
    rationale: "Only viable workaround for providing both real-time booking and static knowledge"
    alternatives: ["Multi-agent orchestration frameworks", "Wait for ADK constraint removal"]
  - context: "RAG tool description clarity for LLM tool selection"
    choice: "Explicit DO/DO NOT sections in tool description"
    rationale: "Prevents LLM from calling RAG for real-time queries or tools for static knowledge"
    alternatives: ["Rely on agent instruction only", "Use tool name hints"]
metrics:
  duration: 10m
  completed: 2026-01-24
---

# Phase 03 Plan 04: RAG Integration for Reference Implementation Summary

**One-liner:** RAG tools with explicit DO/DO NOT descriptions, hybrid agent coordination pattern, and graceful RAG integration in main agent

## Objective Completed

Created complete RAG integration components for the reference implementation:
- RAG tools module with factory function and pre-configured instance
- Hybrid agent module demonstrating ADK constraint workaround
- Updated main agent with RAG integration hooks and documentation

These provide working reference code for Exercise 3 and demonstrate production patterns for combining tools and RAG.

## What Was Built

### 1. RAG Tools Module (rag_tools.py)
**Purpose:** Configure VertexAiRagRetrieval tool with proper descriptions

**Key features:**
- Factory function `create_destination_knowledge_tool()` for flexibility
- Pre-configured `destination_knowledge` instance for convenience
- Explicit DO/DO NOT description preventing tool confusion (Pitfall 5)
- Clear error messages with fix instructions
- Graceful degradation when RAG_CORPUS_ID not set
- Comments explaining ADK single-tool constraint

**Pattern demonstrated:** Pattern 3 from research - proper RAG tool configuration

### 2. Hybrid Agent Module (hybrid_agent.py)
**Purpose:** Coordinate booking and destination agents for comprehensive assistance

**Key features:**
- `create_booking_agent()` - function calling tools only (flights, hotels)
- `create_destination_agent()` - RAG tool only (single-tool constraint)
- `HybridTravelAssistant` class with intent detection and routing
- Destination extraction for automatic enrichment
- Async pattern matching Phase 2 implementation
- Demo showing all query types (booking-only, knowledge-only, mixed)

**Pattern demonstrated:** Pattern 5 from research - sequential agent coordination workaround

**Routing logic:**
1. Knowledge-only query → destination agent
2. Booking query → booking agent (with optional destination enrichment)
3. Ambiguous → booking agent as default

### 3. Main Agent Updates (agent.py)
**Purpose:** Document RAG integration path for Exercise 3

**Changes:**
- Replaced placeholder RAG section with detailed configuration guide
- Dynamic instruction that mentions knowledge base when RAG_CORPUS_ID set
- Added HYBRID ASSISTANT section referencing hybrid_agent.py
- Commented imports showing Exercise 3 progression
- Graceful degradation maintaining booking-only functionality

## Technical Details

### ADK Constraint Workaround

**The Problem:**
ADK's VertexAiRagRetrieval tool cannot be mixed with function calling tools in the same agent instance. This prevents building a single agent with both capabilities.

**The Solution:**
Sequential agent coordination pattern:
```python
# Separate agents
booking_agent = Agent(tools=[search_flights, search_hotels])
destination_agent = Agent(tools=[destination_knowledge])  # RAG only

# Coordinator
class HybridTravelAssistant:
    def assist(query):
        if needs_booking:
            response = booking_agent.run(query)
            if destination_detected:
                tips = destination_agent.run(tip_query)
                return combine(response, tips)
        elif needs_knowledge:
            return destination_agent.run(query)
```

**Why this works:**
- Each agent maintains its own tool constraint
- Coordinator handles routing based on intent detection
- Results can be combined at the coordinator level
- Async pattern allows sequential or parallel execution

### RAG Tool Description Pattern

**Critical for tool selection:**
```python
description='''Retrieve destination information from travel guide knowledge base.

USE THIS TOOL to answer questions about:
- Visa requirements and entry rules (static immigration policy)
- Top attractions and landmarks (guide recommendations)
[... explicit list ...]

DO NOT use this tool for:
- Real-time flight availability → use search_flights() instead
- Real-time hotel availability → use search_hotels() instead
[... explicit exclusions ...]
'''
```

**Without DO/DO NOT:** LLM may call RAG for "Find flights to Tokyo" or call search_flights for "Visa requirements for Tokyo"

**With DO/DO NOT:** Clear boundary between static knowledge (RAG) and real-time data (tools)

## Files Created/Modified

### Created
1. **workshop-materials/reference-implementation/rag_tools.py** (113 lines)
   - Exports: `create_destination_knowledge_tool()`, `destination_knowledge`
   - Dependencies: `google.adk.tools.retrieval.vertex_ai_rag_retrieval`, `vertexai.preview.rag`
   - Environment: `RAG_CORPUS_ID`

2. **workshop-materials/reference-implementation/hybrid_agent.py** (287 lines)
   - Exports: `HybridTravelAssistant`, `hybrid_travel_assistant()`, `create_booking_agent()`, `create_destination_agent()`
   - Dependencies: `tools`, `rag_tools`, `google.adk.agents`, `google.adk.runners`
   - Environment: `MODEL`, `RAG_CORPUS_ID`

### Modified
3. **workshop-materials/reference-implementation/agent.py** (223 lines)
   - Added: RAG corpus configuration section
   - Added: Hybrid assistant reference section
   - Updated: Instruction with dynamic RAG capability
   - Maintains: Backward compatibility (works without RAG_CORPUS_ID)

## Decisions Made

### 1. Sequential Coordination Over Multi-Agent Orchestration
**Context:** ADK constraint prevents mixing RAG and function tools

**Decision:** Implement simple sequential coordination in HybridTravelAssistant class

**Rationale:**
- Workshop-appropriate complexity (participants can understand in 10 minutes)
- No additional framework dependencies
- Demonstrates core pattern that scales to orchestration frameworks
- Matches async pattern from Phase 2

**Alternatives considered:**
- LangGraph orchestration: Too complex for workshop, adds dependency
- Agent-to-Agent (A2A) communication: Not yet standardized in ADK
- Future ADK constraint removal: Can't rely on roadmap timing

### 2. Explicit DO/DO NOT Descriptions
**Context:** LLM needs guidance on when to use RAG vs tools

**Decision:** Include detailed DO/DO NOT sections in RAG tool description

**Rationale:**
- Prevents common tool selection mistakes
- Reinforces Phase 2 teaching (tools for real-time, RAG for static)
- Pattern extends to all tool descriptions (consistency)
- Research Pitfall 5 specifically calls this out

**Alternatives considered:**
- Rely on agent instruction only: Less precise, tools get confused
- Use tool name hints: Too subtle, not reliable
- Post-processing tool selection: Complex, violates agent autonomy

### 3. Graceful Degradation for Missing RAG_CORPUS_ID
**Context:** Reference implementation must work before and after Exercise 3

**Decision:** All RAG components handle missing corpus ID gracefully

**Rationale:**
- Participants can explore code before completing Exercise 3
- Booking functionality works immediately
- Clear error messages guide setup
- Demonstrates production error handling pattern

**Implementation:**
- rag_tools.py: Warning message, destination_knowledge = None
- hybrid_agent.py: create_destination_agent() returns None
- agent.py: Dynamic instruction mentions Exercise 3 coming

## Patterns Demonstrated

### 1. Factory Function Pattern
**File:** rag_tools.py

**Pattern:**
```python
def create_destination_knowledge_tool(
    corpus_id: Optional[str] = None,
    similarity_top_k: int = DEFAULT_TOP_K,
    vector_distance_threshold: float = DEFAULT_THRESHOLD,
) -> VertexAiRagRetrieval:
    """Create configured RAG tool with parameters."""
    ...

# Pre-configured instance
destination_knowledge = create_destination_knowledge_tool()
```

**Benefits:**
- Flexibility for custom configurations
- Convenience for common case
- Testability (can create with mock corpus)
- Exercise 3B teaches parameter tuning

### 2. Intent-Based Routing
**File:** hybrid_agent.py

**Pattern:**
```python
def _detect_intent(query: str) -> tuple[bool, bool]:
    """Keyword-based intent detection."""
    needs_booking = any(kw in query for kw in BOOKING_KEYWORDS)
    needs_knowledge = any(kw in query for kw in KNOWLEDGE_KEYWORDS)
    return needs_booking, needs_knowledge
```

**Benefits:**
- Simple to understand (workshop-appropriate)
- Extensible (add keywords as needed)
- Production path: Replace with NER/classification model
- Demonstrates routing concept for orchestration

### 3. Async Event Streaming
**File:** hybrid_agent.py

**Pattern:**
```python
async def _run_agent(agent: Agent, query: str) -> str:
    """Run agent and extract final response."""
    async for event in runner.run_async(...):
        if event.is_final_response():
            return event.content.parts[0].text
```

**Benefits:**
- Matches Phase 2 pattern (consistency)
- Supports tool call observation
- Production-ready (handles streaming)
- ADK best practice

## Testing Evidence

### Verification Completed
1. ✅ rag_tools.py imports without RAG_CORPUS_ID (graceful degradation)
2. ✅ hybrid_agent.py creates booking agent without RAG (fallback works)
3. ✅ agent.py maintains backward compatibility
4. ✅ No hardcoded corpus IDs (environment variable only)

### File Structure Verification
- rag_tools.py: 113 lines, 1 factory function, 7 RAG_CORPUS_ID references
- hybrid_agent.py: 287 lines, 9 functions, 5 booking_agent references
- agent.py: 223 lines, 9 RAG references, 4 hybrid_agent references

All files exceed minimum line requirements from must_haves.

## Deviations from Plan

None - plan executed exactly as written.

All three modules created with specified features:
- RAG tools module with factory and explicit descriptions
- Hybrid agent with coordination pattern and async
- Main agent with RAG integration documentation

## Next Phase Readiness

### Prerequisites for 03-05 (Workshop Notebook)
✅ **Ready:** All reference implementations complete
- rag_tools.py provides working RAG tool configuration
- hybrid_agent.py demonstrates hybrid pattern
- agent.py shows progressive enhancement path

### Integration Points
1. **Exercise 3A:** Participants explore corpus (03-02 provides corpus)
2. **Exercise 3B:** Configure RAG tool using rag_tools.py as reference
3. **Exercise 3C:** Create RAG-only agent using create_destination_agent() pattern
4. **Exercise 3D:** Test retrieval (corpus has destination guides from 03-01)
5. **Exercise 3E:** Implement hybrid pattern using HybridTravelAssistant as reference

### Documentation Needs for Workshop
- **Pattern explanation:** Why ADK constraint exists, how coordination works
- **Decision flowchart:** Tools vs RAG (when to use each)
- **Troubleshooting:** Common errors and fixes
- **Advanced section:** Multi-agent orchestration frameworks (bonus content)

## Workshop Teaching Points

### Key Concepts to Emphasize
1. **Tools vs RAG distinction:** Real-time (tools) vs static (RAG)
2. **Single-tool constraint:** Why RAG can't mix with function tools
3. **Coordination pattern:** How to work around constraint
4. **Explicit descriptions:** Critical for LLM tool selection
5. **Graceful degradation:** Production error handling

### Code Walkthrough Order
1. Show rag_tools.py → factory pattern, DO/DO NOT descriptions
2. Show create_booking_agent() → familiar from Phase 2
3. Show create_destination_agent() → single-tool constraint
4. Show HybridTravelAssistant routing → intent detection
5. Show assist() method → coordination logic
6. Run demo → see routing in action

### Common Questions to Address
- **Q:** Why can't we just add RAG to the tools list?
  **A:** ADK architecture constraint - show error if attempted

- **Q:** Is coordination pattern production-ready?
  **A:** Yes for simple cases, orchestration frameworks for complex

- **Q:** How do we tune similarity_top_k and threshold?
  **A:** Exercise 3F challenge - experiment with values

## Production Considerations

### Improvements for Real Applications
1. **Intent detection:** Replace keyword matching with NER/classification model
2. **Destination extraction:** Use entity recognition, not dictionary lookup
3. **Error handling:** Add retry logic, timeout handling, circuit breakers
4. **Monitoring:** Track routing decisions, RAG retrieval quality
5. **Orchestration:** Consider LangGraph/other framework for complex routing

### Scaling the Pattern
- **Multiple RAG corpora:** Route to specialized corpus based on query type
- **Caching:** Cache RAG responses for repeated queries
- **A/B testing:** Compare routing strategies
- **Feedback loop:** Track which agent users prefer for different queries

## Links to Research

- **Pattern 3:** VertexAiRagRetrieval tool configuration → implemented in rag_tools.py
- **Pattern 4:** RAG-only agent → create_destination_agent()
- **Pattern 5:** Hybrid agent coordination → HybridTravelAssistant class
- **Pitfall 5:** Vague tool descriptions → explicit DO/DO NOT sections

## Commits

| Task | Commit | Files |
|------|--------|-------|
| 1. Create RAG Tools Module | 3fa1d2f | workshop-materials/reference-implementation/rag_tools.py |
| 2. Create Hybrid Agent Module | 6a94509 | workshop-materials/reference-implementation/hybrid_agent.py |
| 3. Update Main Agent | 3071e57 | workshop-materials/reference-implementation/agent.py |

**Total commits:** 3 (one per task, atomic and revertable)

## Success Metrics

✅ All success criteria met:
- [x] rag_tools.py provides factory function with explicit DO/DO NOT descriptions
- [x] hybrid_agent.py demonstrates ADK constraint workaround
- [x] agent.py gracefully handles missing RAG configuration
- [x] All modules use consistent async pattern from Phase 2
- [x] Error messages include fix instructions
- [x] Comments explain ADK constraint and hybrid pattern rationale

## Time Investment

**Duration:** 10 minutes
**Breakdown:**
- Task 1 (RAG tools): 3 minutes
- Task 2 (Hybrid agent): 4 minutes
- Task 3 (Main agent updates): 2 minutes
- Verification & summary: 1 minute

**Efficiency:** On target for autonomous execution
