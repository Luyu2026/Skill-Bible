# 参数与结果口径

| 参数 | 含义 |
|---|---|
| 两个位置参数 | 左、右 CSV 路径 |
| `--key COL` | 必填，可重复形成复合键，顺序固定 |
| `--compare COL` | 可重复；省略时比较全部共同非键列 |
| `--numeric COL=TOL` | 可重复，指定绝对容差；必须为有限非负十进制数 |
| `--delimiter CHAR` | 默认逗号；`tab` 表示制表符 |
| `--encoding NAME` | 默认 `utf-8-sig`，两份文件使用同一编码 |
| `--out-dir PATH` | 必填，新建目录，不覆盖已有路径 |

表头必须非空且无重复列名；数据记录列数必须与表头一致。只含表头的单侧空表允许核对；双方都空时需人工核实。数值列允许 Python Decimal 的有限十进制格式（可含符号/指数）；单元格数值文本上限 200 字符、十进制元组指数绝对值上限 1000，超出时标为非法数值；空串、NaN、Infinity、千分位和货币符号均作为非法数值，不擅自清洗。非法数值仅针对声明了数值口径、且进入唯一键配对的行判断；单侧和歧义行不参与数值比较。

`record` 为表头之后从 1 开始的数据记录序号；单元格含换行时，它不等于文件物理行号。空行按 CSV 记录解析后会因列数不匹配被拒绝。主键按元组匹配，不用拼接字符串，避免分隔符碰撞。

`summary.left_rows/right_rows` 是输入行数。每一侧均满足：

```
总行数 = matched_rows + changed_rows + invalid_pair_rows
       + only_<该侧>_rows + ambiguous_<该侧>_rows + invalid_key_<该侧>_rows
```

`matched_rows` / `changed_rows` / `invalid_pair_rows` 是配对记录数，在左右各占一行。一个配对只要有非法数值就全部进入 `invalid_pairs`，其中仍保留可判定的其他字段差异。`match_rate` = matched_rows / (matched_rows + changed_rows)，仅衡量已成功比较的配对；分母为 0 时为 null。该比例不包括单侧、歧义、空键、非法数值配对，不能当作全量迁移成功率。

`columns_only_left/right` 始终报告，即使显式缩小比较范围；存在单侧列时状态至少为 different。相同结构中用 `--compare` 排除的字段列于 `uncompared_columns`，same 只表示选定范围一致。只比较键时仍会检查键集合和唯一性。

JSON 明细保留原始字符串。若要把它转成 Excel/CSV，必须把不可信单元格写作文本，避免表格软件将 `=`, `+`, `-`, `@` 等内容当作公式；本脚本不输出可执行公式。
