# Webhooks

ALQari delivers workflow results to your own HTTPS endpoint by adding a **Webhook Output node** inside a workflow. There is no standalone webhook-registration REST endpoint — webhooks are configured as part of a workflow.

---

## How It Works

Add a Webhook Output node to a workflow. When the workflow runs, ALQari sends an HTTP `POST` with a JSON body to your endpoint.

| Property | Detail |
|----------|--------|
| Method | HTTP `POST`, JSON body |
| Timeout | 30 seconds |
| Redirects | Disabled |
| Destination | Public HTTPS URL, validated before delivery |
| Success | Considered delivered when the response status is `< 400` |

---

## Payload

```
POST https://your-app.com/webhooks/alqari
Content-Type: application/json

{
  "workflow_id": "wf_7dR2",
  "run_id": "run_5Qm1",
  "status": "completed"
}
```

Run statuses: `pending`, `running`, `completed`, `failed`, `paused`.

---

## Receiver Best Practices

- Use a public **HTTPS** endpoint.
- Design your receiver to be **idempotent** — the same run may be delivered more than once.
- Validate incoming requests with your own controls (e.g., a shared secret or allowlist).
- Respond quickly with a `2xx` status and process the payload asynchronously.

### Minimal Express.js receiver

```js
import express from "express";

const app = express();

app.post("/webhooks/alqari", express.json(), (req, res) => {
  const { workflow_id, run_id, status } = req.body;
  console.log("Workflow event:", workflow_id, run_id, status);

  // Respond quickly; process asynchronously.
  res.sendStatus(200);
});

app.listen(3000);
```

---

## Related

- Run a workflow and track its status → see the Workflows section in [API Overview](api-overview.md).
