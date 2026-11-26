# 可移植个人档案

## 1. 适合什么场景

换 AI 或换电脑时，可以把同一份有出处的个人档案交给新助手，继续沿用项目背景和写作偏好。

## 2. 解决什么问题

减少重复介绍自己、旧偏好冒充新偏好、AI 把推断当事实的问题。它整理关键个人信息，不保存全部聊天记录。

## 3. 一个关键机制

每条信息有稳定 id、来源和状态。两份材料说法不同就保留双方值、标记待裁决，能读取档案文件的 AI 可沿 id 回查，不静默覆盖。

## 4. 你会拿到什么

一个默认私有的档案文件夹：事实、偏好、项目、待确认项、来源登记和可直接阅读的 PROFILE.md。附本机校验结果及三道回读题；双端验证需在目标 AI/设备实际执行。

## 5. 怎么开始

提供一两份你愿意使用的材料，指定新档案目录。脚本使用 Python 3 标准库，无网络依赖。以下命令在含本 Skill 文件夹的目录执行：

```bash
python3 portable-personal-profile/scripts/init_profile.py my-profile
# 由 AI 按 references/profile-schema.md 登记来源并填入结构化文件
python3 portable-personal-profile/scripts/validate_profile.py my-profile
python3 portable-personal-profile/scripts/render_profile.py my-profile
# 生成公开候选文件，分享前人工检查
python3 portable-personal-profile/scripts/render_profile.py my-profile --public
```

把整个私有档案通过压缩包、用户选定同步盘或私有 Git 仓库迁移；新端重新校验并做相同回读题。只分享公开候选文件时，不附原始来源目录。

想先看成品，可以打开[模拟示例与复跑步骤](examples/README.md)。

对话里有新决定时，可以说「把这条对话新增的决定和项目进度续写到上次的档案」。档案会沿用原记录 ID。打开私有 `PROFILE.md` 后，点记录下的来源即可打开包内摘录。

## 6. 可直接复制的调用模板

```text
使用 portable-personal-profile，把我提供的项目复盘和写作偏好整理到 ./my-profile。
只用这些材料，来源登记并保留可定位摘录；缺失项列待确认。
冲突保留双方值等我裁决，敏感字段显式标记，不保存凭证。
请生成结构化档案和 PROFILE.md，运行本机校验，给我三个要求引用 id 与来源的回读题。
说明实际完成的验证；未执行跨 AI/设备验证就标待执行。
```
