"""
validate_document.py — Run rule-based AI validation on a processed document.

Usage:
    python validate_document.py <document_id> ["<newline-numbered rules>"]

Environment variables:
    ALQARI_API_KEY   Required.
    ALQARI_BASE_URL  Optional. Defaults to https://api.alqari.sa
"""

import os
import sys
import json
import requests

BASE_URL = os.environ.get("ALQARI_BASE_URL", "https://api.alqari.sa").rstrip("/")

# Newline-numbered rules. Edit to match your validation requirements.
DEFAULT_RULES_TEXT = (
    "1. All required fields are present.\n"
    "2. The total matches the sum of line items.\n"
    "3. The issue date is not after the due date."
)


def get_api_key() -> str:
    key = os.environ.get("ALQARI_API_KEY")
    if not key:
        print("Error: ALQARI_API_KEY environment variable is not set.", file=sys.stderr)
        sys.exit(1)
    return key


def validate_document(document_id: str, rules_text: str) -> dict:
    api_key = get_api_key()
    headers = {"Authorization": f"Bearer {api_key}"}
    # ai-validate takes document_id and rules_text as query parameters.
    params = {"document_id": document_id, "rules_text": rules_text}
    resp = requests.post(
        f"{BASE_URL}/services/ai-validate",
        headers=headers,
        params=params,
        timeout=60,
    )
    resp.raise_for_status()
    return resp.json()


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python validate_document.py <document_id> [rules_text]", file=sys.stderr)
        sys.exit(1)

    document_id = sys.argv[1]
    rules_text = sys.argv[2] if len(sys.argv) > 2 else DEFAULT_RULES_TEXT

    print(f"Running validation on document: {document_id}")
    result = validate_document(document_id, rules_text)
    print(json.dumps(result, ensure_ascii=False, indent=2))

    verdict = result.get("overall_verdict")
    print(f"\nOverall verdict: {verdict}")


if __name__ == "__main__":
    main()
