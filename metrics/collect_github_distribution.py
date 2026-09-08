#!/usr/bin/env python3
"""Read privacy-preserving GitHub distribution aggregates for Skill-Bible.

This script never contacts Skill users or their machines. It reads only GitHub
repository metrics that GitHub exposes to the repository owner or publicly.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime, timezone
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


DEFAULT_REPOSITORY = "Luyu2026/Skill-Bible"
API_ROOT = "https://api.github.com"


def request_json(url: str, token: str | None) -> tuple[dict | list | None, str | None]:
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "skill-bible-distribution-report",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"

    try:
        with urlopen(Request(url, headers=headers), timeout=15) as response:
            return json.load(response), None
    except HTTPError as error:
        if error.code in {401, 403, 404}:
            return None, f"GitHub 返回 {error.code}，该指标需要有效的仓库 owner 授权或暂不可用。"
        return None, f"GitHub 返回 {error.code}。"
    except URLError:
        return None, "当前无法连接 GitHub。"


def source(status: str, note: str | None = None) -> dict[str, str | None]:
    return {"status": status, "note": note}


def collect(repository: str, token: str | None) -> dict:
    generated_at = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    base_url = f"{API_ROOT}/repos/{repository}"
    report = {
        "generated_at": generated_at,
        "repository": repository,
        "privacy": {
            "collects": "仅 GitHub 仓库层面的聚合分发指标",
            "does_not_collect": "不读取用户提示词、材料、文件、输出、账户或本地 Skill 调用",
        },
        "availability": {},
        "metrics": {},
    }

    repo, repo_error = request_json(base_url, token)
    if isinstance(repo, dict):
        report["availability"]["repository"] = source("available")
        report["metrics"]["repository"] = {
            "stars": repo.get("stargazers_count"),
            "forks": repo.get("forks_count"),
            "watchers": repo.get("subscribers_count"),
            "open_issues": repo.get("open_issues_count"),
            "created_at": repo.get("created_at"),
            "updated_at": repo.get("updated_at"),
        }
    else:
        report["availability"]["repository"] = source("unavailable", repo_error)

    releases, releases_error = request_json(f"{base_url}/releases", token)
    if isinstance(releases, list):
        downloads = sum(
            asset.get("download_count", 0)
            for release in releases
            for asset in release.get("assets", [])
        )
        report["availability"]["release_downloads"] = source("available")
        report["metrics"]["release_downloads"] = {
            "release_count": len(releases),
            "asset_downloads_total": downloads,
        }
    else:
        report["availability"]["release_downloads"] = source("unavailable", releases_error)

    if not token:
        note = "需要仓库 owner 授权；未配置 GITHUB_TOKEN。"
        for metric in ("views_14d", "clones_14d", "top_referrers", "popular_paths"):
            report["availability"][metric] = source("requires_owner_auth", note)
        return report

    traffic_endpoints = {
        "views_14d": "traffic/views",
        "clones_14d": "traffic/clones",
        "top_referrers": "traffic/popular/referrers",
        "popular_paths": "traffic/popular/paths",
    }
    for name, suffix in traffic_endpoints.items():
        data, error = request_json(f"{base_url}/{suffix}", token)
        if data is None:
            report["availability"][name] = source("unavailable", error)
            continue
        report["availability"][name] = source("available")
        report["metrics"][name] = data

    return report


def markdown(report: dict) -> str:
    lines = [
        "# Skill-Bible GitHub 分发数据",
        "",
        f"- 生成时间：{report['generated_at']}",
        f"- 仓库：`{report['repository']}`",
        "- 范围：仅 GitHub 仓库层面聚合指标；不收集用户内容或本地调用。",
        "",
        "## 当前指标",
        "",
    ]
    repository = report["metrics"].get("repository")
    if repository:
        lines.extend([
            f"- Star：{repository['stars']}",
            f"- Fork：{repository['forks']}",
            f"- Watch：{repository['watchers']}",
            f"- Open Issue：{repository['open_issues']}",
        ])
    else:
        lines.append("- 仓库公开指标：本次未成功读取。")

    releases = report["metrics"].get("release_downloads")
    if releases:
        lines.extend([
            f"- Release 数：{releases['release_count']}",
            f"- Release 资源累计下载：{releases['asset_downloads_total']}",
        ])

    lines.extend(["", "## 数据可用性", ""])
    names = {
        "repository": "仓库公开指标",
        "release_downloads": "Release 下载",
        "views_14d": "近 14 天浏览",
        "clones_14d": "近 14 天 clone",
        "top_referrers": "主要来源",
        "popular_paths": "热门路径",
    }
    for key, status in report["availability"].items():
        label = names.get(key, key)
        note = f"：{status['note']}" if status.get("note") else ""
        lines.append(f"- {label}：{status['status']}{note}")

    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repository", default=DEFAULT_REPOSITORY)
    parser.add_argument("--format", choices=("json", "markdown"), default="markdown")
    args = parser.parse_args()

    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("SKILL_BIBLE_GITHUB_TOKEN")
    report = collect(args.repository, token)
    output = json.dumps(report, ensure_ascii=False, indent=2) if args.format == "json" else markdown(report)
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
