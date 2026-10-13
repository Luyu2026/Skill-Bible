#!/usr/bin/env python3
"""一条命令出片：brief.json → 配音 → 合成 HTML → 逐帧渲染 → 配乐混音 → MP4

用法:
  python3 make.py brief.json                       # 用 brief 里的 style
  python3 make.py brief.json --style kinetic       # 换风格，内容不变
  python3 make.py brief.json --preview             # 只出 HTML + 每场静帧，先看版面
  python3 make.py brief.json --format 9:16         # 竖版
  python3 make.py --list-styles

产出（默认在 brief 同目录 out/<style>-<format>/）:
  index.html      浏览器打开即可预览（自动播放，?t=3.5 停在某一秒）
  stills/         每场中点静帧（自检用）
  <name>.mp4      成片
"""
import argparse, hashlib, json, os, re, shutil, subprocess, sys, wave
from pathlib import Path

HERE = Path(__file__).resolve().parent
TPL = HERE.parent / "templates"
SIZES = {"16:9": (1920, 1080), "9:16": (1080, 1920), "1:1": (1080, 1080)}
# 风格 → 配乐情绪、edge-tts 音色和语速
STYLE_META = {
    "apple-keynote": ("ambient", "zh-CN-YunjianNeural", "-2%"),
    "saas-glow":     ("tech",    "zh-CN-YunxiNeural", "+4%"),
    "kinetic":       ("beat",    "zh-CN-YunxiNeural", "+14%"),
    "flat-mg":       ("bouncy",  "zh-CN-XiaoxiaoNeural", "+8%"),
    "editorial":     ("ambient", "zh-CN-XiaoxiaoNeural", "-4%"),
    "neo-brutal":    ("beat",    "zh-CN-YunxiaNeural", "+10%"),
    "cyber-glitch":  ("synth",   "zh-CN-YunyangNeural", "+6%"),
    "bento":         ("bouncy",  "zh-CN-XiaoyiNeural", "+4%"),
}

def run(cmd, **kw):
    r = subprocess.run(cmd, capture_output=True, text=True, **kw)
    if r.returncode:
        sys.stderr.write(r.stdout[-2000:] + r.stderr[-3000:])
        raise SystemExit(f"命令失败: {' '.join(map(str, cmd[:4]))} …")
    return r.stdout

def dur_of(f):
    return float(run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(f)]).strip())

# ---------- 配音 ----------
def tts(text, out_wav, engine, voice, rate, cache):
    """返回实际用的引擎。auto: edge → say；结果按文本哈希缓存。"""
    key = hashlib.md5(f"v2|{engine}|{voice}|{rate}|{text}".encode()).hexdigest()[:12]
    cached = cache / f"{key}.wav"
    if cached.exists():
        shutil.copy(cached, out_wav); return json.loads((cache / f"{key}.json").read_text())["engine"]
    used = None
    for eng in ([engine] if engine != "auto" else ["edge", "say"]):
        tmp = out_wav.with_suffix(".tmp.mp3" if eng == "edge" else ".tmp.aiff")
        try:
            if eng == "edge":
                cmd = ["uvx", "--from", "edge-tts", "edge-tts", "--voice", voice, f"--rate={rate}", "--text", text, "--write-media", str(tmp)]
                subprocess.run(cmd, capture_output=True, timeout=60, check=True)
            elif eng == "say":
                v = voice if voice and not voice.startswith("zh-CN-") else "Tingting"
                wpm = int(225 * (1 + int(re.sub(r"[^\d-]", "", rate or "0") or 0) / 100))
                subprocess.run(["say", "-v", v, "-r", str(wpm), "-o", str(tmp), text], capture_output=True, timeout=60, check=True)
            elif eng == "kokoro":
                tmp = tmp.with_suffix(".wav")
                subprocess.run(["npx", "-y", "hyperframes", "tts", text, "--voice", voice if voice.startswith("z") else "zf_xiaoxiao", "--output", str(tmp)], capture_output=True, timeout=180, check=True)
            if tmp.exists() and tmp.stat().st_size > 2000:
                # 统一成 48k 单声道，去掉首尾静音
                run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(tmp), "-af",
                     "silenceremove=start_periods=1:start_threshold=-45dB,areverse,silenceremove=start_periods=1:start_threshold=-45dB,areverse",
                     "-ar", "48000", "-ac", "1", str(out_wav)])
                used = eng; break
        except Exception:
            pass
        finally:
            if tmp.exists(): tmp.unlink()
    if not used:
        raise SystemExit("配音失败：edge-tts 和 say 都不可用。可以在 brief 里给每场写 \"voiceFile\" 用自己的录音，或 voice.engine 设为 none。")
    shutil.copy(out_wav, cached); (cache / f"{key}.json").write_text(json.dumps({"engine": used}))
    return used

def cues_for(text, dur):
    """把旁白切成字幕句，按字数分配时长（相对旁白开头）。"""
    parts = [p for p in re.split(r"(?<=[，。！？；：,.!?;:])", text) if p.strip()]
    lines, buf = [], ""
    for p in parts:
        if len(buf) + len(p) > 18 and buf: lines.append(buf); buf = p
        else: buf += p
    if buf: lines.append(buf)
    total = sum(len(l) for l in lines) or 1; t = 0; out = []
    for l in lines:
        d = dur * len(l) / total
        out.append({"start": round(t, 3), "end": round(t + d, 3), "text": re.sub(r"[，。；：,.;:]$", "", l.strip())}); t += d
    return out

# ---------- 文字检查：宣传片里不允许出现 emoji ----------
EMOJI = re.compile("[\U0001F000-\U0001FAFF\U00002600-\U000027BF\U00002B00-\U00002BFF\U0001F900-\U0001F9FF\uFE0F\u200D\u20E3\u2300-\u23FF]")

def find_emoji(node, path="brief"):
    bad = []
    if isinstance(node, str):
        hit = EMOJI.findall(node)
        if hit: bad.append(f"{path}: {node!r} 里有 {''.join(dict.fromkeys(hit))}")
    elif isinstance(node, dict):
        for k, v in node.items():
            if k not in ("logo", "image", "images", "voiceFile", "bgm", "fontFile", "css", "url"): bad += find_emoji(v, f"{path}.{k}")
    elif isinstance(node, list):
        for i, v in enumerate(node): bad += find_emoji(v, f"{path}[{i}]")
    return bad

# ---------- 图标：Lucide 线性图标（ISC 协议），按名字引用，如 "icon": "gamepad-2" ----------
ICON_DIR = HERE / "node_modules" / "lucide-static" / "icons"

def icon_svg(name):
    f = ICON_DIR / f"{name}.svg"
    if not f.exists():
        near = sorted(p.stem for p in ICON_DIR.glob(f"*{name.split('-')[0]}*.svg"))[:12] if ICON_DIR.exists() else []
        raise SystemExit(f"没有图标 {name!r}。图标用 Lucide 的名字（https://lucide.dev/icons），相近的有: {', '.join(near) or '无'}"
                         + ("" if ICON_DIR.exists() else "\n先在 scripts/ 下运行 npm install"))
    svg = re.sub(r"<!--.*?-->", "", f.read_text(), flags=re.S).strip()
    return re.sub(r'\s(class|width|height)="[^"]*"', "", svg)

# ---------- 素材 ----------
def load_logo(p, mono):
    if not p: return "", ""
    p = Path(p)
    if p.suffix.lower() == ".svg":
        svg = p.read_text()
        svg = re.sub(r"<\?xml.*?\?>", "", svg)
        if "xmlns=" not in svg: svg = svg.replace("<svg", '<svg xmlns="http://www.w3.org/2000/svg"', 1)
        svg = re.sub(r'\s(width|height|class|aria-hidden)="[^"]*"', "", svg.split(">", 1)[0]) + ">" + svg.split(">", 1)[1]
        if mono: svg = re.sub(r'\sfill="(?!none)[^"]*"', "", svg); svg = re.sub(r"fill:\s*#[0-9a-fA-F]{3,6}", "fill:currentColor", svg)
        return svg, ""
    return "", str(p)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("brief", nargs="?")
    ap.add_argument("--style"); ap.add_argument("--format"); ap.add_argument("--out")
    ap.add_argument("--fps", type=int, default=30)
    ap.add_argument("--preview", action="store_true", help="只出 HTML 和静帧，不渲染视频")
    ap.add_argument("--no-voice", action="store_true"); ap.add_argument("--no-bgm", action="store_true")
    ap.add_argument("--remix", action="store_true", help="画面已渲染过（_video.mp4 还在），只重做配音配乐混音")
    ap.add_argument("--list-styles", action="store_true")
    a = ap.parse_args()
    if a.list_styles:
        for k, (m, v, r) in STYLE_META.items(): print(f"{k:14s} 配乐:{m:8s} 音色:{v}")
        return
    brief_path = Path(a.brief).resolve(); base = brief_path.parent
    B = json.loads(brief_path.read_text())
    bad = find_emoji(B)
    if bad:
        raise SystemExit("宣传片里不能用 emoji，先改掉这些地方（卡片图标用 Lucide 图标名，如 \"icon\": \"gamepad-2\"）：\n  " + "\n  ".join(bad))
    style = a.style or B.get("style", "flat-mg")
    if style not in STYLE_META: raise SystemExit(f"没有风格 {style}，可选: {', '.join(STYLE_META)}")
    fmt = a.format or B.get("format", "16:9"); W, H = SIZES[fmt]
    out = Path(a.out or base / "out" / f"{style}-{fmt.replace(':', 'x')}").resolve()
    (out / "assets").mkdir(parents=True, exist_ok=True); (out / "voice").mkdir(exist_ok=True)
    cache = base / ".tts-cache"; cache.mkdir(exist_ok=True)
    mood, edge_voice, edge_rate = STYLE_META[style]
    vcfg = B.get("voice", {})
    engine = "none" if a.no_voice else vcfg.get("engine", "auto")
    voice = vcfg.get("voice") or edge_voice
    rate = vcfg.get("rate") or edge_rate

    # 复制图片素材，路径改成相对 index.html
    copied = {}
    def asset(p):
        if not p or str(p).startswith(("http", "data:")): return p
        src = (base / p).resolve()
        if not src.exists(): raise SystemExit(f"找不到素材 {p}")
        if src not in copied:
            dst = out / "assets" / f"{len(copied):02d}-{src.name}"; shutil.copy(src, dst); copied[src] = f"assets/{dst.name}"
        return copied[src]

    prod = B["product"]
    svg, logo_png = load_logo(base / prod["logo"] if prod.get("logo") else None, prod.get("logoMono", False))
    brand = {"name": prod.get("name", ""), "slogan": prod.get("slogan", ""), "logoSvg": svg, "logo": asset(prod["logo"]) if logo_png else "",
             "colors": {k: v for k, v in (prod.get("colors") or {}).items()}}

    scenes, engines = [], set()
    for i, s in enumerate(B["scenes"]):
        d = dict(s)
        for k in ("image",):
            if d.get(k): d[k] = asset(d[k])
        if d.get("images"): d["images"] = [asset(x) for x in d["images"]]
        if d.get("items"):
            items = []
            for it in d["items"]:
                if isinstance(it, dict):
                    it = dict(it)
                    if it.get("image"): it["image"] = asset(it["image"])
                    if it.get("icon"): it["iconSvg"] = icon_svg(it.pop("icon"))
                items.append(it)
            d["items"] = items
        text = d.pop("say", "")
        vf = out / "voice" / f"s{i + 1:02d}.wav"
        if d.get("voiceFile"):
            run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(base / d.pop("voiceFile")), "-ar", "48000", "-ac", "1", str(vf)]); engines.add("file")
        elif text and engine != "none":
            engines.add(tts(text, vf, engine, voice, rate, cache))
        if vf.exists():
            vd = dur_of(vf)
            d["voice"] = {"file": f"voice/{vf.name}", "dur": round(vd, 3), "text": text, "cues": cues_for(text, vd) if text else []}
        scenes.append(d)
    print(f"配音: {', '.join(engines) or '无'}  ({len([s for s in scenes if s.get('voice')])} 段)")

    PV = {"W": W, "H": H, "fps": a.fps, "style": style, "brand": brand, "scenes": scenes,
          "captions": B.get("captions", True), "tokens": B.get("tokens", {})}
    css = (TPL / "base.css").read_text() + "\n" + (TPL / "styles.css").read_text() + "\n"
    # 自定义展示字体（品牌字体 / 更粗的黑体）：brief 里 "fontFile": "fonts/xxx.ttf"
    if B.get("fontFile"):
        ff = (base / B["fontFile"]).resolve(); shutil.copy(ff, out / "assets" / ff.name)
        css += f'@font-face {{ font-family: "PV Display"; src: url("assets/{ff.name}"); font-weight: 100 900; }}\n:root {{ --display: "PV Display", "PingFang SC", sans-serif !important; }}\n'
    css += B.get("css", "")
    html_doc = f"""<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><title>{brand['name']} · {style}</title>
<style>{css}
body.preview {{ background:#111; }} body.preview #stage {{ transform: scale(var(--fit,1)); }}</style></head>
<body><div id="stage"><div id="bg"></div><div id="fx"></div><div id="cap"></div></div>
<script>window.PV = {json.dumps(PV, ensure_ascii=False)};</script>
<script>{(TPL / 'styles.js').read_text()}</script>
<script>{(TPL / 'runtime.js').read_text()}</script>
<script>if(!window.__PV_RENDER__){{const f=()=>{{document.body.classList.add('preview');document.documentElement.style.setProperty('--fit',Math.min(innerWidth/PV.W,innerHeight/PV.H));}};f();addEventListener('resize',f);}}</script>
</body></html>"""
    # stage 里的 #bg/#fx/#cap 需要在 scene 之下/之上：runtime 会把 scene 插到 stage 末尾，用 z-index 控制层级
    (out / "index.html").write_text(html_doc)

    node = shutil.which("node")
    tl_probe = out / "_probe.mp4"
    shutil.rmtree(out / "stills", ignore_errors=True)
    run([node, str(HERE / "render.mjs"), str(out / "index.html"), str(tl_probe), "--stills", "auto", "--stills-dir", str(out / "stills")])
    tl = json.loads((out / "_probe.timeline.json").read_text())
    (out / "timeline.json").write_text(json.dumps(tl, indent=2, ensure_ascii=False)); (out / "_probe.timeline.json").unlink()
    print(f"时长 {tl['duration']:.1f}s，{len(tl['scenes'])} 场；静帧 → {out / 'stills'}")
    if a.preview:
        print(f"预览: open {out / 'index.html'}"); return

    silent = out / "_video.mp4"
    if not (a.remix and silent.exists()):
        subprocess.run([node, str(HERE / "render.mjs"), str(out / "index.html"), str(silent), "--fps", str(a.fps)], check=True)
    (out / "_video.timeline.json").unlink(missing_ok=True)

    # ---------- 混音：旁白按时间轴摆好 + 配乐压在下面 ----------
    D = tl["duration"]
    inputs, filters, labels = ["-i", str(silent)], [], []
    k = 1
    for s in tl["scenes"]:
        if not s.get("voice"): continue
        inputs += ["-i", str(out / s["voice"]["file"])]
        ms = int(s["voice"]["start"] * 1000)
        filters.append(f"[{k}:a]adelay={ms}|{ms},apad=whole_dur={D}[v{k}]"); labels.append(f"[v{k}]"); k += 1
    bgm_src = None if a.no_bgm else B.get("bgm", "auto")
    if bgm_src == "auto":
        bgm_src = str(out / "bgm.wav"); run([sys.executable, str(HERE / "bgm.py"), mood, f"{D + .5:.2f}", bgm_src])
    elif bgm_src and bgm_src != "none":
        bgm_src = str((base / bgm_src).resolve())
    else:
        bgm_src = None
    final = out / f"{B.get('name', prod.get('name', 'promo'))}-{style}-{fmt.replace(':', 'x')}.mp4"
    if labels:
        filters.append(f"{''.join(labels)}amix=inputs={len(labels)}:normalize=0,loudnorm=I=-16:TP=-1.5[vo]")
    if bgm_src:
        inputs += ["-stream_loop", "-1", "-i", bgm_src]
        bg_db = B.get("bgmVolume", -16 if labels else -10)
        filters.append(f"[{k}:a]atrim=0:{D},afade=t=in:d=0.4,afade=t=out:st={max(D - 1.5, 0)}:d=1.5,volume={bg_db}dB[bg]")
        if labels:
            filters.append("[vo]asplit[vo1][vo2];[bg][vo2]sidechaincompress=threshold=0.04:ratio=6:attack=15:release=350[bgd];[vo1][bgd]amix=inputs=2:normalize=0,alimiter=limit=0.95[aout]")
        else:
            filters.append("[bg]anull[aout]")
    elif labels:
        filters.append("[vo]anull[aout]")
    if filters:
        run(["ffmpeg", "-y", "-loglevel", "error", *inputs, "-filter_complex", ";".join(filters), "-map", "0:v", "-map", "[aout]",
             "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-t", f"{D}", "-movflags", "+faststart", str(final)])
        silent.unlink()
    else:
        silent.rename(final)
    tl_probe.unlink(missing_ok=True)
    print(f"✅ 成片 {final}  ({dur_of(final):.1f}s)")

if __name__ == "__main__":
    main()
