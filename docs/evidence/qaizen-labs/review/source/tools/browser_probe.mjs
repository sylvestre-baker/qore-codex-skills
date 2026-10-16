#!/usr/bin/env node
/** Observe an authorized read-only web surface using an explicitly available Playwright driver. */
import fs from 'node:fs/promises';
import path from 'node:path';
import { createRequire } from 'node:module';

const usage = 'Usage: node tools/browser_probe.mjs --url URL --output NEW_DIR [--actions FILE] [--policy FILE] [--playwright-module PATH] [--label TEXT]';
const options = {};
for (let index = 2; index < process.argv.length; index += 2) {
  const flag = process.argv[index];
  if (flag === '--help') { console.log(usage); process.exit(0); }
  if (!['--url', '--output', '--actions', '--policy', '--playwright-module', '--label'].includes(flag) || !process.argv[index + 1]) {
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
const policy = options.policy ? JSON.parse(await fs.readFile(options.policy, 'utf8')) : { allowed_origins: [target.origin] };
if (!Array.isArray(policy.allowed_origins) || !policy.allowed_origins.includes(target.origin)
  || policy.allowed_origins.some(origin => new URL(origin).origin !== origin)) throw new Error('Policy needs exact allowed origins including the entry.');
const output = path.resolve(options.output);
await fs.mkdir(output, { recursive: false });
const events = { console: [], page_errors: [], network: [], requests_failed: [], blocked_mutations: [], blocked_navigation: [], route_errors: [], navigation: [], actions: [] };
const started = new Date().toISOString();
const result = {
  schema: 'qore-browser-probe/1', label: options.label || 'Authorized read-only browser observation',
  started_at: started, target: target.href, status: 'BLOCKED',
  scope: 'Navigation, screenshots, DOM, keyboard, console and network observation. No accessibility or performance certification.',
  driver: { name: 'Playwright Chromium', node: process.version },
  capabilities: Object.fromEntries(['navigation', 'screenshot', 'dom', 'keyboard', 'console', 'network'].map(name => [name, { status: 'NOT_TESTED' }])),
  snapshots: [], limits: ['An isolated browser context is used; no user browser session is accessed.', 'Non-GET/HEAD/OPTIONS requests are blocked. Structured events omit request headers and bodies; raw traces, DOM, video and screenshots may retain network/page data and require separate review before sharing.', 'HTTP document redirects are blocked before following, including same-origin redirects; that support is unqualified. Top-level documents use one guarded fetch without redirect following, then the actual response is fulfilled into the browser.', 'This is an execution record, not a product-quality or general-performance benchmark.'],
  policy: { allowed_origins: policy.allowed_origins, service_workers: 'block', allowed_methods: ['GET', 'HEAD', 'OPTIONS'] },
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
  context = await browser.newContext({ viewport: { width: 1280, height: 800 }, locale: 'en-US', serviceWorkers: 'block', recordVideo: { dir: path.join(output, 'video'), size: { width: 1280, height: 800 } } });
  await context.route('**/*', async route => {
    const request = route.request();
    try {
      let documentNavigation = request.isNavigationRequest();
      if (documentNavigation) {
        try { documentNavigation = !request.frame().parentFrame(); }
        catch { /* The first popup request may not have an associated Frame yet. Guard it conservatively. */ }
      }
      if (documentNavigation && !policy.allowed_origins.includes(new URL(request.url()).origin)) {
        events.blocked_navigation.push({ at: new Date().toISOString(), url: request.url(), reason: 'Main-frame or popup origin is outside policy' });
        return await route.abort('blockedbyclient');
      }
      if (!['GET', 'HEAD', 'OPTIONS'].includes(request.method())) {
        events.blocked_mutations.push({ at: new Date().toISOString(), method: request.method(), url: request.url(), reason: 'Read-only probe policy' });
        return await route.abort('blockedbyclient');
      }
      if (documentNavigation) {
        // Playwright does not route subsequent redirect hops. Refuse redirect responses
        // instead of discovering an unauthorized document only after it has loaded.
        const response = await route.fetch({ maxRedirects: 0, timeout: 30000 });
        const destination = response.headers().location;
        if (response.status() >= 300 && response.status() < 400 && destination) {
          events.blocked_navigation.push({ at: new Date().toISOString(), from: request.url(), url: new URL(destination, request.url()).href,
            status: response.status(), reason: 'HTTP document redirect refused before following; same-origin support is unqualified' });
          await response.dispose();
          return await route.abort('blockedbyclient');
        }
        return await route.fulfill({ response });
      }
      return await route.continue();
    } catch (error) {
      events.route_errors.push({ at: new Date().toISOString(), url: request.url(), reason: error.name });
      try { await route.abort('failed'); } catch { /* Retain the guard failure even if the request already ended. */ }
    }
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
      viewport: { width: innerWidth, height: innerHeight, device_pixel_ratio: devicePixelRatio },
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
  const waitForPredicate = async (check, description) => {
    const deadline = Date.now() + 15000;
    while (true) {
      if (await check()) return;
      if (Date.now() >= deadline) throw new Error(description + ' within 15000 ms');
      await page.waitForTimeout(50);
    }
  };
  for (const action of actions) {
    const at = new Date().toISOString();
    let actionOutcome = 'completed';
    const locator = () => action.role ? page.getByRole(action.role, { name: action.name, exact: action.exact !== false }) : page.locator(action.selector);
    if (action.type === 'click') await locator().click();
    else if (action.type === 'click-if-visible') {
      if (await locator().isVisible()) await locator().click();
      else actionOutcome = 'not_present';
    }
    else if (action.type === 'keyboard') await page.keyboard.press(action.key);
    else if (action.type === 'assert-text') await page.getByText(action.text, { exact: action.exact !== false }).waitFor({ state: 'visible' });
    else if (action.type === 'assert-url') await page.waitForURL(action.url, { waitUntil: 'domcontentloaded', timeout: 15000 });
    else if (action.type === 'reload') await page.reload({ waitUntil: 'domcontentloaded' });
    else if (action.type === 'history-back') await page.goBack({ waitUntil: 'domcontentloaded' });
    else if (action.type === 'history-forward') await page.goForward({ waitUntil: 'domcontentloaded' });
    else if (action.type === 'assert-visible' || action.type === 'assert-hidden') await locator().waitFor({ state: action.type === 'assert-visible' ? 'visible' : 'hidden' });
    else if (action.type === 'assert-focused') {
      await waitForPredicate(() => locator().evaluateAll(elements => {
        if (elements.length > 1) throw new Error('Expected one focus target');
        return elements.length === 1 && elements[0] === document.activeElement;
      }), `Expected focused control: ${action.selector || action.name}`);
    }
    else if (action.type === 'assert-attribute') {
      await waitForPredicate(() => locator().evaluateAll((elements, expected) => {
        if (elements.length > 1) throw new Error('Expected one attribute target');
        return elements.length === 1 && elements[0].getAttribute(expected.attribute) === expected.value;
      }, { attribute: action.attribute, value: action.value }), `Attribute mismatch: ${action.attribute}`);
    }
    else if (action.type === 'assert-none-checked') {
      if (await page.locator('input:checked,[aria-checked="true"],[aria-selected="true"]').count()) throw new Error('An answer or selection is checked.');
    }
    else if (action.type === 'traverse-focus') {
      const key = action.key || 'Tab';
      const maximum = action.max_steps ?? 24;
      if (!['Tab', 'Shift+Tab'].includes(key) || !Number.isInteger(maximum) || maximum < 1 || maximum > 50) throw new Error('Traversal requires Tab/Shift+Tab and 1..50 steps.');
      let reached = false;
      for (let step = 1; step <= maximum; step += 1) {
        await page.keyboard.press(key);
        const active = await page.evaluate(() => ({ tag: document.activeElement.tagName, id: document.activeElement.id, text: document.activeElement.textContent?.trim().slice(0, 200) }));
        reached = await locator().evaluate(element => element === document.activeElement);
        events.actions.push({ at: new Date().toISOString(), type: 'focus-step', key, step, active_element: active, reached, outcome: 'observed' });
        if (reached) break;
      }
      if (!reached) throw new Error(`Control was not reached by ${key} in ${maximum} steps: ${action.selector || action.name}`);
    }
    else if (action.type !== 'snapshot') throw new Error(`Unsupported action type: ${action.type}`);
    events.actions.push({ at, ...action, outcome: actionOutcome, url: page.url() });
    await page.waitForTimeout(900);
    if (events.route_errors.length || events.blocked_navigation.length || !policy.allowed_origins.includes(new URL(page.url()).origin)) throw new Error('Navigation guard blocked an attempt or encountered an error.');
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
  if (context) {
    try { await context.close(); }
    catch (error) { result.limits.push(`Context cleanup failed: ${error.name}`); result.status = 'PARTIAL'; process.exitCode = 1; }
  }
  if (video) {
    try { const videoPath = await video.path(); result.video = path.relative(output, videoPath); }
    catch (error) { result.limits.push(`Video could not be saved: ${error.message}`); }
  }
  if (browser) {
    try { await browser.close(); }
    catch (error) { result.limits.push(`Browser cleanup failed: ${error.name}`); result.status = 'PARTIAL'; process.exitCode = 1; }
  }
  result.finished_at = new Date().toISOString();
  result.counts = Object.fromEntries(Object.entries(events).map(([key, value]) => [key, value.length]));
  await write('events.json', events);
  await write('result.json', result);
  console.log(JSON.stringify({ status: result.status, target: result.target, output, capabilities: result.capabilities, error: result.error }, null, 2));
}
