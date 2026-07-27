<div align="center">

<img src="assets/banner.svg" alt="Awesome AI Literature Review Agents & Tools" width="100%">

# Awesome AI Literature Review Agents & Tools

**🤖 面向「智能体文献综述」的最强开源技能、工具与框架大全**

_让 AI 智能体帮你完成 检索 → 阅读 → 抽取 → 综述 → 引用核查 的全流程_

[![Awesome](https://awesome.re/badge.svg)](https://awesome.re)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)
[![License: CC0-1.0](https://img.shields.io/badge/License-CC0%201.0-lightgrey.svg)](LICENSE)
[![Stars](https://img.shields.io/github/stars/brycewang-stanford/lit-review-agent-tools?style=social)](https://github.com/brycewang-stanford/lit-review-agent-tools/stargazers)
[![Last Commit](https://img.shields.io/github/last-commit/brycewang-stanford/lit-review-agent-tools)](https://github.com/brycewang-stanford/lit-review-agent-tools/commits)
<!-- BEGIN GENERATED:badge -->
![Tools](https://img.shields.io/badge/tools-66-blue)
<!-- END GENERATED:badge -->

**简体中文** · [English](README.en.md) · **[🔍 可搜索站点](https://brycewang-stanford.github.io/lit-review-agent-tools/)**

<!-- BEGIN GENERATED:tagline -->
<em>收录 <b>66</b> 个用于文献综述的开源项目，按使用场景分类 · 每季度更新 · 欢迎 PR</em>
<!-- END GENERATED:tagline -->

</div>

---

> 🔍 **[打开可搜索版本 →](https://brycewang-stanford.github.io/lit-review-agent-tools/)** —— 按使用场景、维护状态、许可证即时筛选，中英双语。
>
> 🧪 **[实测工作流 →](recipes/)** —— 4 条**真跑过**的流水线（含实际输出与踩坑），全部无需 API key。
> 例：ASReview 在一份已发表综述的数据上，**只筛 5.5%（248/4544）就找全了 38 篇相关文献**。
>
> 🧭 **[按工作阶段查表 →](STAGES.md)** —— 检索/筛选/抽取/精读/综合/引用核查/写作/评审。
>
> 收录用于**文献综述（Literature Review）**的开源 AI 智能体、Claude Code / Codex 技能、MCP 服务器、系统综述筛选工具、PDF 解析、引文图谱与自动综述框架。
> 目标：成为研究者用 AI 做文献工作的**一站式导航**。⭐ **Star 收藏，随时查阅。**

## 📑 目录

- [为什么需要这个清单](#为什么需要这个清单)
- [⚡ 30 秒选型](#-30-秒选型)
<!-- BEGIN GENERATED:toc -->
- [🌟 综合研究智能体与技能](#-综合研究智能体与技能)
- [🔎 深度研究与自动综述生成](#-深度研究与自动综述生成)
- [🧪 自主科研：从想法到论文](#-自主科研从想法到论文)
- [📚 文献问答与 RAG](#-文献问答与-rag)
- [🧮 系统综述与文献筛选](#-系统综述与文献筛选)
- [🔌 MCP 服务器](#-mcp-服务器)
- [🗂️ 文献管理与 Zotero / Obsidian 集成](#️-文献管理与-zotero--obsidian-集成)
- [📄 PDF → 结构化数据抽取](#-pdf--结构化数据抽取)
- [🕸️ 引文图谱与 API 客户端](#️-引文图谱与-api-客户端)
- [✍️ 论文写作与同行评审助手](#️-论文写作与同行评审助手)
- [📖 精选清单（Awesome Lists）](#-精选清单awesome-lists)
<!-- END GENERATED:toc -->
- [🏢 商业 / 闭源工具（参考）](#-商业--闭源工具参考)
- [🧭 如何选择（决策表）](#-如何选择决策表)
- [📈 Star 趋势](#-star-趋势)
- [🤝 参与贡献](#-参与贡献)
- [📄 许可证](#-许可证)

> 另见：[STAGES.md](STAGES.md)（按阶段的覆盖矩阵）· [recipes/](recipes/)（实测工作流）· [HEALTH.md](HEALTH.md)（每个项目的完整元数据）· [CHANGELOG.md](CHANGELOG.md)（新增与观察名单）· [data/tools.json](data/tools.json)（可直接使用的数据集）

> ⭐ = 编辑推荐 ｜ Stars 为 GitHub API 快照，**每周由 GitHub Action 自动刷新**。
>
> **状态**（按最近一次 push 计算）：🟢 90 天内 · 🟡 一年内 · 🔴 超过一年 · 🗄️ 已归档。
> 状态只是「近况」而非「好坏」——成熟稳定的工具可以一年不更新照样好用，🔴 的意思是**依赖前先确认一下**。
>
> **许可证**直接影响你能不能用：`none` = 仓库**没有许可证文件**，法律上默认保留所有权利；
> `CC-BY-NC*` **禁止商业使用**；`custom` = 自定义许可，请自行阅读。完整元数据见 [HEALTH.md](HEALTH.md)。

---

## 为什么需要这个清单

文献综述是研究中最耗时的环节之一：检索、去重、精读、主题归纳、引用核查……
近两年出现了大量能自动化其中某些（甚至全部）步骤的 AI 工具，但它们分散在 GitHub 各处、质量参差、命名混乱。

本清单的三个原则：

1. **按使用场景分类** —— 你带着「我要干什么」来，而不是从上百个仓库里大海捞针。
2. **只收强相关且可用的开源项目** —— 闭源工具单列一节做参考对照。
3. **信息真实** —— Star 数用 GitHub API 校对，链接持续用 CI 检查失效。

---

## ⚡ 30 秒选型

```
我用 Claude Code，想要「研究→论文」端到端 ─────────▶ academic-research-skills ⭐
我想让 AI 自动调研一个主题并产出带引用报告 ─────────▶ GPT Researcher / STORM
我想全自动「从想法到可投稿论文」 ───────────────────▶ AI-Scientist-v2 / AutoResearchClaw
我要对一堆 PDF 做「带引用」的问答 ───────────────────▶ PaperQA2
我在做严谨 PRISMA 系统综述（筛几千条摘要） ──────────▶ ASReview / prismAId
我要把 PDF 变成干净的 Markdown 喂给 LLM ────────────▶ MinerU / Docling / marker
我想把文献能力接进 Claude / Cursor（MCP） ──────────▶ paper-search-mcp / zotero-mcp
我想在 Zotero 里直接和文献库对话 ───────────────────▶ zotero-gpt / PapersGPT
```

---

<!-- BEGIN GENERATED:categories -->
## 🌟 综合研究智能体与技能

> 覆盖「研究 → 写作 → 评审 → 修订」全流程的端到端方案，多为 Claude Code / Codex 技能。

| 项目 | Stars | 状态 | 许可证 | 说明 |
|---|---|---|---|---|
| ⭐ [academic-research-skills](https://github.com/Imbad0202/academic-research-skills) | ~39.7k | 🟢 | CC-BY-NC-4.0 | **本领域最受欢迎的项目。** 一套 Claude Code 技能，10 阶段流水线（研究→写作→评审→修订→定稿），内置引用/论断「诚信门」，跨 Semantic Scholar + OpenAlex + Crossref 三源校验。理念：*「AI 是副驾，不是主驾」*。`/plugin install academic-research-skills` |
| [academic-research-skills-codex](https://github.com/Imbad0202/academic-research-skills-codex) | ~7.2k | 🟢 | CC-BY-NC-4.0 | 上者的 Codex 原生版，人在环中的学术研究流程 |
| [Research-Paper-Writing-Skills](https://github.com/Master-cai/Research-Paper-Writing-Skills) | ~5.5k | 🟢 | MIT | ML/CV/NLP 论文写作技能包（改编自彭思达老师笔记），兼容 Codex / Claude Code / Gemini |
| [claude-skills](https://github.com/alirezarezvani/claude-skills) | ~23.3k | 🟢 | MIT | 大型技能合集，内含 litreview / grants / deep-research 研究栈，跨 Claude Code / Codex / Gemini / Cursor |
| [academic-paper-skills](https://github.com/lishix520/academic-paper-skills) | ~1.1k | 🟡 | MIT | Strategist（规划）+ Composer（写作）双技能，带质量检查点 |
| [dr-claw](https://github.com/OpenLAIR/dr-claw) | ~1.0k | 🟢 | custom | 「科研 IDE」，内置多个 AI 助手角色 |
| [ScienceClaw](https://github.com/beita6969/ScienceClaw) | 870 | 🟢 | MIT | 自进化的 AI 科研伙伴，285 个技能，主打「零幻觉」 |
| [qinyan-academic-skills](https://github.com/LeonChaoX/qinyan-academic-skills) | 722 | 🟢 | MIT | 多语言的 182 个可安装 AI 智能体技能库，覆盖多学科 |
| [agent-research-skills](https://github.com/lingzhi227/agent-research-skills) | 238 | 🟡 | none | 面向系统性文献综述的 Claude Code 技能，含引用校验脚本 |
| [medsci-skills](https://github.com/Aperivue/medsci-skills) | 220 | 🟢 | MIT | 医学科研技能：检索、报告规范/引用核查、统计、出版图表、投稿（医生-研究者出品） |

---

## 🔎 深度研究与自动综述生成

> 输入一个主题，自动检索并产出带引用的综述 / 报告 / 相关工作章节。

| 项目 | Stars | 状态 | 许可证 | 说明 |
|---|---|---|---|---|
| ⭐ [STORM](https://github.com/stanford-oval/storm) | ~30.3k | 🟡 | MIT | 斯坦福 OVAL 出品，基于检索的「预写作 + 写作」两阶段，生成维基百科式长文并附引用；含多智能体对话式版本 Co-STORM |
| ⭐ [gpt-researcher](https://github.com/assafelovic/gpt-researcher) | ~28.7k | 🟢 | Apache-2.0 | 自主研究智能体，对任意主题做深度调研并生成带引用报告；通用型，非学术专用 |
| [deep-research](https://github.com/dzhng/deep-research) | ~19.4k | 🟡 | MIT | 极简的迭代式深度研究智能体（搜索 + 抓取 + LLM 精炼），代码短小易改 |
| [open_deep_research](https://github.com/langchain-ai/open_deep_research) | ~12.4k | 🟢 | MIT | LangChain 官方的开源深度研究参考实现 |
| [local-deep-research](https://github.com/LearningCircuit/local-deep-research) | ~8.8k | 🟢 | MIT | 本地/隐私优先的深度研究，10+ 数据源含 arXiv / PubMed，可全本地 LLM |
| [open-deep-research](https://github.com/nickscamara/open-deep-research) | ~6.3k | 🔴 | Apache-2.0 | 基于 Firecrawl 对网页数据推理的开源 deep-research 复刻 |
| [SurveyX](https://github.com/IAAR-Shanghai/SurveyX) | 986 | 🟡 | none | 从一个主题自动生成学术综述论文 |
| [LitLLM](https://github.com/LitLLM/LitLLM) | 44 | 🟢 | Apache-2.0 | 专注科学文献综述的工具包，用 RAG + 提示工程快速生成 related work（TMLR 2025） |
| [opendraft](https://github.com/federicodeponte/opendraft) | 338 | 🟢 | MIT | 免费开源的 AI 论文写作，19 个智能体协作起草长文 |
| [AutoSurveyGPT](https://github.com/a554b554/AutoSurveyGPT) | 156 | 🔴 | MIT | 用 GPT 从 Google Scholar 检索并排序论文，自动生成文献综述 |

---

## 🧪 自主科研：从想法到论文

> 端到端「全自动科学发现」——文献调研 + 提出假设 + 跑实验 + 写作 + 自评审。野心最大的一类。

| 项目 | Stars | 状态 | 许可证 | 说明 |
|---|---|---|---|---|
| ⭐ [AI-Scientist](https://github.com/SakanaAI/AI-Scientist) | ~14.3k | 🟡 | custom | Sakana AI，端到端全自动科学发现（文献→实验→写作→评审）；另有 [v2](https://github.com/SakanaAI/AI-Scientist-v2)（~6.9k，agentic 树搜索，达 workshop 级） |
| [AutoResearchClaw](https://github.com/aiming-lab/AutoResearchClaw) | ~13.9k | 🟢 | MIT | 自进化的自主科研：从想法到可投稿 LaTeX 论文（OpenAlex/S2/arXiv 真实文献 + 沙盒实验 + 多智能体评审） |
| [Agent-Laboratory](https://github.com/SamuelSchmidgall/AgentLaboratory) | ~5.8k | 🟡 | MIT | 端到端自主研究流程：文献综述 → 实验 → 报告写作 |
| [SciAgentsDiscovery](https://github.com/lamm-mit/SciAgentsDiscovery) | 627 | 🔴 | Apache-2.0 | 多智能体（本体学家/科学家/批评家）自动生成假设与科学发现 |
| [Zochi](https://github.com/IntologyAI/Zochi) | 311 | 🟡 | MIT | 「人工科学家」，从发现到被同行评审接收的端到端 |
| [DeepInnovator](https://github.com/HKUDS/DeepInnovator) | 279 | 🟡 | MIT | 自主生成研究想法、问题、可检验假设与实验设计 |

---

## 📚 文献问答与 RAG

> 针对一批 PDF / 论文语料做**带引用**的问答与信息抽取。

| 项目 | Stars | 状态 | 许可证 | 说明 |
|---|---|---|---|---|
| ⭐ [paper-qa](https://github.com/Future-House/paper-qa) | ~8.9k | 🟢 | Apache-2.0 | FutureHouse 出品，高精度科学文献 RAG，回答**必带引用**；PaperQA2 号称文献检索达到超人水平 |
| [paperai](https://github.com/neuml/paperai) | ~1.8k | 🟢 | Apache-2.0 | 面向医学与科研论文的语义检索 + 问答 |
| [openpaper](https://github.com/khoj-ai/openpaper) | 395 | 🟢 | AGPL-3.0 | 科研文库工作台：阅读/标注论文 + 带引用溯源的 AI 综述助手 |

---

## 🧮 系统综述与文献筛选

> 面向严谨的循证 / PRISMA 系统综述，帮你从上千条摘要中高效筛选。

| 项目 | Stars | 状态 | 许可证 | 说明 |
|---|---|---|---|---|
| ⭐ [ASReview](https://github.com/asreview/asreview) | 956 | 🟢 | Apache-2.0 | 主动学习的系统综述筛选工具，交互式排序论文、大幅缩短筛选时间；学术界成熟方案 |
| [LatteReview](https://github.com/PouriaRouzrokh/LatteReview) | 117 | 🟢 | CC-BY-NC-ND-4.0 | 低代码 Python 包，用 AI 智能体自动化系统综述筛选（OpenAI/Gemini/Claude/Ollama） |
| [prismAId](https://github.com/Open-and-Sustainable/prismAId) | 24 | 🟢 | AGPL-3.0 | 基于生成式 AI 的协议驱动系统综述工具，无需编程、可复现的筛选与抽取 |
| [prisma-review-tool](https://github.com/Black-Lights/prisma-review-tool) | 小众 | 🟡 | MIT | PRISMA 2020 全流程，经 MCP 做 AI 辅助筛选（arXiv/OpenAlex/S2，无需 API key） |

---

## 🔌 MCP 服务器

> 把文献能力接入 Claude / Cursor / Cline 等支持 Model Context Protocol 的客户端。

| 项目 | Stars | 状态 | 许可证 | 说明 |
|---|---|---|---|---|
| ⭐ [zotero-mcp](https://github.com/54yyyu/zotero-mcp) | ~4.4k | 🟢 | MIT | 把 Zotero 文献库（本地 + Web API）接给 AI：语义检索、PDF 全文、引用分析。最流行的 Zotero MCP |
| ⭐ [arxiv-mcp-server](https://github.com/blazickjp/arxiv-mcp-server) | ~3.0k | 🟢 | Apache-2.0 | 检索与分析 arXiv 论文，下载并把 PDF 转 Markdown 喂给 LLM；提供 `.mcpb` 包 |
| [paper-search-mcp](https://github.com/openags/paper-search-mcp) | ~2.3k | 🟢 | MIT | 跨 20+ 源检索/下载论文（arXiv、PubMed、bioRxiv、S2、OpenAlex、Crossref、CORE…） |
| [PubMed-MCP-Server](https://github.com/JackKuo666/PubMed-MCP-Server) | 122 | 🔴 | MIT | 检索、访问与分析 PubMed 文章（元数据 + 深度分析） |
| [alex-mcp](https://github.com/drAbreu/alex-mcp) | 50 | 🟡 | MIT | OpenAlex MCP，专注作者消歧与机构/成果查询 |
| [openalex-research-mcp](https://github.com/oksure/openalex-research-mcp) | 37 | 🟢 | MIT | OpenAlex（2.4 亿+ 成果）：引用分析、研究趋势、合作网络 |

---

## 🗂️ 文献管理与 Zotero / Obsidian 集成

> 在你已有的文献管理 / 笔记工作流里嵌入 AI。

| 项目 | Stars | 状态 | 许可证 | 说明 |
|---|---|---|---|---|
| ⭐ [zotero-gpt](https://github.com/MuiseDestiny/zotero-gpt) | ~7.3k | 🟢 | AGPL-3.0 | 把 GPT 集成进 Zotero，直接和你的文献库对话 |
| [papersgpt-for-zotero](https://github.com/papersgpt/papersgpt-for-zotero) | ~2.6k | 🟢 | AGPL-3.0 | Zotero AI + MCP 插件，跨 30+ LLM 聊天/批量处理 PDF |
| [ai-research-assistant](https://github.com/lifan0127/ai-research-assistant) | ~1.7k | 🔴 | AGPL-3.0 | Zotero 内的「Aria」LLM 研究助手 |
| [paper-note-filler](https://github.com/chauff/paper-note-filler) | 47 | 🟡 | none | Obsidian 插件，从 arXiv / ACL Anthology / Semantic Scholar 自动建笔记 |

---

## 📄 PDF → 结构化数据抽取

> 文献综述的隐形基础设施：把 PDF 变成干净、带结构的 Markdown / JSON 喂给 LLM。

| 项目 | Stars | 状态 | 许可证 | 说明 |
|---|---|---|---|---|
| ⭐ [MinerU](https://github.com/opendatalab/MinerU) | ~75.8k | 🟢 | Apache-2.0 | 高精度 PDF/Office → LLM 就绪的 Markdown/JSON（VLM+OCR，100+ 语言，公式/表格） |
| [docling](https://github.com/docling-project/docling) | ~63.8k | 🟢 | MIT | IBM 出品的文档解析器，为 GenAI/RAG 准备 PDF/文档 |
| [marker](https://github.com/datalab-to/marker) | ~37.9k | 🟢 | Apache-2.0 | 快速把 PDF/文档转成干净 Markdown/JSON，对科研文档友好 |
| [PDFMathTranslate](https://github.com/PDFMathTranslate/PDFMathTranslate) | ~35.8k | 🟢 | AGPL-3.0 | 保留排版的科研 PDF 翻译（公式/图表不变形） |
| [grobid](https://github.com/grobidOrg/grobid) | ~5.0k | 🟢 | Apache-2.0 | 从学术 PDF 抽取结构化 TEI/XML（元数据、参考文献、章节） |
| [paperetl](https://github.com/neuml/paperetl) | 697 | 🟡 | Apache-2.0 | 面向医学与科研论文的 ETL 管线，入库为结构化数据 |
| [scipdf_parser](https://github.com/titipata/scipdf_parser) | 455 | 🔴 | MIT | 科研 PDF 的 Python 解析器（正文 + 图，基于 GROBID） |

---

## 🕸️ 引文图谱与 API 客户端

> 做引文网络分析，或用代码直接调各大学术数据库。

| 项目 | Stars | 状态 | 许可证 | 说明 |
|---|---|---|---|---|
| [scholarly](https://github.com/scholarly-python-package/scholarly) | ~1.9k | 🟡 | Unlicense | Pythonic 的 Google Scholar 作者/论文检索 |
| [semanticscholar](https://github.com/danielnsilva/semanticscholar) | 476 | 🟢 | MIT | Semantic Scholar API 的非官方 Python 客户端 |
| [pyalex](https://github.com/J535D165/pyalex) | 400 | 🟢 | MIT | 轻量的 OpenAlex API Python 接口 |
| [ArxivDigest](https://github.com/AutoLLM/ArxivDigest) | 452 | 🔴 | MIT | 个性化每日 arXiv 摘要，GPT 打相关性分 + 邮件推送 |
| [citegraph](https://github.com/Citegraph/citegraph) | 22 | 🟡 | MIT | 500 万+ 论文/引用网络的开源可视化（CS 文献） |

---

## ✍️ 论文写作与同行评审助手

> 起草、润色，以及在投稿前做「AI 预审」。

| 项目 | Stars | 状态 | 许可证 | 说明 |
|---|---|---|---|---|
| [lmms-lab-writer](https://github.com/EvolvingLMMs-Lab/lmms-lab-writer) | 256 | 🟢 | MIT | 本地优先的 agentic LaTeX 写作，用于 AI 辅助学术写作 |
| [academic-writing-agents](https://github.com/andrehuang/academic-writing-agents) | 146 | 🟢 | MIT | Claude Code 插件：10+ 专家智能体协作做学术写作评审、调研、起草、润色 |
| [ai-peer-review](https://github.com/poldrack/ai-peer-review) | 151 | 🟢 | MIT | 多 LLM 元评审：独立评审 + 综合成 meta-review |
| [open_reviewer](https://github.com/maxidl/openreviewer) | 14 | 🔴 | none | 为 ML/AI 会议论文生成高质量同行评审，用于投稿前反馈 |
| [academic-research-plugin](https://github.com/JeanDiable/academic-research-plugin) | 18 | 🟡 | MIT | Claude Code 插件：文献综述、论文评审、引用管理，检索 arXiv/S2/DBLP 并识别研究空白 |

---

## 📖 精选清单（Awesome Lists）

> 想系统了解全貌，从这些社区维护的清单入手。

| 清单 | Stars | 状态 | 许可证 | 说明 |
|---|---|---|---|---|
| [Awesome-LLM-Scientific-Discovery](https://github.com/HKUST-KnowComp/Awesome-LLM-Scientific-Discovery) | 421 | 🟢 | MIT | EMNLP 2025 综述清单：LLM 用于科学发现 |
| [Awesome-Auto-Research-Tools](https://github.com/handsome-rich/Awesome-Auto-Research-Tools) | ~1.1k | 🟢 | CC0-1.0 | 自动化文献检索、论文阅读、实验管理与代码生成 |
| [awesome-ai-auto-research](https://github.com/worldbench/awesome-ai-auto-research) | 445 | 🟢 | MIT | AI 自动科研综述 |
| [LLM4SR](https://github.com/du-nlp-lab/LLM4SR) | 131 | 🔴 | MIT | LLM 用于科学研究综述的论文与资源合集 |
| [awesome-ai-research-tools](https://github.com/0x11c11e/awesome-ai-research-tools) | 54 | 🟢 | CC0-1.0 | 文献综述、文献管理、数据分析等 AI 科研工具 |
| [awesome-evidence-synthesis](https://github.com/evidencesynthesis-tools/awesome-evidence-synthesis) | 20 | 🟢 | CC0-1.0 | 系统综述、荟萃分析与证据合成的开源工具 |
<!-- END GENERATED:categories -->

---

## 🏢 商业 / 闭源工具（参考）

> 非开源，但在文献工作中广泛使用，列此便于对照。

- **[Elicit](https://elicit.com)** — 从数百万论文中抽取数据、生成证据表
- **[Consensus](https://consensus.app)** — 面向科研问题的语义搜索引擎
- **[Scite](https://scite.ai)** — 引用上下文分析（支持/反对/提及）
- **[Undermind](https://undermind.ai)** · **[SciSpace](https://typeset.io)** — 深度文献检索与阅读助手
- **[Research Rabbit](https://researchrabbit.ai)** · **[Connected Papers](https://connectedpapers.com)** — 引文关系可视化探索

---

## 🧭 如何选择（决策表）

| 你的需求 | 推荐 |
|---|---|
| 我用 Claude Code，想要「研究→论文」端到端流程 | **academic-research-skills**（领域第一，功能最全） |
| 我想要通用的「帮我调研这个主题」自主智能体 | **GPT Researcher** / **STORM** |
| 我想生成维基/综述式长文并附引用 | **STORM / Co-STORM** |
| 我想全自动「从想法到可投稿论文」 | **AI-Scientist-v2** / **AutoResearchClaw** |
| 我要对一堆 PDF 做带引用的问答 | **PaperQA / PaperQA2** |
| 我在做严谨的 PRISMA 系统综述（筛几千条摘要） | **ASReview** 或 **prismAId** |
| 我要把 PDF 变成干净 Markdown 喂给 LLM | **MinerU / Docling / marker** |
| 我想把文献能力接进自己的 AI 客户端（MCP） | **paper-search-mcp / zotero-mcp** |
| 我想在 Zotero 里直接和文献库对话 | **zotero-gpt / PapersGPT** |
| 我想在投稿前让 AI 预审论文 | **open_reviewer / ai-peer-review** |
| 我只是想浏览全貌 | 上面的 **Awesome 清单** |

---

## 📈 Star 趋势

> 领域里几个代表性项目的 Star 走势（自动更新）。

[![Star History Chart](https://api.star-history.com/svg?repos=Imbad0202/academic-research-skills,stanford-oval/storm,assafelovic/gpt-researcher,Future-House/paper-qa,SakanaAI/AI-Scientist&type=Date)](https://star-history.com/#Imbad0202/academic-research-skills&stanford-oval/storm&assafelovic/gpt-researcher&Future-House/paper-qa&SakanaAI/AI-Scientist&Date)

---

## 🤝 参与贡献

欢迎补充遗漏的优秀项目！请阅读 [CONTRIBUTING.md](CONTRIBUTING.md)：

1. Fork 本仓库 → 在对应分类新增一行
2. 保持格式一致：`[名称](链接) | Stars | 一句话说明`
3. **中英两份 README 都要更新**（`README.md` 与 `README.en.md`）
4. 只收录**可用、维护中、与文献综述强相关**的项目
5. 提交 PR，并在描述里说明推荐理由

> 也可以直接用 [Issue 模板](.github/ISSUE_TEMPLATE/add-a-tool.yml) 一键推荐一个工具。
>
> 想了解本项目接下来的建设计划（数据层 / 活跃度信号 / 可搜索站点 / 实战 recipes），见 [ROADMAP.md](ROADMAP.md)。

觉得有用的话，请点一个 ⭐ **Star**，让更多研究者发现它！

## 📄 许可证

[![CC0](https://licensebuttons.net/p/zero/1.0/88x31.png)](LICENSE)

本清单采用 [CC0-1.0](LICENSE)（公共领域贡献）。清单中各项目版权归其各自作者所有。
