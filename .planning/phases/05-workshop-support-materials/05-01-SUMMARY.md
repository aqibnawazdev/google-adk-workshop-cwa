---
phase: 05
plan: 01
subsystem: workshop-support
tags: [troubleshooting, documentation, error-handling, participant-support]
dependency-graph:
  requires: [02-tools-functions.ipynb, 01-hello-agent.ipynb]
  provides: [TROUBLESHOOTING.md, notebook-troubleshooting-links]
  affects: [03-rag-knowledge.ipynb, 04-sessions-state.ipynb]
tech-stack:
  patterns: [symptom-first-organization, error-pattern-classification, quick-index]
key-files:
  created:
    - workshop-materials/TROUBLESHOOTING.md
  modified:
    - workshop-materials/01-hello-agent.ipynb
    - workshop-materials/02-tools-functions.ipynb
decisions:
  - symptom-based-structure: "Errors organized by symptom (what participants see) not by tool/component"
  - 8-pattern-coverage: "8 error categories covering auth, deps, API, async, network, types, RAG, state"
  - preserve-inline: "Keep inline troubleshooting in notebooks for quick help during exercises"
metrics:
  duration: 3min
  completed: 2026-01-24
---

# Phase 5 Plan 1: Centralized Troubleshooting Guide Summary

**One-liner:** Symptom-based troubleshooting guide with 8 error patterns covering auth, dependencies, async, and common ADK issues.

## Completed Tasks

| Task | Description | Commit | Key Changes |
|------|-------------|--------|-------------|
| 1 | Create TROUBLESHOOTING.md with symptom-based structure | 4470c3e | 728-line guide with Quick Index, 8 error patterns |
| 2 | Update notebook checkpoints to reference TROUBLESHOOTING.md | 40a5076 | Added links in 01 setup, 02 troubleshooting sections |

## Summary

Created a centralized troubleshooting guide organized by error symptom (not by tool) to help workshop participants resolve common issues independently.

### Key Deliverables

1. **TROUBLESHOOTING.md** (728 lines)
   - Quick Index mapping error messages to sections
   - 8 error pattern sections with consistent structure:
     - Module Not Found (google.adk, google.generativeai)
     - Authentication Errors (invalid API key, missing credentials)
     - API Access Issues (API not enabled, quota exceeded)
     - Async/Runtime Errors (nested event loop in Colab/Jupyter)
     - Network Issues (timeouts, connection refused)
     - Type/Validation Errors (wrong types, missing returns)
     - RAG Errors (corpus not found, no results)
     - State Errors (missing keys, injection failures)
   - Each pattern includes: Symptom, Common Causes, Resolution Steps, Prevention, If Still Broken
   - Getting More Help section with ADK docs links

2. **Notebook Cross-References**
   - 01-hello-agent.ipynb: Reference in Setup Instructions
   - 02-tools-functions.ipynb: References in two troubleshooting sections
   - Preserves inline troubleshooting for quick help during exercises

### Error Pattern Structure

Each error pattern follows this consistent format:
```markdown
## [Error Category]

### Symptom
[Exact error message participants will see]

### Common Causes
1. [Cause 1]
2. [Cause 2]

### Resolution Steps
1. [Step with code]
2. [Verification step]

### Prevention
[How to avoid this error]

### If Still Broken
[Escalation path or diagnostic commands]
```

## Decisions Made

| Decision | Rationale |
|----------|-----------|
| Symptom-first organization | Participants experience errors as symptoms ("I see ModuleNotFoundError"), not as categories ("ADK issue"). Faster to find solutions. |
| 8 error patterns | Covers the major error categories without overwhelming detail. Balances comprehensiveness with navigability. |
| Preserve inline troubleshooting | Keep quick help in notebooks to reduce context switching. Link to centralized guide for detailed resolution. |
| Getting More Help section | Provides escalation path and official documentation links for issues not covered. |

## Artifacts Created

- `workshop-materials/TROUBLESHOOTING.md` - 728 lines, symptom-based error resolution guide
- Updated `workshop-materials/01-hello-agent.ipynb` - 1 reference to TROUBLESHOOTING.md
- Updated `workshop-materials/02-tools-functions.ipynb` - 2 references to TROUBLESHOOTING.md

## Verification Results

- [x] TROUBLESHOOTING.md exists with 728 lines (requirement: 200+)
- [x] Quick Index at top maps error messages to sections
- [x] 8 error pattern sections with consistent structure
- [x] Contains "ModuleNotFoundError" pattern
- [x] Notebooks cross-reference TROUBLESHOOTING.md
- [x] Inline troubleshooting in notebooks preserved

## Deviations from Plan

None - plan executed exactly as written.

## Next Phase Readiness

Plan 05-01 complete. The troubleshooting guide provides:
- Self-service debugging for common workshop errors
- Consistent error resolution patterns
- Links from notebooks to centralized guide

Ready for subsequent support material plans (context engineering docs, production readiness, etc.).
