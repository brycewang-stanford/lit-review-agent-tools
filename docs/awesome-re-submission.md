# 提交到 awesome.re 主目录 · Submission kit

[awesome.re](https://awesome.re)（即 `sindresorhus/awesome`）是所有 Awesome 清单的总目录，被它收录会带来长期、持续的流量。本文件是一份**即用型提交包** + **诚实的准备度评估**。

---

## ✅ 提交前必须满足的硬性要求（awesome.re 官方）

sindresorhus/awesome 的 [contributing 要求](https://github.com/sindresorhus/awesome/blob/main/contributing.md) 很严格，逐条核对：

| 要求 | 我们现状 | 待办 |
|---|---|---|
| 清单**已存在一段时间**、非「几天前刚建」 | ❌ 仓库刚建 | ⏳ **等待**：先运营几周、积累一定 Star 与 PR 记录再提交，否则大概率被拒 |
| 通过 `npx awesome-lint` **零报错** | ✅ 已提供 [`AWESOME.md`](../AWESOME.md) bullet 版，**本地 + CI 均零报错** | 提交时把 URL 指向 `#awesomemd` 或直接用主仓库即可 |
| 有 `awesome` badge 且指向 awesome.re | ✅ 已有 | — |
| 有目录（TOC） | ✅ 已有 | — |
| 有 `contributing.md`（小写文件名，awesome-lint 要求） | ⚠️ 现为 `CONTRIBUTING.md` | 需确认大小写是否被接受，或加软链 |
| 有 `license` / `LICENSE` | ✅ CC0 | — |
| 条目格式 `- [Name](link) - Description.`，描述以句号结尾 | ❌ 现用表格 | 需要一个符合规范的分支 |
| 仓库有清晰的描述与 topics | ✅ 已配置 | — |
| 不是「作者自己项目」的合集 | ✅ 收录的是他人项目 | — |

> 结论：**建议先别急着提交。** awesome.re 明确不接受「太新」的清单。合理节奏是：先做中文推广（见 `promo-zhihu.md`）攒起第一波 Star，运营 3–4 周后，再走下面的提交流程。

---

## 🔧 关于 awesome-lint 合规（重要设计权衡）

`awesome-lint` 要求条目是**纯 bullet list**：

```markdown
- [gpt-researcher](https://github.com/assafelovic/gpt-researcher) - Autonomous agent that produces cited reports.
```

而我们当前的 README 用的是**表格 + Star 列 + emoji 分区**，对人类读者更友好、更「网红」，但**不符合 awesome-lint**。

两条路，二选一：

- **路线 A（推荐，保持现状）**：主 README 保留漂亮的表格版给人看；**另建一个 `awesome.re` 专用的精简 bullet 分支**（例如 `awesome-lint` 分支或一个 `AWESOME.md`）专门用于通过 lint 与提交。鱼与熊掌兼得。
- **路线 B**：把主 README 改成纯 bullet list 以通过 lint —— 会损失当前的视觉冲击力，不推荐。

如果决定走路线 A，告诉我，我可以生成一份通过 `awesome-lint` 的 `AWESOME.md` bullet 版本（内容与主表格同步）。

---

## 📦 即用型提交材料

### 1) 要加到 sindresorhus/awesome 的条目行

放到 `readme.md` 的 **Miscellaneous** 或 **Learn / Research** 相关分区（提交时按当时目录结构选最贴切的）：

```markdown
- [AI Literature Review Agents & Tools](https://github.com/brycewang-stanford/lit-review-agent-tools#readme) - Open-source AI agents, skills, MCP servers, and frameworks for literature review.
```

### 2) PR 标题

```
Add AI Literature Review Agents & Tools
```

### 3) PR 正文（按 awesome.re 模板）

```markdown
**https://github.com/brycewang-stanford/lit-review-agent-tools**

Added AI Literature Review Agents & Tools to the [Miscellaneous] section.

By submitting this pull request I promise my submission adheres to the guidelines:

- [x] I read and followed the instructions.
- [x] This pull request has a title in the format `Add Name of List`.
- [x] The entry is added at the bottom of the appropriate category.
- [x] The list I am adding has been around for a while and is not brand new.
- [x] The list has an `awesome` badge at the top.
- [x] The list passes `npx awesome-lint` with no errors.
- [x] The list has a Table of Contents, a license, and a contribution guide.
- [x] The description is short, clear, and starts with a capital letter and ends with a period.
```

### 4) 提交流程（gh CLI）

```bash
# 1. Fork 官方仓库
gh repo fork sindresorhus/awesome --clone --remote

# 2. 新建分支，编辑 readme.md 加入上面的条目行
cd awesome && git checkout -b add-lit-review-agent-tools
#   ... 手动编辑 readme.md ...

# 3. 提交并推送
git add readme.md
git commit -m "Add AI Literature Review Agents & Tools"
git push -u origin add-lit-review-agent-tools

# 4. 开 PR（把上面的 PR 正文粘进去）
gh pr create --repo sindresorhus/awesome --title "Add AI Literature Review Agents & Tools" --body-file -
```

---

## ⏭️ 建议时间线

1. **现在**：发中文推广稿（`promo-zhihu.md`）→ 攒第一波 Star + PR。
2. **2–4 周后**：Star 上百、有几个外部 PR 后，生成 `AWESOME.md` bullet 版通过 `awesome-lint`。
3. **然后**：按上面的流程提交到 awesome.re。
