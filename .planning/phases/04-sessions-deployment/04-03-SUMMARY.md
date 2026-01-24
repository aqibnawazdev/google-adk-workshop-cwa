---
phase: 04-sessions-deployment
plan: 03
subsystem: infra
tags: [vertex-ai, agent-engine, deployment, production]

# Dependency graph
requires:
  - phase: 04-01 and 04-02
    provides: Reference implementation with agent, tools, and state management
provides:
  - Deployment guide for Vertex AI Agent Engine
  - Automated deployment script with CLI interface
  - Post-workshop self-paced exploration materials
affects: [05-support-materials, instructor-preparation]

# Tech tracking
tech-stack:
  added: [vertexai.agent_engines, AdkApp]
  patterns: [agent-engine-deployment, staging-bucket, cleanup-billing]

key-files:
  created:
    - workshop-materials/DEPLOYMENT.md
    - workshop-materials/reference-implementation/deploy.py
  modified: []

key-decisions:
  - "Post-workshop deployment focus - impractical for hands-on during 15-minute allocation"
  - "Instructor demonstration model - deploy.py enables live demo"
  - "Cleanup prominence - cost awareness for participants"

patterns-established:
  - "agent_engines.create for ADK deployment"
  - "async_stream_query for deployed agent queries"
  - "Environment variable configuration (GOOGLE_CLOUD_PROJECT, STAGING_BUCKET)"

# Metrics
duration: 2min
completed: 2026-01-24
---

# Phase 4 Plan 3: Vertex AI Agent Engine Deployment Summary

**Comprehensive deployment guide and automation script for Vertex AI Agent Engine with instructor demo support and post-workshop self-paced exploration**

## Performance

- **Duration:** 2 min
- **Started:** 2026-01-24T14:01:30Z
- **Completed:** 2026-01-24T14:03:45Z
- **Tasks:** 2
- **Files created:** 2

## Accomplishments

- Created 436-line DEPLOYMENT.md with complete deployment workflow
- Created 335-line deploy.py with CLI automation for deploy/test/cleanup
- Prerequisites documented: GCP project, APIs, bucket, IAM
- Troubleshooting table covers 8 common deployment errors
- Cost considerations section with cleanup instructions prominently featured
- Both files cross-reference each other for discoverability

## Task Commits

Each task was committed atomically:

1. **Task 1: Create DEPLOYMENT.md guide** - `fbf683b` (docs)
2. **Task 2: Create deploy.py script** - `efc8224` (feat)

## Files Created/Modified

- `workshop-materials/DEPLOYMENT.md` - Complete deployment guide with prerequisites, steps, troubleshooting, costs
- `workshop-materials/reference-implementation/deploy.py` - CLI tool for deploy/test/cleanup/list actions

## Decisions Made

1. **Post-workshop deployment focus** - Deployment is impractical for hands-on during 15-minute workshop allocation; guide designed for self-paced exploration afterward
2. **Instructor demonstration model** - deploy.py enables live demonstration during workshop without requiring participant GCP setup
3. **Cleanup prominence** - Cost awareness is critical; cleanup instructions appear in multiple sections and script confirmation prompt
4. **us-central1 default** - Most commonly available region with good quota availability

## Deviations from Plan

None - plan executed exactly as written.

## Issues Encountered

None - straightforward documentation and script creation.

## User Setup Required

None - no external service configuration required during plan execution. Participants who wish to deploy post-workshop will need GCP project setup as documented in DEPLOYMENT.md.

## Next Phase Readiness

- Deployment materials complete for instructor demonstration
- deploy.py ready for workshop demo flow
- Participants have comprehensive post-workshop guide
- INFRA-07 learning objective addressed

**Next plans:** 04-04 (Session Management Notebook) and 04-05 (Session Management Reference Docs)

---
*Phase: 04-sessions-deployment*
*Completed: 2026-01-24*
