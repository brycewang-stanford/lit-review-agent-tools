<div align="center">

# 贡献指南 · Contributing Guide

**简体中文** · [English](#english)

</div>

感谢你愿意让这份清单变得更好！🎉 本项目收录**用于文献综述（Literature Review）的开源 AI 智能体、Claude Code / Codex 技能、MCP 服务器、系统综述筛选工具与自动综述框架**。

## ✅ 收录标准

一个项目要被收录，应尽量满足：

1. **强相关** — 与「文献检索 / 阅读 / 综述 / 引用核查」直接相关，而非泛泛的 LLM/Agent 工具。
2. **可用且开源** — 有公开仓库、能实际跑起来（闭源商业工具只在「商业工具」一节做参考对照）。
3. **在维护** — 近一年内有提交，或社区认可度高、被广泛使用。
4. **信息真实** — 链接有效、描述准确、Star 数为近似值即可（写「~」前缀）。

> ❌ 不收录：纯营销页面、已归档且无替代价值的死项目、与文献综述无关的通用工具、付费墙后无法验证的项目。

## 📝 如何添加一个项目

1. Fork 本仓库。
2. 找到最合适的分类小节，在表格中**按相关性/Star 数大致排序**新增一行。
3. **中英两个 README 都要更新**（`README.md` 和 `README.en.md`），保持条目一致。
4. 保持格式统一：

   ```markdown
   | [项目名](https://github.com/owner/repo) | ~1.2k | 一句话说明它做什么、有什么独特之处 |
   ```

   - Star 数用近似值：`~39.4k`、`~900`、`~0.3k`；未知写 `—`。
   - 说明控制在**一句话**，突出「它解决什么问题 / 独特点」，避免复制官方 slogan。
   - 编辑推荐项目可在名称前加 `⭐`（请在 PR 里说明理由）。

5. 提交 PR，标题写 `Add: <项目名>`，正文简述**推荐理由**（你用过吗？它解决了什么？）。

## 🔧 本地检查（可选）

我们用 [awesome-lint](https://github.com/sindresorhus/awesome-lint) 和链接检查保证质量。CI 会自动跑，你也可以本地跑：

```bash
npx awesome-lint
```

## 🌐 关于双语

- 两份 README 是**一等公民**，内容需对齐。
- 若你只熟悉一种语言，先更新一份并在 PR 里注明，维护者会帮忙补另一份 —— 不要因此不提交。

## 🙌 其他贡献方式

- 修正失效链接、过时的 Star 数、错误描述。
- 提出更好的分类方式或「如何选择」决策建议。
- 补充某个工具的真实使用体验（放进说明里，非常有价值）。

---

<a name="english"></a>

# Contributing Guide (English)

[简体中文](#贡献指南--contributing-guide) · **English**

Thanks for helping make this list better! 🎉 This project curates **open-source AI agents, Claude Code / Codex skills, MCP servers, systematic-review screeners, and auto-survey frameworks for literature review**.

## ✅ Inclusion criteria

A project should ideally meet all of these:

1. **Clearly relevant** — directly about literature search / reading / synthesis / citation-checking, not a generic LLM/agent tool.
2. **Usable & open-source** — has a public repo you can actually run (closed/commercial tools appear only in the "Commercial" reference section).
3. **Maintained** — commits within the last year, or strong, widely-recognized adoption.
4. **Accurate info** — working link, honest description, approximate star counts are fine (prefix with `~`).

> ❌ Not included: pure marketing pages, dead & archived projects with no lasting value, generic tools unrelated to lit review, or paywalled projects that can't be verified.

## 📝 How to add a project

1. Fork the repo.
2. Find the most fitting category and add a row, **roughly ordered by relevance / stars**.
3. **Update both READMEs** (`README.md` and `README.en.md`) so entries stay in sync.
4. Keep the format consistent:

   ```markdown
   | [name](https://github.com/owner/repo) | ~1.2k | One line: what it does and what's unique about it |
   ```

   - Approximate stars: `~39.4k`, `~900`, `~0.3k`; use `—` if unknown.
   - Keep the note to **one line**, emphasizing "what problem it solves / what's unique" — don't just copy the official slogan.
   - Editor's picks may prefix the name with `⭐` (explain why in the PR).

5. Open a PR titled `Add: <project>`, and explain **why it belongs** (have you used it? what does it solve?).

## 🔧 Local checks (optional)

We use [awesome-lint](https://github.com/sindresorhus/awesome-lint) plus link checking. CI runs automatically; you can also run:

```bash
npx awesome-lint
```

## 🌐 On bilinguality

- Both READMEs are **first-class citizens** and must stay aligned.
- If you only know one language, update that one and note it in your PR — a maintainer will mirror it. Don't let this stop you from contributing.

## 🙌 Other ways to help

- Fix dead links, stale star counts, or inaccurate descriptions.
- Propose better categorization or "how to choose" guidance.
- Add real hands-on experience with a tool (put it in the note — hugely valuable).

By contributing, you agree that your contributions are released under [CC0-1.0](LICENSE) (public domain).
