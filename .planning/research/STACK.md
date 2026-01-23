# Stack Research

**Domain:** Google ADK Workshop (Travel Booking Agent)
**Researched:** 2026-01-23
**Confidence:** HIGH

## Recommended Stack

### Core Technologies

| Technology | Version | Purpose | Why Recommended |
|------------|---------|---------|-----------------|
| Python | 3.11 or 3.12 | Runtime language for workshop and agent | Google ADK requires Python >=3.10. Python 3.11/3.12 offer 10-60% performance gains, better error messages, full compatibility with AI libraries, and are the sweet spot for 2026. Python 3.9 support will be deprecated by Google Cloud SDK on January 27, 2026. |
| google-adk | 1.23.0 | Agent development framework | Latest stable release (Jan 22, 2026). Production-ready v1.0+ framework optimized for Gemini and Google Cloud. Code-first approach makes agent development feel like software development. |
| google-cloud-aiplatform | >=1.112 | Vertex AI SDK for deployment | Required for deploying agents to Vertex AI Agent Engine. Install with: `pip install google-cloud-aiplatform[agent_engines,adk]>=1.112`. Client-based design introduced in v1.112. |
| Gemini 2.5 Flash | gemini-2.5-flash | LLM for agent reasoning | Recommended model for ADK agents in 2026. Gemini 2.0 Flash is deprecated (shutdown March 31, 2026). Gemini 3 Flash is also available but 2.5 Flash is stable and well-documented. |

### Supporting Libraries

| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| python-dotenv | latest | Environment variable management | Required for storing API keys and credentials in .env files. Standard practice for 12-factor apps. Auto-loads GOOGLE_API_KEY, PROJECT_ID, etc. |
| pytest | latest | Testing and evaluation | ADK provides AgentEvaluator class for pytest integration. Use for CI/CD pipeline testing, conversation-based evaluation with golden datasets. |
| asyncio | built-in (3.11+) | Asynchronous execution | Required for ADK agent operations. Use `await` in notebooks, `asyncio.run()` in scripts. |
| Flask | 3.x (optional) | Workshop web interface | Optional for creating custom web UIs. ADK provides built-in `adk web` command (development only). For production, FastAPI is recommended over Flask. |

### Development Tools

| Tool | Purpose | Notes |
|------|---------|-------|
| Google Cloud SDK (gcloud CLI) | GCP authentication and deployment | Requires Python 3.10-3.14. Use `gcloud auth login` and `gcloud auth application-default login` for setup. Updated regularly through 2026. |
| ADK CLI | Agent scaffolding and execution | Installed with google-adk. Commands: `adk create`, `adk run`, `adk web`, `adk eval`, `adk deploy`. |
| Google Colab | Workshop delivery platform | Free tier with GPU/TPU access. Official ADK Crash Course uses 2 Colab notebooks. Supports asyncio natively. Perfect for 90-minute workshops. |
| Jupyter Notebook | Local development alternative | Alternative to Colab for local environments. ADK examples work in both Colab and Jupyter. |
| Google AI Studio | API key generation | Free tier for Gemini API keys at https://aistudio.google.com/app/apikey. Use for non-production workshop environments. |
| Git/GitHub | Version control | Standard for distributing workshop materials and sample code. Google maintains adk-samples repository. |

## Installation

```bash
# Create virtual environment (recommended)
python3.11 -m venv .venv
source .venv/bin/activate  # Linux/Mac
# .venv\Scripts\activate.bat  # Windows CMD

# Core ADK installation
pip install google-adk==1.23.0

# Vertex AI SDK with ADK support (for deployment)
pip install google-cloud-aiplatform[agent_engines,adk]>=1.112

# Supporting libraries
pip install python-dotenv pytest

# Optional: Flask for custom web interface
pip install flask>=3.0

# Google Cloud SDK (separate installation)
# Download from: https://cloud.google.com/sdk/docs/install-sdk
```

## Alternatives Considered

| Recommended | Alternative | When to Use Alternative |
|-------------|-------------|-------------------------|
| google-adk | LangChain | Use LangChain if team already has LangChain expertise or needs framework-agnostic approach. ADK is better for Google Cloud-first workshops. |
| google-adk | LlamaIndex | Use LlamaIndex if primary focus is RAG/document retrieval. ADK provides RAG tools but LlamaIndex specializes in it. |
| google-adk | AG2 (AutoGen) | Use AG2 for multi-agent communication patterns. ADK supports multi-agent but AG2 has more mature agent-to-agent protocols. |
| Gemini 2.5 Flash | Gemini 3 Flash | Use Gemini 3 Flash (latest) for cutting-edge performance (78% on SWE-bench Verified). Use 2.5 Flash for stability and better documentation. |
| Google Colab | Local Jupyter | Use local Jupyter if workshop has network restrictions or data privacy requirements. Colab is easier for participant setup (no installation). |
| FastAPI | Flask | Use FastAPI for production deployments (ADK docs recommend it). Flask is simpler for teaching REST API concepts in workshops. |
| Vertex AI Agent Engine | Cloud Run | Use Cloud Run for full control over scaling and infrastructure. Use Agent Engine for simplest managed deployment (recommended for workshops). |
| Markdown | Jupyter Book / Sphinx | Use Jupyter Book for executable documentation. Markdown is simpler for tutorial-style workshop materials. |

## What NOT to Use

| Avoid | Why | Use Instead |
|-------|-----|-------------|
| Python 3.9 or earlier | Google Cloud SDK deprecating Python 3.9 support on Jan 27, 2026. Python 3.7 is EOL. | Python 3.11 or 3.12 |
| Gemini 2.0 Flash | Deprecated, shutdown on March 31, 2026 | Gemini 2.5 Flash or Gemini 3 Flash |
| google-adk < 1.0 | Pre-production versions lack stability guarantees | google-adk >= 1.23.0 |
| Custom context management | ADK's context engineering framework is production-tested and handles sessions, memory, state automatically | Use ADK's Session, State, and Memory Bank |
| Manual tool registration | Error-prone and verbose | Use ADK's built-in tools (Google Search, Code Execution, RAG) and McpToolset for MCP integration |
| adk web in production | Development-only web interface, not production-ready | FastAPI or deploy to Vertex AI Agent Engine |
| Plain Flask deployment | Requires significant boilerplate for agent integration | Use ADK's API Server or deploy to Agent Engine |

## Stack Patterns by Variant

### Workshop Delivery Stack (90-minute hands-on)

**Recommended Pattern:**
- Google Colab notebooks for exercises (no local installation required)
- Markdown README for setup instructions
- Pre-provisioned GCP accounts with Vertex AI API enabled
- GitHub repository with sample code and solutions
- Live demo using `adk web` for quick visualization
- Deployment exercise using `adk deploy agent_engine`

**Why:**
- Zero-install setup for participants (Colab handles everything)
- Pre-provisioned accounts avoid billing setup time
- Markdown is simple, version-controllable, and widely supported
- ADK CLI commands are beginner-friendly
- 90 minutes requires minimal setup friction

### Agent Implementation Stack (what participants build)

**Core Pattern:**
```
travel_agent/
├── .env                    # API keys, project config
├── __init__.py            # Python package marker
├── agent.py               # Main agent logic
├── requirements.txt       # Dependencies
└── tests/
    └── test_agent.py      # pytest tests
```

**Components:**
- ADK Agent with custom tools (flight search, hotel search, activity lookup)
- Gemini 2.5 Flash for reasoning
- Session management for user preferences (budget, dates, travelers)
- RAG integration with Vertex AI RAG Engine for destination knowledge
- Function calling for booking APIs (simulated or sandbox APIs)
- Deploy to Vertex AI Agent Engine

**Why:**
- Simple project structure (4-5 files)
- Demonstrates all required concepts: tools, RAG, sessions, deployment
- Can complete in 90 minutes with pre-built tool templates
- Real deployment experience without complex infrastructure

### Advanced Workshop Extension Stack (optional)

**If extending beyond 90 minutes:**
- MCP Toolbox for Databases (connect to real travel inventory DB)
- Multi-agent architecture (Inspiration Agent, Planning Agent, Booking Agent)
- FastAPI REST interface for custom frontend
- Agent evaluation with pytest and golden datasets
- Cloud Run deployment for production-like experience

**Why:**
- Shows production patterns
- Demonstrates ADK's advanced capabilities
- MCP integration is 2026 best practice for tool interoperability

## Version Compatibility

| Package A | Compatible With | Notes |
|-----------|-----------------|-------|
| google-adk@1.23.0 | Python 3.10-3.14 | Officially supports 3.10, 3.11, 3.12, 3.13, 3.14 |
| google-adk@1.23.0 | Gemini 2.5 Flash, 3.0 Flash, 3.0 Pro | Model-agnostic but optimized for Gemini family |
| google-cloud-aiplatform@1.112+ | google-adk@1.23.0 | Use `[agent_engines,adk]` extras for full compatibility |
| pytest | google-adk@1.23.0 | Use AgentEvaluator from google.adk.evaluation.agent_evaluator |
| Python 3.11/3.12 | Google Cloud SDK (2026) | SDK requires Python 3.10-3.14 as of Jan 2026 |
| ADK McpToolset | MCP servers | Supports any MCP-compliant server (MCP Toolbox, custom MCP servers) |

## Workshop-Specific Stack Decisions

### Workshop Infrastructure

| Technology | Version | Purpose | Rationale |
|------------|---------|---------|-----------|
| Google Colab | N/A (hosted) | Notebook environment | Free tier with generous compute. No installation. Supports ADK asyncio patterns. Official ADK tutorials use Colab. |
| Markdown | N/A | Tutorial documentation | Simple, portable, version-controllable. Supported in GitHub, Colab, Jupyter. Easy for participants to follow. |
| GitHub | N/A | Code distribution | Industry standard. Participants can fork and extend. Version control for workshop iterations. |
| Pre-provisioned GCP Projects | N/A | Participant accounts | Eliminates billing setup (15-20 min savings). Ensures quota limits. Prevents cost surprises. |

### Travel Booking Agent Specifics

| Component | Technology | Rationale |
|-----------|-----------|-----------|
| Flight search tool | Custom ADK tool with mock API | Real flight APIs require complex auth. Mock API demonstrates tool pattern without API complexity. |
| Hotel search tool | Google Maps Places API | Free tier available. Real-world API. Teaches ADK + external API integration. |
| Destination knowledge | Vertex AI RAG Engine | Demonstrates RAG pattern. Pre-built ADK tool. Can pre-load with travel guides PDF. |
| User preferences | ADK Session State | Built-in session management. Persistent across conversation. Core ADK pattern. |
| Booking confirmation | Custom ADK tool with simulation | Real booking APIs require payment processors. Simulation demonstrates tool orchestration. |

### Rationale Summary

**Why Google Colab over local Jupyter:**
- 90-minute constraint eliminates time for local Python/package setup
- Free GPU/TPU if participants want to experiment post-workshop
- Consistent environment (no "works on my machine" issues)
- Pre-installed common libraries reduce pip install time

**Why Markdown over Jupyter Book:**
- Jupyter Book requires Sphinx, theme configuration, build step
- Markdown renders natively in GitHub and Colab
- Simpler for workshop maintainers to update
- Participants can read on GitHub without cloning

**Why Gemini 2.5 Flash over 3.0 Flash:**
- More stable (3.0 is very new)
- Better documentation and examples
- Lower latency for workshop exercises
- 3.0 can be mentioned as "what's next" in workshop conclusion

**Why FastAPI mentioned but Flask acceptable:**
- ADK official docs recommend FastAPI for production
- Flask is simpler to explain in 90 minutes
- If workshop includes REST API module, Flask is adequate for teaching
- Production guidance should mention FastAPI migration path

**Why pytest over unittest:**
- ADK provides native AgentEvaluator integration with pytest
- Industry standard for Python testing
- Simpler syntax for beginners
- Async test support with pytest-asyncio

**Why Vertex AI Agent Engine over Cloud Run:**
- One command deployment: `adk deploy agent_engine`
- No container knowledge required
- Free tier: 50 hours vCPU + 100 hours RAM monthly
- Appropriate for workshop scope
- Cloud Run can be mentioned for "production" discussion

## Sources

### HIGH Confidence Sources (Official Documentation)

- [Google ADK Official Documentation](https://google.github.io/adk-docs/) - Complete framework documentation
- [google-adk PyPI Package](https://pypi.org/project/google-adk/) - Version 1.23.0 release (Jan 22, 2026)
- [Vertex AI Agent Builder Overview](https://docs.cloud.google.com/agent-builder/agent-development-kit/overview) - Official Google Cloud docs
- [ADK Python Quickstart](https://google.github.io/adk-docs/get-started/python/) - Setup and installation requirements
- [Gemini Models Documentation](https://google.github.io/adk-docs/agents/models/google-gemini/) - ADK Gemini integration
- [Google Cloud SDK Release Notes](https://docs.cloud.google.com/sdk/docs/release-notes) - gcloud CLI version tracking
- [Vertex AI Pricing](https://cloud.google.com/vertex-ai/pricing) - Free tier and pricing details

### MEDIUM Confidence Sources (Official Tutorials and Examples)

- [ADK Crash Course Codelab](https://codelabs.developers.google.com/onramp/instructions) - Official 2-notebook workshop
- [Travel Agent MCP Toolbox Codelab](https://codelabs.developers.google.com/travel-agent-mcp-toolbox-adk) - Travel agent example
- [Building AI Agents with ADK Foundation](https://codelabs.developers.google.com/devsite/codelabs/build-agents-with-adk-foundation) - Foundational tutorial
- [ADK API Server Documentation](https://google.github.io/adk-docs/runtime/api-server/) - API server implementation
- [ADK Tools Documentation](https://google.github.io/adk-docs/tools/) - Built-in tools reference
- [ADK Deployment Guide](https://google.github.io/adk-docs/deploy/agent-engine/deploy/) - Vertex AI deployment steps
- [ADK Session Management](https://google.github.io/adk-docs/sessions/) - Context, state, and memory patterns
- [ADK MCP Integration](https://google.github.io/adk-docs/mcp/) - Model Context Protocol support
- [Google ADK GitHub Repository](https://github.com/google/adk-python) - Source code and examples
- [Google ADK Samples Repository](https://github.com/google/adk-samples) - Sample agents

### MEDIUM Confidence Sources (Community and Analysis)

- [Context Engineering in ADK Architecture](https://medium.com/@raphael.mansuy/context-engineering-inside-googles-adk-architecture-for-production-ai-agents-083151ddcf61) - Dec 2025 analysis
- [Agent Evaluation with Google ADK Practical Guide](https://medium.com/@dcheng_93016/agent-evaluation-with-google-adk-a-practical-guide-for-agent-builders-a3c1622f550c) - Nov 2025
- [ADK meets MCP: Bridging Worlds of AI Agents](https://medium.com/google-cloud/adk-meets-mcp-bridging-worlds-of-ai-agents-1ed96ef5399c) - MCP integration patterns
- [Get Schwifty with FastAPI: Adding REST API to ADK](https://medium.com/google-cloud/get-schwifty-with-the-fastapi-adding-a-rest-api-to-our-agentic-application-with-google-adk-6b87a4ea7567) - FastAPI integration guide
- [DataCamp ADK Guide with Demo Project](https://www.datacamp.com/tutorial/agent-development-kit-adk) - Tutorial overview

### General References

- [python-dotenv PyPI](https://pypi.org/project/python-dotenv/) - Environment variable management
- [Python Version Status](https://devguide.python.org/versions/) - Python version lifecycle
- [Markdown Guide](https://www.markdownguide.org/) - Documentation format reference

---
**Stack research for:** Google ADK Workshop - Travel Booking Agent with Context Engineering
**Researched:** 2026-01-23
**Overall Assessment:** HIGH confidence. All core technologies verified with official sources. Version numbers current as of January 2026. Workshop pattern based on official Google Codelabs structure. Stack choices align with 90-minute constraint and free-tier requirements.
