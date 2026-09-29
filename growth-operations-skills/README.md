# 增长运营岗位技能（Growth Operations）

> 陆羽Skill 为「增长运营」岗位生成的体系化 Skill 套件，覆盖增长运营完整工作链：**目标拆解 → 实验验证 → 激活优化 → 留存机制 → 渠道预算 → 数据诊断**。
> 生成时间：2026-09-29 · 生成器：luyu-skill（元 Skill 工厂）

## 套件结构

```
growth-operations-master/           # 🎯 总控：分诊 → 路由 → 编排
├── 执行链（产出型）   # 每个执行链带 references/*-template.md 输出模板
└── 顾问团（判断型）   # 子总控 + 3 专家视角 + 3 方法论
```

## 完整 Skill 清单

### 🎯 总控（1）

| Skill | 说明 |
|---|---|
| [growth-operations-master](./growth-operations-master/) | 增长运营总控：分诊问题 → 路由到最合适的 Skill → 编排多 Skill 链路 |

### ⚙️ 执行链（6，产出型）

| Skill | 什么时候用 | 产出 |
|---|---|---|
| [growth-operations-strategy](./growth-operations-strategy/) | 定增长目标/北极星指标/年度规划 | 增长策略文档（北极星/拆解树/假设库/路线图） |
| [growth-operations-experiment](./growth-operations-experiment/) | 做实验/A-B 测试/判断改动要不要上 | 实验设计文档 + 结果评估结论 |
| [growth-operations-activation](./growth-operations-activation/) | 新用户流失/激活率低/onboarding 优化 | 激活漏斗诊断 + 优化方案 |
| [growth-operations-retention](./growth-operations-retention/) | 留存低/用户流失/召回/习惯养成 | 留存机制方案（Hook/召回/实验） |
| [growth-operations-channel](./growth-operations-channel/) | 预算分配/渠道评估/CAC 太高 | 渠道评估表 + 预算分配建议 |
| [growth-operations-diagnosis](./growth-operations-diagnosis/) | 数据跌了/指标异常/增长复盘 | 诊断报告 + 行动建议（证据分级） |

### 🧭 顾问团（7，判断型）

| Skill | 说明 |
|---|---|
| [growth-operations-advisory-board](./growth-operations-advisory-board/) | 顾问团总控：路由 + 评审会模式 + 分歧地图 |
| [growth-operations-advisor-zhang-ximeng](./growth-operations-advisor-zhang-ximeng/) | 张溪梦：数据驱动增长/北极星/增长团队 |
| [growth-operations-advisor-andrew-chen](./growth-operations-advisor-andrew-chen/) | Andrew Chen：冷启动/网络效应/增长战略 |
| [growth-operations-advisor-alex-schultz](./growth-operations-advisor-alex-schultz/) | Alex Schultz：留存第一/魔法时刻/激活漏斗 |
| [growth-operations-method-lean-startup](./growth-operations-method-lean-startup/) | 《精益创业》：实验循环/MVP/增长引擎 |
| [growth-operations-method-hooked](./growth-operations-method-hooked/) | 《上瘾》：Hook 模型/习惯养成/多变奖励 |
| [growth-operations-method-liuliangchi](./growth-operations-method-liuliangchi/) | 《流量池》：流量池/裂变/品效合一/私域 |

## 什么时候用

| 场景 | 用哪个 |
|---|---|
| 「增长没方向」「目标怎么定」 | master → strategy |
| 「做个实验」「改动要不要上」 | master → experiment |
| 「新用户流失」「激活低」 | master → activation |
| 「留存低」「怎么召回」 | master → retention |
| 「预算怎么分」「哪个渠道值得投」 | master → channel |
| 「数据跌了」「异常归因」 | master → diagnosis |
| 「方案行不行」「专家评审」 | advisory-board（评审会） |

## 质量保障

- 调研材料：`references/research/`（行业调研 + 3 专家蒸馏 + 3 方法论提炼）
- 执行链均带 `references/*-template.md` 输出模板（可复用/可迭代）
- 每个 Skill 均含 SKILL.md + README.md + SOURCES.md
- 内部 Skill 互相引用形成完整链路（master 路由 → 执行链 → 顾问团判断）
- 专家组合避开已有套件（活动/通用运营）重复：张溪梦/Andrew Chen/Alex Schultz + 《精益创业》《上瘾》《流量池》
- 中国语境配置项：裂变合规、微信生态、投放平台差异、数据合规（见各 Skill 边界）
