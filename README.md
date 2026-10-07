<div align="center">

<img src="assets/demo-thumbnail.png" alt="ALQari Developer Hub" width="180"/>

# ALQari Developer Hub

**ALQari is an Arabic-first Document Intelligence & Workflow Automation platform.** It turns Arabic and English documents into trusted, structured data over a single REST API — printed OCR, Arabic handwriting recognition, layout understanding, structured data extraction, rule-based validation, Human-in-the-Loop review, document Q&A, and workflow automation. OCR is one stage of the pipeline, not the end product.

[![Validate OpenAPI](https://github.com/AlQari-ai/.github/actions/workflows/validate-openapi.yml/badge.svg)](https://github.com/AlQari-ai/.github/actions/workflows/validate-openapi.yml)
[![Markdown Lint](https://github.com/AlQari-ai/.github/actions/workflows/markdown-lint.yml/badge.svg)](https://github.com/AlQari-ai/.github/actions/workflows/markdown-lint.yml)
[![Test Examples](https://github.com/AlQari-ai/.github/actions/workflows/test-examples.yml/badge.svg)](https://github.com/AlQari-ai/.github/actions/workflows/test-examples.yml)
[![Deploy Docs](https://github.com/AlQari-ai/.github/actions/workflows/deploy-docs.yml/badge.svg)](https://github.com/AlQari-ai/.github/actions/workflows/deploy-docs.yml)
[![OpenAPI](https://img.shields.io/badge/OpenAPI-3.1-green?logo=openapi-initiative)](openapi/openapi.yaml)
[![License](https://img.shields.io/badge/license-MIT-blue)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen)](CONTRIBUTING.md)

</div>

---

![ALQari Demo](assets/alqari-demo.gif)

## Quickstart (3 steps)

### 1 — Get your API key

Sign up at **[alqari.sa](https://alqari.sa)** → **Dashboard** → **API Keys** → create a new key.

```bash
export ALQARI_API_KEY="your_api_key_here"
```

### 2 — Upload a document and run OCR

Upload and OCR happen in a single step. Send `multipart/form-data` with a `file` field.

```bash
curl -X POST https://api.alqari.sa/services/upload-ocr \
  -H "Authorization: Bearer $ALQARI_API_KEY" \
  -F "file=@invoice.pdf"
```

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

### 3 — Retrieve structured OCR output

Use the `document_id` from step 2 to fetch structured OCR regions (text, confidence, bounding box, page).

```bash
curl https://api.alqari.sa/services/ocr-output/doc_9xKpL3mN/ocr \
  -H "Authorization: Bearer $ALQARI_API_KEY"
```

<img src="assets/sample-ar-handwriting.jpg" alt="Sample Arabic handwritten document" width="420" align="right" style="margin-left:16px;border:1px solid #ddd;border-radius:4px;" />

Structured OCR response (`GET /services/ocr-output/{document_id}/ocr`). Each region carries the recognized text, OCR confidence (`0.0`–`1.0`), a 4-point bounding-box polygon, and the page number:

```json
{
  "results": [
    {
      "text": "الأمية معوقة للتنمية في كل المجالات",
      "confidence": 0.7835,
      "bbox": [[614, 298], [1494, 298], [1494, 394], [614, 394]],
      "page": 1
    },
    {
      "text": "١/ الأمية وأسبابها :.",
      "confidence": 0.7012,
      "bbox": [[1327, 444], [1879, 444], [1879, 554], [1327, 554]],
      "page": 1
    }
  ],
  "credits_consumed": 0,
  "remaining_credits": 4980
}
```

The `bbox` is a 4-corner polygon in order top-left, top-right, bottom-right, bottom-left, in the native page units (not normalized). For plain text use `/text`, and for document layout (blocks, tables, figures) use `/layout`.

> Full sample output → [`examples/sample-output/ocr-response.json`](examples/sample-output/ocr-response.json)

---

## What ALQari Can Do

| Capability              | Description                                                        |
|-------------------------|-------------------------------------------------------------------|
| **OCR**                 | Extract text from printed Arabic & English documents              |
| **Handwriting OCR**     | Recognize Arabic handwritten text                                 |
| **Structured OCR**      | Per-region text with confidence scores and bounding-box polygons  |
| **Layout analysis**     | Blocks, tables, and figures with page sizes                       |
| **Validation**          | Run rule-based AI validation against processed documents          |
| **Document Q&A**        | Ask natural-language questions about a processed document         |
| **Workflow automation** | Run published workflows and integrate via n8n / Odoo             |

---

## Comparison & Evaluation

ALQari publishes a transparent capability comparison across leading document intelligence solutions, covering:

- Arabic printed OCR and English OCR
- Arabic handwriting recognition
- Tables, layout detection, and structured extraction
- Validation and confidence / grounding
- Human-in-the-Loop review
- Workflow automation
- API, private / self-host deployment, and enterprise integration

Each cell reflects what is publicly documented at the time of writing; a lack of documentation is not recorded as a negative. Accuracy figures are not claimed as independent benchmark scores. For how measured results should be evaluated reproducibly, see the [Arabic Document Intelligence Benchmark Methodology](docs/arabic-document-intelligence-benchmark-methodology.md).

- Comparison (English): **[alqari.sa/benchmark](https://alqari.sa/benchmark)**
- Comparison (Arabic): **[alqari.sa/ar/benchmark](https://alqari.sa/ar/benchmark)**

---

## Repository Structure

```
alqari-developer-hub/
├── docs/               # Full API reference and guides
├── openapi/            # OpenAPI 3.1 specification (JSON + YAML)
├── examples/
│   ├── curl/           # cURL one-liners for every endpoint
│   ├── python/         # Python examples using requests
│   └── node/           # Node.js examples using fetch
├── postman/            # Postman collection + environment
├── scripts/            # Developer utility scripts
└── .github/workflows/  # CI: OpenAPI validation, markdown lint
```

---

## Documentation

| Guide | Description |
|-------|-------------|
| [Quickstart](docs/quickstart.md) | Upload your first document in minutes |
| [Authentication](docs/authentication.md) | API key setup and Bearer token usage |
| [API Overview](docs/api-overview.md) | Endpoints, versioning, and base URL |
| [Upload Documents](docs/upload-documents.md) | Supported formats and upload options |
| [OCR](docs/ocr.md) | Printed and handwritten Arabic OCR |
| [Validation](docs/validation.md) | Rule-based AI validation |
| [Chat](docs/chat.md) | Document Q&A |
| [Errors](docs/errors.md) | Error codes and troubleshooting |
| [Rate Limits](docs/rate-limits.md) | Throttling behavior |
| [Security](docs/security.md) | Security practices |

The official, always-current API reference is at **[alqari.sa/api-docs](https://alqari.sa/api-docs)**.

---

## Code Examples

### Python

```python
import os, requests

API_KEY = os.environ["ALQARI_API_KEY"]
BASE_URL = "https://api.alqari.sa"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

# Upload and run OCR in one step
with open("invoice.pdf", "rb") as f:
    resp = requests.post(f"{BASE_URL}/services/upload-ocr",
                         headers=HEADERS, files={"file": f})
doc_id = resp.json()["document_id"]

# Retrieve structured OCR regions
ocr = requests.get(f"{BASE_URL}/services/ocr-output/{doc_id}/ocr",
                   headers=HEADERS)
print(ocr.json())
```

### Node.js

```js
import fetch from "node-fetch";
import FormData from "form-data";
import fs from "fs";

const BASE = "https://api.alqari.sa";
const HEADERS = { Authorization: `Bearer ${process.env.ALQARI_API_KEY}` };

const form = new FormData();
form.append("file", fs.createReadStream("invoice.pdf"));

const upload = await fetch(`${BASE}/services/upload-ocr`, {
  method: "POST",
  headers: { ...HEADERS, ...form.getHeaders() },
  body: form
});
const { document_id } = await upload.json();

const ocr = await fetch(`${BASE}/services/ocr-output/${document_id}/ocr`, {
  headers: HEADERS
});
console.log(await ocr.json());
```

---

## OpenAPI Specification

The full OpenAPI 3.1 spec lives in [`openapi/`](openapi/). Import it into Postman, Insomnia, or any API client.

### Fetch the latest spec from the live API

**Install dependencies once:**

```bash
pip install requests pyyaml
```

**Run:**

```bash
python scripts/fetch-openapi.py
```

The script probes these URLs in order and uses the first valid OpenAPI document it finds:

```
https://api.alqari.sa/openapi.json
https://api.alqari.sa/api/openapi.json
https://api.alqari.sa/swagger.json
https://api.alqari.sa/docs/openapi.json
```

On success it writes `openapi/openapi.json` and `openapi/openapi.yaml`, then prints a summary:

```
========================================================
  OpenAPI Specification Summary
========================================================
  Title      : ALQari Document Intelligence API
  Version    : (from live spec)
  Paths      : (from live spec)
  Operations : (from live spec)
  Tags       : Services, OCR, Validation, Chat, Workflows
========================================================
```

If no spec is found, the script exits with a clear error listing every URL it tried.

> **`ALQARI_API_KEY`** is sent as a Bearer token when set, and is never printed or logged. The variable is optional for public spec endpoints.

---

## Postman

Import [`postman/alqari.postman_collection.json`](postman/alqari.postman_collection.json) and [`postman/alqari.postman_environment.json`](postman/alqari.postman_environment.json) into Postman, set `ALQARI_API_KEY`, and run any request immediately.

---

## Contributing

We welcome issues, corrections, and example contributions. See [CONTRIBUTING.md](CONTRIBUTING.md).

---

## Security

Do not commit API keys. See [SECURITY.md](SECURITY.md) for our responsible disclosure policy.

---

## License

[MIT](LICENSE) © ALQari

## Links

- Website: https://alqari.sa
- API docs: https://alqari.sa/api-docs
- Pricing: https://alqari.sa/pricing
