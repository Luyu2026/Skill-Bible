# 商业化运营岗位技能（Commercial Operations Skills）

> 陆羽Skill 为「商业化运营」岗位生成的体系化 Skill 套件，涵盖商业化完整工作链。侧重**做决策 + 产出质量**。
> 生成时间：2026-09 · 生成器：[陆羽Skill](https://github.com/Luyu2026/Skill-Bible/tree/main/luyu-skill)（元 Skill 工厂）

## 这套库解决什么

商业化运营是"让业务赚钱"的工作——从商业模式设计、定价、会员订阅、广告变现到收入诊断与复盘。这套 Skill 库把商业化完整工作链沉淀为 **14 个 Skill**：**先感知判断（顾问团），再产出交付（执行链）**，总控负责路由和编排。

## 成员总览

### 🎯 总控（1）

| Skill | 用途 |
|---|---|
| [commercial-master](./commercial-master/) | 商业化运营总控：分诊问题 → 路由到最合适的 Skill → 编排多 Skill 链路 |

### ⚙️ 执行链（6，产出型）

| Skill | 什么时候用 | 产出 |
|---|---|---|
| [commercial-strategy](./commercial-strategy/) | 商业模式、变现路径、商业化蓝图 | 商业化蓝图（模式评估/优先级/三阶段路径） |
| [commercial-pricing](./commercial-pricing/) | 定价、涨价、降价、价格策略 | 定价方案（盈亏平衡价/策略/价格带） |
| [commercial-membership](./commercial-membership/) | 会员体系、订阅、权益设计 | 会员方案（锚点/权益梯度/价格档/续费） |
| [commercial-ads](./commercial-ads/) | 广告变现、流量变现、广告位 | 广告变现方案（组合/收入测算/体验平衡） |
| [commercial-diagnostics](./commercial-diagnostics/) | 收入跌了、商业化数据、LTV 异常 | 诊断报告（归因/健康度/行动建议） |
| [commercial-review](./commercial-review/) | 季度/年度商业化复盘 | 复盘报告（对账/归因/C-I-S-S/行动项） |

### 🧭 顾问团（7，判断型）

| Skill | 视角 | 擅长 |
|---|---|---|
| [commercial-advisory-board](./commercial-advisory-board/) | 顾问团总控 | 路由 / 多专家评审会 |
| [commercial-advisor-liurun](./commercial-advisor-liurun/) | 刘润（商业洞察） | 生意值不值得做、模式靠不靠谱 |
| [commercial-advisor-wangsai](./commercial-advisor-wangsai/) | 王赛（增长战略） | 增长从哪里来、战略取舍 |
| [commercial-advisor-songxing](./commercial-advisor-songxing/) | 宋星（数据驱动） | 用户/流量怎么变现实效最好 |
| [commercial-method-growthfive](./commercial-method-growthfive/) | 《增长五线》 | 增长路径设计 |
| [commercial-method-leananalytics](./commercial-method-leananalytics/) | 《精益数据分析》 | 找到最重要指标、验证决策 |
| [commercial-method-membership](./commercial-method-membership/) | 《订阅经济》 | 会员/订阅模式设计 |

## 建议使用路径

```
第一次用：先找 commercial-master，说清你的问题 → 它告诉你该用哪个
明确场景：直接调对应执行链 Skill（如"帮我定个价"→ commercial-pricing）
要专家意见：commercial-advisory-board 开评审会，或直接调某位顾问
```

## 安装方式

每个 Skill 是独立目录（SKILL.md + README.md + SOURCES.md），复制到你的 Agent 技能目录即可。
全套复制后，先体验 `commercial-master` 的路由，再按需深入单个 Skill。

## 演示工作包

从执行链中挑选最能代表真实工作价值的 2 个场景，制作了可公开展示的完整交付样稿（**数据均为模拟**，替换真实业务数据后可直接用于开会/决策/执行）：

| 演示包 | 场景 | 对应 Skill |
|---|---|---|
| [定价方案演示：SaaS 涨价决策](./commercial-pricing/references/demo/demo-commercial-pricing.md) | 涨不涨价？涨多少？怎么涨不流失？ | `commercial-pricing` |
| [商业化诊断演示：收入连续两季下滑](./commercial-diagnostics/references/demo/demo-commercial-diagnostics.md) | 收入为什么跌？是模式、定价还是留存问题？ | `commercial-diagnostics` |

> 演示规范见 `references/demo-document-standard.md`。

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