# pm-master

> 产品工作的总入口：先判断你现在卡在哪，再把任务交给最合适的一个 Skill，或串成一条必要的工作链。

## 适合什么场景

当你遇到的是一个产品问题，但不知道应该先写 PRD、做调研、排优先级、看数据，还是开评审时，用它。

- 你只描述了一个需求或困境，不确定该从哪一步开始
- 一个任务跨了多步，例如从想法推进到开发就绪
- 你需要先判断“该不该做”，再落到具体方案
- 你手上已有 PRD、数据、需求池或竞品材料，但不确定下一步

不必为了写一份明确的 PRD、做一次具体的竞品分析而先调用它；直接使用对应的专项 Skill 会更快。

## 它会给你什么

1. **当前判断**：你属于“需要结论”“需要交付物”还是“需要一条工作链”。
2. **下一步路由**：推荐一个最合适的 Skill，并说明一句原因。
3. **必要时的链路**：列出步骤、每步交付物和需要你确认的节点；每一步都可独立停下，不强推完整流程。

## 怎么开始

把下面这句话和你的材料一起发给 Agent：

```text
请调用 pm-master，帮我处理下面这件事：

（粘贴你的问题、背景、数据、需求池、PRD 或文件）
```

例如：

```text
请调用 pm-master：我们想给新用户做一个邀请活动，但不确定值不值得做，
现在只有近三个月的注册和付费数据。请判断我第一步该做什么。
```

## 常见路径

| 你现在的情况 | 推荐路径 |
|---|---|
| 有想法，但不确定是否真值得做 | `pm-advisory-board` → `pm-prd-writer` |
| 需求已经写了，准备进评审 | `pm-review-board` → 修订 PRD → `pm-tracking-spec-writer` |
| 需求很多，不知道先做什么 | `pm-prioritization-engine` → `pm-roadmap-planner` |
| 指标下滑，想找到下一步动作 | `pm-analytics` → `pm-experiment-designer` → `pm-postmortem-writer` |
| 想通过调研或竞品找到机会 | `pm-advisory-board` / `pm-competitor-deconstructor` → `pm-survey-designer` → `pm-prioritization-engine` |

## 它能调度的能力

<details>
<summary><strong>执行类：把问题做成一份可交付的东西</strong></summary>

| 需要什么 | 对应 Skill |
|---|---|
| 写或补全需求文档 | `pm-prd-writer` |
| 提前发现评审问题 | `pm-review-board` |
| 给需求排优先级 | `pm-prioritization-engine` |
| 做版本计划与排期 | `pm-roadmap-planner` |
| 分析数据异动 | `pm-analytics` |
| 设计 A/B 实验 | `pm-experiment-designer` |
| 设计埋点与指标口径 | `pm-tracking-spec-writer` |
| 设计问卷 | `pm-survey-designer` |
| 拆解竞品 | `pm-competitor-deconstructor` |
| 做上线或实验复盘 | `pm-postmortem-writer` |
| 把截图或网页变成原型 | `pm-image2proto`、`pm-image2pencil`、`pm-url2proto` |

</details>

<details>
<summary><strong>判断类：先把“该不该做”想明白</strong></summary>

`pm-advisory-board` 会按问题调用 Cagan、Torres、俞军，以及 Mom Test、Story Mapping、Build Trap 等视角；它提供有条件的判断和分歧，不替你拍板。

</details>

## 使用边界

- 不编造你未提供的用户事实、数据或资源；信息不足会标注为“待确认”。
- 简单问题优先一步解决，只有真正跨步骤的任务才编排链路。
- 总控负责路由和交接；每个专项 Skill 对自己的输出质量负责。

完整的 Agent 调度规则见 [SKILL.md](./SKILL.md)，来源与保留机制见 [SOURCES.md](./SOURCES.md)。
