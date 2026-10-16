#!/usr/bin/env node
/** Observe an authorized read-only web surface using an explicitly available Playwright driver. */
import fs from 'node:fs/promises';
import path from 'node:path';
import { createRequire } from 'node:module';

const usage = 'Usage: node tools/browser_probe.mjs --url URL --output NEW_DIR [--actions FILE] [--playwright-module PATH] [--label TEXT]';
const options = {};
for (let index = 2; index < process.argv.length; index += 2) {
  const flag = process.argv[index];
  if (flag === '--help') { console.log(usage); process.exit(0); }
  if (!['--url', '--output', '--actions', '--playwright-module', '--label'].includes(flag) || !process.argv[index + 1]) {
    console.error(usage); process.exit(2);
  }
  options[flag.slice(2)] = process.argv[index + 1];
}
if (!options.url || !options.output) { console.error(usage); process.exit(2); }
const target = new URL(options.url);
if (!['http:', 'https:'].includes(target.protocol) || target.username || target.password) {
  throw new Error('The target must be an HTTP(S) URL without embedded credentials.');
}
const actions = options.actions ? JSON.parse(await fs.readFile(options.actions, 'utf8')) : [];
if (!Array.isArray(actions) || actions.length > 40) throw new Error('Actions must be an array of at most 40 steps.');
const output = path.resolve(options.output);
await fs.mkdir(output, { recursive: false });
const events = { console: [], page_errors: [], network: [], requests_failed: [], blocked_mutations: [], navigation: [], actions: [] };
const started = new Date().toISOString();
const result = {
  schema: 'qore-browser-probe/1', label: options.label || 'Authorized read-only browser observation',
  started_at: started, target: target.href, status: 'BLOCKED',
  scope: 'Navigation, screenshots, DOM, keyboard, console and network observation. No accessibility or performance certification.',
  driver: { name: 'Playwright Chromium', node: process.version },
  capabilities: Object.fromEntries(['navigation', 'screenshot', 'dom', 'keyboard', 'console', 'network'].map(name => [name, { status: 'NOT_TESTED' }])),
  snapshots: [], limits: ['An isolated browser context is used; no user browser session is accessed.', 'Non-GET/HEAD/OPTIONS requests are blocked. No request headers or bodies are retained.', 'This is an execution record, not a product-quality or general-performance benchmark.'],
};
const write = async (name, value) => fs.writeFile(path.join(output, name), JSON.stringify(value, null, 2) + '\n');
let browser;
let context;
let page;
let video;
let traceStarted = false;
try {
  const require = createRequire(import.meta.url);
  let playwright;
  try { playwright = require(options['playwright-module'] || 'playwright'); }
  catch { throw new Error('Playwright is unavailable. Supply a locally installed optional driver with --playwright-module PATH; no installation was attempted.'); }
  try { result.driver.version = require(path.join(options['playwright-module'] || 'playwright', 'package.json')).version; } catch { /* Driver version can remain unknown. */ }
  browser = await playwright.chromium.launch({ headless: true });
  result.driver.browser_version = browser.version();
  context = await browser.newContext({ viewport: { width: 1280, height: 800 }, locale: 'en-US', recordVideo: { dir: path.join(output, 'video'), size: { width: 1280, height: 800 } } });
  await context.route('**/*', async route => {
    const request = route.request();
    if (!['GET', 'HEAD', 'OPTIONS'].includes(request.method())) {
      events.blocked_mutations.push({ at: new Date().toISOString(), method: request.method(), url: request.url(), reason: 'Read-only probe policy' });
      return route.abort('blockedbyclient');
    }
    return route.continue();
  });
  await context.tracing.start({ screenshots: true, snapshots: true, sources: false });
  traceStarted = true;
  page = await context.newPage();
  video = page.video();
  page.setDefaultTimeout(15000);
  page.on('console', message => events.console.push({ at: new Date().toISOString(), type: message.type(), text: message.text(), location: message.location() }));
  page.on('pageerror', error => events.page_errors.push({ at: new Date().toISOString(), message: error.message }));
  page.on('response', response => events.network.push({ at: new Date().toISOString(), url: response.url(), method: response.request().method(), status: response.status(), resource_type: response.request().resourceType() }));
  page.on('requestfailed', request => events.requests_failed.push({ at: new Date().toISOString(), url: request.url(), method: request.method(), error: request.failure()?.errorText }));
  page.on('framenavigated', frame => { if (frame === page.mainFrame()) events.navigation.push({ at: new Date().toISOString(), url: frame.url() }); });
  const snapshot = async label => {
    const stem = `${String(result.snapshots.length).padStart(2, '0')}-${label.replace(/[^a-z0-9-]/gi, '-').slice(0, 64)}`;
    const dom = await page.evaluate(() => ({
      url: location.href, title: document.title, language: document.documentElement.lang,
      headings: [...document.querySelectorAll('h1,h2,h3')].map(element => ({ tag: element.tagName, text: element.innerText })),
      links: [...document.querySelectorAll('a[href]')].map(element => ({ text: element.innerText, href: element.href })).filter(item => item.text.trim()),
      buttons: [...document.querySelectorAll('button')].map(element => ({ text: element.innerText, type: element.type, disabled: element.disabled })),
      active_element: document.activeElement ? { tag: document.activeElement.tagName, text: document.activeElement.textContent?.trim().slice(0, 200), id: document.activeElement.id } : null,
      text: document.body.innerText,
    }));
    await write(`${stem}.dom.json`, dom);
    result.capabilities.dom = { status: 'OBSERVED', evidence: `${stem}.dom.json` };
    await page.screenshot({ path: path.join(output, `${stem}.png`), fullPage: true });
    result.capabilities.screenshot = { status: 'OBSERVED', evidence: `${stem}.png` };
    result.snapshots.push({ at: new Date().toISOString(), label, url: page.url(), dom: `${stem}.dom.json`, screenshot: `${stem}.png` });
    return dom;
  };
  const response = await page.goto(target.href, { waitUntil: 'domcontentloaded', timeout: 30000 });
  if (response && response.status() >= 400) throw new Error(`Entry returned HTTP ${response.status()}.`);
  await page.waitForTimeout(1500);
  result.capabilities.navigation = { status: 'OBSERVED', evidence: 'events.json#/navigation', entry_status: response?.status() ?? null };
  result.capabilities.console = { status: 'OBSERVED', evidence: 'events.json#/console', note: 'Listener attached before entry navigation; an empty list means no emitted events were observed.' };
  result.capabilities.network = { status: 'OBSERVED', evidence: 'events.json#/network' };
  await snapshot('entry');
  await page.keyboard.press('Tab');
  const focused = await page.evaluate(() => ({ tag: document.activeElement.tagName, id: document.activeElement.id, text: document.activeElement.textContent?.trim().slice(0, 200) }));
  result.capabilities.keyboard = { status: 'OBSERVED', key: 'Tab', active_element: focused, evidence: 'events.json#/actions/0' };
  events.actions.push({ at: new Date().toISOString(), type: 'keyboard', key: 'Tab', active_element: focused, outcome: 'completed' });
  for (const action of actions) {
    const at = new Date().toISOString();
    const locator = () => action.role ? page.getByRole(action.role, { name: action.name, exact: action.exact !== false }) : page.locator(action.selector);
    if (action.type === 'click') await locator().click();
    else if (action.type === 'keyboard') await page.keyboard.press(action.key);
    else if (action.type === 'assert-text') await page.getByText(action.text, { exact: action.exact !== false }).waitFor({ state: 'visible' });
    else if (action.type === 'assert-url') { if (page.url() !== action.url) throw new Error(`Expected URL ${action.url}; observed ${page.url()}.`); }
    else if (action.type !== 'snapshot') throw new Error(`Unsupported action type: ${action.type}`);
    events.actions.push({ at, ...action, outcome: 'completed', url: page.url() });
    await page.waitForTimeout(900);
    if (action.type === 'snapshot') await snapshot(action.label || 'state');
  }
  await snapshot('final');
  result.status = 'COMPLETE';
} catch (error) {
  result.error = error.message;
  result.status = result.snapshots.length ? 'PARTIAL' : 'BLOCKED';
  process.exitCode = 1;
} finally {
  if (traceStarted) {
    try { await context.tracing.stop({ path: path.join(output, 'trace.zip') }); result.trace = 'trace.zip'; }
    catch (error) { result.limits.push(`Trace could not be saved: ${error.message}`); }
  }
  if (context) await context.close();
  if (video) {
    try { const videoPath = await video.path(); result.video = path.relative(output, videoPath); }
    catch (error) { result.limits.push(`Video could not be saved: ${error.message}`); }
  }
  if (browser) await browser.close();
  result.finished_at = new Date().toISOString();
  result.counts = Object.fromEntries(Object.entries(events).map(([key, value]) => [key, value.length]));
  await write('events.json', events);
  await write('result.json', result);
  console.log(JSON.stringify({ status: result.status, target: result.target, output, capabilities: result.capabilities, error: result.error }, null, 2));
}
