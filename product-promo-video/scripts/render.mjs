// 确定性渲染：打开 index.html → 逐帧 seek(t) 截图 → 管道喂给 ffmpeg → 无声 MP4
// 用法: node render.mjs <index.html> <out.mp4> [--fps 30] [--from 0 --to 5] [--stills 2.5,6,9 --stills-dir dir]
// 同时把时间轴写到 <out>.timeline.json（混音要用：每段旁白从第几秒开始）
import puppeteer from "puppeteer-core";
import { spawn } from "node:child_process";
import { writeFileSync, mkdirSync } from "node:fs";
import path from "node:path";
import { findChrome } from "./chrome.mjs";

const argv = process.argv.slice(2);
const opt = (k, d) => { const i = argv.indexOf("--" + k); return i >= 0 ? argv[i + 1] : d; };
const html = path.resolve(argv[0]), out = path.resolve(argv[1]);
const fps = Number(opt("fps", 30));

const browser = await puppeteer.launch({
  executablePath: findChrome(), headless: true,
  args: ["--no-sandbox", "--hide-scrollbars", "--force-color-profile=srgb", "--disable-web-security", "--allow-file-access-from-files", "--font-render-hinting=none"],
});
const page = await browser.newPage();
page.on("pageerror", e => console.error("页面报错:", e.message));
await page.evaluateOnNewDocument(() => { window.__PV_RENDER__ = true; });
await page.goto("file://" + html, { waitUntil: "load" });
const { W, H } = await page.evaluate(() => ({ W: window.PV.W, H: window.PV.H }));
await page.setViewport({ width: W, height: H, deviceScaleFactor: 1 });
await page.evaluate(async () => {
  if (document.fonts) await document.fonts.ready;
  await Promise.all([...document.images].map(i => i.complete ? 0 : new Promise(r => { i.onload = i.onerror = r; })));
});
const tl = await page.evaluate(() => window.PV_TIMELINE);
writeFileSync(out.replace(/\.mp4$/, "") + ".timeline.json", JSON.stringify(tl, null, 2));

// 只截几张静帧（自检用）；auto = 每场 62% 处一张
const stills = opt("stills");
if (stills) {
  const dir = path.resolve(opt("stills-dir", path.dirname(out)));
  mkdirSync(dir, { recursive: true });
  const list = stills === "auto" ? tl.scenes.map(s => +(s.start + s.dur * .62).toFixed(2)) : stills.split(",").map(Number);
  for (const [k, s] of list.entries()) {
    await page.evaluate(t => window.seek(t), s);
    await page.screenshot({ path: path.join(dir, `s${String(k + 1).padStart(2, "0")}-${s.toFixed(2)}s.jpg`), type: "jpeg", quality: 88 });
  }
  await browser.close();
  console.log(`静帧 ${stills} → ${dir}`);
  process.exit(0);
}

const from = Number(opt("from", 0)), to = Math.min(Number(opt("to", tl.duration)), tl.duration);
const total = Math.round((to - from) * fps);
console.log(`渲染 ${W}×${H} ${(to - from).toFixed(1)}s @${fps}fps = ${total} 帧`);

const ff = spawn("ffmpeg", ["-y", "-loglevel", "error", "-f", "image2pipe", "-framerate", String(fps), "-c:v", "mjpeg", "-i", "-",
  "-c:v", "libx264", "-preset", "medium", "-crf", "17", "-pix_fmt", "yuv420p", "-movflags", "+faststart", out], { stdio: ["pipe", "inherit", "inherit"] });
const cdp = await page.createCDPSession();
const t0 = Date.now();
for (let i = 0; i < total; i++) {
  await page.evaluate(t => window.seek(t), from + i / fps);
  const { data } = await cdp.send("Page.captureScreenshot", { format: "jpeg", quality: 94, optimizeForSpeed: true });
  if (!ff.stdin.write(Buffer.from(data, "base64"))) await new Promise(r => ff.stdin.once("drain", r));
  if (i % 30 === 0) process.stdout.write(`  ${i}/${total}  ${((Date.now() - t0) / 1000).toFixed(0)}s\r`);
}
ff.stdin.end();
await new Promise(r => ff.on("close", r));
await browser.close();
console.log(`\n画面完成 → ${out}`);
