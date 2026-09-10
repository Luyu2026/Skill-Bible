#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Strict, offline SRT time transformation. Python 3.9+."""
import argparse
from fractions import Fraction
import json
from pathlib import Path
import re
import sys

STAMP = r"[0-9]{2,}:[0-5][0-9]:[0-5][0-9],[0-9]{3}"
TIMELINE = re.compile(rf"({STAMP}) --> ({STAMP})")


def milliseconds(value):
    if not re.fullmatch(STAMP, value):
        raise ValueError("Expected HH:MM:SS,mmm with valid minutes and seconds")
    h, m, tail = value.split(":")
    s, ms = tail.split(",")
    return ((int(h) * 60 + int(m)) * 60 + int(s)) * 1000 + int(ms)


def stamp(value):
    h, value = divmod(value, 3600000)
    m, value = divmod(value, 60000)
    s, ms = divmod(value, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def rounded(value):
    magnitude = abs(value)
    result = (2 * magnitude.numerator + magnitude.denominator) // (2 * magnitude.denominator)
    return result if value >= 0 else -result


def parse(text):
    text = text.removeprefix("\ufeff").replace("\r\n", "\n").replace("\r", "\n").strip("\n")
    if not text.strip():
        raise ValueError("Empty subtitle file")
    cues, seen = [], set()
    for pos, block in enumerate(re.split(r"\n[ \t]*\n(?:[ \t]*\n)*", text), 1):
        lines = block.split("\n")
        if len(lines) < 3 or not re.fullmatch(r"[0-9]+", lines[0]):
            raise ValueError(f"Invalid SRT block {pos}: index, time line and text required")
        number = int(lines[0])
        if number in seen:
            raise ValueError(f"Duplicate index in block {pos}")
        seen.add(number)
        match = TIMELINE.fullmatch(lines[1])
        if not match or not any(line.strip() for line in lines[2:]):
            raise ValueError(f"Invalid time line or empty text in block {pos}")
        # Reject a missing block separator instead of swallowing another cue as text.
        if any(TIMELINE.fullmatch(line) for line in lines[2:]):
            raise ValueError(f"Embedded time line in block {pos}; check blank separators")
        start, end = map(milliseconds, match.groups())
        if end <= start:
            raise ValueError(f"Non-positive duration in block {pos}")
        cues.append({"index": lines[0], "start": start, "end": end, "text": "\n".join(lines[2:])})
    return cues


def diagnostics(cues, prefix):
    warnings = []
    if any(b["start"] < a["start"] for a, b in zip(cues, cues[1:])):
        warnings.append(prefix + "_out_of_order")
    latest_end = -1
    for cue in sorted(cues, key=lambda c: c["start"]):
        if cue["start"] < latest_end:
            warnings.append(prefix + "_overlap")
            break
        latest_end = max(latest_end, cue["end"])
    return warnings


def mapping(args):
    if args.offset_ms is not None:
        return Fraction(1), Fraction(args.offset_ms), None
    if len(args.anchor) != 2:
        raise ValueError("Linear correction requires exactly two --anchor pairs")
    anchors = []
    for pair in args.anchor:
        parts = pair.split("=")
        if len(parts) != 2:
            raise ValueError("Anchor must be source=target")
        anchors.append(tuple(map(milliseconds, parts)))
    (s1, t1), (s2, t2) = anchors
    if s2 <= s1 or t2 <= t1:
        raise ValueError("Source and target anchors must both strictly increase")
    scale = Fraction(t2 - t1, s2 - s1)
    return scale, Fraction(t1) - scale * s1, anchors


def transform(cues, scale, offset, anchors, negative):
    result, changes = [], []
    clipped = dropped = extrapolated = 0
    for cue in cues:
        start = rounded(scale * cue["start"] + offset)
        end = rounded(scale * cue["end"] + offset)
        action = "retimed"
        if anchors and (cue["start"] < anchors[0][0] or cue["end"] > anchors[1][0]):
            extrapolated += 1
        if start < 0 and negative == "error":
            raise ValueError(f"Negative start at index {cue['index']}; explicit clipping or new timing required")
        if negative == "clip" and end <= 0:
            dropped += 1
            action = "dropped"
        else:
            if start < 0:
                start = 0
                clipped += 1
                action = "clipped"
            if end <= start:
                raise ValueError(f"Duration collapsed after rounding at index {cue['index']}")
            result.append(dict(cue, start=start, end=end))
        changes.append({"index": cue["index"], "before": [stamp(cue["start"]), stamp(cue["end"])],
                        "after": None if action == "dropped" else [stamp(start), stamp(end)], "action": action})
    warnings = diagnostics(cues, "input") + diagnostics(result, "output")
    if clipped or dropped:
        warnings.append("negative_time_clipping")
    if extrapolated:
        warnings.append("outside_anchor_range")
    report = {"mode": "linear" if anchors else "offset", "scale": str(scale), "offset_ms": str(offset),
              "anchors_ms": anchors, "negative_policy": negative,
              "input_cues": len(cues), "output_cues": len(result), "clipped_cues": clipped,
              "dropped_cues": dropped, "extrapolated_cues": extrapolated, "warnings": warnings, "changes": changes}
    return result, report


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--offset-ms", type=int)
    group.add_argument("--anchor", action="append")
    parser.add_argument("--negative", choices=["error", "clip"], default="error")
    parser.add_argument("--encoding", default="utf-8-sig")
    parser.add_argument("--out-dir", required=True, type=Path)
    args = parser.parse_args(argv)
    created = False
    try:
        scale, offset, anchors = mapping(args)
        cues = parse(args.input.read_text(encoding=args.encoding))
        output, report = transform(cues, scale, offset, anchors, args.negative)
        payload = "\n\n".join(f"{c['index']}\n{stamp(c['start'])} --> {stamp(c['end'])}\n{c['text']}" for c in output)
        payload += "\n" if output else ""
        args.out_dir.mkdir(parents=False, exist_ok=False)
        created = True
        with (args.out_dir / "corrected.srt").open("w", encoding="utf-8", newline="\n") as stream:
            stream.write(payload)
        (args.out_dir / "report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(json.dumps({"status": "converted", "input_cues": len(cues), "output_cues": len(output), "warnings": report["warnings"]}))
        return 0
    except (OSError, ValueError, LookupError) as exc:
        if created:
            for filename in ("corrected.srt", "report.json"):
                (args.out_dir / filename).unlink(missing_ok=True)
            args.out_dir.rmdir()
        print(json.dumps({"status": "error", "message": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
