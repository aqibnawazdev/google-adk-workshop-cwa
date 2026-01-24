# Phase 3: RAG & Knowledge Integration - Research

**Researched:** 2026-01-24
**Domain:** Vertex AI RAG Engine, ADK RAG Integration, Travel Destination Knowledge, Workshop Education
**Confidence:** HIGH

## Summary

Phase 3 teaches Retrieval-Augmented Generation (RAG) by integrating Vertex AI RAG Engine with Google ADK agents to retrieve static destination knowledge. The research confirms that Vertex AI RAG Engine (GA as of 2026) provides a managed, production-ready platform for indexing documents and performing semantic search, seamlessly integrating with ADK through the `VertexAiRagRetrieval` tool.

The critical insight for workshop success is the **Tools vs RAG distinction** established in Phase 2: use function calling for real-time data (flights, hotels), use RAG for static knowledge (destination guides, visa requirements). Phase 3 reinforces this by demonstrating the complementary pattern - agents combine both capabilities to provide comprehensive travel recommendations.

The key technical challenge is **chunking strategy for travel content**. Travel guides contain heterogeneous content - narrative sections, lists, tables, maps - that require layout-aware chunking. Vertex AI RAG Engine's Document AI layout parser addresses this by detecting document structure (paragraphs, tables, headings) and creating context-aware chunks, significantly improving retrieval quality over naive character-based splitting.

For workshop delivery in 90 minutes, the **pre-indexed corpus pattern** is essential: instructors create and populate the RAG corpus with 10-15 destination guide PDFs before the workshop, participants only interact with the corpus through agent queries. This eliminates 15-20 minutes of corpus setup time and keeps focus on RAG integration patterns, not infrastructure.

**Primary recommendation:** Use Vertex AI RAG Engine with pre-indexed destination corpus (Tokyo, Paris, New York, etc.), integrate via `VertexAiRagRetrieval` tool with single-tool-only constraint, demonstrate layout-aware chunking with Document AI parser, and provide clear examples showing RAG retrieval + tool calling hybrid pattern for comprehensive travel recommendations.

## Standard Stack

The established stack for ADK RAG integration:

### Core
| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| google-adk | 1.23.0 | Agent framework | Built-in VertexAiRagRetrieval tool for RAG integration |
| Vertex AI RAG Engine | GA (v1) | Managed RAG backend | Production-ready, managed corpus/embeddings/vector search |
| Document AI Layout Parser | GA | PDF parsing with structure detection | Context-aware chunking for travel guides with tables/lists |
| textembedding-gecko@003 | Latest | Embedding model | Best balance of quality and speed for multilingual travel content |
| Gemini 2.5 Flash | Latest | LLM model | Fast generation combining RAG context with tool results |

### Supporting
| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| Google Cloud Storage | Current | PDF document storage | Host destination guide PDFs before importing to corpus |
| vertexai.preview.rag | Latest | RAG corpus API client | Create/manage corpora, import files programmatically |
| gcloud CLI | Current | Corpus management | Pre-workshop corpus setup via command line |

### Alternatives Considered
| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| Vertex AI RAG Engine | LangChain + Pinecone/Weaviate | More control but requires managing vector DB, embeddings, chunking manually |
| Document AI layout parser | Simple character/token chunking | Faster but loses structure context (tables, lists), worse retrieval quality |
| Pre-indexed corpus | Live corpus creation in workshop | Shows full workflow but consumes 15-20 min, complex for beginners |
| textembedding-gecko@003 | OpenAI embeddings | Vendor lock-in concern but Vertex AI native, multilingual support |

**Implementation Pattern:**
```python
# Source: https://google.github.io/adk-docs/tools/google-cloud/vertex-ai-rag-engine/
from google.adk.agents import Agent
from google.adk.tools.retrieval.vertex_ai_rag_retrieval import VertexAiRagRetrieval
from vertexai.preview import rag

# Configure RAG retrieval tool
destination_knowledge = VertexAiRagRetrieval(
    name='retrieve_destination_info',
    description='Retrieve destination information including visa requirements, attractions, weather, and cultural tips from travel guides.',
    rag_resources=[
        rag.RagResource(
            rag_corpus='projects/{project}/locations/{location}/ragCorpora/{corpus_id}'
        )
    ],
    similarity_top_k=5,  # Return top 5 most relevant chunks
    vector_distance_threshold=0.6,  # Filter low-confidence results
)

# IMPORTANT: RAG tool must be the ONLY tool on this agent instance
# For hybrid agents (tools + RAG), see Architecture Pattern 5
rag_agent = Agent(
    model='gemini-2.5-flash',
    name='destination_guide',
    description='Travel destination expert with knowledge base access.',
    instruction='You retrieve destination information from your knowledge base.',
    tools=[destination_knowledge],  # Only RAG tool
)
```

## Architecture Patterns

### Recommended Workshop Structure
```
03-rag-and-knowledge-integration.ipynb
├── Concept: What is RAG? (5 min)
│   ├── Static knowledge vs real-time data
│   └── When RAG complements function calling
├── Exercise 3A: Explore pre-indexed corpus (5 min)
│   ├── Query corpus via gcloud/API
│   └── Inspect chunk structure and metadata
├── Exercise 3B: Configure RAG retrieval tool (7 min)
│   ├── TODO: Set corpus resource path
│   ├── TODO: Configure similarity_top_k
│   └── TODO: Write tool description
├── Exercise 3C: Create RAG-only agent (5 min)
│   └── Agent with single RAG tool
├── Exercise 3D: Test destination queries (8 min)
│   ├── "What are visa requirements for Japan?"
│   ├── "Best time to visit Paris?"
│   └── "Cultural etiquette in Tokyo?"
├── Exercise 3E: Hybrid agent pattern (10 min)
│   ├── Combine flight search + destination knowledge
│   └── Multi-turn conversation showing both capabilities
└── Challenge: Improve retrieval quality (optional)
    └── Adjust similarity threshold and top_k
```

### Pattern 1: Pre-Indexed Corpus Setup (Instructor-Side)
**What:** Create and populate RAG corpus before workshop with destination guide PDFs
**When to use:** Workshop preparation (48 hours before)
**Example:**
```bash
# Source: https://docs.cloud.google.com/vertex-ai/generative-ai/docs/rag-engine/rag-quickstart
# Step 1: Create RAG corpus
curl -X POST \
  -H "Authorization: Bearer $(gcloud auth print-access-token)" \
  -H "Content-Type: application/json" \
  https://us-central1-aiplatform.googleapis.com/v1/projects/${PROJECT_ID}/locations/us-central1/ragCorpora \
  -d '{
    "display_name": "travel-destination-guides",
    "description": "Destination guides for workshop: Tokyo, Paris, New York, etc."
  }'

# Response includes corpus ID:
# projects/{project}/locations/us-central1/ragCorpora/{corpus_id}

# Step 2: Upload PDFs to GCS
gsutil cp destination-guides/*.pdf gs://${BUCKET_NAME}/destination-guides/

# Step 3: Import PDFs into corpus with layout parsing
curl -X POST \
  -H "Authorization: Bearer $(gcloud auth print-access-token)" \
  -H "Content-Type: application/json" \
  https://us-central1-aiplatform.googleapis.com/v1/projects/${PROJECT_ID}/locations/us-central1/ragCorpora/${CORPUS_ID}/ragFiles:import \
  -d '{
    "import_rag_files_config": {
      "gcs_source": {
        "uris": ["gs://'${BUCKET_NAME}'/destination-guides/*.pdf"]
      },
      "rag_file_chunking_config": {
        "chunk_size": 1024,
        "chunk_overlap": 256
      },
      "rag_file_parsing_config": {
        "use_advanced_pdf_parsing": true  # Enables Document AI layout parser
      },
      "max_embedding_requests_per_min": 1000
    }
  }'

# Indexing takes 5-10 minutes for 10-15 PDFs
# Verify completion:
gcloud ai rag-corpora describe ${CORPUS_ID} --location=us-central1
```

### Pattern 2: Layout-Aware Chunking for Travel Guides
**What:** Use Document AI layout parser to preserve document structure in chunks
**When to use:** When travel guides contain tables, lists, and structured content
**Why critical:** Naive character-based chunking splits mid-table or mid-list, destroying context; layout parser detects structural elements and creates semantically meaningful chunks
**Example:**
```python
# Source: https://docs.cloud.google.com/vertex-ai/generative-ai/docs/rag-engine/layout-parser-integration
# Document structure (Tokyo guide):
"""
# Tokyo Travel Guide

## Visa Requirements
- US citizens: Visa-free for up to 90 days
- Valid passport required
- Return ticket may be requested at immigration

## Top Attractions
| Attraction | District | Entry Fee | Best Time |
|------------|----------|-----------|-----------|
| Senso-ji Temple | Asakusa | Free | Early morning |
| Tokyo Skytree | Sumida | ¥2,100 | Sunset |
| Shibuya Crossing | Shibuya | Free | Evening |

## Weather by Season
Spring (Mar-May): 10-20°C, cherry blossoms peak early April
Summer (Jun-Aug): 25-35°C, humid, rainy season in June
...
"""

# WITHOUT layout parser (bad):
# Chunk might split mid-table:
"""
...
| Attraction | District | Entry Fee | Best Time |
|------------|----------|-----------|-----------|
| Senso-ji Temple | Asakusa | Free | Early morning |
| Tokyo Skyt
"""
# Next chunk starts: "ree | Sumida | ¥2,100 | Sunset |"
# Table structure lost, unusable for retrieval

# WITH layout parser (good):
# Chunk 1: Full "Visa Requirements" section with complete list
# Chunk 2: Full attractions table with all rows intact
# Chunk 3: Full weather section with seasonal details
# Layout parser detects list/table boundaries, preserves structure
```

**Configuration:**
```python
# In corpus import config
"rag_file_parsing_config": {
    "use_advanced_pdf_parsing": true  # Enables Document AI layout parser
}

# Default chunk_size: 1024 tokens (~800 words)
# Default chunk_overlap: 256 tokens (~200 words)
# These defaults work well for travel guides with mixed content
```

### Pattern 3: VertexAiRagRetrieval Tool Configuration
**What:** Configure RAG retrieval tool with corpus reference and retrieval parameters
**When to use:** Exercise 3B in workshop
**Example:**
```python
# Source: https://google.github.io/adk-docs/tools/google-cloud/vertex-ai-rag-engine/
from google.adk.tools.retrieval.vertex_ai_rag_retrieval import VertexAiRagRetrieval
from vertexai.preview import rag
import os

# Configure RAG tool
destination_knowledge = VertexAiRagRetrieval(
    name='retrieve_destination_info',

    # Description helps LLM decide when to use this tool
    description='''Retrieve destination information from travel guide knowledge base.

    Use this tool to answer questions about:
    - Visa requirements and entry rules
    - Top attractions and landmarks
    - Weather and best time to visit
    - Cultural tips and local customs
    - Safety information and travel advisories
    - Transportation and getting around
    - Food and dining recommendations

    DO NOT use this tool for:
    - Real-time flight or hotel availability (use search tools instead)
    - Current pricing or booking status
    - Live event schedules
    ''',

    # Corpus reference (from pre-indexed corpus)
    rag_resources=[
        rag.RagResource(
            rag_corpus=os.environ.get('RAG_CORPUS_ID')
            # Format: projects/{project}/locations/{location}/ragCorpora/{corpus_id}
        )
    ],

    # Retrieval parameters
    similarity_top_k=5,  # Return top 5 most relevant chunks
    vector_distance_threshold=0.6,  # Filter results with similarity < 0.6
)

# CRITICAL CONSTRAINT: This tool can ONLY be used alone in an agent
# Cannot mix with function calling tools in same agent instance
# See Pattern 5 for hybrid approach
```

**Parameter tuning guidance:**
- `similarity_top_k`: Start with 5, increase to 10 if answers lack detail, decrease to 3 if too much irrelevant context
- `vector_distance_threshold`: 0.6 is default, lower (0.4) for more permissive retrieval, higher (0.8) for stricter relevance
- For workshop: Use defaults (5, 0.6) to avoid complexity

### Pattern 4: RAG-Only Agent (Exercise 3C)
**What:** Create agent with only RAG retrieval tool for destination queries
**When to use:** Teaching RAG concepts in isolation before hybrid patterns
**Example:**
```python
# Source: ADK best practices
from google.adk.agents import Agent

# RAG-only agent (constrained to knowledge base)
destination_expert = Agent(
    model='gemini-2.5-flash',
    name='destination_expert',
    description='Expert on travel destinations with access to destination guide knowledge base.',

    instruction='''You are a travel destination expert.

YOUR KNOWLEDGE:
- You have access to detailed destination guides covering visa requirements,
  attractions, weather, cultural tips, and travel advice
- Use your retrieve_destination_info tool to answer questions about destinations
- Always cite specific information from the guides when available

LIMITATIONS:
- You CANNOT search for flights or hotels (no real-time availability)
- You CANNOT provide current pricing or booking information
- Your knowledge is from travel guides (static), not live data

HOW TO HELP:
1. When asked about a destination, use your retrieval tool to find relevant information
2. Provide comprehensive answers combining information from multiple guide sections
3. If the guide doesn't cover a topic, say so honestly
4. Recommend using booking tools for real-time availability and pricing

Be informative, encouraging, and help travelers prepare for their trips.''',

    tools=[destination_knowledge],  # ONLY RAG tool (constraint)
)

# Test RAG retrieval
response = destination_expert.generate_content(
    "What are the visa requirements for US citizens traveling to Japan? "
    "And what's the best time to visit for cherry blossoms?"
)
print(response.text)
# Expected: Agent retrieves from corpus, cites visa-free 90-day rule and
# early April cherry blossom season from Tokyo guide
```

### Pattern 5: Hybrid Agent with Tools + RAG (Exercise 3E)
**What:** Combine function calling tools and RAG knowledge in coordinated agent system
**When to use:** Demonstrating real-world pattern where agent uses both real-time and static data
**Why complex:** ADK constraint - VertexAiRagRetrieval cannot be mixed with other tools in same agent instance
**Workaround:** Use multi-agent coordination or sequential tool usage
**Example:**
```python
# Source: Workshop best practices (addressing ADK limitation)
# Option 1: Sequential approach (simpler for workshop)
from google.adk.agents import Agent

# Agent 1: Tool-based agent (flights, hotels)
booking_agent = Agent(
    model='gemini-2.5-flash',
    name='booking_agent',
    description='Search for flights and hotels.',
    instruction='Use your tools to find real-time availability and pricing.',
    tools=[search_flights, search_hotels],  # From Phase 2
)

# Agent 2: RAG-based agent (destination knowledge)
destination_agent = Agent(
    model='gemini-2.5-flash',
    name='destination_agent',
    description='Provide destination information from knowledge base.',
    instruction='Retrieve destination guides to answer travel questions.',
    tools=[destination_knowledge],  # RAG only
)

# Orchestration logic (in notebook or wrapper)
def hybrid_travel_assistant(user_query: str) -> str:
    """
    Route queries to appropriate agent based on content.
    Combine results for comprehensive recommendations.
    """
    # Simple routing based on keywords
    if any(word in user_query.lower() for word in ['flight', 'hotel', 'book', 'search', 'availability']):
        # Real-time search needed
        booking_result = booking_agent.generate_content(user_query)

        # Extract destination from query (simplified)
        if 'tokyo' in user_query.lower():
            # Enrich with destination knowledge
            guide_query = "What should I know about visiting Tokyo?"
            guide_result = destination_agent.generate_content(guide_query)

            return f"{booking_result.text}\n\n**Destination Tips:**\n{guide_result.text}"

        return booking_result.text

    else:
        # Knowledge base query
        return destination_agent.generate_content(user_query).text

# Test hybrid pattern
print(hybrid_travel_assistant(
    "Find me flights from SFO to Tokyo on March 15, budget $900"
))
# Expected: Flight results + Tokyo travel tips (visa, attractions, weather)

print(hybrid_travel_assistant(
    "What are cultural customs I should know when visiting Tokyo?"
))
# Expected: RAG retrieval from Tokyo destination guide
```

**Workshop note:** Explain this pattern explicitly in Exercise 3E. Participants need to understand:
1. Why the limitation exists (ADK architecture constraint)
2. How to work around it (sequential agents, routing logic)
3. When this matters (production systems with tools + RAG)

### Pattern 6: Destination Guide Content Structure
**What:** Standardized structure for destination guide PDFs to ensure consistent retrieval
**When to use:** Creating/curating destination guides for workshop corpus
**Example structure:**
```markdown
# [City Name] Travel Guide

## Quick Facts
- Country: ...
- Language: ...
- Currency: ...
- Time zone: ...
- Emergency number: ...

## Visa Requirements
[Structured by nationality]
- US citizens: ...
- EU citizens: ...
- Requirements: ...

## Best Time to Visit
[Seasonal breakdown]
- Spring (Mar-May): Weather, crowds, events
- Summer (Jun-Aug): ...
- Fall (Sep-Nov): ...
- Winter (Dec-Feb): ...

## Top Attractions
[Table format preferred - layout parser preserves]
| Attraction | District | Entry Fee | Hours | Best Time |
|------------|----------|-----------|-------|-----------|
| [Name] | [Area] | [Price] | [Schedule] | [Recommendation] |

## Neighborhoods & Districts
[Section per major area]
### [District Name]
- Character: ...
- Must-see: ...
- Food: ...
- Transport: ...

## Food & Dining
- Signature dishes: ...
- Where to eat: ...
- Price ranges: ...
- Dietary restrictions: ...

## Transportation
- From airport: ...
- Public transit: ...
- Taxis/ride-share: ...
- Walking/biking: ...

## Cultural Tips & Customs
- Greetings: ...
- Tipping: ...
- Dress code: ...
- Do's and don'ts: ...

## Safety & Health
- Safe areas: ...
- Areas to avoid: ...
- Health precautions: ...
- Travel insurance: ...

## Practical Information
- Electricity: ...
- Internet/SIM cards: ...
- Money/ATMs: ...
- Business hours: ...
```

**Why this structure works:**
- Consistent sections across all destination guides enable reliable retrieval
- Tables preserved by layout parser maintain structured data
- Hierarchical headings create natural chunk boundaries
- Bullet points and lists stay intact in chunks
- Covers all common traveler questions (visa, weather, attractions, culture)

**Workshop corpus recommendation:** 10-15 destinations covering:
- Major Asian cities: Tokyo, Singapore, Bangkok
- European cities: Paris, London, Rome
- North American cities: New York, San Francisco, Toronto
- Diverse visa requirements and cultural contexts
- 8-12 pages per guide (manageable chunk count)

### Anti-Patterns to Avoid

- **Mixing RAG tool with function calling tools in same agent**: Violates ADK constraint, will fail at runtime
- **Corpus creation during workshop time**: Consumes 15-20 minutes, adds complexity, risks failures
- **Character-based chunking for structured documents**: Destroys tables and lists, degrades retrieval quality
- **No chunk overlap**: Loses context at chunk boundaries, misses information spanning sections
- **Vague RAG tool descriptions**: LLM doesn't know when to use RAG vs tools, calls wrong capability
- **No similarity threshold**: Returns irrelevant chunks, pollutes context, wastes tokens
- **Unstructured destination guides**: Inconsistent formats make retrieval unpredictable
- **Large chunk size (>1500 tokens)**: Dilutes semantic density, worse embedding quality
- **Small chunk size (<500 tokens)**: Fragments context, loses narrative flow

## Don't Hand-Roll

Problems that look simple but have existing solutions:

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Vector database management | Custom Pinecone/Weaviate setup | Vertex AI RAG Engine managed vector DB | Fully managed, auto-scaling, integrated with Gemini |
| PDF parsing and chunking | PyPDF2 + character splitting | Document AI layout parser | Preserves structure (tables, lists), context-aware chunks |
| Embedding generation | OpenAI API or local models | textembedding-gecko@003 | Vertex AI native, multilingual, optimized for search |
| Similarity search | Manual cosine similarity | RAG Engine retrieval API | Optimized indexing, filtering, caching |
| Corpus version control | Custom document versioning | RAG corpus import/update API | Built-in file management, metadata tracking |
| Retrieval evaluation | Custom metrics | Vertex AI Model Evaluation | Standardized RAG metrics (faithfulness, relevance, citation) |

**Key insight:** Vertex AI RAG Engine is production-ready managed service. Don't rebuild infrastructure - focus workshop time on integration patterns, query optimization, and hybrid agent design.

## Common Pitfalls

### Pitfall 1: Ignoring Single-Tool Constraint for VertexAiRagRetrieval
**What goes wrong:** Attempt to add VertexAiRagRetrieval alongside search_flights/search_hotels in same agent, runtime error or incorrect behavior
**Why it happens:**
- ADK documentation mentions constraint but easy to miss
- Natural assumption: "Just add RAG to list of tools"
- Phase 2 pattern (multiple tools) doesn't extend to RAG
**How to avoid:**
- Teach constraint explicitly in Exercise 3C introduction
- Show working example of RAG-only agent first
- Demonstrate hybrid pattern (Pattern 5) with separate agents
- Include troubleshooting: "If you see [error], check tool list"
**Warning signs:**
- Error: "VertexAiRagRetrieval tool cannot be combined with other tools"
- Agent calls tools but never triggers RAG retrieval
- Unexpected tool selection behavior
**Code example:**
```python
# ❌ BAD: Mixing RAG with function calling tools
agent = Agent(
    model='gemini-2.5-flash',
    tools=[
        search_flights,  # Function calling tool
        search_hotels,   # Function calling tool
        destination_knowledge,  # VertexAiRagRetrieval - VIOLATION
    ],
)
# Runtime error or unpredictable behavior

# ✅ GOOD: Separate agents
tools_agent = Agent(tools=[search_flights, search_hotels])
rag_agent = Agent(tools=[destination_knowledge])
```

### Pitfall 2: Character-Based Chunking Destroys Document Structure
**What goes wrong:** Travel guides chunked by character count split mid-table or mid-list, retrieval returns incomplete/unusable information
**Why it happens:**
- Default chunking often character-based (simple to implement)
- Looks fine in text files but fails on structured PDFs
- Problem invisible until testing retrieval quality
**How to avoid:**
- Always enable Document AI layout parser for PDFs: `"use_advanced_pdf_parsing": true`
- Test with sample queries that need table data: "What are entry fees for Tokyo attractions?"
- Inspect chunks after indexing - verify tables/lists intact
- Use structured destination guide template (Pattern 6)
**Warning signs:**
- Retrieved chunks show half a table row
- List items cut off mid-sentence
- Agent says "information not found" when it's in guide but split across chunks
**Example:**
```python
# ❌ BAD: Character-based chunking config
"rag_file_chunking_config": {
    "chunk_size": 1000,  # Characters, not aware of structure
    "chunk_overlap": 100
}
# No layout parsing enabled

# Result: Table split mid-row
"""
...| Tokyo Skytree | Sumida | ¥2,
"""
# Next chunk: """100 | Sunset |..."""

# ✅ GOOD: Layout-aware chunking
"rag_file_chunking_config": {
    "chunk_size": 1024,  # Tokens (smarter)
    "chunk_overlap": 256
},
"rag_file_parsing_config": {
    "use_advanced_pdf_parsing": true  # Document AI layout parser
}

# Result: Complete table in single chunk
"""
| Attraction | District | Entry Fee | Best Time |
|------------|----------|-----------|-----------|
| Senso-ji Temple | Asakusa | Free | Early morning |
| Tokyo Skytree | Sumida | ¥2,100 | Sunset |
| Shibuya Crossing | Shibuya | Free | Evening |
"""
```

### Pitfall 3: Corpus Indexing During Workshop Time
**What goes wrong:** Workshop starts, participants wait 10-15 minutes for corpus to index, time pressure builds, errors compound
**Why it happens:**
- Want to show "full RAG workflow" including corpus creation
- Underestimate indexing time (varies with PDF count/size)
- Network issues during upload cause failures
**How to avoid:**
- Pre-index corpus 48+ hours before workshop (Pattern 1)
- Provide read-only corpus access to participants
- Exercise 3A: explore pre-indexed corpus (5 min) instead of creating (20 min)
- Save corpus creation for "What's Next" bonus content
**Warning signs:**
- Workshop timeline shows corpus creation during session
- No pre-workshop validation of corpus availability
- Participants need write access to create corpora
**Better approach:**
```python
# ❌ BAD: Workshop includes corpus creation
# Exercise 3A (20 minutes): Create RAG corpus
# - Create corpus via API (5 min)
# - Upload PDFs to GCS (5 min)
# - Import files to corpus (2 min)
# - Wait for indexing (10-15 min) ← kills timeline
# - Test retrieval (3 min)

# ✅ GOOD: Pre-indexed corpus exploration
# Exercise 3A (5 minutes): Explore pre-indexed corpus
# - Instructor shares corpus ID
# - Participants query corpus metadata
# - Inspect sample chunks and structure
# - Proceed to tool integration (Exercise 3B)
# Corpus creation shown as bonus/homework
```

### Pitfall 4: No Similarity Threshold Filtering
**What goes wrong:** RAG returns chunks with low semantic similarity, pollutes context with irrelevant information, agent generates confused responses
**Why it happens:**
- Default behavior returns top_k chunks regardless of relevance
- Corpus contains diverse destinations, query matches weakly across many
- No quality gate on retrieval results
**How to avoid:**
- Set `vector_distance_threshold=0.6` (default recommended value)
- Test with off-topic queries: "What are visa requirements for Mars?"
- Agent should say "no information found" rather than hallucinating
- Exercise 3F (challenge): tune threshold, observe quality changes
**Warning signs:**
- Agent answers Tokyo questions with Paris guide content
- Retrieved chunks mention destination but unrelated topics
- Agent prefixes with "Based on the information provided..." but answer is wrong
**Code example:**
```python
# ❌ BAD: No filtering
destination_knowledge = VertexAiRagRetrieval(
    name='retrieve_destination_info',
    description='...',
    rag_resources=[rag.RagResource(rag_corpus=corpus_id)],
    similarity_top_k=10,  # Returns top 10 regardless of relevance
    # Missing: vector_distance_threshold
)

# Query: "Visa requirements for Tokyo"
# Returns: Chunks about Paris visas (0.3 similarity), NYC attractions (0.25),
#          Tokyo weather (0.8), Tokyo visas (0.9), Bangkok culture (0.2)
# Agent confused by irrelevant Paris/NYC/Bangkok chunks

# ✅ GOOD: Threshold filtering
destination_knowledge = VertexAiRagRetrieval(
    name='retrieve_destination_info',
    description='...',
    rag_resources=[rag.RagResource(rag_corpus=corpus_id)],
    similarity_top_k=10,  # Request 10 candidates
    vector_distance_threshold=0.6,  # Filter to similarity >= 0.6
)

# Same query now returns only: Tokyo weather (0.8), Tokyo visas (0.9)
# Low-quality matches filtered out, cleaner context
```

### Pitfall 5: Vague RAG Tool Descriptions
**What goes wrong:** LLM calls RAG tool for real-time queries (flights, pricing) or calls search tools for static knowledge (visa rules)
**Why it happens:**
- Tool description doesn't clearly delineate RAG vs tools boundary
- LLM guesses based on generic "retrieve information" description
- Phase 2 vs Phase 3 distinction not reinforced in tool metadata
**How to avoid:**
- Explicit DO/DO NOT sections in RAG tool description (Pattern 3)
- Contrast with function tool descriptions: "real-time" vs "knowledge base"
- Test with ambiguous queries: "How do I get to Tokyo?" (could be flight search OR transportation guide)
- Agent instruction should also clarify: "Use RAG for static knowledge, tools for real-time data"
**Warning signs:**
- Agent uses RAG to answer "Find me flights to Tokyo" (should use search_flights)
- Agent uses search_hotels for "What neighborhoods should I stay in Tokyo?" (should use RAG)
- No clear pattern to tool selection
**Code example:**
```python
# ❌ BAD: Vague description
destination_knowledge = VertexAiRagRetrieval(
    name='retrieve_destination_info',
    description='Get information about travel destinations.',
    # Unclear: What kind of information? When to use vs search tools?
    ...
)

# ✅ GOOD: Explicit DO/DO NOT
destination_knowledge = VertexAiRagRetrieval(
    name='retrieve_destination_info',
    description='''Retrieve destination information from travel guide knowledge base.

    Use this tool to answer questions about:
    - Visa requirements and entry rules (static policy)
    - Top attractions and landmarks (guide recommendations)
    - Weather and best time to visit (seasonal patterns)
    - Cultural tips and local customs (etiquette, traditions)
    - Transportation within city (how to get around)
    - Food recommendations and local cuisine

    DO NOT use this tool for:
    - Real-time flight or hotel availability → use search_flights/search_hotels
    - Current pricing or booking status → use search tools
    - Live event schedules or availability → real-time data not in guides

    This tool searches static destination guides, not live databases.''',
    ...
)
```

### Pitfall 6: Not Testing Retrieval Quality Before Workshop
**What goes wrong:** Workshop starts, retrieval returns wrong chunks, agent gives bad answers, no time to fix corpus
**Why it happens:**
- Corpus created and indexed but never tested with sample queries
- Assume "indexing succeeded" means "retrieval works well"
- Discovery during live workshop too late
**How to avoid:**
- Pre-workshop validation checklist (48 hours before):
  - Create test queries covering all destination guides
  - Verify retrieved chunks are relevant and complete
  - Check tables/lists intact in chunks
  - Test similarity threshold filtering
  - Validate agent responses using retrieved context
- Exercise 3A should include validation step
**Warning signs:**
- No documented test queries in workshop prep
- First time testing retrieval is during Exercise 3D
- Participants discover broken retrieval together
**Validation script:**
```python
# Pre-workshop validation (instructor runs 48h before)
from google.adk.tools.retrieval.vertex_ai_rag_retrieval import VertexAiRagRetrieval
from vertexai.preview import rag

# Configure tool
tool = VertexAiRagRetrieval(
    name='test_retrieval',
    description='Test',
    rag_resources=[rag.RagResource(rag_corpus=CORPUS_ID)],
    similarity_top_k=5,
    vector_distance_threshold=0.6,
)

# Test queries (one per destination guide)
test_queries = [
    "What are visa requirements for US citizens visiting Japan?",
    "Best time to visit Paris for cherry blossoms?",  # Should fail - Paris has no cherry blossoms
    "Top attractions in New York City",
    "Cultural customs in Tokyo",
    "How to get from airport to city center in Singapore",
]

for query in test_queries:
    print(f"\n🔍 Query: {query}")
    # Manual retrieval test
    # In real workshop, agent calls this automatically
    # Here we verify chunks directly
    # (Simplified - actual API call needed)
    print("✓ Retrieval successful" if check_retrieval(query) else "✗ Retrieval failed")

# Expected results:
# ✓ Japan visa query → returns relevant chunks from Tokyo guide
# ✗ Paris cherry blossoms → no relevant results (threshold filters low matches)
# ✓ NYC attractions → returns table from New York guide intact
# etc.
```

### Pitfall 7: Confusing Tools vs RAG Use Cases
**What goes wrong:** Participants don't internalize decision framework, try to use RAG for real-time data or tools for static knowledge
**Why it happens:**
- Phase 2 and Phase 3 taught separately without reinforcing contrast
- No explicit decision tree provided
- Hybrid pattern (Phase 3E) not emphasized enough
**How to avoid:**
- Start Phase 3 by reviewing Tools vs RAG decision matrix (from Phase 2 research)
- Every exercise includes comment: "Why RAG not tools for this query?"
- Exercise 3E explicitly tests understanding: participants predict tool/RAG before execution
- Provide decision flowchart in notebook
**Teaching moment:**
```markdown
## Tools vs RAG Decision Flowchart

User query
    ↓
Does this need REAL-TIME data?
(prices, availability, current status)
    ↓
   YES → Use FUNCTION CALLING TOOLS
         (search_flights, search_hotels)
    ↓
    NO → Is this STATIC KNOWLEDGE?
          (guides, policies, cultural info)
    ↓
   YES → Use RAG RETRIEVAL
         (destination_knowledge)
    ↓
    NO → General knowledge
          LLM can answer directly

Examples:
✓ "Find flights to Tokyo" → Tools (real-time availability)
✓ "What's Tokyo like in spring?" → RAG (static seasonal guide)
✓ "Book a hotel in Shibuya under $200/night" → Tools (real-time pricing)
✓ "What are visa requirements for Japan?" → RAG (static policy)
✓ "What's 2+2?" → Direct LLM (no tool/RAG needed)
```

## Code Examples

Verified patterns from official sources and workshop best practices:

### Complete Pre-Workshop Corpus Setup Script
```bash
# Source: https://docs.cloud.google.com/vertex-ai/generative-ai/docs/rag-engine/rag-quickstart
# Run 48 hours before workshop

#!/bin/bash
set -e

# Configuration
PROJECT_ID="your-workshop-project"
LOCATION="us-central1"
CORPUS_NAME="travel-destination-guides"
BUCKET_NAME="${PROJECT_ID}-destination-guides"
GUIDES_DIR="./destination-guides-pdfs"

echo "🚀 Setting up RAG corpus for workshop..."

# 1. Create GCS bucket for PDFs
echo "📦 Creating GCS bucket..."
gsutil mb -p ${PROJECT_ID} -l ${LOCATION} gs://${BUCKET_NAME}/

# 2. Upload destination guide PDFs
echo "📄 Uploading destination guides..."
gsutil -m cp ${GUIDES_DIR}/*.pdf gs://${BUCKET_NAME}/guides/

# 3. Create RAG corpus
echo "🗄️ Creating RAG corpus..."
CORPUS_RESPONSE=$(curl -s -X POST \
  -H "Authorization: Bearer $(gcloud auth print-access-token)" \
  -H "Content-Type: application/json" \
  https://${LOCATION}-aiplatform.googleapis.com/v1/projects/${PROJECT_ID}/locations/${LOCATION}/ragCorpora \
  -d '{
    "display_name": "'${CORPUS_NAME}'",
    "description": "Destination guides for ADK workshop: Tokyo, Paris, NYC, Singapore, etc."
  }')

CORPUS_ID=$(echo ${CORPUS_RESPONSE} | jq -r '.name' | awk -F'/' '{print $NF}')
echo "✓ Corpus created: ${CORPUS_ID}"

# 4. Import PDFs into corpus with layout parsing
echo "📚 Importing PDFs to corpus (this takes 5-10 minutes)..."
curl -X POST \
  -H "Authorization: Bearer $(gcloud auth print-access-token)" \
  -H "Content-Type: application/json" \
  https://${LOCATION}-aiplatform.googleapis.com/v1/projects/${PROJECT_ID}/locations/${LOCATION}/ragCorpora/${CORPUS_ID}/ragFiles:import \
  -d '{
    "import_rag_files_config": {
      "gcs_source": {
        "uris": ["gs://'${BUCKET_NAME}'/guides/*.pdf"]
      },
      "rag_file_chunking_config": {
        "chunk_size": 1024,
        "chunk_overlap": 256
      },
      "rag_file_parsing_config": {
        "use_advanced_pdf_parsing": true
      },
      "max_embedding_requests_per_min": 1000
    }
  }'

echo "⏳ Indexing in progress..."
echo "   Check status: gcloud ai rag-corpora describe ${CORPUS_ID} --location=${LOCATION}"

# 5. Save corpus ID for workshop
FULL_CORPUS_ID="projects/${PROJECT_ID}/locations/${LOCATION}/ragCorpora/${CORPUS_ID}"
echo "${FULL_CORPUS_ID}" > corpus-id.txt
echo "✅ Corpus ID saved to corpus-id.txt"
echo "   Share with participants: ${FULL_CORPUS_ID}"

# 6. Test retrieval (wait for indexing to complete first)
echo "🔍 Test retrieval after indexing completes..."
echo "   Sample query: 'What are visa requirements for Japan?'"
```

### RAG Retrieval Tool with Error Handling
```python
# Source: Workshop best practices
from google.adk.tools.retrieval.vertex_ai_rag_retrieval import VertexAiRagRetrieval
from vertexai.preview import rag
import os

def create_destination_knowledge_tool():
    """
    Create VertexAiRagRetrieval tool for destination guides.

    Returns configured RAG retrieval tool.
    Raises ValueError if RAG_CORPUS_ID not set.
    """
    corpus_id = os.environ.get('RAG_CORPUS_ID')
    if not corpus_id:
        raise ValueError(
            "RAG_CORPUS_ID environment variable not set. "
            "Expected format: projects/{project}/locations/{location}/ragCorpora/{corpus_id}"
        )

    try:
        tool = VertexAiRagRetrieval(
            name='retrieve_destination_info',

            description='''Retrieve destination information from travel guide knowledge base.

            Use this tool to answer questions about:
            - Visa requirements and entry rules
            - Top attractions and landmarks
            - Weather and best time to visit
            - Cultural tips and local customs
            - Safety information
            - Transportation within city
            - Food and dining recommendations

            DO NOT use for real-time flight/hotel search or current pricing.''',

            rag_resources=[
                rag.RagResource(rag_corpus=corpus_id)
            ],

            similarity_top_k=5,
            vector_distance_threshold=0.6,
        )

        print(f"✓ RAG tool configured with corpus: {corpus_id}")
        return tool

    except Exception as e:
        raise RuntimeError(f"Failed to create RAG tool: {str(e)}")

# Usage in workshop notebook
destination_knowledge = create_destination_knowledge_tool()
```

### RAG-Only Agent (Exercise 3C)
```python
# Source: ADK patterns
from google.adk.agents import Agent
from google.adk.tools.retrieval.vertex_ai_rag_retrieval import VertexAiRagRetrieval
from vertexai.preview import rag
import os

# Create RAG tool
destination_knowledge = VertexAiRagRetrieval(
    name='retrieve_destination_info',
    description='''Retrieve destination guide information.

    Covers: visa requirements, attractions, weather, cultural tips, safety,
    transportation, food recommendations.

    Do NOT use for real-time bookings or current pricing.''',
    rag_resources=[
        rag.RagResource(rag_corpus=os.environ['RAG_CORPUS_ID'])
    ],
    similarity_top_k=5,
    vector_distance_threshold=0.6,
)

# Create RAG-only agent
destination_expert = Agent(
    model='gemini-2.5-flash',
    name='destination_expert',
    description='Travel destination expert with knowledge base access.',

    instruction='''You are a travel destination expert with access to comprehensive destination guides.

YOUR CAPABILITIES:
- Retrieve information from destination guides using your tool
- Answer questions about visa requirements, attractions, weather, culture
- Provide practical travel advice based on guide content
- Cite specific information from guides when available

YOUR LIMITATIONS:
- You CANNOT search for flights or hotels (no real-time booking data)
- You CANNOT provide current prices or availability
- Your knowledge comes from static guides, not live sources

HOW TO HELP:
1. Use retrieve_destination_info tool for all destination-related queries
2. Combine information from multiple guide sections for comprehensive answers
3. If guide doesn't cover a topic, admit this honestly
4. Suggest using booking tools for real-time availability

Be informative, encouraging, and help travelers prepare confidently.''',

    tools=[destination_knowledge],  # ONLY RAG tool
)

# Test queries
test_queries = [
    "What are the visa requirements for US citizens traveling to Japan?",
    "What's the best time to visit Paris?",
    "What cultural customs should I know before visiting Tokyo?",
    "What are the top attractions in New York City?",
]

print("=" * 60)
print("Destination Expert Agent - RAG Retrieval Demo")
print("=" * 60)

for query in test_queries:
    print(f"\n🧑 You: {query}")
    response = destination_expert.generate_content(query)
    print(f"🤖 Agent: {response.text}")
    print("-" * 60)
```

### Hybrid Agent Pattern - Sequential Coordination
```python
# Source: Workshop Pattern 5 (addressing ADK single-tool constraint)
from google.adk.agents import Agent

# Agent 1: Tool-based (real-time booking)
booking_agent = Agent(
    model='gemini-2.5-flash',
    name='booking_agent',
    description='Search flights and hotels with real-time availability.',
    instruction='''You search for flights and hotels using your tools.

    Always ask for required details: origin, destination, dates, passengers/guests.
    Filter by budget if user mentions price limits.
    Present 2-3 best options with prices and key details.''',
    tools=[search_flights, search_hotels],  # From Phase 2
)

# Agent 2: RAG-based (static knowledge)
destination_agent = Agent(
    model='gemini-2.5-flash',
    name='destination_agent',
    description='Provide destination information from knowledge base.',
    instruction='''You retrieve destination guide information.

    Use your tool to answer questions about visa requirements, attractions,
    weather, culture, safety, and practical travel tips.
    Cite specific sections from guides when available.''',
    tools=[destination_knowledge],  # RAG only
)

# Orchestrator function
def travel_assistant(user_query: str) -> str:
    """
    Hybrid travel assistant combining booking tools and destination knowledge.

    Routes query to appropriate agent, enriches booking results with destination tips.
    """
    query_lower = user_query.lower()

    # Detect booking intent
    booking_keywords = ['flight', 'hotel', 'book', 'search', 'availability',
                        'reserve', 'find', 'price', 'cost']
    needs_booking = any(keyword in query_lower for keyword in booking_keywords)

    # Detect destination knowledge intent
    knowledge_keywords = ['visa', 'require', 'weather', 'season', 'attraction',
                          'culture', 'custom', 'tip', 'safety', 'best time']
    needs_knowledge = any(keyword in query_lower for keyword in knowledge_keywords)

    if needs_booking:
        # Get booking results
        print("🔧 Calling booking agent...")
        booking_response = booking_agent.generate_content(user_query)

        # Extract destination from query (simplified - production would use NER)
        destinations = {
            'tokyo': 'Tokyo', 'japan': 'Tokyo',
            'paris': 'Paris', 'france': 'Paris',
            'new york': 'New York', 'nyc': 'New York',
            'singapore': 'Singapore',
        }

        destination = None
        for keyword, city in destinations.items():
            if keyword in query_lower:
                destination = city
                break

        # Enrich with destination tips if destination detected
        if destination:
            print(f"📚 Enriching with {destination} destination knowledge...")
            guide_query = f"What should I know about visiting {destination}? Provide top 3 tips."
            guide_response = destination_agent.generate_content(guide_query)

            return (
                f"{booking_response.text}\n\n"
                f"**✈️ {destination} Travel Tips:**\n{guide_response.text}"
            )

        return booking_response.text

    elif needs_knowledge:
        # Pure knowledge query
        print("📚 Calling destination agent...")
        return destination_agent.generate_content(user_query).text

    else:
        # General query - route to booking agent as default
        print("🔧 Routing to booking agent...")
        return booking_agent.generate_content(user_query).text

# Test hybrid pattern
print("=" * 60)
print("Hybrid Travel Assistant Demo")
print("=" * 60)

# Test 1: Booking with enrichment
print("\n" + "=" * 60)
query1 = "Find me flights from SFO to Tokyo on March 15, budget $900"
print(f"🧑 You: {query1}")
print(travel_assistant(query1))

# Test 2: Pure knowledge query
print("\n" + "=" * 60)
query2 = "What cultural customs should I know before visiting Tokyo?"
print(f"🧑 You: {query2}")
print(travel_assistant(query2))

# Test 3: Hotel booking with enrichment
print("\n" + "=" * 60)
query3 = "Find hotels in Paris for March 20-25, max $300/night"
print(f"🧑 You: {query3}")
print(travel_assistant(query3))
```

### Workshop Exercise Structure (Notebook Cells)
```python
# Cell 1: Concept Introduction
"""
# Exercise 3: RAG & Knowledge Integration

## What is RAG (Retrieval-Augmented Generation)?

RAG gives your agent access to private knowledge - documents, guides, policies - that
weren't in the LLM's training data. The agent retrieves relevant information from a
knowledge base and uses it to generate accurate, grounded responses.

**How it works:**
1. You index documents (PDFs, HTML, text) into a corpus
2. Documents are chunked and converted to embeddings (vectors)
3. User asks a question
4. Agent searches corpus for relevant chunks (semantic similarity)
5. Agent uses retrieved chunks as context to answer the question

**Tools vs RAG - When to Use Each:**

Use FUNCTION CALLING (Phase 2) when:
✓ Data changes frequently (flight availability, hotel pricing)
✓ Requires real-time API calls
✓ Need calculations or transformations

Use RAG (this phase) when:
✓ Data is static or slow-changing (destination guides, policies)
✓ Information already in documents
✓ Need semantic search across large corpus

**Example:**
- "Find flights to Tokyo" → TOOL (search_flights) - real-time availability
- "What's the best time to visit Tokyo?" → RAG - static seasonal guide

**In this exercise, you'll:**
- Explore a pre-indexed corpus of destination guides
- Configure a RAG retrieval tool
- Create an agent that searches the knowledge base
- Combine tools and RAG for comprehensive travel recommendations

⏱️ Estimated time: 40 minutes
"""

# Cell 2: Setup and Authentication
"""
## Setup: Load RAG Corpus ID

The instructor has pre-created a RAG corpus with 10-15 destination guides.
You'll use this corpus for retrieval exercises.
"""

import os
from google.adk.agents import Agent
from google.adk.tools.retrieval.vertex_ai_rag_retrieval import VertexAiRagRetrieval
from vertexai.preview import rag

# Corpus ID provided by instructor
# Format: projects/{project}/locations/{location}/ragCorpora/{corpus_id}
RAG_CORPUS_ID = "projects/your-workshop-project/locations/us-central1/ragCorpora/1234567890"

# Store in environment
os.environ['RAG_CORPUS_ID'] = RAG_CORPUS_ID

print(f"✓ RAG Corpus ID: {RAG_CORPUS_ID}")

# Cell 3: Exercise 3A - Explore Corpus
"""
## Exercise 3A: Explore Pre-Indexed Corpus

Let's inspect the corpus to see what destination guides are available.
"""

# List files in corpus (requires vertexai library)
from google.cloud import aiplatform

aiplatform.init(
    project=os.environ['GOOGLE_CLOUD_PROJECT'],
    location='us-central1',
)

# Query corpus metadata
# (Simplified - actual API call would list files)
print("📚 Destination guides in corpus:")
print("  - Tokyo, Japan")
print("  - Paris, France")
print("  - New York City, USA")
print("  - Singapore")
print("  - London, UK")
print("  - Rome, Italy")
print("  (+ more)")

print("\n📄 Each guide includes:")
print("  - Visa requirements")
print("  - Top attractions")
print("  - Weather by season")
print("  - Cultural tips and customs")
print("  - Transportation and practical info")

# Cell 4: Exercise 3B - Configure RAG Tool
"""
## Exercise 3B: Configure RAG Retrieval Tool

Create a VertexAiRagRetrieval tool that searches the destination guide corpus.

**Your tasks:**
1. Fill in the corpus resource path (use RAG_CORPUS_ID variable)
2. Set similarity_top_k (how many chunks to retrieve)
3. Set vector_distance_threshold (minimum similarity score)
4. Write a clear tool description (helps LLM decide when to use this tool)
"""

from google.adk.tools.retrieval.vertex_ai_rag_retrieval import VertexAiRagRetrieval
from vertexai.preview import rag

destination_knowledge = VertexAiRagRetrieval(
    name='retrieve_destination_info',

    # TODO: Write tool description
    # Hint: Explain what information this tool provides
    # Hint: Clarify when to use this vs booking tools
    description='''
    TODO: Fill in description

    Use this tool to answer questions about:
    - TODO: list capabilities

    DO NOT use this tool for:
    - TODO: list limitations (real-time data)
    ''',

    # TODO: Configure RAG resources
    rag_resources=[
        rag.RagResource(
            rag_corpus=os.environ['RAG_CORPUS_ID']  # TODO: Use the environment variable
        )
    ],

    # TODO: Set retrieval parameters
    similarity_top_k=5,  # TODO: How many chunks? (try 5)
    vector_distance_threshold=0.6,  # TODO: Minimum similarity? (try 0.6)
)

print("✓ RAG tool configured")

# Cell 5: Solution Check
"""
✅ Checkpoint: Verify your configuration
"""
# Verify tool created successfully
assert destination_knowledge.name == 'retrieve_destination_info'
assert len(destination_knowledge.rag_resources) > 0
print("✓ Tool configuration looks good!")

# Cell 6: Exercise 3C - Create RAG-Only Agent
"""
## Exercise 3C: Create RAG-Only Agent

Create an agent that uses ONLY the RAG retrieval tool.

**Important:** VertexAiRagRetrieval can only be used by itself - you cannot
combine it with function calling tools in the same agent. We'll handle this
limitation in Exercise 3E.
"""

# TODO: Create agent with RAG tool
destination_expert = Agent(
    model='gemini-2.5-flash',
    name='destination_expert',
    description='TODO: Agent description',

    instruction='''TODO: Write agent instruction

    Explain:
    - What the agent can do (retrieve from guides)
    - What it cannot do (real-time booking)
    - How to use the retrieve_destination_info tool
    ''',

    tools=[destination_knowledge],  # TODO: Add RAG tool (only this tool!)
)

print("✓ Destination expert agent created")

# Cell 7: Exercise 3D - Test Destination Queries
"""
## Exercise 3D: Test RAG Retrieval

Ask the agent questions that should be answered from destination guides.

Watch for:
- Does the agent call the RAG tool?
- Are retrieved chunks relevant?
- Does the answer cite guide information?
"""

test_queries = [
    "What are the visa requirements for US citizens traveling to Japan?",
    "What's the best time to visit Paris?",
    "What cultural customs should I know before visiting Tokyo?",
]

for query in test_queries:
    print(f"\n{'=' * 60}")
    print(f"🧑 You: {query}")
    response = destination_expert.generate_content(query)
    print(f"🤖 Agent: {response.text}")

# Cell 8: Exercise 3E - Hybrid Agent Pattern
"""
## Exercise 3E: Combine Tools and RAG

Real travel assistants need both real-time booking and destination knowledge.
But ADK doesn't allow mixing VertexAiRagRetrieval with function tools in one agent.

**Solution:** Create separate agents and coordinate them.
"""

# Reuse booking agent from Phase 2
from tools import search_flights, search_hotels  # Your Phase 2 tools

booking_agent = Agent(
    model='gemini-2.5-flash',
    name='booking_agent',
    description='Search flights and hotels.',
    instruction='Use your tools to find real-time availability and pricing.',
    tools=[search_flights, search_hotels],
)

# We already have destination_agent (from 3C)

# TODO: Write coordination function
def travel_assistant(user_query: str) -> str:
    """
    Route queries to booking or destination agent.
    Combine results when appropriate.
    """
    query_lower = user_query.lower()

    # TODO: Detect if query needs booking tools
    if 'flight' in query_lower or 'hotel' in query_lower:
        # TODO: Call booking_agent
        # TODO: Optionally enrich with destination tips
        pass

    # TODO: Detect if query needs destination knowledge
    elif 'visa' in query_lower or 'weather' in query_lower:
        # TODO: Call destination_agent
        pass

    else:
        # TODO: Default to booking_agent
        pass

# Test hybrid assistant
print(travel_assistant(
    "Find me flights from SFO to Tokyo on March 15, budget $900"
))
# Expected: Flight results + Tokyo travel tips

# Cell 9: Challenge (Optional)
"""
## Challenge: Tune Retrieval Quality

Experiment with similarity_top_k and vector_distance_threshold.

**Questions to explore:**
- What happens if you increase top_k to 10? 20?
- What happens if you lower threshold to 0.4? Raise to 0.8?
- Which settings give best answers for your test queries?
"""

# TODO: Create new RAG tool with different parameters
# TODO: Test with same queries
# TODO: Compare results

# Cell 10: Wrap-Up
"""
## What You Learned

✅ RAG provides agents with private knowledge from documents
✅ Use RAG for static knowledge, tools for real-time data
✅ Layout-aware chunking preserves document structure
✅ Similarity thresholds filter low-quality results
✅ ADK constraint: RAG tool cannot mix with function tools in same agent
✅ Hybrid pattern: Coordinate separate agents for tools + RAG

**Next Steps:**
- Exercise 4: Session management and conversation memory
- Bonus: Create your own destination guide and add to corpus
- Production: Multi-agent orchestration patterns
"""
```

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| Custom vector DB (Pinecone/Weaviate) | Vertex AI RAG Engine (managed) | Vertex AI RAG GA (2025) | Eliminates infrastructure management, auto-scaling |
| Character-based chunking | Document AI layout parser | Document AI integration (2025) | Preserves tables/lists, context-aware chunks |
| Manual embedding generation | Automatic via RAG Engine | RAG Engine GA | Consistent embeddings, no pipeline management |
| LangChain + custom RAG pipeline | ADK VertexAiRagRetrieval tool | ADK 1.20+ | Simpler integration, fewer dependencies |
| corpus create during app runtime | Pre-indexed corpus pattern | Workshop best practice | Faster app startup, predictable performance |
| Mixed tools without routing | Explicit tool vs RAG agents | ADK constraint workaround | Clear separation, better tool selection |
| No retrieval quality metrics | Vertex AI Model Evaluation | Vertex AI Eval (2025) | Standardized RAG metrics (faithfulness, relevance) |

**Deprecated/outdated:**
- **Manual vector DB setup**: Vertex AI RAG Engine provides managed alternative
- **Simple character splitting**: Document AI layout parser superior for structured PDFs
- **Corpus versioning via timestamp**: RAG Engine has built-in file update/import
- **Embedding model selection complexity**: textembedding-gecko@003 default works for most cases

## Open Questions

Things that couldn't be fully resolved:

1. **Chunk Size Optimization for Travel Guides**
   - What we know: Default 1024 tokens works, Document AI layout parser improves quality
   - What's unclear: Optimal chunk_size for travel guides with mixed content (narrative + tables)
   - Recommendation: Use default 1024/256 for workshop. Mention in "Advanced RAG" that chunk size tuning is corpus-specific. Production would A/B test 512, 1024, 1500 tokens with retrieval quality metrics. Travel guides likely benefit from larger chunks (1024+) to preserve narrative context, but needs validation with sample queries.

2. **Hybrid Agent Architecture - Production Pattern**
   - What we know: ADK constraint prevents mixing VertexAiRagRetrieval with function tools
   - What's unclear: Best production pattern - multi-agent coordination, LangGraph orchestration, or future ADK support?
   - Recommendation: Teach sequential coordination pattern (Pattern 5) in workshop as it's simplest. Mention in "What's Next" that production systems might use Agent-to-Agent (A2A) communication or orchestration frameworks. Monitor ADK roadmap for potential constraint relaxation.

3. **Corpus Update Frequency for Destination Guides**
   - What we know: Destination guides are "static" compared to flight data but do change (visa policies, new attractions)
   - What's unclear: How often to re-index corpus in production? Monthly? Quarterly? Event-driven?
   - Recommendation: Workshop uses frozen corpus (no updates during session). Documentation should note that production travel apps need update strategy. Most destination info stable (quarterly update sufficient), but visa policies event-driven (monitor government announcements, trigger re-index).

4. **Multi-Corpus Querying**
   - What we know: VertexAiRagRetrieval accepts list of rag_resources, can query multiple corpora
   - What's unclear: When to split vs combine? One corpus for all destinations vs one per destination?
   - Recommendation: Workshop uses single corpus (all destination guides together) for simplicity. Advanced pattern: separate corpora for different guide types (city guides, country policies, cultural context), agent queries relevant corpus based on query classification. Needs testing with 100+ documents to validate performance.

5. **Retrieval Quality Metrics in Workshop**
   - What we know: Production RAG needs evaluation (faithfulness, relevance, citation coverage)
   - What's unclear: How to demonstrate RAG quality assessment in 40-minute workshop exercise?
   - Recommendation: Exercise 3D manually validates retrieval (instructor reviews chunks with participants). Mention Vertex AI Model Evaluation in "What's Next" with links to docs. Workshop time doesn't allow automated metrics, but showing manual validation teaches critical thinking about retrieval quality.

6. **Destination Guide Content Curation**
   - What we know: Guide structure matters for retrieval quality (Pattern 6)
   - What's unclear: Create guides from scratch vs curate from existing sources? Licensing concerns?
   - Recommendation: For workshop, create original guides (10-15 destinations, 8-12 pages each) using Pattern 6 template. Avoids licensing issues, ensures consistent structure. Alternative: Use public domain travel guides (WikiTravel CC-BY-SA) with attribution. Production apps likely license professional content (Lonely Planet API, Fodor's, etc.).

## Sources

### Primary (HIGH confidence)
- [Vertex AI RAG Engine Overview](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/rag-engine/rag-overview) - Official architecture and capabilities (updated 2026-01-22)
- [Manage RAG Corpus](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/rag-engine/manage-your-rag-corpus) - Corpus CRUD operations
- [RAG Engine API Reference](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/model-reference/rag-api) - API specifications
- [ADK RAG Engine Tool](https://google.github.io/adk-docs/tools/google-cloud/vertex-ai-rag-engine/) - VertexAiRagRetrieval integration
- [Fine-tune RAG Transformations](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/rag-engine/fine-tune-rag-transformations) - Chunk size/overlap configuration
- [Document AI Layout Parser Integration](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/rag-engine/layout-parser-integration) - Structure-aware chunking
- [Parse and Chunk Documents](https://docs.cloud.google.com/generative-ai-app-builder/docs/parse-chunk-documents) - Chunking strategies

### Secondary (MEDIUM confidence)
- [GitHub: adk-vertex-ai-rag-engine](https://github.com/arjunprabhulal/adk-vertex-ai-rag-engine) - Community example of ADK + RAG
- [Build a RAG Agent with Google ADK & Vertex AI](https://brightdata.com/blog/ai/build-rag-agent-google-adk-vertex-ai) - Tutorial (2026)
- [RAG vs Function Calling - Digital Tourism Think Tank](https://www.thinkdigital.travel/opinion/destinations-are-embracing-ai-heres-why-rag-matters-more) - Travel industry RAG use cases
- [RAG-Powered Tourism Platform - Incubity](https://incubity.ambilio.com/rag-powered-tourism-destination-recommendation-platform/) - Industry application
- [TravelRAG: Knowledge Graph Framework](https://www.mdpi.com/2220-9964/13/11/414) - Academic research on travel RAG architecture
- [Codecademy: Build AI Travel Assistant with ADK](https://www.codecademy.com/article/build-an-ai-travel-assistant-with-google-agent-development-kit-adk) - Educational resource
- [DataCamp: ADK Visual Agent Builder Tutorial](https://www.datacamp.com/tutorial/google-adk-visual-agent-builder-tutorial-with-demo-project) - Travel planner demo

### Tertiary (LOW confidence - Verification Needed)
- [RAG Evaluation Guide - EvidentlyAI](https://www.evidentlyai.com/llm-guide/rag-evaluation) - Metrics and best practices (2026)
- [RAG Evaluation Metrics - Label Your Data](https://labelyourdata.com/articles/llm-fine-tuning/rag-evaluation) - Enterprise metrics (2026)
- [Writing Travel Guides - Textbroker](https://www.textbroker.com/creating-travel-guides) - Content structure best practices
- [Travel Guide Writing Tips - Spines](https://spines.com/writing-a-travel-guide-tips-and-tricks/) - Professional guide creation
- [Introduction to RAG - Coursera](https://www.coursera.org/projects/introduction-to-rag) - 2-hour workshop timing reference

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH - Vertex AI RAG Engine GA status confirmed, ADK integration documented in official sources
- Architecture patterns: HIGH - Pre-indexed corpus, layout parser, hybrid agent patterns verified from multiple official sources
- Pitfalls: MEDIUM - Single-tool constraint documented in ADK docs, chunking issues verified across sources, corpus timing based on workshop best practices
- Destination guide content: MEDIUM - Structure recommendations from travel writing guides, needs validation with actual corpus testing

**Research date:** 2026-01-24
**Valid until:** 2026-02-24 (30 days - Vertex AI RAG Engine stable, but fast-moving field)
**Recommended re-validation:** Test chunking strategy with sample destination guide PDFs (Tokyo, Paris) before finalizing Exercise 3 materials. Verify ADK constraint on VertexAiRagRetrieval + function tools still applies in latest version.

**Critical dependencies for Phase 3 planning:**
1. Sample destination guide PDFs (10-15) with standardized structure (Pattern 6)
2. Pre-workshop corpus setup script validation (Pattern 1)
3. Hybrid agent coordination pattern testing (Pattern 5 workaround)
4. Retrieval quality validation with representative queries (Pitfall 6)
