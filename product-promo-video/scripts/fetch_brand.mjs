// 从产品官网抓品牌素材：名称、标题、描述、slogan 候选、logo、图标、主色、桌面/手机截图。
// 用法: node fetch_brand.mjs <url> <out-dir> [--wait 4000] [--no-mobile]
// 产出: <out-dir>/brand.json 以及 logo-*.png/svg、icon-*.png、shot-desktop*.png、shot-mobile.png
// brand.json 只是「候选」，写 brief 前要人看一遍：哪个是真 logo、哪句是真 slogan。
import puppeteer from "puppeteer-core";
import { mkdirSync, writeFileSync } from "node:fs";
import path from "node:path";
import { findChrome } from "./chrome.mjs";

const args = process.argv.slice(2);
const url = args[0];
const outDir = path.resolve(args[1] || "brand");
const wait = Number(args[args.indexOf("--wait") + 1]) || 4000;
const doMobile = !args.includes("--no-mobile");
if (!url) { console.error("用法: node fetch_brand.mjs <url> <out-dir>"); process.exit(1); }
mkdirSync(outDir, { recursive: true });

const UA_DESK = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36";
const UA_MOB = "Mozilla/5.0 (iPhone; CPU iPhone OS 17_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Mobile/15E148 Safari/604.1";

const browser = await puppeteer.launch({
  executablePath: findChrome(), headless: true,
  args: ["--no-sandbox", "--hide-scrollbars", "--force-color-profile=srgb", "--lang=zh-CN"],
});

// 关掉常见的登录弹窗 / 气泡 / cookie 条。有的站会定时再弹，所以每次截图前都清一次
async function clean(page) {
  await page.evaluate(() => {
    const sel = '[class*="mask"],[class*="Mask"],[class*="modal"],[class*="Modal"],[class*="cookie"],[class*="Cookie"],[class*="login-tip"],[class*="popup"],[class*="Popup"],[class*="dialog"],[class*="Dialog"],[class*="popover"],[class*="Popover"],[class*="toast"],[class*="guide"]';
    document.querySelectorAll(sel).forEach(el => {
      const pos = getComputedStyle(el).position;
      if (pos === "fixed" || pos === "absolute") el.remove();
    });
    document.body.style.overflow = "";
  });
}

async function open(ua, vp) {
  const page = await browser.newPage();
  await page.setUserAgent(ua);
  await page.setViewport(vp);
  await page.setExtraHTTPHeaders({ "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8" });
  try { await page.goto(url, { waitUntil: "networkidle2", timeout: 45000 }); }
  catch (e) { console.warn("页面没等到 networkidle，继续:", e.message); }
  await new Promise(r => setTimeout(r, wait));
  await clean(page);
  return page;
}

const page = await open(UA_DESK, { width: 1440, height: 900, deviceScaleFactor: 2 });

const info = await page.evaluate(() => {
  const meta = n => document.querySelector(`meta[name="${n}"],meta[property="${n}"]`)?.content?.trim() || "";
  const abs = u => { try { return new URL(u, location.href).href; } catch { return ""; } };
  const icons = [...document.querySelectorAll('link[rel*="icon"],link[rel="apple-touch-icon"],link[rel="mask-icon"]')]
    .map(l => ({ rel: l.rel, href: abs(l.href), sizes: l.getAttribute("sizes") || "" }));

  // logo 候选：class/id/alt/src/aria 里带 logo 的 img/svg，按「靠上、靠左、尺寸合理」打分
  const cands = [];
  document.querySelectorAll("img,svg,a,div,i,span").forEach(el => {
    const s = [el.className?.baseVal ?? el.className, el.id, el.getAttribute("alt"), el.getAttribute("src"), el.getAttribute("aria-label"), el.getAttribute("title")]
      .filter(Boolean).join(" ").toLowerCase();
    if (!/logo|brand/.test(s)) return;
    const r = el.getBoundingClientRect();
    if (r.width < 16 || r.height < 12 || r.width > 600 || r.height > 300) return;
    const tag = el.tagName.toLowerCase();
    const hasVisual = tag === "img" || tag === "svg" || el.querySelector("img,svg") || getComputedStyle(el).backgroundImage !== "none";
    if (!hasVisual) return;
    const score = (r.top < 200 ? 3 : 0) + (r.left < 500 ? 1 : 0) + (tag === "svg" ? 2 : tag === "img" ? 1 : 0) - r.top / 500;
    el.setAttribute("data-pv-logo", String(cands.length));
    cands.push({ i: cands.length, tag, score, w: Math.round(r.width), h: Math.round(r.height),
      src: tag === "img" ? abs(el.currentSrc || el.src) : abs(el.querySelector("img")?.currentSrc || el.querySelector("img")?.src || ""), hint: s.slice(0, 80) });
  });
  cands.sort((a, b) => b.score - a.score);

  // 主色：按可见面积统计非灰色的背景色/文字色/边框色
  const tally = {};
  const add = (c, w) => {
    const m = c && c.match(/rgba?\((\d+),\s*(\d+),\s*(\d+)(?:,\s*([\d.]+))?/);
    if (!m || (m[4] !== undefined && +m[4] < 0.6)) return;
    const [r, g, b] = [+m[1], +m[2], +m[3]];
    const mx = Math.max(r, g, b), mn = Math.min(r, g, b);
    if (mx - mn < 40) return;                      // 灰阶不算品牌色
    const hex = "#" + [r, g, b].map(v => v.toString(16).padStart(2, "0")).join("");
    tally[hex] = (tally[hex] || 0) + w;
  };
  document.querySelectorAll("body *").forEach(el => {
    const r = el.getBoundingClientRect();
    if (!r.width || !r.height || r.top > 2400) return;
    const cs = getComputedStyle(el);
    const area = Math.min(r.width * r.height, 200000);
    add(cs.backgroundColor, area);
    if (el.childNodes.length && [...el.childNodes].some(n => n.nodeType === 3 && n.textContent.trim())) add(cs.color, area * 3);
    if (el.tagName === "svg" || el.closest("svg")) add(cs.fill, area * 2);
  });
  const colors = Object.entries(tally).sort((a, b) => b[1] - a[1]).slice(0, 8).map(([hex, w]) => ({ hex, weight: Math.round(w) }));

  const heads = [...document.querySelectorAll("h1,h2")].map(h => h.innerText.trim()).filter(t => t && t.length < 60).slice(0, 12);
  const nav = [...document.querySelectorAll("nav a, header a, [class*=channel] a, [class*=nav] a")]
    .map(a => a.innerText.trim()).filter(t => t && t.length <= 8).filter((t, i, s) => s.indexOf(t) === i).slice(0, 40);

  return {
    url: location.href, title: document.title.trim(),
    siteName: meta("og:site_name") || meta("application-name"),
    description: meta("description") || meta("og:description"),
    keywords: meta("keywords"), ogImage: abs(meta("og:image")), themeColor: meta("theme-color"),
    icons, logoCandidates: cands.slice(0, 6), colors, headings: heads, navTexts: nav,
  };
});

// 下载图标和 og 图
async function download(u, name) {
  try {
    const res = await fetch(u, { headers: { "User-Agent": UA_DESK, Referer: url } });
    if (!res.ok) return "";
    const ct = res.headers.get("content-type") || "";
    const ext = ct.includes("svg") ? "svg" : ct.includes("png") ? "png" : ct.includes("jpeg") || ct.includes("jpg") ? "jpg" : ct.includes("webp") ? "webp" : ct.includes("icon") ? "ico" : (u.split("?")[0].split(".").pop() || "bin").slice(0, 4);
    const f = `${name}.${ext}`;
    writeFileSync(path.join(outDir, f), Buffer.from(await res.arrayBuffer()));
    return f;
  } catch { return ""; }
}
// 存 logo 候选（元素截图，透明底）
const logos = [];
for (const c of info.logoCandidates.slice(0, 4)) {
  const el = await page.$(`[data-pv-logo="${c.i}"]`);
  if (!el) continue;
  const f = `logo-${logos.length + 1}.png`;
  try {
    await el.screenshot({ path: path.join(outDir, f), omitBackground: true });
    const svg = c.tag === "svg" ? await el.evaluate(e => e.outerHTML) : "";
    if (svg) writeFileSync(path.join(outDir, `logo-${logos.length + 1}.svg`), svg);
    // 元素截图会带上背后的 banner，所以有原图就再存一份原图（通常是透明底）
    const raw = c.src ? await download(c.src, `logo-${logos.length + 1}-raw`) : "";
    logos.push({ file: f, raw, svg: svg ? `logo-${logos.length + 1}.svg` : "", ...c });
  } catch { /* 元素不可截图就跳过 */ }
}

const iconFiles = [];
for (const [k, ic] of info.icons.slice(0, 4).entries()) {
  const f = await download(ic.href, `icon-${k + 1}`);
  if (f) iconFiles.push({ file: f, ...ic });
}
const ogFile = info.ogImage ? await download(info.ogImage, "og-image") : "";

// 正文配图：滚动到底触发懒加载，存下所有宽度 ≥ 600 的图片和视频封面（产品界面、场景图通常在这里）
const media = [];
if (!args.includes("--no-images")) {
  const H = await page.evaluate(() => document.body.scrollHeight);
  for (let y = 0; y < Math.min(H, 30000); y += 700) { await page.evaluate(y => scrollTo(0, y), y); await new Promise(r => setTimeout(r, 250)); }
  await new Promise(r => setTimeout(r, 1500));
  const list = await page.evaluate(() => {
    const out = [], seen = new Set();
    document.querySelectorAll("img, video[poster], picture source").forEach(el => {
      let u = el.tagName === "VIDEO" ? el.poster : el.tagName === "SOURCE" ? (el.srcset || "").split(",").pop().trim().split(" ")[0] : (el.currentSrc || el.src);
      if (!u || u.startsWith("data:") || seen.has(u)) return;
      const w = el.naturalWidth || el.videoWidth || el.getBoundingClientRect().width * 2;
      if (el.tagName === "IMG" && w < 600) return;
      seen.add(u); out.push({ url: new URL(u, location.href).href, w, alt: (el.alt || "").slice(0, 80), kind: el.tagName.toLowerCase() });
    });
    return out.slice(0, 30);
  });
  for (const [k, m] of list.entries()) {
    const f = await download(m.url, `img-${String(k + 1).padStart(2, "0")}`);
    if (f) media.push({ file: f, ...m });
  }
}

// 截图：首屏 + 往下两屏 + 手机版
const shots = [];
await page.evaluate(() => scrollTo(0, 0));
await clean(page);
await page.screenshot({ path: path.join(outDir, "shot-desktop.png") });
shots.push("shot-desktop.png");
for (const k of [1, 2]) {
  await page.evaluate(y => scrollTo(0, y), k * 900);
  await new Promise(r => setTimeout(r, 1200));
  await clean(page);
  await page.screenshot({ path: path.join(outDir, `shot-desktop-${k + 1}.png`) });
  shots.push(`shot-desktop-${k + 1}.png`);
}
if (doMobile) {
  const mp = await open(UA_MOB, { width: 390, height: 844, deviceScaleFactor: 3, isMobile: true, hasTouch: true });
  await clean(mp);
  await mp.screenshot({ path: path.join(outDir, "shot-mobile.png") });
  shots.push("shot-mobile.png");
}
await browser.close();

const brand = { ...info, files: { logos, icons: iconFiles, ogImage: ogFile, screenshots: shots, images: media } };
writeFileSync(path.join(outDir, "brand.json"), JSON.stringify(brand, null, 2));
console.log(`标题: ${info.title}\n描述: ${info.description}\n主色候选: ${info.colors.map(c => c.hex).join(" ")}`);
console.log(`logo 候选 ${logos.length} 个，图标 ${iconFiles.length} 个，截图 ${shots.length} 张，正文配图 ${media.length} 张 → ${outDir}`);
