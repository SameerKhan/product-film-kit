// Offline, deny-by-default capture harness template (Playwright).
// Serves a LOCAL build of your web app, fulfils every API call from fixtures, mirrors your own static
// assets from a hashed local folder, and aborts everything else. Nothing reaches production.
//
// Adapt: DIST (your built app), API (your endpoints -> fixture responses), MIRROR_HOSTS, SEED (localStorage).
// Run:   node harness.mjs survey     -> screenshots of ROUTES + a network gate report
import http from "node:http";
import path from "node:path";
import fs from "node:fs";
import { fileURLToPath } from "node:url";
import { chromium } from "playwright";

const ROOT = path.dirname(fileURLToPath(import.meta.url));
const DIST = process.env.DIST || path.join(ROOT, "dist");                      // your app's static build
const FIXTURES_PATH = process.env.FIXTURES || path.join(ROOT, "fixtures.json");
if (!fs.existsSync(FIXTURES_PATH)) throw new Error(`no fixtures at ${FIXTURES_PATH}: copy fixtures.example.json to fixtures.json and edit it, or set FIXTURES`);
const FIXTURES = JSON.parse(fs.readFileSync(FIXTURES_PATH, "utf8"));
const MIRROR_HOSTS = new Set((process.env.MIRROR_HOSTS || "").split(",").filter(Boolean)); // e.g. static.yourapp.com
const ROUTES = ["dashboard", "calendar", "inbox", "reports"];

// Refuse to run if any variable that would point the app at a live account is set. Name your app's own
// live-mode variables (comma-separated) in REFUSE_IF_SET; a name regex would also match OS variables
// such as macOS's SECURITYSESSIONID and block every run.
for (const k of (process.env.REFUSE_IF_SET || "PLAYWRIGHT_STORAGE_STATE,E2E_EMAIL,E2E_PASSWORD").split(",").filter(Boolean))
  if (process.env[k]) throw new Error(`refusing to run: ${k} is set (live mode is not allowed)`);

function serveDist(dir) {           // tiny static server with SPA fallback, bound to loopback only
  const types = { ".html": "text/html", ".js": "text/javascript", ".css": "text/css", ".svg": "image/svg+xml", ".png": "image/png", ".json": "application/json", ".woff2": "font/woff2" };
  const srv = http.createServer((req, res) => {
    const root = fs.realpathSync(dir);
    let p = path.resolve(root, "." + decodeURIComponent(new URL(req.url, "http://x").pathname));
    // containment on the REAL path (no ../ escapes, no prefix-sibling dirs, no symlinks out of the build)
    const real = fs.existsSync(p) ? fs.realpathSync(p) : "";
    if (!real || !(real === root || real.startsWith(root + path.sep)) || fs.statSync(real).isDirectory()) p = path.join(root, "index.html"); else p = real;
    res.writeHead(200, { "content-type": types[path.extname(p)] || "application/octet-stream" }); fs.createReadStream(p).pipe(res);
  });
  return new Promise((r) => srv.listen(0, "127.0.0.1", () => r({ srv, url: `http://127.0.0.1:${srv.address().port}` })));
}

export async function start(opts = {}) {
  const made = {};   // everything created so far, so a failed start never leaves a server or browser behind
  try { return await startInner(opts, made); }
  catch (e) { await made.ctx?.close().catch(() => {}); await made.browser?.close().catch(() => {}); made.srv?.close(); throw e; }
}

async function startInner({ dpr = 1, video = null, viewport = { width: 1920, height: 1080 } }, made) {
  const { srv, url } = await serveDist(DIST); made.srv = srv; const ORIGIN = new URL(url).origin;
  const log = { fixture: [], aborted: [], unmatched: [], pageErrors: [], bad: [] };
  // channel "chrome" uses the installed Google Chrome with a fresh temp profile when the pinned browser build is missing
  const browser = made.browser = await chromium.launch({ headless: true, ...(process.env.CHROME_CHANNEL ? { channel: process.env.CHROME_CHANNEL } : {}) });
  const ctx = made.ctx = await browser.newContext({ viewport, deviceScaleFactor: dpr, serviceWorkers: "block",
    ...(video ? { recordVideo: { dir: video, size: viewport } } : {}) });
  const cors = { "access-control-allow-origin": ORIGIN, "access-control-allow-credentials": "true", "access-control-allow-headers": "*",
    "access-control-allow-methods": "GET,POST,PUT,PATCH,DELETE,OPTIONS" };
  const json = (r, body) => r.fulfill({ status: 200, contentType: "application/json", headers: cors, body: JSON.stringify(body) });
  // [method or "*", path regex, handler]. Keep this list explicit: an unmatched API call FAILS the run.
  // keys are "METHOD /path-regex"; patterns are anchored, so /api/v1/posts never matches /api/v1/posts/delete
  const API = Object.entries(FIXTURES).map(([k, body]) => { const [m, re] = k.split(" "); return [m, new RegExp(`^(?:${re.replace(/^\^|\$$/g, "")})$`), (r) => json(r, body)]; });

  await ctx.routeWebSocket(/.*/, (ws) => ws.close());
  await ctx.route("**/*", async (route) => {           // installed on the CONTEXT, before any page exists
    const req = route.request(); const u = new URL(req.url()); const method = req.method().toUpperCase();
    const local = ["localhost", "127.0.0.1", "::1"].includes(u.hostname);
    const api = new RegExp(process.env.API_PATH || "^/api(/|$)").test(u.pathname);
    if (u.origin === ORIGIN && !api) return route.continue();   // the only real transport: the local build's files
    if (api || local) {   // API calls (relative or absolute) are fixtures; anything else local is unmatched
      if (method === "OPTIONS") return route.fulfill({ status: 204, headers: cors, body: "" });
      for (const [m, re, h] of API) if ((m === "*" || m === method) && re.test(u.pathname)) { log.fixture.push(`${method} ${u.pathname}`); return h(route); }
      log.unmatched.push(`${method} ${u.host}${u.pathname}`); return route.abort("blockedbyclient");
    }
    if (MIRROR_HOSTS.has(u.hostname)) {
      const f = path.join(ROOT, "mirror", u.hostname, u.pathname);
      if (f.startsWith(path.join(ROOT, "mirror")) && fs.existsSync(f)) { log.fixture.push(`MIRROR ${u.pathname}`); return route.fulfill({ status: 200, path: f }); }
    }
    log.aborted.push(u.href); return route.abort("blockedbyclient");
  });
  let page = null;
  ctx.on("page", (p) => { if (page && p !== page) p.close().catch(() => {}); });   // popups closed on open
  page = await ctx.newPage();
  page.on("pageerror", (e) => log.pageErrors.push(e.message));
  page.on("response", (r) => { if (r.status() >= 400) log.bad.push({ url: r.url(), why: `HTTP ${r.status()}` }); });
  page.on("requestfailed", (r) => log.bad.push({ url: r.url(), why: r.failure()?.errorText || "failed" }));
  const SEED = JSON.parse(process.env.SEED_LOCALSTORAGE || "{}");                // e.g. {"authToken":"synthetic","workspace":"demo"}
  await page.addInitScript((seed) => { for (const [k, v] of Object.entries(seed)) localStorage.setItem(k, v); }, SEED);
  const close = async () => { await ctx.close().catch(() => {}); await browser.close().catch(() => {}); await new Promise((r) => srv.close(r)); };
  for (const sig of ["SIGINT", "SIGTERM", "SIGHUP"]) process.once(sig, () => close().then(() => process.exit(130)));   // no orphan browsers
  return { page, ctx, ORIGIN, log, close };
}

export function gates(log) {
  // requests the router aborted on purpose (third-party hosts) also surface as failures; only the rest count
  const expected = new Set(log.aborted);
  const bad = log.bad.filter((b) => !expected.has(b.url)).map((b) => `${b.why} ${b.url}`);
  const g = { unmatched: [...new Set(log.unmatched)], pageErrors: log.pageErrors, aborted: [...expected],
    fixtureCalls: log.fixture.length, unexpectedFailures: [...new Set(bad)] };
  g.pass = !g.unmatched.length && !g.pageErrors.length && !g.unexpectedFailures.length;
  return g;
}

if (process.argv[1].endsWith("harness.mjs") && process.argv[2] === "survey") {
  const out = path.join(ROOT, "survey"); fs.mkdirSync(out, { recursive: true });
  const { page, ORIGIN, log, close } = await start();
  try {
    for (const r of ROUTES) {
      await page.goto(`${ORIGIN}/${r}`, { waitUntil: "domcontentloaded", timeout: 60000 }).catch((e) => console.log("nav", r, e.message.split("\n")[0]));
      await page.waitForTimeout(3000);
      await page.screenshot({ path: path.join(out, r.replace(/\//g, "_") + ".png") });
    }
  } finally { const g = gates(log); console.log(JSON.stringify(g, null, 1)); await close(); process.exitCode = g.pass ? 0 : 1; }
}
