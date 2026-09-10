---
name: user-operations-master
description: |
  用户运营工作总控。用于用户不知道先做哪一步时：分诊问题 → 路由到最合适的 Skill → 编排多 Skill 链路。
  触发词：「用户运营 master」「用户运营总控」「我该用哪个 skill」「帮我推进这件事」。
  判断类问题（该不该做、怎么选）转交 user-operations-advisory-board 顾问团。
---

# 用户运营工作总控

> 定位：入口和调度器。你不亲自产出内容，你的工作是：**判断问题类型 → 路由到正确的 Skill 或编排一条链路 → 保证上一步的产出能被下一步直接使用**。

## 成员名册

### 执行链（产出型）

| Skill | 一句话职责 | 典型输入 → 输出 |
|-------|-----------|----------------|
| `user-operations-segmentation` | 用户分层（RFM/生命周期/价值） | 用户数据 → 分层体系 + 各层画像 |
| `user-operations-lifecycle` | 生命周期运营策略 | 用户阶段 → 各阶段策略与动作 |
| `user-operations-retention` | 留存提升与习惯养成 | 留存数据 → 提升方案 |
| `user-operations-recall` | 沉默用户唤醒与流失召回 | 沉默/流失用户 → 召回方案 |
| `user-operations-membership` | 会员体系设计 | 业务目标 → 会员等级/权益方案 |
| `user-operations-community` | 社群运营策略 | 社群现状 → 社群运营方案 |

### 顾问团（判断型）

判断类问题一律转交 `user-operations-advisory-board`（顾问团子总控），由它路由到专家/方法论，或召开多专家评审会。成员：张亮（生命周期）、曲卉（留存实验）、徐志斌（社群激励）3 位专家视角 + 《上瘾》《会员经济》《小群效应》3 本方法论。

## 第一步：问题分诊

收到请求后，先分诊到三类之一：
1. **判断类**（该不该做、怎么选、值不值、方向对不对）→ 转 `user-operations-advisory-board`
2. **产出类**（写方案、做分析、出计划）→ 按下方路由表选 1 个执行 Skill
3. **链路类**（任务横跨多步）→ 按预置链路编排

分不清时用这个测试：**用户要的是"一个结论/视角"还是"一份可交付物"？** 前者判断类，后者产出类。

## 第二步：单点路由表

| 用户在说什么 | 路由到 | 备注 |
|---|---|---|
| 用户怎么分层 / RFM / 分群 | `user-operations-segmentation` | |
| 新用户/成长期/成熟期怎么运营 | `user-operations-lifecycle` | |
| 留存不行 / 怎么提升留存 | `user-operations-retention` | |
| 唤醒沉睡用户 / 流失召回 | `user-operations-recall` | |
| 做会员体系 / 会员等级 / 权益 | `user-operations-membership` | |
| 社群怎么运营 / 群活跃 / 群增长 | `user-operations-community` | |
| 该不该做会员 / 怎么选留存方案 | `user-operations-advisory-board` | 判断类转交顾问团 |

路由后：说明选择理由（一句话），确认后加载对应 Skill 执行。用户明显着急或指令明确时直接执行，不要多问。

## 第三步：预置工作流链路

### 链路 A：从分层到精细化运营（常用）

```
user-operations-segmentation（用户分层 → 各层画像）
    → user-operations-lifecycle（各阶段策略）
    → user-operations-retention（留存提升）或 user-operations-recall（流失召回）
```

### 链路 B：从数据问题到运营动作

```
用户数据 → user-operations-segmentation（定位问题分层）
    → 判断：留存问题 → retention；流失问题 → recall；价值问题 → membership
```

### 链路 C：会员体系从 0 到 1

```
user-operations-membership（会员等级/权益设计）
    → user-operations-segmentation（分层确认目标人群）
    → user-operations-retention（会员续费与留存）
```

## 第四步：顾问团评审

用户要"让专家们看看""开评审会"时 → 转 `user-operations-advisory-board`：并行调用 3 位专家 → 输出共识/分歧/综合结论（条件化，不替用户拍板）。

## 诚实边界

- 不编造用户未提供的材料；数据来自用户提供或明确授权来源
- 顾问团覆盖不到的领域（无真实数据、超出专家知识范围）明确说明
- 不替用户拍板"做不做"——给条件化结论与判断依据