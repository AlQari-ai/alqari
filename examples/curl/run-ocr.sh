#!/usr/bin/env bash
# run-ocr.sh — Retrieve structured OCR output for a document
#
# Usage:
#   export ALQARI_API_KEY="your_api_key_here"
#   bash run-ocr.sh <document_id> [format]
#
# format (optional): ocr (default) | text | layout
#
# Examples:
#   bash run-ocr.sh doc_9xKpL3mN            # structured OCR regions (JSON)
#   bash run-ocr.sh doc_9xKpL3mN text       # plain text
#   bash run-ocr.sh doc_9xKpL3mN layout     # layout analysis (JSON)

set -euo pipefail

BASE_URL="${ALQARI_BASE_URL:-https://api.alqari.sa}"
DOCUMENT_ID="${1:?Usage: bash run-ocr.sh <document_id> [format]}"
FORMAT="${2:-ocr}"

if [[ -z "${ALQARI_API_KEY:-}" ]]; then
  echo "Error: ALQARI_API_KEY environment variable is not set." >&2
  exit 1
fi

echo "Fetching OCR output ($FORMAT) for document: $DOCUMENT_ID"

if [[ "$FORMAT" == "text" ]]; then
  curl --fail-with-body \
    --url "${BASE_URL}/services/ocr-output/${DOCUMENT_ID}/text" \
    --header "Authorization: Bearer ${ALQARI_API_KEY}"
else
  curl --fail-with-body \
    --url "${BASE_URL}/services/ocr-output/${DOCUMENT_ID}/${FORMAT}" \
    --header "Authorization: Bearer ${ALQARI_API_KEY}" \
    | python3 -m json.tool
fi
