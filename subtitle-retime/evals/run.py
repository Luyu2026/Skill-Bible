#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Run synthetic examples in an isolated temporary directory; no network."""
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/retime.py"
spec = importlib.util.spec_from_file_location("retime", SCRIPT)
retime = importlib.util.module_from_spec(spec)
spec.loader.exec_module(retime)


def run():
    cases = json.loads((ROOT / "evals/evals.json").read_text(encoding="utf-8"))["cases"]
    for case in cases:
        with tempfile.TemporaryDirectory() as temp:
            cwd = Path(temp)
            source = cwd / "input.srt"
            original = case["input"].encode(case.get("encoding", "utf-8"))
            source.write_bytes(original)
            result = subprocess.run([sys.executable, str(SCRIPT), "input.srt", *case["args"], "--out-dir", "result"], cwd=cwd, capture_output=True, text=True)
            assert result.returncode == case["exit"], (case["id"], result.stderr)
            assert source.read_bytes() == original, "Input changed"
            assert not (cwd / "SHOULD_NOT_EXIST").exists()
            out = cwd / "result"
            if case["exit"]:
                assert not out.exists(), "Failed conversion created output"
                assert case["error"] in json.loads(result.stderr)["message"]
            else:
                report = json.loads((out / "report.json").read_text(encoding="utf-8"))
                assert [report[k] for k in ("input_cues", "output_cues", "dropped_cues", "clipped_cues")] == case["counts"]
                assert report["input_cues"] == report["output_cues"] + report["dropped_cues"]
                assert [c["after"] for c in report["changes"]] == case["times"]
                assert report["warnings"] == case.get("warnings", [])
                raw = (out / "corrected.srt").read_bytes()
                assert b"\r" not in raw and not raw.startswith(b"\xef\xbb\xbf")
                parsed = retime.parse(raw.decode("utf-8")) if raw else []
                before = retime.parse(case["input"])
                kept = [c for c, change in zip(before, report["changes"]) if change["action"] != "dropped"]
                assert [(c["index"], c["text"]) for c in kept] == [(c["index"], c["text"]) for c in parsed]
                # A rerun must refuse to overwrite the actual deliverables.
                saved = {f.name: f.read_bytes() for f in out.iterdir()}
                retry = subprocess.run([sys.executable, str(SCRIPT), "input.srt", *case["args"], "--out-dir", "result"], cwd=cwd, capture_output=True)
                assert retry.returncode == 2
                assert saved == {f.name: f.read_bytes() for f in out.iterdir()}
            print("PASS " + case["id"])
    print(f"{len(cases)} executable scenarios passed; interaction cases require separate review.")


if __name__ == "__main__":
    run()
