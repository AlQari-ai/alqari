# Quickstart

Get your first OCR result in under 5 minutes.

## Prerequisites

- An ALQari account — [sign up free](https://alqari.sa/signup)
- An API key (starts with `qari_`) — [generate one](https://alqari.sa/dashboard/api-keys)
- `curl`, Python 3.8+, or Node.js 18+

---

## Step 1 — Set your API key

```bash
export ALQARI_API_KEY="qari_your_api_key_here"
```

> **Tip:** Add this to your shell profile (`~/.bashrc`, `~/.zshrc`) or use a `.env` file (see [`.env.example`](../.env.example)).

---

## Step 2 — Upload a document and run OCR

Upload and OCR happen in a single step. Send `multipart/form-data` with a `file` field — do not set the `Content-Type` header manually.

```bash
curl -X POST https://api.alqari.sa/services/upload-ocr \
  -H "Authorization: Bearer $ALQARI_API_KEY" \
  -F "file=@/path/to/document.pdf"
```

**Response:**

```json
{
  "document_id": "doc_9xKpL3mN",
  "file_name": "document.pdf",
  "pages": 3,
  "processing_time": 4.21,
  "total_words": 512,
  "document_language": "ar",
  "text": "فاتورة ضريبية ...",
  "credits_consumed": 3,
  "remaining_credits": 4977,
  "included_outputs": {
    "text_url": "https://api.alqari.sa/services/ocr-output/doc_9xKpL3mN/text",
    "markdown_url": "https://api.alqari.sa/services/ocr-output/doc_9xKpL3mN/markdown",
    "html_url": "https://api.alqari.sa/services/ocr-output/doc_9xKpL3mN/html",
    "blocks_url": "https://api.alqari.sa/services/ocr-output/doc_9xKpL3mN/blocks"
  },
  "premium_outputs": {
    "layout_url": "https://api.alqari.sa/services/ocr-output/doc_9xKpL3mN/layout",
    "extraction_url": "https://api.alqari.sa/services/ocr-output/doc_9xKpL3mN/ocr"
  }
}
```

Save the `document_id` — you'll use it to retrieve outputs.

**Optional query parameters:** `mode=fast|premium`, `language=auto|ar|en`, `process_for_chat=true`, `skip_vlm`, `department_id`. For example:

```bash
curl -X POST "https://api.alqari.sa/services/upload-ocr?mode=premium&language=ar" \
  -H "Authorization: Bearer $ALQARI_API_KEY" \
  -F "file=@invoice_2024.pdf"
```

---

## Step 3 — Retrieve structured OCR

Fetch the structured OCR regions. Each region carries the text, OCR confidence, a 4-point bounding box, and the page number.

```bash
curl https://api.alqari.sa/services/ocr-output/doc_9xKpL3mN/ocr \
  -H "Authorization: Bearer $ALQARI_API_KEY"
```

**Response:**

```json
{
  "results": [
    {
      "text": "Invoice No: INV-0001",
      "confidence": 0.984,
      "bbox": [
        [72.0, 118.0],
        [268.0, 118.0],
        [268.0, 138.0],
        [72.0, 138.0]
      ],
      "page": 1
    }
  ],
  "credits_consumed": 0,
  "remaining_credits": 4980
}
```

For plain text use `/text`, and for layout analysis (blocks, tables, figures) use `/layout`.

---

## What's Next?

- Retrieve OCR outputs in every format → [OCR](ocr.md)
- Validate document data → [Validation](validation.md)
- Chat with the document → [Chat](chat.md)
- Review the full endpoint list → [API Overview](api-overview.md)

---

## Language Support

| Value    | Description                  |
|----------|------------------------------|
| `auto`   | Auto-detect (default)        |
| `ar`     | Arabic (printed & handwriting) |
| `en`     | English                      |
