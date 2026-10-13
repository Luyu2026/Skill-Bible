/* product-promo-video 运行时
 * 输入: window.PV = { W, H, fps, brand, style, scenes:[{type, ..., start, dur, voice:{start,dur,text,cues}}], captions }
 * 输出: window.DURATION 和 window.seek(t) —— 画面完全由 t 决定，渲染器逐帧调 seek 截图。
 * 风格: window.STYLES[name] = { tokens, text, image, card, transition, bg(), decor?, sceneHook? }
 * 预览: 直接用浏览器打开 index.html 会自动播放（带 ?t=3.2 停在第 3.2 秒）。
 */
(() => {
  // ---------- 缓动与工具 ----------
  const clamp = (x, a = 0, b = 1) => Math.max(a, Math.min(b, x));
  const lerp = (a, b, p) => a + (b - a) * p;
  const E = {
    lin: x => x,
    out3: x => 1 - Math.pow(1 - x, 3),
    out5: x => 1 - Math.pow(1 - x, 5),
    in3: x => x * x * x,
    io3: x => x < .5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2,
    expo: x => x === 1 ? 1 : 1 - Math.pow(2, -10 * x),
    back: x => { const c = 1.9; return 1 + (c + 1) * Math.pow(x - 1, 3) + c * Math.pow(x - 1, 2); },
    elastic: x => x === 0 || x === 1 ? x : Math.pow(2, -10 * x) * Math.sin((x * 10 - .75) * (2 * Math.PI / 3)) + 1,
    step: n => x => Math.floor(x * n) / n,
  };
  // 确定性伪随机（同一个 seed 每帧一样）
  const rand = s => { const x = Math.sin(s * 127.1 + 311.7) * 43758.5453; return x - Math.floor(x); };
  const seg = (t, s, d) => clamp((t - s) / d);
  window.PVU = { clamp, lerp, E, rand, seg };

  const P = window.PV, S = window.STYLES[P.style];
  if (!S) throw new Error("未知风格 " + P.style);
  const T = S.tokens, root = document.documentElement;
  // 品牌色覆盖风格默认色
  const tok = Object.assign({}, T, P.brand.colors || {}, P.tokens || {});
  for (const [k, v] of Object.entries(tok)) if (typeof v === "string") root.style.setProperty("--" + k, v);
  root.style.setProperty("--W", P.W + "px"); root.style.setProperty("--H", P.H + "px");
  document.body.className = `st-${P.style} ${P.W >= P.H ? "land" : "port"}`;

  const stage = document.getElementById("stage");
  const h = (tag, cls, html) => { const e = document.createElement(tag); if (cls) e.className = cls; if (html != null) e.innerHTML = html; return e; };
  const esc = s => String(s ?? "").replace(/[&<>]/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;" }[c]));
  // **重点** → <em>；\n → 换行
  const rich = s => esc(s).replace(/\*\*(.+?)\*\*/g, "<em>$1</em>").replace(/\n/g, "<br>");

  // ---------- 动画注册 ----------
  // 每个动画单元: {el, scene, at(场景内秒), dur, fn(el,p,lt,extra)}
  const anims = [];
  const addAnim = (scene, el, at, dur, fn, extra = {}) => anims.push({ scene, el, at, dur, fn, extra });

  // 把文字拆成字（保留 <em>/<br>），用于逐字动画
  function splitChars(el) {
    const out = [];
    const walk = (node, inEm) => {
      [...node.childNodes].forEach(n => {
        if (n.nodeType === 3) {
          const frag = document.createDocumentFragment();
          for (const ch of n.textContent) {
            const sp = h("span", "ch" + (inEm ? " ch-em" : ""), ch === " " ? "&nbsp;" : esc(ch));
            frag.appendChild(sp); out.push(sp);
          }
          n.replaceWith(frag);
        } else if (n.nodeName === "EM") walk(n, true);
        else if (n.nodeName !== "BR") walk(n, inEm);
      });
    };
    walk(el, false);
    return out;
  }
  // 按 <br> 拆行，每行包一层遮罩（maskUp 用）
  function splitLines(el) {
    const parts = el.innerHTML.split(/<br\s*\/?>/);
    el.innerHTML = parts.map(p => `<span class="line"><span class="line-in">${p}</span></span>`).join("");
    return [...el.querySelectorAll(".line-in")];
  }

  // ---------- 文字入场预设 ----------
  const TEXT = {
    fadeUp(sc, el, at, o = {}) {
      addAnim(sc, el, at, o.dur || .7, (el, p) => { const e = E.out3(p); el.style.opacity = e; el.style.transform = `translateY(${(1 - e) * (o.dist || 40)}px)`; });
    },
    blurIn(sc, el, at, o = {}) {
      addAnim(sc, el, at, o.dur || 1.1, (el, p) => { const e = E.out3(p); el.style.opacity = e; el.style.filter = `blur(${(1 - e) * 18}px)`; el.style.transform = `scale(${lerp(1.08, 1, e)})`; });
    },
    letterSpace(sc, el, at, o = {}) { // 字距收拢（发布会/奢侈品常见）
      addAnim(sc, el, at, o.dur || 1.4, (el, p) => { const e = E.out5(p); el.style.opacity = E.out3(clamp(p * 1.6)); el.style.letterSpacing = `${(1 - e) * .5}em`; el.style.filter = `blur(${(1 - e) * 6}px)`; });
    },
    charStagger(sc, el, at, o = {}) {
      const chs = splitChars(el), gap = o.gap ?? Math.min(.05, 1 / Math.max(chs.length, 1));
      chs.forEach((c, i) => addAnim(sc, c, at + i * gap, o.dur || .6, (c, p) => { const e = E.out3(p); c.style.opacity = e; c.style.transform = `translateY(${(1 - e) * 0.6}em)`; }));
    },
    charPop(sc, el, at, o = {}) { // 逐字弹出（MG/卡通）
      const chs = splitChars(el), gap = o.gap ?? Math.min(.06, 1.2 / Math.max(chs.length, 1));
      chs.forEach((c, i) => addAnim(sc, c, at + i * gap, o.dur || .55, (c, p) => { c.style.opacity = clamp(p * 4); c.style.transform = `scale(${E.back(p)}) rotate(${(1 - E.out3(p)) * (i % 2 ? 14 : -14)}deg)`; }));
    },
    maskUp(sc, el, at, o = {}) { // 行遮罩上推（编辑/高级感）
      const lines = splitLines(el);
      lines.forEach((l, i) => addAnim(sc, l, at + i * (o.gap || .12), o.dur || .9, (l, p) => { l.style.transform = `translateY(${(1 - E.out5(p)) * 110}%)`; }));
    },
    punch(sc, el, at, o = {}) { // 大字砸入（快节奏）
      addAnim(sc, el, at, o.dur || .45, (el, p, lt) => {
        const e = E.out5(p); el.style.opacity = clamp(p * 5);
        const shake = p < 1 ? 0 : Math.max(0, .15 - (lt - (o.dur || .45))) * 40 * Math.sin(lt * 90);
        el.style.transform = `scale(${lerp(o.from || 2.4, 1, e)}) translateX(${shake}px)`;
      });
    },
    typewriter(sc, el, at, o = {}) {
      const chs = splitChars(el), cps = o.cps || 16;
      const caret = h("span", "caret", "▍"); el.appendChild(caret);
      addAnim(sc, el, at, chs.length / cps + 1.5, (el, p, lt) => {
        const n = Math.floor(lt * cps); chs.forEach((c, i) => c.style.opacity = i < n ? 1 : 0);
        caret.style.opacity = (Math.floor(lt * 2.2) % 2 === 0 || n < chs.length) ? 1 : 0;
      });
    },
    glitch(sc, el, at, o = {}) { // 乱码解码 + RGB 分离
      const chs = splitChars(el), pool = "▓▒░#@$%&*01ABCDEFXYZ<>/\\";
      const orig = chs.map(c => c.textContent);
      addAnim(sc, el, at, o.dur || 1.0, (el, p, lt) => {
        const f = Math.floor(lt * 30);
        chs.forEach((c, i) => {
          const done = p >= (i + 1) / (chs.length + 2) + .1;
          c.textContent = done ? orig[i] : pool[Math.floor(rand(f * 31 + i) * pool.length)];
          c.style.opacity = p > i / chs.length * .5 ? 1 : 0;
        });
        const k = (1 - p) * 10 + (rand(f) > .9 ? 6 : 0);
        el.style.textShadow = `${k}px 0 var(--glitchA, #ff004c), ${-k}px 0 var(--glitchB, #00e5ff)`;
        el.style.transform = `translateX(${rand(f + 7) > .85 ? (rand(f) - .5) * 30 : 0}px)`;
      });
    },
    slideHard(sc, el, at, o = {}) { // 硬切滑入（新粗野）
      addAnim(sc, el, at, o.dur || .35, (el, p) => { const e = E.step(5)(p); el.style.opacity = p > 0 ? 1 : 0; el.style.transform = `translateX(${(1 - e) * -120}px)`; });
    },
    none(sc, el, at) { addAnim(sc, el, at, .01, (el, p) => el.style.opacity = p > 0 ? 1 : 0); },
  };

  // ---------- 图片 / 媒体入场预设 ----------
  const IMAGE = {
    floatUp(sc, el, at, o = {}) {
      addAnim(sc, el, at, o.dur || 1.0, (el, p, lt) => { const e = E.out5(p); el.style.opacity = e; el.style.transform = `translateY(${(1 - e) * 140 + Math.sin(lt * 1.2) * 6}px) scale(${lerp(.96, 1, e)})`; }, { hold: true });
    },
    tilt3d(sc, el, at, o = {}) { // 透视立起来（SaaS 发布会常见）
      addAnim(sc, el, at, o.dur || 1.4, (el, p, lt) => { const e = E.out5(p); el.style.opacity = clamp(p * 2.5); el.style.transform = `perspective(1800px) rotateX(${lerp(38, 10, e) - Math.min(lt * .6, 4)}deg) rotateY(${lerp(-18, -6, e)}deg) translateY(${(1 - e) * 160}px) scale(${lerp(.86, 1, e)})`; }, { hold: true });
    },
    zoomOut(sc, el, at, o = {}) {
      addAnim(sc, el, at, o.dur || 1.2, (el, p, lt) => { const e = E.out3(p); el.style.opacity = e; el.style.filter = `blur(${(1 - e) * 14}px)`; el.style.transform = `scale(${lerp(1.25, 1, e) + lt * .006})`; }, { hold: true });
    },
    popBounce(sc, el, at, o = {}) {
      addAnim(sc, el, at, o.dur || .8, (el, p, lt) => { el.style.opacity = clamp(p * 4); el.style.transform = `scale(${E.back(p)}) rotate(${(1 - E.out3(p)) * -8 + Math.sin(lt * 1.6) * .6}deg)`; }, { hold: true });
    },
    wipe(sc, el, at, o = {}) {
      addAnim(sc, el, at, o.dur || .9, (el, p, lt) => { const e = E.io3(p); el.style.opacity = 1; el.style.clipPath = `inset(0 ${(1 - e) * 100}% 0 0)`; el.style.transform = `scale(${1.04 - e * .04 + lt * .004})`; }, { hold: true });
    },
    glitch(sc, el, at, o = {}) {
      addAnim(sc, el, at, o.dur || .8, (el, p, lt) => {
        const f = Math.floor(lt * 30), on = p < 1 && rand(f) > .4;
        el.style.opacity = p > 0 ? 1 : 0;
        el.style.clipPath = on ? `inset(${rand(f + 1) * 60}% 0 ${rand(f + 2) * 30}% 0)` : "none";
        el.style.transform = `translateX(${on ? (rand(f + 3) - .5) * 60 : 0}px)`;
        el.style.filter = on ? `hue-rotate(${rand(f) * 180}deg) saturate(2)` : "none";
      }, { hold: true });
    },
    slideHard(sc, el, at, o = {}) {
      addAnim(sc, el, at, o.dur || .4, (el, p) => { const e = E.step(6)(p); el.style.opacity = p > 0 ? 1 : 0; el.style.transform = `translate(${(1 - e) * 200}px, ${(1 - e) * -40}px)`; }, { hold: true });
    },
  };

  // ---------- 转场预设（out = 上一场，in = 下一场，p 0..1） ----------
  const fx = document.getElementById("fx");
  const TRANS = {
    cut(o, i, p) { o.style.opacity = p < .5 ? 1 : 0; i.style.opacity = p < .5 ? 0 : 1; },
    fade(o, i, p) { o.style.opacity = 1 - p; i.style.opacity = p; },
    blur(o, i, p) { const e = E.io3(p); o.style.opacity = 1 - e; o.style.filter = `blur(${e * 24}px)`; i.style.opacity = e; i.style.filter = `blur(${(1 - e) * 24}px)`; },
    push(o, i, p) { const e = E.io3(p); o.style.transform = `translateX(${-e * 100}%)`; i.style.transform = `translateX(${(1 - e) * 100}%)`; i.style.opacity = 1; },
    pushUp(o, i, p) { const e = E.io3(p); o.style.transform = `translateY(${-e * 100}%)`; i.style.transform = `translateY(${(1 - e) * 100}%)`; i.style.opacity = 1; },
    zoom(o, i, p) { const e = E.io3(p); o.style.transform = `scale(${1 + e * .6})`; o.style.opacity = 1 - e; i.style.transform = `scale(${lerp(.75, 1, e)})`; i.style.opacity = e; },
    circle(o, i, p) { const e = E.io3(p); i.style.opacity = 1; i.style.clipPath = `circle(${e * 75}% at 50% 50%)`; },
    // 品牌色色块扫过（MG / 扁平风）
    shapeWipe(o, i, p) {
      const e = E.io3(p);
      fx.style.display = "block"; fx.className = "fx-wipe";
      fx.style.transform = `translateX(${lerp(-110, 110, e)}%) skewX(-12deg)`;
      o.style.opacity = e < .5 ? 1 : 0; i.style.opacity = e < .5 ? 0 : 1;
    },
    flash(o, i, p) { fx.style.display = "block"; fx.className = "fx-flash"; fx.style.opacity = 1 - Math.abs(p - .5) * 2; o.style.opacity = p < .5 ? 1 : 0; i.style.opacity = p < .5 ? 0 : 1; },
    glitchCut(o, i, p) {
      const f = Math.floor(p * 12), a = p < .5 ? o : i, b = p < .5 ? i : o;
      a.style.opacity = 1; b.style.opacity = 0;
      a.style.transform = `translateX(${(rand(f) - .5) * 80}px)`;
      a.style.clipPath = `inset(${rand(f + 1) * 40}% 0 ${rand(f + 2) * 40}% 0)`;
      a.style.filter = `hue-rotate(${rand(f + 3) * 90}deg)`;
      fx.style.display = "block"; fx.className = "fx-scan"; fx.style.opacity = 1 - Math.abs(p - .5) * 2;
    },
    stripes(o, i, p) { // 多条色带依次扫过
      fx.style.display = "block"; fx.className = "fx-stripes";
      [...fx.children].forEach((c, k) => { const e = E.io3(clamp(p * 1.6 - k * .12)); c.style.transform = `translateX(${lerp(-105, 105, e)}%)`; });
      o.style.opacity = p < .5 ? 1 : 0; i.style.opacity = p < .5 ? 0 : 1;
    },
  };
  // 色带元素
  for (let k = 0; k < 4; k++) fx.appendChild(h("i"));

  window.PV_TEXT = TEXT; window.PV_IMAGE = IMAGE; window.PV_TRANS = TRANS;

  // ---------- 场景布局 ----------
  const media = (src, frame) => {
    const wrap = h("div", "media frame-" + (frame || "none"));
    if (frame === "browser") wrap.appendChild(h("div", "bar", "<i></i><i></i><i></i><span></span>"));
    if (frame === "phone") wrap.appendChild(h("div", "notch"));
    const box = h("div", "screen"); const img = h("img"); img.src = src; box.appendChild(img); wrap.appendChild(box);
    return wrap;
  };
  const logoEl = (cls = "logo") => {
    const b = P.brand, w = h("div", cls);
    if (b.logoSvg) w.innerHTML = b.logoSvg; else if (b.logo) { const im = h("img"); im.src = b.logo; w.appendChild(im); }
    else w.appendChild(h("div", "logo-text", esc(b.name)));
    return w;
  };
  const textBlock = (sc, d, cls = "copy") => {
    const box = h("div", cls);
    if (d.kicker) box.appendChild(h("div", "kicker", rich(d.kicker)));
    if (d.title) box.appendChild(h("div", "title", rich(d.title)));
    if (d.sub) box.appendChild(h("div", "sub", rich(d.sub)));
    return box;
  };
  // 每种场景：建 DOM + 安排入场
  const LAYOUT = {
    logo(sc, d, el) {
      const lg = logoEl(); el.appendChild(lg);
      const tl = h("div", "tagline", rich(d.tagline || P.brand.slogan || "")); el.appendChild(tl);
      (S.logoIn || IMAGE.popBounce)(sc, lg, .2);
      S.text.sub(sc, tl, .9);
    },
    slogan(sc, d, el) {
      const tb = textBlock(sc, d, "copy center"); el.appendChild(tb);
      animCopy(sc, tb, .15);
    },
    feature(sc, d, el, idx) {
      const side = d.side || (idx % 2 ? "right" : "left");
      el.classList.add("side-" + side);
      const tb = textBlock(sc, d); el.appendChild(tb);
      if (d.bullets) { const ul = h("ul", "bullets"); d.bullets.forEach(b => ul.appendChild(h("li", "", rich(b)))); tb.appendChild(ul); }
      const m = media(d.image, d.frame || (P.W >= P.H ? "browser" : "phone")); el.appendChild(m);
      animCopy(sc, tb, .1);
      if (d.bullets) [...tb.querySelectorAll("li")].forEach((li, k) => S.text.sub(sc, li, 1.0 + k * .25));
      S.image(sc, m, .35);
      if (d.focus) addAnim(sc, m.querySelector("img"), 1.4, Math.max(sc.dur - 1.6, 1), (img, p) => { // 慢推镜到重点区域
        const e = E.io3(p), [fx_, fy, z] = d.focus; img.style.transformOrigin = `${fx_ * 100}% ${fy * 100}%`; img.style.transform = `scale(${lerp(1, z || 1.5, e)})`;
      }, { keep: true });
    },
    cards(sc, d, el) {
      const tb = textBlock(sc, d, "copy center top"); el.appendChild(tb); animCopy(sc, tb, .1);
      const g = h("div", "grid n" + d.items.length); el.appendChild(g);
      d.items.forEach((it, k) => {
        const c = h("div", "card");
        if (it.image) { const im = h("div", "card-img"); im.style.backgroundImage = `url("${it.image}")`; c.appendChild(im); }
        else if (it.iconSvg) c.appendChild(h("div", "card-icon", it.iconSvg));
        else c.appendChild(h("div", "card-num", String(k + 1).padStart(2, "0")));
        c.appendChild(h("div", "card-label", rich(it.label)));
        if (it.desc) c.appendChild(h("div", "card-desc", rich(it.desc)));
        g.appendChild(c); (S.card || IMAGE.popBounce)(sc, c, .6 + k * (S.cardGap || .14));
      });
    },
    stats(sc, d, el) {
      const tb = textBlock(sc, d, "copy center top"); el.appendChild(tb); animCopy(sc, tb, .1);
      const g = h("div", "stats n" + d.items.length); el.appendChild(g);
      d.items.forEach((it, k) => {
        const c = h("div", "stat"), v = h("div", "stat-v"), l = h("div", "stat-l", rich(it.label));
        c.append(v, l); g.appendChild(c);
        const m = String(it.value).match(/^([^\d]*)([\d.]+)(.*)$/) || ["", "", it.value, ""];
        const num = parseFloat(m[2]), dec = (m[2].split(".")[1] || "").length;
        (S.card || IMAGE.floatUp)(sc, c, .5 + k * .18);
        addAnim(sc, v, .6 + k * .18, 1.6, (v, p) => { v.innerHTML = esc(m[1]) + (isNaN(num) ? esc(m[2]) : (num * E.out5(p)).toFixed(dec)) + `<small>${esc(m[3])}</small>`; });
      });
    },
    // 标签流：danmaku(弹幕飞过) / cloud(散点弹出) / marquee(整行滚动)
    tags(sc, d, el) {
      const tb = textBlock(sc, d, "copy center mid"); el.appendChild(tb); animCopy(sc, tb, .2);
      const mode = d.mode || S.tagMode || "cloud", box = h("div", "tagfield mode-" + mode); el.appendChild(box);
      const lanes = mode === "danmaku" ? (P.W >= P.H ? 9 : 14) : 0;
      d.items.forEach((txt, k) => {
        const t = h("span", "tag" + (k % 3 === 0 ? " tag-a" : k % 3 === 1 ? " tag-b" : ""), rich(txt)); box.appendChild(t);
        if (mode === "danmaku") {
          // 一部分弹幕开场就已经在屏幕上，避免空屏；速度按字数略有差异，像真弹幕
          const lane = k % lanes, y = 5 + lane * (90 / lanes), v = P.W * (.2 + rand(k) * .12);
          const x0 = P.W * (rand(k + 9) * 1.6 - .2) + Math.floor(k / lanes) * P.W * .5;
          t.style.top = y + "%";
          addAnim(sc, t, 0, sc.dur, (t, p, lt) => { t.style.opacity = 1; t.style.transform = `translateX(${x0 - lt * v}px)`; });
        } else if (mode === "marquee") {
          t.style.top = (8 + (k % 6) * 15) + "%";
          addAnim(sc, t, 0, sc.dur, (t, p, lt) => { const dir = (k % 6) % 2 ? 1 : -1, x = (Math.floor(k / 6) * 380 + lt * 160 * dir) % (P.W + 400); t.style.opacity = 1; t.style.transform = `translateX(${dir > 0 ? x - 400 : P.W + x}px)`; });
        } else {
          // 均匀分布在两圈椭圆上（内外交替），避免互相压住，也避开中间的标题
          const n = d.items.length, ang = (k / n) * Math.PI * 2 + (rand(k * 3) - .5) * .25 - Math.PI / 2, ring = k % 2 ? .40 : .31;
          t.style.left = (50 + Math.cos(ang) * ring * 100 * (P.W >= P.H ? .98 : .9)) + "%"; t.style.top = (50 + Math.sin(ang) * ring * 100 * (P.W >= P.H ? 1.05 : .75)) + "%";
          addAnim(sc, t, .4 + k * .09, .6, (t, p, lt) => { t.style.opacity = clamp(p * 3); t.style.transform = `translate(-50%,-50%) scale(${E.back(p)}) translateY(${Math.sin(lt * 1.3 + k) * 6}px)`; });
        }
      });
    },
    gallery(sc, d, el) { // 多张截图墙，缓慢平移
      const tb = textBlock(sc, d, "copy center mid over"); el.appendChild(tb);
      const wall = h("div", "wall"); el.insertBefore(wall, tb);
      const cols = P.W >= P.H ? 4 : 3;
      for (let c = 0; c < cols; c++) {
        const col = h("div", "wcol"); wall.appendChild(col);
        for (let r = 0; r < 4; r++) { const im = h("div", "wimg"); im.style.backgroundImage = `url("${d.images[(c * 4 + r) % d.images.length]}")`; col.appendChild(im); }
        addAnim(sc, col, 0, sc.dur, (col, p, lt) => { col.style.transform = `translateY(${(c % 2 ? -1 : 1) * (lt * 40) - (c % 2 ? 0 : 400)}px)`; });
      }
      addAnim(sc, wall, 0, .8, (w, p) => w.style.opacity = E.out3(p));
      animCopy(sc, tb, .5);
    },
    end(sc, d, el) {
      const lg = logoEl("logo small"); el.appendChild(lg);
      const tb = textBlock(sc, { title: d.title || P.brand.slogan, sub: d.sub }, "copy center"); el.appendChild(tb);
      if (d.cta) { const b = h("div", "cta", rich(d.cta)); el.appendChild(b); IMAGE.popBounce(sc, b, 1.3); }
      (S.logoIn || IMAGE.popBounce)(sc, lg, .1);
      animCopy(sc, tb, .5);
    },
  };
  function animCopy(sc, box, at) {
    const k = box.querySelector(".kicker"), t = box.querySelector(".title"), s = box.querySelector(".sub");
    let a = at;
    if (k) { S.text.kicker(sc, k, a); a += .25; }
    if (t) { S.text.title(sc, t, a); a += .45; }
    if (s) S.text.sub(sc, s, a + .1);
  }

  // ---------- 时间轴：场景时长由旁白长度决定 ----------
  const TD = S.transitionDur ?? .6;
  const MIN = { logo: 3.2, slogan: 3.0, feature: 4.5, cards: 4.5, stats: 4.0, tags: 4.2, gallery: 4.0, end: 4.0 };
  {
    let t = 0;
    P.scenes.forEach((d, i) => {
      const lead = i ? TD + .1 : .5, vd = d.voice?.dur || 0;
      d.dur = Math.max((d.min || MIN[d.type] || 3.5) * (S.pace || 1), vd ? lead + vd + .35 + (i < P.scenes.length - 1 ? TD : .8) : 0);
      d.start = t;
      if (d.voice) { d.voice.start = t + lead; (d.voice.cues || []).forEach(c => { c.start += d.voice.start; c.end += d.voice.start; }); }
      t += d.dur - TD;
    });
    const last = P.scenes[P.scenes.length - 1];
    P.duration = +(last.start + last.dur).toFixed(3);
    window.PV_TIMELINE = { duration: P.duration, fps: P.fps, scenes: P.scenes.map(d => ({ type: d.type, start: d.start, dur: d.dur, voice: d.voice ? { file: d.voice.file, start: d.voice.start, dur: d.voice.dur } : null })) };
  }

  // ---------- 搭场景 ----------
  const scenes = P.scenes.map((d, idx) => {
    const el = h("section", `scene t-${d.type}` + (d.theme ? " theme-" + d.theme : ""));
    el.style.opacity = 0; stage.appendChild(el);
    const sc = { idx, el, start: d.start, dur: d.dur, d };
    (LAYOUT[d.type] || LAYOUT.slogan)(sc, d, el, idx);
    if (S.sceneHook) S.sceneHook(sc, d, el, { h, addAnim, TEXT, IMAGE });
    return sc;
  });
  window.DURATION = P.duration;

  // 背景 / 装饰层（风格自带）
  const bg = document.getElementById("bg");
  const bgUpdate = S.bg ? S.bg(bg, { h, P, rand }) : null;

  // 字幕
  const cap = document.getElementById("cap");
  const cues = [];
  if (P.captions) P.scenes.forEach(d => (d.voice?.cues || []).forEach(c => cues.push(c)));

  // 预设 / 状态复位：每帧先把所有动画元素放回初始态，再按时间推进（保证可任意 seek）
  const touched = new Set(anims.map(a => a.el));
  function reset(el) { el.style.opacity = 0; el.style.transform = ""; el.style.filter = ""; el.style.clipPath = ""; }

  function seek(t) {
    fx.style.display = "none"; fx.style.opacity = ""; fx.style.transform = "";
    for (const sc of scenes) {
      const vis = t >= sc.start - .0001 && t < sc.start + sc.dur;
      sc.el.style.display = vis ? "" : "none";
      sc.el.style.opacity = vis ? 1 : 0; sc.el.style.transform = ""; sc.el.style.filter = ""; sc.el.style.clipPath = "";
    }
    for (const a of anims) {
      const sc = scenes[a.scene.idx];
      if (sc.el.style.display === "none") continue;
      const lt = t - sc.start - a.at;
      if (lt < 0) { if (a.extra.keep) a.el.style.transform = ""; else reset(a.el); continue; }
      if (!a.extra.keep) a.el.style.opacity = 1;
      a.fn(a.el, clamp(lt / a.dur), lt, a.extra);
    }
    // 转场：第 i 场最后 TD 秒和第 i+1 场开头重叠
    for (let i = 0; i < scenes.length - 1; i++) {
      const a = scenes[i], b = scenes[i + 1], s = b.start, e = a.start + a.dur;
      if (t >= s && t < e) {
        const name = b.d.transition || S.transition;
        (TRANS[name] || TRANS.fade)(a.el, b.el, clamp((t - s) / (e - s)));
      }
    }
    // 最后一场收尾淡出
    const last = scenes[scenes.length - 1];
    if (t > P.duration - .5) last.el.style.opacity = clamp((P.duration - t) / .5);
    if (bgUpdate) bgUpdate(t);
    if (cap) {
      const c = cues.find(c => t >= c.start && t < c.end);
      cap.innerHTML = c ? `<span>${esc(c.text)}</span>` : ""; cap.style.opacity = c ? 1 : 0;
    }
  }
  window.seek = seek;
  // 浏览器里直接打开时：自动播放预览
  const q = new URLSearchParams(location.search);
  if (!window.__PV_RENDER__) {
    if (q.has("t")) seek(parseFloat(q.get("t")));
    else {
      const t0 = performance.now();
      const audio = document.getElementById("vo"); if (audio) audio.play().catch(() => {});
      const loop = () => { const t = ((performance.now() - t0) / 1000) % P.duration; seek(t); requestAnimationFrame(loop); };
      loop();
    }
  }
})();
