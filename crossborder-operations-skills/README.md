# 跨境电商运营岗位技能（Cross-border Operations Skills）

> 陆羽Skill 为「跨境电商运营」岗位生成的体系化 Skill 套件，涵盖跨境出海完整工作链。侧重**做决策 + 产出质量**。
> 生成时间：2026-10 · 生成器：[陆羽Skill](https://github.com/Luyu2026/Skill-Bible/tree/main/luyu-skill)（元 Skill 工厂）

## 这套库解决什么

跨境电商运营是"把货卖到海外"的完整工作链：平台选择、选品、Listing、投放、履约、数据。这套 Skill 库把跨境出海完整工作链沉淀为 **14 个 Skill**：**先感知判断（顾问团），再产出交付（执行链）**，总控负责路由和编排。

## 成员总览

### 🎯 总控（1）

| Skill | 用途 |
|---|---|
| [crossborder-master](./crossborder-master/) | 跨境电商运营总控：分诊问题 → 路由到最合适的 Skill → 编排多 Skill 链路 |

### ⚙️ 执行链（6，产出型）

| Skill | 什么时候用 | 产出 |
|---|---|---|
| [crossborder-platform](./crossborder-platform/) | 选平台、入驻、平台对比 | 平台评估报告 + 入驻路径 |
| [crossborder-selection](./crossborder-selection/) | 选品、货源、这个品能不能做 | 选品评估 A/B/C/D + 盈利测算 |
| [crossborder-listing](./crossborder-listing/) | Listing、标题、五点、转化率 | Listing 优化方案 + 关键词词库 |
| [crossborder-traffic](./crossborder-traffic/) | 广告、投放、ACOS、预算 | 投放计划 + 渠道组合 + 止损线 |
| [crossborder-service](./crossborder-service/) | 物流、履约、客服、退货、差评 | 履约方案 + 客服 SOP |
| [crossborder-data](./crossborder-data/) | 销量下滑、复盘、库存积压 | 诊断报告 + 行动建议 |

### 🧭 顾问团（7，判断型）

| Skill | 视角 | 擅长 |
|---|---|---|
| [crossborder-advisory-board](./crossborder-advisory-board/) | 顾问团总控 | 路由 / 多专家评审会 |
| [crossborder-advisor-chenxianting](./crossborder-advisor-chenxianting/) | 陈贤亭（行业趋势） | 行业前景、平台选择前瞻 |
| [crossborder-advisor-lipengbo](./crossborder-advisor-lipengbo/) | 李鹏博（模式方法论） | 模式判断、业务诊断 |
| [crossborder-advisor-wangshutong](./crossborder-advisor-wangshutong/) | 王树彤（平台生态） | 中小卖家机会、平台关系 |
| [crossborder-method-30](./crossborder-method-30/) | 《跨境电商3.0时代》 | 模式升级路径 |
| [crossborder-method-amazon](./crossborder-method-amazon/) | 《亚马逊运营从入门到精通》 | 平台运营实操 |
| [crossborder-method-dtc](./crossborder-method-dtc/) | 《DTC品牌出海》 | 独立站/品牌路线 |

## 建议使用路径

```
第一次用：先找 crossborder-master，说清你的问题 → 它告诉你该用哪个
明确场景：直接调对应执行链 Skill（如"帮我选个品"→ crossborder-selection）
要专家意见：crossborder-advisory-board 开评审会，或直接调某位顾问
```

## 安装方式

每个 Skill 是独立目录（SKILL.md + README.md + SOURCES.md），复制到你的 Agent 技能目录即可。
全套复制后，先体验 `crossborder-master` 的路由，再按需深入单个 Skill。

## 演示工作包

从执行链中挑选最能代表真实工作价值的 1 个场景，制作了可公开展示的完整交付样稿（**数据均为模拟**，替换真实业务数据后可直接用于决策/执行）：

| 演示包 | 场景 | 对应 Skill |
|---|---|---|
| [选品评估演示：便携榨汁杯要不要做](./crossborder-selection/references/demo/demo-crossborder-selection.md) | 亚马逊新品选品决策 | `crossborder-selection` |

> 演示规范见 `references/demo-document-standard.md`。

## 是什么保证质量

- **调研驱动**：专家/方法论均经蒸馏，心智模型/决策规则标注来源与诚实边界（见 `references/research/`）
- **参考模板**：每个执行链 Skill 带 `references/*-template.md` 完整输出模板（含每节写作指引），SKILL.md 保持轻量（判断+工作流）
- **不编造**：交付物基于你提供的真实材料，信息不足标注 [待确认]
- **证据分级**：数据结论区分 A（数据支持）/ B（强推断）/ C（推测）
- **诚实边界**：每个 Skill 明确写"做不到什么"，不夸大适用范围

## 调研时间戳

2026-10。调研快照与专家/书籍蒸馏见 `references/research/`。

---

> 本职业 Skill 套件由 [陆羽Skill](https://github.com/Luyu2026/Skill-Bible/tree/main/luyu-skill) 生成。
> 哪个专家/哪本书/哪个执行场景不符合预期，告诉我，我单独重做那一个。