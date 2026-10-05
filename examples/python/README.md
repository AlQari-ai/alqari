# Python Examples

Self-contained Python scripts for the ALQari API.

## Requirements

Python 3.8+ and the `requests` library:

```bash
pip install -r requirements.txt
```

## Configuration

```bash
export ALQARI_API_KEY="qari_your_api_key_here"
export ALQARI_BASE_URL="https://api.alqari.sa"   # optional, this is the default
```

## Scripts

| Script | Description |
|--------|-------------|
| `upload_document.py`   | Upload a document and run OCR (`POST /services/upload-ocr`) |
| `get_ocr_output.py`    | Fetch OCR output (`GET /services/ocr-output/{id}/ocr\|text\|layout`) |
| `validate_document.py` | Run rule-based validation (`POST /services/ai-validate`) |
| `chat_with_document.py`| Ask a question about a document (`POST /services/chat/{id}`) |

## Usage

```bash
# Upload + OCR → returns document_id
python upload_document.py /path/to/document.pdf

# Retrieve structured OCR regions (or: text | layout)
python get_ocr_output.py doc_9xKpL3mN
python get_ocr_output.py doc_9xKpL3mN text

# Validate against your own rules
python validate_document.py doc_9xKpL3mN

# Ask a question (upload with process_for_chat=true first)
python chat_with_document.py doc_9xKpL3mN "ما إجمالي الفاتورة؟"
```

> The authoritative API reference is at [alqari.sa/api-docs](https://alqari.sa/api-docs).
