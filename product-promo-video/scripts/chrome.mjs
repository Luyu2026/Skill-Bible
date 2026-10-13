// 找一个能用的 Chrome：环境变量 > puppeteer 缓存 > 系统安装的 Chrome / Edge / Chromium
import { existsSync, globSync } from "node:fs";

export function findChrome() {
  const home = process.env.HOME;
  const list = [
    process.env.CHROME_PATH,
    ...globSync(home + "/.cache/puppeteer/chrome-headless-shell/*/*/chrome-headless-shell"),
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    ...globSync(home + "/.cache/puppeteer/chrome/*/*/*/Contents/MacOS/Google Chrome for Testing"),
    "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
    "/usr/bin/google-chrome", "/usr/bin/chromium", "/usr/bin/chromium-browser",
  ].filter(Boolean);
  const hit = list.find(p => existsSync(p));
  if (!hit) { console.error("找不到 Chrome。装一个，或设置 CHROME_PATH。"); process.exit(1); }
  return hit;
}
