/**
 * get-ocr-output.js — Retrieve OCR output for a document.
 *
 * Usage:
 *   node get-ocr-output.js <document_id> [format]
 *
 *   format: ocr (default) | text | layout
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
  console.error("Usage: node get-ocr-output.js <document_id> [format]");
  process.exit(1);
}

const format = process.argv[3] ?? "ocr";

console.log(`Fetching OCR output (${format}) for document: ${documentId}`);

const resp = await fetch(`${BASE_URL}/services/ocr-output/${documentId}/${format}`, {
  headers: { Authorization: `Bearer ${API_KEY}` },
});

if (!resp.ok) {
  const err = await resp.json().catch(() => ({}));
  console.error(`Error ${resp.status}:`, JSON.stringify(err, null, 2));
  process.exit(1);
}

// /text returns plain text; /ocr and /layout return JSON.
if (format === "text") {
  console.log(await resp.text());
} else {
  console.log(JSON.stringify(await resp.json(), null, 2));
}
