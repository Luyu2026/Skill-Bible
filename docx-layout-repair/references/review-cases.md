# 模拟复审：周报标题与超链接保护

真实问题：已有周报标题无法导航，但正文与风险段必须原样保留。
完整详尽：明确对象盘点、run 级修改和字段更新边界；复杂对象不能无提示重建。

## 原稿与本轮成品

原稿取自 demo-input.docx，本次重新执行样式修复并另存临时 DOCX，再打开核对。

| 原文 | 本轮样式 | 正文变更 |
| --- | --- | --- |
| 项目周报 | Title | 无 |
| 本周进展 | Heading 1 | 无 |
| 完成接口联调，耗时 3 天。 | Normal | 无 |
| 风险 | Heading 1 | 无 |
| 测试环境尚未开放。 | Normal | 无 |

可使用的原有同案例成品：[demo-output.docx](../demo-output.docx)。
新增边界：插入包含“原链接文字”的 hyperlink XML，只设置段落样式；操作前后超链接节点 XML 一致。
这验证样式修改不会主动重建 runs；不推断所有 Word 对象都已保真。

下一步：接收方在目标 Word/WPS 打开检查分页；此短文无目录需求，不额外插入目录。

## 核验与局限

重新打开生成 DOCX，原五段文本逐项一致，Heading 1 共两段。
未使用 Word/LibreOffice 渲染，未验收导航窗格实际操作、目录页码或跨页长表。

## 采用的机制

采用 [python-docx 内置样式规则](https://python-docx.readthedocs.io/en/stable/user/styles-using.html)，通过英文样式名建立语义层级。
不采用整段赋值重写：它可能损坏超链接、域及字符格式；视觉验收另列。
