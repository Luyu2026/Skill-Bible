# CSV 多文件合并

将多个月份、门店或活动的 CSV 明细汇总成一张表，按列名对齐，附上每行来源文件；保留编号前导零、重复记录和多行文本。

## 使用

将整个 `csv-stack` 文件夹放入你的 Agent 的 Skills 目录，例如 `~/.codex/skills/` 或 `~/.claude/skills/`。需要 Python 3.9+，无需额外依赖或联网。

对 Agent 说：

> 用 $csv-stack 把 7 月和 8 月的订单 CSV 合成一份明细，保留订单编号和来源，告诉我每份输入及最终行数。

> 把两个门店的导出 CSV 合并，不同列全部保留，缺列留空；保留重复记录，输出新文件。

也可以在此目录直接运行：

```bash
python3 scripts/stack_csv.py "july.csv" "august.csv" --output "combined.csv"
```

得到 `combined.csv` 和终端 JSON 行数摘要。默认要求列名集合一致，允许列顺序不同；明确需要扩展列时加 `--mode union`。详见 [参数说明](references/usage.md)。

这是纵向追加明细，不执行按 ID 关联、去重、求和或 Excel 工作簿编辑。输入不修改，已有结果不覆盖；错误不会输出半成品 CSV。表格软件可能自动转换文本或解释公式，导入时请按数据用途选择文本列类型。

## 授权

指令、说明与案例适用 [CC BY-NC 4.0](LICENSE)；可执行代码适用 [Apache-2.0](LICENSE-CODE)。
