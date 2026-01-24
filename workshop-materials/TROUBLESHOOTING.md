# Troubleshooting Guide

This guide helps you resolve common errors during the ADK workshop. Errors are organized by symptom - find the error message you're seeing and follow the resolution steps.

## Quick Index

Find your error message and jump to the solution:

| Error Message | Section |
|---------------|---------|
| `ModuleNotFoundError: No module named 'google.adk'` | [Module Not Found](#module-not-found) |
| `ModuleNotFoundError: No module named 'google.generativeai'` | [Module Not Found](#module-not-found) |
| `Invalid API key` | [Authentication Errors](#authentication-errors) |
| `API key not valid` | [Authentication Errors](#authentication-errors) |
| `Request had invalid authentication credentials` | [Authentication Errors](#authentication-errors) |
| `GOOGLE_API_KEY not set` | [Authentication Errors](#authentication-errors) |
| `API not enabled` | [API Access Issues](#api-access-issues) |
| `Quota exceeded` | [API Access Issues](#api-access-issues) |
| `Permission denied` | [API Access Issues](#api-access-issues) |
| `RuntimeError: This event loop is already running` | [Async/Runtime Errors](#asyncruntime-errors) |
| `RuntimeError: no running event loop` | [Async/Runtime Errors](#asyncruntime-errors) |
| `asyncio.run() cannot be called from a running event loop` | [Async/Runtime Errors](#asyncruntime-errors) |
| `TimeoutError` | [Network Issues](#network-issues) |
| `Connection refused` | [Network Issues](#network-issues) |
| `Unable to resolve host` | [Network Issues](#network-issues) |
| `TypeError: expected str` | [Type/Validation Errors](#typevalidation-errors) |
| `Function returns None` | [Type/Validation Errors](#typevalidation-errors) |
| `Tool not called` | [Type/Validation Errors](#typevalidation-errors) |
| `Corpus not found` | [RAG Errors](#rag-errors) |
| `No relevant results` | [RAG Errors](#rag-errors) |
| `KeyError` in state | [State Errors](#state-errors) |
| `State key not found` | [State Errors](#state-errors) |

---

## Module Not Found

### Symptom

```
ModuleNotFoundError: No module named 'google.adk'
```

or

```
ModuleNotFoundError: No module named 'google.generativeai'
```

### Common Causes

1. **ADK not installed** - You haven't run the setup cell yet
2. **Wrong environment** - Running in base Python instead of notebook kernel
3. **Version conflict** - Another package downgraded or removed ADK
4. **Kernel not restarted** - Installation completed but kernel still has old imports cached

### Resolution Steps

1. **Run the installation cell:**
   ```python
   !pip install -q google-adk==1.23.0
   ```

2. **Restart the kernel:**
   - In Colab: Runtime > Restart runtime
   - In Jupyter: Kernel > Restart Kernel

3. **Verify installation:**
   ```python
   import google.adk
   print(google.adk.__version__)
   # Should print: 1.23.0
   ```

4. **If still failing, check for conflicts:**
   ```python
   !pip list | grep google
   ```
   Look for multiple `google-*` packages with conflicting versions.

### Prevention

- Always run the setup cell at the top of each notebook before any imports
- Don't install packages manually in terminal while notebook is running
- Use exact version pins (`==1.23.0`) to prevent automatic upgrades

### If Still Broken

1. Create a fresh notebook/runtime
2. Run only the install cell first
3. Restart runtime
4. Then run your code

---

## Authentication Errors

### Symptom

```
google.auth.exceptions.DefaultCredentialsError: Could not automatically determine credentials
```

or

```
Error: Invalid API key
```

or

```
API key not valid. Please pass a valid API key.
```

or

```
GOOGLE_API_KEY environment variable not set
```

### Common Causes

1. **API key not set** - You didn't run the API key configuration cell
2. **Invalid API key** - Typo in the key or key was revoked
3. **Wrong project** - API key from a different project without Generative AI enabled
4. **Key expired** - Some API keys have expiration dates
5. **Environment variable not persisted** - Key was set in a different cell/session

### Resolution Steps

1. **Get a valid API key:**
   - Go to https://aistudio.google.com/apikey
   - Click "Create API Key"
   - Copy the key (it starts with `AIza...`)

2. **Configure the key in your notebook:**
   ```python
   import os
   import google.generativeai as genai
   from getpass import getpass

   api_key = getpass('Enter your Google AI API Key: ')
   genai.configure(api_key=api_key)
   os.environ['GOOGLE_API_KEY'] = api_key

   print("API Key configured!")
   ```

3. **Verify the key works:**
   ```python
   import google.generativeai as genai
   model = genai.GenerativeModel('gemini-2.5-flash')
   response = model.generate_content("Say hello")
   print(response.text)
   ```

4. **If using environment variables, ensure they're set:**
   ```python
   import os
   print("GOOGLE_API_KEY:", "Set" if os.environ.get('GOOGLE_API_KEY') else "NOT SET")
   ```

### Prevention

- Run the API key configuration cell at the start of every session
- Never hardcode API keys in notebooks (use `getpass` for input)
- Keep your API key secure and don't share it
- Test authentication immediately after setup, before writing code

### If Still Broken

1. Generate a new API key at https://aistudio.google.com/apikey
2. Delete any old keys you're not using
3. Restart your notebook runtime completely
4. Enter the new key in the configuration cell

---

## API Access Issues

### Symptom

```
PermissionDenied: 403 Generative Language API has not been used in project...
```

or

```
ResourceExhausted: 429 Quota exceeded for quota metric...
```

or

```
Access denied: The caller does not have permission
```

### Common Causes

1. **API not enabled** - Generative Language API not enabled for your project
2. **Quota exceeded** - You've hit rate limits or daily quotas
3. **Billing not enabled** - Some APIs require a billing account
4. **Wrong region** - API not available in your selected region

### Resolution Steps

**For "API not enabled":**

1. The Google AI API (aistudio.google.com) keys work without enabling APIs
2. If you're using Vertex AI, enable the API in Cloud Console:
   - Go to https://console.cloud.google.com/apis/library
   - Search for "Generative Language API" or "Vertex AI API"
   - Click Enable
   - Wait 2-5 minutes for propagation

**For "Quota exceeded":**

1. Wait a few minutes - rate limits often reset quickly
2. Check your quotas:
   - Go to https://console.cloud.google.com/iam-admin/quotas
   - Filter by "Generative Language API"
3. Request a quota increase if needed for your use case

**For "Permission denied":**

1. Verify your API key is for the correct project
2. Ensure the API key has no restrictions blocking the Generative Language API
3. Check API key restrictions at https://console.cloud.google.com/apis/credentials

### Prevention

- Use Google AI API keys from aistudio.google.com (simpler setup)
- Keep track of your API usage during the workshop
- If doing intensive testing, add short delays between requests

### If Still Broken

1. Try creating a completely new API key
2. If using Vertex AI, verify your project has billing enabled
3. Contact your workshop instructor for help

---

## Async/Runtime Errors

### Symptom

```
RuntimeError: This event loop is already running
```

or

```
RuntimeError: asyncio.run() cannot be called from a running event loop
```

or

```
RuntimeError: no running event loop
```

### Common Causes

1. **Using asyncio.run() in Colab/Jupyter** - These environments already have a running event loop
2. **Nested event loops** - Trying to start a new loop inside an existing one
3. **Missing await** - Calling async function without await

### Resolution Steps

**For Colab/Jupyter environments:**

1. **Use `await` directly instead of `asyncio.run()`:**

   Wrong:
   ```python
   import asyncio
   asyncio.run(my_async_function())  # This fails in Colab
   ```

   Correct:
   ```python
   await my_async_function()  # Use await directly
   ```

2. **For ADK agent calls:**

   Wrong:
   ```python
   asyncio.run(runner.run_async(...))  # Fails
   ```

   Correct:
   ```python
   async for event in runner.run_async(
       user_id=user_id,
       session_id=session.id,
       new_message=Content(parts=[Part(text="Hello")], role="user")
   ):
       if event.is_final_response():
           print(event.content.parts[0].text)
   ```

3. **If you must use asyncio.run() (not recommended in notebooks):**
   ```python
   import nest_asyncio
   nest_asyncio.apply()  # Allows nested event loops
   asyncio.run(my_function())
   ```

### Prevention

- Always use `await` directly in Colab/Jupyter cells
- Follow the ADK pattern: `async for event in runner.run_async(...)`
- Define helper functions as `async def` and call them with `await`

### If Still Broken

1. Restart your notebook runtime completely
2. Run cells in order from the top
3. Ensure you're not mixing synchronous and asynchronous patterns

---

## Network Issues

### Symptom

```
TimeoutError: The read operation timed out
```

or

```
ConnectionError: Unable to connect to server
```

or

```
requests.exceptions.ConnectionError: Connection refused
```

### Common Causes

1. **Slow internet connection** - API calls timing out
2. **Firewall blocking requests** - Corporate networks may block API endpoints
3. **VPN interference** - VPN may route traffic through blocked regions
4. **Google service issues** - Temporary service outages (rare)

### Resolution Steps

1. **Test basic connectivity:**
   ```python
   import requests
   try:
       response = requests.get("https://generativelanguage.googleapis.com", timeout=10)
       print(f"Status: {response.status_code}")
   except Exception as e:
       print(f"Connection failed: {e}")
   ```

2. **Increase timeout for slow connections:**
   ```python
   # ADK uses default timeouts, but you can configure requests timeout
   import google.generativeai as genai
   genai.configure(api_key=your_key)
   ```

3. **If on corporate network:**
   - Try using mobile hotspot temporarily
   - Ask IT about API endpoint whitelisting
   - Check if VPN is required or if it should be disabled

4. **Check Google service status:**
   - Visit https://status.cloud.google.com/
   - Look for any ongoing incidents with AI/ML services

### Prevention

- Test connectivity before the workshop (48 hours ahead)
- Have a backup internet option (mobile hotspot)
- If on corporate network, verify API access with IT beforehand

### If Still Broken

1. Try a different network (mobile hotspot, different WiFi)
2. Disable VPN if using one
3. Wait a few minutes and retry (may be temporary)
4. Contact workshop instructor for alternative options

---

## Type/Validation Errors

### Symptom

```
TypeError: expected str instance, got NoneType
```

or

```
Function returns None instead of expected data
```

or

```
Agent doesn't call my tool / Tool not invoked
```

### Common Causes

1. **Missing return statement** - Function returns None by default
2. **Wrong parameter types** - Passing wrong types to functions
3. **Missing type hints** - ADK can't generate tool schema without type hints
4. **Poor docstring** - LLM doesn't understand when to use the tool
5. **Tool not added to agent** - Forgot to include tool in `tools=[]` list

### Resolution Steps

**For "Function returns None":**

1. Check your function has a `return` statement:
   ```python
   def search_flights(origin: str, destination: str) -> dict:
       # ... your code ...
       return {"status": "success", "flights": [...]}  # Must return!
   ```

**For "Tool not called by agent":**

1. Verify tool is in the agent's tools list:
   ```python
   agent = Agent(
       model='gemini-2.5-flash',
       name='my_agent',
       tools=[search_flights, search_hotels],  # Include your functions!
       ...
   )
   ```

2. Check your function has proper type hints:
   ```python
   def search_flights(
       origin: str,         # Type hint required
       destination: str,    # Type hint required
       date: str,           # Type hint required
   ) -> dict:               # Return type hint
   ```

3. Verify your docstring is descriptive:
   ```python
   def search_flights(origin: str, destination: str, date: str) -> dict:
       """
       Search for available flights between airports.

       Args:
           origin: Departure airport code (e.g., 'SFO', 'LAX')
           destination: Arrival airport code (e.g., 'NRT', 'CDG')
           date: Departure date in YYYY-MM-DD format

       Returns:
           Dictionary with flight results
       """
   ```

**For "Wrong type" errors:**

1. Check what the function expects vs what you're passing
2. Use print debugging to see actual values:
   ```python
   def search_flights(origin: str, destination: str) -> dict:
       print(f"DEBUG: origin={origin}, type={type(origin)}")
       print(f"DEBUG: destination={destination}, type={type(destination)}")
   ```

### Prevention

- Always include type hints on all function parameters
- Always include a descriptive docstring with Args and Returns
- Always have a `return` statement (never rely on implicit None)
- Test your functions directly before adding to agent

### If Still Broken

1. Test the function in isolation first (without the agent)
2. Check the solution cells in the notebook for reference
3. Print debug output to see what values are being passed

---

## RAG Errors

### Symptom

```
Corpus not found: projects/.../ragCorpora/...
```

or

```
No relevant results found for query
```

or

```
RAG retrieval returned empty results
```

### Common Causes

1. **RAG corpus not created** - The knowledge base doesn't exist yet
2. **Corpus ID mismatch** - Using wrong corpus ID in code
3. **Documents not indexed** - Content not yet processed into the corpus
4. **Query too specific** - No matching content in the knowledge base
5. **Indexing not complete** - Documents still being processed

### Resolution Steps

**For "Corpus not found":**

1. Verify RAG_CORPUS_ID is set correctly:
   ```python
   import os
   print(os.environ.get('RAG_CORPUS_ID', 'NOT SET'))
   ```

2. If using Vertex AI RAG, check the corpus exists:
   ```python
   from vertexai.preview import rag
   corpora = rag.list_corpora()
   for corpus in corpora:
       print(f"Corpus: {corpus.name}")
   ```

3. For workshop exercises, the RAG corpus may need to be created first (see Exercise 3)

**For "No relevant results":**

1. Check if documents are indexed:
   ```python
   from vertexai.preview import rag
   corpus = rag.get_corpus(name=RAG_CORPUS_ID)
   print(f"Document count: {corpus.document_count}")
   ```

2. Wait for indexing to complete (can take several minutes)

3. Try a broader query:
   ```python
   # Too specific:
   "What is the exact visa fee for Japan in 2026?"

   # Better:
   "Japan visa requirements"
   ```

**For workshop without RAG setup:**

1. The RAG features are introduced in Exercise 3
2. Before Exercise 3, RAG-related code will not work
3. Follow Exercise 3 setup instructions to create the corpus

### Prevention

- Complete Exercise 3 setup before using RAG features
- Allow 5-10 minutes for document indexing after upload
- Use the 48-hour pre-workshop validation to set up RAG corpus ahead of time

### If Still Broken

1. Re-run the RAG corpus creation steps
2. Verify documents uploaded successfully
3. Wait and retry (indexing takes time)
4. Ask instructor for pre-configured corpus ID

---

## State Errors

### Symptom

```
KeyError: 'user:preferred_airline'
```

or

```
State key not found: user:budget
```

or

```
NoneType has no attribute 'get'
```

### Common Causes

1. **Accessing state key before it's set** - Key doesn't exist yet
2. **Wrong key name** - Typo in state key name
3. **State not initialized** - Session state is empty
4. **Wrong state scope** - Using `user:` when should be `temp:` or vice versa

### Resolution Steps

**For "KeyError" when accessing state:**

1. Use optional access with default value:
   ```python
   # Wrong - raises KeyError if not set:
   budget = state["user:budget"]

   # Correct - returns None if not set:
   budget = state.get("user:budget")

   # Even better - provide default:
   budget = state.get("user:budget", 1000)
   ```

2. Check if key exists before accessing:
   ```python
   if "user:budget" in state:
       budget = state["user:budget"]
   else:
       budget = None
   ```

3. Use the ADK optional injection syntax in instructions:
   ```
   User budget: {user:budget?}
   ```
   The `?` makes the injection optional (won't error if not set)

**For "Wrong key" issues:**

1. Print current state to see what's available:
   ```python
   print("Current state keys:", list(state.keys()))
   ```

2. Verify key naming convention:
   - `user:` prefix for user preferences (persists)
   - `temp:` prefix for temporary data (current session only)
   - `app:` prefix for application settings

### Prevention

- Always use `.get()` with a default value when accessing state
- Use the `?` optional marker in instruction state injections: `{user:key?}`
- Initialize default state values at session start
- Document your state key naming convention

### If Still Broken

1. Print the entire state to debug:
   ```python
   async def debug_state(session_service, session_id):
       session = await session_service.get_session(
           app_name="my_app",
           user_id=user_id,
           session_id=session_id
       )
       print("Full state:", dict(session.state))
   ```

2. Re-run cells that set state values
3. Create a new session and start fresh

---

## Getting More Help

### Workshop Resources

- **Setup Guide:** [00-setup-verification.ipynb](00-setup-verification.ipynb)
- **Exercise 1:** [01-hello-agent.ipynb](01-hello-agent.ipynb)
- **Exercise 2:** [02-tools-functions.ipynb](02-tools-functions.ipynb)
- **Reference Implementation:** [reference-implementation/](reference-implementation/)

### Official Documentation

- **Google ADK Documentation:** https://google.github.io/adk-docs/
- **Google AI API Keys:** https://aistudio.google.com/apikey
- **Generative AI Python SDK:** https://github.com/google/generative-ai-python

### During the Workshop

If you're stuck during the workshop:

1. **Try the troubleshooting steps** in this guide first
2. **Check the solution cells** in the exercise notebooks
3. **Ask a neighbor** - they may have solved the same issue
4. **Raise your hand** for instructor help

### Debugging Tips

1. **Print debug output** in your functions to see what's happening:
   ```python
   print(f"DEBUG: Function called with {param1}, {param2}")
   ```

2. **Test functions in isolation** before adding to agents:
   ```python
   # Test directly
   result = search_flights("SFO", "NRT", "2026-03-15")
   print(result)
   ```

3. **Restart and re-run from top** if things get confusing:
   - Runtime > Restart runtime
   - Run all cells from the beginning

4. **Compare with solutions** in the collapsed solution cells

---

*Last updated: Workshop Phase 5*
