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
const plainObject = value => value !== null && typeof value === 'object' && !Array.isArray(value);
const exactKeys = (value, allowed, required = []) => plainObject(value)
  && Object.keys(value).every(key => allowed.includes(key)) && required.every(key => Object.hasOwn(value, key));
const boundedText = value => typeof value === 'string' && value.trim() === value && value.length > 0 && value.length <= 1000;
const validAttributes = value => plainObject(value) && Object.keys(value).length > 0 && Object.keys(value).length <= 20
  && Object.entries(value).every(([key, expected]) => /^[a-zA-Z_:][a-zA-Z0-9_.:-]*$/.test(key)
    && (expected === null || typeof expected === 'string' && expected.length <= 1000));
if (Object.hasOwn(policy, 'activation_guard')) {
  const guard = policy.activation_guard;
  if (!Array.isArray(guard) || guard.length < 1 || guard.length > 30 || guard.some(control =>
    !exactKeys(control, ['id', 'selector', 'role', 'name', 'state', 'attributes'], ['id', 'selector', 'role', 'name', 'state'])
    || !boundedText(control.id) || !/^[a-z][a-z0-9-]{0,63}$/.test(control.id)
    || !boundedText(control.selector) || !['button', 'link'].includes(control.role) || !boundedText(control.name)
    || Object.hasOwn(control, 'attributes') && !validAttributes(control.attributes)
    || !Array.isArray(control.state) || control.state.length < 1 || control.state.length > 16
    || control.state.some(check => !exactKeys(check, ['selector', 'visible', 'attributes'], ['selector'])
      || !boundedText(check.selector) || !Object.hasOwn(check, 'visible') && !Object.hasOwn(check, 'attributes')
      || Object.hasOwn(check, 'visible') && typeof check.visible !== 'boolean'
      || Object.hasOwn(check, 'attributes') && !validAttributes(check.attributes)))
    || new Set(guard.map(control => control.id)).size !== guard.length) {
    throw new Error('activation_guard must be a nonempty list of unique id/selector/role/name/state descriptors with only supported fields.');
  }
}
const output = path.resolve(options.output);
await fs.mkdir(output, { recursive: false });
const events = { console: [], page_errors: [], network: [], requests_failed: [], blocked_mutations: [], blocked_navigation: [], route_errors: [], navigation: [], actions: [], activation_checks: [], blocked_activations: [] };
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
if (policy.activation_guard) {
  result.policy.activation_guard = policy.activation_guard;
  result.limits.push('The optional activation guard checks actual native controls, labels and declared state before activation. It is a cooperative observation boundary, not isolation from arbitrary page scripts or full accessible-name certification. Guarded keys are Tab/Shift+Tab and unmodified Enter/Space only.');
}
const write = async (name, value) => fs.writeFile(path.join(output, name), JSON.stringify(value, null, 2) + '\n');
// This function is serialized into the isolated page before application scripts run.
const installActivationGuard = ({ controls, origins }) => {
  const records = [];
  const interactive = 'button,a[href],summary,input,select,textarea,label,[role="button"],[role="link"],[role="radio"],[role="checkbox"],[role="switch"],[role="option"],[role="tab"],[role="menuitem"],[role="menuitemradio"],[role="menuitemcheckbox"],[role="combobox"],[role="slider"],[role="spinbutton"],[tabindex]:not([tabindex="-1"]),[contenteditable]:not([contenteditable="false"])';
  const normalize = value => String(value ?? '').replace(/\s+/g, ' ').trim();
  const visible = element => element.getClientRects().length > 0
    && !['hidden', 'collapse'].includes(getComputedStyle(element).visibility) && !element.closest('[hidden]');
  const observed = element => {
    if (!(element instanceof Element)) return null;
    const text = normalize(element.innerText ?? element.textContent);
    const labelledBy = element.getAttribute('aria-labelledby');
    const name = labelledBy ? normalize(labelledBy.split(/\s+/).map(id => document.getElementById(id)?.textContent ?? '').join(' '))
      : normalize(element.getAttribute('aria-label') || text || element.getAttribute('title'));
    const role = element.tagName === 'BUTTON' || element.tagName === 'SUMMARY' ? 'button'
      : element.tagName === 'A' && element.hasAttribute('href') ? 'link' : null;
    return { tag: element.tagName.toLowerCase(), id: element.id || null, role, declared_role: element.getAttribute('role'), name, text,
      type: element.getAttribute('type'), href: element.getAttribute('href'), visible: visible(element),
      disabled: element.matches(':disabled') || element.getAttribute('aria-disabled')?.trim().toLowerCase() === 'true' || Boolean(element.closest('[inert]')) };
  };
  const attributes = (element, expected) => Object.fromEntries(Object.keys(expected || {}).map(key => [key, element.getAttribute(key)]));
  const matchesAttributes = (actual, expected) => Object.entries(expected || {}).every(([key, value]) => actual?.[key] === value);
  const inspect = (element, trigger, source, refusal = null) => {
    const target = observed(element);
    const entry = { at: new Date().toISOString(), source, trigger, url: location.href, target, allowed: false, control: null, states: [] };
    let reason = refusal;
    if (!reason && !target) reason = 'No actual element was resolved or focused.';
    if (!reason && (!target.role || !target.visible || target.disabled)) reason = 'The actual target is not a visible enabled native button, link or summary.';
    if (!reason && target.declared_role && target.declared_role !== target.role) reason = 'The declared role conflicts with the native control.';
    if (!reason && element.closest('form,label,[contenteditable]:not([contenteditable="false"])')) reason = 'Form, label and editable activations are outside the approved scope.';
    if (!reason && element.tagName === 'BUTTON' && (element.form || ['submit', 'reset'].includes((element.getAttribute('type') || '').toLowerCase()))) reason = 'Submission and reset controls are forbidden.';
    if (!reason && element.tagName === 'A' && (element.hasAttribute('download') || element.target && element.target !== '_self'
      || !['http:', 'https:'].includes(new URL(element.href, location.href).protocol) || !origins.includes(new URL(element.href, location.href).origin))) reason = 'The link destination or activation mode is outside policy.';
    if (!reason && element.tagName === 'SUMMARY' && (element.parentElement?.tagName !== 'DETAILS'
      || element.parentElement.querySelector('summary') !== element)) reason = 'Only the first native summary of its details is permitted.';
    if (!reason && (element.querySelector(interactive) || element.parentElement?.closest(interactive))) reason = 'Nested or enclosing interactive controls are forbidden.';
    const candidates = [];
    if (!reason) {
      for (const descriptor of controls) {
        let elements;
        try { elements = document.querySelectorAll(descriptor.selector); }
        catch { reason = `Invalid control selector: ${descriptor.id}`; break; }
        if (elements.length !== 1 || elements[0] !== element) continue;
        const check = { control: descriptor.id, attributes: attributes(element, descriptor.attributes), predicates: [] };
        let valid = descriptor.role === target.role && descriptor.name === target.name
          && (!target.text || descriptor.name === target.text) && matchesAttributes(check.attributes, descriptor.attributes);
        for (const predicate of descriptor.state) {
          let states;
          try { states = document.querySelectorAll(predicate.selector); }
          catch { states = []; }
          const actual = states.length === 1 ? { visible: visible(states[0]), attributes: attributes(states[0], predicate.attributes) } : null;
          const passed = actual !== null && (!Object.hasOwn(predicate, 'visible') || actual.visible === predicate.visible)
            && matchesAttributes(actual?.attributes, predicate.attributes);
          check.predicates.push({ selector: predicate.selector, matches: states.length, expected: predicate, actual, passed });
          valid = valid && passed;
        }
        check.passed = valid;
        entry.states.push(check);
        if (valid) candidates.push(descriptor.id);
      }
      if (!reason && candidates.length !== 1) reason = candidates.length ? 'Multiple descriptors approve this target; policy is ambiguous.'
        : 'No unique descriptor approves the actual target, label, attributes and current state.';
    }
    entry.allowed = !reason;
    entry.control = entry.allowed ? candidates[0] : null;
    entry.reason = reason || 'Actual target and declared state match the approved descriptor.';
    records.push(entry);
    return entry;
  };
  const resolveEventTarget = event => {
    const first = event.composedPath().find(node => node instanceof Element);
    return first?.closest(interactive) || first;
  };
  const prevent = (event, entry) => { if (!entry.allowed) { event.preventDefault(); event.stopImmediatePropagation(); } };
  const capture = (event, element, trigger, refusal = null) => {
    let entry;
    try { entry = inspect(element, trigger, 'event-capture', refusal); }
    catch {
      entry = { at: new Date().toISOString(), source: 'event-capture', trigger, url: location.href,
        target: null, allowed: false, control: null, states: [], reason: 'Activation inspection failed; the event was refused.' };
      records.push(entry);
    }
    prevent(event, entry);
  };
  for (const type of ['pointerdown', 'mousedown', 'click']) {
    addEventListener(type, event => capture(event, resolveEventTarget(event), type), true);
  }
  addEventListener('keydown', event => {
    if (['Tab', 'Shift', 'Control', 'Alt', 'Meta'].includes(event.key)) return;
    const activation = event.key === 'Enter' || event.key === ' ';
    const refusal = !activation ? 'Guarded keyboard permits Tab/Shift+Tab and unmodified Enter/Space only.'
      : event.shiftKey || event.ctrlKey || event.altKey || event.metaKey ? 'Modified activation keys are forbidden.' : null;
    capture(event, document.activeElement, event.key === ' ' ? 'Space' : event.key, refusal);
  }, true);
  addEventListener('submit', event => capture(event, event.target, 'submit', 'Form submission is forbidden.'), true);
  Object.defineProperty(window, '__qoreActivationGuard', { value: { inspect, drain: () => records.splice(0) }, writable: false });
};
let browser;
let context;
let page;
let video;
let traceStarted = false;
const collectActivationRecords = async () => {
  if (!policy.activation_guard || !page || page.isClosed()) return [];
  const records = await page.evaluate(() => window.__qoreActivationGuard?.drain() || []);
  events.activation_checks.push(...records);
  events.blocked_activations.push(...records.filter(record => !record.allowed));
  return records;
};
try {
  const require = createRequire(import.meta.url);
  let playwright;
  try { playwright = require(options['playwright-module'] || 'playwright'); }
  catch { throw new Error('Playwright is unavailable. Supply a locally installed optional driver with --playwright-module PATH; no installation was attempted.'); }
  try { result.driver.version = require(path.join(options['playwright-module'] || 'playwright', 'package.json')).version; } catch { /* Driver version can remain unknown. */ }
  browser = await playwright.chromium.launch({ headless: true });
  result.driver.browser_version = browser.version();
  context = await browser.newContext({ viewport: { width: 1280, height: 800 }, locale: 'en-US', serviceWorkers: 'block', recordVideo: { dir: path.join(output, 'video'), size: { width: 1280, height: 800 } } });
  if (policy.activation_guard) await context.addInitScript(installActivationGuard, { controls: policy.activation_guard, origins: policy.allowed_origins });
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
  const guardActivation = async (action, chosen = null) => {
    if (!policy.activation_guard) return action.key;
    let refusal = null;
    let key = action.key;
    if (action.type === 'keyboard') {
      if (['Tab', 'Shift+Tab'].includes(key)) return key;
      const parts = typeof key === 'string' ? key.split('+') : [];
      const last = parts.at(-1);
      const activation = ['Enter', 'Return', 'NumpadEnter', 'Space', 'Spacebar', ' '].includes(last);
      refusal = !activation ? 'Guarded keyboard permits Tab/Shift+Tab and unmodified Enter/Space only.'
        : parts.length > 1 ? 'Modified activation keys are forbidden.' : null;
      key = ['Space', 'Spacebar', ' '].includes(last) ? 'Space' : last === 'Return' ? 'Enter' : key;
    } else {
      try { await chosen.waitFor({ state: 'visible' }); }
      catch { refusal = 'The activation locator did not resolve exactly one visible control.'; chosen = null; }
    }
    const parameters = { trigger: action.type === 'keyboard' ? action.key : action.type, refusal, focused: action.type === 'keyboard' };
    const entry = chosen ? await chosen.evaluate((element, args) => window.__qoreActivationGuard.inspect(element, args.trigger, 'preflight', args.refusal), parameters)
      : await page.evaluate(args => window.__qoreActivationGuard.inspect(args.focused ? document.activeElement : null, args.trigger, 'preflight', args.refusal), parameters);
    await collectActivationRecords();
    if (!entry.allowed) {
      events.actions.push({ at: new Date().toISOString(), ...action, outcome: 'blocked', reason: entry.reason, url: page.url() });
      throw new Error(`Activation guard blocked ${parameters.trigger}: ${entry.reason}`);
    }
    return key;
  };
  for (const action of actions) {
    const at = new Date().toISOString();
    let actionOutcome = 'completed';
    const locator = () => action.role ? page.getByRole(action.role, { name: action.name, exact: action.exact !== false }) : page.locator(action.selector);
    if (action.type === 'click') {
      const chosen = locator();
      await guardActivation(action, chosen);
      await chosen.click();
    }
    else if (action.type === 'click-if-visible') {
      if (await locator().isVisible()) {
        const chosen = locator();
        await guardActivation(action, chosen);
        await chosen.click();
      }
      else actionOutcome = 'not_present';
    }
    else if (action.type === 'keyboard') await page.keyboard.press(await guardActivation(action));
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
    const captured = await collectActivationRecords();
    const blocked = captured.find(entry => !entry.allowed);
    if (blocked) {
      events.actions.push({ at, ...action, outcome: 'blocked', reason: blocked.reason, url: page.url() });
      throw new Error(`Activation guard blocked ${blocked.trigger}: ${blocked.reason}`);
    }
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
  try { await collectActivationRecords(); }
  catch (error) { result.limits.push(`Activation records could not be collected: ${error.name}`); }
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
