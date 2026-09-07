#!/usr/bin/env python3
"""Emit a minimal, opt-in Skill-Bible run receipt.

The helper deliberately never reads prompts, documents, output, file paths,
account names, or environment variables other than its explicit configuration.
Failure is always non-blocking: a Skill must work without telemetry.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path
from urllib import request


ALLOWED_EVENTS = {"started", "completed", "failed", "feedback"}
ALLOWED_AGENTS = {"codex", "claude", "workbuddy", "other", "unknown"}
ALLOWED_BUCKETS = {"under-1m", "1-5m", "5-15m", "15m-plus", "unknown"}
ALLOWED_FEEDBACK = {"helpful", "partly_helpful", "not_helpful"}


def load_config(path: str) -> dict:
    config_path = Path(os.path.expanduser(path))
    if not config_path.is_file():
        return {}
    try:
        return json.loads(config_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}


def build_event(args: argparse.Namespace, config: dict) -> dict:
    event = {
        "event_id": str(uuid.uuid4()),
        "occurred_at": datetime.now(timezone.utc).isoformat(),
        "skill_id": args.skill_id,
        "skill_version": args.skill_version,
        "event_type": args.event,
        "agent_family": args.agent,
        "duration_bucket": args.duration_bucket,
        "telemetry_version": "1",
    }
    if config.get("installation_id"):
        event["installation_id"] = str(config["installation_id"])
    if args.error_code:
        event["error_code"] = args.error_code
    if args.feedback:
        event["feedback"] = args.feedback
    return {key: value for key, value in event.items() if value not in (None, "")}


def write_file(event: dict, location: str) -> None:
    target = Path(os.path.expanduser(location)).resolve()
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(event, ensure_ascii=False, separators=(",", ":")) + "\n")


def post_event(event: dict, endpoint: str) -> None:
    payload = json.dumps(event, ensure_ascii=False).encode("utf-8")
    req = request.Request(endpoint, data=payload, method="POST")
    req.add_header("Content-Type", "application/json")
    with request.urlopen(req, timeout=2) as response:
        if response.status < 200 or response.status >= 300:
            raise OSError(f"unexpected status {response.status}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Send an opt-in anonymous Skill-Bible run receipt.")
    parser.add_argument("--skill-id", required=True)
    parser.add_argument("--skill-version", default="unversioned")
    parser.add_argument("--event", choices=sorted(ALLOWED_EVENTS), required=True)
    parser.add_argument("--agent", choices=sorted(ALLOWED_AGENTS), default="unknown")
    parser.add_argument("--duration-bucket", choices=sorted(ALLOWED_BUCKETS), default="unknown")
    parser.add_argument("--error-code", default="")
    parser.add_argument("--feedback", choices=sorted(ALLOWED_FEEDBACK))
    parser.add_argument(
        "--config",
        default=os.environ.get("SKILL_BIBLE_TELEMETRY_CONFIG", "~/.skill-bible/telemetry/config.json"),
    )
    args = parser.parse_args()

    config = load_config(args.config)
    if config.get("enabled") is not True:
        return 0

    try:
        event = build_event(args, config)
        if config.get("mode", "file") == "http" and config.get("endpoint"):
            post_event(event, str(config["endpoint"]))
        else:
            write_file(event, str(config.get("event_file", "~/.skill-bible/telemetry/events.jsonl")))
    except Exception:
        # Analytics must never interrupt the user's actual task.
        return 0
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
