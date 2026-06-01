<div align="center">

# 塔勒布.skill

> *"Don't cross a river if it is four feet deep on average."*

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Skill-blueviolet)](https://claude.ai/code)
[![Nuwa](https://img.shields.io/badge/Made%20with-女娲.skill-orange)](https://github.com/alchaincyf/nuwa-skill)

<br>

**Nassim Nicholas Taleb的认知操作系统。不是语录合集，是可运行的思维框架。**

<br>

基于 Incerto 五部曲、50+ 场访谈、Twitter/Medium 碎片表达、<br>
外部批评分析等 40+ 个来源深度调研，<br>
提炼 6 个核心心智模型、9 条决策启发式和完整的表达DNA。

[看效果](#效果示例) · [安装](#安装) · [蒸馏了什么](#蒸馏了什么) · [调研来源](#调研来源)

</div>

---

## 效果示例

### 问：我想辞职全职做AI创业，手上有50万存款，够撑一年。值不值得赌？

```
塔勒布    ❯ 你刚刚犯了一个经典的遍历性错误。

            你看了一眼AI创业的「平均回报」——某某人融了几千万，
            某某公司估值翻了十倍——然后你觉得这个赌局的期望值是正的。

            但你不是在玩集合概率。你是一个人，只有一条命，
            50万花完就是花完了。100个人赌，10个赢了你看得到，
            90个输了你看不到。但更要命的是：你输了就出局了。

            正确的做法？杠铃策略。
            不要辞职。90%的精力保住现金流，10%做你的AI项目。

            「All-in」是一个被硅谷包装得很漂亮的自杀策略。就这样。
```

### 问：我朋友推荐一个年化8%的理财产品，过去5年很稳定，从没亏过。

```
塔勒布    ❯ 「过去5年从没亏过。」

            你知道火鸡在感恩节前的第1000天也可以这样说吗？
            「过去1000天，每天都被喂食，从没饿过。」
            然后第1001天，它变成了晚餐。

            一个产品「从没亏过」不是安全的证据。
            它可能恰恰是危险的证据——
            说明它在积累隐性的尾部风险。

            让我问你三个问题：
            这个8%来自哪里？最坏情况你会亏多少？
            推荐给你的朋友，他自己投了多少？

            如果他只投了5%的身家，那他对你说「很稳」的时候，
            他没有足够的skin in the game。
```

### 问：每周都有新AI工具出来，我总觉得跟不上，该学什么？

```
塔勒布    ❯ 你问错了问题。
            问题不是「该学什么」，问题是「该不学什么」。
            Via Negativa.

            每周出来的新AI工具，99%会在一年内消失。
            你现在焦虑地追逐的东西，
            大部分在你学会之前就已经死了。
            这不是猜测——这是林迪效应的反面。

            Python存在了35年。概率论存在了400年。
            写作存在了5000年。
            它们的预期寿命远超任何叫「XX.ai」的东西。

            停止订阅那些「每日AI新闻」。
            停止刷那些「10个你必须知道的新工具」。
            做减法，不是做加法。

            深度胜过广度。一万倍。
```

### 问：很多AI大佬都说AGI三年内就到，该相信吗？

```
塔勒布    ❯ 先告诉我一件事：
            这些「大佬」如果预测错了，会发生什么？

            他们会被开除吗？会亏钱吗？
            不会。他们明年会继续上台演讲，继续收出场费，
            继续说「再等两年」。
            一个没有后果的预测不是预测，是marketing。

            而且注意——说「AGI很快到来」的人大多在卖什么东西。
            卖GPU的说很快，因为你今天就要买显卡。
            卖AI课程的说很快，因为你今天就要报名。
            他们的「预测」和他们的「利益」完全对齐。
            这不叫预测，这叫广告。

            别预测。建立反脆弱性。
            如果AGI真的来了，你怎么从中获益？
            如果十年后还没来，你的当下决策会让你破产吗？

            回答这两个问题，比听任何「大佬」都有用。
```

> 完整的4轮实战对话记录在 [`examples/`](examples/) 目录。

这不是ChatGPT套了个塔勒布面具。每段回应都在运用具体的心智模型——「遍历性检验」「火鸡问题」「林迪效应」「Skin in the Game」。它不复读语录，它用塔勒布的认知框架分析你的问题。

---

## 安装

```bash
npx skills add alchaincyf/taleb-skill
```

然后在 Claude Code 里：

```
> 用塔勒布的视角帮我分析这个投资决策
> 这个项目有尾部风险吗？
> 切换到塔勒布，我在纠结要不要all-in
> 这些专家的预测有skin in the game吗？
```

---

## 蒸馏了什么

### 6个心智模型

| 模型 | 一句话 | 来源 |
|------|--------|------|
| **非对称风险思维** | 永远先看下行风险的代价，而不是期望值 | 1987年黑色星期一、Universa 2020年3月 |
| **反脆弱偏好** | 不是抵抗混乱，而是从混乱中获益 | 杠铃策略、硬拉训练、间歇性断食 |
| **Skin in the Game检验** | 别告诉我你怎么想，告诉我你的投资组合 | 汉谟拉比法典、CalPERS案例 |
| **林迪效应筛选** | 存在越久的东西，越可能继续存在 | 地中海饮食、东正教200+天斋戒 |
| **Via Negativa** | 改进不来自增加更多，而来自去除有害的 | 饮食排除法、laconic写作 |
| **领域特异性** | 能力和理性都是领域特定的，不能跨域迁移 | 主教vs经济学家、塔勒布本人 |

### 9条决策启发式

1. 预防原则（不确定时行动，而非等待）
2. 杠铃策略（极端保守 + 极端冒险，避免中间地带）
3. 遍历性检验（会破产吗？）
4. 火鸡问题（过去的稳定不能预测未来）
5. 少数派规则（找到那不妥协的3%）
6. 框架重置（不回答烂问题，重新定义问题）
7. 绿木交易员原则（实践知识 > 理论知识）
8. 凸性试错（保留上行，限制下行）
9. 反信号启发式（粗犷 = 能力信号）

### 表达DNA

- **词汇**：IYI、Fragilista、BS Vendor、Mediocristan/Extremistan、iatrogenics、ergodicity
- **句式**：格言体为主，类比攻击句（X is to Y what Z is to W），反转句
- **节奏**：先砸结论再给理由，极短句和极长句交替，「OK?」结尾
- **态度**：确定性极高，攻击性是feature，古典引用压制现代争论
- **幽默**：地中海式苦涩格言，极端对比制造笑点

### 7对内在张力

这不是脸谱化的「风险大师」。Skill保留了塔勒布的矛盾：

- 思想反脆弱 vs 自尊脆弱
- 反学院 vs 自己是NYU教授
- 主张减法 vs Twitter上不断增加噪音
- 鼓吹skin in the game vs 自己在某些领域缺乏
- 蔑视社交媒体辩论 vs 是Twitter上最活跃的知识分子
- 推崇沉默和行动 vs 是最多话的公共知识分子
- 书中倡导谦逊 vs 个人行为展现傲慢

---

## 调研来源

5个调研文件，全部在 [`references/`](references/) 目录：

| 文件 | 内容 |
|------|------|
| `research.md` | 调研总览、一手来源索引、矛盾与待验证 |
| `塔勒布思想体系调研.md` | Incerto五部曲、11条核心论点、20+自创术语、智识谱系 |
| `塔勒布深度对话调研.md` | 8个核心访谈源、13个经典类比、框架重置思维模式 |
| `塔勒布碎片表达与社交媒体人格调研.md` | 表达DNA、五级攻击体系、6组核心矛盾 |
| `塔勒布外部批评调研.md` | 「两个塔勒布」分裂、vs Kahneman/Pinker对比 |
| `塔勒布重大决策与实际行动调研-20260404.md` | 1987年黑色星期一、Universa 3612%回报、言行一致性评分 |

### 一手来源

Incerto五部曲 (2001-2018) · Statistical Consequences of Fat Tails (2020) · The Bed of Procrustes · Tim Ferriss Show #691 · BLOCKCON 2018 (Taleb & Naval) · Conversations with Tyler Ep.41 · EconTalk多期 · The Spectator深度采访 · Art of Manliness播客 · Medium/INCERTO专栏 · arXiv论文

### 外部批评

Allen Farrington "A Tale of Two Talebs" · Steven Pinker逐条反驳 · Daniel Kahneman锚定偏差批评 · Ryan Murphy (SMU) · Discover Magazine · The Economist / The Guardian书评 · Genetic Literacy Project

信息源已排除知乎/微信公众号/百度百科。

---

## 这个Skill是怎么造出来的

由 [女娲.skill](https://github.com/alchaincyf/nuwa-skill) 自动生成。

女娲的工作流程：输入一个名字 → 多个Agent并行调研（著作/对话/表达/批评/决策）→ 交叉验证提炼心智模型 → 构建SKILL.md → 质量验证。

想蒸馏其他人？安装女娲：

```bash
npx skills add alchaincyf/nuwa-skill
```

然后说「蒸馏一个XXX」就行了。

---

## 仓库结构

```
taleb-skill/
├── README.md
├── SKILL.md                                        # 可直接安装使用
├── LICENSE
├── references/
│   ├── research.md                                 # 调研总览
│   ├── 塔勒布思想体系调研.md
│   ├── 塔勒布深度对话调研.md
│   ├── 塔勒布碎片表达与社交媒体人格调研.md
│   ├── 塔勒布外部批评调研.md
│   └── 塔勒布重大决策与实际行动调研-20260404.md
└── examples/
    └── demo-conversation.md                        # 4轮实战对话记录
```

---

## 更多.skill

女娲已蒸馏的其他人物，每个都可独立安装：

| 人物 | 领域 | 安装 |
|------|------|------|
| [乔布斯.skill](https://github.com/alchaincyf/steve-jobs-skill) | 产品/设计/战略 | `npx skills add alchaincyf/steve-jobs-skill` |
| [马斯克.skill](https://github.com/alchaincyf/elon-musk-skill) | 工程/成本/第一性原理 | `npx skills add alchaincyf/elon-musk-skill` |
| [纳瓦尔.skill](https://github.com/alchaincyf/naval-skill) | 财富/杠杆/人生哲学 | `npx skills add alchaincyf/naval-skill` |
| [芒格.skill](https://github.com/alchaincyf/munger-skill) | 投资/多元思维/逆向思考 | `npx skills add alchaincyf/munger-skill` |
| [费曼.skill](https://github.com/alchaincyf/feynman-skill) | 学习/教学/科学思维 | `npx skills add alchaincyf/feynman-skill` |
| [张雪峰.skill](https://github.com/alchaincyf/zhangxuefeng-skill) | 教育/职业规划/阶层流动 | `npx skills add alchaincyf/zhangxuefeng-skill` |

想蒸馏更多人？用 [女娲.skill](https://github.com/alchaincyf/nuwa-skill)，输入任何名字即可。

## 许可证

MIT — 随便用，随便改，随便蒸馏。

---



---

## 关于作者

**花叔 Huashu** — AI Native Coder，独立开发者，代表作：小猫补光灯（AppStore 付费榜 Top1）

| 平台 | 链接 |
|------|------|
| 🌐 官网 | [bookai.top](https://bookai.top) · [huasheng.ai](https://www.huasheng.ai) |
| 𝕏 Twitter | [@AlchainHust](https://x.com/AlchainHust) |
| 📺 B站 | [花叔](https://space.bilibili.com/14097567) |
| ▶️ YouTube | [@Alchain](https://www.youtube.com/@Alchain) |
| 📕 小红书 | [花叔](https://www.xiaohongshu.com/user/profile/5abc6f17e8ac2b109179dfdf) |
| 💬 公众号 | 微信搜「花叔」或扫码关注 ↓ |

<img src="wechat-qrcode.jpg" alt="公众号二维码" width="360">

<div align="center">

*The three most harmful addictions are heroin, carbohydrates, and a monthly salary.*

<br>

MIT License &copy; [花叔 Huashu](https://github.com/alchaincyf)

Made with [女娲.skill](https://github.com/alchaincyf/nuwa-skill)

</div>
