# Postman Collection

Ready-to-use Postman collection and environment for the ALQari API.

## Import

1. Open **Postman** → **Import**
2. Select `alqari.postman_collection.json`
3. Select `alqari.postman_environment.json`
4. In the **Environments** panel, select **ALQari** and set `ALQARI_API_KEY` to your API key (starts with `qari_`)

## Variables

| Variable          | Description                         | Default                   |
|-------------------|-------------------------------------|---------------------------|
| `ALQARI_API_KEY`  | Your API key (set this manually)    | `qari_your_api_key_here`  |
| `ALQARI_BASE_URL` | API base URL (unversioned)          | `https://api.alqari.sa`   |
| `DOCUMENT_ID`     | Auto-set by the Upload & OCR request| —                         |

## Workflow

Run requests in this order for a complete end-to-end flow:

1. **Services / Upload & OCR** — sets `DOCUMENT_ID` automatically
2. **OCR Output / Get OCR Text** (or Structured OCR, Layout Analysis)
3. **Validation / Validate Document**
4. **Document Q&A / Chat with Document** — upload with `process_for_chat=true` first

## Regenerating

To regenerate from the OpenAPI spec:

```bash
python ../scripts/generate-postman.py
```

> The authoritative API reference is at [alqari.sa/api-docs](https://alqari.sa/api-docs).
