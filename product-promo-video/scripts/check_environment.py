#!/usr/bin/env python3
"""Report whether the local machine can preview or render a promo video."""
import shutil
import subprocess


def version(command):
    path = shutil.which(command)
    if not path:
        return None
    try:
        line = subprocess.run(
            [command, "--version"], capture_output=True, text=True, timeout=5
        ).stdout.splitlines()[0]
    except Exception:
        line = path
    return line or path


def main():
    checks = {
        "node": ("静帧预览和渲染", True),
        "ffmpeg": ("MP4 合成、配音和配乐", False),
    }
    missing_required = []
    print("产品宣传视频环境检查")
    for command, (purpose, preview_required) in checks.items():
        found = version(command)
        if found:
            print(f"[可用] {command}: {found}")
        else:
            level = "静帧预览也需要" if preview_required else "完整 MP4 需要"
            print(f"[缺少] {command}: {purpose}（{level}）")
            if preview_required:
                missing_required.append(command)

    chrome_paths = [
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        "/Applications/Chromium.app/Contents/MacOS/Chromium",
    ]
    chrome = next((path for path in chrome_paths if __import__("os").path.exists(path)), None)
    chrome = chrome or shutil.which("google-chrome") or shutil.which("chromium")
    if chrome:
        print(f"[可用] Chrome/Chromium: {chrome}")
    else:
        print("[缺少] Chrome/Chromium: 静帧预览和 MP4 渲染需要浏览器")
        missing_required.append("Chrome/Chromium")

    if missing_required:
        raise SystemExit("静帧路径尚不可用，请先补齐上面的必要环境。")
    print("静帧路径可用。若 ffmpeg 显示缺少，仍可先用 --preview 审阅画面，补齐后再输出 MP4。")


if __name__ == "__main__":
    main()
