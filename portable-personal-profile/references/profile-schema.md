# Schema v1

所有文件 UTF-8。manifest.json 是对象：schema_version=1、version（字符串）、visibility=private；simulation 为可选布尔值。四个 JSONL 文件每行一个对象，空档案允许空文件。全包 id 全局唯一，使用小写字母开头的字母数字、点和连字符。

facts、preferences、projects、open-questions 统一必填：

| 字段 | 含义 |
|---|---|
| id | 稳定语义键，例如 fact.identity、pref.copy-length、project.navigator |
| category | 具体类别，例如 identity、writing、project、question |
| content | 非空、单一主张或待回答的问题 |
| source_type | document / user / ai / import |
| source_refs | 非空列表，来源 id，可附 #小节定位 |
| collected_at | ISO 日期/时间，采集时间不是事件发生时间 |
| status | confirmed/current/inferred/unconfirmed/expired/superseded/conflict |
| confidence | 0–1 数字；表示提取者把握，不表示事实已确认 |
| review_trigger | 非空下次复核日期或具体事件 |
| sensitive | 布尔值，敏感信息为 true |

sources.json 是数组；每项 id 唯一，type 同 source_type 枚举，collected_at 为 ISO 时间，path 为包内存在的相对 UTF-8 摘录文件，另可有 title、模拟标记。source_refs 的 #后缀是人工可读定位，由回读检查，不是脚本自动语义核验。

冲突仍只有一个主记录 id，content 写冲突摘要，status=conflict、resolution=pending_user、variants 至少两个不同值。每个 variant 包含 content、source_type、source_refs。主记录来源应汇总双方。未标 conflict 而携带 variants 或出现重复 id 都校验失败；不要用新 id 绕过去重。

例如偏好记录可写为以下 JSON（仅 schema 示例，不代表用户事实）：

```json
{"id":"pref.copy-length","category":"writing","content":"字数限制有分歧","source_type":"document","source_refs":["s1","s2"],"collected_at":"2026-11-25","status":"conflict","confidence":1.0,"review_trigger":"本人区分适用情境后","sensitive":false,"resolution":"pending_user","variants":[{"content":"短于200字","source_type":"document","source_refs":["s1"]},{"content":"不限字数但结构简洁","source_type":"document","source_refs":["s2"]}]}
```

没有实现自动抽取、自动合并、真实性验证或语义矛盾识别。Agent 负责这些判断，validator 提供结构门槛。JSONL 一行一条便于 diff，Git 不保证自动合并在语义上正确。
