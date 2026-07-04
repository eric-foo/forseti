# Forseti Prompt Templates

This folder stores Forseti-local prompt templates.

The authoritative registry is:

`C:\Users\vmon7\Desktop\projects\orca\.agents\workflow-overlay\template-registry.md`

Template files are subordinate to the registry. If a template path, status,
template target, or output mode differs from the registry, stop and resolve the
registry first.

Template targets are prompt-shaping labels only. They do not select, recommend,
rank, or route runtime model choice.

Structure:

- `shared/`: reusable Forseti behavior contracts and preflight defaults included by other templates.
- `research/`: evidence-only research and evidence-synthesis prompt templates.
- `review/`: read-only artifact review templates.
- `wrappers/`: thin-wrapper templates for launching existing prompt artifacts.
- `portable/`: self-contained method templates for repo-agnostic reviewers.

Note: model-target templates (`_generic/`) were retired 2026-06-13 (unused; owner decision).

Do not add implementation, runtime, package, test, scraping, or automation
templates while Forseti remains docs-first.
