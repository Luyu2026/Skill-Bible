# 明确模拟案例：PDF 页面处理与可追溯提取

模拟输入：文件页序 1 为封面；页序 2 印刷页码 1，正文为 Revenue 1200; Cost 800; Net 400。
用户目标：提取正文页，不要封面。
成品定位：文件页序 2 / 印刷页码 1；Revenue=1200，Cost=800，Net=400。
核验：1200-800=400；没有将封面算作正文第一页；扫描 OCR 能力需环境另验。

## 实际交付文件

- [demo-input.pdf](demo-input.pdf)
- [demo-output.pdf](demo-output.pdf)
- [demo-output.txt](demo-output.txt)

## 本次实际验收

系统 PDFKit 实际读取两页输入；提取文件页序 2 的文字并生成单页 PDF；重新打开确认 1 页，三个金额匹配。未测试扫描件 OCR。
