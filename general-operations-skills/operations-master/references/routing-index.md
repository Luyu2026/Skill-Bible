# operations-master · 路由索引

> 本文件是 operations-master 的分诊规则、路由表与预置链路索引，供 Agent 路由时快速查表。
> SKILL.md 保持轻量，路由细节在此维护。

## 成员名册

### 执行链（产出型）

| Skill | 一句话职责 | 典型输入 → 输出 |
|-------|-----------|----------------|
| `operations-data-analysis` | 数据归因与决策 | 数据/现象 → 诊断报告 + 行动建议 |
| `operations-activity-planner` | 活动策划与成本收益判断 | 活动目标/约束 → 可执行活动方案 + ROI 预估 |
| `operations-content-strategy` | 内容选题与策略 | 账号定位/素材 → 选题清单 + 内容计划 |
| `operations-user-segmentation` | 用户分层与触达策略 | 用户数据/画像 → 分层策略 + 触达计划 |
| `operations-review` | 运营动作复盘 | 动作记录/数据 → 复盘报告 + 行动项 |
| `operations-strategy` | 阶段性运营策略制定 | 目标/资源/现状 → 策略文档 |

### 顾问团（判断型）

判断类问题一律转交 `operations-advisory-board`（顾问团子总控），由它路由到专家/方法论，或召开多专家评审会。成员：黄有璨（运营价值）、张亮（运营体系）、曲卉（增长实验）3 位专家视角 + 《运营之光》《精益数据分析》《增长黑客》3 本方法论。

## 单点路由表

| 用户在说什么 | 路由到 | 备注 |
|---|---|---|
| 数据跌了 / 分析这个数据 / 指标异常 | `operations-data-analysis` | |
| 做个活动 / 活动方案 / 大促策划 | `operations-activity-planner` | |
| 发什么内容 / 选题 / 内容计划 | `operations-content-strategy` | |
| 用户怎么分层 / 触达策略 / 唤醒 | `operations-user-segmentation` | |
| 复盘 / 活动总结 / 迭代 | `operations-review` | |
| 下季度策略 / 运营规划 | `operations-strategy` | |
| 这个活动该不该做 / 值不值得 / 怎么选 | `operations-advisory-board` | 判断类转交顾问团 |

路由后：说明选择理由（一句话），确认后加载对应 Skill 执行。用户明显着急或指令明确时直接执行，不要多问。

## 预置工作流链路

用户任务横跨多步时，推荐链路并列出每步的交接物。**每一步的产出必须是下一步的合法输入**。

### 链路 A：从目标到月度运营计划（常用）

```
operations-strategy（季度目标/AARRR 拆解 → 策略文档）
    → operations-user-segmentation（分层与触达计划）
    → operations-content-strategy（内容选题与排期）
    → operations-activity-planner（关键节点活动方案）
```

### 链路 B：从数据异常到运营动作

```
operations-data-analysis（归因诊断 → 行动建议）
    → 对应执行 Skill（若判断为内容问题 → content-strategy；若为活动问题 → activity-planner）
    → operations-review（执行后复盘 → 迭代）
```

### 链路 C：判断先行

```
operations-advisory-board（该不该做/怎么选 → 条件化结论）
    → 对应执行 Skill（落地执行）
```
