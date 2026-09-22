# product-operations-master · 路由索引

> 本文件是 product-operations-master 的分诊规则、路由表与预置链路索引，供 Agent 路由时快速查表。
> SKILL.md 保持轻量，路由细节在此维护；SKILL.md 中「核心判断」表格与此保持一致。

## 单点路由表

| 用户说 | 卡点 | 路由到 |
|---|---|---|
| 「产品上线后怎么运营」「没方向」 | 运营策略缺失 | `product-operations-strategy` |
| 「用户不用/留存差」「激活率低」 | 激活/留存卡住 | `product-operations-activation` |
| 「激励体系怎么设计」「积分/等级」 | 激励设计卡住 | `product-operations-incentive` |
| 「数据怎么看」「迭代方向」 | 数据决策卡住 | `product-operations-data` |
| 「版本怎么规划」「上线节奏」 | 版本运营卡住 | `product-operations-release` |
| 「用户反馈怎么处理」「需求池」 | 反馈闭环卡住 | `product-operations-feedback` |
| 「产品运营方向判断」「值不值得做」 | 价值判断 | `product-operations-advisory-board`（顾问团） |

## 预置工作流链路

1. **从 0 到 1 产品运营**：strategy（定策略）→ activation（激活）→ incentive（激励）→ data（数据迭代）→ release（版本节奏）
2. **留存/激活问题诊断**：data 发现问题 → 判断是激活/激励/产品问题 → 路由对应 Skill → 回到 data 验证
3. **新版本上线**：feedback（收集需求）→ release（规划版本）→ data（验证效果）

## 关键原则

- **用户价值第一**：一切运营动作先问「给用户创造什么价值」（俞军：用户价值 = 新体验 - 旧体验 - 替换成本）
- **数据驱动**：迭代方向来自数据，不来自感觉
- **激励为行为服务**：激励体系设计围绕「想让用户做的行为」，不是为激励而激励
- **生命周期视角**：不同阶段（引入/成长/成熟/衰退）运营重点不同
