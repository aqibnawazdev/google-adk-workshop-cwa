# Phase 1: Foundation & Setup - Research

**Researched:** 2026-01-23
**Domain:** Google Agent Development Kit (ADK) 1.23.0, Vertex AI, Workshop Education
**Confidence:** HIGH

## Summary

Phase 1 establishes the foundational environment and capabilities for a 90-minute ADK workshop using Google Colab for zero-install delivery. The research confirms that Google ADK 1.23.0 (released January 22, 2026) provides a mature, stable platform for building conversational agents with Gemini 2.5 Flash.

The critical insight for workshop success is that setup traditionally consumes 40+ minutes of workshop time, creating a massive risk to the 90-minute timeline. The solution lies in three strategies: (1) Google Colab eliminates local environment setup entirely, (2) pre-provisioned GCP accounts with enabled APIs remove permission delays, and (3) a robust verification script executed 48 hours before the workshop catches authentication and dependency issues before participants arrive.

The basic "Hello World" agent should demonstrate the core ADK agent lifecycle: instantiation with model configuration, system instructions (prompt engineering), and conversational interaction. The reference implementation should reveal the progressive architecture (agent → tools → context) without exposing all future phases, serving as both motivation and roadmap.

**Primary recommendation:** Use Google Colab with pre-configured authentication snippets, require 48-hour pre-validation via verification notebook, and keep the basic agent to <15 lines of code to ensure participants experience success within the first 20 minutes.

## Standard Stack

The established stack for ADK workshop delivery:

### Core
| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| google-adk | 1.23.0 | Agent framework | Official Google framework, latest stable release (Jan 22, 2026) |
| Python | 3.11 or 3.12 | Runtime environment | ADK requires 3.10+, but 3.11/3.12 recommended for performance |
| Gemini | 2.5 Flash | LLM model | Latest production model, optimized for conversational agents |
| Vertex AI | Current | Deployment platform | Fully managed Google Cloud service for agent runtime |
| Google Colab | Enterprise/Free | Delivery environment | Zero-install, browser-based, pre-authenticated with Google |

### Supporting
| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| uv | Latest | Fast package manager | Optional alternative to pip for faster installs |
| google-auth | Latest (transitive) | Authentication | Automatically installed with google-adk |
| google-cloud-aiplatform | Latest (transitive) | Vertex AI client | Automatically installed with google-adk |

### Alternatives Considered
| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| Vertex AI backend | Google AI Studio (API key) | Simpler auth (just API key) but no production features like sessions/memory |
| Google Colab | Local Jupyter | More control but 30+ min setup time, dependency conflicts |
| Gemini 2.5 Flash | Gemini 2.5 Pro | Better quality but slower, more expensive, overkill for workshop |

**Installation (Colab):**
```python
# In first Colab cell
!pip install google-adk==1.23.0
```

**Installation (Local - for reference only):**
```bash
# Create virtual environment
python3.12 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install ADK
pip install google-adk==1.23.0
```

## Architecture Patterns

### Recommended Workshop Structure
```
workshop-materials/
├── 00-setup-verification.ipynb    # Pre-workshop validation (48h ahead)
├── 01-hello-agent.ipynb           # Basic conversational agent (Phase 1)
├── 02-tools-functions.ipynb       # Function calling (Phase 2)
├── 03-rag-knowledge.ipynb         # RAG integration (Phase 3)
├── 04-sessions-memory.ipynb       # Session management (Phase 4)
└── reference-implementation/       # Complete working agent
    ├── agent.py                    # Full implementation
    ├── .env.template               # Configuration template
    └── README.md                   # Architecture explanation
```

### Pattern 1: Colab Authentication Setup
**What:** Authentication snippet that works in both free Colab and Colab Enterprise
**When to use:** First cell of every workshop notebook
**Example:**
```python
# Source: https://docs.cloud.google.com/colab/docs/run-code-adc
from google.colab import auth

# Authenticate for GCP services
PROJECT_ID = "your-workshop-project-id"
auth.authenticate_user(project_id=PROJECT_ID)

# Verify authentication
!gcloud config set project $PROJECT_ID
print(f"✓ Authenticated with project: {PROJECT_ID}")
```

### Pattern 2: Minimal Agent Definition
**What:** Simplest possible working agent for initial success
**When to use:** First agent creation exercise
**Example:**
```python
# Source: https://codelabs.developers.google.com/devsite/codelabs/build-agents-with-adk-foundation
from google.adk.agents import Agent

# Create a basic conversational agent
agent = Agent(
    model='gemini-2.5-flash',
    name='hello_agent',
    description='A friendly assistant for basic questions.',
    instruction='You are a helpful assistant. Be concise and friendly.',
)

# Test the agent
response = agent.generate_content("Hello! What can you do?")
print(response.text)
```

### Pattern 3: Progressive Reference Implementation
**What:** Complete agent showing target architecture without revealing future phases
**When to use:** Motivation and roadmap for participants
**Structure:**
```python
# reference-implementation/agent.py
from google.adk.agents import Agent

# Agent with tools (hints at Phase 2)
root_agent = Agent(
    model='gemini-2.5-flash',
    name='workshop_assistant',
    description='Complete workshop agent with tools and knowledge.',
    instruction='''You are a workshop assistant for learning ADK.
    Use your tools to provide accurate, helpful information.
    Be encouraging and explain concepts clearly.''',
    tools=[
        # Tool definitions (commented with "You'll learn this in Phase 2")
    ],
)
```

### Pattern 4: Environment Verification Script
**What:** Automated validation of all dependencies and access
**When to use:** 48 hours before workshop, as first notebook cell
**Example:**
```python
# Verification checklist
checks = {
    'Python version': lambda: sys.version_info >= (3, 11),
    'google-adk installed': lambda: importlib.import_module('google.adk'),
    'GCP authentication': lambda: subprocess.run(['gcloud', 'auth', 'list'],
                                                 capture_output=True).returncode == 0,
    'Vertex AI API enabled': lambda: test_api_call(),
    'Gemini access': lambda: test_model_call(),
}

# Run all checks with clear pass/fail
for check_name, check_fn in checks.items():
    try:
        check_fn()
        print(f"✓ {check_name}")
    except Exception as e:
        print(f"✗ {check_name}: {str(e)}")
        # Provide troubleshooting link
```

### Anti-Patterns to Avoid
- **Complex initial agent**: Don't show tools, RAG, or multi-agent patterns in first example (overwhelms beginners)
- **Local environment setup**: Don't require pip/conda/virtualenv setup during workshop (kills 30-40 minutes)
- **Service account credentials**: Don't use .json key files (security risk, complexity, easy to leak in notebooks)
- **"It works on my machine"**: Don't skip pre-validation - discover auth issues before workshop starts
- **Silent failures**: Don't let verification pass when APIs fail (catch errors and show clear messages)

## Don't Hand-Roll

Problems that look simple but have existing solutions:

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Python dependency management | Custom install script | `pip install -r requirements.txt` or `uv pip install` | pip resolves dependencies, handles conflicts, industry standard |
| LLM authentication | Custom OAuth flow | google.colab.auth.authenticate_user() | Pre-built, tested, handles token refresh automatically |
| Agent conversation loop | Manual while loop with input() | adk run or adk web | Built-in REPL, history, proper error handling |
| Environment verification | Manual try/except blocks | pip check + custom validation script | pip check validates dependencies, custom script verifies API access |
| Configuration management | Custom .ini parser | .env file with python-dotenv | Standard pattern, prevents credential leaks, ADK expects this |
| Model selection | Hardcode model strings | ADK model configuration system | Supports easy model switching, version management |

**Key insight:** Workshop setup is where custom solutions most often fail. Use battle-tested tools (Colab auth, pip, ADK CLI) rather than building "simpler" alternatives that break under edge cases (proxy networks, SSO, regional restrictions).

## Common Pitfalls

### Pitfall 1: Authentication Time Sink
**What goes wrong:** Participants spend 20-40 minutes troubleshooting GCP authentication during workshop
**Why it happens:**
- Different auth methods for local vs Colab vs Colab Enterprise
- Service account key confusion (downloading .json, setting GOOGLE_APPLICATION_CREDENTIALS)
- Proxy/corporate network blocking OAuth flows
- Expired credentials or wrong project permissions
**How to avoid:**
- Use pre-provisioned GCP projects with APIs already enabled
- Provide single authentication snippet tested in target environment (Colab)
- Run 48-hour pre-validation requiring participants to execute verification notebook
- Have backup authentication method ready (API keys for Google AI Studio)
**Warning signs:**
- Participant sees "Permission denied" or "API not enabled" errors
- OAuth redirect fails or hangs
- gcloud commands return "You are not currently authenticated"

### Pitfall 2: Dependency Conflicts in Local Environments
**What goes wrong:** Participants with existing Python installations get version conflicts, import errors
**Why it happens:**
- System Python with globally installed packages
- Conda/pip mixing in same environment
- Incompatible transitive dependencies (google-auth, protobuf versions)
- Python 2.7 still on PATH
**How to avoid:**
- Use Google Colab to eliminate local environment entirely
- If local setup required, mandate fresh virtual environment
- Provide exact requirements.txt with pinned versions
- Include verification step that catches version mismatches
**Warning signs:**
- "ModuleNotFoundError" despite pip install succeeding
- "ImportError: cannot import name X from Y"
- Protobuf version warnings

### Pitfall 3: API Quota Exhaustion
**What goes wrong:** Workshop participants hit API rate limits or quota exhaustion mid-session
**Why it happens:**
- Multiple participants sharing same GCP project
- Retry loops consuming quota rapidly
- Free tier limits on Gemini API
**How to avoid:**
- Use separate GCP projects per participant (or small groups)
- Enable billing on workshop projects (even $1 prevents free tier limits)
- Monitor quota usage dashboard before/during workshop
- Have instructor project as backup
**Warning signs:**
- "Resource exhausted" or "Quota exceeded" errors
- Intermittent failures that resolve after waiting
- Sudden slowdown in API responses

### Pitfall 4: "Works in Examples, Fails in My Code"
**What goes wrong:** Participants copy example code but it doesn't work when they modify it
**Why it happens:**
- Subtle differences in model names (gemini-2.5-flash vs gemini-2.5-flash-latest)
- Missing import statements from abbreviated examples
- Incorrect indentation in Python (mixing tabs/spaces)
- Environment variables not set (.env file not loaded)
**How to avoid:**
- Provide complete, runnable code examples (no "..." ellipses)
- Include all imports explicitly in every example
- Use Colab cells that execute independently
- Show .env template and verification that variables loaded
**Warning signs:**
- "NameError: name 'Agent' is not defined"
- "model not found" errors
- Code works in instructor notebook but not participant notebook

### Pitfall 5: Network/Firewall Issues in Corporate Environments
**What goes wrong:** Corporate firewalls block Google Cloud API endpoints or OAuth redirects
**Why it happens:**
- SSL inspection proxies breaking TLS to *.googleapis.com
- Blocked domains in corporate DNS
- VPN routing conflicts
**How to avoid:**
- Test Colab access from corporate network before workshop
- Provide alternative: Google AI Studio API key (bypasses some restrictions)
- Have IT whitelist required domains: *.googleapis.com, *.google.com, colab.research.google.com
- Offer personal Google accounts as fallback (use personal laptop/hotspot)
**Warning signs:**
- SSL certificate errors
- "Connection timeout" or "Connection refused"
- OAuth redirect to localhost:8085 hangs

### Pitfall 6: Setup Consuming Workshop Time
**What goes wrong:** First 40 minutes spent on setup, leaving 50 minutes for actual learning
**Why it happens:**
- Underestimating setup complexity
- Not pre-validating environments
- Debugging individual participant issues one-by-one
- "Just one more thing" syndrome (install this, configure that)
**How to avoid:**
- Use Google Colab to eliminate setup phase
- Require 48-hour pre-validation with verification notebook
- Set hard time limit: "Setup ends at 10:15 regardless of completion"
- Pair participants who finish early with those still troubleshooting
- Move stragglers to observer role, help after workshop
**Warning signs:**
- Workshop agenda shows >15 minutes for setup
- No pre-workshop validation requirement
- Setup instructions longer than 1 page

## Code Examples

Verified patterns from official sources:

### Basic Agent Creation (Hello World)
```python
# Source: https://codelabs.developers.google.com/devsite/codelabs/build-agents-with-adk-foundation
from google.adk.agents import Agent

# Minimal working agent
agent = Agent(
    model='gemini-2.5-flash',
    name='hello_agent',
    description='A simple conversational assistant.',
    instruction='You are a helpful assistant. Be concise and friendly.',
)

# Test conversation
response = agent.generate_content("Hello! Tell me about yourself.")
print(response.text)
```

### Colab Environment Setup
```python
# Source: https://docs.cloud.google.com/colab/docs/run-code-adc
# Cell 1: Authentication
from google.colab import auth
import os

PROJECT_ID = "your-workshop-project"
LOCATION = "us-central1"

auth.authenticate_user(project_id=PROJECT_ID)
os.environ['GOOGLE_CLOUD_PROJECT'] = PROJECT_ID
os.environ['GOOGLE_CLOUD_LOCATION'] = LOCATION

print(f"✓ Authenticated with project: {PROJECT_ID}")
```

```python
# Cell 2: Install ADK
!pip install -q google-adk==1.23.0
print("✓ google-adk installed")
```

```python
# Cell 3: Verify installation
import sys
import google.adk

print(f"✓ Python {sys.version_info.major}.{sys.version_info.minor}")
print(f"✓ google-adk {google.adk.__version__}")
```

### Environment Verification Script
```python
# Source: Workshop best practices (composite from multiple sources)
import sys
import subprocess
import importlib.util

def verify_environment():
    """
    Verify all dependencies and API access for ADK workshop.
    Returns True if all checks pass, False otherwise.
    """
    results = {}

    # Check 1: Python version
    python_version = sys.version_info
    results['Python 3.11+'] = python_version >= (3, 11)

    # Check 2: google-adk installation
    try:
        import google.adk
        results['google-adk installed'] = True
        results['google-adk version'] = google.adk.__version__ == '1.23.0'
    except ImportError:
        results['google-adk installed'] = False
        results['google-adk version'] = False

    # Check 3: GCP authentication
    try:
        result = subprocess.run(
            ['gcloud', 'auth', 'list'],
            capture_output=True,
            text=True,
            timeout=5
        )
        results['GCP authenticated'] = 'ACTIVE' in result.stdout
    except Exception:
        results['GCP authenticated'] = False

    # Check 4: Vertex AI API access
    try:
        from google.cloud import aiplatform
        # This will fail if API not enabled
        aiplatform.init(project=os.environ.get('GOOGLE_CLOUD_PROJECT'))
        results['Vertex AI API enabled'] = True
    except Exception as e:
        results['Vertex AI API enabled'] = False
        results['Vertex AI error'] = str(e)

    # Check 5: Gemini model access
    try:
        from google.adk.agents import Agent
        test_agent = Agent(
            model='gemini-2.5-flash',
            name='test',
            description='Test agent',
            instruction='Say hello.',
        )
        response = test_agent.generate_content("Hello")
        results['Gemini access'] = len(response.text) > 0
    except Exception as e:
        results['Gemini access'] = False
        results['Gemini error'] = str(e)

    # Print results
    print("Environment Verification Results")
    print("=" * 50)
    for check, passed in results.items():
        if isinstance(passed, bool):
            status = "✓ PASS" if passed else "✗ FAIL"
            print(f"{status}: {check}")
        else:
            print(f"  → {check}: {passed}")

    all_passed = all(v for v in results.values() if isinstance(v, bool))
    print("=" * 50)
    if all_passed:
        print("✓ All checks passed! Ready for workshop.")
    else:
        print("✗ Some checks failed. Please troubleshoot before workshop.")
        print("\nTroubleshooting guide: [URL to workshop docs]")

    return all_passed

# Run verification
verify_environment()
```

### Reference Implementation Preview
```python
# Source: Based on https://github.com/google/adk-samples patterns
from google.adk.agents import Agent

# This is what you'll build by the end of the workshop
workshop_agent = Agent(
    model='gemini-2.5-flash',
    name='workshop_assistant',
    description='A complete workshop agent with tools and knowledge.',
    instruction='''You are a helpful workshop assistant.

    Your capabilities:
    - Answer questions using your tools (Phase 2)
    - Search your knowledge base for information (Phase 3)
    - Remember conversation context across sessions (Phase 4)

    Always be encouraging and explain concepts clearly.''',

    # Tools (you'll add these in Phase 2)
    tools=[],  # TODO: Add get_weather, get_time functions

    # Knowledge (you'll add this in Phase 3)
    # knowledge_base=...  # TODO: Add RAG integration
)

# Preview interaction
print("Reference Implementation Preview")
print("This is what you'll build in this workshop!")
print("\nTry asking: 'What can you help me with?'")
```

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| LangChain for agent framework | Google ADK | ADK 1.0 (late 2024) | Simpler API, better Gemini integration, Google-supported |
| Manual tool calling logic | ADK automatic tool dispatch | ADK 1.0 | Less boilerplate, built-in retry/error handling |
| google-generativeai SDK | ADK with Vertex AI backend | ADK 1.15+ | Production features (sessions, evaluation, deployment) |
| Service account JSON keys | Application Default Credentials | Cloud best practices | Better security, simpler auth flow |
| gemini-pro model | gemini-2.5-flash | Gemini 2.5 release (2025) | Faster, cheaper, better quality |
| Individual agent files | adk create scaffolding | ADK 1.0 | Consistent project structure |
| Custom agent evaluation | Built-in ADK evaluation framework | ADK 1.20+ | Standardized testing, better metrics |
| @experimental decorators | Stable APIs | ADK 1.23 (Jan 2026) | Production-ready code execution sandboxes |

**Deprecated/outdated:**
- **google-generativeai direct use**: Still works but ADK provides better abstraction for agent workflows
- **Gemini 1.5 models**: Replaced by Gemini 2.5 series (use gemini-2.5-flash for workshops)
- **Manual session management**: ADK now has built-in session persistence via Vertex AI Agent Engine
- **@experimental decorator**: Removed in 1.23.0, features now stable

## Open Questions

Things that couldn't be fully resolved:

1. **Pre-provisioned GCP Account Strategy**
   - What we know: Workshop needs pre-provisioned GCP accounts with Vertex AI API enabled (INFRA-04)
   - What's unclear: Best approach - one project per participant, one project shared, or instructor project only?
   - Recommendation: Create one GCP project per participant (or per pair) to avoid quota conflicts. Use Terraform/gcloud scripts to provision 50+ projects rapidly. Include cleanup script to destroy after workshop.

2. **Colab Enterprise vs Free Colab**
   - What we know: Both support ADK, Enterprise has better authentication
   - What's unclear: Can we assume participants have Colab Enterprise access, or must we support free tier?
   - Recommendation: Design for free Colab (lowest common denominator), note Enterprise advantages in docs. Test all notebooks in both environments.

3. **Reference Implementation Scope**
   - What we know: Should show target architecture without revealing future phases
   - What's unclear: How much to show? Full code with comments, or skeleton with TODOs?
   - Recommendation: Show complete working agent but comment out Phase 2-4 features with "You'll learn this in Phase X" notes. Participants can see what's possible without spoiling learning progression.

4. **48-Hour Pre-Validation Enforcement**
   - What we know: Pre-validation prevents setup problems during workshop
   - What's unclear: How to enforce? Honor system, required submission, automated checking?
   - Recommendation: Require participants to complete verification notebook and paste screenshot/output in pre-workshop form. Non-completion = can attend but may need to pair with validated participant.

5. **Network/Firewall Fallback Strategy**
   - What we know: Corporate networks may block Google Cloud APIs
   - What's unclear: What's the backup plan when Vertex AI fails due to network?
   - Recommendation: Provide dual authentication: (1) Vertex AI via ADC (preferred), (2) Google AI Studio API key (fallback). Google AI Studio has fewer network restrictions, simpler auth, works for learning even if not production-ready.

## Sources

### Primary (HIGH confidence)
- Google ADK official docs: https://google.github.io/adk-docs/
- ADK Python releases: https://github.com/google/adk-python/releases (v1.23.0 confirmed Jan 22, 2026)
- Google Codelabs ADK Foundation: https://codelabs.developers.google.com/devsite/codelabs/build-agents-with-adk-foundation
- Vertex AI Agent Engine docs: https://docs.cloud.google.com/agent-builder/agent-engine/overview
- Vertex AI authentication: https://docs.cloud.google.com/vertex-ai/generative-ai/docs/start/gcp-auth
- Colab authentication guide: https://docs.cloud.google.com/colab/docs/run-code-adc
- ADK sample repository: https://github.com/google/adk-samples

### Secondary (MEDIUM confidence)
- Workshop time management research: 90-minute sessions optimal, 8x prep time multiplier (https://www.wavetable.net/resources/how-to-calculate-the-time-you-need-to-create-a-workshop)
- Colab workshop best practices: Use pre-existing Google accounts, share as viewer (https://www.aifire.co/p/the-complete-guide-to-google-colab-for-free-ai-development)
- Python dependency best practices: Virtual environments essential, pip check for validation (https://packaging.python.org/tutorials/managing-dependencies/)
- AI agent prompt engineering: Context engineering focus, tight tool sets, few-shot examples (https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)
- AI agent common mistakes: Poor architecture, over-complexity, security issues (https://www.wildnetedge.com/blogs/common-ai-agent-development-mistakes-and-how-to-avoid-them)

### Tertiary (LOW confidence)
- Workshop feedback timing: 48-hour window for quality responses (https://www.theysaid.io/blog/workshop-feedback-surveys)
- Deep work cycles: 90-minute focus blocks align with ultradian rhythms (https://dev.to/teamcamp/the-90-minute-sprint-model-how-deep-work-cycles-transform-developer-output-43f1)

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH - ADK 1.23.0 confirmed from official GitHub release, version tested in official Codelabs
- Architecture: HIGH - Patterns verified in official documentation and sample repositories
- Pitfalls: MEDIUM - Drawn from workshop best practices literature and AI agent development guides, not ADK-specific

**Research date:** 2026-01-23
**Valid until:** 2026-02-23 (30 days - stable framework, but fast-moving AI field)
**Recommended re-validation:** Before workshop delivery, verify ADK version still current and Gemini model availability
