# Rate Limits

ALQari does not currently publish specific rate limits, and responses do **not** include guaranteed `X-RateLimit-*` or `Retry-After` headers. Excessive request volumes may be throttled.

> This behavior may change in the future. For current, authoritative details, see the official API docs: [alqari.sa/api-docs](https://alqari.sa/api-docs).

---

## Recommended Client Behavior

Because throttling can occur under excessive load, design clients to be resilient:

- Use **exponential backoff with jitter** when a request fails transiently.
- Do not assume `Retry-After` is present — fall back to your own backoff schedule.
- Avoid tight retry loops; cap the number of retries.

```python
import time, random, requests

def request_with_backoff(method, url, max_retries=5, **kwargs):
    for attempt in range(max_retries):
        resp = requests.request(method, url, **kwargs)
        if resp.status_code < 429:
            return resp
        # No guaranteed Retry-After header — use our own backoff
        retry_after = int(resp.headers.get("Retry-After", 2 ** attempt))
        time.sleep(retry_after + random.uniform(0, 1))
    return resp
```

---

## File & Workflow Limits

| Limit | Value |
|-------|-------|
| Upload file-size limit (`upload-ocr`) | 20 MB |
| Oversized file (`upload-ocr`) | `FILE_TOO_LARGE` / HTTP 413 |
| Workflow trigger file-count | Default max 20 files, hard max 100 files |

The 20 MB limit is the `upload-ocr` file size. The 20/100 file limits are workflow-trigger file counts — not an `upload-ocr` batch limit.

---

## Billing

Processing responses return `credits_consumed` and `remaining_credits` to reflect credit usage. For current pricing, see [alqari.sa/pricing](https://alqari.sa/pricing) or contact **sales@alqari.sa** for Enterprise options.
