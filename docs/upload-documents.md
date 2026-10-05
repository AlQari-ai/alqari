# Upload Documents

Upload a file to ALQari and run OCR in one step. The same `document_id` is then used to retrieve OCR outputs, run validation, or ask questions.

---

## Endpoint

```
POST /services/upload-ocr
```

**Content-Type:** `multipart/form-data` — do not set the header manually.

---

## Supported File Types

Accepted upload file types are governed by an allowlist:

```
.pdf .png .jpg .jpeg .tif .tiff .bmp .webp .docx .doc .txt .md .csv .json .xml .html
```

Not all types behave identically for OCR.

| Limit | Value |
|-------|-------|
| Upload file-size limit | **20 MB** |
| Oversized file | `FILE_TOO_LARGE` / HTTP `413` |

---

## Request

| Parameter | Location | Type | Required | Description |
|-----------|----------|------|----------|-------------|
| `file` | form field | file | Yes | The document file |
| `skip_vlm` | query | boolean | No | Skip the advanced visual analysis step (default `true`) |
| `mode` | query | `fast` \| `premium` | No | Processing tier |
| `language` | query | `auto` \| `ar` \| `en` | No | Document language hint |
| `department_id` | query | string | No | Optional department association |
| `process_for_chat` | query | boolean | No | Enable later [Document Q&A](chat.md) (default `false`) |
| `Idempotency-Key` | header | string | No | Optional. Used for billing de-duplication only: a request already billed is not charged again when retried with the same key. Not a response cache, does not replay a stored result, and has no documented TTL or retry window. |

> The `Idempotency-Key` header is read manually from the request, so it is absent from the backend-generated OpenAPI. It is documented here in prose only.

---

## Example

```bash
curl -X POST "https://api.alqari.sa/services/upload-ocr?mode=premium&language=ar" \
  -H "Authorization: Bearer $ALQARI_API_KEY" \
  -F "file=@invoice.pdf"
```

---

## Response

```json
{
  "document_id": "doc_9xKpL3mN",
  "file_name": "invoice.pdf",
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

---

## Document Statuses

Document processing status is persisted as one of:

| Status        | Description                           |
|---------------|---------------------------------------|
| `processing`  | OCR is running                        |
| `completed`   | Processing is done                    |
| `failed`      | Processing failed                     |

---

## Next Steps

- Retrieve OCR outputs → [OCR](ocr.md)
- Validate the document → [Validation](validation.md)
- Ask questions about it → [Chat](chat.md) (upload with `process_for_chat=true`)
