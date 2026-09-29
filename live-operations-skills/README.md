# 直播运营岗位技能（Live Operations Skills）

> 陆羽Skill 为「直播运营」岗位生成的体系化 Skill 套件，涵盖直播完整工作链。侧重**做决策 + 产出质量**。
> 生成时间：2026-09 · 生成器：[陆羽Skill](https://github.com/Luyu2026/Skill-Bible/tree/main/luyu-skill)（元 Skill 工厂）

## 这套库解决什么

直播运营看似只有"开播"，实际是一条完整工作链：策划排品、写话术、控场、引流、投流、复盘。这套 Skill 库把直播的完整工作链沉淀为 **14 个 Skill**：**先感知判断（顾问团），再产出交付（执行链）**，总控负责路由和编排。

## 成员总览

### 🎯 总控（1）

| Skill | 用途 |
|---|---|
| [live-master](./live-master/) | 直播运营总控：分诊问题 → 路由到最合适的 Skill → 编排多 Skill 链路 |

### ⚙️ 执行链（6，产出型）

| Skill | 什么时候用 | 产出 |
|---|---|---|
| [live-session-planning](./live-session-planning/) | 策划一场直播、排品、定节奏 | 直播方案（目标拆解/排品表/备货/风险预案） |
| [live-script](./live-script/) | 写话术、逼单、开场白 | 话术脚本（开场/单品五段式/逼单/互动留人） |
| [live-hosting](./live-hosting/) | 控场、突发处理、开播前检查 | 控场 SOP（节奏把控/数据监控/突发预案/分工） |
| [live-feed](./live-feed/) | 短视频引流、切片、预告 | 引流计划（三阶段目标/选题/发布节奏/承接） |
| [live-ads](./live-ads/) | 投流、千川、直播间流量 | 投流计划（阶段策略/定向/出价/素材/止损线） |
| [live-analytics](./live-analytics/) | 复盘、场次数据、迭代 | 复盘报告（对账/环节拆解/C-I-S-S/行动项） |

### 🧭 顾问团（7，判断型）

| Skill | 视角 | 擅长 |
|---|---|---|
| [live-advisory-board](./live-advisory-board/) | 顾问团总控 | 路由 / 多专家评审会 |
| [live-advisor-li-jiaqi](./live-advisor-li-jiaqi/) | 李佳琦（直播转化） | 转化怎么提、选品标准、话术强度 |
| [live-advisor-dong-yuhui](./live-advisor-dong-yuhui/) | 董宇辉（内容直播） | 留人、内容差异化、人设打磨 |
| [live-advisor-luo-yonghao](./live-advisor-luo-yonghao/) | 罗永浩（直播生意） | 值不值得做、供应链、规模化 |
| [live-method-influence](./live-method-influence/) | 《影响力》 | 转化机制、逼单设计 |
| [live-method-contagious](./live-method-contagious/) | 《疯传》 | 切片传播、引流内容 |
| [live-method-conversion](./live-method-conversion/) | 《爆款文案》 | 话术卖点、痛点开场 |

## 建议使用路径

```
第一次用：先找 live-master，说清你的问题 → 它告诉你该用哪个
明确场景：直接调对应执行链 Skill（如"帮我写这场直播的话术"→ live-script）
要专家意见：live-advisory-board 开评审会，或直接调某位顾问
```

## 安装方式

每个 Skill 是独立目录（SKILL.md + README.md + SOURCES.md），复制到你的 Agent 技能目录即可。
全套复制后，先体验 `live-master` 的路由，再按需深入单个 Skill。

## 演示工作包

从执行链中挑选最能代表真实工作价值的 2 个场景，制作了可公开展示的完整交付样稿（**数据均为模拟**，替换真实业务数据后可直接用于开会/决策/执行）：

| 演示包 | 场景 | 对应 Skill |
|---|---|---|
| [话术脚本演示：一场女装直播](./live-script/references/demo/demo-live-script.md) | 从排品到逼单的完整话术脚本 | `live-script` |
| [直播复盘演示：GMV 未达标的场次诊断](./live-analytics/references/demo/demo-live-analytics.md) | 这场为什么没达标？下一场怎么改？ | `live-analytics` |

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
