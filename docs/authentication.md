# Authentication

All ALQari API requests require authentication using a **Bearer token** (your API key).

---

## Getting an API Key

1. Sign in to [alqari.sa/dashboard](https://alqari.sa/dashboard)
2. Navigate to **API Keys**
3. Click **Create new key** (requires an organization Admin)
4. Copy the key immediately — the full key is shown only once

API keys start with `qari_` followed by 40 hex characters. They are stored hashed after creation, have **no scopes**, and **no create-time expiration**.

---

## Using Your API Key

Include your API key in the `Authorization` header of every request:

```
Authorization: Bearer YOUR_API_KEY
```

### cURL

```bash
curl https://api.alqari.sa/services/ocr-output/doc_9xKpL3mN/text \
  -H "Authorization: Bearer $ALQARI_API_KEY"
```

### Python

```python
import os, requests

headers = {"Authorization": f"Bearer {os.environ['ALQARI_API_KEY']}"}
resp = requests.get(
    "https://api.alqari.sa/services/ocr-output/doc_9xKpL3mN/text",
    headers=headers,
)
```

### Node.js

```js
const headers = {
  Authorization: `Bearer ${process.env.ALQARI_API_KEY}`
};
const resp = await fetch(
  "https://api.alqari.sa/services/ocr-output/doc_9xKpL3mN/text",
  { headers }
);
```

---

## Alternative: Session Token

For end-user apps, sign in via `POST /auth/login` with `email_or_phone` and `password` to receive an `access_token`, used in the `Authorization` header the same way:

```bash
curl -X POST https://api.alqari.sa/auth/login \
  -H "Content-Type: application/json" \
  -d '{ "email_or_phone": "you@company.sa", "password": "••••••••" }'
```

A successful response returns: `access_token`, `refresh_token`, `token_type`, `user_name`, `email`, `phone_number`.

Session tokens are short-lived — use a `qari_` key for long-running server integrations.

---

## Managing API Keys

Creating, listing, and revoking API keys requires an organization Admin.

| Method | Path | Summary |
|--------|------|---------|
| `POST` | `/api-keys` | Create a key (body: `{ "name": "..." }`) |
| `GET`  | `/api-keys` | List keys (metadata only, never the secret) |
| `DELETE` | `/api-keys/{id}` | Revoke a key |

```bash
curl -X POST https://api.alqari.sa/api-keys \
  -H "Authorization: Bearer <JWT>" \
  -H "Content-Type: application/json" \
  -d '{ "name": "Production server" }'
```

---

## Key Rotation

1. Create a new key in the dashboard
2. Update your application to use the new key
3. Delete (revoke) the old key

To revoke a compromised key immediately, go to **Dashboard → API Keys → Revoke**.

---

## Security Best Practices

- **Never** hardcode API keys in source code or commit them to public repositories.
- Use environment variables or a secrets manager (AWS Secrets Manager, HashiCorp Vault, etc.).
- Use the [`.env.example`](../.env.example) pattern for local development.
- Treat your API key like a password. If it leaks, revoke it immediately and issue a new one.

---

## Authentication Errors

| HTTP Status | Meaning                              |
|-------------|--------------------------------------|
| `401`       | Missing or invalid credentials       |
| `422`       | Malformed request body               |

Domain errors carry a stable machine-readable `code` — branch on `code`, not the message text. See [Errors](errors.md) for the full error response format.
