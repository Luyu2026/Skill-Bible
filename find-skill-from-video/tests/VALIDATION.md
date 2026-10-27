# 验证记录

## 两阶段交互（2026-10-28）

按最新交互要求，默认先快速找原作（预计 1–2 分钟），未确认则询问是否找同类并给额外耗时预期；只有用户同意才开启 GitHub/SkillHub 替代检索（预计另用 1–3 分钟）。两阶段分别计时，等待回复不计入检索。已有明确兜底授权则不重复询问。

结果打包器新增显式授权门禁；原视频不可读时，可用用户需求/分享文案中的明确功能作为替代比较目标，但不能作为原作身份证据。新增三项离线测试覆盖无授权拒绝替代、描述驱动替代不升级原作、授权不能替代明确目标或真实源文件。共 31 项离线测试通过，Skill 格式校验及 diff 检查通过。这些是模拟回归，不代表真实视频准确率或实际用时；本次未重新进行豆包真实视频测速。

## 真实行为测试后迭代（2026-10-27）

在豆包工作自动/高模式，以四个用户实际视频做八个独立对话对照，交错先后、每组预算 270 秒。原版显式 Skill 运行界面用时 127/176/170/124 秒；普通查找 126/255/190/167 秒。单次、小样本、共享账号且未隔离缓存，不能据此承诺稳定提速或整体准确率。两者都存在相似视频串用和自报耗时不可靠；原版 Skill 也没有稳定遵守证据门禁。

主控独立打开六项视频原页，读到章节要点并从画面确认 ChatCut、Remotion，证实对照两组的另一套六项清单不能称完整原作。生图视频原页明确“后台私我”，不能把其他版本评论口令或发布日期移植过来。小红书原页取证不足；不将另一通用引擎的相似效果当作已确认来源。

基于这些失败新增原 ID 锁定、公开浏览器优先、合集覆盖分开报告、私域获取边界、真实计时和交付门禁。离线回归增至 28 项：错视频来源拒绝、明确落地 URL 可用、未核验帧拒绝、重复文件不补合集数量、作者冲突不升级线索。新增测试是模拟数据，不替代真实回测。完整真实日志保存在安装包外，不公开个人对话记录。

新增真实回测：同一六项视频，新对话、180秒预算。首次修订版正确拒绝错视频名单作为原作，但界面用时322秒，预算执行失败；未实际调用正常浏览器，且归档耗时过多。不能宣称修订版已稳定提速。进一步明确浏览器调用、剩余30秒停止规则，并加入结构化输入模板，避免为格式阅读脚本源码。

第二次修订版真实回测界面124秒，预算达标，但仍没有调用浏览器、读取源Skill文件或执行门禁；状态虽为待补证，正文却把异视频名单称为高概率原名单，验收不通过。最后增加状态/正文一致性规则；此措辞修订未另做真实回测。28项离线测试及输入模板运行通过，不等于宿主会遵守调用流程，当前仍需总控验收原作身份和合集完整性。

以下为此前发布阶段的历史验证，不能代替本轮真实测试结论。

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

## 历史未验证范围（离线模拟阶段）

主环境验收补充：缺少 yt-dlp 时返回结构化 dependency 失败，不抛出未处理异常；搜索/视频新增 `--summary`，精简显示但保留完整证据文件，新增 3 项回归，最终共 22 项。Skill 格式验证与 compileall 均 exit 0。

发布迭代：依据用户指定的成功对话，工作流改为一句话输入、优先宿主 Agent 的现成视频理解、沿作者定位上游，脚本只作降级；无法找到/获取原作才展开 GitHub、SkillHub 同类推荐。新增 2 项证据门禁测试：有方法与来源的真实正文提取可不带时间码；标题级内容、未核验片段、错误视频来源仍被拒绝。最终共 24 项离线测试通过；不代表每个宿主 Agent 都有视频工具，也不代表同一视频已重新端到端跑通。

有限真实请求：默认 GitHub 查询 job-market-map 成功（3.091 秒，SkillHub skipped）；原抖音元信息请求 1.573 秒因 403/fresh cookies 失败（exit 2），未下载、未抽帧、未绕过限制。记录存安装包外的迭代目录；这不是端到端查找成功或提速倍数证明。

- 未对真实视频平台（抖音、B 站、YouTube 等）做端到端验证；未使用真实 GitHub token 实测代码检索；未验证 SkillHub 线上响应形状。测试仅验证脚本在离线合成输入下的行为契约。
