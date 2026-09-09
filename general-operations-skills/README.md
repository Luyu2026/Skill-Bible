# 通用运营岗位技能（General Operations Skills）

> 陆羽Skill 为「综合/通用运营」岗位生成的体系化 Skill 套件，涵盖运营完整工作链。侧重**做决策 + 产出质量**。
> 生成时间：2026-09 · 生成器：luyu-skill（元 Skill 工厂）

## 这套库解决什么

运营工作看起来零散——今天看数据、明天做活动、后天想选题，还要判断"这个动作值不值得做"。
这套 Skill 库把运营的完整工作链沉淀为 14 个 Skill：**先感知判断（顾问团），再产出交付（执行链）**，总控负责路由和编排。

## 成员总览

### 🎯 总控（1）

| Skill | 用途 |
|---|---|
| [operations-master](./operations-master/) | 运营工作总控：分诊问题 → 路由到最合适的 Skill → 编排多 Skill 链路 |

### ⚙️ 执行链（6，产出型）

| Skill | 什么时候用 | 产出 |
|---|---|---|
| [operations-strategy](./operations-strategy/) | 定季度/年度运营策略 | 策略文档（目标拆解/资源分配/节奏） |
| [operations-data-analysis](./operations-data-analysis/) | 数据跌了/指标异常/要归因 | 诊断报告 + 行动建议（证据分级） |
| [operations-activity-planner](./operations-activity-planner/) | 做活动/大促策划 | 完整活动方案（含 ROI 测算/风控） |
| [operations-content-strategy](./operations-content-strategy/) | 内容选题/内容计划 | 选题清单 + 内容排期 |
| [operations-user-segmentation](./operations-user-segmentation/) | 用户分层/触达策略/唤醒 | 分层体系 + 差异化策略 |
| [operations-review](./operations-review/) | 活动/项目/月度复盘 | 复盘报告 + 可追踪行动项 |

### 🧭 顾问团（7，判断型）

| Skill | 视角 | 擅长 |
|---|---|---|
| [operations-advisory-board](./operations-advisory-board/) | 顾问团总控 | 路由 / 多专家评审会 |
| [operations-advisor-huang](./operations-advisor-huang/) | 黄有璨（运营价值） | 值不值得做、做局/破局 |
| [operations-advisor-zhang](./operations-advisor-zhang/) | 张亮（运营体系） | 体系怎么搭、执行质量 |
| [operations-advisor-qu](./operations-advisor-qu/) | 曲卉（增长实验） | 看什么指标、实验设计 |
| [operations-method-light-of-operations](./operations-method-light-of-operations/) | 《运营之光》 | 做局破局、运营思维 |
| [operations-method-lean-analytics](./operations-method-lean-analytics/) | 《精益数据分析》 | 第一关键指标 OMTM、数据诊断 |
| [operations-method-growth-hacking](./operations-method-growth-hacking/) | 《增长黑客》 | 增长实验循环、北极星指标 |

## 建议使用路径

```
第一次用：先找 operations-master，说清你的问题 → 它告诉你该用哪个
明确场景：直接调对应执行链 Skill（如"帮我复盘上个月活动"→ operations-review）
要专家意见：operations-advisory-board 开评审会，或直接调某位顾问
```

## 安装方式

每个 Skill 是独立目录（SKILL.md + README.md + SOURCES.md），复制到你的 Agent 技能目录即可。
全套复制后，先体验 `operations-master` 的路由，再按需深入单个 Skill。

## 是什么保证质量

- **调研驱动**：3 位专家 + 3 本书均经专项调研（见 `references/research/`），心智模型/决策规则标注来源与诚实边界
- **不编造**：交付物基于你提供的真实材料，信息不足标注 [待确认]
- **证据分级**：数据结论区分 A（数据支持）/ B（强推断）/ C（推测）

## 调研时间戳与来源

- 调研时间：2026-09 · 方法：陆羽Skill（nuwa 蒸馏方法论 + career.skill 工厂流程）
- 所有来源与参考机制见每个 Skill 的 `SOURCES.md` 与 `references/research/`

## 迭代建议

哪个专家/哪本书/哪个执行场景不符合预期？告诉陆羽Skill（luyu-skill），可单独重做那一个。