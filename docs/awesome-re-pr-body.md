<!-- Body for the sindresorhus/awesome PR. Their template is a checklist —
     paste this, then tick their boxes. -->

**https://github.com/brycewang-stanford/lit-review-agent-tools**

A curated list of open-source AI agents, skills, MCP servers and frameworks for
literature review — covering search, screening, extraction, reading, synthesis,
citation checking, writing and review.

What is different about it:

- Every entry carries a **maintenance status and licence**, refreshed weekly from
  the GitHub API. Four listed projects ship no licence file at all and three
  forbid commercial use; the list says so rather than leaving you to find out.
- The list is generated from a single YAML source, and CI rejects any hand-edit
  that would let the rendered files drift.
- It ships **workflows that were actually executed**, not described — including a
  three-way benchmark of the PDF extractors and a measured screening run.
- The catalogue is published as a reusable JSON dataset.

Requirements:

- `npx awesome-lint` passes on the readme, and runs on every push in CI.
- Licence: CC0-1.0. Contribution guidelines in `contributing.md`.
- Topics include `awesome` and `awesome-list`. Default branch is `main`.
