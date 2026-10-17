#!/usr/bin/env node
import { readFileSync } from 'node:fs';

const args = process.argv.slice(2);
const json = args.includes('--json');
const files = args.filter(arg => !arg.startsWith('--'));
if (files.length !== 1 || args.some(arg => arg.startsWith('--') && arg !== '--json')) {
  console.error('usage: spec-lint.mjs <spec.md> [--json]');
  process.exit(2);
}
let source;
try { source = readFileSync(files[0], 'utf8'); }
catch (error) { console.error(`spec-lint: cannot read input: ${error.message}`); process.exit(2); }
const lines = source.replace(/\r\n/g, '\n').split('\n');
const problems = [];
const fail = (code, message, line) => problems.push({ code, message, ...(line ? { line } : {}) });
const version = lines[0].match(/^<!--\s*qore-spec\/(\d+)\s*-->\s*$/);
if (!version) fail('schema', 'The first line must declare <!-- qore-spec/1 -->.');
else if (version[1] !== '1') fail('schema', `Unsupported qore-spec/${version[1]}; expected qore-spec/1.`);

// Parse fences before looking for steps: keywords outside Gherkin prove nothing.
const blocks = [];
let open = null;
for (let index = 0; index < lines.length; index++) {
  const fence = lines[index].match(/^\s{0,3}(`{3,}|~{3,})\s*([^\s]*)\s*$/);
  if (!open && fence) {
    open = { marker: fence[1][0], width: fence[1].length, language: fence[2].toLowerCase(), line: index + 1, lines: [] };
  } else if (open && fence && fence[1][0] === open.marker && fence[1].length >= open.width && !fence[2]) {
    blocks.push(open); open = null;
  } else if (open) open.lines.push({ text: lines[index], line: index + 1 });
}
if (open) fail('fence', 'An opened code fence is not closed.', open.line);
const gherkin = blocks.filter(block => block.language === 'gherkin');
if (!gherkin.length) fail('gherkin', 'At least one fenced Gherkin scenario is required.');
const scenarios = [];
for (const block of gherkin) {
  let current = null;
  let docstring = null;
  let examples = null;
  const blockScenarios = scenarios.length;
  for (const row of block.lines) {
    // Docstring arguments are literal payload, including apparent steps/scenarios.
    if (docstring) {
      if (row.text.trim() === docstring.marker) docstring = null;
      continue;
    }
    const delimiter = row.text.match(/^\s*("""|```)([^"`]*)$/);
    if (delimiter) {
      docstring = { marker: delimiter[1], line: row.line };
      continue;
    }
    const scenario = row.text.match(/^\s*Scenario( Outline)?:\s*(.*)$/i);
    if (scenario) {
      const name = scenario[2].trim();
      const explicit = name.match(/^\[?([A-Za-z]+-?\d+)\]?(?=\s|:|$)/);
      current = { id: explicit ? explicit[1] : `Scenario ${scenarios.length + 1}`, name, line: row.line, steps: new Set(), outline: Boolean(scenario[1]), examples: [] };
      examples = null;
      scenarios.push(current);
    } else if (current) {
      if (/^\s*Examples:/i.test(row.text)) {
        examples = { line: row.line, rows: [] };
        current.examples.push(examples);
        continue;
      }
      if (examples) {
        if (/^\s*\|.*\|\s*$/.test(row.text)) examples.rows.push(row.text.trim());
        continue;
      }
      const step = row.text.match(/^\s*(Given|When|Then)\s+\S/i);
      if (step) current.steps.add(step[1].toLowerCase());
    }
  }
  if (docstring) fail('docstring', 'A Gherkin docstring is not closed with its opening delimiter.', docstring.line);
  if (scenarios.length === blockScenarios) fail('gherkin', 'An empty Gherkin fence is not acceptance criteria.', block.line);
}
const ids = new Set();
for (const scenario of scenarios) {
  if (!scenario.name) fail('scenario', 'A scenario must have a name.', scenario.line);
  if (ids.has(scenario.id)) fail('duplicate-id', `Duplicate scenario ID: ${scenario.id}.`, scenario.line);
  ids.add(scenario.id);
  for (const step of ['given', 'when', 'then']) if (!scenario.steps.has(step)) fail('step', `${scenario.id} lacks its own ${step} step.`, scenario.line);
  if (scenario.outline && !scenario.examples.length) fail('examples', `${scenario.id} requires populated Examples.`, scenario.line);
  for (const examples of scenario.examples) {
    if (examples.rows.length < 2 || !/[^|\s]/.test(examples.rows[0])) {
      fail('examples', `${scenario.id} Examples requires a header and at least one data row.`, examples.line);
    }
  }
}
if (!blocks.some(block => block.language === 'mermaid' && block.lines.some(row => /^\s*sequenceDiagram\s*$/.test(row.text)))) {
  fail('sequence', 'A fenced Mermaid sequenceDiagram is required.');
}

const coverageRows = lines.filter(line => /^\s*(?:[-*|#]\s*)*(?:\*\*)?Coverage(?:\*\*)?\s*[:|]/i.test(line));
if (!coverageRows.length) fail('coverage', 'A coverage line mapping each scenario to a story or decision is required.');
const coverage = coverageRows.join(' ').replace(/\*\*/g, '');
// Expand compact ranges such as A02-A04 without prescribing story/decision IDs.
const expanded = coverage.replace(/\b([A-Za-z]+-?)(\d+)\s*[-–]\s*(?:\1)?(\d+)\b/g, (all, prefix, begin, end) => {
  const first = Number(begin), last = Number(end);
  if (last < first || last - first > 1000) { fail('coverage-range', `Invalid coverage range: ${all}.`); return all; }
  return Array.from({ length: last - first + 1 }, (_, offset) => `${prefix}${String(first + offset).padStart(begin.length, '0')}`).join(' ');
});
const escape = value => value.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
for (const id of ids) {
  const mentions = expanded.split(';').filter(clause => new RegExp(`\\b${escape(id)}\\b`).test(clause));
  if (!mentions.length) fail('uncovered', `Scenario ${id} is missing from coverage.`);
  else if (!mentions.some(clause => /(?:→|->|=>|\|)\s*[^\s;.|]/.test(clause))) fail('coverage-target', `Scenario ${id} needs a coverage mapping target.`);
}
const prefixes = new Set([...ids].map(id => id.match(/^([A-Za-z]+-?)\d+$/)?.[1]).filter(Boolean));
for (const token of expanded.match(/\b[A-Za-z]+-?\d+\b|\bScenario\s+\d+\b/g) || []) {
  if ((token.startsWith('Scenario ') || prefixes.has(token.match(/^([A-Za-z]+-?)\d+$/)?.[1])) && !ids.has(token)) fail('orphan-coverage', `Coverage references unknown scenario ${token}.`);
}
const result = { valid: !problems.length, schema: 'qore-spec/1', scenarios: scenarios.map(({ id, name, line }) => ({ id, name, line })), problems };
if (json) console.log(JSON.stringify(result, null, 2));
else if (result.valid) console.log(`spec-lint: valid qore-spec/1 (${scenarios.length} scenarios).`);
else for (const problem of problems) console.error(`spec-lint: ${problem.message}${problem.line ? ` (line ${problem.line})` : ''}`);
process.exit(result.valid ? 0 : 1);
