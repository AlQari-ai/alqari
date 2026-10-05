#!/usr/bin/env bash
# upload-document.sh — Upload a document to ALQari and run OCR in one step
#
# Usage:
#   export ALQARI_API_KEY="your_api_key_here"
#   bash upload-document.sh /path/to/document.pdf
#
# Optional env vars:
#   ALQARI_BASE_URL  (default: https://api.alqari.sa)
#   ALQARI_LANGUAGE  (default: auto)   one of: auto | ar | en
#   ALQARI_MODE      (default: unset)  one of: fast | premium

set -euo pipefail

BASE_URL="${ALQARI_BASE_URL:-https://api.alqari.sa}"
LANGUAGE="${ALQARI_LANGUAGE:-auto}"
FILE_PATH="${1:?Usage: bash upload-document.sh <file_path>}"

if [[ -z "${ALQARI_API_KEY:-}" ]]; then
  echo "Error: ALQARI_API_KEY environment variable is not set." >&2
  exit 1
fi

if [[ ! -f "$FILE_PATH" ]]; then
  echo "Error: File not found: $FILE_PATH" >&2
  exit 1
fi

QUERY="language=${LANGUAGE}"
if [[ -n "${ALQARI_MODE:-}" ]]; then
  QUERY="${QUERY}&mode=${ALQARI_MODE}"
fi

echo "Uploading: $FILE_PATH"

curl --fail-with-body \
  --request POST \
  --url "${BASE_URL}/services/upload-ocr?${QUERY}" \
  --header "Authorization: Bearer ${ALQARI_API_KEY}" \
  --form "file=@${FILE_PATH}" \
  | python3 -m json.tool
