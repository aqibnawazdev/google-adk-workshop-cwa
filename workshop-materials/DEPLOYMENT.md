# Deploying ADK Agents to Vertex AI Agent Engine

This guide covers deploying your ADK travel assistant to Vertex AI Agent Engine for production use.

> **Workshop Note:** Deployment is a post-workshop exploration topic. During the workshop, the instructor will demonstrate the deployment process. Use this guide for self-paced learning afterward.

---

## Table of Contents

1. [What is Vertex AI Agent Engine?](#what-is-vertex-ai-agent-engine)
2. [Prerequisites](#prerequisites)
3. [Deployment Steps](#deployment-steps)
4. [Testing Your Deployed Agent](#testing-your-deployed-agent)
5. [Monitoring and Management](#monitoring-and-management)
6. [Troubleshooting](#troubleshooting)
7. [Cost Considerations](#cost-considerations)
8. [Next Steps](#next-steps)

---

## What is Vertex AI Agent Engine?

Vertex AI Agent Engine is a managed runtime for deploying ADK agents to production. It provides:

- **Managed Infrastructure:** No servers to maintain, automatic scaling
- **Built-in Session Management:** Persistent conversations across requests
- **Secure API Endpoint:** HTTPS endpoints with IAM authentication
- **Monitoring:** Integrated with Cloud Logging and Cloud Monitoring
- **RAG Integration:** Seamless connection to Vertex AI RAG Engine

### When to Use Agent Engine

| Scenario | Recommendation |
|----------|---------------|
| Development/testing | Use local ADK (`adk run`) or Colab |
| Production API | Deploy to Agent Engine |
| High availability needed | Deploy to Agent Engine |
| Cost-sensitive experimentation | Stay local |

---

## Prerequisites

Before deploying, ensure you have:

### 1. Google Cloud Project

```bash
# Set your project
export GOOGLE_CLOUD_PROJECT="your-project-id"
gcloud config set project $GOOGLE_CLOUD_PROJECT
```

### 2. Required APIs Enabled

```bash
# Enable required APIs
gcloud services enable \
    aiplatform.googleapis.com \
    storage.googleapis.com \
    cloudbuild.googleapis.com \
    cloudresourcemanager.googleapis.com
```

### 3. Cloud Storage Bucket (for staging)

```bash
# Create a bucket for deployment artifacts
export STAGING_BUCKET="gs://${GOOGLE_CLOUD_PROJECT}-adk-staging"
gsutil mb -l us-central1 $STAGING_BUCKET
```

### 4. IAM Permissions

Your account needs these roles:
- `roles/aiplatform.user` - Deploy and manage agents
- `roles/storage.objectCreator` - Upload staging files
- `roles/iam.serviceAccountUser` - Use service accounts

```bash
# Grant permissions (run as project admin)
gcloud projects add-iam-policy-binding $GOOGLE_CLOUD_PROJECT \
    --member="user:your-email@example.com" \
    --role="roles/aiplatform.user"
```

### 5. Python Dependencies

```bash
pip install google-cloud-aiplatform>=1.60.0 google-adk
```

---

## Deployment Steps

### Step 1: Prepare Your Agent

Ensure your agent follows ADK patterns. Here's the structure from our workshop:

```python
# reference-implementation/agent.py
from google.adk.agents import Agent
from tools import search_flights, search_hotels
from state_utils import remember_preference, get_preference, clear_preference

def create_agent() -> Agent:
    """Create the travel booking assistant agent."""
    return Agent(
        model='gemini-2.5-flash',
        name='travel_booking_assistant',
        description='Travel assistant with flight and hotel search.',
        instruction='''You are an expert travel booking assistant.

YOUR CAPABILITIES:
- Search for flights between airports
- Find hotels in any destination
- Remember user preferences

Use your tools to help users plan trips.''',
        tools=[search_flights, search_hotels, remember_preference, get_preference, clear_preference],
    )
```

### Step 2: Initialize Vertex AI

```python
import vertexai
from vertexai import agent_engines

# Initialize with your project
vertexai.init(
    project="your-project-id",
    location="us-central1",  # Choose a supported region
    staging_bucket="gs://your-bucket-adk-staging"
)
```

### Step 3: Create AdkApp Wrapper

The `AdkApp` class wraps your agent for deployment:

```python
from vertexai.agent_engines import AdkApp
from agent import create_agent

# Create the deployable app
adk_app = AdkApp(
    agent=create_agent(),
    enable_tracing=True,  # Optional: Enable Cloud Trace
)
```

### Step 4: Deploy to Agent Engine

```python
# Deploy the agent
remote_agent = agent_engines.create(
    adk_app=adk_app,
    display_name="travel-assistant-production",
    description="Production travel booking assistant"
)

# Save the endpoint for later use
print(f"Agent deployed successfully!")
print(f"Resource name: {remote_agent.resource_name}")
```

The deployment process:
1. Packages your agent code and dependencies
2. Uploads to Cloud Storage staging bucket
3. Builds a container image via Cloud Build
4. Deploys to managed infrastructure
5. Creates an API endpoint

**Deployment typically takes 5-10 minutes.**

### Step 5: Get the Endpoint

```python
# The resource name is your endpoint identifier
endpoint = remote_agent.resource_name
print(f"Endpoint: {endpoint}")

# Format: projects/{project}/locations/{location}/reasoningEngines/{engine_id}
```

---

## Testing Your Deployed Agent

### Query the Deployed Agent

```python
from vertexai import agent_engines

# Connect to your deployed agent
remote_agent = agent_engines.get("your-resource-name")

# Create a session
session = remote_agent.create_session(user_id="test-user")

# Stream a query
response_text = ""
async for event in remote_agent.async_stream_query(
    session_id=session.id,
    message="Find flights from SFO to Tokyo on March 15"
):
    if event.content:
        response_text += event.content

print(response_text)
```

### Verify Tool Execution

```python
# Test that tools are being called
async for event in remote_agent.async_stream_query(
    session_id=session.id,
    message="Search for hotels in Paris under $200/night"
):
    # Check for function calls
    if hasattr(event, 'function_call') and event.function_call:
        print(f"Tool called: {event.function_call.name}")
        print(f"Args: {event.function_call.args}")
```

### Test Session Persistence

```python
# First message - set preference
async for event in remote_agent.async_stream_query(
    session_id=session.id,
    message="Remember my budget is $1500"
):
    pass

# Second message - should use saved preference
async for event in remote_agent.async_stream_query(
    session_id=session.id,
    message="Find me a flight to London"
):
    if event.content:
        print(event.content)
        # Should mention budget constraint
```

---

## Monitoring and Management

### View Logs

```bash
# View agent logs in Cloud Logging
gcloud logging read "resource.type=aiplatform.googleapis.com/ReasoningEngine" \
    --project=$GOOGLE_CLOUD_PROJECT \
    --limit=50
```

### List Deployed Agents

```python
# List all deployed agents
agents = agent_engines.list()
for agent in agents:
    print(f"Name: {agent.display_name}")
    print(f"Resource: {agent.resource_name}")
    print(f"Created: {agent.create_time}")
    print()
```

### Update an Agent

```python
# Get existing agent
remote_agent = agent_engines.get("your-resource-name")

# Create updated app
updated_app = AdkApp(
    agent=create_updated_agent(),  # Your updated agent
    enable_tracing=True,
)

# Update deployment
remote_agent.update(adk_app=updated_app)
```

---

## Troubleshooting

| Error | Cause | Solution |
|-------|-------|----------|
| `Permission denied` | Missing IAM roles | Add `roles/aiplatform.user` role |
| `Staging bucket not found` | Bucket doesn't exist | Create bucket with `gsutil mb` |
| `API not enabled` | APIs not activated | Run `gcloud services enable aiplatform.googleapis.com` |
| `Quota exceeded` | Hit deployment limits | Request quota increase or delete unused agents |
| `Build failed` | Dependency issues | Check requirements.txt, ensure all imports resolve |
| `Agent not responding` | Deployment incomplete | Wait for deployment to finish (check Cloud Build) |
| `Tool execution failed` | Tool code error | Test locally with `adk run` first |
| `Session not found` | Session expired | Create new session, check session timeout settings |

### Debug Deployment Issues

```bash
# Check Cloud Build logs
gcloud builds list --limit=5

# Get specific build details
gcloud builds describe BUILD_ID

# Check agent status
gcloud ai reasoning-engines list --region=us-central1
```

### Common Fixes

**Import errors:**
```bash
# Ensure all dependencies are in requirements.txt
pip freeze > requirements.txt
```

**Timeout during deployment:**
```bash
# Increase timeout (default is 1800s)
agent_engines.create(
    adk_app=adk_app,
    display_name="my-agent",
    timeout=3600  # 1 hour
)
```

---

## Cost Considerations

### What You Pay For

1. **Compute:** Per-second billing while agent is running
2. **Storage:** Staging bucket and container registry
3. **Requests:** Per-query costs for Gemini API calls
4. **Egress:** Data transfer out of Google Cloud

### Estimated Costs

| Component | Estimated Cost |
|-----------|---------------|
| Agent idle (per hour) | ~$0.10 |
| Per query (simple) | ~$0.001 |
| Per query (with tools) | ~$0.003 |
| Storage (per GB/month) | ~$0.02 |

*Costs vary by region and usage. Check [Vertex AI Pricing](https://cloud.google.com/vertex-ai/pricing) for current rates.*

### Cleanup to Stop Billing

**Critical: Delete agents you're not using!**

```python
# Delete a deployed agent
remote_agent = agent_engines.get("your-resource-name")
remote_agent.delete()
print("Agent deleted - billing stopped")
```

```bash
# Using gcloud CLI
gcloud ai reasoning-engines delete AGENT_ID --region=us-central1

# Delete staging bucket (optional)
gsutil rm -r gs://your-bucket-adk-staging
```

### Cost Management Tips

1. **Delete test deployments immediately** after verification
2. **Use local development** (`adk run`) for iteration
3. **Set budget alerts** in Cloud Console
4. **Monitor usage** in Billing Dashboard
5. **Consider scheduling** - stop agents during off-hours if not needed 24/7

---

## Next Steps

### After Workshop Deployment Practice

1. **Deploy the basic agent** from `reference-implementation/agent.py`
2. **Test with the provided script** in `reference-implementation/deploy.py`
3. **Query your deployed agent** and verify tool execution
4. **Clean up** - delete the test deployment

### Production Considerations

- **Authentication:** Add API key or OAuth for public access
- **Rate limiting:** Configure quotas to prevent abuse
- **Versioning:** Use display names with versions (`travel-assistant-v1`)
- **Multi-region:** Deploy to multiple regions for latency optimization
- **CI/CD:** Automate deployments with Cloud Build triggers

### Resources

- [Vertex AI Agent Engine Documentation](https://cloud.google.com/vertex-ai/docs/reasoning-engine/overview)
- [ADK Deployment Guide](https://google.github.io/adk-docs/deploy/)
- [Google Cloud Pricing Calculator](https://cloud.google.com/products/calculator)
- [IAM Roles for Vertex AI](https://cloud.google.com/vertex-ai/docs/general/access-control)

---

## Quick Reference: Deploy Script

Use the provided deployment script for automated deployment:

```bash
# From workshop-materials/reference-implementation/
cd reference-implementation

# Deploy
python deploy.py --action deploy

# Test
python deploy.py --action test --endpoint "projects/xxx/locations/xxx/reasoningEngines/xxx"

# Cleanup (important!)
python deploy.py --action cleanup --endpoint "projects/xxx/locations/xxx/reasoningEngines/xxx"
```

See `reference-implementation/deploy.py` for the complete implementation.

---

*This guide is part of the Google ADK Workshop materials. For workshop support, contact your instructor.*
