# 私域运营岗位技能（Private Domain Operations）

> 陆羽Skill 为「私域运营」岗位生成的体系化 Skill 套件，覆盖私域运营完整工作链：**体系设计 → 引流 → 社群运营 → 转化 → 裂变 → 数据分层**。
> 生成时间：2026-09 · 生成器：luyu-skill（元 Skill 工厂）

## 套件结构

```
private-domain-operations-master/          # 🎯 总控：分诊 → 路由 → 编排
├── 执行链（产出型）   # 每个执行链带 references/*-template.md 输出模板
└── 顾问团（判断型）   # 子总控 + 专家视角 + 方法论
```

## 完整 Skill 清单

| Skill | 说明 |
|---|---|
| [private-domain-operations-master](./private-domain-operations/private-domain-operations-master/) | 🎯 总控：分诊 → 路由 → 编排（3 条预置链路） |
| [private-domain-operations-strategy](./private-domain-operations/private-domain-operations-strategy/) | 体系设计：渠道/人设/承接/转化路径 |
| [private-domain-operations-traffic](./private-domain-operations/private-domain-operations-traffic/) | 引流：钩子/路径/承接 |
| [private-domain-operations-community](./private-domain-operations/private-domain-operations-community/) | 社群运营：内容/互动/成交三线 |
| [private-domain-operations-conversion](./private-domain-operations/private-domain-operations-conversion/) | 转化：信任→成交→复购 |
| [private-domain-operations-referral](./private-domain-operations/private-domain-operations-referral/) | 裂变转介绍：激励/路径/风控 |
| [private-domain-operations-data](./private-domain-operations/private-domain-operations-data/) | 数据分层：标签/SCRM |
| [private-domain-operations-advisory-board](./private-domain-operations/private-domain-operations-advisory-board/) | 🧭 顾问团总控：评审会+分歧地图 |
| [private-domain-operations-advisor-xu](./private-domain-operations/private-domain-operations-advisor-xu/) | 徐志斌：社群运营 |
| [private-domain-operations-advisor-zhang](./private-domain-operations/private-domain-operations-advisor-zhang/) | 张亮：生命周期运营 |
| [private-domain-operations-advisor-qu](./private-domain-operations/private-domain-operations-advisor-qu/) | 曲卉：留存/复购实验 |
| [private-domain-operations-method-small-group](./private-domain-operations/private-domain-operations-method-small-group/) | 《小群效应》：三近一反/临界规模 |
| [private-domain-operations-method-membership](./private-domain-operations/private-domain-operations-method-membership/) | 《会员经济》：会员体系/超级用户 |
| [private-domain-operations-method-private-domain](./private-domain-operations/private-domain-operations-method-private-domain/) | 私域方法论：链路/标签/SCRM |

## 什么时候用

| 场景 | 用哪个 |
|---|---|
| 「私域运营怎么做」「没方向」 | master → strategy/planning |
| 「效果不好」「怎么优化」 | master → 对应环节 |
| 「方案行不行」「值不值得做」 | advisory-board（评审会） |

## 质量保障

- 调研材料：`references/research/`（私域专项调研（私域方法、小群效应书）+ 复用（徐志斌/张亮/曲卉/小群效应/会员经济））
- 执行链均带 `references/*-template.md` 输出模板（可复用/可迭代）
- 每个 Skill 均含 SKILL.md + README.md + SOURCES.md
- 内部 Skill 互相引用形成完整链路（master 路由 → 执行链 → 顾问团判断）
