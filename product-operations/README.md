# 产品运营岗位技能（Product Operations）

> 陆羽Skill 为「产品运营」岗位生成的体系化 Skill 套件，覆盖产品运营完整工作链：**运营策略 → 激活留存 → 激励体系 → 数据迭代 → 版本运营 → 反馈闭环**。
> 生成时间：2026-09 · 生成器：luyu-skill（元 Skill 工厂）

## 套件结构

```
product-operations-master/          # 🎯 总控：分诊 → 路由 → 编排
├── 执行链（产出型）   # 每个执行链带 references/*-template.md 输出模板
└── 顾问团（判断型）   # 子总控 + 专家视角 + 方法论
```

## 完整 Skill 清单

| Skill | 说明 |
|---|---|
| [product-operations-master](./product-operations/product-operations-master/) | 🎯 总控：分诊 → 路由 → 编排（3 条预置链路） |
| [product-operations-strategy](./product-operations/product-operations-strategy/) | 运营策略：阶段定位、北极星指标、运营抓手 |
| [product-operations-activation](./product-operations/product-operations-activation/) | 激活留存：Aha Moment、激活路径、留存曲线 |
| [product-operations-incentive](./product-operations/product-operations-incentive/) | 激励体系：积分/等级/勋章、行为设计 |
| [product-operations-data](./product-operations/product-operations-data/) | 数据迭代：看板/漏斗/实验 |
| [product-operations-release](./product-operations/product-operations-release/) | 版本运营：节奏/上线/效果验证 |
| [product-operations-feedback](./product-operations/product-operations-feedback/) | 反馈闭环：收集/分类/需求池/回应 |
| [product-operations-advisory-board](./product-operations/product-operations-advisory-board/) | 🧭 顾问团总控：评审会+分歧地图 |
| [product-operations-advisor-zhang](./product-operations/product-operations-advisor-zhang/) | 张亮：产品运营体系 |
| [product-operations-advisor-qu](./product-operations/product-operations-advisor-qu/) | 曲卉：激活/留存实验 |
| [product-operations-advisor-yujun](./product-operations/product-operations-advisor-yujun/) | 俞军：用户价值判断 |
| [product-operations-method-hooked](./product-operations/product-operations-method-hooked/) | 《上瘾》：Hook 模型/习惯养成 |
| [product-operations-method-growth-hacking](./product-operations/product-operations-method-growth-hacking/) | 《增长黑客》：实验循环/北极星 |
| [product-operations-method-lean-analytics](./product-operations/product-operations-method-lean-analytics/) | 《精益数据分析》：第一关键指标 |

## 什么时候用

| 场景 | 用哪个 |
|---|---|
| 「产品运营怎么做」「没方向」 | master → strategy/planning |
| 「效果不好」「怎么优化」 | master → 对应环节 |
| 「方案行不行」「值不值得做」 | advisory-board（评审会） |

## 质量保障

- 调研材料：`references/research/`（产品运营专项调研（俞军、产品运营方法）+ 复用（张亮/曲卉/上瘾/会员经济/增长黑客/精益数据分析））
- 执行链均带 `references/*-template.md` 输出模板（可复用/可迭代）
- 每个 Skill 均含 SKILL.md + README.md + SOURCES.md
- 内部 Skill 互相引用形成完整链路（master 路由 → 执行链 → 顾问团判断）
