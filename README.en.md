<div align="center">

[中文](./README.md) · **English**

# 🧠 Skill Bible

#### Turn recurring real-world blockers into Skills that agents can run reliably and people can reuse.

[![Skills](https://img.shields.io/badge/Skills-18-2563EB?style=for-the-badge)](#-skills)
![Language](https://img.shields.io/badge/Language-English-16A34A?style=for-the-badge)
![Focus](https://img.shields.io/badge/Focus-Real--World-F59E0B?style=for-the-badge)
![Community](https://img.shields.io/badge/Community-Open-7C3AED?style=for-the-badge)

![Claude Code](https://img.shields.io/badge/Claude_Code-Skill-D97706?style=flat-square&logo=anthropic&logoColor=white)
![Codex](https://img.shields.io/badge/Codex-Skill-10B981?style=flat-square&logo=openai&logoColor=white)
![Cross Agent](https://img.shields.io/badge/Cross--Agent-Ready-3B82F6?style=flat-square)

</div>

Skill Bible is an open collection of agent Skills for Claude Code, Codex, Workbuddy, OpenClaw, Hermes Agent, CodeBuddy, Gemini CLI, OpenCode, and other compatible agents.

Each Skill starts with a concrete situation: a job application with no reply, a resume that cannot explain the right capability, an interview answer that falls apart under follow-up questions, or a decision that feels too important to make from emotion alone.

---

## 🗂️ Start with the problem you have now

You do not need to understand Skills, MCP, or agents first. Start with the situation you are in.

| What is happening now? | Try this first | What you get first |
|---|---|---|
| You applied to many jobs and do not know which ones deserve real effort | [Job Application Match](./job-application-match/) | A practical application order |
| One experience needs to work for different roles, but every resume version sounds generic | [Resume JD Tailor](./resume-jd-tailor/) | Role-specific resume language |
| You have an interview tomorrow and do not know which questions to practice first | [Interview Prep Brief](./interview-prep-brief/) | Likely questions, project stories, and follow-up paths |
| You just finished an interview and know it went wrong, but not what to fix next time | [Interview Transcript Replay](./interview-transcript-replay/) | Three answers you can practice for the next round |
| Your job search changes every day and you cannot tell what matters today | [Job Search Pilot](./job-search-pilot/) | The next action for the current event |
| You want to change direction without making an emotional, irreversible decision | [Life Odyssey Planner](./life-odyssey-planner/) | Three viable paths and one reversible experiment |

Every Skill page starts with the same three answers: when to use it, what to provide, and what result it can move forward.

## 💡 What Skill Bible is building

Many difficult tasks are not difficult because people cannot do them. They are difficult because each time they require fresh judgment, scattered materials, and a new plan.

Skill Bible turns the repeated, judgment-heavy part of those tasks into reusable agent workflows. You can run one Skill on its own or connect several into a longer workflow.

The job-search workflow is the first complete example:

`Job Match → Resume Tailor → Interview Brief → Interview Round Prep → Interview Replay`

Skills do not invent your experience or make your final decision. They organize the evidence, questions, actions, and feedback needed to make a better one.

## 🤝 Community curation

Skill Bible is not trying to mirror every Skill file on the internet. We care whether a Skill solves a real problem, can be reproduced by someone else, works on the agents it claims to support, and is maintained responsibly.

| Status | Meaning | How to read it |
|---|---|---|
| Community Candidate | Source, author, and license are complete; it has not been verified yet | Discoverable, not a recommendation |
| Verified | At least one reproducible basic run is complete | Safe to try from the instructions |
| Editor's Pick | Clear real-world value, documented boundaries, and maintainable quality | Worth prioritizing |

Want to submit an original Skill, recommend an external project, or volunteer as a tester? Read [Submit a Skill](./SUBMIT_A_SKILL.md). External projects remain credited to their authors and linked to their original source. Projects without clear permission are indexed, not mirrored.

## ✨ Skills

### ✍️ Content creation

| Skill | What it helps with |
|---|---|
| [daily-idea-expander](./daily-idea-expander/) | Turn a rough idea into a structured short-video script, edit version, quotes, and titles |

### 💼 Job search and interviews

| Skill | What it helps with |
|---|---|
| [job-search-pilot](./job-search-pilot/) | A job-search controller for changing events: role decisions, resumes, interviews, follow-ups, and no-response situations |
| [job-application-match](./job-application-match/) | Separate aspirational roles from roles your current evidence can support, then choose what to apply for and what to improve first |
| [interview-prep-brief](./interview-prep-brief/) | Turn a JD, candidate background, and question bank into a focused interview brief |
| [interview-round-prep](./interview-round-prep/) | Prepare the same project differently for each interview round |
| [interview-transcript-replay](./interview-transcript-replay/) | Turn an interview transcript into the key misses, revised answers, and a practice plan |
| [resume-jd-tailor](./resume-jd-tailor/) | Turn existing experience into role-specific resume bullets without inventing facts |
| [offer-decision-advisor](./offer-decision-advisor/) | Compare offers across role, industry, income, city, constraints, and non-negotiables |

### 🛤️ Life and long-term decisions

| Skill | What it helps with |
|---|---|
| [life-odyssey-planner](./life-odyssey-planner/) | Map three credible paths and one reversible 90-day experiment |
| [multi-year-path-planner](./multi-year-path-planner/) | Separate facts, signals, and assumptions to find the next weekly priority |

### 🧠 Perspectives

The perspective Skills are research-based mental models for decisions, products, learning, and investing. They include Duan Yongping, Charlie Munger, Naval Ravikant, Steve Jobs, Elon Musk, Richard Feynman, and Nassim Taleb.

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

You can submit an original Skill or simply recommend an external one. Use [Submit a Skill](./SUBMIT_A_SKILL.md) to include its source, real-world scenario, and example run.

Skill Bible keeps the final right to include, grade, and recommend a Skill. The goal is not a pile of files. The goal is to help Chinese-speaking users find Skills that actually work.
