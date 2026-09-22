# overseas-marketing-master · 路由索引

> 本文件是 overseas-marketing-master 的分诊规则、路由表与预置链路索引，供 Agent 路由时快速查表。
> SKILL.md 保持轻量，路由细节在此维护。

## 成员名册

### 执行链（产出型）

| Skill | 一句话职责 | 典型输入 → 输出 |
|-------|-----------|----------------|
| `overseas-marketing-research` | 海外市场调研与竞品分析 | 目标市场 → 市场机会报告 |
| `overseas-marketing-branding` | 品牌定位与差异化 | 产品/目标市场 → 品牌定位文档 |
| `overseas-marketing-content-seo` | 内容营销 + SEO | 关键词/受众 → 内容策略 + SEO 计划 |
| `overseas-marketing-paid-ads` | 付费投放（Google/Meta/社媒） | 预算/目标 → 投放策略 + 广告计划 |
| `overseas-marketing-email` | 邮件营销与自动化 | 用户列表/目标 → 邮件策略 + 自动化流 |
| `overseas-marketing-analytics` | 营销数据分析与归因 | 数据 → 诊断报告 + 优化建议 |

### 顾问团（判断型）

判断类问题一律转交 `overseas-marketing-advisory-board`（顾问团子总控），由它路由到专家/方法论，或召开多专家评审会。成员：Seth Godin（营销哲学）、Neil Patel（SEO/增长实操）、Cialdini（说服心理学）3 位专家视角 + 《This Is Marketing》《Influence》《Building a StoryBrand》3 本方法论。

## 单点路由表

| 用户在说什么 | 路由到 | 备注 |
|---|---|---|
| 海外市场调研 / 竞品分析 / 市场机会 | `overseas-marketing-research` | |
| 品牌定位 / 差异化 / 品牌故事 | `overseas-marketing-branding` | |
| SEO / 内容营销 / 关键词 / 博客 | `overseas-marketing-content-seo` | |
| 谷歌广告 / Meta 广告 / 投放 | `overseas-marketing-paid-ads` | |
| 邮件营销 / 自动化流 / 转化 | `overseas-marketing-email` | |
| 营销数据分析 / 归因 / ROAS | `overseas-marketing-analytics` | |
| 该不该投这个渠道 / 怎么选定位 | `overseas-marketing-advisory-board` | 判断类转交顾问团 |

路由后：说明选择理由（一句话），确认后加载对应 Skill 执行。用户明显着急或指令明确时直接执行，不要多问。

## 预置工作流链路

### 链路 A：从 0 到 1 出海（新市场启动）

```
overseas-marketing-research（市场调研 → 机会报告）
    → overseas-marketing-branding（品牌定位 → 定位文档）
    → overseas-marketing-content-seo（内容与 SEO 基建）
    → overseas-marketing-paid-ads（付费投放冷启动）
```

### 链路 B：从数据问题到优化

```
overseas-marketing-analytics（数据诊断 → 定位瓶颈）
    → 对应执行 Skill（若投放问题 → paid-ads；若内容问题 → content-seo；若转化问题 → email/branding）
```

### 链路 C：判断先行

```
overseas-marketing-advisory-board（该不该做/怎么选 → 条件化结论）
    → 对应执行 Skill（落地执行）
```
