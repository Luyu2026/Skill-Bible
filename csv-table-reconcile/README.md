# CSV 双表差异核对

两张导出表看起来差不多，却不确定少了哪条记录、哪里改过？提供两份 CSV/TSV 和用于识别记录的字段，就能拿到差异摘要与逐条明细。

适用于订单导出核对、库存快照比较、CRM 迁移验收、名单版本检查。支持复合键、重复键隔离，以及明确指定的数值容差；不自动合并数据，不判断账务是否合规。

## 安装与调用

把此页面链接发给你的 Agent：

```text
请安装这个 Skill：https://github.com/Luyu2026/Skill-Bible/tree/main/csv-table-reconcile
只安装这一项，并告诉我下一句话如何调用。
```

也可将本目录完整放入 Agent 的 Skill 目录。直接说：

```text
用 $csv-table-reconcile 核对 before.csv 和 after.csv。
它们是同一天的订单导出，按 order_id + line_id 匹配。
比较 status 和 amount，amount 允许绝对差 0.01，其余精确比较。
```

需要 Python 3.9 或更新版本，无第三方依赖。默认读取 UTF-8 CSV，支持显式分隔符/编码设置。其他文件格式先导出 CSV；不会连接你的业务系统。

## 你会得到什么

- `summary.md`：核对范围、状态和分类计数。
- `report.json`：差异记录、左右原值、记录序号、异常原因和计算口径。

输出目录必须尚不存在。所有字段默认按原文比较；前导零、大小写和空格均保留。重复键不会被自动去重。数据全量载入内存，超大文件需要另行分区处理。

完整参数与结果口径见 [核对规则](references/comparison-rules.md)。[匿名示例案例](evals/evals.json) 可用于检查安装后的行为。

## 授权

指令、文档、案例采用 [CC BY-NC 4.0](LICENSE)，脚本采用 [Apache-2.0](LICENSE-CODE)。个人非商业使用可按许可证使用；内容的商业使用需另行授权。用户输入和生成的业务核对结果不因此改变其权属。
