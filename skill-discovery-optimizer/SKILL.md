---
name: skill-discovery-optimizer
description: 当用户要创建或调整 Skill 的名称、description、Agent metadata 或相邻 Skill 边界，并希望 Agent 在恰当场景正确发现和调用它时使用。优化触发与反触发；不用于把 README 写成营销文案。
---

# Skill 发现优化器

让 Agent 在看到 Skill 列表时，能判断“现在该不该读这个 Skill”。核心是清楚的触发条件和边界，而不是更夸张的功能介绍。

## 需要的材料

- Skill 要解决的单一任务；
- 用户最自然的 5—10 种说法；
- 必要输入和稳定输出；
- 最相近的 2—3 个 Skill；
- 不该由这个 Skill 接手的场景。

缺少相邻 Skill 信息时，先搜索当前 Skill 库，不要凭名称猜冲突。

## 优化规则

1. `name` 使用稳定、行动导向的 kebab-case 名称，不随营销口号变化。
2. `description` 优先说明用户何时需要它，包含典型语境和一个必要边界。
3. 不把完整工作流、安装说明、夸张成果或全部功能塞进 description。
4. 对相近 Skill 写清“我处理什么、我不处理什么、何时交给对方”。
5. 同步检查 `SKILL.md` frontmatter、`agents/openai.yaml` 和 README 首段，三者不能矛盾。

## 发现测试

生成五条用户口语化测试：两条应触发、两条应路由给相邻 Skill、一条信息不足。发现失败时优先修正描述和边界，不靠堆关键词抢调用。

## 输出

- 推荐名称；
- 可直接写入 frontmatter 的 description；
- 相邻 Skill 边界表；
- 五条发现测试与预期路由；
- 需要同步更新的文件清单。

## 边界

- 不承诺“写了描述就一定被调用”，不同 Agent 的发现机制不同。
- 不贬低相邻 Skill 来抢流量。
- 不通过万能描述吸收不属于自己的任务。
