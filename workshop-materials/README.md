# Google ADK Workshop: Travel Booking Assistant

Build a production-ready AI agent that can search flights, find hotels, and provide personalized travel recommendations.

## Workshop Overview

**Duration:** 90 minutes
**Level:** Beginner to AI agents (Python experience required)
**What you'll build:** A conversational travel assistant with function calling, knowledge retrieval, and session memory

## Getting Started

### Before the Workshop (Required)

1. **Read the setup guide:** [SETUP.md](./SETUP.md)
2. **Run the verification notebook:** [00-setup-verification.ipynb](./00-setup-verification.ipynb)
3. **Confirm all checks pass** at least 48 hours before workshop

### Workshop Materials

| File | Description | Time |
|------|-------------|------|
| [00-setup-verification.ipynb](./00-setup-verification.ipynb) | Pre-workshop environment check | Pre-work |
| [01-hello-agent.ipynb](./01-hello-agent.ipynb) | Exercise 1: Create your first agent | 15 min |
| [02-tools-functions.ipynb](./02-tools-functions.ipynb) | Exercise 2: Add function calling | 20 min |
| [03-rag-knowledge.ipynb](./03-rag-knowledge.ipynb) | Exercise 3: Integrate knowledge base | 20 min |
| [04-sessions-state.ipynb](./04-sessions-state.ipynb) | Exercise 4: Add session memory | 20 min |

### Falling Behind?

If you need to catch up during the workshop, use our checkpoint branches:

```bash
# Jump to Exercise 2 starting point (with Exercise 1 complete)
git checkout checkpoint/exercise-2
```

See [CHECKPOINTS.md](./CHECKPOINTS.md) for full catch-up instructions and troubleshooting.

### Reference Implementation

See the complete working agent in [reference-implementation/](./reference-implementation/):
- `agent.py` - Full implementation with all features
- `README.md` - Architecture explanation
- `.env.template` - Configuration template

## What You'll Learn

### Exercise 1: Your First Agent
- Create a conversational agent with ADK
- Understand agent configuration (model, name, description, instruction)
- The importance of the `instruction` parameter for agent behavior

### Exercise 2: Function Calling
- Give your agent tools to search for real data
- Implement `search_flights()` and `search_hotels()` functions
- Understand when and how agents call functions

### Exercise 3: RAG Integration
- Connect your agent to a knowledge base
- Retrieve destination information from Vertex AI RAG
- Combine real-time search with static knowledge

### Exercise 4: Sessions & Memory
- Make your agent remember user preferences
- Implement conversation state with Vertex AI Sessions
- Deploy your agent to production

## Context Engineering Focus

This workshop demonstrates **context engineering** - the practice of providing AI agents with the right context to make good decisions:

| Context Type | Example | Exercise |
|--------------|---------|----------|
| Tools (Real-time data) | Flight/hotel search results | Exercise 2 |
| Knowledge (Static data) | Destination guides, visa info | Exercise 3 |
| Memory (Conversation state) | User preferences, budget | Exercise 4 |
| Instructions (Behavior rules) | How to present options | All exercises |

## Troubleshooting

See [SETUP.md](./SETUP.md#troubleshooting) for common issues and solutions.

## Resources

- [Google ADK Documentation](https://google.github.io/adk-docs/)
- [ADK GitHub Repository](https://github.com/google/adk-python)
- [Vertex AI Documentation](https://cloud.google.com/vertex-ai/docs)

---

*Workshop materials for Google ADK v1.23.0*
