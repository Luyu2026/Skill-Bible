# 来源档案（SOURCES.md）

本文件记录 陆羽Skill（luyu-skill）的来源与改造说明。仅作归档用途，不影响使用。

## 来源信息

| 项 | 内容 |
|---|---|
| 方法论参考 1 | [alchaincyf/nuwa-skill](https://github.com/alchaincyf/nuwa-skill)（女娲·Skill造人术，MIT） |
| 方法论参考 2 | [SpaceZephyr/career.skill](https://github.com/SpaceZephyr/career.skill)（职业 Skill 工厂 2.0，MIT） |
| 体系化参考 | Skill-Bible 现有 pm 模块（Master + Skill 链结构） |
| 创建时间 | 2026-09 |

## 参考/保留的机制

**来自 nuwa-skill（女娲）**：
- 蒸馏五层：心智模型 / 决策启发式 / 表达 DNA / 反模式 / 诚实边界
- 心智模型三重验证：跨域复现 + 生成力 + 排他性
- 回答工作流（Agentic Protocol）：问题分类（事实/框架/混合）+ 研究维度从心智模型反推
- 信息源优先级与黑名单（知乎/微信公众号/百度百科永远排除）
- 失败降级路径：来源不足则缩小规模、加大诚实边界，绝不编造

**来自 career.skill（职业工厂）**：
- 工厂化流程：输入分级（L1/L2/L3）→ 行业画像 → 遴选 3 专家 + 3 书 → 并行蒸馏 → 构建 → 质量验证
- 专家/书籍蒸馏的方法论模板（references/ 下三份文档）
- 品味守则：长文>金句、争议>共识、框架>结论、互补>堆名气、诚实>完整
- 快速模式 / 更新模式

**来自 Skill-Bible pm 模块（我们自己的体系）**：
- **Master + Skill 链**：不只生成顾问团，而是生成 总控 + 执行链 + 顾问团 的完整体系（这是与 career.skill 的关键差异）
- **先调研再 Skill 化**：Phase 1 行业基本概念调研，是体系化生成的前提
- 每个生成 Skill 带 SKILL.md + README.md + SOURCES.md 的完整目录结构

## 优化了什么

| 改动 | 原因 |
|---|---|
| 从"工厂生成顾问团"升级为"工厂生成完整 Skill 链" | 用户明确：一个职业模块要覆盖完整工作链（总控+执行+顾问团），不是只有判断能力 |
| 新增 Phase 1 行业基本概念调研 | 用户明确：先调研行业基本概念，再走总控 Skill 化，不能跳过调研直接生成 |
| 命名"陆羽Skill" | 这是 Skill-Bible 的元 Skill，不沿用外部命名 |
| 融入 Skill-Bible 规范 | 生成物满足：体系化、直接上传、来源档案、README 服务使用者 |

## 为什么这么改

Skill-Bible 的定位是「一个模块解决一个具体职位/职能的问题」。陆羽Skill 是这个定位的元能力：输入职业 → 自动调研 → 体系化生成该职业的 Skill 链。它站在 nuwa（蒸馏方法论）和 career.skill（工厂化流程）的肩膀上，但产物形态对齐 Skill-Bible 自身的模块化体系（Master + Skill 链）。
