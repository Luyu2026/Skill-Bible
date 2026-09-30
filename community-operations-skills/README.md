# 社区运营岗位技能（Community Operations）

> 陆羽Skill 为「社区运营」岗位生成的体系化 Skill 套件，覆盖社区运营完整工作链：**社区定位 → 成员招募 → 活跃机制 → 内容生态 → 社区活动 → 商业化 → 数据复盘**。
> 生成时间：2026-09-30 · 生成器：luyu-skill（元 Skill 工厂）

## 套件结构

```
community-operations-master/        # 🎯 总控：分诊 → 路由 → 编排
├── 执行链（产出型）   # 每个执行链带 references/*-template.md 输出模板
└── 顾问团（判断型）   # 子总控 + 3 专家视角 + 3 方法论
```

## 完整 Skill 清单

### 🎯 总控（1）

| Skill | 说明 |
|---|---|
| [community-operations-master](./community-operations-master/) | 社区运营总控：分诊问题 → 路由到最合适的 Skill → 编排多 Skill 链路 |

### ⚙️ 执行链（7，产出型）

| Skill | 什么时候用 | 产出 |
|---|---|---|
| [community-operations-positioning](./community-operations-positioning/) | 社区怎么定位/建什么群/规则 | 社区定位卡（人群/主题/归属感/规则） |
| [community-operations-recruitment](./community-operations-recruitment/) | 怎么拉人/冷启动/种子用户 | 招募方案（渠道/话术/种子策略） |
| [community-operations-engagement](./community-operations-engagement/) | 社区不活跃/死群/促活 | 活跃机制方案（话题/仪式/激励） |
| [community-operations-content](./community-operations-content/) | 社区没内容/UGC 引导 | 内容生态方案（UGC/官方/沉淀） |
| [community-operations-activity](./community-operations-activity/) | 社区活动/线上线下面基 | 社区活动方案（目标/形式/流程） |
| [community-operations-monetization](./community-operations-monetization/) | 社区怎么赚钱/变现 | 商业化方案（路径/时机/阶梯） |
| [community-operations-review](./community-operations-review/) | 数据复盘/违规治理 | 复盘报告（结构/健康度/治理） |

### 🧭 顾问团（7，判断型）

| Skill | 说明 |
|---|---|
| [community-operations-advisory-board](./community-operations-advisory-board/) | 顾问团总控：路由 + 评审会模式 + 分歧地图 |
| [community-operations-advisor-spinks](./community-operations-advisor-spinks/) | David Spinks：归属感生意/生命周期/社区驱动增长 |
| [community-operations-advisor-millington](./community-operations-advisor-millington/) | Richard Millington：目标驱动/贡献者金字塔/密度×质量 |
| [community-operations-advisor-luyan](./community-operations-advisor-luyan/) | 卢彦：社群三角/先社群后商业/情感经营 |
| [community-operations-method-buzzing](./community-operations-method-buzzing/) | 《Buzzing Communities》：社区管理方法论 |
| [community-operations-method-belonging](./community-operations-method-belonging/) | 《The Business of Belonging》：社区商业方法论 |
| [community-operations-method-shequnsiwei](./community-operations-method-shequnsiwei/) | 《社群思维》：中国社群方法论 |

## 什么时候用

| 场景 | 用哪个 |
|---|---|
| 「社区怎么定位」「建什么群」 | master → positioning |
| 「怎么拉人」「冷启动」 | master → recruitment |
| 「社区不活跃」「死群」 | master → engagement |
| 「社区没内容」「UGC」 | master → content |
| 「社区活动」「搞个活动」 | master → activity |
| 「社区怎么赚钱」「变现」 | master → monetization |
| 「数据复盘」「违规处理」 | master → review |
| 「这个方向行不行」「专家评审」 | advisory-board（评审会） |

## 质量保障

- 调研材料：`references/research/`（行业调研 + 3 专家蒸馏 + 3 方法论提炼）
- 执行链均带 `references/*-template.md` 输出模板（可复用/可迭代）
- 每个 Skill 均含 SKILL.md + README.md + SOURCES.md
- 内部 Skill 互相引用形成完整链路（master 路由 → 执行链 → 顾问团判断）
- 专家组合避开已有套件（私域/用户/活动/内容/新媒体/增长）重复：Spinks/Millington/卢彦 + 《Buzzing Communities》《The Business of Belonging》《社群思维》
- 中国语境配置项：微信群合规（群聊监管）、私域变现、关系链裂变（见各 Skill 边界）
