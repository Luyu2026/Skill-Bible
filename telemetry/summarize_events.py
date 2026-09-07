#!/usr/bin/env python3
"""Create a concise daily or weekly Skill-Bible telemetry report from JSONL."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from datetime import datetime, timedelta, timezone
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--events", default="~/.skill-bible/telemetry/events.jsonl")
    parser.add_argument("--days", type=int, choices=(1, 7), default=1)
    args = parser.parse_args()

    cutoff = datetime.now(timezone.utc) - timedelta(days=args.days)
    events = []
    source = Path(args.events).expanduser()
    if source.is_file():
        for line in source.read_text(encoding="utf-8").splitlines():
            try:
                item = json.loads(line)
                when = datetime.fromisoformat(item["occurred_at"].replace("Z", "+00:00"))
                if when >= cutoff:
                    events.append(item)
            except (KeyError, TypeError, ValueError, json.JSONDecodeError):
                continue

    title = "日报" if args.days == 1 else "周报"
    starts = sum(event.get("event_type") == "started" for event in events)
    completes = sum(event.get("event_type") == "completed" for event in events)
    failures = sum(event.get("event_type") == "failed" for event in events)
    installs = {event.get("installation_id") for event in events if event.get("installation_id")}
    per_skill = Counter(event.get("skill_id", "unknown") for event in events)
    per_error = Counter(event.get("error_code", "unknown") for event in events if event.get("event_type") == "failed")

    print(f"# Skill-Bible 使用{title}")
    print()
    print(f"统计窗口：最近 {args.days} 天")
    print(f"- 启动：{starts}")
    print(f"- 完成：{completes}")
    print(f"- 失败：{failures}")
    print(f"- 匿名安装实例：{len(installs)}")
    if starts:
        print(f"- 完成率：{completes / starts:.1%}")
    if per_skill:
        print("\n## 调用最多的 Skill")
        for skill, count in per_skill.most_common(5):
            print(f"- `{skill}`：{count}")
    if per_error:
        print("\n## 主要失败原因")
        for code, count in per_error.most_common(5):
            print(f"- `{code}`：{count}")
    if not events:
        print("\n暂无回执。请确认用户已明确开启匿名回执，并配置了本地文件或公开接收端。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
