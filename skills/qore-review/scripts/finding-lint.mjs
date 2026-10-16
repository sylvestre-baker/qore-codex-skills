#!/usr/bin/env node
import { readFileSync } from 'node:fs';

const args = process.argv.slice(2);
const paths = args.filter(arg => !arg.startsWith('--'));
const declarations = args.filter(arg => arg.startsWith('--verifier='));
const verifier = declarations[0]?.slice('--verifier='.length);
const json = args.includes('--json');
if (paths.length !== 1 || declarations.length !== 1 || !['ran', 'skipped'].includes(verifier) || args.some(arg => arg.startsWith('--') && arg !== '--json' && !arg.startsWith('--verifier='))) {
  console.error('usage: finding-lint.mjs <packet.json> --verifier=ran|skipped [--json]'); process.exit(2);
}
let packet;
try { packet = JSON.parse(readFileSync(paths[0], 'utf8')); }
catch (error) { console.error(`finding-lint: cannot read JSON: ${error.message}`); process.exit(2); }
const object = value => value !== null && typeof value === 'object' && !Array.isArray(value);
const text = value => typeof value === 'string' && value.trim().length > 0;
const problems = [];
const findings = object(packet) && Array.isArray(packet.findings) ? packet.findings : [];
if (!object(packet) || !Array.isArray(packet.findings)) problems.push({ code: 'envelope', why: 'Expected an object containing findings: []; arrays, null and missing findings are refused.' });
const verdicts = ['CONFIRMED', 'PLAUSIBLE', 'REFUTED'];
const severities = ['critical', 'high', 'medium', 'low', 'info'];
const ids = new Set();
const checkable = /[\w./-]+\.[A-Za-z]{1,8}\b|\b[0-9a-f]{7,40}\b|\b\d+(?:\.\d+)*\b/;
for (const [index, finding] of findings.entries()) {
  const id = object(finding) && text(finding.id) ? finding.id : `#${index + 1}`;
  const fail = (code, why) => problems.push({ id, code, why });
  if (!object(finding)) { fail('shape', 'Each finding must be an object.'); continue; }
  for (const key of ['id', 'title', 'severity']) if (!text(finding[key])) fail('field', `${key} must be a non-empty string.`);
  if (text(finding.id)) {
    if (ids.has(finding.id)) fail('duplicate-id', 'Finding IDs must be unique.');
    ids.add(finding.id);
  }
  if (!severities.includes(finding.severity)) fail('severity', `severity must be one of ${severities.join(', ')}.`);
  if (!verdicts.includes(finding.verdict)) fail('verdict', `verdict must be one of ${verdicts.join(', ')}.`);
  if (!text(finding.evidence) || !checkable.test(finding.evidence)) fail('evidence', 'Evidence must name a checkable source or measurement.');
  if (verifier === 'skipped' && finding.verdict !== 'PLAUSIBLE') fail('verification', 'Missing independent verification permits only PLAUSIBLE findings.');
  if (finding.verdict === 'REFUTED') {
    if (!text(finding.refuted_because)) fail('refutation', 'REFUTED requires a retained refuted_because reason.');
  } else {
    if (finding.verdict === 'CONFIRMED' && !text(finding.counterexample)) fail('counterexample', 'Every CONFIRMED finding requires a concrete counterexample.');
  }
}
const valid = !problems.length;
const blocking = valid && verifier === 'ran' ? findings.filter(finding => finding.verdict === 'CONFIRMED' && ['critical', 'high'].includes(finding.severity)).map(finding => finding.id) : [];
const coverage = valid && verifier === 'ran' ? 'COMPLETE' : 'PARTIAL';
const result = {
  valid, coverage, verdict: !valid ? 'INVALID' : blocking.length ? 'DO-NOT-SHIP' : verifier === 'skipped' ? 'PENDING' : 'SHIP',
  verifier, total: findings.length,
  counts: Object.fromEntries(verdicts.map(verdict => [verdict, findings.filter(finding => object(finding) && finding.verdict === verdict).length])),
  blocking_findings: blocking, findings, problems,
  limit: 'The verifier flag records an execution declaration; validate actual independent phase evidence separately.',
};
if (json) console.log(JSON.stringify(result, null, 2));
else {
  console.log(`finding-lint: ${valid ? 'valid' : 'refused'}; coverage ${coverage}; verdict ${result.verdict}; ${blocking.length} blocking findings.`);
  for (const problem of problems) console.error(`${problem.id || 'packet'}: ${problem.why}`);
}
process.exit(valid ? 0 : 1);
