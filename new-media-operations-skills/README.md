# 新媒体运营岗位技能（New Media Operations）

> 陆羽Skill 为「新媒体运营」岗位生成的体系化 Skill 套件，覆盖新媒体运营完整工作链：**账号定位 → 内容创作 → 涨粉经营 → 爆款打造 → 多平台分发 → 数据复盘**。
> 生成时间：2026-09-29 · 生成器：luyu-skill（元 Skill 工厂）

## 套件结构

```
new-media-operations-master/        # 🎯 总控：分诊 → 路由 → 编排
├── 执行链（产出型）   # 每个执行链带 references/*-template.md 输出模板
└── 顾问团（判断型）   # 子总控 + 3 专家视角 + 3 方法论
```

## 完整 Skill 清单

### 🎯 总控（1）

| Skill | 说明 |
|---|---|
| [new-media-operations-master](./new-media-operations-master/) | 新媒体运营总控：分诊问题 → 路由到最合适的 Skill → 编排多 Skill 链路 |

### ⚙️ 执行链（6，产出型）

| Skill | 什么时候用 | 产出 |
|---|---|---|
| [new-media-operations-positioning](./new-media-operations-positioning/) | 账号怎么定位/起号/人设 | 账号定位卡（赛道/人群/人设/差异化） |
| [new-media-operations-content](./new-media-operations-content/) | 写什么/选题/内容没流量 | 选题清单 + 内容脚本/文案 |
| [new-media-operations-growth](./new-media-operations-growth/) | 涨粉慢/粉丝经营 | 涨粉打法方案（内容涨粉/互动/私域承接） |
| [new-media-operations-viral](./new-media-operations-viral/) | 怎么出爆款/内容没爆 | 爆款选题 + 结构拆解 + 内容方案 |
| [new-media-operations-distribution](./new-media-operations-distribution/) | 多平台发布/矩阵运营 | 多平台分发计划 + 矩阵布局建议 |
| [new-media-operations-review](./new-media-operations-review/) | 数据复盘/为什么没爆 | 复盘报告（爆款归因/失败归因/迭代） |

### 🧭 顾问团（7，判断型）

| Skill | 说明 |
|---|---|
| [new-media-operations-advisory-board](./new-media-operations-advisory-board/) | 顾问团总控：路由 + 评审会模式 + 分歧地图 |
| [new-media-operations-advisor-qiuye](./new-media-operations-advisor-qiuye/) | 秋叶：矩阵运营/账号定位/个人IP/变现 |
| [new-media-operations-advisor-zhouzuoluo](./new-media-operations-advisor-zhouzuoluo/) | 粥左罗：内容创作/选题/写作方法论 |
| [new-media-operations-advisor-lvbai](./new-media-operations-advisor-lvbai/) | 吕白：爆款公式/对标拆解/黄金开头 |
| [new-media-operations-method-baokuan](./new-media-operations-method-baokuan/) | 《爆款文案》：转化文案/标题6式 |
| [new-media-operations-method-tipping-point](./new-media-operations-method-tipping-point/) | 《引爆点》：传播三法则/记忆点 |
| [new-media-operations-method-positioning](./new-media-operations-method-positioning/) | 《定位》：心智抢占/差异化 |

## 什么时候用

| 场景 | 用哪个 |
|---|---|
| 「账号怎么定位」「起号」 | master → positioning |
| 「写什么」「内容没流量」 | master → content |
| 「涨粉慢」「粉丝经营」 | master → growth |
| 「怎么出爆款」「没爆」 | master → viral |
| 「多平台发布」「矩阵」 | master → distribution |
| 「数据复盘」「为什么没爆」 | master → review |
| 「这个方向行不行」「专家评审」 | advisory-board（评审会） |

## 质量保障

- 调研材料：`references/research/`（行业调研 + 3 专家蒸馏 + 3 方法论提炼）
- 执行链均带 `references/*-template.md` 输出模板（可复用/可迭代）
- 每个 Skill 均含 SKILL.md + README.md + SOURCES.md
- 内部 Skill 互相引用形成完整链路（master 路由 → 执行链 → 顾问团判断）
- 专家组合避开已有套件（内容/用户/KOL/增长运营）重复：秋叶/粥左罗/吕白 + 《爆款文案》《引爆点》《定位》
- 中国语境配置项：平台调性差异（公众号/抖音/小红书/B站）、内容合规（广告法/敏感领域）、导流私域规则（见各 Skill 边界）
