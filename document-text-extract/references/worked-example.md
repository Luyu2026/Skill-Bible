# 模拟 PDF 的实际文字提取

## 输入

明确模拟：[两页原生 PDF](simulated-source.pdf)，要求提取全部正文及第二页费用表。
第 1 页为双栏，第 2 页有金额和负号。输入为英文，避免把字体缺失误当识别准确性。
实际使用 pdfminer 提取文字，并用 pypdfium2 渲染两页，对照渲染图核验阅读顺序和表格列位。
原始机器提取结果：[未清洗提取稿](simulated-raw-extract.txt)。

## 可复制正文

### simulated-source.pdf · 物理第 1 页

SIMULATED - Quarterly note

左栏：
Left A: received 40 tickets.
Left B: previous period 32.

右栏：
Right A: pending files 8.
Right B: closed count unknown.

原始提取按上下坐标交错输出左 A、右 A、左 B、右 B；本稿按渲染图恢复先左栏、后右栏。
本稿保留原文，不翻译或扩写业务结论。

### simulated-source.pdf · 物理第 2 页

SIMULATED - Expenses

表名：simulated-source-p2-table1。

| Item | Amount CNY |
| --- | --- |
| Training | 1200.00 |
| Transport | -80.50 |

CSV：

```csv
Item,Amount CNY
Training,1200.00
Transport,-80.50
```

## 覆盖与关键字段核验

| 位置 | 核验内容 | 结果 |
| --- | --- | --- |
| 第 1 页 | 两栏各两行 | 四行完整，按栏恢复顺序 |
| 第 2 页标题行 | Amount CNY | 金额单位保留为 CNY |
| 第 2 页 Training 行 | 1200.00 | 小数点和两位小数保留 |
| 第 2 页 Transport 行 | -80.50 | 负号保留，未改成正数 |
| 第 2 页全表 | 两列两条数据 | 无列位交换 |

请求 2 页，完成 2 页，无未覆盖页；原 PDF 为原生文本，无扫描区域。
两页渲染图见 [第 1 页](simulated-page-1.png)、[第 2 页](simulated-page-2.png)。

## 使用边界与下一步

这次实际验证了原生 PDF 提取、多栏恢复和金额表重建，没有验证扫描 OCR、手写或公式识别。
遇到扫描页且无 OCR/视觉工具时，保留页码并列“未提取扫描区域”，请求高清图或文字版本；不能照此样例宣称扫描页完成。
用户若指出金额错误，需提供原页局部图并定位表名、行、列；修正后同时更新表格和 CSV。
