# Node.js Examples

Copy-paste ready Node.js scripts for the ALQari API.

## Requirements

Node.js 18+ (uses native `fetch` and ES modules)

```bash
npm install
```

## Configuration

```bash
export ALQARI_API_KEY="qari_your_api_key_here"
export ALQARI_BASE_URL="https://api.alqari.sa"   # optional, this is the default
```

## Scripts

| Script | Description |
|--------|-------------|
| `upload-document.js`   | Upload a document and run OCR (`POST /services/upload-ocr`) |
| `get-ocr-output.js`    | Fetch OCR output (`GET /services/ocr-output/{id}/ocr\|text\|layout`) |
| `validate-document.js` | Run rule-based validation (`POST /services/ai-validate`) |
| `chat-with-document.js`| Ask a question about a document (`POST /services/chat/{id}`) |

## Usage

```bash
# Upload + OCR → returns document_id
node upload-document.js /path/to/document.pdf

# Retrieve structured OCR regions (or: text | layout)
node get-ocr-output.js doc_9xKpL3mN
node get-ocr-output.js doc_9xKpL3mN text

# Validate against your own rules
node validate-document.js doc_9xKpL3mN

# Ask a question (upload with process_for_chat=true first)
node chat-with-document.js doc_9xKpL3mN "ما إجمالي الفاتورة؟"
```

> The authoritative API reference is at [alqari.sa/api-docs](https://alqari.sa/api-docs).
