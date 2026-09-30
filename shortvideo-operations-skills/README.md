# 短视频编导岗位技能（Short Video Operations Skills）

> 陆羽Skill 为「短视频编导」岗位生成的体系化 Skill 套件，涵盖短视频完整生产链。侧重**做决策 + 产出质量**。
> 生成时间：2026-10 · 生成器：[陆羽Skill](https://github.com/Luyu2026/Skill-Bible/tree/main/luyu-skill)（元 Skill 工厂）

## 这套库解决什么

短视频编导是从"起号定位"到"发布复盘"的完整内容生产链：定位、选题、脚本、拍摄、剪辑、运营。这套 Skill 库把完整工作链沉淀为 **14 个 Skill**：**先感知判断（顾问团），再产出交付（执行链）**，总控负责路由和编排。

## 成员总览

### 🎯 总控（1）

| Skill | 用途 |
|---|---|
| [shortvideo-master](./shortvideo-master/) | 短视频编导总控：分诊问题 → 路由到最合适的 Skill → 编排多 Skill 链路 |

### ⚙️ 执行链（6，产出型）

| Skill | 什么时候用 | 产出 |
|---|---|---|
| [shortvideo-account](./shortvideo-account/) | 起号、定位、人设搭建 | 账号定位卡（定位一句话/人设/差异化） |
| [shortvideo-topic](./shortvideo-topic/) | 选题、追热点、内容日历 | 选题清单（选题池/评分卡/日历） |
| [shortvideo-script](./shortvideo-script/) | 写脚本、口播稿、分镜 | 视频脚本（钩子/结构/口播/分镜） |
| [shortvideo-production](./shortvideo-production/) | 拍摄、机位、光线、器材 | 拍摄执行清单（拆镜/光线/拍摄SOP） |
| [shortvideo-editing](./shortvideo-editing/) | 剪辑、字幕、BGM、节奏 | 剪辑方案（节奏/精剪/包装/导出） |
| [shortvideo-operations](./shortvideo-operations/) | 发布、数据、复盘、迭代 | 发布运营复盘（数据归因/迭代计划） |

### 🧭 顾问团（7，判断型）

| Skill | 视角 | 擅长 |
|---|---|---|
| [shortvideo-advisory-board](./shortvideo-advisory-board/) | 顾问团总控 | 路由 / 多专家评审会 |
| [shortvideo-advisor-zhangqi](./shortvideo-advisor-zhangqi/) | 张琦（口播爆款） | 口播怎么爆、观点怎么提炼 |
| [shortvideo-advisor-fangqi](./shortvideo-advisor-fangqi/) | 房琪（内容表达） | 文案打动人、表达质感 |
| [shortvideo-advisor-he](./shortvideo-advisor-he/) | 何同学（制作创意） | 创意设计、制作质感 |
| [shortvideo-method-sticky](./shortvideo-method-sticky/) | 《让创意更有黏性》 | 内容被记住、传播设计 |
| [shortvideo-method-copywriting](./shortvideo-method-copywriting/) | 《文案的基本修养》 | 口播/旁白怎么写 |
| [shortvideo-method-supersymbol](./shortvideo-method-supersymbol/) | 《超级符号》 | 账号记忆点、识别体系 |

## 建议使用路径

```
第一次用：先找 shortvideo-master，说清你的问题 → 它告诉你该用哪个
明确场景：直接调对应执行链 Skill（如"帮我写个脚本"→ shortvideo-script）
要专家意见：shortvideo-advisory-board 开评审会，或直接调某位顾问
```

## 安装方式

每个 Skill 是独立目录（SKILL.md + README.md + SOURCES.md），复制到你的 Agent 技能目录即可。
全套复制后，先体验 `shortvideo-master` 的路由，再按需深入单个 Skill。

## 演示工作包

从执行链中挑选最能代表真实工作价值的 1 个场景，制作了可公开展示的完整交付样稿（**数据均为模拟**，替换真实业务数据后可直接用于开会/决策/执行）：

| 演示包 | 场景 | 对应 Skill |
|---|---|---|
| [脚本演示：一条口播视频从 0 到成片](./shortvideo-script/references/demo/demo-shortvideo-script.md) | 起号后第一条口播怎么做 | `shortvideo-script` |

> 演示规范见 `references/demo-document-standard.md`。

## 是什么保证质量

- **调研驱动**：专家/方法论均经蒸馏，心智模型/决策规则标注来源与诚实边界（见 `references/research/`）
- **参考模板**：每个执行链 Skill 带 `references/*-template.md` 完整输出模板（含每节写作指引），SKILL.md 保持轻量（判断+工作流），生成时按模板输出——借鉴自 pm-prd-writer 的成熟做法
- **不编造**：交付物基于你提供的真实材料，信息不足标注 [待确认]
- **证据分级**：数据结论区分 A（数据支持）/ B（强推断）/ C（推测）
- **诚实边界**：每个 Skill 明确写"做不到什么"，不夸大适用范围

## 调研时间戳

2026-10。调研快照与专家/书籍蒸馏见 `references/research/`。

---

> 本职业 Skill 套件由 [陆羽Skill](https://github.com/Luyu2026/Skill-Bible/tree/main/luyu-skill) 生成。
> 哪个专家/哪本书/哪个执行场景不符合预期，告诉我，我单独重做那一个。