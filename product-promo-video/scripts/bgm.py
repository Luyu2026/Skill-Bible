#!/usr/bin/env python3
"""合成一段临时配乐（无版权问题，但只是「能用」级别）。正式片请换授权曲：brief 里写 "bgm": "/path/to/music.mp3"。

用法: python3 bgm.py <mood> <秒数> <out.wav> [--bpm 110]
mood: ambient（发布会/编辑）| tech（SaaS）| beat（快节奏/粗野）| bouncy（MG/便当）| synth（赛博）
"""
import sys, wave
import numpy as np

SR = 44100
MOODS = {
    #        bpm  调式        和弦级数(半音, 相对主音)                       乐器
    "ambient": (84, 57, [[0, 4, 7, 11], [-3, 0, 4, 7], [5, 9, 12, 16], [7, 11, 14, 17]], dict(pad=1, arp=.35, kick=0, hat=0, bass=.4)),
    "tech":    (104, 57, [[0, 3, 7, 10], [-4, 0, 3, 7], [-7, -3, 0, 5], [-2, 2, 5, 9]], dict(pad=.8, arp=.55, kick=.5, hat=.25, bass=.6)),
    "beat":    (124, 52, [[0, 3, 7], [0, 3, 7], [-4, 0, 3], [-2, 2, 5]], dict(pad=.35, arp=.4, kick=1, hat=.5, bass=.9, clap=.6)),
    "bouncy":  (116, 60, [[0, 4, 7], [-5, -1, 2], [-3, 0, 4], [-7, -3, 0]], dict(pad=.45, arp=.75, kick=.65, hat=.35, bass=.6, clap=.35)),
    "synth":   (100, 50, [[0, 3, 7, 10], [-4, 0, 3, 7], [-2, 2, 5, 9], [-5, -1, 2, 5]], dict(pad=.7, arp=.7, kick=.85, hat=.4, bass=.9, clap=.45)),
}

def hz(m): return 440.0 * 2 ** ((m - 69) / 12)

def env(n, a, r):
    e = np.ones(n); a, r = int(a * SR), int(r * SR)
    if a: e[:a] = np.linspace(0, 1, a)
    if r: e[-r:] *= np.linspace(1, 0, r)
    return e

def tone(f, dur, harm=4, bright=1.0, detune=0.0):
    t = np.arange(int(dur * SR)) / SR
    s = np.zeros_like(t)
    for k in range(1, harm + 1):
        for d in ((-detune, detune) if detune else (0,)):
            s += np.sin(2 * np.pi * f * k * (1 + d) * t) * (bright ** (k - 1)) / k
    return s / max(1, harm)

def main():
    mood, secs, out = sys.argv[1], float(sys.argv[2]), sys.argv[3]
    bpm, root, prog, mix = MOODS.get(mood, MOODS["ambient"])
    if "--bpm" in sys.argv: bpm = float(sys.argv[sys.argv.index("--bpm") + 1])
    beat = 60 / bpm; bar = beat * 4
    n = int((secs + 1) * SR)
    L = np.zeros(n); R = np.zeros(n)
    rng = np.random.default_rng(7)

    def put(sig, at, pan=0.0, g=1.0):
        i = int(at * SR)
        if i >= n: return
        sig = sig[: n - i] * g
        L[i:i + len(sig)] += sig * (1 - pan) ; R[i:i + len(sig)] += sig * (1 + pan)

    bars = int(secs / bar) + 2
    for b in range(bars):
        chord = prog[b % len(prog)]; t0 = b * bar
        if mix.get("pad"):
            for j, c in enumerate(chord):
                s = tone(hz(root + 12 + c), bar + .4, harm=5, bright=.55, detune=.003) * env(int((bar + .4) * SR), .5, .6)
                put(s, t0, pan=(j - 1.5) * .25, g=.10 * mix["pad"])
        if mix.get("bass"):
            for k in range(4 if mood != "ambient" else 1):
                d = beat * (1 if mood != "ambient" else 4) * .9
                s = tone(hz(root - 12 + chord[0]), d, harm=3, bright=.4) * env(int(d * SR), .01, d * .6)
                put(s, t0 + k * beat, g=.28 * mix["bass"])
        if mix.get("arp"):
            step = beat / (2 if mood in ("ambient",) else 4 if mood == "synth" else 2)
            seq = chord + [c + 12 for c in chord]
            for k in range(int(bar / step)):
                note = seq[(k * (3 if mood == "bouncy" else 1)) % len(seq)]
                d = step * 1.8
                e = np.exp(-np.arange(int(d * SR)) / SR * (9 if mood != "ambient" else 4))
                s = tone(hz(root + 24 + note), d, harm=3 if mood != "synth" else 6, bright=.5 if mood != "synth" else .8) * e
                put(s, t0 + k * step, pan=.4 * np.sin(k), g=.12 * mix["arp"])
        for k in range(4):
            tb = t0 + k * beat
            if mix.get("kick") and (mood != "tech" or k % 2 == 0):
                d = .35; t = np.arange(int(d * SR)) / SR
                f = 45 + 90 * np.exp(-t * 28)
                put(np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 9), tb, g=.55 * mix["kick"])
            if mix.get("hat"):
                for off in (beat / 2,) if mood != "synth" else (beat / 4, beat * 3 / 4):
                    d = .06; noise = np.diff(rng.standard_normal(int(d * SR) + 1))
                    put(noise * np.exp(-np.arange(len(noise)) / SR * 70), tb + off, pan=.3, g=.05 * mix["hat"])
            if mix.get("clap") and k in (1, 3):
                d = .2; noise = rng.standard_normal(int(d * SR))
                noise = np.convolve(noise, np.ones(6) / 6, "same") - np.convolve(noise, np.ones(40) / 40, "same")
                put(noise * np.exp(-np.arange(len(noise)) / SR * 22), tb, g=.22 * mix["clap"])

    st = np.stack([L, R], 1)[: int(secs * SR)]
    st /= (np.abs(st).max() + 1e-9); st = np.tanh(st * 1.6) / np.tanh(1.6)
    fade = int(1.5 * SR); st[:int(.3 * SR)] *= np.linspace(0, 1, int(.3 * SR))[:, None]; st[-fade:] *= np.linspace(1, 0, fade)[:, None]
    pcm = (st * 0.7 * 32767).astype(np.int16)
    with wave.open(out, "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())
    print(f"配乐 {mood} {bpm:.0f}bpm {secs:.1f}s → {out}")

if __name__ == "__main__":
    main()
