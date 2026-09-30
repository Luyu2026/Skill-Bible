# 小红书运营岗位技能（Xiaohongshu Operations Skills）

> 陆羽Skill 为「小红书运营」岗位生成的体系化 Skill 套件，涵盖小红书账号完整运营链。侧重**做决策 + 产出质量**。
> 生成时间：2026-10 · 生成器：[陆羽Skill](https://github.com/Luyu2026/Skill-Bible/tree/main/luyu-skill)（元 Skill 工厂）

## 这套库解决什么

小红书运营是"从起号到变现"的完整工作链：定位、内容、视觉、发布、增长、变现。这套 Skill 库把小红书全链路沉淀为 **14 个 Skill**：**先感知判断（顾问团），再产出交付（执行链）**，总控负责路由和编排。

## 成员总览

### 🎯 总控（1）

| Skill | 用途 |
|---|---|
| [xhs-master](./xhs-master/) | 小红书运营总控：分诊问题 → 路由到最合适的 Skill → 编排多 Skill 链路 |

### ⚙️ 执行链（6，产出型）

| Skill | 什么时候用 | 产出 |
|---|---|---|
| [xhs-account](./xhs-account/) | 起号、定位、人设搭建 | 账号定位卡（定位一句话/人设/栏目） |
| [xhs-content](./xhs-content/) | 选题、笔记创作、标题 | 笔记方案（标题/正文/标签/SEO词） |
| [xhs-visual](./xhs-visual/) | 封面、配图、排版、视频 | 视觉方案（风格/封面/图序） |
| [xhs-publish](./xhs-publish/) | 发布、互动、评论运营 | 发布计划（时机/频率/互动策略） |
| [xhs-growth](./xhs-growth/) | 涨粉、数据复盘、爆款拆解 | 增长复盘（爆款要素/扑街归因） |
| [xhs-monetization](./xhs-monetization/) | 变现、接广、带货、引流 | 变现方案（路径/测算/风险） |

### 🧭 顾问团（7，判断型）

| Skill | 视角 | 擅长 |
|---|---|---|
| [xhs-advisory-board](./xhs-advisory-board/) | 顾问团总控 | 路由 / 多专家评审会 |
| [xhs-advisor-maowenchao](./xhs-advisor-maowenchao/) | 猫文超（运营实战） | 账号运营打法、流量逻辑 |
| [xhs-advisor-qufan](./xhs-advisor-qufan/) | 曲凡（生活方式内容） | 内容气质、种草设计 |
| [xhs-advisor-fangqi](./xhs-advisor-fangqi/) | 方琦（视频与直播） | 视频/直播内容打法 |
| [xhs-method-weakcommunication](./xhs-method-weakcommunication/) | 《弱传播》 | 叙事视角、共鸣设计 |
| [xhs-method-copywriting-manual](./xhs-method-copywriting-manual/) | 《文案创作完全手册》 | 标题/文案打磨 |
| [xhs-method-superip](./xhs-method-superip/) | 《超级IP》 | 人设IP、粉丝经营 |

## 建议使用路径

```
第一次用：先找 xhs-master，说清你的问题 → 它告诉你该用哪个
明确场景：直接调对应执行链 Skill（如"帮我写篇种草笔记"→ xhs-content）
要专家意见：xhs-advisory-board 开评审会，或直接调某位顾问
```

## 安装方式

每个 Skill 是独立目录（SKILL.md + README.md + SOURCES.md），复制到你的 Agent 技能目录即可。
全套复制后，先体验 `xhs-master` 的路由，再按需深入单个 Skill。

## 演示工作包

从执行链中挑选最能代表真实工作价值的 1 个场景，制作了可公开展示的完整交付样稿（**数据均为模拟**，替换真实业务数据后可直接用于决策/执行）：

| 演示包 | 场景 | 对应 Skill |
|---|---|---|
| [笔记方案演示：出租屋改造种草笔记](./xhs-content/references/demo/demo-xhs-content.md) | 一篇从小白到达人的种草笔记 | `xhs-content` |

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