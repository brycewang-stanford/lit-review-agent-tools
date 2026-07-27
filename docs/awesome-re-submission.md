# 提交到 awesome.re · Submission kit

[awesome.re](https://awesome.re)（即 `sindresorhus/awesome`）是所有 Awesome 清单的总目录。
本文件是**即用型提交包**：所有能提前做的都已经做完，剩下的只有等时间。

> **状态（2026-07-27）**：技术要求已全部满足。**唯一未满足的是 30 天龄期**。
> 仓库创建于 **2026-07-25**，官方要求「至少存在 30 天」，因此**最早可提交日期是 2026-08-24**。

---

## 逐条核对官方要求

来源：[pull_request_template.md](https://github.com/sindresorhus/awesome/blob/main/pull_request_template.md) 与 [create-list.md](https://github.com/sindresorhus/awesome/blob/main/create-list.md)。

| 要求 | 状态 |
|---|---|
| **清单已存在至少 30 天** | ⏳ **唯一阻塞项**。创建于 2026-07-25，最早可提交 **2026-08-24** |
| `npx awesome-lint` 对**仓库 README** 零报错 | ✅ README.md 现在就是合规 bullet 清单，CI 每次 push 都验 |
| 条目格式 `- [Title](URL#readme) - Description.` | ✅ 见下方文案 |
| 主标题 title case `# Awesome Name of List` | ✅ `# Awesome AI Literature Review` |
| `Contents` 章节（不叫 "Table of Contents"） | ✅ |
| Awesome badge 指向 awesome.re | ✅ |
| 默认分支 `main` | ✅ |
| GitHub topics 含 `awesome` 与 `awesome-list` | ✅ 共 15 个 topic |
| CC0 / 知识共享许可（非代码许可） | ✅ CC0-1.0 |
| `contributing.md`（**小写文件名**） | ✅ 已从 `CONTRIBUTING.md` 改名 |
| 仓库有清晰描述与 topics | ✅ |
| 不是「作者自己项目」的合集 | ✅ 收录的全是他人项目 |
| 仓库名 `awesome-*` 小写 slug | ⚠️ 现为 `lit-review-agent-tools`。**已决定暂不改名**——改名会让已发布的推广链接与 Pages 网址失效。GitHub 上存在不少已收录但不遵守此命名的清单，可以先试；若被要求改名，届时再改 |

## 为满足要求所做的结构调整（2026-07-27）

awesome.re 的条目指向 `URL#readme`，也就是说**他们的 lint 查的是仓库 README 本身**，
旁边放一份合规文件是没用的。因此：

| 文件 | 现在是什么 |
|---|---|
| `README.md` | **合规英文 bullet 清单**（awesome.re 看的就是它） |
| `README.zh.md` | 中文富表格版（原 `README.md`） |
| `README.en.md` | 英文富表格版 |
| ~~`AWESOME.md`~~ | 已删除，其内容成为 `README.md` |
| `CONTRIBUTING.md` → `contributing.md` | 小写，符合要求 |

三份文件全部由 `data/tools.yaml` 生成，不存在同步问题。

---

## 提交文案（直接复制）

**PR 标题**（注意：不带 "Awesome" 一词，动词大写）：

```
Add AI Literature Review
```

**要加进 `sindresorhus/awesome` 的 `readme.md` 的那一行**：

```markdown
- [AI Literature Review](https://github.com/brycewang-stanford/lit-review-agent-tools#readme) - Open-source agents and tools that search, screen, extract, and synthesize scholarly literature.
```

**放哪个区**：`## Miscellaneous`，紧邻已有的 `Scientific Writing` 条目附近；
提交前请对照该区当前的排列顺序插入。

> 描述写的是**主题本身**而不是「这个清单如何如何」，首字母大写、句号结尾、无营销词
> —— 这三点是他们明确要求的。

---

## 到日子之后的操作步骤

```bash
# 0. 先确认自己仓库仍然干净
npx awesome-lint README.md          # 必须零报错
make check                          # 生成物必须已提交

# 1. fork 并克隆主目录仓库
gh repo fork sindresorhus/awesome --clone --remote
cd awesome

# 2. 开分支
git checkout -b add-ai-literature-review

# 3. 手动把上面那一行插进 readme.md 的 Miscellaneous 区
#    （对照周围条目的顺序，不要破坏缩进）

# 4. 本地自检
npx awesome-lint          # 主目录仓库自己也要过 lint

# 5. 提交
git commit -am "Add AI Literature Review"
git push -u origin add-ai-literature-review
gh pr create --repo sindresorhus/awesome \
  --title "Add AI Literature Review" \
  --body-file ../lit-review-agent-tools/docs/awesome-re-pr-body.md
```

提交后请逐条勾选他们 PR 模板里的清单——维护者会严格按模板审。

---

## 为什么不是现在就提交

他们的规则原文是 **"Has been around for at least 30 days."**，从首次真实提交或开源之日算起。
本仓库距今 **2 天**。现在提交的唯一结果是被 close，而重复提交比等待更伤。

这段时间可以做的事：
1. 中文推广已发布，观察 Star 与 issue/PR 的自然增长。
2. 让每周的元数据刷新 workflow 正常跑几轮，积累真实的提交历史。
3. 补 1–2 条 `recipes/`（尤其是需要 LLM key 的那几个，我们跑不了）。
4. 到 **2026-08-24** 之后，按上面的步骤走。
