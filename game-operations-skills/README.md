# 游戏运营岗位技能（Game Operations Skills）

> 陆羽Skill 为「游戏运营」岗位生成的体系化 Skill 套件，覆盖游戏运营完整工作链：**玩家生命周期 → 分层 → 活动 → 商业化 → 数据分析 → 社区内容**。
> 生成时间：2026-09 · 生成器：luyu-skill（元 Skill 工厂）

## 套件结构

```
game-master/          # 🎯 总控：分诊 → 路由 → 编排
├── 执行链（产出型）★带 references/*-template.md 输出模板
│   ├── game-lifecycle/        # 生命周期五阶段策略
│   ├── game-segmentation/     # 玩家分层（大R/中R/小R/白嫖）
│   ├── game-events/           # 活动策划（类型库/目标匹配）
│   ├── game-monetization/     # 商业化（首充/月卡/战令/抽卡）
│   ├── game-analytics/        # 数据（留存/活跃/付费/流失）
│   └── game-community/        # 社区内容（官方/UGC/社群）
└── 顾问团（判断型）
    ├── game-advisory-board/   # 🧭 子总控：评审会+分歧地图
    ├── game-advisor-ops/      # 游戏运营实战专家
    ├── game-advisor-chou/     # Yu-kai Chou（Octalysis 游戏化）
    ├── game-advisor-qu/       # 曲卉（增长实验）
    ├── game-method-ops/       # 游戏运营方法论
    ├── game-method-chou/      # 《游戏化实战》
    └── game-method-hooked/    # 《上瘾》
```

## 什么时候用

| 场景 | 用哪个 |
|---|---|
| 「游戏怎么运营」「没方向」 | master → lifecycle |
| 「玩家分层」「大R怎么维护」 | master → segmentation |
| 「活动怎么设计」 | master → events |
| 「商业化/付费率低」 | master → monetization |
| 「数据怎么看」「留存低」 | master → analytics |
| 「社区活跃低」 | master → community |
| 「方案行不行」「值不值得做」 | advisory-board（评审会） |

## 质量保障

- 调研材料：`references/research/`（游戏运营方法论 + 游戏化书籍 + 复用材料）
- 执行链均带 `references/*-template.md` 输出模板（可复用/可迭代）
- 每个 Skill 均含 SKILL.md + README.md + SOURCES.md
