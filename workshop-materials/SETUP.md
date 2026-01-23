# ADK Workshop Setup Guide

Complete this setup **48 hours before the workshop** to ensure a smooth experience.

## Quick Start (Recommended: Google Colab)

The fastest way to get started:

1. Open the verification notebook: [00-setup-verification.ipynb](./00-setup-verification.ipynb)
2. Click "Run All" (Runtime → Run all)
3. When prompted, authorize Google Cloud access
4. Verify all checks pass (green checkmarks)

**That's it!** If all checks pass, you're ready for the workshop.

---

## Prerequisites

### Required
- Google account (Gmail, Google Workspace, or Cloud Identity)
- Workshop GCP project ID (provided by instructor)
- Modern web browser (Chrome recommended for Colab)

### Provided for You
- Pre-configured GCP project with Vertex AI API enabled
- Sufficient quota for workshop exercises
- Workshop materials and notebooks

---

## Option A: Google Colab (Recommended)

Google Colab eliminates local setup entirely. All dependencies are pre-installed or easily added.

### Step 1: Access Workshop Materials

1. Open the workshop folder in Google Drive (link provided by instructor)
2. Or clone from GitHub: `[workshop-repo-url]`

### Step 2: Verify Your Environment

1. Open `00-setup-verification.ipynb`
2. Update `PROJECT_ID` with your workshop project ID
3. Run all cells
4. Each check should show ✓

### Step 3: Test Authentication

When you run the authentication cell, you'll see:
1. A popup or link to Google OAuth
2. Choose your Google account
3. Authorize access to Google Cloud
4. Return to Colab

**Expected result:** "✓ Authenticated with project: your-project-id"

### Common Colab Issues

| Issue | Solution |
|-------|----------|
| OAuth popup blocked | Allow popups from colab.research.google.com |
| "Permission denied" | Verify you're using the correct Google account |
| "API not enabled" | Contact instructor - project may need configuration |

---

## Option B: Local Development (Advanced)

Use this if you prefer local development or need to work offline.

### Requirements

- Python 3.11 or 3.12
- pip or uv package manager
- gcloud CLI installed

### Step 1: Install Python

**macOS:**
```bash
brew install python@3.12
```

**Ubuntu/Debian:**
```bash
sudo apt update && sudo apt install python3.12 python3.12-venv
```

**Windows:**
Download from https://python.org/downloads/ (3.12.x)

### Step 2: Create Virtual Environment

```bash
# Create project directory
mkdir adk-workshop && cd adk-workshop

# Create virtual environment
python3.12 -m venv .venv

# Activate it
source .venv/bin/activate  # macOS/Linux
# .venv\Scripts\activate   # Windows
```

### Step 3: Install Dependencies

```bash
pip install google-adk==1.23.0
```

### Step 4: Authenticate with GCP

```bash
# Install gcloud CLI if needed: https://cloud.google.com/sdk/docs/install
gcloud auth application-default login
gcloud config set project YOUR_PROJECT_ID
```

### Step 5: Verify Installation

```bash
python -c "
import google.adk
print(f'ADK version: {google.adk.__version__}')

from google.adk.agents import Agent
agent = Agent(
    model='gemini-2.5-flash',
    name='test',
    description='Test agent',
    instruction='Say hello'
)
print(agent.generate_content('Hello').text[:100])
print('✓ Local environment ready!')
"
```

---

## Troubleshooting

### Authentication Issues

**"Permission denied" or "Not authenticated"**

1. Re-run the authentication cell/command
2. Verify you're using the correct Google account
3. Check that your account has access to the workshop project

**OAuth redirect fails or hangs**

1. Check if popup blocker is active
2. Try a different browser (Chrome works best)
3. If on corporate network, try personal hotspot temporarily

**"API not enabled" error**

The Vertex AI API may not be enabled. Contact instructor or:
```bash
gcloud services enable aiplatform.googleapis.com
```

### Dependency Issues

**ModuleNotFoundError: No module named 'google.adk'**

```bash
pip install google-adk==1.23.0
```

**Version mismatch warnings**

```bash
pip uninstall google-adk
pip install google-adk==1.23.0
```

### Model Access Issues

**"Model not found" or quota errors**

1. Verify project has Gemini API access
2. Check quota: https://console.cloud.google.com/iam-admin/quotas
3. Try a different model: `gemini-2.0-flash` as fallback

### Network Issues

**Connection timeout on corporate network**

1. VPN may be blocking Google Cloud APIs
2. Try disconnecting VPN temporarily
3. Fallback: Use personal device with mobile hotspot

---

## Pre-Workshop Checklist

Complete all items 48 hours before workshop:

- [ ] I have my workshop GCP project ID
- [ ] I can access Google Colab (colab.research.google.com)
- [ ] I ran 00-setup-verification.ipynb successfully
- [ ] All verification checks passed (green checkmarks)
- [ ] I submitted my verification screenshot (if required)

If any checks fail, contact the instructor with:
1. Screenshot of the error
2. Which verification step failed
3. Any error messages shown

---

## Getting Help

- **During workshop:** Raise hand or use chat
- **Before workshop:** [instructor contact info]
- **ADK documentation:** https://google.github.io/adk-docs/

---

*Last updated: 2026-01-23*
