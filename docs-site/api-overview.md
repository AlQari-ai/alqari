# API Overview

ALQari exposes a REST API over HTTPS to upload documents, run Arabic and English OCR with structured text (coordinates and confidence), analyze layout, run rule-based validation, ask natural-language questions about a document, and automate workflows.

> The authoritative, always-current reference is the official API docs: **[alqari.sa/api-docs](https://alqari.sa/api-docs)**.

---

## Contents

1. [Base URL](#base-url)
2. [Authentication](#authentication)
3. [Request & Response Conventions](#request--response-conventions)
4. [Versioning](#versioning)
5. [Endpoint Reference](#endpoint-reference)
   - [Upload & OCR](#upload--ocr)
   - [OCR outputs](#ocr-outputs)
   - [Validation](#validation)
   - [Document Q&A](#document-qa)
   - [Workflows](#workflows)
6. [Common API Flows](#common-api-flows)
7. [Developer Notes](#developer-notes)

---

## Base URL

| Environment | Base URL                   |
|-------------|----------------------------|
| Production  | `https://api.alqari.sa`    |

Always use HTTPS. Paths are currently **unversioned** — there is no `/v1/` or `/v2/` prefix.

---

## Authentication

All endpoints require a **Bearer token**. Create an API key (starts with `qari_`) from your dashboard and pass it in the `Authorization` header on every request:

```
Authorization: Bearer <ALQARI_API_KEY>
```

### Example

```bash
curl https://api.alqari.sa/services/ocr-output/doc_9xKpL3mN/text \
  -H "Authorization: Bearer $ALQARI_API_KEY"
```

### Alternative: session token

For end-user apps, sign in via `POST /auth/login` with `email_or_phone` and `password` to receive an `access_token`, used in the `Authorization` header the same way. Session tokens are short-lived — use a `qari_` key for long-running server integrations.

### Security rules

- Store keys in environment variables or a secrets manager — never in source code.
- Never expose API keys in browser-side JavaScript or mobile app bundles.
- API keys have no scopes and no create-time expiration; the full key is shown only once at creation.
- Rotate production keys immediately if compromised — see [Dashboard → API Keys](https://alqari.sa/dashboard/api-keys).

---

## Request & Response Conventions

| Convention | Detail |
|---|---|
| **Encoding** | UTF-8 for all request and response bodies |
| **JSON requests** | `Content-Type: application/json` |
| **File uploads** | `multipart/form-data` — do not set `Content-Type` manually |
| **Response formats** | Vary by endpoint: JSON, plain text, or HTML |
| **Success codes** | `200 OK`, `202 Accepted` |
| **Domain error body** | `{ "detail", "code", "violations", "context" }` — branch on `code`, not message text |
| **Validation error body** | `422` — `{ "detail": [ { "loc", "msg", "type" } ] }` |
| **Billing fields** | Processing responses include `credits_consumed` and `remaining_credits` |

See [Errors](errors.md) for the full list of stable error codes.

---

## Versioning

Paths are currently **unversioned**: there is no `/v1/` or `/v2/` prefix, no version header, and no versioned host. This may change in the future.

---

## Endpoint Reference

### Upload & OCR

Upload a file and run OCR in one step.

| Method | Path | Summary | Auth | Request Type | Success Response |
|--------|------|---------|------|--------------|-----------------|
| `POST` | `/services/upload-ocr` | Upload a file and run OCR | Bearer | `multipart/form-data` | `200` — upload result |

**Query parameters:**

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `skip_vlm` | boolean | `true` | Skip the advanced visual analysis step |
| `mode` | `fast` \| `premium` | — | Processing tier |
| `language` | `auto` \| `ar` \| `en` | — | Document language hint |
| `department_id` | string | — | Optional department association |
| `process_for_chat` | boolean | `false` | Enable later Document Q&A |

**Response fields:** `document_id`, `file_name`, `pages`, `processing_time`, `total_words`, `document_language`, `text`, `credits_consumed`, `remaining_credits`, `included_outputs` (`text_url`, `markdown_url`, `html_url`, `blocks_url`), and `premium_outputs` (`layout_url`, `extraction_url`).

> `extraction_url` returns the structured OCR-region output (text, confidence, bounding boxes, page references). It is **not** a generic custom-field extraction endpoint — there is no public custom-schema extraction API.

See [Upload Documents](upload-documents.md) for file support and limits.

---

### OCR outputs

Retrieve outputs derived from the OCR job using the `document_id`.

| Method | Path | Summary | Returns |
|--------|------|---------|---------|
| `GET` | `/services/ocr-output/{document_id}/text` | Full extracted text | `text/plain` |
| `GET` | `/services/ocr-output/{document_id}/ocr` | Structured OCR regions | JSON |
| `GET` | `/services/ocr-output/{document_id}/layout` | Layout analysis | JSON |
| `GET` | `/services/ocr-output/{document_id}/markdown` | Markdown | text/Markdown |
| `GET` | `/services/ocr-output/{document_id}/html` | HTML | HTML |
| `GET` | `/services/ocr-output/{document_id}/blocks` | Interactive blocks viewer | HTML (not JSON) |

**Structured OCR (`/ocr`)** returns `results[]`, each element carrying:

| Field | Type | Description |
|-------|------|-------------|
| `text` | string | Recognized text for the region |
| `confidence` | number | OCR recognition confidence, `0.0`–`1.0` |
| `bbox` | number[][] | 4-corner polygon: top-left, top-right, bottom-right, bottom-left (page-relative, not normalized) |
| `page` | integer | Page number |

The response also includes `credits_consumed` and `remaining_credits`.

See [OCR](ocr.md) for full examples.

---

### Validation

Run rule-based AI validation against an already-processed document.

| Method | Path | Summary | Auth | Request Type | Success Response |
|--------|------|---------|------|--------------|-----------------|
| `POST` | `/services/ai-validate` | Run validation rules | Bearer | query params | `200` — ValidationResult |

**Query parameters:** `document_id` (required), `rules_text` (required, newline-numbered rules).

Per-rule `verdict` values are `PASS`, `FAIL`, `WARNING`, or `N/A`. `bounding_boxes` may be `null` or `[]`, so do not assume every rule has coordinates.

See [Validation](validation.md).

---

### Document Q&A

Ask a natural-language question about a document processed with `process_for_chat=true`.

| Method | Path | Summary | Auth | Request Type | Success Response |
|--------|------|---------|------|--------------|-----------------|
| `POST` | `/services/chat/{document_id}` | Ask a question about a document | Bearer | `application/json` | `200` — ChatResponse |

The public chat response returns an `answer` and token usage only. It does not include page citations, source arrays, or bounding-box citations.

See [Chat](chat.md).

---

### Workflows

Run published automation workflows and track their runs.

| Method | Path | Summary | Auth | Success Response |
|--------|------|---------|------|-----------------|
| `POST` | `/workflows/{workflow_id}/run-upload` | Run a workflow by uploading a file | `qari_` API key | `200` — run object |
| `POST` | `/workflows/{workflow_id}/test-run-upload/async` | Start an async run | `qari_` API key | `202` — pending run |
| `GET` | `/workflows/runs/{run_id}` | Get run status/result | Bearer | `200` — run object |

Run statuses: `pending`, `running`, `completed`, `failed`, `paused`.

To build pipelines outside the ALQari canvas (n8n, Odoo, or any HTTP client), use the `/services/integration/*` endpoints: `upload-ocr`, `extract-fields`, and `human-review`.

---

## Common API Flows

### Flow 1 — Upload → Structured OCR

The most common flow. Turn a scanned PDF into searchable, machine-readable text.

```
1. POST /services/upload-ocr                          → document_id
2. GET  /services/ocr-output/{document_id}/ocr        → results[]{text,confidence,bbox,page}
   (or /text for plain text, /layout for layout analysis)
```

```bash
# Step 1 — upload + OCR
DOC=$(curl -sX POST https://api.alqari.sa/services/upload-ocr \
  -H "Authorization: Bearer $ALQARI_API_KEY" \
  -F "file=@invoice.pdf" | jq -r .document_id)

# Step 2 — retrieve structured OCR regions
curl -s https://api.alqari.sa/services/ocr-output/$DOC/ocr \
  -H "Authorization: Bearer $ALQARI_API_KEY"
```

---

### Flow 2 — Upload (chat) → Document Q&A

Let users query a document in natural language.

```
1. POST /services/upload-ocr?process_for_chat=true    → document_id
2. POST /services/chat/{document_id}                  → answer
```

```bash
DOC=$(curl -sX POST "https://api.alqari.sa/services/upload-ocr?process_for_chat=true" \
  -H "Authorization: Bearer $ALQARI_API_KEY" \
  -F "file=@invoice.pdf" | jq -r .document_id)

curl -sX POST https://api.alqari.sa/services/chat/$DOC \
  -H "Authorization: Bearer $ALQARI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"message":"ما إجمالي الفاتورة؟"}'
```

---

### Flow 3 — Upload → Validate

Check a processed document against your own rules.

```
1. POST /services/upload-ocr                          → document_id
2. POST /services/ai-validate?document_id=...&rules_text=...   → verdicts
```

```bash
curl -sX POST "https://api.alqari.sa/services/ai-validate?document_id=$DOC&rules_text=1.%20Check%20required%20fields" \
  -H "Authorization: Bearer $ALQARI_API_KEY"
```

---

## Developer Notes

### Environment

- The base URL can be injected via the `ALQARI_BASE_URL` environment variable (defaults to `https://api.alqari.sa`).
- There is no public sandbox host; test against production with your own API key.

### API Key Security

- **Never** embed API keys in frontend code (HTML, JS bundles, mobile apps).
- Use environment variables or a secrets manager (AWS Secrets Manager, Azure Key Vault, HashiCorp Vault).
- Create separate keys per environment and rotate on exposure.

### Processing

Upload-and-OCR completes within the request — configure appropriate HTTP timeouts for larger documents. The async workflow endpoint returns `202` with a `run_id`; poll `GET /workflows/runs/{run_id}` for the outcome.
