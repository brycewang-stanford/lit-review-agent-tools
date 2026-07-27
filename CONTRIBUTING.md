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

> ⚠️ **不要直接编辑 README.md / README.en.md / AWESOME.md 里的表格和列表。**
> 它们由 [`data/tools.yaml`](data/tools.yaml) 自动生成，手改会被 CI 拦下。

1. Fork 本仓库。
2. 在 [`data/tools.yaml`](data/tools.yaml) 对应分类下新增**一段条目**（同一分类内**按相关性/Star 数大致排序**）：

   ```yaml
   - name: "项目名"
     repo: owner/repo          # 只写 owner/repo，链接由脚本生成
     category: paper-qa-rag    # 见 data/categories.yaml
     added: 2026-07-27
     desc_zh: "一句话说明它做什么、有什么独特之处"
     desc_en: "One line: what it does and what's unique about it"
     desc_awesome: "Same idea, plain English, ending with a period."
   ```

   - `desc_zh` / `desc_en` 渲染进两个 README；`desc_awesome` 渲染进 `AWESOME.md`，
     需**首字母大写、以句号结尾**（awesome-lint 的硬性要求）。
   - 说明控制在**一句话**，突出「它解决什么问题 / 独特点」，避免复制官方 slogan。
   - 编辑推荐项目加 `editor_pick: true`（渲染成 ⭐，请在 PR 里说明理由）。
   - 没有 Star 数时写 `stars: null` 并补 `stars_label: {zh: "小众", en: "niche"}`。
   - **不用手填** `stars` / `pushed_at` / `archived` / `license` / `language` / `status`
     —— 这些由 `make refresh` 从 GitHub API 抓取。唯一例外：GitHub 识别不出的许可证
     （报 `NOASSERTION`），可以自己读 LICENSE 后手填，刷新脚本不会覆盖。

3. 运行 `make build` 重新生成所有文件，**把生成结果一起提交**。
4. 提交 PR，标题写 `Add: <项目名>`，正文简述**推荐理由**（你用过吗？它解决了什么？）。

## 🔧 本地检查

```bash
make validate   # 检查 data/ 里的字段、重复项、分类是否合法
make build      # 重新生成 README.md / README.en.md / AWESOME.md / data/tools.json
make check      # CI 跑的这条：生成结果如果没提交就报错
make refresh    # 从 GitHub API 刷新 Star / 活跃度 / 许可证，然后重新生成
make lint       # awesome-lint（需要 Node）
```

只需要 Python 3 和 `pyyaml`（`pip install pyyaml`）。

## 🌐 关于双语

- 中英文说明都存在同一条目里（`desc_zh` / `desc_en`），**结构上不可能再走偏**。
- 若你只熟悉一种语言，先填一份并在 PR 里注明，维护者会帮忙补另一份 —— 不要因此不提交。

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

> ⚠️ **Don't hand-edit the tables or lists in README.md / README.en.md / AWESOME.md.**
> They're generated from [`data/tools.yaml`](data/tools.yaml), and CI rejects manual edits.

1. Fork the repo.
2. Add **one entry** to [`data/tools.yaml`](data/tools.yaml) under the right category
   (**roughly ordered by relevance / stars** within it):

   ```yaml
   - name: "project-name"
     repo: owner/repo          # owner/repo only — the URL is generated
     category: paper-qa-rag    # see data/categories.yaml
     added: 2026-07-27
     desc_zh: "一句话说明它做什么、有什么独特之处"
     desc_en: "One line: what it does and what's unique about it"
     desc_awesome: "Same idea, plain English, ending with a period."
   ```

   - `desc_zh` / `desc_en` render into the two READMEs; `desc_awesome` renders into
     `AWESOME.md` and **must start with a capital and end with a period** (awesome-lint).
   - Keep it to **one line**, emphasizing "what problem it solves / what's unique" —
     don't just copy the official slogan.
   - Editor's picks set `editor_pick: true` (renders as ⭐; explain why in the PR).
   - No star count? Use `stars: null` plus `stars_label: {zh: "小众", en: "niche"}`.
   - **Don't hand-write** `stars` / `pushed_at` / `archived` / `license` / `language` /
     `status` — `make refresh` pulls those from the GitHub API. One exception: a license
     GitHub can't detect (it reports `NOASSERTION`) may be filled in by hand after reading
     the repo's LICENSE, and the refresher will not overwrite it.

3. Run `make build` to regenerate every surface, and **commit the generated output too**.
4. Open a PR titled `Add: <project>`, and explain **why it belongs** (have you used it? what does it solve?).

## 🔧 Local checks

```bash
make validate   # field, duplicate, and category checks over data/
make build      # regenerate README.md / README.en.md / AWESOME.md / data/tools.json
make check      # what CI runs: fails if generated output isn't committed
make refresh    # pull stars / freshness / licenses from the GitHub API, then rebuild
make lint       # awesome-lint (needs Node)
```

Only Python 3 and `pyyaml` are required (`pip install pyyaml`).

## 🌐 On bilinguality

- Both languages live in the same entry (`desc_zh` / `desc_en`), so they **can no longer drift**.
- If you only know one language, fill in that one and note it in your PR — a maintainer will mirror it. Don't let this stop you from contributing.

## 🙌 Other ways to help

- Fix dead links, stale star counts, or inaccurate descriptions.
- Propose better categorization or "how to choose" guidance.
- Add real hands-on experience with a tool (put it in the note — hugely valuable).

By contributing, you agree that your contributions are released under [CC0-1.0](LICENSE) (public domain).
