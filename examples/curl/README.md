# cURL Examples

Copy-paste ready cURL commands for the ALQari API.

## Prerequisites

```bash
export ALQARI_API_KEY="qari_your_api_key_here"
export ALQARI_BASE_URL="https://api.alqari.sa"   # optional, this is the default
```

## Scripts

| Script | Description |
|--------|-------------|
| `upload-document.sh`   | Upload a PDF or image and run OCR (`POST /services/upload-ocr`) |
| `run-ocr.sh`           | Fetch OCR output (`GET /services/ocr-output/{id}/ocr\|text\|layout`) |
| `validate-document.sh` | Run rule-based validation (`POST /services/ai-validate`) |
| `chat-with-document.sh`| Ask a question about a document (`POST /services/chat/{id}`) |

## Usage

```bash
# Upload + OCR → returns document_id
bash upload-document.sh /path/to/document.pdf

# Retrieve structured OCR regions (or: text | layout)
bash run-ocr.sh doc_9xKpL3mN
bash run-ocr.sh doc_9xKpL3mN text

# Validate against your own rules
bash validate-document.sh doc_9xKpL3mN

# Ask a question (upload with process_for_chat=true first)
bash chat-with-document.sh doc_9xKpL3mN "ما إجمالي الفاتورة؟"
```

> The authoritative API reference is at [alqari.sa/api-docs](https://alqari.sa/api-docs).
