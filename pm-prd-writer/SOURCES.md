# 来源档案（SOURCES.md）

本文件记录 pm-prd-writer 的来源与改造说明。仅作归档用途，不影响使用。

## 来源信息

| 项 | 内容 |
|---|---|
| 原作者 | SpaceZephyr（空格的键盘） |
| 原仓库 | https://github.com/SpaceZephyr/pm-skills |
| 原 Skill | `pm-prd-writer`（PM-Skill 2.0 执行工具箱） |
| 原协议 | MIT License |
| 复制时间 | 2026-09 |

## 参考/保留的机制

- **阶段零需求体检**：动笔前检查「需求来源 / 用户价值 / 成功定义」三个信号，让风险显性化
- **四阶段工作流**：需求澄清（Clarify）→ 结构化输出（Structure）→ 自动补漏（Enrich）→ 验收输出（Deliver）
- **澄清问题分级**：必须回答（阻塞动笔）/ 最好回答（影响完整度）/ 可以先跳过（后面补）
- **自动补漏清单**：异常与边界 / 埋点与数据 / 非功能需求 / 系统对接
- **待确认项三条硬规则**：默认建议值 + 影响范围 + 按优先级排序
- **失败兜底策略**：信息不足时输出「需求梳理文档」而非硬写半成品 PRD
- **质量检查清单**：12 项自查
- **PRD 完整模板**：`references/prd-template.md`（五大章节 + 功能模块递归结构）

## 优化了什么

| 改动 | 原因 |
|---|---|
| 上下游衔接改为通用描述 | 原版引用 `pm-master`、`pm-review-board`、`pm-tracking-spec-writer` 等 Skill-Bible 当前未收录的 Skill，改为通用表述，避免指向不存在的能力 |
| 新增「延展机制」章节 | 符合 Skill-Bible 规范：材料不足时允许参考同类成熟项目的产品机制，参考机制不照搬内容 |
| description 微调 | 保持触发词完整，去掉对未收录 Skill 的依赖暗示 |

## 为什么这么改

Skill-Bible 采用「只保留验证过真的好用的 Skill」原则：当前仅收录 pm-prd-writer，其余 pm-* Skill（评审、埋点、实验等）在跑通后再逐步扩展。因此本文档与 SKILL.md 中不引用未收录的 Skill，避免用户安装后遇到失效链接。
