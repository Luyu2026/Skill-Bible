中文 · [English](./README.en.md)

# Skill Bible

把真实卡住的场景，做成大家都能用的 Skill。

Claude Code / Codex / Workbuddy / OpenClaw / Hermes Agent / CodeBuddy / Gemini CLI / OpenCode 等 AI 智能体开源技能集合；已收录日常创作工具、求职面试工作流、思维视角角色、编程辅助等 Skill。

每个 Skill 都试图把一个反复出现的现实问题，拆成 Agent 可以稳定执行、用户可以复用的工作流。

Skill 使用分享视频可在 **抖音 / 小红书 / 公众号** 搜索 **陆羽** 查看。

新收录的 Skill README 统一以真实使用场景开头；具体写法见 [贡献规范](./CONTRIBUTING.md)。

## 先从这里开始

不用先理解 Skill、MCP 或 Agent。先看你现在卡在哪：

| 你现在遇到的事 | 先试这个 | 你会先拿到什么 |
|---|---|---|
| 投了很多岗位没回应，不知道该删哪个、该认真投哪个 | [岗位匹配](./job-application-match/) | 一份能执行的投递顺序 |
| 同一段经历投不同岗位，简历越改越像套话 | [岗位简历定制](./resume-jd-tailor/) | 适配不同岗位的简历表达 |
| 明天面试，不知道题库里该先练哪几题 | [面试准备](./interview-prep-brief/) | 高概率题、项目故事和追问链路 |
| 刚面完，知道没讲好却不知道下次怎么改 | [面试复盘](./interview-transcript-replay/) | 3 个下次能直接练的答案 |
| 找工作每天都在变，不知道今天最该推进什么 | [求职全流程](./job-search-pilot/) | 当前事件对应的下一步动作 |
| 想转方向或辞职，又不想靠情绪做决定 | [人生路径](./life-odyssey-planner/) | 3 条能走的路和一个可逆实验 |

每个页面顶部都会先告诉你：它适合什么时刻、你只需要给什么、最后能推进什么结果。

## Skill Bible 想解决什么

很多事情并不是不会做，而是每次都要重新判断、重新组织材料、重新找路径：拿到陌生 JD 不知道怎么准备，经历不少却不知道该往哪个岗位写，面试结束后知道哪里答得不好却不知道下次如何改。

Skill Bible 从真实场景出发，把这些重复但费脑的环节做成可复用能力。你可以单独调用一个 Skill，也可以把几个 Skill 串成一条完整工作流。

求职是目前已经跑通的一条工作流：

`岗位匹配 → 简历定制 → 岗位面试备书 → 多轮面试准备 → 面试录音复盘`

除此之外，内容创作、思维视角和编程辅助等 Skill 也可以独立使用，后续会逐步补齐它们各自的组合方式和真实案例。

它们不替你虚构经历或替你做最终选择，但会把判断所需的材料、问题、动作和反馈闭环整理清楚。

## Skill Bible 怎么收录社区 Skill

Skill-Bible 不追求把所有文件搬进来。我们更在意：这个 Skill 是否真的解决问题、别人能不能跑通、它在哪些 Agent 上可用、作者是否愿意持续维护。

| 状态 | 含义 | 用户该怎样理解 |
|---|---|---|
| 社区候选 | 基础信息、来源和许可证已提交，尚未完成验证 | 可以发现，不代表推荐 |
| 已验证 | 至少完成一次可复现的基础运行测试 | 可以按说明尝试 |
| 编辑精选 | 真实场景里有明确价值，文档、边界和维护都达标 | 值得优先花时间 |

想提交原创 Skill、推荐外部项目或报名做测试，先看[提交入口](./SUBMIT_A_SKILL.md)。原作者保留署名和原始链接；未明确许可的外部项目只做索引，不镜像代码。

## 内容创作

| Skill | 用途 |
|---|---|
| [daily-idea-expander](./daily-idea-expander/) | 把碎片想法扩写成视频文案——结构化口播稿、剪辑版、金句、标题一键输出 |

## 求职面试

| Skill | 用途 |
|---|---|
| [job-search-pilot](./job-search-pilot/) | 求职全流程总控：适合求职中不断遇到不同事件的人。无论是判断岗位、改简历、准备面试、面后复盘还是投递无回复，只需描述此刻发生的事，即可得到当前最需要的直接答案 |
| [job-application-match](./job-application-match/) | 校招/社招先分清“值得冲的好岗位”和“按当前经历适合投的岗位”，再按岗位直接给出简历改写、示例数据版和具体投递行动清单；校招可读取公开岗位池，社招使用用户提供的 JD、链接或截图 |
| [interview-prep-brief](./interview-prep-brief/) | 根据岗位 JD、候选人背景和题库/面经，生成岗位面试备书：高概率题目、带数据的可直接用答案、追问链路和备面计划；本地材料不足时可参考外部项目机制优化拆解，支持飞书文档或本地 Markdown |
| [interview-round-prep](./interview-round-prep/) | 在面试备书基础上继续拆一面、二面、三面/终面、HR 面，按轮次生成高概率题、回答思路、可直接开口答案和追问预判；适合面试前按轮次集中练习，支持飞书文档或本地 Markdown |
| [interview-transcript-replay](./interview-transcript-replay/) | 根据面试录音转写、PDF、飞书文档或纯文本记录，提炼真实面试问题，诊断原回答失分点，并生成核心问题复盘、其他问题复盘、可直接开口答案和下次练习计划 |
| [resume-jd-tailor](./resume-jd-tailor/) | 根据目标岗位 JD 和原始经历，把“信息很少/写得很薄”的经历改成可直接复制进简历的岗位定制 bullet；输出可切入岗位对比、写法策略、无数据占位版与逻辑自洽示例数据版，支持飞书文档或本地 Markdown |
| [offer-decision-advisor](./offer-decision-advisor/) | Offer 选择顾问：比较两份及以上 Offer，结合兴趣、行业、岗位、薪资、城市与个人底线，给出可解释的建议、反转条件和入职前核实话术 |

## 人生选择

| Skill | 用途 |
|---|---|
| [life-odyssey-planner](./life-odyssey-planner/) | 人生奥德赛计划：当你不知道该继续深耕、保留工作探索新方向还是重构路径时，基于真实约束推演三条可信路线，并落到一个可逆的 90 天实验 |
| [multi-year-path-planner](./multi-year-path-planner/) | 1、2、5 年路径推演：基于 Agent 可见的历史会话和项目材料，区分事实、信号与假设，持续判断长期路径、本周主押注与停止条件 |

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

将 Skill 目录放入 `~/.claude/skills/`（Claude Code）或 `~/.codex/skills/`（Codex CLI），激活即可使用。Workbuddy、OpenClaw 等其他 Agent，请按各自的 Skill 目录规则放置。

第一次接触 Skill、不知道该从哪里开始，可以先看[《从零开始使用 Skill》](./使用教程/skill-usage-guide.md)。

### 最简单的安装方式

找到你想用的 Skill，复制它所在页面的网址，然后把下面这段话发给你正在使用的 Agent：

```text
请帮我安装这个 Skill：
[把 Skill 页面的网址粘贴在这里]

我只想安装这一个 Skill，不需要下载整个仓库。
请你自己判断我当前使用的 Agent、正确的 Skill 安装目录和下载方式，并直接完成安装。
安装完成后告诉我：它装在了哪里，以及我下一句话该怎么调用它。
```

如果你想一次安装整个 Skill-Bible，也可以把仓库首页地址发给 Agent：

```text
请帮我安装这个仓库里的全部 Skill：
https://github.com/Luyu2026/Skill-Bible

请你自己判断我当前使用的 Agent、正确的 Skill 安装目录和下载方式，并直接完成安装。
安装完成后告诉我：它们装在了哪里，以及我下一句话该怎么调用其中一个 Skill。
```

如果你没有配置飞书 CLI，也可以正常使用需要文档输出的 skill；对应 skill 会优先生成本地 Markdown，不会因为飞书权限卡住。

## 一起把它做得更好

你可以提交一个原创 Skill，也可以只提交一个值得收录的外部链接。先不要在群里丢压缩包，统一通过[提交入口](./SUBMIT_A_SKILL.md)留下来源、使用场景和真实案例。

Skill-Bible 保留最终收录、分级和推荐权。目的不是做一个文件堆，而是让中文用户更快找到真正能用的 Skill。
