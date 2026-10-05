# Errors

ALQari uses conventional HTTP status codes. Domain errors carry a human-readable `detail` plus a stable machine-readable `code`.

> Branch your logic on the `code` field, not on the message text.

---

## Error Response Formats

### Domain error

```json
{
  "detail": "Document not found",
  "code": "DOCUMENT_NOT_FOUND",
  "violations": null,
  "context": null
}
```

Fields (`violations`, `context`) may be `null` depending on the error.

### Validation error (422)

```json
{
  "detail": [
    { "loc": ["body", "file"], "msg": "field required", "type": "missing" }
  ]
}
```

### Unexpected error (500)

```json
{
  "detail": "An unexpected error occurred. Please try again."
}
```

---

## HTTP Status Codes

| Status | Meaning                                                 |
|--------|---------------------------------------------------------|
| `200`  | OK — request succeeded                                  |
| `202`  | Accepted — async run started                            |
| `401`  | Unauthorized — missing or invalid credentials           |
| `404`  | Not Found — resource does not exist                     |
| `413`  | Payload Too Large — file exceeds the 20 MB limit        |
| `422`  | Unprocessable Entity — request body failed validation   |
| `500`  | Internal Server Error — unexpected server error         |

---

## Stable Error Codes

Branch your logic on the `code` field. The stable codes are:

| Code                        | Description                                           |
|-----------------------------|-------------------------------------------------------|
| `DOCUMENT_NOT_FOUND`        | Document ID does not exist                            |
| `OCR_NOT_READY`             | OCR output requested before processing completed      |
| `CHAT_NOT_READY`            | Chat requested before the document is processed for chat |
| `CHAT_SERVICE_UNAVAILABLE`  | Chat service is temporarily unavailable               |
| `PREMIUM_OCR_UNAVAILABLE`   | A premium OCR output was requested but is unavailable |
| `UNSUPPORTED_FILE_TYPE`     | Uploaded file type is not supported                   |
| `CORRUPTED_FILE`            | Uploaded file could not be read                       |
| `FILE_TOO_LARGE`            | File exceeds the upload size limit (HTTP 413)         |
| `WORKFLOW_NOT_ACTIVE`       | The target workflow is not active                     |

---

## Rate Limiting

ALQari does not currently publish specific rate limits, and responses do not include guaranteed `X-RateLimit-*` or `Retry-After` headers. Excessive request volumes may be throttled. See [Rate Limits](rate-limits.md).

---

## Troubleshooting

| Symptom | Likely Cause | Fix |
|---------|--------------|-----|
| `401` | Missing `Authorization` header | Add `Authorization: Bearer $ALQARI_API_KEY` |
| `DOCUMENT_NOT_FOUND` | Wrong document ID | Verify the `document_id` from the upload response |
| `OCR_NOT_READY` | Output requested too early | Retry after processing completes |
| `CHAT_NOT_READY` | Chat not enabled | Upload with `process_for_chat=true` |
| `FILE_TOO_LARGE` (413) | File > 20 MB | Compress or split the file |

---

## Contact Support

If a problem persists, contact **support@alqari.sa** with details of the failing request.
