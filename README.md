# Skill Bible

Claude Code / Codex / Workbuddy / OpenClaw / Hermes Agent / CodeBuddy / Workbuddy / Gemini CLI / OpenCode/
等AI智能体开源技能集合。收录日常创作工具、思维视角角色、编程辅助等 skill。

## 内容创作

| Skill | 用途 |
|---|---|
| [daily-idea-expander](./daily-idea-expander/) | 把碎片想法扩写成视频文案——结构化口播稿、剪辑版、金句、标题一键输出 |

## 求职面试

| Skill | 用途 |
|---|---|
| [interview-prep-brief](./interview-prep-brief/) | 根据岗位 JD、候选人背景和题库/面经，生成岗位面试备书：高概率题目、带数据的可直接用答案、追问链路和备面计划；本地材料不足时可参考外部项目机制优化拆解，支持飞书文档或本地 Markdown |
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
