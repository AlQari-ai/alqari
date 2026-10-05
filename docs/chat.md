# Document Q&A

Ask natural-language questions about a document that has been processed for chat.

To enable chat on a document, upload it with `process_for_chat=true` (see [OCR](ocr.md)).

> The public chat response returns an `answer` and token usage only. It does **not** include page citations, source arrays, or bounding-box citations.

---

## Endpoint

```
POST /services/chat/{document_id}
```

---

## Request Body

```json
{
  "message": "ما إجمالي الفاتورة؟"
}
```

| Field     | Type   | Required | Description                                      |
|-----------|--------|----------|--------------------------------------------------|
| `message` | string | Yes      | The question or instruction in Arabic or English |

---

## Example

```bash
curl -X POST https://api.alqari.sa/services/chat/doc_9xKpL3mN \
  -H "Authorization: Bearer $ALQARI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{ "message": "ما إجمالي الفاتورة؟" }'
```

**Response:**

```json
{
  "document_id": "doc_9xKpL3mN",
  "question": "ما إجمالي الفاتورة؟",
  "answer": "إجمالي الفاتورة هو SAR 124,500.00",
  "tokens_used": { "input": 812, "output": 24 },
  "credits_consumed": 1,
  "remaining_credits": 4975
}
```

---

## Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `document_id` | string | The document being queried |
| `question` | string | The question you asked |
| `answer` | string | The model's answer |
| `tokens_used` | object | `{ input, output }` token counts |
| `credits_consumed` | integer | Credits used by this request |
| `remaining_credits` | integer | Credits remaining on the account |

---

## Notes

- The document must be uploaded with `process_for_chat=true` to enable chat.
- Questions can be asked in Arabic or English regardless of the document language.
- If chat is not yet ready, the API returns the `CHAT_NOT_READY` error code — see [Errors](errors.md).
