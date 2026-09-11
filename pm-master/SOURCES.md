# 来源档案（SOURCES.md）

本文件记录 pm-master 的来源与改造说明。仅作归档用途，不影响使用。

## 来源信息

| 项 | 内容 |
|---|---|
| 原作者 | SpaceZephyr（空格的键盘） |
| 原仓库 | https://github.com/SpaceZephyr/pm-skills |
| 原 Skill | `pm-master`（PM-Skill 2.0） |
| 原协议 | MIT License |
| Copy 时间 | 2026-09 |

## 参考/保留的机制


- **references**：无（运行不需要额外参考资料）

## 优化了什么

| 改动 | 原因 |
|---|---|
| 新增 README.md | 按 Skill-Bible 规范：用户打开 README 即知"是不是我要用的、我给什么、拿走什么" |
| 新增 SOURCES.md | 来源档案：保留原作者地址与参考机制，符合 MIT 协议要求 |

## 为什么这么改

Skill-Bible 采用模块化收录：一个职能模块尽可能覆盖完整工作链。本 Skill 是产品经理工作链的一环，由 `pm-master` 总控统一路由；上下游衔接见 SKILL.md 内「上下游衔接」章节。

---

## 2026-09 模块优化记录（陆羽Skill 标准复检）

按陆羽Skill（luyu-skill）标准对产品经理模块其余 21 个 Skill（PRD 不动）复检后，本轮优化如下：

### 1. 执行型 Skill 补「输出参考模板」

| Skill | 新增模板 | 说明 |
|---|---|---|
| pm-review-board | `references/review-report-template.md` | 评审结论报告 |
| pm-prioritization-engine | `references/priority-report-template.md` | 优先级排序报告 |
| pm-survey-designer | `references/survey-design-template.md` | 问卷设计文档 |
| pm-competitor-deconstructor | `references/competitor-analysis-template.md` | 竞品拆解报告 |
| pm-postmortem-writer | `references/postmortem-report-template.md` | 复盘报告 |
| pm-roadmap-planner | `references/roadmap-plan-template.md` | 产品路线图 |
| pm-tracking-spec-writer | `references/tracking-spec-template.md` | 埋点方案设计文档 |

- 模板由 SKILL.md 内嵌输出结构提取生成（保留原结构 + 写作指引），SKILL.md 输出章节加「📋 完整输出模板见 references/xxx-template.md」引用
- **收益**：对齐 pm-prd-writer 的参考模板最佳实践（luyu-skill 固化），模板可独立复用/迭代；SKILL.md 保留原版深度（最小侵入，不删原内容）

### 2. 全部 Skill 补「延展机制」章节

- 19 个 Skill（除 pm-prd-writer 已有、pm-master 为总控）统一补「延展机制」：
  > 材料不足以把问题拆深时，去 GitHub 参考同类成熟项目的产品机制（如何拆解、如何区分类型、如何追问、如何验收），参考机制不照搬内容
- **收益**：对齐 luyu-skill 规范"每个 Skill 内置延展机制"，Skill 不再是封闭脚本，具备自进化能力

### 3. 边界检查结论

- 原版 pm-skills 的「兜底策略」章节已覆盖"不编造、降级"等诚实边界，**未重复添加**（避免冗余）
- 原版「上下游衔接」引用的兄弟 Skill 全部存在于当前模块（22 个），引用有效，未改动

### 未优化的部分（说明）

- pm-prd-writer：按用户要求不动（已是参考模板标杆）
- pm-master：总控职责不变，仅记录本条优化档案
- 4 个带 HTML 资产模板的 Skill（analytics/experiment/roadmap/tracking）：已有 `assets/*.html` 运行模板，不再加 Markdown 模板

### 优化原则

按陆羽Skill"有优化空间就优化、没有大优化点就不为优化而优化"：只做**低风险高价值**的结构性补齐（模板 + 延展机制），保留原版全部判断深度，不重写成熟内容。
