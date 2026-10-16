#!/usr/bin/env node
import { readFileSync } from 'node:fs';

const die = message => { console.error(`stop-rule: ${message}`); process.exit(2); };
const object = value => value !== null && typeof value === 'object' && !Array.isArray(value);
const text = value => typeof value === 'string' && value.trim().length > 0;
let run;
try { run = JSON.parse(readFileSync(process.argv[2] || 0, 'utf8')); }
catch (error) { die(`Cannot read JSON: ${error.message}`); }
if (!object(run)) die('Input must be an object.');
if (!Array.isArray(run.in_scope) || !run.in_scope.length || run.in_scope.some(gate => !text(gate)) || new Set(run.in_scope).size !== run.in_scope.length) die('in_scope must contain unique non-empty gate names.');
if (!Array.isArray(run.iterations) || !run.iterations.length) die('iterations must be non-empty.');
const scope = run.in_scope;
const gateList = (value, label) => {
  if (!Array.isArray(value) || value.some(gate => !scope.includes(gate)) || new Set(value).size !== value.length) die(`${label} must contain unique in-scope gates.`);
};
const reasons = (value, label) => {
  if (!object(value) || Object.entries(value).some(([gate, reason]) => !scope.includes(gate) || !text(reason))) die(`${label} must map in-scope gates to non-empty reasons.`);
};
if (run.not_applicable !== undefined) reasons(run.not_applicable, 'not_applicable');
let previousN = 0;
const measuredAt = {}, measuredScores = {};
let lastFix = 0;
const states = [];
for (const [index, iteration] of run.iterations.entries()) {
  if (!object(iteration) || !Number.isInteger(iteration.n) || iteration.n <= previousN) die(`Iteration ${index + 1} needs a strictly increasing positive integer n.`);
  previousN = iteration.n;
  if (!object(iteration.scores)) die(`Iteration ${iteration.n} needs a scores object.`);
  const blockedInput = iteration.infra_blocked === undefined ? [] : iteration.infra_blocked;
  const skippedInput = iteration.skipped === undefined ? {} : iteration.skipped;
  const naInput = iteration.not_applicable === undefined ? {} : iteration.not_applicable;
  gateList(iteration.measured, `Iteration ${iteration.n} measured`);
  gateList(blockedInput, `Iteration ${iteration.n} infra_blocked`);
  reasons(skippedInput, `Iteration ${iteration.n} skipped`);
  reasons(naInput, `Iteration ${iteration.n} not_applicable`);
  if (iteration.fix_applied !== undefined && typeof iteration.fix_applied !== 'boolean') die('fix_applied must be boolean.');
  if (iteration.g6_passed !== undefined && typeof iteration.g6_passed !== 'boolean') die('g6_passed must be boolean.');
  const na = { ...(run.not_applicable || {}), ...naInput };
  for (const [gate, reason] of Object.entries(na)) {
    if (/\b(unavailable|no tools?|missing tools?|not installed|infra(?:structure)? blocked|timeout)\b/i.test(reason)) die(`Non-applicability for ${gate} cannot be justified by tool absence.`);
    if (Object.hasOwn(skippedInput, gate) || blockedInput.includes(gate)) die(`${gate} cannot be both not applicable and skipped/blocked.`);
  }
  for (const [gate, score] of Object.entries(iteration.scores)) {
    if (!scope.includes(gate) || !Number.isInteger(score) || score < 0 || score > 5) die(`Iteration ${iteration.n}: scores must be integers 0..5 for in-scope gates.`);
    if (!iteration.measured.includes(gate) && measuredScores[gate] !== undefined && score !== measuredScores[gate]) die(`Iteration ${iteration.n}: score for ${gate} changed without measurement.`);
  }
  for (const gate of iteration.measured) {
    if (Object.hasOwn(skippedInput, gate) || blockedInput.includes(gate) || Object.hasOwn(na, gate)) die(`Iteration ${iteration.n}: ${gate} cannot be measured and omitted.`);
    if (gate === 'G6' && iteration.g6_passed !== undefined) measuredScores[gate] = iteration.g6_passed ? 5 : 0;
    else if (!Object.hasOwn(iteration.scores, gate)) die(`Iteration ${iteration.n}: measured ${gate} needs a score.`);
    else measuredScores[gate] = iteration.scores[gate];
    measuredAt[gate] = iteration.n;
  }
  // A fix lands after this iteration's observations, invalidating them all.
  if (iteration.fix_applied) lastFix = iteration.n;
  const required = scope.filter(gate => !Object.hasOwn(na, gate));
  const skipped = required.filter(gate => Object.hasOwn(skippedInput, gate));
  const blocked = required.filter(gate => blockedInput.includes(gate));
  const missing = required.filter(gate => measuredAt[gate] === undefined || measuredScores[gate] === undefined);
  const stale = required.filter(gate => measuredAt[gate] !== undefined && measuredAt[gate] <= lastFix);
  const failing = required.filter(gate => measuredScores[gate] !== undefined && measuredScores[gate] < 4);
  const covered = !skipped.length && !blocked.length && !missing.length && !stale.length;
  states.push({ iteration, required, skipped, blocked, missing, stale, failing, na, scores: { ...measuredScores }, covered });
}
const last = states.at(-1);
let stuck = 0, plateau = 0;
for (let index = 1; index < states.length; index++) {
  const now = states[index], before = states[index - 1];
  const shared = now.required.filter(gate => before.scores[gate] !== undefined && now.scores[gate] !== undefined);
  const improved = shared.some(gate => now.scores[gate] > before.scores[gate]) && !shared.some(gate => now.scores[gate] < before.scores[gate]);
  plateau = improved ? 0 : plateau + 1;
  const unchangedFailures = now.failing.length && now.failing.length === before.failing.length && now.failing.every(gate => before.failing.includes(gate) && now.scores[gate] <= before.scores[gate]);
  stuck = unchangedFailures ? stuck + 1 : 0;
}
const zeroed = last.required.filter(gate => last.scores[gate] === 0);
const coverage = last.covered ? 'COMPLETE' : last.required.length && last.blocked.length === last.required.length ? 'BLOCKED' : 'PARTIAL';
let decision = 'CONTINUE', verdict = last.failing.length ? 'DO-NOT-SHIP' : 'PENDING';
if (last.iteration.n > 6) { decision = 'STOP_CEILING'; verdict = zeroed.length || last.failing.length ? 'DO-NOT-SHIP' : 'BEST-EFFORT'; }
else if (last.covered && last.required.length && !last.failing.length && last.iteration.g6_passed !== false) { decision = 'SHIP'; verdict = 'SHIP'; }
else if (!last.required.length) { decision = 'NOT_APPLICABLE'; verdict = 'NOT-APPLICABLE'; }
else if (last.iteration.n >= 6) { decision = 'STOP_CEILING'; verdict = zeroed.length || last.failing.length ? 'DO-NOT-SHIP' : 'BEST-EFFORT'; }
else if (coverage === 'BLOCKED') decision = 'BLOCKED';
else if (zeroed.length) { decision = 'FIX'; verdict = 'DO-NOT-SHIP'; }
else if (stuck >= 2) decision = 'CHANGE_APPROACH';
else if (plateau >= 3) { decision = 'STOP_PLATEAU'; verdict = 'BEST-EFFORT'; }
console.log(JSON.stringify({
  decision, verdict, coverage, iteration: last.iteration.n, ceiling: 6,
  surface_score: zeroed.length ? 0 : null,
  consecutive_fresh_passes: last.covered && !last.failing.length && last.required.length ? 1 : 0,
  passes_required: 1, lowest_failing_gate: [...last.failing].sort((left, right) => last.scores[left] - last.scores[right])[0] || null,
  failing_gates: last.failing, stale_gates: last.stale, missing_gates: last.missing,
  skipped: last.skipped, infra_blocked: last.blocked, not_applicable: last.na,
  stuck_count: stuck, no_improve_count: plateau,
  limit: 'Coverage describes observations. SHIP is a scoped review result, not deployment authorization. Non-applicability reasons require independent review.',
}, null, 2));
