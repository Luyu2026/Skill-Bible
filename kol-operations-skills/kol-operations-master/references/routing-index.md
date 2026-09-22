# kol-operations-master · 路由索引

> 本文件是 kol-operations-master 的分诊规则、路由表与预置链路索引，供 Agent 路由时快速查表。
> SKILL.md 保持轻量，路由细节在此维护。

## 成员名册

### 执行链（产出型）

| Skill | 一句话职责 | 典型输入 → 输出 |
|-------|-----------|----------------|
| `kol-operations-strategy` | KOL 营销策略制定 | 目标/预算 → 策略文档（平台/分层/预算分配） |
| `kol-operations-discovery` | KOL 寻源与筛选 | 需求/平台 → 候选 KOL 清单（含评估） |
| `kol-operations-outreach` | 触达与谈判 | 候选清单 → 触达邮件 + 谈判方案 |
| `kol-operations-co-creation` | 内容共创与审核 | 品牌/达人 → 内容 Brief + 审核清单 |
| `kol-operations-campaign` | 投放执行与追踪 | 排期/权益 → 执行计划 + 追踪表 |
| `kol-operations-analytics` | 效果分析与优化 | 数据 → 效果报告 + 复投建议 |

### 顾问团（判断型）

判断类问题一律转交 `kol-operations-advisory-board`（顾问团子总控），由它路由到专家/方法论，或召开多专家评审会。成员：Gary Vee（内容/个人品牌）、Neal Schaffer（KOL 策略）、Brittany Hennessy（达人实操）3 位专家视角 + 《Influencer》《Contagious》《Leverage》3 本方法论。

## 单点路由表

| 用户在说什么 | 路由到 | 备注 |
|---|---|---|
| KOL 策略 / 预算分配 / 平台选择 | `kol-operations-strategy` | |
| 找达人 / 筛达人 / 达人评估 | `kol-operations-discovery` | |
| 联系达人 / 谈判 / 报价 | `kol-operations-outreach` | |
| 内容 Brief / 脚本审核 | `kol-operations-co-creation` | |
| 投放排期 / 权益追踪 | `kol-operations-campaign` | |
| KOL 效果分析 / ROI / 复投 | `kol-operations-analytics` | |
| 该不该做 KOL / 选哪个达人 / 报价是否合理 | `kol-operations-advisory-board` | 判断类转交顾问团 |

路由后：说明选择理由（一句话），确认后加载对应 Skill 执行。用户明显着急或指令明确时直接执行，不要多问。

## 预置工作流链路

### 链路 A：从 0 到 1 KOL 投放（常用）

```
kol-operations-strategy（策略 → 平台/分层/预算）
    → kol-operations-discovery（寻源 → 候选清单）
    → kol-operations-outreach（触达 → 合作名单）
    → kol-operations-co-creation（Brief → 内容）
    → kol-operations-campaign（投放 → 追踪）
    → kol-operations-analytics（效果 → 复投）
```

### 链路 B：从效果问题到优化

```
kol-operations-analytics（效果诊断 → 定位问题）
    → 判断：选人有问题 → discovery；内容有问题 → co-creation；报价有问题 → outreach
```

### 链路 C：判断先行

```
kol-operations-advisory-board（该不该做/怎么选 → 条件化结论）
    → 对应执行 Skill（落地执行）
```
