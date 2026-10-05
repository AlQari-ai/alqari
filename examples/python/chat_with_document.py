"""
chat_with_document.py — Ask questions about a document using natural language.

The document must have been uploaded with process_for_chat=true.

Usage:
    python chat_with_document.py <document_id> "<question>"

    Run without a question to start an interactive session.

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


def send_message(document_id: str, message: str) -> dict:
    api_key = get_api_key()
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    resp = requests.post(
        f"{BASE_URL}/services/chat/{document_id}",
        headers=headers,
        json={"message": message},
        timeout=60,
    )
    resp.raise_for_status()
    return resp.json()


def interactive_session(document_id: str) -> None:
    """Run an interactive chat session (each question is independent)."""
    print(f"Chatting with document: {document_id}")
    print("Type your question in Arabic or English. Press Ctrl+C to exit.\n")

    while True:
        try:
            message = input("You: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nExiting.")
            break

        if not message:
            continue

        result = send_message(document_id, message)
        print(f"\nALQari: {result.get('answer')}\n")


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python chat_with_document.py <document_id> [\"<question>\"]", file=sys.stderr)
        sys.exit(1)

    document_id = sys.argv[1]

    if len(sys.argv) > 2:
        message = sys.argv[2]
        print(f"Document: {document_id}")
        print(f"Question: {message}\n")
        result = send_message(document_id, message)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        interactive_session(document_id)


if __name__ == "__main__":
    main()
