# Skill Bible

把真实卡住的场景，做成大家都能用的 Skill。

Claude Code / Codex / Workbuddy / OpenClaw / Hermes Agent / CodeBuddy / Gemini CLI / OpenCode 等 AI 智能体开源技能集合；已收录日常创作工具、求职面试工作流、思维视角角色、编程辅助等 Skill。

每个 Skill 都试图把一个反复出现的现实问题，拆成 Agent 可以稳定执行、用户可以复用的工作流。

Skill 使用分享视频可在 **抖音 / 小红书 / 公众号** 搜索 **陆羽** 查看。

## 这套 Skill 想解决什么

很多事情并不是不会做，而是每次都要重新判断、重新组织材料、重新找路径：拿到陌生 JD 不知道怎么准备，经历不少却不知道该往哪个岗位写，面试结束后知道哪里答得不好却不知道下次如何改。

Skill Bible 从真实场景出发，把这些重复但费脑的环节做成可复用能力。你可以单独调用一个 Skill，也可以把几个 Skill 串成一条完整工作流。

当前已经跑通的一条求职链路是：

`简历定制 → 岗位面试备书 → 多轮面试准备 → 面试录音复盘`

它不替你虚构经历或替你做最终选择，但会把判断所需的材料、问题、动作和反馈闭环整理清楚。

## 内容创作

| Skill | 用途 |
|---|---|
| [daily-idea-expander](./daily-idea-expander/) | 把碎片想法扩写成视频文案——结构化口播稿、剪辑版、金句、标题一键输出 |

## 求职面试

| Skill | 用途 |
|---|---|
| [interview-prep-brief](./interview-prep-brief/) | 根据岗位 JD、候选人背景和题库/面经，生成岗位面试备书：高概率题目、带数据的可直接用答案、追问链路和备面计划；本地材料不足时可参考外部项目机制优化拆解，支持飞书文档或本地 Markdown |
| [interview-round-prep](./interview-round-prep/) | 在面试备书基础上继续拆一面、二面、三面/终面、HR 面，按轮次生成高概率题、回答思路、可直接开口答案和追问预判；适合面试前按轮次集中练习，支持飞书文档或本地 Markdown |
| [interview-transcript-replay](./interview-transcript-replay/) | 根据面试录音转写、PDF、飞书文档或纯文本记录，提炼真实面试问题，诊断原回答失分点，并生成核心问题复盘、其他问题复盘、可直接开口答案和下次练习计划 |
| [resume-jd-tailor](./resume-jd-tailor/) | 根据目标岗位 JD 和原始经历，把“信息很少/写得很薄”的经历改成可直接复制进简历的岗位定制 bullet；输出可切入岗位对比、写法策略、无数据占位版与逻辑自洽示例数据版，支持飞书文档或本地 Markdown |

## 思维视角

每个 skill 基于多轮真实调研提炼心智模型、决策启发式和表达 DNA，激活后以第一人称角色扮演。

| Skill | 人物 | 一句话 |
|---|---|---|
| [duan-yongping-perspective](./duan-yongping-perspective/) | 段永平 | 做对的事，把事做对。买股票就是买公司。 |
| [munger-perspective](./munger-perspective/) | 查理·芒格 | 反过来想，总是反过来想。告诉我我会死在哪，我就永远不去。 |
| [naval-perspective](./naval-perspective/) | Naval Ravikant | 财富是你睡着后还在为你工作的东西。 |
| [steve-jobs-perspective](./steve-jobs-perspective/) | 史蒂夫·乔布斯 | 聚焦不是对你想做的事说 Yes，是对一百个好主意说 No。 |
| [elon-musk-perspective](./elon-musk-perspective/) | 埃隆·马斯克 | 物理定律是唯一硬约束，其他一切都是建议。 |
| [feynman-perspective](./feynman-perspective/) | 理查德·费曼 | 如果你不能向大一新生解释清楚，说明你自己没真懂。 |
| [taleb-perspective](./taleb-perspective/) | 纳西姆·塔勒布 | 不要当脆弱的傻瓜。反脆弱的事物从混乱中获益。 |

## 编程辅助

| Skill | 用途 |
|---|---|
| [codex-pet-maker](./codex-pet-maker/) | 创建/修复/安装 Codex 桌面编程宠物动画，内含 10 个成品 pet |

## 使用方式

将 skill 目录放入 `~/.claude/skills/`（Claude Code）或 `~/.codex/skills/`（Codex CLI），激活即可使用。

```bash
# 克隆所有 skill 到本地
git clone https://github.com/Luyu2026/Skill-Bible.git
```

如果你没有配置飞书 CLI，也可以正常使用需要文档输出的 skill；对应 skill 会优先生成本地 Markdown，不会因为飞书权限卡住。
