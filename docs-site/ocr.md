# OCR

Extract text from scanned, photographed, or printed Arabic and English documents — including Arabic handwriting.

Upload and OCR happen in a single step via `POST /services/upload-ocr`. The resulting outputs (plain text, structured regions, layout, markdown, HTML) are retrieved from `GET /services/ocr-output/{document_id}/...`.

---

## Upload & run OCR

```
POST /services/upload-ocr
```

Send as `multipart/form-data` with a `file` field. Do not set the `Content-Type` header manually. Processing completes within the request — configure appropriate HTTP timeouts for larger documents.

### Query parameters

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `skip_vlm` | boolean | `true` | Skip the advanced visual analysis step |
| `mode` | `fast` \| `premium` | — | Processing tier |
| `language` | `auto` \| `ar` \| `en` | — | Document language hint |
| `department_id` | string | — | Optional department association |
| `process_for_chat` | boolean | `false` | Enable later [Document Q&A](chat.md) |

### Optional header

| Header | Description |
|--------|-------------|
| `Idempotency-Key` | Optional. Supply a unique key per upload for billing de-duplication only: if a request that was already billed is retried with the same key, it is not charged again. It is not a response cache, does not replay a stored result, and has no documented TTL or retry window. |

> The `Idempotency-Key` header is read manually from the request, so it is absent from the backend-generated OpenAPI. It is documented here in prose only.

### Example — Arabic, premium tier

```bash
curl -X POST "https://api.alqari.sa/services/upload-ocr?mode=premium&language=ar&process_for_chat=true" \
  -H "Authorization: Bearer $ALQARI_API_KEY" \
  -F "file=@invoice_2024.pdf"
```

### Upload response

```json
{
  "document_id": "doc_9xKpL3mN",
  "file_name": "invoice_2024.pdf",
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

> `extraction_url` is the structured OCR-region output — it is **not** a generic custom-field extraction endpoint.

---

## Plain text output

```
GET /services/ocr-output/{document_id}/text
```

Returns the full extracted text as `text/plain`.

```bash
curl https://api.alqari.sa/services/ocr-output/doc_9xKpL3mN/text \
  -H "Authorization: Bearer $ALQARI_API_KEY"
```

```
Content-Type: text/plain

فاتورة ضريبية
Invoice No: INV-0001
...
```

---

## Structured OCR output

```
GET /services/ocr-output/{document_id}/ocr
```

Returns the structured OCR regions as JSON. Each element carries the text, its confidence, a 4-point bounding box, and the page number.

```bash
curl https://api.alqari.sa/services/ocr-output/doc_9xKpL3mN/ocr \
  -H "Authorization: Bearer $ALQARI_API_KEY"
```

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

### `results[]` fields

| Field | Type | Description |
|-------|------|-------------|
| `text` | string | Recognized text for the region |
| `confidence` | number | OCR recognition confidence, `0.0`–`1.0` |
| `bbox` | number[][] | 4-corner polygon (see below) |
| `page` | integer | Page number |

### Bounding boxes

`results[].bbox` is a 4-corner polygon in order: top-left, top-right, bottom-right, bottom-left. The origin is the top-left of the page. Coordinates are page-relative, use the native page units of the input, and are **not** normalized.

```json
"bbox": [
  [x1, y1],
  [x2, y2],
  [x3, y3],
  [x4, y4]
]
```

Note: the OCR box (`results[].bbox`) is a 4-point polygon, while the layout box (`layout.blocks[].bbox`) is a rectangle `[left, top, right, bottom]`. The two shapes are different.

### Confidence scores

`results[].confidence` is OCR recognition confidence for the region (`0.0`–`1.0`). This is not a business-field confidence score. Layout block confidence is returned under a different key: `layout.blocks[].conf`.

| Range     | Meaning                                 |
|-----------|-----------------------------------------|
| 0.95–1.00 | Excellent — reliable                    |
| 0.80–0.94 | Good — minor corrections may be needed  |
| 0.60–0.79 | Fair — review recommended               |
| < 0.60    | Low — manual review required            |

---

## Layout output

```
GET /services/ocr-output/{document_id}/layout
```

Returns the document layout analysis as JSON: blocks, tables, figures, and page sizes. The layout block box is a rectangle `[left, top, right, bottom]`.

```json
{
  "source": "invoice_2024.pdf",
  "pages": 1,
  "page_sizes": { "1": [826, 1280] },
  "blocks": [
    {
      "id": 0,
      "text": "Invoice No: INV-0001",
      "conf": 0.984,
      "bbox": [72, 118, 268, 138],
      "block_type": "paragraph",
      "page": 1,
      "raw_label": "paragraph"
    }
  ],
  "tables": [],
  "figures": [],
  "credits_consumed": 0,
  "remaining_credits": 4980
}
```

---

## Other rendered formats

| Endpoint | Returns |
|----------|---------|
| `GET /services/ocr-output/{document_id}/markdown` | Markdown |
| `GET /services/ocr-output/{document_id}/html` | HTML |
| `GET /services/ocr-output/{document_id}/blocks` | HTML (interactive blocks viewer) — not JSON |

For structured JSON use the `/ocr` or `/layout` endpoints.

---

## Supported languages

| Value    | Description                    |
|----------|--------------------------------|
| `auto`   | Auto-detect (default)          |
| `ar`     | Arabic (printed & handwriting) |
| `en`     | English                        |
