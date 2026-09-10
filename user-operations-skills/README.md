# 用户运营岗位技能（User Operations Skills）

> 陆羽Skill 为「用户运营」岗位生成的体系化 Skill 套件，覆盖用户全生命周期（分层 → 生命周期 → 留存 → 召回 → 会员 → 社群）。侧重**做决策 + 产出质量**。
> 生成时间：2026-09 · 生成器：luyu-skill（元 Skill 工厂）

## 这套库解决什么

用户运营工作的主线是**让用户留下来、贡献更多价值**——但"留存""唤醒""会员"这些词背后，是大量需要判断和产出的工作。这套库把用户运营完整工作链沉淀为 14 个 Skill：**先感知判断（顾问团），再产出交付（执行链）**，总控负责路由和编排。

与「通用运营」套件的分工：通用运营覆盖运营全链路（数据/活动/内容/策略），本套件聚焦**用户全生命周期**（分层/生命周期/留存/召回/会员/社群），两者错位互补。

## 成员总览

### 🎯 总控（1）

| Skill | 用途 |
|---|---|
| [user-operations-master](./user-operations-master/) | 用户运营工作总控：分诊问题 → 路由到最合适的 Skill → 编排多 Skill 链路 |

### ⚙️ 执行链（6，产出型）

| Skill | 什么时候用 | 产出 |
|---|---|---|
| [user-operations-segmentation](./user-operations-segmentation/) | 用户怎么分层 / RFM / 分群 | 分层体系 + 各层差异化策略 |
| [user-operations-lifecycle](./user-operations-lifecycle/) | 新用户/成长期/成熟期怎么运营 | 各阶段策略 + 运营日历 |
| [user-operations-retention](./user-operations-retention/) | 留存不行 / 怎么提升留存 | 留存提升方案（机制+实验） |
| [user-operations-recall](./user-operations-recall/) | 唤醒沉睡用户 / 流失召回 | 召回方案（钩子/渠道/成本） |
| [user-operations-membership](./user-operations-membership/) | 做会员体系 / 等级权益 | 会员体系设计方案 |
| [user-operations-community](./user-operations-community/) | 社群怎么运营 / 群不活跃 | 社群运营方案 |

### 🧭 顾问团（7，判断型）

| Skill | 视角 | 擅长 |
|---|---|---|
| [user-operations-advisory-board](./user-operations-advisory-board/) | 顾问团总控 | 路由 / 多专家评审会 |
| [user-operations-advisor-zhang](./user-operations-advisor-zhang/) | 张亮（运营体系） | 生命周期策略、体系搭建 |
| [user-operations-advisor-qu](./user-operations-advisor-qu/) | 曲卉（增长实验） | 留存提升、看什么指标 |
| [user-operations-advisor-xu](./user-operations-advisor-xu/) | 徐志斌（社群激励） | 社群运营、用户激励、传播 |
| [user-operations-method-hooked](./user-operations-method-hooked/) | 《上瘾》 | 习惯养成、留存机制设计 |
| [user-operations-method-membership](./user-operations-method-membership/) | 《会员经济》 | 会员模式、用户关系升级 |
| [user-operations-method-small-group](./user-operations-method-small-group/) | 《小群效应》 | 社群结构、激励设计、社交增长 |

## 建议使用路径

```
第一次用：先找 user-operations-master，说清你的问题 → 它告诉你该用哪个
明确场景：直接调对应执行链 Skill（如"帮我设计会员体系"→ membership）
要专家意见：user-operations-advisory-board 开评审会，或直接调某位顾问
```

## 预置链路

- **A 分层到精细化**：segmentation → lifecycle → retention/recall
- **B 数据问题到动作**：segmentation（定位问题分层）→ retention/recall/membership
- **C 会员从 0 到 1**：membership → segmentation → retention

## 安装方式

每个 Skill 是独立目录（SKILL.md + README.md + SOURCES.md，执行型另带 references/ 输出模板），复制到你的 Agent 技能目录即可。全套复制后，先体验 `user-operations-master` 的路由，再按需深入单个 Skill。

## 是什么保证质量

- **调研驱动**：3 位专家 + 3 本书均经专项调研（见 `references/research/`），心智模型/决策规则标注来源与诚实边界
- **参考模板**：每个执行链 Skill 带 `references/*-template.md` 完整输出模板（含每节写作指引），SKILL.md 保持轻量（判断+工作流）——luyu-skill 固化的最佳实践
- **不编造**：交付物基于你提供的真实材料，信息不足标注 [待确认]
- **证据分级**：数据结论区分 A（数据支持）/ B（强推断）/ C（推测）

## 调研时间戳与来源

- 调研时间：2026-09 · 方法：陆羽Skill（nuwa 蒸馏方法论 + career.skill 工厂流程）
- 张亮/曲卉调研复用自「通用运营」套件；徐志斌 + 《上瘾》《会员经济》《小群效应》为本套件新调研
- 所有来源与参考机制见每个 Skill 的 `SOURCES.md` 与 `references/research/`

## 迭代建议

哪个专家/哪本书/哪个执行场景不符合预期？告诉陆羽Skill（luyu-skill），可单独重做那一个。