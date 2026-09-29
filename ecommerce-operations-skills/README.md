# 电商运营岗位技能（E-commerce Operations Skills）

> 陆羽Skill 为「电商运营」岗位生成的体系化 Skill 套件，涵盖电商经营完整工作链。侧重**做决策 + 产出质量**。
> 生成时间：2026-09 · 生成器：[陆羽Skill](https://github.com/Luyu2026/Skill-Bible/tree/main/luyu-skill)（元 Skill 工厂）

## 这套库解决什么

电商运营看似零散——今天选品、明天备大促、后天投流量、还要盯数据、定复盘。这套 Skill 库把电商经营的完整工作链沉淀为 **13 个 Skill**：**先感知判断（顾问团），再产出交付（执行链）**，总控负责路由和编排。

## 成员总览

### 🎯 总控（1）

| Skill | 用途 |
|---|---|
| [ecommerce-master](./ecommerce-master/) | 电商运营总控：分诊问题 → 路由到最合适的 Skill → 编排多 Skill 链路 |

### ⚙️ 执行链（5，产出型）

| Skill | 什么时候用 | 产出 |
|---|---|---|
| [ecommerce-product-selection](./ecommerce-product-selection/) | 选品/爆款判断、这个品能不能上 | 选品评估报告（A/B/C/D 结论 + 盈利测算 + 测款计划） |
| [ecommerce-activity-planning](./ecommerce-activity-planning/) | 大促/活动策划、双11/618、店庆 | 完整活动方案（目标拆解/玩法/备货/预算/风险预案） |
| [ecommerce-traffic-operations](./ecommerce-traffic-operations/) | 投广告、预算分配、流量不够 | 投放计划（渠道组合/出价素材/预算分配/止损线） |
| [ecommerce-data-analysis](./ecommerce-data-analysis/) | 数据跌了、转化率低、要归因 | 诊断报告 + 行动建议（证据分级） |
| [ecommerce-review](./ecommerce-review/) | 活动/月度/季度经营复盘 | 复盘报告（C-I-S-S 经验提炼 + 可追踪行动项） |

### 🧭 顾问团（7，判断型）

| Skill | 视角 | 擅长 |
|---|---|---|
| [ecommerce-advisory-board](./ecommerce-advisory-board/) | 顾问团总控 | 路由 / 多专家评审会 |
| [ecommerce-advisor-huang](./ecommerce-advisor-huang/) | 黄若（零售效率） | 这生意值不值得做、怎么长期赢 |
| [ecommerce-advisor-xiaomali](./ecommerce-advisor-xiaomali/) | 小马宋（营销转化） | 产品怎么好卖、转化怎么提 |
| [ecommerce-advisor-wuya](./ecommerce-advisor-wuya/) | 无涯（电商操盘） | 打法定夺、节奏选择、少走弯路 |
| [ecommerce-method-see-ecommerce](./ecommerce-method-see-ecommerce/) | 《我看电商》 | 电商模式可行性、零售效率 |
| [ecommerce-method-alibaba-sales](./ecommerce-method-alibaba-sales/) | 《阿里铁军销售法》 | 目标倒推、客户分层、话术 SOP |
| [ecommerce-method-growth-hacking](./ecommerce-method-growth-hacking/) | 《增长黑客》 | 低成本验证增长点、北极星指标 |

## 建议使用路径

```
第一次用：先找 ecommerce-master，说清你的问题 → 它告诉你该用哪个
明确场景：直接调对应执行链 Skill（如"帮我复盘上个月经营"→ ecommerce-review）
要专家意见：ecommerce-advisory-board 开评审会，或直接调某位顾问
```

## 安装方式

每个 Skill 是独立目录（SKILL.md + README.md + SOURCES.md），复制到你的 Agent 技能目录即可。
全套复制后，先体验 `ecommerce-master` 的路由，再按需深入单个 Skill。

## 是什么保证质量

- **调研驱动**：专家/方法论均经蒸馏，心智模型/决策规则标注来源与诚实边界（见 `references/research/`）
- **参考模板**：每个执行链 Skill 带 `references/*-template.md` 完整输出模板（含每节写作指引），SKILL.md 保持轻量（判断+工作流），生成时按模板输出——借鉴自 pm-prd-writer 的成熟做法
- **不编造**：交付物基于你提供的真实材料，信息不足标注 [待确认]
- **证据分级**：数据结论区分 A（数据支持）/ B（强推断）/ C（推测）
- **诚实边界**：每个 Skill 明确写"做不到什么"，不夸大适用范围

## 调研时间戳

2026-09。调研快照与专家/书籍蒸馏见 `references/research/`。

---

> 本职业 Skill 套件由 [陆羽Skill](https://github.com/Luyu2026/Skill-Bible/tree/main/luyu-skill) 生成。
> 哪个专家/哪本书/哪个执行场景不符合预期，告诉我，我单独重做那一个。
