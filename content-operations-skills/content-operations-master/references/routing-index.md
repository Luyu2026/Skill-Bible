# content-operations-master · 路由索引

> 本文件是 content-operations-master 的分诊规则、路由表与预置链路索引，供 Agent 路由时快速查表。
> SKILL.md 保持轻量，路由细节在此维护；SKILL.md 中「核心判断」表格与此保持一致。

## 单点路由表

| 用户说 | 卡点 | 路由到 |
|---|---|---|
| 「内容该怎么做」「没方向」「不知道发什么」 | 策略缺失 | `content-operations-strategy` |
| 「选题」「不知道写什么」 | 选题卡住 | `content-operations-topic` |
| 「帮我写/改文章」「文案不好」 | 生产卡住 | `content-operations-production` |
| 「发了没效果」「怎么分发」「要不要投流」 | 分发卡住 | `content-operations-distribution` |
| 「数据怎么看」「哪篇好」 | 复盘卡住 | `content-operations-analytics` |
| 「老板觉得没价值」「内容 ROI」 | 价值论证 | `content-operations-advisory-board`（顾问团） |

## 预置工作流链路

1. **从 0 到 1 搭内容体系**：strategy → topic → production → distribution → analytics（每周复盘循环）
2. **单篇内容全流程**：topic（定题）→ production（生产）→ distribution（分发）→ analytics（复盘，沉淀经验回 topic）
3. **数据异常诊断**：analytics 发现问题 → 判断是选题/生产/分发哪环 → 路由对应 Skill → 回到 analytics 验证

## 关键原则

- **内容为业务服务**：先问内容要服务什么业务目标（品牌/获客/留存/转化），不服务业务的内容是无根之萍
- **质量 > 数量**：宁可一篇精品，不发十篇水文
- **数据闭环**：每次生产→分发的数据必须回流到下次选题
