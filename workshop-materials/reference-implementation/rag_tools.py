"""
RAG Knowledge Tools - Reference Implementation

Provides destination knowledge retrieval using Vertex AI RAG Engine.
Demonstrates proper VertexAiRagRetrieval configuration with explicit
tool descriptions (critical for correct tool selection).

IMPORTANT CONSTRAINT (Pattern 5):
VertexAiRagRetrieval CANNOT be mixed with function calling tools
in the same agent. For hybrid agents, use separate agents with
coordination logic (see hybrid_agent.py).
"""

import os
from typing import Optional
from google.adk.tools.retrieval.vertex_ai_rag_retrieval import VertexAiRagRetrieval
from vertexai.preview import rag

# ============================================================
# CONFIGURATION
# ============================================================

RAG_CORPUS_ID = os.environ.get('RAG_CORPUS_ID')

# Retrieval parameters (from research - default values work well)
DEFAULT_TOP_K = 5
DEFAULT_THRESHOLD = 0.6


# ============================================================
# RAG TOOL FACTORY (Exercise 3B pattern)
# ============================================================

def create_destination_knowledge_tool(
    corpus_id: Optional[str] = None,
    similarity_top_k: int = DEFAULT_TOP_K,
    vector_distance_threshold: float = DEFAULT_THRESHOLD,
) -> VertexAiRagRetrieval:
    """
    Create VertexAiRagRetrieval tool for destination guides.

    Args:
        corpus_id: RAG corpus ID (uses RAG_CORPUS_ID env var if not provided)
        similarity_top_k: Number of chunks to retrieve (default 5)
        vector_distance_threshold: Minimum similarity score (default 0.6)

    Returns:
        Configured RAG retrieval tool

    Raises:
        ValueError: If corpus_id not provided and RAG_CORPUS_ID not set
    """
    corpus = corpus_id or RAG_CORPUS_ID

    if not corpus:
        raise ValueError(
            "RAG corpus ID not provided. Either:\n"
            "  1. Pass corpus_id parameter, or\n"
            "  2. Set RAG_CORPUS_ID environment variable\n"
            "Expected format: projects/{project}/locations/{location}/ragCorpora/{id}"
        )

    # Create tool with explicit description (Pitfall 5 prevention)
    tool = VertexAiRagRetrieval(
        name='retrieve_destination_info',

        # CRITICAL: Explicit DO/DO NOT description guides LLM tool selection
        description='''Retrieve destination information from travel guide knowledge base.

USE THIS TOOL to answer questions about:
- Visa requirements and entry rules (static immigration policy)
- Top attractions and landmarks (guide recommendations)
- Best time to visit by season (weather patterns, events)
- Cultural tips and local customs (etiquette, traditions)
- Safety information and travel advisories
- Transportation within the city (metro, buses, taxis)
- Food and dining recommendations (local cuisine, prices)
- Neighborhoods and districts to explore
- Practical travel information (plugs, currency, language)

DO NOT use this tool for:
- Real-time flight availability → use search_flights() instead
- Real-time hotel availability → use search_hotels() instead
- Current pricing or booking status → use search tools
- Live event schedules or ticket availability

This tool searches STATIC destination guides, not live databases.
Use for travel planning knowledge, not booking transactions.''',

        rag_resources=[
            rag.RagResource(rag_corpus=corpus)
        ],

        similarity_top_k=similarity_top_k,
        vector_distance_threshold=vector_distance_threshold,
    )

    print(f"RAG tool configured with corpus: {corpus[:50]}...")
    return tool


# ============================================================
# PRE-CONFIGURED INSTANCE (for simple usage)
# ============================================================

# Create default instance if corpus ID is available
destination_knowledge = None
try:
    if RAG_CORPUS_ID:
        destination_knowledge = create_destination_knowledge_tool()
except Exception as e:
    print(f"Warning: Could not create default RAG tool: {e}")
    print("Set RAG_CORPUS_ID environment variable to enable RAG.")
