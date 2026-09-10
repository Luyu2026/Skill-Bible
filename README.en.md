<div align="center">

[中文](./README.md) · **English**

# 🧠 Skill Bible

#### Turn recurring real-world blockers into Skills that agents can run reliably and people can reuse.

[![Skills](https://img.shields.io/badge/Skills-66-2563EB?style=for-the-badge)](#-skills)
![Language](https://img.shields.io/badge/Language-English-16A34A?style=for-the-badge)
![Focus](https://img.shields.io/badge/Focus-Real--World-F59E0B?style=for-the-badge)
![Community](https://img.shields.io/badge/Community-Open-7C3AED?style=for-the-badge)

![Claude Code](https://img.shields.io/badge/Claude_Code-Skill-D97706?style=flat-square&logo=anthropic&logoColor=white)
![Codex](https://img.shields.io/badge/Codex-Skill-10B981?style=flat-square&logo=openai&logoColor=white)
![Cross Agent](https://img.shields.io/badge/Cross--Agent-Ready-3B82F6?style=flat-square)

</div>

Skill Bible is an open collection of agent Skills for Claude Code, Codex, Workbuddy, OpenClaw, Hermes Agent, CodeBuddy, Gemini CLI, OpenCode, and other compatible agents.

It is not a collection for one kind of task. Each Skill starts from a recurring real-world blocker: deciding where to apply, turning an idea into a publishable draft, sorting noisy research into a judgment, or removing the same friction from a coding workflow again and again.

When a problem keeps returning and should not require fresh thinking every time, it is worth turning into a Skill. A Skill does not invent your experience or make the final decision for you. It preserves the judgment, workflow, and quality bar so an agent can run it reliably and you can reuse it.

One immediate task can use one Skill. A longer process can let several Skills share the same material and take over in sequence. Job search, for example, can move from role decisions to resumes, interviews, and review.

---

## 🗂️ Directory

| Category | What it helps with | Included now |
|---|---|---|
| ✍️ [**Content creation**](#content-creation) | Turn ideas, materials, and judgments into publishable work | Idea expansion, visual narrative, subtitle timing correction |
| 💼 [**Job search and interviews**](#job-search-and-interviews) | Move from role selection to resume, interviews, and offers | 12 job-search Skills |
| 📈 [**Investment research**](#investment-research) | Research markets, companies, and trading discipline with different frameworks | Chan theory framework |
| 🛤️ [**Long-term planning**](#long-term-planning) | Separate facts, signals, and assumptions to make clearer path decisions | 1 path Skill |
| 🧠 [**Perspectives**](#perspectives) | Use distinct thinking frameworks to cover decision blind spots | 13 perspective Skills |
| 📦 [**Product management**](#product-management) | Move from product judgment and research to prototypes, data, experiments, and review | 21 PM Skills (incl. advisory suite) |
| 📣 [**General operations**](#general-operations) | Cover the full operations workflow: data, campaigns, content, user segmentation, review | 14 operations Skills (incl. advisory suite) |
| 👥 [**User operations**](#user-operations) | Cover the full user lifecycle: segmentation, lifecycle, retention, recall, membership, community | 14 user operations Skills (incl. advisory suite) |
| 🧰 [**Development**](#development-tools) | Add practical capabilities to an agent-driven workflow | Codex pets and more |

---

## ✨ Skills

<a id="content-creation"></a>
### ✍️ Content creation

| Skill | What it helps with |
|---|---|
| [daily-idea-expander](./daily-idea-expander/) | Turn a rough idea into a structured short-video script, edit version, quotes, and titles |
| [wechat-visual-narrative](./wechat-visual-narrative/) | Read a finished WeChat article, identify its visual mode, and plan, generate, and place images that improve comprehension rather than decorate the page |
| [subtitle-retime](./subtitle-retime/) | Correct SRT timing offsets or linear drift from two anchors; preserve text and originals, and deliver a new subtitle file with a per-cue timing report |

<a id="job-search-and-interviews"></a>
### 💼 Job search and interviews

| Skill | What it helps with |
|---|---|
| [job-search-pilot](./job-search-pilot/) | A job-search controller for changing events: role decisions, resumes, interviews, follow-ups, and no-response situations |
| [job-application-match](./job-application-match/) | Separate aspirational roles from roles your current evidence can support, then choose what to apply for and what to improve first |
| [interview-prep-brief](./interview-prep-brief/) | Turn a JD, candidate background, and question bank into a focused interview brief |
| [interview-resume-deep-dive](./interview-resume-deep-dive/) | Turn resume bullets into a two-layer interview bank of surface questions and follow-ups, each grounded in real evidence with a speakable answer and the next likely challenge |
| [interview-round-prep](./interview-round-prep/) | Prepare the same project differently for each interview round |
| [interview-script-naturalizer](./interview-script-naturalizer/) | Turn AI-generated or overly formal interview scripts into natural, speakable answers that retain the user's facts and hold up under follow-up questions |
| [interview-learning-loop](./interview-learning-loop/) | Maintain one evolving interview-training record, update today's task, and route each new practice or interview signal to the right next action |
| [interview-transcript-replay](./interview-transcript-replay/) | Turn an interview transcript into the key misses, revised answers, and a practice plan |
| [resume-ai-naturalizer](./resume-ai-naturalizer/) | Replace generic AI phrasing with evidence-based resume language while preserving facts and follow-up boundaries |
| [resume-jd-tailor](./resume-jd-tailor/) | Turn existing experience into role-specific resume bullets without inventing facts |
| [feishu-resume-template-exporter](./feishu-resume-template-exporter/) | Turn a structured Feishu resume into Word and PDF files that follow the bundled resume layout |
| [offer-decision-advisor](./offer-decision-advisor/) | Compare offers across role, industry, income, city, constraints, and non-negotiables |

<a id="investment-research"></a>
### 📈 Investment research

| Skill | What it helps with |
|---|---|
| [chanlun-framework](./chanlun-framework/) | Chan theory: decompose price action into trend types, central zones, divergences, and buy/sell points to locate positions at the right level; for research, review, and risk checks, not for buy/sell verdicts |

<a id="long-term-planning"></a>
### 🛤️ Long-term planning

| Skill | What it helps with |
|---|---|
| [multi-year-path-planner](./multi-year-path-planner/) | Separate facts, signals, and assumptions to find the next weekly priority |

<a id="perspectives"></a>
### 🧠 Perspectives

The perspective Skills are research-based mental models for decisions, products, learning, and investing. Each is distilled from multi-round research into mental models, decision heuristics, and expression DNA, then activated as first-person role-play.

| Skill | Person | One line |
|---|---|---|
| [duan-yongping-perspective](./duan-yongping-perspective/) | Duan Yongping | Do the right things, and do things right. Buying a stock is buying the company. |
| [munger-perspective](./munger-perspective/) | Charlie Munger | Invert, always invert. Tell me where I'll die, so I never go there. |
| [naval-perspective](./naval-perspective/) | Naval Ravikant | Wealth is what keeps working for you while you sleep. |
| [steve-jobs-perspective](./steve-jobs-perspective/) | Steve Jobs | Focus is not saying yes to what you want; it is saying no to a hundred good ideas. |
| [elon-musk-perspective](./elon-musk-perspective/) | Elon Musk | Physics is the only hard constraint; everything else is a suggestion. |
| [feynman-perspective](./feynman-perspective/) | Richard Feynman | If you can't explain it to a freshman, you don't really understand it. |
| [taleb-perspective](./taleb-perspective/) | Nassim Taleb | Don't be a fragile fool. Antifragile things gain from disorder. |
| [livermore-perspective](./livermore-perspective/) | Jesse Livermore | Don't predict direction; wait for the line of least resistance to confirm. |
| [graham-perspective](./graham-perspective/) | Benjamin Graham | Mr. Market quotes daily; your margin of safety decides whether to listen. |
| [li-ka-shing-perspective](./li-ka-shing-perspective/) | Li Ka-shing | Think failure first, then success. Cash is king; fix the roof in sunshine. |
| [inamori-perspective](./inamori-perspective/) | Kazuo Inamori | As a human being, what is right? Pure motive, no selfish intent. |
| [laozi-perspective](./laozi-perspective/) | Laozi | The Way moves by returning. Things reverse at the extreme; the soft overcomes the hard. |
| [wang-yangming-perspective](./wang-yangming-perspective/) | Wang Yangming | Mind is principle; knowledge and action are one. Extend your innate knowing. |

<a id="product-management"></a>
### 📦 Product management

Start with `pm-master` when the product problem is unclear, then bring in only the needed Skills for discovery, requirements, review, prioritization, roadmap, measurement, experimentation, analysis, or retrospective. Every Skill also works on its own.

| Skill | What it helps with |
|---|---|
| [pm-master](./pm-master/) | Product workflow dispatcher: triage the problem → route to the right Skill → orchestrate multi-Skill chains so each step's output feeds the next |
| [pm-prd-writer](./pm-prd-writer/) | Turn a fuzzy idea or user problem into a reviewable PRD: stage-zero requirement check, four-stage workflow (clarify → structure → enrich → deliver), and a confirmation checklist; degrades to a scoping doc when input is insufficient |
| [pm-review-board](./pm-review-board/) | Simulate a six-role review (product, engineering, test, design, operations, legal) with severity tiers and opinion quality red lines, surfacing review-day objections before the meeting |
| [pm-advisory-board](./pm-advisory-suite/pm-advisory-board/) | Expert advisory board: Cagan, Torres, Yu Jun + Mom Test / Story Mapping / Build Trap, making "should we do this" disagreements explicit |
| [pm-advisor-cagan](./pm-advisory-suite/pm-advisor-cagan/) | Marty Cagan lens: review value, usability, feasibility, and business-sustainability risks |
| [pm-advisor-torres](./pm-advisory-suite/pm-advisor-torres/) | Teresa Torres lens: organize outcomes, opportunities, solutions, and assumptions into an opportunity solution tree |
| [pm-advisor-yujun](./pm-advisory-suite/pm-advisor-yujun/) | Yu Jun lens: user value = new experience − old experience − switching cost |
| [pm-method-mom-test](./pm-advisory-suite/pm-method-mom-test/) | The Mom Test: rewrite interviews around past behavior, concrete facts, and real commitments |
| [pm-method-story-mapping](./pm-advisory-suite/pm-method-story-mapping/) | User Story Mapping: align the full journey and slice an end-to-end testable MVP |
| [pm-method-build-trap](./pm-advisory-suite/pm-method-build-trap/) | Escaping the Build Trap: reconnect the roadmap to observable outcomes |
| [pm-survey-designer](./pm-survey-designer/) | Design high-quality surveys from research goals: every question maps to a hypothesis, with bias/double-barrel/sampling checks |
| [pm-competitor-deconstructor](./pm-competitor-deconstructor/) | Deconstruct competitors across strategy, capability, experience, and growth; separate borrowable from non-copyable and unvalidated opportunities |
| [pm-prioritization-engine](./pm-prioritization-engine/) | RICE / ICE / Kano multi-model scoring + hard constraints + sensitivity analysis |
| [pm-roadmap-planner](./pm-roadmap-planner/) | Turn quarterly goals, capacity, and dependencies into a version roadmap with milestones, risks, and buffers |
| [pm-tracking-spec-writer](./pm-tracking-spec-writer/) | Break product goals and user journeys into event dictionaries, metric definitions, privacy boundaries, and QA checklists |
| [pm-experiment-designer](./pm-experiment-designer/) | Complete A/B experiment design: falsifiable hypotheses, allocation, sample size, stop rules, and decision criteria |
| [pm-analytics](./pm-analytics/) | From data signals to product decisions: data health check, metric decomposition, evidence-graded attribution, visualized report |
| [pm-postmortem-writer](./pm-postmortem-writer/) | Structured retrospective: 5-Why root-cause evidence + enforced graded action items, ready to publish |
| [pm-image2proto](./pm-image2proto/) | Screenshot → runnable, inspectable, editable HTML prototype |
| [pm-image2pencil](./pm-image2pencil/) | Screenshot → editable Pencil design + structured design doc |
| [pm-url2proto](./pm-url2proto/) | Authorized webpage → local, maintainable Next.js prototype project |

<a id="general-operations"></a>
### 📣 General operations

A Skill suite for the general operations role, covering the full operations workflow (data → campaigns → content → users → review → strategy). Start with `operations-master` to triage the blocker, then bring in what's needed; judgment questions go to the `operations-advisory-board` (Huang Youcan / Zhang Liang / Qu Hui + three classic methodology books).

| Skill | What it helps with |
|---|---|
| [operations-master](./general-operations-skills/operations-master/) | Operations dispatcher: triage → route to the right Skill → orchestrate multi-Skill chains |
| [operations-strategy](./general-operations-skills/operations-strategy/) | Period strategy: goal decomposition, strategy selection, resource allocation, milestone rhythm |
| [operations-data-analysis](./general-operations-skills/operations-data-analysis/) | Data attribution & decisions: turn metric anomalies/funnels/retention into evidence-graded (A/B/C) findings and actions |
| [operations-activity-planner](./general-operations-skills/operations-activity-planner/) | Campaign planning: fuzzy idea → executable plan with ROI estimate and risk control |
| [operations-content-strategy](./general-operations-skills/operations-content-strategy/) | Content strategy: topic matrix + publishing calendar + data feedback loop |
| [operations-user-segmentation](./general-operations-skills/operations-user-segmentation/) | User segmentation & outreach: RFM/lifecycle tiers + differentiated strategies per tier |
| [operations-review](./general-operations-skills/operations-review/) | Retrospective: root-cause evidence (5-Why) + enforced graded, trackable action items |
| [operations-advisory-board](./general-operations-skills/operations-advisory-board/) | Advisory board dispatcher: route to experts/methods, or run a multi-expert review (consensus/disagreement/synthesized conclusion) |
| [operations-advisor-huang](./general-operations-skills/operations-advisor-huang/) | Huang Youcan lens: operations value judgment, "setting the game" / breakthrough thinking, deferred rewards |
| [operations-advisor-zhang](./general-operations-skills/operations-advisor-zhang/) | Zhang Liang lens: four-module operations system, user lifecycle, refined operations |
| [operations-advisor-qu](./general-operations-skills/operations-advisor-qu/) | Qu Hui lens: growth experiment loop, North Star metric, growth model |
| [operations-method-light-of-operations](./general-operations-skills/operations-method-light-of-operations/) | *The Light of Operations*: setting the game, four operations mindsets, the operations formula |
| [operations-method-lean-analytics](./general-operations-skills/operations-method-lean-analytics/) | *Lean Analytics*: One Metric That Matters, lean analytics cycle, five stage gates |
| [operations-method-growth-hacking](./general-operations-skills/operations-method-growth-hacking/) | *Hacking Growth*: growth experiment loop, North Star metric, AARRR funnel |

<a id="user-operations"></a>
### 👥 User operations

A systematic Skill suite generated by LuyuSkill for the user operations role, covering the full user lifecycle (segmentation → lifecycle → retention → recall → membership → community). Start with `user-operations-master` to triage the blocker; judgment questions go to the `user-operations-advisory-board` (Zhang Liang / Qu Hui / Xu Zhibin + three methodology books).

| Skill | What it helps with |
|---|---|
| [user-operations-master](./user-operations-skills/user-operations-master/) | User operations dispatcher: triage → route to the right Skill → orchestrate multi-Skill chains |
| [user-operations-segmentation](./user-operations-skills/user-operations-segmentation/) | Segmentation system: RFM/lifecycle/value tiers + differentiated strategies per tier |
| [user-operations-lifecycle](./user-operations-skills/user-operations-lifecycle/) | Lifecycle operations: stage goals/strategies/actions + stage conversion and churn prevention |
| [user-operations-retention](./user-operations-skills/user-operations-retention/) | Retention: diagnose → locate churn → design habit mechanisms → retention experiments |
| [user-operations-recall](./user-operations-skills/user-operations-recall/) | Win-back & recall: hook design + channel cost + recall experiments |
| [user-operations-membership](./user-operations-skills/user-operations-membership/) | Membership: tiers/benefits/points/growth value/ROI |
| [user-operations-community](./user-operations-skills/user-operations-community/) | Community: small-group split/activity mechanics/incentives & conversion |
| [user-operations-advisory-board](./user-operations-skills/user-operations-advisory-board/) | Advisory board dispatcher: route to experts/methods, or run a multi-expert review |
| [user-operations-advisor-zhang](./user-operations-skills/user-operations-advisor-zhang/) | Zhang Liang lens: lifecycle, acquisition/retention, refined operations |
| [user-operations-advisor-qu](./user-operations-skills/user-operations-advisor-qu/) | Qu Hui lens: retention experiments, North Star metric, growth model |
| [user-operations-advisor-xu](./user-operations-skills/user-operations-advisor-xu/) | Xu Zhibin lens: small-group effect, social dividend, user incentives |
| [user-operations-method-hooked](./user-operations-skills/user-operations-method-hooked/) | *Hooked*: Hook model, habit formation, retention mechanics |
| [user-operations-method-membership](./user-operations-skills/user-operations-method-membership/) | *The Membership Economy*: membership model, value ladder, freemium |
| [user-operations-method-small-group](./user-operations-skills/user-operations-method-small-group/) | *The Small Group Effect*: three-close-one-reverse, community growth & incentive engine |

<a id="development-tools"></a>
### 🧰 Development

| Skill | What it helps with |
|---|---|
| [codex-pet-maker](./codex-pet-maker/) | Create, repair, package, and install animated Codex desktop pets |

## 📦 Install one Skill

Open the page of the Skill you want, copy its URL, and send this to your agent:

```text
Please install this Skill:
[paste the Skill page URL here]

I only want this one Skill, not the whole repository.
Please identify my current agent, choose the correct Skill directory and download method, and install it.
Afterward, tell me where it was installed and give me one sentence I can use to trigger it.
```

To install the whole collection, send your agent this repository URL:

```text
https://github.com/Luyu2026/Skill-Bible
```

If you do not have Feishu CLI configured, document-producing Skills can still write local Markdown rather than stopping on permissions.

## 🌱 Contribute

You can submit an original Skill or simply recommend an external one. Use [Submit / recommend a Skill](https://github.com/Luyu2026/Skill-Bible/issues/new?template=submit-skill.yml) and complete the form with its source, real-world scenario, and example run.

Skill Bible is not trying to mirror every Skill file on the internet. We care whether a Skill solves a real problem, can be reproduced by someone else, works on the agents it claims to support, and is maintained responsibly.

| Status | Meaning | How to read it |
|---|---|---|
| Community Candidate | Source, author, and license are complete; it has not been verified yet | Discoverable, not a recommendation |
| Verified | At least one reproducible basic run is complete | Safe to try from the instructions |
| Editor's Pick | Clear real-world value, documented boundaries, and maintainable quality | Worth prioritizing |

Skill Bible keeps the final right to include, grade, and recommend a Skill. The goal is not a pile of files. The goal is to help Chinese-speaking users find Skills that actually work.

## License

Skill-Bible uses split licensing so people and Agents can determine reuse
rights clearly:

- Original Skill instructions, documentation, examples, and evaluation
  materials are available under [CC BY-NC 4.0](./LICENSE): attribution is
  required, and commercial use requires separate permission.
- Code and scripts are available under [Apache License 2.0](./LICENSE-CODE).
- Third-party material, fonts, templates, images, user-provided material, and
  the Skill-Bible name and visual identity are not automatically licensed by
  either license. See [NOTICE](./NOTICE) for the scope and exceptions.

For commercial licensing, open a GitHub Issue with the intended use and
contact details.
