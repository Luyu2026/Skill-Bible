# 字幕时间轴校正

字幕整体慢了两秒，或者开头正常、结尾越差越多时，生成一份校正后的 SRT 和可核对的时间变更报告。

## 安装与使用

把 `subtitle-retime` 整个目录放入 Agent 的 Skill 安装目录（如 `~/.codex/skills/` 或 `~/.claude/skills/`）。需要 Python 3.9+，无需额外安装依赖。

直接对 Agent 说：

> 用 $subtitle-retime 处理 lecture.srt，字幕比声音晚 2 秒，整体提前，保留原文件。

> 用 $subtitle-retime 校正访谈字幕：字幕 00:00:10,000 对应视频 00:00:12,000，字幕 00:10:10,000 对应视频 00:10:18,000。请输出新字幕和校正报告。

命令行也可直接使用：

```bash
python3 scripts/retime.py lecture.srt --offset-ms -2000 --out-dir corrected
```

命令在本 Skill 目录内执行；其他位置请使用脚本的实际路径。输入文件路径相对于当前工作目录。输出目录必须尚不存在。

## 你会拿到什么

- `corrected.srt`：UTF-8、LF 换行的新字幕；文字、标签、条目顺序与编号保持不变。
- `report.json`：变换参数、每条字幕原/新时间码、裁剪或丢弃数量、重叠和乱序提示，不含字幕正文。

支持严格的、空行分隔的 SRT，时间码为 `HH:MM:SS,mmm`（小时至少两位）。不支持 WebVTT、ASS、时间行位置扩展或缺分隔符的损坏 SRT。不会自动听音对齐、翻译、改字幕内容，也不能用一个线性变换修复多处剪辑断点。负时间默认报错；明确需要片头裁剪时可用 `--negative clip`，细节见 [时间规则](references/timing-rules.md)。

## 授权

指令、文档与案例使用 [CC BY-NC 4.0](LICENSE)；脚本使用 [Apache License 2.0](LICENSE-CODE)。见 [NOTICE](NOTICE)。
