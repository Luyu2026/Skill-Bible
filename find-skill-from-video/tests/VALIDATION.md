# 验证记录

执行日期：2026-10-27（优化版）。验证为“离线契约测试”，全部为合成 fixture，不代表真实视频/API 成功。

## 命令与结果

| 命令 | 退出码 | 结果 |
| --- | --- | --- |
| `python3 -m compileall -q work/skills/find-skill-from-video/scripts work/skills/find-skill-from-video/tests` | 0 | 编译通过 |
| `python3 find-skill-from-video/tests/test_fixtures.py` | 0 | Skill-Bible 发布前复跑 24 tests，OK |

## 优化后覆盖的行为

- 默认只请求 GitHub（仓库检索；配置 token 时追加代码检索），SkillHub 绝不默认访问，只保留 `source=skipped`（reason 含 “not selected”）记录。
- `--sources github,skillhub` 显式选择后才请求 SkillHub，且只发送已证实的 `keyword` 参数（无 page/pageSize/sortBy）。
- 单请求 timeout 与总预算可配置并校验；每次真实 fetch 的超时取 `min(request_timeout, remaining_budget)`，预算耗尽后剩余请求 `skipped`，不自动重试，记录 `elapsed_seconds` 与 `budget_exhausted`。
- limitations 按 `github_code` 实际记录（success/failed/skipped）说明代码检索结果；token 存在不等于检索成功。
- `video_evidence.py` 元数据+字幕同命令失败但已写出可读 `video.info.json`/已保存字幕时，保留可用元信息与字幕并记录失败，不丢弃。
- `compose_result.py` 的 `search_scope` 透传输入查询范围（query/search_query/queries 等），不止来源名；调用方提供的 search_scope 补充不覆盖。
- `video_evidence.py` 默认 `--frames 0`：不下载视频、不执行 ffmpeg；显式 `--frames N` 才下载并抽帧；字幕默认 `zh.*,en.*`，可用 `--sub-langs` 扩展；子进程受 `min(单阶段 timeout, 剩余总预算)` 约束；`is_live` 直播跳过均匀抽帧；失败保留 stage/elapsed_seconds/resume。
- `compose_result.py` 有限范围语义：内容已读、检索完成、`sources_checked` 至少含一个成功主路径（github / github_code / public_web / direct_upstream）且无未解决冲突时才允许 `not_found`（含义为“本次实际范围未找到”）；`search_scope`（sources_checked、search_complete）透传结果；confirmed_original 不要求 SkillHub。
- 原作身份门禁与替代门禁原有测试不回退：已确认原作、缺锚点、疑似原作、同能力替代、reference_only、无字幕不伪造转写等行为保持。

## 未验证（离线模拟局限）

主环境验收补充：缺少 yt-dlp 时返回结构化 dependency 失败，不抛出未处理异常；搜索/视频新增 `--summary`，精简显示但保留完整证据文件，新增 3 项回归，最终共 22 项。Skill 格式验证与 compileall 均 exit 0。

发布迭代：依据用户指定的成功对话，工作流改为一句话输入、优先宿主 Agent 的现成视频理解、沿作者定位上游，脚本只作降级；无法找到/获取原作才展开 GitHub、SkillHub 同类推荐。新增 2 项证据门禁测试：有方法与来源的真实正文提取可不带时间码；标题级内容、未核验片段、错误视频来源仍被拒绝。最终共 24 项离线测试通过；不代表每个宿主 Agent 都有视频工具，也不代表同一视频已重新端到端跑通。

有限真实请求：默认 GitHub 查询 job-market-map 成功（3.091 秒，SkillHub skipped）；原抖音元信息请求 1.573 秒因 403/fresh cookies 失败（exit 2），未下载、未抽帧、未绕过限制。记录存安装包外的迭代目录；这不是端到端查找成功或提速倍数证明。

- 未对真实视频平台（抖音、B 站、YouTube 等）做端到端验证；未使用真实 GitHub token 实测代码检索；未验证 SkillHub 线上响应形状。测试仅验证脚本在离线合成输入下的行为契约。
