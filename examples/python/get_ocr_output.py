"""
get_ocr_output.py — Retrieve OCR output for a document.

Usage:
    python get_ocr_output.py <document_id> [format]

    format: ocr (default) | text | layout

Environment variables:
    ALQARI_API_KEY   Required.
    ALQARI_BASE_URL  Optional. Defaults to https://api.alqari.sa
"""

import os
import sys
import json
import requests

BASE_URL = os.environ.get("ALQARI_BASE_URL", "https://api.alqari.sa").rstrip("/")


def get_api_key() -> str:
    key = os.environ.get("ALQARI_API_KEY")
    if not key:
        print("Error: ALQARI_API_KEY environment variable is not set.", file=sys.stderr)
        sys.exit(1)
    return key


def get_ocr_output(document_id: str, output_format: str = "ocr"):
    api_key = get_api_key()
    headers = {"Authorization": f"Bearer {api_key}"}
    resp = requests.get(
        f"{BASE_URL}/services/ocr-output/{document_id}/{output_format}",
        headers=headers,
        timeout=60,
    )
    resp.raise_for_status()
    # /text returns plain text; /ocr and /layout return JSON.
    if output_format == "text":
        return resp.text
    return resp.json()


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python get_ocr_output.py <document_id> [format]", file=sys.stderr)
        sys.exit(1)

    document_id = sys.argv[1]
    output_format = sys.argv[2] if len(sys.argv) > 2 else "ocr"

    print(f"Fetching OCR output ({output_format}) for document: {document_id}")
    result = get_ocr_output(document_id, output_format)
    if isinstance(result, str):
        print(result)
    else:
        print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
