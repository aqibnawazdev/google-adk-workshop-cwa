---
phase: 05-workshop-support-materials
plan: 02
subsystem: documentation
tags:
  - context-engineering
  - decision-framework
  - architecture-guidance

dependency_graph:
  requires:
    - phase-02 (function calling tools)
    - phase-03 (RAG integration)
    - phase-04 (session state)
  provides:
    - context engineering decision framework
    - tools vs RAG vs sessions guidance
    - post-workshop architectural decision support
  affects:
    - 05-03 (production readiness may reference)
    - 05-04 (git checkpoints may reference)

tech_stack:
  added: []
  patterns:
    - decision framework documentation
    - ASCII flowchart visualization
    - quick reference card format

key_files:
  created:
    - workshop-materials/CONTEXT-ENGINEERING.md
  modified:
    - workshop-materials/reference-implementation/README.md

decisions:
  - decision: ASCII flowchart for decision tree
    rationale: Works in all markdown renderers, no external dependencies, easy to copy/print
  - decision: Quick Reference Card format at end
    rationale: Printable summary for development use, covers all three approaches
  - decision: 5 common mistakes with corrections
    rationale: Prevents architectural errors, teaches debugging pattern recognition

metrics:
  duration: 2min
  completed: 2026-01-24
---

# Phase 5 Plan 02: Context Engineering Decision Framework Summary

Context engineering decision framework documentation providing scannable decision tables, ASCII flowchart, workshop exercise mappings, common mistake corrections, and post-workshop application guidance.

## What Was Done

### Task 1: Create CONTEXT-ENGINEERING.md with decision framework

Created comprehensive 444-line context engineering guide with:

**1. Introduction** - What context engineering is and why it matters for AI agents

**2. Quick Decision Table** - Scannable in under 30 seconds:
| Question | Tool | RAG | Session |
|----------|------|-----|---------|
| Real-time data? | YES | NO | NO |
| Pre-indexed docs? | NO | YES | NO |
| User preference? | NO | NO | YES |

**3. ASCII Decision Flowchart** - Traceable for any data source:
```
Does this need REAL-TIME data?
    |
   YES --> Use FUNCTION CALLING TOOLS
    |
   NO
    v
Is this STATIC KNOWLEDGE?
    |
   YES --> Use RAG RETRIEVAL
```

**4. Detailed Comparison Table** - Data freshness, latency, cost, setup complexity

**5. Workshop Exercise Mappings**:
- Exercise 2: Function Calling Tools (search_flights, search_hotels)
- Exercise 3: RAG Knowledge Retrieval (destination_knowledge)
- Exercise 4: Session State (user:budget, user:travel_style)

**6. Common Mistakes Section** - 5 mistakes with corrections:
1. Using RAG for real-time data
2. Using tools for static knowledge
3. Storing real-time data in session state
4. Forgetting user preferences
5. Mixing RAG with function tools in same agent

**7. Post-Workshop Application Guide**:
- Step-by-step process for new projects
- Data source classification table
- E-commerce customer service example

**8. Hybrid Patterns** - ADK constraint documentation and coordinator solution

**9. Quick Reference Card** - Printable summary for development use

### Task 2: Add context engineering reference to reference README

Added cross-reference link from the brief inline "Tools vs RAG" framework in README.md to the comprehensive CONTEXT-ENGINEERING.md guide.

## Verification Results

All checks passed:
- File exists: `workshop-materials/CONTEXT-ENGINEERING.md` (444 lines)
- Contains decision table: "Function Calling" column present
- Contains flowchart: "REAL-TIME" decision node present
- Contains common mistakes: "Common Mistakes" section present
- References workshop exercises: "Exercise 2", "Exercise 3", "Exercise 4" mapped
- Reference README updated: Links to `../CONTEXT-ENGINEERING.md`
- Key links validated: References `search_flights`, `search_hotels`, `destination_knowledge`

## Commits

| Hash | Type | Description |
|------|------|-------------|
| c5331c2 | docs | Create context engineering decision framework |
| 5e00b51 | docs | Link reference README to context engineering guide |

## Deviations from Plan

None - plan executed exactly as written.

## Files Changed

```
workshop-materials/
├── CONTEXT-ENGINEERING.md           # NEW: 444 lines
└── reference-implementation/
    └── README.md                    # MODIFIED: +2 lines (cross-reference)
```

## Next Phase Readiness

Ready for 05-03 (Production Readiness Checklist). The context engineering framework provides architectural guidance that the production checklist can build upon.
