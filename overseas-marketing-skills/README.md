# 海外市场营销岗位技能（Overseas Marketing Skills）

> 陆羽Skill 为「海外市场营销」岗位生成的体系化 Skill 套件，覆盖海外营销完整工作链（市场调研 → 品牌定位 → 内容/SEO → 付费投放 → 邮件营销 → 数据分析）。侧重**做决策 + 产出质量**。
> 生成时间：2026-09 · 生成器：luyu-skill（元 Skill 工厂）

## 这套库解决什么

海外营销（出海）的工作链条长、环节多：先调研市场、再定品牌定位、然后搭内容 SEO、投付费广告、做邮件转化、最后数据分析优化——每一步都容易踩坑，且判断类问题（该不该进这个市场、选哪个渠道）和执行类问题（怎么写方案）交织。

这套库把海外营销完整工作链沉淀为 14 个 Skill：**先感知判断（顾问团），再产出交付（执行链）**，总控负责路由和编排。

## 成员总览

### 🎯 总控（1）

| Skill | 用途 |
|---|---|
| [overseas-marketing-master](./overseas-marketing-master/) | 海外营销工作总控：分诊问题 → 路由到最合适的 Skill → 编排多 Skill 链路 |

### ⚙️ 执行链（6，产出型）

| Skill | 什么时候用 | 产出 |
|---|---|---|
| [overseas-marketing-research](./overseas-marketing-research/) | 想进入海外市场/验证市场机会 | 市场机会报告（评分矩阵选市场） |
| [overseas-marketing-branding](./overseas-marketing-branding/) | 品牌定位/差异化/品牌故事 | 品牌定位文档（定位句式+MVA） |
| [overseas-marketing-content-seo](./overseas-marketing-content-seo/) | SEO/内容营销/关键词研究 | 内容与 SEO 计划（关键词地图） |
| [overseas-marketing-paid-ads](./overseas-marketing-paid-ads/) | Google/Meta/社媒投放 | 广告投放计划（盈亏线+测试） |
| [overseas-marketing-email](./overseas-marketing-email/) | 邮件营销/自动化流 | 邮件策略（欢迎流/弃购流） |
| [overseas-marketing-analytics](./overseas-marketing-analytics/) | 营销数据/归因/ROAS | 数据分析报告（证据分级） |

### 🧭 顾问团（7，判断型）

| Skill | 视角 | 擅长 |
|---|---|---|
| [overseas-marketing-advisory-board](./overseas-marketing-advisory-board/) | 顾问团总控 | 路由 / 多专家评审会 |
| [overseas-marketing-advisor-godin](./overseas-marketing-advisor-godin/) | Seth Godin（营销哲学） | 品牌/内容方向、MVA |
| [overseas-marketing-advisor-patel](./overseas-marketing-advisor-patel/) | Neil Patel（增长实操） | SEO、渠道 ROI、内容执行 |
| [overseas-marketing-advisor-cialdini](./overseas-marketing-advisor-cialdini/) | Cialdini（说服心理） | 转化率、文案、定价心理 |
| [overseas-marketing-method-this-is-marketing](./overseas-marketing-method-this-is-marketing/) | 《This Is Marketing》 | MVA、制造改变、五步法 |
| [overseas-marketing-method-influence](./overseas-marketing-method-influence/) | 《影响力》 | 六大原则、预说服、转化优化 |
| [overseas-marketing-method-storybrand](./overseas-marketing-method-storybrand/) | 《StoryBrand》 | SB7 叙事、官网文案 |

## 建议使用路径

```
第一次用：先找 overseas-marketing-master，说清你的问题 → 它告诉你该用哪个
明确场景：直接调对应执行链 Skill（如"帮我做市场调研"→ research）
要专家意见：overseas-marketing-advisory-board 开评审会，或直接调某位顾问
```

## 预置链路

- **A 从 0 到 1 出海**：research（市场机会）→ branding（定位）→ content-seo（基建）→ paid-ads（冷启动）
- **B 数据问题到优化**：analytics（诊断）→ paid-ads / content-seo / email
- **C 判断先行**：advisory-board（条件化结论）→ 对应执行 Skill

## 安装方式

每个 Skill 是独立目录（SKILL.md + README.md + SOURCES.md，执行型另带 references/ 输出模板），复制到你的 Agent 技能目录即可。全套复制后，先体验 `overseas-marketing-master` 的路由，再按需深入单个 Skill。

## 是什么保证质量

- **调研驱动**：3 位专家 + 3 本书均经专项调研（见 `references/research/`），心智模型/决策规则标注来源与诚实边界
- **参考模板**：每个执行链 Skill 带 `references/*-template.md` 完整输出模板（含每节写作指引），SKILL.md 保持轻量（判断+工作流）——luyu-skill 固化的最佳实践
- **不编造**：交付物基于你提供的真实材料，信息不足标注 [待确认]
- **证据分级**：数据结论区分 A（数据支持）/ B（强推断）/ C（推测）

## 调研时间戳与来源

- 调研时间：2026-09 · 方法：陆羽Skill（nuwa 蒸馏方法论 + career.skill 工厂流程）
- 专家：Seth Godin / Neil Patel / Robert Cialdini；书籍：《This Is Marketing》《Influence》《Building a StoryBrand》
- 所有来源与参考机制见每个 Skill 的 `SOURCES.md` 与 `references/research/`

## 迭代建议

哪个专家/哪本书/哪个执行场景不符合预期？告诉陆羽Skill（luyu-skill），可单独重做那一个。