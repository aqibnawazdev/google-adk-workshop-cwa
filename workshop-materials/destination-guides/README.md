# Destination Travel Guides

This directory contains comprehensive destination guides for the RAG knowledge base used in the ADK workshop.

## Contents

**10 destination guides** covering major travel destinations worldwide:

- **Asia**: Tokyo (Japan), Singapore, Bangkok (Thailand)
- **Europe**: Paris (France), London (UK), Rome (Italy), Barcelona (Spain)
- **North America**: New York (USA)
- **Middle East**: Dubai (UAE)
- **Oceania**: Sydney (Australia)

Each guide provides comprehensive travel information suitable for AI-powered travel assistants.

## Guide Structure

All guides follow a standardized 10-section structure for consistent RAG retrieval:

### 1. Quick Facts
- Country, language, currency, timezone
- Population, emergency numbers
- International airport codes
- Climate overview

### 2. Visa Requirements
- Entry requirements by nationality
- Visa-free stays and limitations
- Required documents (passport validity, etc.)
- Special notes (ESTA, ETIAS, e-visas)

### 3. Best Time to Visit
- Seasonal breakdown (spring, summer, fall, winter)
- Weather patterns and temperatures
- Crowd levels and peak seasons
- Special events and festivals
- Pros and cons for each season

### 4. Top Attractions
**Table format** (critical for layout-aware chunking):

| Attraction | Location | Entry Fee | Hours | Best Time |
|------------|----------|-----------|-------|-----------|
| ... | ... | ... | ... | ... |

- 10-12 must-see attractions per destination
- Practical details: pricing, hours, booking requirements
- Tips for avoiding crowds

### 5. Neighborhoods & Districts
- Character and vibe of major areas
- Must-see sites in each neighborhood
- Food and dining highlights
- Transportation connections
- Best activities for different traveler types

### 6. Food & Dining
- Signature local dishes with descriptions
- Where to eat (categories: street food, casual, fine dining)
- Price ranges and budgeting
- Dining customs and etiquette
- Dietary restrictions and alternatives
- Tipping practices

### 7. Transportation
- Airport to city center options
- Public transit systems (metro, buses, trams)
- Taxis and ride-sharing services
- Transport cards and passes
- Navigation tips for tourists
- Approximate costs

### 8. Cultural Tips & Customs
- Greetings and basic phrases
- Social etiquette and do's/don'ts
- Dress codes and modesty expectations
- Local laws and regulations
- Tipping customs
- Important cultural sensitivities

### 9. Safety & Health
- Overall safety assessment
- Areas to avoid or be cautious in
- Common scams and how to avoid them
- Emergency services and medical care
- Health precautions and vaccinations
- Food and water safety
- Travel insurance recommendations

### 10. Practical Information
- Electricity and plug types
- Internet access and SIM cards
- Money, ATMs, and currency exchange
- Business hours and holidays
- Language tips and useful phrases
- Recommended apps and resources

## For Instructors

### Pre-Workshop Setup (48 hours before workshop)

Follow these steps to prepare the RAG corpus:

#### Step 1: Convert Guides to PDF

```bash
cd workshop-materials
python scripts/convert-guides-to-pdf.py
```

This creates PDFs in `destination-guides/pdf/` directory with:
- Professional formatting and styling
- Preserved table structures
- Readable fonts and layout
- Proper page breaks

**Requirements**: `pip install markdown2 weasyprint`

#### Step 2: Create and Populate RAG Corpus

```bash
cd workshop-materials
./scripts/setup-rag-corpus.sh your-project-id
```

This script:
1. Creates GCS bucket for PDF storage
2. Uploads all destination guide PDFs
3. Creates Vertex AI RAG corpus
4. Imports PDFs with Document AI layout parser
5. Configures chunking (1024 tokens / 256 overlap)
6. Outputs corpus ID for workshop use

**Duration**: 5-10 minutes for indexing

**Output files**:
- `corpus-id.txt` - Full corpus resource path
- `corpus-env.txt` - Environment variable format for .env files

#### Step 3: Validate Corpus

```bash
python scripts/validate-corpus.py
```

Or with explicit corpus ID:

```bash
python scripts/validate-corpus.py projects/your-project/locations/europe-west1/ragCorpora/123456
```

This tests:
- Corpus accessibility
- Retrieval configuration
- Coverage of all destinations
- Table content preservation

**Run this 24-48 hours before workshop** to ensure time for fixes if needed.

#### Step 4: Share Corpus ID with Participants

Add the corpus ID to:
1. **Exercise 3 notebook** (cell 2: Setup section)
2. **Workshop .env template**
3. **Setup instructions** (pre-workshop email)

Example:
```python
# Exercise 3 notebook
RAG_CORPUS_ID = "projects/adk-workshop-2026/locations/europe-west1/ragCorpora/1234567890"
```

### Corpus Configuration Details

The corpus is configured with:

- **Chunking strategy**:
  - Chunk size: 1024 tokens (~800 words)
  - Overlap: 256 tokens (~200 words)
  - Strategy: Token-based (not character-based)

- **Parser**: Document AI layout parser
  - Enabled via `use_advanced_pdf_parsing: true`
  - Preserves table structures
  - Detects headings and lists
  - Maintains semantic boundaries

- **Embedding model**: textembedding-gecko@003
  - Managed by Vertex AI RAG Engine
  - Multilingual support
  - Optimized for semantic search

- **Indexing time**: 5-10 minutes for 10 PDFs
  - Check status: `gcloud ai rag-corpora describe <corpus-id> --location=europe-west1`

### Troubleshooting

**Issue**: Indexing not complete after 15 minutes
- Check Vertex AI quota limits
- Verify PDFs uploaded correctly to GCS
- Review Cloud Logging for import errors

**Issue**: Validation tests fail
- Wait for indexing to complete (check status)
- Verify Vertex AI API is enabled
- Check authentication: `gcloud auth login`

**Issue**: Retrieval returns wrong destination
- Check similarity threshold (lower to 0.5 for testing)
- Verify PDF content matches expected destination
- Inspect chunks manually via RAG API

**Issue**: Tables not preserved in chunks
- Confirm `use_advanced_pdf_parsing: true` in import config
- Check PDF conversion preserved table formatting
- May need to regenerate PDFs with better table CSS

## For Participants

**You don't need to create the corpus!** It's pre-indexed by the instructor.

In Exercise 3, you'll:
1. Receive the corpus ID from your instructor
2. Configure a `VertexAiRagRetrieval` tool pointing to the corpus
3. Create an agent that searches the knowledge base
4. Query destinations and retrieve travel information
5. Combine RAG with function calling tools for comprehensive travel planning

The corpus contains 10 destination guides with comprehensive information about:
- Visa requirements and entry rules
- Top attractions and landmarks
- Weather and best time to visit
- Cultural customs and etiquette
- Safety and health information
- Transportation and navigation
- Food and dining recommendations
- Practical travel tips

## Content Guidelines

These guides were created following best practices for RAG corpus design:

### Accuracy
- Factually correct visa requirements (as of 2026)
- Realistic pricing and practical information
- Authentic cultural customs and etiquette
- Current transportation systems and costs

### Consistency
- All guides use the same 10-section structure
- Similar length (300-600 lines / 8-15 pages)
- Comparable depth and detail
- Uniform table formatting

### Educational Value
- Respectful cultural representation
- Emphasizes responsible and ethical travel
- Practical advice for first-time visitors
- Safety awareness without fear-mongering

### Technical Optimization
- Tables for structured data (attractions, transport)
- Lists for scannable content (do's/don'ts, packing)
- Narrative sections for context and culture
- Clear headings for semantic chunking

## License and Usage

These guides are created specifically for the ADK workshop and are:
- Licensed for educational use in the workshop context
- Not to be redistributed as standalone travel guides
- Based on publicly available travel information
- Synthesized and structured for RAG training purposes

For production travel applications, consider:
- Professional travel content APIs (Lonely Planet, Fodor's, etc.)
- User-generated content with moderation (TripAdvisor, WikiVoyage)
- Official tourism board resources
- Licensed guidebook content

---

**Questions?** Contact the workshop instructor or refer to the Phase 3 documentation in `.planning/phases/03-rag-and-knowledge-integration/`.
