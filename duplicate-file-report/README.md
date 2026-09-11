# 重复文件核对

下载附件和备份越积越多时，找出内容完全相同的文件，生成可核对的报告。文件名不同也能匹配；同名但内容不同不会混在一起。

## 安装与使用

将整个 `duplicate-file-report` 目录放到 `~/.codex/skills/` 或 `~/.claude/skills/`。需要 Python 3.9+，无需安装额外依赖。

对 Agent 说：

> 用 $duplicate-file-report 核对「项目附件」与「附件备份」两个文件夹，给我重复清单和理论冗余大小，保留所有原文件。

也可在本 Skill 目录执行：

```bash
python3 scripts/find_duplicates.py /path/to/attachments /path/to/backup \
  --output /path/to/reports/duplicates.json
```

输出的父目录必须已存在，JSON 文件必须是新文件且在扫描目录之外。输入目录递归扫描，包括隐藏文件；符号链接与设备等特殊文件跳过。报告包含绝对路径，请只在需要时自行分享。

## 交付内容与限制

- 完全相同内容的分组清单，使用大小筛选、SHA-256 和逐字节复核。
- 硬链接单独列出，不重复计算独立副本。
- 理论冗余字节数、跳过项与错误记录。实际磁盘释放量受硬链接、克隆、压缩、稀疏文件、快照等影响。

不识别相似照片、语义相同文档或转码后的音视频，不自动删除或选原件。使用期间目录应保持稳定；扫描不是快照，云盘占位文件可能触发下载。执行成功后的字段解释见 [报告说明](references/report-contract.md)。

## 授权

指令、文档与案例采用 [CC BY-NC 4.0](LICENSE)；脚本采用 [Apache License 2.0](LICENSE-CODE)。见 [NOTICE](NOTICE)。
