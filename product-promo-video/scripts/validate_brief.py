#!/usr/bin/env python3
"""Validate the release reasoning layer that sits on top of the renderer brief."""
import json
import sys
from pathlib import Path


def fail(message):
    print(f"- {message}")


def main():
    if len(sys.argv) != 2:
        raise SystemExit("用法: python3 validate_brief.py <brief.json>")

    path = Path(sys.argv[1])
    try:
        brief = json.loads(path.read_text())
    except (OSError, json.JSONDecodeError) as error:
        raise SystemExit(f"无法读取 brief: {error}")

    errors = []
    campaign = brief.get("campaign")
    if not isinstance(campaign, dict):
        errors.append("缺少 campaign；请说明发布目标、受众、核心承诺和 CTA")
        campaign = {}

    for key, label in {
        "goal": "发布目标",
        "audience": "目标受众",
        "primary_promise": "核心承诺",
        "cta": "CTA",
    }.items():
        if not str(campaign.get(key, "")).strip():
            errors.append(f"campaign.{key} 缺少{label}")

    scenes = brief.get("scenes")
    if not isinstance(scenes, list) or len(scenes) < 3:
        errors.append("至少需要 3 个场景：开场/证明/CTA")
        scenes = []

    if not any(scene.get("type") == "end" for scene in scenes if isinstance(scene, dict)):
        errors.append("缺少 end 场景，无法明确落下 CTA")

    proof_scenes = 0
    for index, scene in enumerate(scenes, start=1):
        if not isinstance(scene, dict):
            errors.append(f"scenes[{index}] 不是对象")
            continue
        kind = scene.get("type", "")
        if kind in {"feature", "gallery", "stats", "tags"}:
            evidence = scene.get("evidence")
            if not str(evidence or "").strip():
                errors.append(f"scenes[{index}] 的 {kind} 场景缺少 evidence 来源或素材说明")
            else:
                proof_scenes += 1
        if kind == "stats":
            for item_index, item in enumerate(scene.get("items", []), start=1):
                if not str(item.get("source", "")).strip():
                    errors.append(f"scenes[{index}].items[{item_index}] 的数据缺少 source")

    if proof_scenes == 0:
        errors.append("没有带 evidence 的证明场景；不要只做口号和动效")

    if errors:
        print("发布 brief 尚未通过：")
        for error in errors:
            fail(error)
        raise SystemExit(1)

    print("发布 brief 校验通过：目标、受众、承诺、证据与 CTA 均已填写。")


if __name__ == "__main__":
    main()
