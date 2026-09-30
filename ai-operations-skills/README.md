# AI 运营岗位技能（AI Operations）

> 陆羽Skill 为「AI 运营」岗位生成的体系化 Skill 套件，聚焦 **AI 产品运营**（运营 AI 应用/大模型产品），覆盖完整工作链：**产品定位 → 实验迭代 → 对话体验 → 内容生态 → 用户增长 → 商业化 → 数据复盘**。
> 生成时间：2026-09-30 · 生成器：luyu-skill（元 Skill 工厂）

## 套件结构

```
ai-operations-master/               # 🎯 总控：分诊 → 路由 → 编排
├── 执行链（产出型）   # 每个执行链带 references/*-template.md 输出模板
└── 顾问团（判断型）   # 子总控 + 3 专家视角 + 3 方法论
```

## 完整 Skill 清单

### 🎯 总控（1）

| Skill | 说明 |
|---|---|
| [ai-operations-master](./ai-operations-master/) | AI 运营总控：分诊问题 → 路由到最合适的 Skill → 编排多 Skill 链路 |

### ⚙️ 执行链（7，产出型）

| Skill | 什么时候用 | 产出 |
|---|---|---|
| [ai-operations-positioning](./ai-operations-positioning/) | AI产品怎么定位/做什么场景/PMF | 产品定位卡（场景/人群/差异化/人机分工） |
| [ai-operations-experiment](./ai-operations-experiment/) | 做个实验/Prompt怎么调/效果对比 | 实验设计文档（假设/变量/指标/决策规则） |
| [ai-operations-chatbot](./ai-operations-chatbot/) | AI回答质量差/幻觉/兜底 | 体验诊断报告（质量/Prompt调优/兜底/幻觉治理） |
| [ai-operations-content](./ai-operations-content/) | 模板库/Prompt库/用户共创 | 内容生态方案（模板/UGC/沉淀） |
| [ai-operations-growth](./ai-operations-growth/) | AI产品怎么增长/获客/新鲜感衰减 | 增长方案（增长循环/激活/口碑/依赖养成） |
| [ai-operations-monetization](./ai-operations-monetization/) | 怎么收费/定价/成本高 | 商业化方案（定价模式/成本核算/增值） |
| [ai-operations-review](./ai-operations-review/) | 数据复盘/成本治理/质量监控 | 复盘报告（质量/留存/成本三角） |

### 🧭 顾问团（7，判断型）

| Skill | 说明 |
|---|---|
| [ai-operations-advisory-board](./ai-operations-advisory-board/) | 顾问团总控：路由 + 评审会模式 + 分歧地图 |
| [ai-operations-advisor-ng](./ai-operations-advisor-ng/) | Andrew Ng：数据飞轮/数据为中心/AI转型 |
| [ai-operations-advisor-rachitsky](./ai-operations-advisor-rachitsky/) | Lenny Rachitsky：增长循环/激活/PMF |
| [ai-operations-advisor-lijiariu](./ai-operations-advisor-lijiariu/) | 李佳芮：AI+私域/对话式营销/场景选择 |
| [ai-operations-method-prediction](./ai-operations-method-prediction/) | 《Prediction Machines》：AI商业/人机分工 |
| [ai-operations-method-ageofai](./ai-operations-method-ageofai/) | 《Competing in the Age of AI》：数据网络效应/AI工厂 |
| [ai-operations-method-humanmachine](./ai-operations-method-humanmachine/) | 《Human + Machine》：人机协作/人在回路 |

## 什么时候用

| 场景 | 用哪个 |
|---|---|
| 「AI产品怎么定位」「做什么场景」 | master → positioning |
| 「做个实验」「Prompt怎么调」 | master → experiment |
| 「AI回答质量差」「幻觉」 | master → chatbot |
| 「模板库」「用户共创」 | master → content |
| 「AI产品怎么增长」 | master → growth |
| 「怎么收费」「成本高」 | master → monetization |
| 「数据复盘」「成本治理」 | master → review |
| 「这个AI方向行不行」「专家评审」 | advisory-board（评审会） |

## 质量保障

- 调研材料：`references/research/`（行业调研 + 3 专家蒸馏 + 3 方法论提炼）
- 执行链均带 `references/*-template.md` 输出模板（可复用/可迭代）
- 每个 Skill 均含 SKILL.md + README.md + SOURCES.md
- 内部 Skill 互相引用形成完整链路（master 路由 → 执行链 → 顾问团判断）
- 专家组合避开已有套件全部人选：Andrew Ng/Lenny Rachitsky/李佳芮 + 《Prediction Machines》《Competing in the Age of AI》《Human + Machine》
- AI 领域特性：质量×留存×成本三角是核心运营命题；中国语境配置项（生成式AI备案、Token成本、个保法数据飞轮限制）见各 Skill 边界
- **新兴领域降级路径**：AI 运营公开语料有限，专家/方法论均按 luyu-skill 降级标准处理（缩小规模、加大诚实边界、不编造）

## 定位说明

本套件聚焦 **AI 产品运营**（运营 AI 应用/大模型产品）。AI 运营的其他分类（AI 赋能传统运营提效、大模型 B 端生态运营）未纳入本套件，如需可按 luyu-skill 单独生成。
