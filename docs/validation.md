# Validation

Run rule-based AI validation against an already-processed document. You supply a set of numbered rules as text; ALQari returns a verdict per rule plus an overall verdict.

> Results are not always perfect — have a human review critical outcomes.

---

## Endpoint

```
POST /services/ai-validate
```

Parameters are passed as **query parameters**.

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `document_id` | string | Yes | The already-processed document |
| `rules_text` | string | Yes | Newline-numbered validation rules |

### Optional header

| Header | Description |
|--------|-------------|
| `Idempotency-Key` | Optional. Used for billing de-duplication only: if a request that was already billed is retried with the same key, it is not charged again. It is not a response cache, does not replay the validation response, and has no documented TTL or retry window. |

> The `Idempotency-Key` header is read manually from the request, so it is absent from the backend-generated OpenAPI. It is documented here in prose only.

---

## Example

```bash
curl -X POST "https://api.alqari.sa/services/ai-validate?document_id=doc_9xKpL3mN&rules_text=1.%20Check%20required%20fields%0A2.%20Validate%20dates" \
  -H "Authorization: Bearer $ALQARI_API_KEY"
```

---

## Response

```json
{
  "document_id": "doc_9xKpL3mN",
  "overall_verdict": "FAIL",
  "summary": {
    "total_rules": 2,
    "passed": 1,
    "failed": 1,
    "warnings": 0,
    "not_applicable": 0
  },
  "results": [
    {
      "rule_number": 1,
      "rule_text": "Check required fields",
      "verdict": "PASS",
      "calculation": null,
      "detail": "All required fields present.",
      "evidence": "Invoice No: INV-0001",
      "bounding_boxes": [
        { "page": 1, "bbox": [[72,118],[268,118],[268,138],[72,138]] }
      ]
    },
    {
      "rule_number": 2,
      "rule_text": "Validate dates",
      "verdict": "FAIL",
      "calculation": null,
      "detail": "Issue date is after due date.",
      "evidence": null,
      "bounding_boxes": null
    }
  ],
  "credits_consumed": 1,
  "remaining_credits": 4976
}
```

---

## Verdicts

Per-rule `verdict` values are:

| Verdict | Meaning |
|---------|---------|
| `PASS` | The rule is satisfied |
| `FAIL` | The rule is not satisfied |
| `WARNING` | The rule is partially satisfied or uncertain |
| `N/A` | The rule does not apply to this document |

`overall_verdict` summarizes the run. `summary` is an object with counts: `total_rules`, `passed`, `failed`, `warnings`, and `not_applicable`.

---

## Bounding Boxes

`bounding_boxes` may be `null` or `[]`, so do not assume every rule has coordinates. Coordinate elements are 4-point polygons, like OCR regions.

---

## Notes

- Validation runs against a document that has already been processed by OCR.
- There is no generic field-extraction or custom-schema endpoint in the public API. AI-validate checks rules; it is not structured field extraction.
