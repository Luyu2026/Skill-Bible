/* 动效风格库。每个风格 = 皮肤(tokens + styles.css 里的 .st-xxx) + 动作(文字/图片/卡片入场) + 转场 + 背景。
 * 品牌色会覆盖 accent / accent2，所以同一个风格换产品不用改代码。
 * 新增风格：在这里加一项，在 styles.css 加 .st-<name> 皮肤，在 references/styles.md 写清楚用法。
 */
(() => {
  const tx = (name, o) => (sc, el, at) => window.PV_TEXT[name](sc, el, at, o);
  const im = (name, o) => (sc, el, at) => window.PV_IMAGE[name](sc, el, at, o);
  const U = () => window.PVU;

  // 一些背景生成器
  const blobs = (n, colors, blur = 160, alpha = .55) => (bg, { h, P, rand }) => {
    const els = [];
    for (let i = 0; i < n; i++) {
      const b = h("i", "blob"); const sz = (.35 + rand(i + 1) * .35) * Math.max(P.W, P.H);
      Object.assign(b.style, { position: "absolute", width: sz + "px", height: sz + "px", borderRadius: "50%", background: colors[i % colors.length], filter: `blur(${blur}px)`, opacity: alpha, left: 0, top: 0 });
      bg.appendChild(b); els.push({ b, sz, i });
    }
    return t => els.forEach(({ b, sz, i }) => {
      const x = (.5 + .42 * Math.sin(t * .23 + i * 2.1)) * P.W - sz / 2, y = (.5 + .38 * Math.cos(t * .19 + i * 1.7)) * P.H - sz / 2;
      b.style.transform = `translate(${x}px, ${y}px)`;
    });
  };

  window.STYLES = {
    // 1. 苹果发布会极简：黑底、大字、慢、柔光。适合：高端硬件、旗舰功能、品牌片
    "apple-keynote": {
      label: "发布会极简", pace: 1.15, transition: "blur", transitionDur: .9,
      tokens: { bg: "#000", fg: "#f5f5f7", sub: "#86868b", accent: "#2997ff", accent2: "#bf5af2", card: "#1d1d1f", hl: "var(--accent)", titleWeight: "700", heroSize: "150px", capBg: "rgba(0,0,0,0)", capFg: "#d2d2d7" },
      text: { kicker: tx("fadeUp", { dist: 20 }), title: tx("blurIn"), sub: tx("fadeUp", { dur: 1 }) },
      image: im("floatUp", { dur: 1.6 }), card: im("floatUp"), cardGap: .2, logoIn: tx("blurIn", { dur: 1.6 }),
      tagMode: "cloud",
      bg: (bg, { h, P }) => { const g = h("i"); Object.assign(g.style, { position: "absolute", inset: "0", background: `radial-gradient(60% 50% at 50% 115%, color-mix(in srgb, var(--accent) 35%, transparent), transparent 70%)` }); bg.appendChild(g); return t => { g.style.opacity = .55 + .25 * Math.sin(t * .6); }; },
    },

    // 2. 科技 SaaS 光晕：深色、渐变光斑、网格、玻璃卡、3D 倾斜截图。适合：软件、AI、开发者工具、B 端
    "saas-glow": {
      label: "科技光晕", pace: 1.0, transition: "zoom", transitionDur: .7,
      tokens: { bg: "#070a14", fg: "#f4f6ff", sub: "#9aa3c0", accent: "#7c5cff", accent2: "#22d3ee", card: "rgba(255,255,255,.06)", hl: "var(--accent2)", radius: "24px", capBg: "rgba(10,14,30,.7)" },
      text: { kicker: tx("fadeUp", { dist: 16 }), title: tx("charStagger"), sub: tx("fadeUp") },
      image: im("tilt3d"), card: im("floatUp"), logoIn: tx("blurIn"), tagMode: "cloud",
      bg: (bg, ctx) => {
        const up = blobs(3, ["var(--accent)", "var(--accent2)", "#3b82f6"], 180, .35)(bg, ctx);
        const grid = ctx.h("i"); Object.assign(grid.style, { position: "absolute", inset: "-100px", backgroundImage: "linear-gradient(rgba(255,255,255,.05) 1px, transparent 1px), linear-gradient(90deg, rgba(255,255,255,.05) 1px, transparent 1px)", backgroundSize: "80px 80px", maskImage: "radial-gradient(ellipse at center, #000 30%, transparent 75%)", WebkitMaskImage: "radial-gradient(ellipse at center, #000 30%, transparent 75%)" });
        bg.appendChild(grid);
        return t => { up(t); grid.style.transform = `translateY(${(t * 12) % 80}px)`; };
      },
    },

    // 3. 快节奏文字（Kinetic Typography）：巨字、砸入、闪切、每场换底色。适合：短视频平台、活动、年轻品牌
    "kinetic": {
      label: "快节奏大字", pace: .8, transition: "flash", transitionDur: .25,
      tokens: { bg: "#111", fg: "#fff", sub: "rgba(255,255,255,.8)", accent: "#ff3b30", accent2: "#ffd60a", card: "rgba(0,0,0,.25)", hl: "var(--accent2)", titleWeight: "900", heroSize: "190px", titleSize: "120px", secSize: "104px", titleTrack: "-.03em", display: "\"PingFang SC\", sans-serif", capBg: "#000" },
      text: { kicker: tx("slideHard"), title: tx("punch"), sub: tx("fadeUp", { dur: .4, dist: 30 }) },
      image: im("zoomOut", { dur: .6 }), card: im("popBounce", { dur: .5 }), cardGap: .08, logoIn: tx("punch", { from: 3 }), tagMode: "marquee",
      sceneHook: (sc, d, el) => { // 底色在 品牌色 / 黑 / 副色 之间轮换，形成节奏
        const pal = ["var(--accent)", "#111", "var(--accent2)", "#fff"], fgs = ["#fff", "#fff", "#111", "#111"];
        const k = sc.idx % pal.length; if (d.type === "logo" || d.type === "end") return;
        el.style.background = pal[k]; el.style.color = fgs[k]; el.style.setProperty("--sub", fgs[k]); el.style.setProperty("--fg", fgs[k]);
        if (k === 0 || k === 2) el.style.setProperty("--hl", fgs[k] === "#fff" ? "#111" : "#fff");
      },
      bg: null,
    },

    // 4. 扁平 MG 动画：明亮配色、几何图形漂浮、逐字弹跳、色块转场。适合：消费 App、教育、社区、年轻用户
    "flat-mg": {
      label: "扁平MG", pace: 1.0, transition: "shapeWipe", transitionDur: .7,
      tokens: { bg: "#fff6f9", fg: "#1f2340", sub: "#5b6080", accent: "#ff6699", accent2: "#00aeec", card: "#fff", hl: "var(--accent)", radius: "36px", cardShadow: "0 18px 0 rgba(31,35,64,.08)", titleWeight: "900", display: "\"PingFang SC\", sans-serif", capBg: "#1f2340", shadow: "0 30px 0 rgba(31,35,64,.10)" },
      text: { kicker: tx("charPop"), title: tx("charPop"), sub: tx("fadeUp") },
      image: im("popBounce"), card: im("popBounce"), logoIn: im("popBounce", { dur: 1 }), tagMode: "cloud",
      bg: (bg, { h, P, rand }) => {
        const shapes = [];
        const kinds = ["circle", "ring", "tri", "plus", "squiggle", "dot"];
        for (let i = 0; i < 14; i++) {
          const s = h("i", "mg-" + kinds[i % kinds.length]); const c = i % 3 === 0 ? "var(--accent)" : i % 3 === 1 ? "var(--accent2)" : "#ffd166";
          s.style.setProperty("--c", c); s.style.position = "absolute"; s.style.left = 0; s.style.top = 0;
          // 只放在四周边带，别压到正文
          const top = i % 2 === 0, x = (i / 14) + rand(i * 5) * .06, y = top ? .02 + rand(i * 9) * .1 : .86 + rand(i * 9) * .08;
          bg.appendChild(s); shapes.push({ s, x: x * P.W, y: y * P.H, sp: .3 + rand(i) * .8, r: rand(i + 3) * 360 });
        }
        return t => shapes.forEach(({ s, x, y, sp, r }, i) => { s.style.transform = `translate(${x + Math.sin(t * sp + i) * 26}px, ${y + Math.cos(t * sp * .8 + i) * 26}px) rotate(${r + t * 30 * (i % 2 ? 1 : -1)}deg)`; });
      },
    },

    // 5. 杂志编辑风：米色纸感、衬线大字、遮罩上推、细线排版、页码。适合：内容、文化、生活方式、高端服务
    "editorial": {
      label: "杂志编辑", pace: 1.15, transition: "pushUp", transitionDur: .9,
      tokens: { bg: "#f3efe6", fg: "#1a1a1a", sub: "#5a554c", accent: "#c8102e", accent2: "#1a1a1a", card: "#ebe5d8", hl: "var(--accent)", font: "\"Songti SC\", \"STSong\", serif", display: "\"Songti SC\", \"STSong\", serif", titleWeight: "900", radius: "4px", capBg: "#1a1a1a", capFg: "#f3efe6", shadow: "0 30px 80px rgba(60,40,10,.18)", frameBg: "#fff" },
      text: { kicker: tx("fadeUp", { dist: 12 }), title: tx("maskUp"), sub: tx("fadeUp", { dur: 1 }) },
      image: im("wipe", { dur: 1.2 }), card: im("wipe"), cardGap: .18, logoIn: tx("letterSpace"), tagMode: "cloud",
      bg: (bg, { h, P }) => {
        const paper = h("i"); Object.assign(paper.style, { position: "absolute", inset: 0, opacity: .35, backgroundImage: `url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='300' height='300'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='.9' numOctaves='3'/%3E%3C/filter%3E%3Crect width='300' height='300' filter='url(%23n)' opacity='.35'/%3E%3C/svg%3E")` });
        const frame = h("i"); Object.assign(frame.style, { position: "absolute", inset: "48px", border: "1.5px solid rgba(26,26,26,.5)" });
        const num = h("b"); Object.assign(num.style, { position: "absolute", right: "80px", bottom: "70px", font: "600 26px/1 'Songti SC', serif", letterSpacing: ".2em" });
        const mast = h("b"); Object.assign(mast.style, { position: "absolute", left: "80px", top: "70px", font: "600 24px/1 'Songti SC', serif", letterSpacing: ".3em", textTransform: "uppercase" });
        mast.textContent = (P.brand.name || "") + "  ·  " + new Date().getFullYear();
        bg.append(paper, frame, num, mast);
        return t => { const i = P.scenes.findIndex(s => t >= s.start && t < s.start + s.dur); num.textContent = String(i + 1).padStart(2, "0") + " / " + String(P.scenes.length).padStart(2, "0"); };
      },
    },

    // 6. 新粗野主义：粗黑描边、硬投影、高饱和、阶梯运动、色带转场。适合：独立开发、潮牌、创意工具
    "neo-brutal": {
      label: "新粗野", pace: .9, transition: "stripes", transitionDur: .6,
      tokens: { bg: "#fff4d6", fg: "#111", sub: "#333", accent: "#ff5c39", accent2: "#3d6bff", card: "#fff", hl: "var(--accent)", radius: "18px", cardShadow: "10px 10px 0 #111", shadow: "14px 14px 0 #111", titleWeight: "900", display: "\"PingFang SC\", sans-serif", capBg: "#111", frameBg: "#fff", barBg: "#ffe14d" },
      text: { kicker: tx("slideHard"), title: tx("slideHard"), sub: tx("slideHard") },
      image: im("slideHard"), card: im("slideHard"), cardGap: .1, logoIn: im("slideHard"), tagMode: "cloud",
      bg: (bg, { h }) => { const g = h("i"); Object.assign(g.style, { position: "absolute", inset: "-60px", backgroundImage: "radial-gradient(#111 2px, transparent 2.5px)", backgroundSize: "44px 44px", opacity: .18 }); bg.appendChild(g); return t => { g.style.transform = `translate(${(t * 22) % 44}px, ${(t * 22) % 44}px)`; }; },
    },

    // 7. 赛博故障：黑底霓虹、扫描线、解码文字、故障转场、透视网格地面。适合：游戏、电竞、Web3、潮流科技
    "cyber-glitch": {
      label: "赛博故障", pace: .9, transition: "glitchCut", transitionDur: .45,
      tokens: { bg: "#05030a", fg: "#e9fbff", sub: "#8ba4b8", accent: "#00f0ff", accent2: "#ff2bd6", card: "rgba(0,240,255,.07)", hl: "var(--accent2)", radius: "6px", glitchA: "var(--accent2)", glitchB: "var(--accent)", display: "\"PingFang SC\", Menlo, monospace", titleWeight: "900", capBg: "rgba(0,0,0,.8)", capFg: "var(--accent)", shadow: "0 0 0 2px var(--accent), 0 0 60px color-mix(in srgb, var(--accent) 45%, transparent)" },
      text: { kicker: tx("typewriter", { cps: 24 }), title: tx("glitch"), sub: tx("typewriter", { cps: 22 }) },
      image: im("glitch"), card: im("glitch", { dur: .5 }), cardGap: .1, logoIn: im("glitch", { dur: 1.1 }), tagMode: "danmaku",
      bg: (bg, { h }) => {
        const floor = h("i"); Object.assign(floor.style, { position: "absolute", left: "-50%", right: "-50%", bottom: "-10%", height: "70%", backgroundImage: "linear-gradient(color-mix(in srgb, var(--accent2) 60%, transparent) 2px, transparent 2px), linear-gradient(90deg, color-mix(in srgb, var(--accent2) 60%, transparent) 2px, transparent 2px)", backgroundSize: "90px 90px", transform: "perspective(500px) rotateX(62deg)", transformOrigin: "50% 100%", maskImage: "linear-gradient(to top, #000, transparent 85%)", WebkitMaskImage: "linear-gradient(to top, #000, transparent 85%)", opacity: .55 });
        const scan = h("i"); Object.assign(scan.style, { position: "absolute", inset: 0, backgroundImage: "repeating-linear-gradient(0deg, rgba(255,255,255,.04) 0 2px, transparent 2px 4px)" });
        const vig = h("i"); Object.assign(vig.style, { position: "absolute", inset: 0, background: "radial-gradient(ellipse at center, transparent 50%, rgba(0,0,0,.8))" });
        bg.append(floor, scan, vig);
        return t => { floor.style.backgroundPosition = `0 ${(t * 120) % 90}px`; scan.style.opacity = .7 + .3 * Math.sin(t * 40); };
      },
    },

    // 8. 便当格：浅灰底、圆角卡片网格、缩放入场、干净克制。适合：功能多的产品、效率工具、硬件参数
    "bento": {
      label: "便当格", pace: 1.0, transition: "zoom", transitionDur: .6,
      tokens: { bg: "#f5f5f7", fg: "#1d1d1f", sub: "#6e6e73", accent: "#0071e3", accent2: "#ff375f", card: "#fff", hl: "var(--accent)", radius: "36px", cardShadow: "0 1px 0 rgba(0,0,0,.04), 0 20px 50px rgba(0,0,0,.06)", titleWeight: "700", capBg: "rgba(29,29,31,.8)", shadow: "0 30px 80px rgba(0,0,0,.12)" },
      text: { kicker: tx("fadeUp", { dist: 14 }), title: tx("fadeUp", { dist: 50, dur: .9 }), sub: tx("fadeUp") },
      image: im("zoomOut"), card: (sc, el, at) => window.PV_IMAGE.zoomOut(sc, el, at, { dur: .8 }), cardGap: .12, logoIn: tx("blurIn"), tagMode: "cloud",
      bg: null,
    },
  };
})();
