# 换一个 AI 后继续使用同一份个人档案

林澄和「航标」项目均为虚构。林澄希望把项目背景和写作偏好带到另一个 AI，同时保留两条需要本人确认的分歧。

[项目复盘](sample-profile/sources/retro.md)和[写作偏好](sample-profile/sources/writing.md)是建档输入。[私有视图](sample-profile/PROFILE.md)展示项目、带出处的两项冲突和待确认的成效。[公开候选视图](sample-profile/PUBLIC_PROFILE.md)只保留可公开的身份与项目。

## 复跑示例

在包含此 Skill 的目录执行以下命令。用未占用的目录名复制示例，便于保留原件。

```bash
cp -R portable-personal-profile/examples/sample-profile ./profile-example
python3 portable-personal-profile/scripts/validate_profile.py ./profile-example
python3 portable-personal-profile/scripts/render_profile.py ./profile-example
python3 portable-personal-profile/scripts/render_profile.py ./profile-example --public
```

预期结果是校验通过，两项冲突仍待本人裁决。私有视图保留两种写作长度和各自的来源，并隐藏模拟敏感记录的正文。公开候选视图省略该敏感记录、两项冲突和未经确认的成效。

## 回读验证

把完整示例目录交给新 AI，让它只读这份目录，回答下列问题并给出记录 ID、状态和来源。核对时可参考本表。

| 问题 | 核对点 |
|---|---|
| 林澄最近在做什么？ | `project.navigator` 为 `confirmed`，来源 `s-retro#project`。林澄负责「航标」需求与评测。 |
| 项目更新最多写多少字？ | `pref.copy-length` 为 `conflict`。两个来源分别写了不超过 200 字和可写 800 字，等本人确认适用情境。 |
| 能把节省 30% 整理时间写进介绍吗？ | `question.impact` 为 `unconfirmed`，来源 `s-retro#unconfirmed`。先补评测记录，再确认能否对外引用。 |
