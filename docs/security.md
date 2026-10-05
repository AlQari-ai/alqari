# Security

Security best practices for integrating with ALQari APIs.

---

## Transport Security

- All ALQari API traffic is encrypted with **TLS 1.2 or higher**.
- Always use HTTPS; never send credentials over plain HTTP.

---

## API Key Security

API keys start with `qari_`, have no scopes, and are shown in full only once at creation. Treat your API key like a password.

### Do

- Store API keys in environment variables or a secrets manager (AWS Secrets Manager, Azure Key Vault, HashiCorp Vault, etc.)
- Use the `.env.example` pattern for local development (excluded from git by `.gitignore`)
- Use separate keys for each environment (development, staging, production)
- Rotate keys regularly and immediately after any suspected exposure

### Do Not

- Hardcode keys in source code
- Commit `.env` files or keys to version control
- Share keys across teams or services
- Expose keys in client-side (browser) code or mobile app bundles
- Log keys in application logs

### Check for Exposed Keys

```bash
# Scan your repo history for accidentally committed secrets
git log -p | grep "qari_"
```

Use tools like [truffleHog](https://github.com/trufflesecurity/trufflehog) or [git-secrets](https://github.com/awslabs/git-secrets) in your CI pipeline. If a key leaks, revoke it immediately from the dashboard and issue a new one.

---

## Webhook Security

Webhooks are delivered from within a workflow via an HTTP POST to your own HTTPS endpoint. When receiving webhook deliveries:

- Use an HTTPS endpoint; deliveries to public HTTP are not supported.
- Design your receiver to be **idempotent**.
- Validate incoming requests with your own controls.
- Deliveries have a 30-second timeout and redirects are disabled; a delivery is considered successful when your response status is `< 400`.

See [Webhooks](webhooks.md).

---

## Data Privacy

- Documents are scoped to your organization.
- For data residency or privacy requirements, contact **privacy@alqari.sa**.

---

## Responsible Disclosure

Found a security vulnerability? See [SECURITY.md](../SECURITY.md).
