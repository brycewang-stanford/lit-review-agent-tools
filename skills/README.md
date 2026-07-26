# Claude Skill — `literature-review-tools`

This repo's curated catalog is also packaged as an installable **[Claude Agent Skill](https://docs.claude.com/en/docs/claude-code/skills)**.
Instead of browsing the README yourself, let Claude pick the right tool: ask *"what should I use to turn PDFs into Markdown for an LLM?"* or *"recommend a tool for a PRISMA systematic review"* and the skill routes you to the best open-source option with a one-line rationale.

```
skills/
└── literature-review-tools/
    ├── SKILL.md              # routing + 30-second picker + decision tables
    └── reference/
        └── catalog.md        # full 70+ tool catalog (progressive disclosure)
```

## Install

**Claude Code** (personal skills live in `~/.claude/skills/`):

```bash
git clone https://github.com/brycewang-stanford/lit-review-agent-tools
cp -r lit-review-agent-tools/skills/literature-review-tools ~/.claude/skills/
```

Restart Claude Code (or run `/doctor`) and the skill auto-loads. Claude invokes it
whenever your request matches literature-review tool selection — no manual trigger needed.

**Project-scoped:** copy the same folder into `.claude/skills/` inside any project.

**Other Agent-SDK / MCP hosts:** point your skills loader at
`skills/literature-review-tools/SKILL.md`.

## How it works

- **`SKILL.md`** carries the YAML frontmatter (`name`, `description`) Claude uses to
  decide *when* to activate, plus the lightweight routing logic (pickers + decision tables).
- **`reference/catalog.md`** holds the full catalog and is only read when Claude needs
  the complete list, exact star counts, or a category not summarized in `SKILL.md` —
  classic progressive disclosure so the base context stays small.

Star counts are periodic GitHub-API snapshots; the repo README is the live source of truth.
