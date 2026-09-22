# activity-operations-master · 路由索引

> 本文件是 activity-operations-master 的分诊规则、路由表与预置链路索引，供 Agent 路由时快速查表。
> SKILL.md 保持轻量，路由细节在此维护；SKILL.md 中「核心判断」表格与此保持一致。

## 单点路由表

| 用户说 | 卡点 | 路由到 |
|---|---|---|
| 「办什么活动」「活动目标怎么定」 | 目标/方向缺失 | `activity-operations-planning` |
| 「活动方案怎么做」「帮我出方案」 | 策划卡住 | `activity-operations-planning` |
| 「裂变/老带新/打卡怎么设计」 | 机制设计卡住 | `activity-operations-mechanics` |
| 「活动执行」「分工/排期/物料」 | 执行卡住 | `activity-operations-execution` |
| 「活动没人参加/没传播」「怎么推广」 | 传播卡住 | `activity-operations-promotion` |
| 「活动效果怎么评估」「复盘」 | 复盘卡住 | `activity-operations-review` |
| 「活动点子行不行」「值不值得办」 | 价值判断 | `activity-operations-advisory-board`（顾问团） |

## 预置工作流链路

1. **从 0 到 1 办活动**：planning（定目标）→ mechanics（设计机制）→ execution（执行落地）→ promotion（传播放大）→ review（复盘沉淀）
2. **活动效果不佳诊断**：review 发现问题 → 判断是目标/机制/执行/传播哪环 → 路由对应 Skill → 回到 review 验证
3. **快速小活动**：planning（轻量版）→ execution → review（一页纸复盘）

## 关键原则

- **目标先行**：先问活动服务什么业务目标（拉新/促活/转化/品牌），没有目标的活动是自嗨
- **ROI 意识**：每个活动要能算账（成本 vs 收益），不能算账的活动不做
- **机制 > 创意**：活动的核心是机制设计（为什么用户愿意参与/分享），不是噱头
- **数据闭环**：每次活动数据必须回流到下次策划
