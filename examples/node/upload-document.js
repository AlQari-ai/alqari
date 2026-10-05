/**
 * upload-document.js — Upload a document to ALQari and run OCR in one step.
 *
 * Usage:
 *   node upload-document.js /path/to/document.pdf
 *
 * Environment variables:
 *   ALQARI_API_KEY   Required.
 *   ALQARI_BASE_URL  Optional. Defaults to https://api.alqari.sa
 *   ALQARI_LANGUAGE  Optional. Defaults to "auto" (auto | ar | en)
 *   ALQARI_MODE      Optional. Processing tier (fast | premium)
 */

import fs from "fs";
import path from "path";
import FormData from "form-data";

const BASE_URL  = (process.env.ALQARI_BASE_URL  ?? "https://api.alqari.sa").replace(/\/$/, "");
const LANGUAGE  = process.env.ALQARI_LANGUAGE   ?? "auto";
const MODE      = process.env.ALQARI_MODE;
const API_KEY   = process.env.ALQARI_API_KEY;

if (!API_KEY) {
  console.error("Error: ALQARI_API_KEY environment variable is not set.");
  process.exit(1);
}

const filePath = process.argv[2];
if (!filePath) {
  console.error("Usage: node upload-document.js <file_path>");
  process.exit(1);
}

if (!fs.existsSync(filePath)) {
  console.error(`Error: File not found: ${filePath}`);
  process.exit(1);
}

const form = new FormData();
form.append("file", fs.createReadStream(filePath), path.basename(filePath));

const params = new URLSearchParams({ language: LANGUAGE });
if (MODE) params.set("mode", MODE);

console.log(`Uploading: ${filePath}`);

const resp = await fetch(`${BASE_URL}/services/upload-ocr?${params}`, {
  method: "POST",
  headers: {
    Authorization: `Bearer ${API_KEY}`,
    ...form.getHeaders(),
  },
  body: form,
});

if (!resp.ok) {
  const err = await resp.json().catch(() => ({}));
  console.error(`Error ${resp.status}:`, JSON.stringify(err, null, 2));
  process.exit(1);
}

const data = await resp.json();
console.log(JSON.stringify(data, null, 2));
console.log(`\nDocument ID: ${data.document_id}`);
