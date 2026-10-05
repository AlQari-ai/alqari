#!/usr/bin/env bash
# validate-document.sh — Run rule-based AI validation on a processed document
#
# Usage:
#   export ALQARI_API_KEY="your_api_key_here"
#   bash validate-document.sh <document_id> ["<newline-numbered rules>"]

set -euo pipefail

BASE_URL="${ALQARI_BASE_URL:-https://api.alqari.sa}"
DOCUMENT_ID="${1:?Usage: bash validate-document.sh <document_id> [rules_text]}"
RULES_TEXT="${2:-$'1. All required fields are present.\n2. The total matches the sum of line items.'}"

if [[ -z "${ALQARI_API_KEY:-}" ]]; then
  echo "Error: ALQARI_API_KEY environment variable is not set." >&2
  exit 1
fi

echo "Running validation on document: $DOCUMENT_ID"

# ai-validate takes document_id and rules_text as query parameters.
# curl --data-urlencode (with -G) URL-encodes them safely into the query string.
curl --fail-with-body \
  --get \
  --request POST \
  --url "${BASE_URL}/services/ai-validate" \
  --data-urlencode "document_id=${DOCUMENT_ID}" \
  --data-urlencode "rules_text=${RULES_TEXT}" \
  --header "Authorization: Bearer ${ALQARI_API_KEY}" \
  | python3 -m json.tool
