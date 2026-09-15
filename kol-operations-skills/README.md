# 海外KOL运营岗位技能（KOL Operations Skills）

> 陆羽Skill 为「海外KOL运营」岗位生成的体系化 Skill 套件，覆盖 KOL 营销完整工作链（策略 → 寻源 → 触达 → 共创 → 投放 → 分析）。侧重**做决策 + 产出质量**。
> 生成时间：2026-09 · 生成器：luyu-skill（元 Skill 工厂）

## 这套库解决什么

海外 KOL（网红/达人）营销链条长、环节多：先定策略（平台/分层/预算）、再找达人（筛选/评估）、然后触达谈判（报价/条款）、内容共创（Brief/审核）、投放执行（排期/追踪）、最后数据分析（效果/复投）。每个环节都容易踩坑，且判断类问题（选哪个达人、报价是否合理）和执行类问题（怎么写 Brief）交织。

这套库把 KOL 营销完整工作链沉淀为 14 个 Skill：**先感知判断（顾问团），再产出交付（执行链）**，总控负责路由和编排。

## 成员总览

### 🎯 总控（1）

| Skill | 用途 |
|---|---|
| [kol-operations-master](./kol-operations-master/) | KOL 运营工作总控：分诊问题 → 路由到最合适的 Skill → 编排多 Skill 链路 |

### ⚙️ 执行链（6，产出型）

| Skill | 什么时候用 | 产出 |
|---|---|---|
| [kol-operations-strategy](./kol-operations-strategy/) | 定 KOL 策略/预算/平台 | 策略文档（平台×分层×预算） |
| [kol-operations-discovery](./kol-operations-discovery/) | 找达人/筛选/评估 | 候选达人清单（对比表） |
| [kol-operations-outreach](./kol-operations-outreach/) | 联系达人/谈判/报价 | 触达方案 + 谈判策略 |
| [kol-operations-co-creation](./kol-operations-co-creation/) | 写 Brief/审脚本 | 内容 Brief + 审核清单 |
| [kol-operations-campaign](./kol-operations-campaign/) | 投放排期/追踪 | 执行计划 + 追踪表 |
| [kol-operations-analytics](./kol-operations-analytics/) | 效果分析/复投 | 效果报告 + 复投建议 |

### 🧭 顾问团（7，判断型）

| Skill | 视角 | 擅长 |
|---|---|---|
| [kol-operations-advisory-board](./kol-operations-advisory-board/) | 顾问团总控 | 路由 / 多专家评审会 |
| [kol-operations-advisor-garyvee](./kol-operations-advisor-garyvee/) | Gary Vee（内容营销） | 达人内容方向、账号增长 |
| [kol-operations-advisor-schaffer](./kol-operations-advisor-schaffer/) | Neal Schaffer（KOL 策略） | 策略漏斗、合作方式、长期关系 |
| [kol-operations-advisor-hennessy](./kol-operations-advisor-hennessy/) | Brittany Hennessy（报价谈判） | 报价评估、谈判、合同 |
| [kol-operations-method-influencer](./kol-operations-method-influencer/) | 《Influencer》 | 分层金字塔、费率定价 |
| [kol-operations-method-contagious](./kol-operations-method-contagious/) | 《Contagious》 | 内容传染性设计（STEPPS） |
| [kol-operations-method-leverage](./kol-operations-method-leverage/) | 《Contagious》传播机制 | 杠杆式传播（低成本撬动） |

## 建议使用路径

```
第一次用：先找 kol-operations-master，说清你的问题 → 它告诉你该用哪个
明确场景：直接调对应执行链 Skill（如"帮我找 20 个美国美妆达人"→ discovery）
要专家意见：kol-operations-advisory-board 开评审会，或直接调某位顾问
```

## 预置链路

- **A 从 0 到 1 KOL 投放**：strategy → discovery → outreach → co-creation → campaign → analytics
- **B 从效果问题到优化**：analytics（诊断）→ discovery / co-creation / outreach
- **C 判断先行**：advisory-board（条件化结论）→ 对应执行 Skill

## 安装方式

每个 Skill 是独立目录（SKILL.md + README.md + SOURCES.md，执行/方法论型另带 references/ 输出模板），复制到你的 Agent 技能目录即可。全套复制后，先体验 `kol-operations-master` 的路由，再按需深入单个 Skill。

## 是什么保证质量

- **调研驱动**：3 位专家 + 3 本书均经专项调研（见 `references/research/`），心智模型/决策规则标注来源与诚实边界
- **参考模板**：6 个执行链 + 3 个方法论 Skill 带 `references/*-template.md` 完整输出模板（含每节写作指引），SKILL.md 保持轻量——luyu-skill 固化的最佳实践
- **不编造**：交付物基于你提供的真实材料，信息不足标注 [待确认]
- **证据分级**：数据结论区分 A（数据支持）/ B（强推断）/ C（推测）

## 调研时间戳与来源

- 调研时间：2026-09 · 方法：陆羽Skill（nuwa 蒸馏方法论 + career.skill 工厂流程）
- 专家：Gary Vee / Neal Schaffer / Brittany Hennessy；书籍：《Influencer》《Contagious》（05 内容传染性设计 + 06 杠杆式传播两个角度）
- 所有来源与参考机制见每个 Skill 的 `SOURCES.md` 与 `references/research/`

## 迭代建议

哪个专家/哪本书/哪个执行场景不符合预期？告诉陆羽Skill（luyu-skill），可单独重做那一个。