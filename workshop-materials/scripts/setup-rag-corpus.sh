#!/bin/bash
#
# RAG Corpus Setup Script for ADK Workshop
#
# This script automates the creation and population of a Vertex AI RAG corpus
# with destination guide PDFs. Run this 48 hours before the workshop to ensure
# indexing completes and corpus is ready for participant use.
#
# Usage:
#   ./setup-rag-corpus.sh <project-id> [location]
#
# Or set environment variable:
#   export GOOGLE_CLOUD_PROJECT=your-project-id
#   ./setup-rag-corpus.sh
#
# Requirements:
#   - gcloud CLI authenticated (gcloud auth login)
#   - Vertex AI API enabled
#   - Cloud Storage API enabled
#   - jq installed (for JSON parsing)
#
# Output:
#   - GCS bucket created with PDFs uploaded
#   - RAG corpus created and indexed
#   - Corpus ID saved to corpus-id.txt
#

set -e  # Exit on error
set -o pipefail  # Catch errors in pipelines

# ============================================================================
# CONFIGURATION
# ============================================================================

PROJECT_ID="${1:-$GOOGLE_CLOUD_PROJECT}"
LOCATION="${2:-europe-west1}"
BUCKET_NAME="${PROJECT_ID}-adk-workshop-rag"
CORPUS_NAME="travel-destination-guides"

# Script directory resolution
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
GUIDES_DIR="${SCRIPT_DIR}/../destination-guides/pdf"

# ============================================================================
# VALIDATION
# ============================================================================

# Check required arguments
if [ -z "$PROJECT_ID" ]; then
    echo "❌ Error: PROJECT_ID not provided"
    echo ""
    echo "Usage:"
    echo "  $0 <project-id> [location]"
    echo ""
    echo "Or set environment variable:"
    echo "  export GOOGLE_CLOUD_PROJECT=your-project-id"
    echo "  $0"
    exit 1
fi

# Check for required tools
command -v gcloud >/dev/null 2>&1 || {
    echo "❌ Error: gcloud CLI not found"
    echo "Install: https://cloud.google.com/sdk/docs/install"
    exit 1
}

command -v jq >/dev/null 2>&1 || {
    echo "❌ Error: jq not found"
    echo "Install: sudo apt-get install jq (or brew install jq on macOS)"
    exit 1
}

# Check for gcloud storage (modern) or gsutil (legacy)
if gcloud storage --help >/dev/null 2>&1; then
    USE_GCLOUD_STORAGE=true
elif command -v gsutil >/dev/null 2>&1; then
    USE_GCLOUD_STORAGE=false
else
    echo "❌ Error: Neither 'gcloud storage' nor 'gsutil' found"
    echo "Update gcloud: gcloud components update"
    exit 1
fi

# ============================================================================
# HEADER
# ============================================================================

echo "==================================================================="
echo "    RAG Corpus Setup for ADK Workshop"
echo "==================================================================="
echo ""
echo "Configuration:"
echo "  Project ID:       $PROJECT_ID"
echo "  Location:         $LOCATION"
echo "  Bucket:           gs://$BUCKET_NAME"
echo "  Corpus name:      $CORPUS_NAME"
echo "  Source PDFs:      $GUIDES_DIR"
echo ""

# ============================================================================
# STEP 1: AUTHENTICATION CHECK
# ============================================================================

echo "[1/7] Checking authentication..."

if ! gcloud auth print-access-token > /dev/null 2>&1; then
    echo "❌ Not authenticated with gcloud"
    echo ""
    echo "Please run:"
    echo "  gcloud auth login"
    echo "  gcloud config set project $PROJECT_ID"
    exit 1
fi

echo "   ✓ Authenticated"

# Verify project access
CURRENT_PROJECT=$(gcloud config get-value project 2>/dev/null || echo "")
if [ "$CURRENT_PROJECT" != "$PROJECT_ID" ]; then
    echo "   ⚠ Warning: Current gcloud project is '$CURRENT_PROJECT'"
    echo "   Setting project to: $PROJECT_ID"
    gcloud config set project "$PROJECT_ID"
fi

echo "   ✓ Project: $PROJECT_ID"

# ============================================================================
# STEP 2: VERIFY PDF FILES
# ============================================================================

echo ""
echo "[2/7] Verifying PDF files..."

if [ ! -d "$GUIDES_DIR" ]; then
    echo "❌ PDF directory not found: $GUIDES_DIR"
    echo ""
    echo "Please run the PDF conversion script first:"
    echo "  python scripts/convert-guides-to-pdf.py"
    exit 1
fi

PDF_COUNT=$(find "$GUIDES_DIR" -name "*.pdf" -type f | wc -l)

if [ "$PDF_COUNT" -eq 0 ]; then
    echo "❌ No PDF files found in: $GUIDES_DIR"
    echo ""
    echo "Please run the PDF conversion script first:"
    echo "  python scripts/convert-guides-to-pdf.py"
    exit 1
fi

echo "   ✓ Found $PDF_COUNT PDF files"
find "$GUIDES_DIR" -name "*.pdf" -type f -exec basename {} \; | sed 's/^/     - /'

# ============================================================================
# STEP 3: CREATE GCS BUCKET
# ============================================================================

echo ""
echo "[3/7] Creating GCS bucket..."

# Check if bucket exists and create if needed
if [ "$USE_GCLOUD_STORAGE" = true ]; then
    if gcloud storage ls "gs://$BUCKET_NAME" --project="$PROJECT_ID" >/dev/null 2>&1; then
        echo "   ✓ Bucket already exists: gs://$BUCKET_NAME"
    else
        echo "   Creating bucket: gs://$BUCKET_NAME"
        gcloud storage buckets create "gs://$BUCKET_NAME" --project="$PROJECT_ID" --location="$LOCATION"
        echo "   ✓ Bucket created"
    fi
else
    if gsutil ls -p "$PROJECT_ID" "gs://$BUCKET_NAME" >/dev/null 2>&1; then
        echo "   ✓ Bucket already exists: gs://$BUCKET_NAME"
    else
        echo "   Creating bucket: gs://$BUCKET_NAME"
        gsutil mb -p "$PROJECT_ID" -l "$LOCATION" "gs://$BUCKET_NAME/"
        echo "   ✓ Bucket created"
    fi
fi

# ============================================================================
# STEP 4: UPLOAD PDFs TO GCS
# ============================================================================

echo ""
echo "[4/7] Uploading PDFs to GCS..."

# Upload all PDFs with progress
if [ "$USE_GCLOUD_STORAGE" = true ]; then
    gcloud storage cp "$GUIDES_DIR"/*.pdf "gs://$BUCKET_NAME/guides/"
else
    gsutil -m cp "$GUIDES_DIR"/*.pdf "gs://$BUCKET_NAME/guides/"
fi

echo "   ✓ Uploaded $PDF_COUNT PDF files to gs://$BUCKET_NAME/guides/"

# ============================================================================
# STEP 5: DELETE EXISTING CORPUS (if any)
# ============================================================================

echo ""
echo "[5/8] Checking for existing corpus..."

# List existing corpora and find matching one
EXISTING_CORPORA=$(curl -s -X GET \
  -H "Authorization: Bearer $(gcloud auth print-access-token)" \
  "https://${LOCATION}-aiplatform.googleapis.com/v1beta1/projects/${PROJECT_ID}/locations/${LOCATION}/ragCorpora")

# Find corpus with matching display name
EXISTING_CORPUS_NAME=$(echo "$EXISTING_CORPORA" | jq -r '.ragCorpora[]? | select(.displayName == "'"$CORPUS_NAME"'") | .name' 2>/dev/null | head -1)

if [ -n "$EXISTING_CORPUS_NAME" ] && [ "$EXISTING_CORPUS_NAME" != "null" ]; then
    echo "   Found existing corpus: $EXISTING_CORPUS_NAME"
    echo "   Deleting..."

    DELETE_RESPONSE=$(curl -s -X DELETE \
      -H "Authorization: Bearer $(gcloud auth print-access-token)" \
      "https://${LOCATION}-aiplatform.googleapis.com/v1beta1/${EXISTING_CORPUS_NAME}")

    # Check for delete errors
    if echo "$DELETE_RESPONSE" | jq -e '.error' >/dev/null 2>&1; then
        echo "   ⚠ Warning: Could not delete existing corpus"
        echo "$DELETE_RESPONSE" | jq '.error'
        echo "   Proceeding anyway..."
    else
        echo "   ✓ Existing corpus deleted"
        # Wait a moment for deletion to propagate
        sleep 3
    fi
else
    echo "   ✓ No existing corpus found with name: $CORPUS_NAME"
fi

# ============================================================================
# STEP 6: CREATE RAG CORPUS
# ============================================================================

echo ""
echo "[6/8] Creating RAG corpus..."

# Create corpus via REST API (using v1beta1 for latest features)
CORPUS_RESPONSE=$(curl -s -X POST \
  -H "Authorization: Bearer $(gcloud auth print-access-token)" \
  -H "Content-Type: application/json" \
  "https://${LOCATION}-aiplatform.googleapis.com/v1beta1/projects/${PROJECT_ID}/locations/${LOCATION}/ragCorpora" \
  -d '{
    "display_name": "'"$CORPUS_NAME"'",
    "description": "Destination travel guides for ADK workshop exercises. Contains comprehensive guides for Tokyo, Paris, New York, Singapore, London, Rome, Bangkok, Sydney, Barcelona, Dubai covering visa requirements, attractions, weather, cultural tips, and practical information."
  }')

# Check for errors
if echo "$CORPUS_RESPONSE" | jq -e '.error' >/dev/null 2>&1; then
    echo "❌ Failed to create corpus"
    echo "$CORPUS_RESPONSE" | jq '.error'
    exit 1
fi

# Extract corpus ID
CORPUS_ID=$(echo "$CORPUS_RESPONSE" | jq -r '.name' | awk -F'/' '{print $NF}')

if [ -z "$CORPUS_ID" ] || [ "$CORPUS_ID" = "null" ]; then
    echo "❌ Failed to extract corpus ID from response"
    echo "Response: $CORPUS_RESPONSE"
    exit 1
fi

FULL_CORPUS_ID="projects/${PROJECT_ID}/locations/${LOCATION}/ragCorpora/${CORPUS_ID}"

echo "   ✓ Corpus created"
echo "   Corpus ID: $CORPUS_ID"
echo "   Full path: $FULL_CORPUS_ID"

# Wait for corpus to be ready (async creation)
echo "   Waiting for corpus to be ready..."
MAX_WAIT=60
WAITED=0
while [ $WAITED -lt $MAX_WAIT ]; do
    CORPUS_STATUS=$(curl -s -X GET \
      -H "Authorization: Bearer $(gcloud auth print-access-token)" \
      "https://${LOCATION}-aiplatform.googleapis.com/v1beta1/${FULL_CORPUS_ID}")

    if echo "$CORPUS_STATUS" | jq -e '.name' >/dev/null 2>&1; then
        echo "   ✓ Corpus is ready"
        break
    fi

    sleep 5
    WAITED=$((WAITED + 5))
    echo "   Still waiting... (${WAITED}s)"
done

if [ $WAITED -ge $MAX_WAIT ]; then
    echo "   ⚠ Warning: Corpus may not be fully ready, proceeding anyway..."
fi

# ============================================================================
# STEP 7: IMPORT PDFs TO CORPUS
# ============================================================================

echo ""
echo "[7/8] Importing PDFs to corpus..."
echo "   (This takes 5-10 minutes - indexing and embedding)"

# Import PDFs with chunking configuration
# Note: Using v1beta1 API for latest features
IMPORT_RESPONSE=$(curl -s -X POST \
  -H "Authorization: Bearer $(gcloud auth print-access-token)" \
  -H "Content-Type: application/json" \
  "https://${LOCATION}-aiplatform.googleapis.com/v1beta1/${FULL_CORPUS_ID}/ragFiles:import" \
  -d '{
    "import_rag_files_config": {
      "gcs_source": {
        "uris": ["gs://'"$BUCKET_NAME"'/guides/*.pdf"]
      },
      "rag_file_transformation_config": {
        "rag_file_chunking_config": {
          "fixed_length_chunking": {
            "chunk_size": 1024,
            "chunk_overlap": 256
          }
        }
      },
      "max_embedding_requests_per_min": 1000
    }
  }')

# Check for import errors
if echo "$IMPORT_RESPONSE" | jq -e '.error' >/dev/null 2>&1; then
    echo "❌ Failed to import PDFs"
    echo "$IMPORT_RESPONSE" | jq '.error'
    exit 1
fi

echo "   ✓ Import request submitted"
echo "   Chunk size: 1024 tokens"
echo "   Chunk overlap: 256 tokens"
echo "   Chunking: fixed length"

# ============================================================================
# STEP 8: SAVE CORPUS ID AND DISPLAY COMPLETION INFO
# ============================================================================

echo ""
echo "[8/8] Saving corpus information..."

# Save to file
echo "$FULL_CORPUS_ID" > corpus-id.txt
echo "   ✓ Corpus ID saved to: corpus-id.txt"

# Create environment file snippet
cat > corpus-env.txt <<EOF
# Add this to your .env file for the workshop:
RAG_CORPUS_ID=$FULL_CORPUS_ID
EOF

echo "   ✓ Environment snippet saved to: corpus-env.txt"

# ============================================================================
# COMPLETION SUMMARY
# ============================================================================

echo ""
echo "==================================================================="
echo "    Setup Complete!"
echo "==================================================================="
echo ""
echo "📋 CORPUS ID (share with participants):"
echo ""
echo "   $FULL_CORPUS_ID"
echo ""
echo "==================================================================="
echo ""
echo "Next Steps:"
echo ""
echo "1. Wait for indexing to complete (5-10 minutes)"
echo "   Check status:"
echo "   gcloud ai rag-corpora describe $CORPUS_ID --location=$LOCATION --project=$PROJECT_ID"
echo ""
echo "2. Validate corpus before workshop (48 hours before):"
echo "   python scripts/validate-corpus.py $FULL_CORPUS_ID"
echo ""
echo "3. Share corpus ID with participants:"
echo "   - Add to Exercise 3 notebook"
echo "   - Include in .env template"
echo "   - Mention in workshop setup instructions"
echo ""
echo "4. Test retrieval with sample queries:"
echo "   - 'What are visa requirements for US citizens visiting Japan?'"
echo "   - 'Best time to visit Paris?'"
echo "   - 'Top attractions in New York City?'"
echo ""
echo "Files created:"
echo "   - corpus-id.txt (corpus identifier)"
echo "   - corpus-env.txt (environment variable format)"
echo ""
echo "GCS bucket: gs://$BUCKET_NAME/guides/ ($PDF_COUNT PDFs)"
echo ""
echo "==================================================================="
