/**
 * validate-document.js — Run rule-based AI validation on a processed document.
 *
 * Usage:
 *   node validate-document.js <document_id> ["<newline-numbered rules>"]
 *
 * Environment variables:
 *   ALQARI_API_KEY   Required.
 *   ALQARI_BASE_URL  Optional. Defaults to https://api.alqari.sa
 */

const BASE_URL = (process.env.ALQARI_BASE_URL ?? "https://api.alqari.sa").replace(/\/$/, "");
const API_KEY  = process.env.ALQARI_API_KEY;

if (!API_KEY) {
  console.error("Error: ALQARI_API_KEY environment variable is not set.");
  process.exit(1);
}

const documentId = process.argv[2];
if (!documentId) {
  console.error("Usage: node validate-document.js <document_id> [rules_text]");
  process.exit(1);
}

// Newline-numbered rules. Edit to match your validation requirements.
const DEFAULT_RULES_TEXT = [
  "1. All required fields are present.",
  "2. The total matches the sum of line items.",
  "3. The issue date is not after the due date.",
].join("\n");

const rulesText = process.argv[3] ?? DEFAULT_RULES_TEXT;

console.log(`Running validation on document: ${documentId}`);

// ai-validate takes document_id and rules_text as query parameters.
const params = new URLSearchParams({ document_id: documentId, rules_text: rulesText });

const resp = await fetch(`${BASE_URL}/services/ai-validate?${params}`, {
  method: "POST",
  headers: { Authorization: `Bearer ${API_KEY}` },
});

if (!resp.ok) {
  const err = await resp.json().catch(() => ({}));
  console.error(`Error ${resp.status}:`, JSON.stringify(err, null, 2));
  process.exit(1);
}

const data = await resp.json();
console.log(JSON.stringify(data, null, 2));
console.log(`\nOverall verdict: ${data.overall_verdict}`);
