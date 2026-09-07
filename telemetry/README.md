# Skill-Bible 匿名运行回执

这套机制用于理解 Skill 的兼容性和失败模式，不用于收集用户的提示词、文件、简历、JD、输出内容、账号或可识别个人信息。

## 默认状态

默认关闭。没有 `~/.skill-bible/telemetry/config.json`，或其中 `enabled` 不是 `true` 时，所有回执命令立即退出，不联网、不写文件，也不影响 Skill 完成任务。

启用前必须由安装者明确创建配置文件。可从 `config.example.json` 开始；使用本地 `file` 模式时，事件只保存在安装者电脑。未来接入公开接收端时，必须在配置中明确写入 endpoint，不能由 Skill 私自指定或替换。

## 只允许收集的字段

- Skill ID 与版本
- Agent 大类
- 事件：启动、完成、失败或用户主动反馈
- 耗时区间与标准化错误码
- 安装者主动生成的随机匿名安装 ID

字段定义见 [event.schema.json](./event.schema.json)。原始输入、输出、路径、文件名、账号和环境变量均不得写入事件。

## 对 Skill 作者的约束

只有在用户已开启回执、辅助程序存在时，才可尽力发送 `started` 与一个终态事件。回执失败必须静默，不得阻断任务、重复重试或提示用户开启。

## 本地报告

```bash
python3 telemetry/summarize_events.py --days 1
python3 telemetry/summarize_events.py --days 7
```

公共接收端、可视化与跨用户汇总尚未启用前，这只能汇总一台电脑上的本地回执。上线集中式接收端前，应先完成隐私声明、保留期限、删除机制、反滥用限制与管理端访问控制。
