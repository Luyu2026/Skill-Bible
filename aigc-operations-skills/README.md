# AIGC 运营岗位技能（AIGC Operations）

> 陆羽Skill 为「AIGC 运营」岗位生成的体系化 Skill 套件（用 AI 工具改造运营工作方式），覆盖完整链路：**Prompt 基本功 → AIGC 内容 → 智能客服 → 数据分析 → 工作流设计 → 评估合规 → 提效复盘**。
> 生成时间：2026-09-30 · 生成器：luyu-skill（元 Skill 工厂）

## 套件结构

```
aigc-operations-master/       # 🎯 总控：分诊 → 路由 → 编排
├── 执行链（产出型）   # 每个执行链带 references/*-template.md 输出模板
└── 顾问团（判断型）   # 子总控 + 3 专家视角 + 3 方法论
```

## 完整 Skill 清单

### 🎯 总控（1）

| Skill | 说明 |
|---|---|
| [aigc-operations-master](./aigc-operations-master/) | AI 提效总控：分诊问题 → 路由到最合适的 Skill → 编排多 Skill 链路 |

### ⚙️ 执行链（7，产出型）

| Skill | 什么时候用 | 产出 |
|---|---|---|
| [aigc-operations-prompt](./aigc-operations-prompt/) | Prompt怎么写/AI工具怎么选 | Prompt 库 + 工具选型方案 |
| [aigc-operations-content](./aigc-operations-content/) | AI写文案/AI做图/内容提效 | AIGC 内容生产 SOP（人机协作） |
| [aigc-operations-chatbot](./aigc-operations-chatbot/) | AI客服/对话式获客 | 智能客服方案（话术库/人机切换） |
| [aigc-operations-analysis](./aigc-operations-analysis/) | AI分析数据/AI写报告 | AI 分析 SOP（取数/洞察/报告） |
| [aigc-operations-workflow](./aigc-operations-workflow/) | AI工作流/团队AI化 | 工作流改造方案（任务拆解/AI嵌入点） |
| [aigc-operations-evaluation](./aigc-operations-evaluation/) | AI产出行不行/合规/幻觉 | 评估与合规检查清单 |
| [aigc-operations-review](./aigc-operations-review/) | AI提效复盘/值不值得用 | 提效复盘报告（效率/质量/成本） |

### 🧭 顾问团（7，判断型）

| Skill | 说明 |
|---|---|
| [aigc-operations-advisory-board](./aigc-operations-advisory-board/) | 顾问团总控：路由 + 评审会模式 + 分歧地图 |
| [aigc-operations-advisor-mollick](./aigc-operations-advisor-mollick/) | Ethan Mollick：AI 协作/人在回路/锯齿边界 |
| [aigc-operations-advisor-renxin](./aigc-operations-advisor-renxin/) | 任鑫：工作流嵌入/场景×工具×流程 |
| [aigc-operations-advisor-fanbing](./aigc-operations-advisor-fanbing/) | 范冰：工具选型/效果数据验证/实验 |
| [aigc-operations-method-cointelligence](./aigc-operations-method-cointelligence/) | 《Co-Intelligence》：AI 协作方法论 |
| [aigc-operations-method-ai2041](./aigc-operations-method-ai2041/) | 《AI 2041》：AI 场景方法论 |
| [aigc-operations-method-comingwave](./aigc-operations-method-comingwave/) | 《The Coming Wave》：AI 治理方法论 |

## 什么时候用

| 场景 | 用哪个 |
|---|---|
| 「Prompt怎么写」「AI不好用」 | master → prompt |
| 「AI写文案」「内容提效」 | master → content |
| 「AI客服」「对话获客」 | master → chatbot |
| 「AI分析数据」「AI写报告」 | master → analysis |
| 「AI工作流」「团队AI化」 | master → workflow |
| 「AI产出行不行」「合规」 | master → evaluation |
| 「AI提效复盘」 | master → review |
| 「这个AI化方向行不行」「专家评审」 | advisory-board（评审会） |

## 质量保障

- 调研材料：`references/research/`（行业调研 + 3 专家蒸馏 + 3 方法论提炼）
- 执行链均带 `references/*-template.md` 输出模板（可复用/可迭代）
- 每个 Skill 均含 SKILL.md + README.md + SOURCES.md
- 内部 Skill 互相引用形成完整链路（master 路由 → 执行链 → 顾问团判断）
- 专家组合避开已有套件全部人选：Ethan Mollick/任鑫/范冰 + 《Co-Intelligence》《AI 2041》《The Coming Wave》
- 中国语境配置项：国产工具生态（豆包/Kimi/即梦）、深度合成标识、数据安全边界（见各 Skill 边界）
- **门槛定位**：低于 AI 产品运营（无需懂模型原理），但强调"人机协作"与"会设计工作流"才是竞争力——执行链侧重场景选择与质量控制

## 定位说明

本套件聚焦 **AIGC 运营**（用 AI 做运营），与 [ai-operations-skills](./ai-operations-skills/)（运营 AI 产品）互补，构成 AI 运营两大分类。适合入门/转岗（门槛低）与团队 AI 化（价值高）。
