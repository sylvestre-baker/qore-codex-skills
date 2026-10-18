#!/usr/bin/env node
import { readFileSync } from 'node:fs';

const args = process.argv.slice(2);
const paths = args.filter(arg => !arg.startsWith('--'));
if (paths.length !== 1 || args.some(arg => arg.startsWith('--') && arg !== '--json')) {
  console.error('usage: redact-for-verifier.mjs <packet.json> [--json]'); process.exit(2);
}
let packet;
try { packet = JSON.parse(readFileSync(paths[0], 'utf8')); }
catch (error) { console.error(`redact-for-verifier: cannot read JSON: ${error.message}`); process.exit(2); }
const object = value => value !== null && typeof value === 'object' && !Array.isArray(value);
const keep = ['id', 'title', 'severity', 'evidence', 'counterexample'];
if (!object(packet) || !Array.isArray(packet.findings) || packet.findings.some(finding => !object(finding))) {
  console.error('redact-for-verifier: expected an object containing findings: [objects].'); process.exit(2);
}
// Only scalar claim fields cross this boundary; nested objects could conceal rationale.
if (packet.findings.some(finding => keep.some(key => key in finding && typeof finding[key] !== 'string'))) {
  console.error('redact-for-verifier: allowlisted fields must be strings.'); process.exit(2);
}
const ids = packet.findings.map(finding => finding.id);
if (ids.some(id => typeof id !== 'string' || !id.trim()) || new Set(ids).size !== ids.length) {
  console.error('redact-for-verifier: every claim requires a unique non-empty ID.'); process.exit(2);
}
if (packet.findings.some(finding => ['title', 'severity', 'evidence'].some(key => typeof finding[key] !== 'string' || !finding[key].trim()) || !['critical', 'high', 'medium', 'low', 'info'].includes(finding.severity))) {
  console.error('redact-for-verifier: claims require non-empty title, known severity and evidence.'); process.exit(2);
}
const dropped = new Set();
const findings = packet.findings.map(finding => {
  for (const key of Object.keys(finding)) if (!keep.includes(key)) dropped.add(key);
  return Object.fromEntries(keep.filter(key => key in finding).map(key => [key, finding[key]]));
});
console.error(`redact-for-verifier: ${findings.length} claims; withheld fields: ${[...dropped].sort().join(', ') || 'none'}.`);
console.log(JSON.stringify({ findings }, null, 2));
