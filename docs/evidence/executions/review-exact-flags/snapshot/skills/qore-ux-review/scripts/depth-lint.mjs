#!/usr/bin/env node
import { readFileSync } from 'node:fs';

if (process.argv.length !== 3) { console.error('usage: depth-lint.mjs <depth.json>'); process.exit(2); }
let packet;
try { packet = JSON.parse(readFileSync(process.argv[2], 'utf8')); }
catch (error) { console.error(`depth-lint: cannot read JSON: ${error.message}`); process.exit(2); }
if (packet === null || typeof packet !== 'object' || Array.isArray(packet)) { console.error('depth-lint: input must be an object.'); process.exit(2); }
const depths = ['full', 'entry', 'state', 'visual', 'copy', 'perf', 'none'];
const problems = [];
if (!depths.includes(packet.depth)) problems.push('Unknown depth.');
const files = packet.changed_files;
if (!Array.isArray(files) || !files.length || files.some(file => typeof file !== 'string' || !file.trim())) problems.push('changed_files must contain non-empty file paths.');
if (packet.depth === 'none' && (typeof packet.justification !== 'string' || !packet.justification.trim())) problems.push('none depth requires a non-applicability justification.');
const normalized = Array.isArray(files) ? files.filter(file => typeof file === 'string').map(file => `/${file.replaceAll('\\', '/')}`) : [];
const matches = (file, patterns) => patterns.some(pattern => pattern.test(file));
const families = {
  copy: [/\/(?:i18n|locales?|lang)\//i, /\.po$/i, /messages?\./i, /translations?/i],
  data: [/service|serializer|repositor|controller|reducer|quer(?:y|ies)|prisma|schema/i, /\/(?:api|hooks?|stores?|data)\//i, /\.sql$/i],
  render: [/\.(?:tsx|jsx|vue|svelte|css|scss|less)$/i, /\/(?:components?|pages?)\//i],
  route: [/rout(?:e|er|es)/i, /\/pages?\/.*\.(?:tsx|jsx|vue|svelte)$/i, /\/app\/(?:.*\/)?(?:page|layout)\.[jt]sx?$/i],
};
const hits = family => normalized.filter(file => matches(file, families[family]));
if (packet.depth === 'copy' && normalized.some(file => !matches(file, families.copy))) problems.push('copy depth contradicted by non-copy files.');
if (packet.depth === 'visual' && hits('data').length) problems.push('visual depth contradicted by data source files.');
if (['copy', 'visual', 'state', 'perf', 'none'].includes(packet.depth) && hits('route').length) problems.push('G0 reachability is mandatory for a route/page change; use entry or full.');
if (packet.depth === 'none' && hits('render').length) problems.push('none depth contradicted by rendering files.');
console.log(JSON.stringify({ valid: !problems.length, depth: packet.depth, changed_files: files, problems }, null, 2));
process.exit(problems.length ? 1 : 0);
