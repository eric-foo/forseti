# Review Outputs

Store read-only reviewer findings reports and overlay-bound verdicts here.
Review outputs do not modify source authority by themselves.

Use typed child folders when the review belongs to a durable workstream:

- `adversarial-artifact-reviews/` for adversarial artifact and code review reports (the primary, most-populated folder).
- `method-validation/` for Core Spine method-validation reviews.
- `proof/` for proof-prep, proof-run, and proof-packet reviews.
- `prompts/`, `workflow/`, `misc/`: forward-looking conventions, created on first use (not all instantiated yet).

Note: a number of adversarial code/artifact reviews sit at the `docs/review-outputs/` root alongside the typed child folders. These are **retained in place by decision** (see `docs/hygiene/queue.md`, ORCA-HYGIENE-004): they are pinned by path — and in several cases by content hash — inside committed decision records, harness contracts, execution-authorization records, and an active handoff's verification command, so relocating them would rewrite provenance/verification ledgers in other lanes for a cosmetic gain. Both the root and `adversarial-artifact-reviews/` are valid locations; **new** reports should default to `adversarial-artifact-reviews/`.

Report filenames should use the reviewed artifact slug, review type, and
version, for example:

`method-validation/core_spine_v0_method_validation_case_frame_locks_adversarial_review_v0.md`

Chat closeouts should not carry the full review when a durable report is
written. Return the compact YAML review summary from
`.agents/workflow-overlay/communication-style.md`, including `report_path`,
`summary`, findings, and `next_action`.

Review reports are findings-first by default. Formal verdicts, blocked/ready
status, validation pass/fail claims, approval, readiness, mandatory
remediation, patch queues, and executor-ready handoffs require Forseti overlay or
prompt binding. Actionable findings should state the
`minimum_closure_condition` and `next_authorized_action`; `patch_queue_entry`
belongs only in a patch-queue review or separately authorized patch/integration
execution lane.
