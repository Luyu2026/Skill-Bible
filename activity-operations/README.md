# 活动运营岗位技能（Activity Operations）

> 陆羽Skill 为「活动运营」岗位生成的体系化 Skill 套件，覆盖活动运营完整工作链：**目标设定 → 机制设计 → 执行落地 → 传播放大 → 复盘沉淀**。
> 生成时间：2026-09 · 生成器：luyu-skill（元 Skill 工厂）

## 套件结构

```
activity-operations-master/          # 🎯 总控：分诊 → 路由 → 编排
├── 执行链（产出型）   # 每个执行链带 references/*-template.md 输出模板
└── 顾问团（判断型）   # 子总控 + 专家视角 + 方法论
```

## 完整 Skill 清单

| Skill | 说明 |
|---|---|
| [activity-operations-master](./activity-operations/activity-operations-master/) | 🎯 总控：分诊 → 路由 → 编排（3 条预置链路） |
| [activity-operations-planning](./activity-operations/activity-operations-planning/) | 活动策划：目标设定、玩法设计、预算排期 |
| [activity-operations-mechanics](./activity-operations/activity-operations-mechanics/) | 机制设计：参与/传播机制、激励结构、风控 |
| [activity-operations-execution](./activity-operations/activity-operations-execution/) | 执行落地：任务分解、排期、上线检查 |
| [activity-operations-promotion](./activity-operations/activity-operations-promotion/) | 传播放大：渠道组合、传播节奏、投流 |
| [activity-operations-review](./activity-operations/activity-operations-review/) | 复盘：数据归因、经验沉淀、行动项 |
| [activity-operations-advisory-board](./activity-operations/activity-operations-advisory-board/) | 🧭 顾问团总控：评审会+分歧地图 |
| [activity-operations-advisor-huang](./activity-operations/activity-operations-advisor-huang/) | 黄有璨：运营价值判断 |
| [activity-operations-advisor-zhang](./activity-operations/activity-operations-advisor-zhang/) | 张亮：运营体系判断 |
| [activity-operations-advisor-qu](./activity-operations/activity-operations-advisor-qu/) | 曲卉：增长实验判断 |
| [activity-operations-method-light-of-operations](./activity-operations/activity-operations-method-light-of-operations/) | 《运营之光》：做局/四大思维/闭环 |
| [activity-operations-method-growth-hacking](./activity-operations/activity-operations-method-growth-hacking/) | 《增长黑客》：实验循环/AARRR/北极星 |
| [activity-operations-method-lean-analytics](./activity-operations/activity-operations-method-lean-analytics/) | 《精益数据分析》：第一关键指标/数据诊断 |

## 什么时候用

| 场景 | 用哪个 |
|---|---|
| 「活动运营怎么做」「没方向」 | master → strategy/planning |
| 「效果不好」「怎么优化」 | master → 对应环节 |
| 「方案行不行」「值不值得做」 | advisory-board（评审会） |

## 质量保障

- 调研材料：`references/research/`（活动/增长专项调研（增长案例、疯传）+ 复用（黄有璨/张亮/曲卉/运营之光/增长黑客/精益数据分析））
- 执行链均带 `references/*-template.md` 输出模板（可复用/可迭代）
- 每个 Skill 均含 SKILL.md + README.md + SOURCES.md
- 内部 Skill 互相引用形成完整链路（master 路由 → 执行链 → 顾问团判断）
