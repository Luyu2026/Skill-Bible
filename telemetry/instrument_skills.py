#!/usr/bin/env python3
"""Add or refresh the standard optional telemetry note in every Skill-Bible Skill."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MARKER_START = "<!-- skill-bible-telemetry:start -->"
MARKER_END = "<!-- skill-bible-telemetry:end -->"


def telemetry_note(skill_id: str) -> str:
    return f"""

{MARKER_START}
## 可选匿名运行回执

仅当安装者已明确开启 Skill-Bible 匿名回执，且同级 `telemetry/emit_event.py` 与配置文件存在时，才可在本次任务开始后记录一次 `started`，在完成或失败后记录一次对应终态。使用 Skill ID `{skill_id}`；仅发送 Skill ID、版本、Agent 大类、事件类型、耗时区间和标准化错误码，绝不发送提示词、材料、文件、输出或账号信息。

回执是尽力而为：配置或辅助程序不存在、网络不可用或发送失败时，立即跳过，不得影响任务、重试、提示用户或改变输出。详细规则见仓库根目录的 `telemetry/README.md`。
{MARKER_END}
""".rstrip() + "\n"


def main() -> int:
    changed = 0
    for skill_file in sorted(ROOT.glob("*/SKILL.md")):
        skill_id = skill_file.parent.name
        content = skill_file.read_text(encoding="utf-8")
        start = content.find(MARKER_START)
        end = content.find(MARKER_END)
        if start != -1 and end != -1:
            end += len(MARKER_END)
            content = content[:start].rstrip() + "\n" + telemetry_note(skill_id)
        elif start == -1 and end == -1:
            content = content.rstrip() + telemetry_note(skill_id)
        else:
            raise RuntimeError(f"broken telemetry marker in {skill_file}")
        skill_file.write_text(content, encoding="utf-8")
        changed += 1
    print(f"instrumented {changed} skills")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
