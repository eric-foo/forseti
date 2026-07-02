# IG Behavioral Residual Burn-Down Adversarial Review v0

```yaml
retrieval_header_version: 1
artifact_role: Adversarial artifact review output
scope: >
  Read-only adversarial review of PR #474's two IG behavioral residual burn-down
  workflow docs, with source-backed verification of behavioral-completeness counts
  and Silver lineage claim discipline against the live F-lake.
use_when:
  - Adjudicating PR #474 before merge.
  - Checking whether the burn-down receipt over-trusts record membership vs source-backed lineage.
  - Checking whether remaining residuals and non-goals stayed visible after the missing-input pass.
authority_boundary: retrieval_only
open_next:
  - docs/workflows/ig_behavioral_missing_input_capture_receipt_v0.md
  - docs/workflows/ig_behavioral_residual_burndown_priority_v0.md
  - docs/prompts/reviews/ig_behavioral_residual_burndown_adversarial_review_prompt_v0.md
branch_or_commit: codex/ig-behavioral-residual-burndown @ 80ef4bbc47e78937277ddfea5e2531bac9a20514
input_hashes:
  docs/workflows/ig_behavioral_residual_burndown_priority_v0.md: 152A3F8C279DB0BF0AB3513F62707DB79217A93B995DE0C0F4821C3158DB9B55
  docs/workflows/ig_behavioral_missing_input_capture_receipt_v0.md: B4E8C2B24BCEDDFEA129622FF64C1BDD94586280898A482C3C9B20FE19B13E0C
stale_if:
  - Either review target hash differs from the input_hashes above.
  - A later F-lake inventory supersedes the receipt's final behavioral read.
  - The IG behavioral lake/projection, silver_lineage, deep-capture, or operator-extraction code changes materially.
```

## Commission, Target, Authority

- **Commission**: decide whether PR #474's docs accurately record what IG residuals were burned down and what remains, without converting a successful run into a broader safety/completeness/validation/readiness claim. Source: `docs/prompts/reviews/ig_behavioral_residual_burndown_adversarial_review_prompt_v0.md`.
- **Review targets** (read-only, no edits):
  - `docs/workflows/ig_behavioral_residual_burndown_priority_v0.md` (Workflow record)
  - `docs/workflows/ig_behavioral_missing_input_capture_receipt_v0.md` (Workflow receipt)
- **Authority**: Orca overlay binds the adversarial-artifact-review lane (`.agents/workflow-overlay/review-lanes.md`), report destination `docs/review-outputs/adversarial-artifact-reviews/`, severity labels `critical|major|minor` for finding priority only, and the `reviewed_by`/`authored_by` provenance contract. Findings are decision input, not approval, validation, readiness, or patch authority.
- **Fitness reference (intent-bearing target)**: the prompt's plain success signal — "a future reader can tell exactly what IG residuals were burned down, which claims depend on the live F-lake, which remaining gaps still block clean behavior, and which work was deliberately not done." Attacked as an alignment axis, not a pass bar.
- **Output mode**: `filesystem-output`; this durable report is the required write; chat returns the courier `review_summary` only.
- **Deep-thinking discipline**: `workflow-deep-thinking` reference-loaded and applied to frame failure modes before findings; `workflow-adversarial-artifact-review` applied to produce them.

## Hash / Revision Check

- Both target hashes recomputed (PowerShell `Get-FileHash -SHA256`) and **match** the prompt's retrieval header exactly → strict review authorized.
- Commit drift: prompt header says `@ 4602b7a5`; worktree HEAD is `80ef4bbc`. `git diff --stat 4602b7a5 80ef4bbc` shows the **only** change is the review-prompt file itself (`...adversarial_review_prompt_v0.md`, +124). This is the prompt's allowed "prompt-only later commit"; both review targets are byte-identical, so strict claims hold.

## Source-Read Ledger

| Source | Why read | Status |
| --- | --- | --- |
| `AGENTS.md`, `.agents/workflow-overlay/README.md` | Project authority / overlay binding | clean @ 80ef4bbc |
| `.agents/workflow-overlay/review-lanes.md`, `retrieval-metadata.md`, `source-loading.md`, `communication-style.md` | Lane binding, header contract, ledger rules, courier shape | clean @ 80ef4bbc |
| `docs/workflows/ig_behavioral_residual_burndown_priority_v0.md` | Review target | clean; hash verified |
| `docs/workflows/ig_behavioral_missing_input_capture_receipt_v0.md` | Review target | clean; hash verified |
| `orca-harness/source_capture/ig_reels_behavioral_projection.py` | How `status`/`residuals`/`complete` are computed | clean @ 80ef4bbc |
| `orca-harness/source_capture/ig_reels_behavioral_lake.py` | Read-side lineage gate + index function the receipt names | clean @ 80ef4bbc |
| `orca-harness/data_lake/silver_lineage.py` | `silver_record_source_backed_status` gate semantics | clean @ 80ef4bbc |
| `orca-harness/runners/run_ig_reels_operator_product_extract.py` | Operator import path, quote validation, `rejected_count` | clean @ 80ef4bbc |
| `orca-harness/runners/run_ig_reels_product_extract.py` | `pending_extraction_counts` (default model `codex-extraction-v0`) | clean @ 80ef4bbc |
| `orca-harness/runners/run_source_capture_ig_reels_deep_capture.py` | Capture route, transient media handle | clean @ 80ef4bbc |
| `orca/.../source_capture_playbook_v0.md` | Access posture for the receipt's Scope/Guard claim | clean @ 80ef4bbc |
| `docs/workflows/ig_canonical_f_deep_capture_product_extraction_receipt_v0.md` | Prior-state cross-check for `DaLBRQiMJhQ` | clean @ 80ef4bbc |
| **`F:\orca-data-lake`** | Live read-only verification (step 7) | **available**; read-only projection run; no writes, no network, no rebuild |
| `F:\...\DaLBRQiMJhQ\...\mentions_codex-operator-assisted-v0__c1cbd54661b97209.json` | Concrete lineage block for the load-bearing `DaLBRQiMJhQ` claim | read; source-backed |

**Live verification performed** (read-only, `rebuild_availability=False`, no writes): re-ran the receipt's named function `project_ig_reels_behavioral_index_from_lake` over `F:\orca-data-lake` from this branch's harness. Result reproduced the receipt's Final Behavioral Read **exactly**: `items=19`, `complete=12`, `complete_with_residuals=2`, `no_extraction_eligible_sources=5`, and identical `residual_prefixes` (`ig_grid_candidate_absent=4`, `ig_transcript_source_render_unavailable=2`, `ig_transcript_source_not_extraction_eligible=3`, `ig_comments_render_unavailable=1`, `ig_transcript_source_no_audio_handle=1`). `DaLBRQiMJhQ` resolves `complete=True`, `residuals=[]`, extracted via `mentions_codex-operator-assisted-v0__c1cbd54661b97209.json` with `source_backed_status=source_backed_complete`.

## Gate Results

- **Trigger gate**: explicit adversarial-artifact-review commission → in lane.
- **Lane collision**: targets are non-code workflow docs; harness code was read as source authority for claim verification, not reviewed for implementation correctness (that stays in the implementation-review lane). No undeclared collision.
- **Artifact-role preflight**: both targets are durable `docs/workflows/` artifacts in scope for the retrieval-metadata contract; read permission only; no paired-artifact rule blocks review.
- **Validation gate**: PR #474 CI `orca-harness-tests` = **pass** (fresh, 1m31s, run 28390635917). PR state = OPEN, **isDraft = true**, mergeStateStatus = CLEAN.
- **Output destination**: bound and present.

## Review Summary

```yaml
review_summary:
  status: completed
  report_path: docs/review-outputs/adversarial-artifact-reviews/ig_behavioral_residual_burndown_adversarial_review_v0.md
  recommendation: accept_with_friction
  reviewed_by: claude-opus-4.8
  authored_by: unrecorded
  summary: "Both docs accurately record the burn-down; final counts and the DaLBRQiMJhQ lineage claim verified exactly against the live F-lake; four minor evidence/clarity findings, no blocker."
  findings_count: 4
  blocking_findings: []
  advisory_findings:
    - F-01: Final Behavioral Read block fuses two functions under one name; reproduction recipe + default-model token undocumented
    - F-02: source-backed-completeness evidence leans on rejected_count=0 (mention-level) without naming the Silver-lineage read gate
    - F-03: residual_prefixes block silently omits no_speech, the reason for 3 of 5 no_extraction_eligible items
    - F-04: priority doc redirects stale counts but leaves its now-done Priority / Next-Allowed-Move actions unmarked
  prior_findings_remediated: []
  next_action: "Land the report alongside PR #474 (commit/push), then optionally apply the four minor doc clarifications; mark PR ready-for-review when intended."
```

## Findings (correctness before friction)

### F-01 — "Final Behavioral Read" provenance fuses functions and omits the reproduction recipe (minor, correctness)

- **Location**: `docs/workflows/ig_behavioral_missing_input_capture_receipt_v0.md:123-148`.
- **Source authority**: `orca-harness/source_capture/ig_reels_behavioral_lake.py:73` (the named function returns a `{shortcode: projection}` dict — it emits no `items=`/`statuses`/`residual_prefixes`/`pending_default_model` lines); `orca-harness/runners/run_ig_reels_product_extract.py:415-438,56` (`pending_extraction_counts`/`count_pending_extractions`, `DEFAULT_EXTRACTION_MODEL = "codex-extraction-v0"`).
- **Evidence**: the receipt presents the whole block as "Fresh read of `F:\orca-data-lake` through `project_ig_reels_behavioral_index_from_lake`." Verified: the `statuses`/`residual_prefixes`/`items=` lines are an author-side aggregation over that function's output (I reproduced them by aggregating its dict), and the `pending_default_model: 1` / `partials_default_model: 0` lines come from a **different** gate (`pending_extraction_counts`, default model `codex-extraction-v0`) that is not named. The model token that defines "default_model," and whether the read rebuilt the availability index, are not recorded.
- **Strongest defense / why it partially fails**: "through [function]" can be read loosely as "via that function plus aggregation," and the numbers are correct (reproduced exactly). It fails as *retrievability*: a future agent cannot reproduce the exact block from the one named function, and "pending_default_model" is uninterpretable without knowing it counts `codex-extraction-v0`-extractable transcripts.
- **Impact**: weak reproducibility of the headline counts; a re-runner could get a differently-shaped output and mistakenly read drift.
- **minimum_closure_condition**: the receipt states the exact reproduction recipe — both function names (index projection + `pending_extraction_counts`), the `codex-extraction-v0` default-model token behind `pending_default_model`, and that the aggregation/availability-rebuild is author-side.
- **next_authorized_action**: owner decision to accept as-is or commission a one-paragraph doc clarification (no code change).
- **Advisory remediation direction**: add a short "how this was read" line naming both runners and the model token; optionally paste the one-liner that produced the block.
- **Red-green proof**: `not_applicable` (non-executable doc-precision finding). **patch_queue_entry**: not authorized in this lane.

### F-02 — Source-backed-completeness evidence leans on `rejected_count=0`, never naming the Silver-lineage read gate (minor, correctness)

- **Location**: `docs/workflows/ig_behavioral_missing_input_capture_receipt_v0.md:98-121` ("The operator responses were conservative... Every import went through quote validation and returned `rejected_count=0`.").
- **Source authority**: `orca-harness/source_capture/ig_reels_behavioral_lake.py:255-259` (a `product_mentions` record only becomes `extracted` when the record set is complete **and** `silver_record_source_backed_status == source_backed_complete`); `orca-harness/data_lake/silver_lineage.py:323-351` (the gate requires `lineage_schema_version` + at least one `raw_ref`/`derived_ref`); `run_ig_reels_operator_product_extract.py:173,194-196` (`rejected_count` is `len(parse_mentions(...).rejected)` — mention-level quote grounding).
- **Evidence**: the receipt's stated evidence for the import quality is `rejected_count=0` and "imported as `[]` instead of forced mentions." That is mention-level quote validation. The thing that actually makes the 12 items *behaviorally complete* is the read-side Silver-lineage gate, which the receipt never names. (Verified real, not vacuous: `DaLBRQiMJhQ`'s record carries `derived_refs=[{lane: silver__capture__reel_transcript, record_id: deepcap_DaLBRQiMJhQ__3d0acddf37734160.json, sha256: 942040…, relation: consumed}]` → `source_backed_complete`.)
- **Strongest defense / why it partially fails**: the receipt cites `project_ig_reels_behavioral_index_from_lake` and lists the lake/projection files in `open_next`, so the gate is one hop away; the completeness claim is **true** and end-to-end verified — this is **not** the membership-over-lineage overclaim of axis 1. It fails only on *surfacing*: a hurried reader can take `rejected_count=0` as the completeness guarantee, when it is a different (mention-level) guarantee and is silent on recall/accuracy.
- **Impact**: a future reader could over-trust `rejected_count=0` as "extraction validated," conflating quote-grounding with source-backed lineage and with extraction quality.
- **minimum_closure_condition**: the receipt names the read-side gate (`silver_record_source_backed_status`) as what backs "complete," and states that `rejected_count=0` is quote-grounding only (not recall/validation).
- **next_authorized_action**: owner decision; optional one-line doc clarification.
- **Advisory remediation direction**: add "complete = record-set-complete + source-backed Silver lineage (raw/derived ref), gated on read" and keep `rejected_count=0` as conservatism evidence only.
- **Red-green proof**: `not_applicable`. **patch_queue_entry**: not authorized.

### F-03 — `residual_prefixes` block silently omits `no_speech`, which explains 3 of 5 no-eligible-source items (minor, correctness)

- **Location**: `docs/workflows/ig_behavioral_missing_input_capture_receipt_v0.md:138-144` (the structured `residual_prefixes`) vs `:150-160` (prose).
- **Source authority**: `orca-harness/source_capture/ig_reels_behavioral_projection.py:31-37,454-455` — `no_speech` is not in `SOURCE_POSTURE_PROBLEMS`/`SOURCE_NON_ELIGIBLE_PROBLEMS`, so a no-speech transcript source produces an ineligible source with **no residual token**. Live read confirms `DaK3uKxBlKy`, `DaKeXcVM0sx`, `DaKkwCiB_2B` resolve `no_extraction_eligible_sources` with `residuals=[]`.
- **Evidence**: the `residual_prefixes` block (which I reproduced exactly) therefore cannot show "no_speech," even though it is the dominant reason for 3 of the 5 `no_extraction_eligible_sources` items. The receipt's prose (`:155,158,159`) does enumerate them as "transcript posture no_speech," so the doc is internally complete — but the structured block read alone undercounts the reasons.
- **Strongest defense / why it partially fails**: axis 4 ("no-speech records distinguished") is satisfied in prose; nothing is hidden under aggregate success. It fails only if a downstream agent treats `residual_prefixes` as a standalone machine-readable gap inventory — then the no-speech reason is invisible. The root behavior is in the projection code, not the doc.
- **Impact**: a structured-only reader undercounts the no-speech gap; mild risk of misrouting the "next blocker" toward render/grid issues over no-speech.
- **minimum_closure_condition**: the receipt notes that the structured `residual_prefixes` block does not carry a `no_speech` token and must be read with the prose item list (or the projection emits a no-speech residual token — implementation-review scope, see below).
- **next_authorized_action**: owner decision; doc note now, and optionally route the projection-token question to the implementation-review lane.
- **Advisory remediation direction**: add a one-line caveat under the block; separately, the implementation-review lane may consider whether `_extraction_rollup` should emit an `ig_transcript_source_no_speech` residual for parity with `no_audio_handle`/`render_unavailable`. **This review does not assert that code change is required** — it is an implementation observation, not an artifact verdict.
- **Red-green proof**: `not_applicable` for the doc finding; the code observation, if taken up, should carry same-check red-green proof in that lane.

### F-04 — Priority doc redirects stale counts but leaves its now-completed Priority / Next-Allowed-Move actions unmarked (minor, correctness)

- **Location**: `docs/workflows/ig_behavioral_residual_burndown_priority_v0.md:28-30` (redirect), `:41-62` (Fresh Read, stale), `:74-102` (Priority list + Next Allowed Move).
- **Source authority**: the superseding receipt (`ig_behavioral_missing_input_capture_receipt_v0.md`) plus the live read — the "First: input coverage for grid-only items" priority is done (7 of 8 captured items now `complete`, 1 no-speech).
- **Evidence**: the Short Answer says "for current residual counts and the next blocker, use [the receipt], not the fresh-read counts below" — it redirects the **counts** only. The actionable "Priority" items 1–4 and "Next Allowed Move" remain in the body unqualified, and item 1's work is already executed per the receipt. `superseded_by` points to the receipt (good), but the in-body actions are not marked done.
- **Strongest defense / why it partially fails**: `superseded_by` + the post-run header largely protect a careful reader. It fails for a skimmer who jumps to the bold "Priority" section and acts on item 1 (already complete) or the "If live local capture is authorized: run a low-interaction deep-capture pass for the eight grid-only items" move (already run).
- **Impact**: low risk of duplicated/now-moot work if the body is read past the header.
- **minimum_closure_condition**: the Priority/Next-Allowed-Move sections are marked superseded/done (or the redirect explicitly covers actions, not just counts).
- **next_authorized_action**: owner decision; optional one-line "these priorities were executed — see receipt" stamp on the section.
- **Advisory remediation direction**: extend the existing post-run redirect to the action sections, or annotate items 1–4 with their done/remaining status.
- **Red-green proof**: `not_applicable`. **patch_queue_entry**: not authorized.

### Friction note (optional, non-blocking)

- The receipt's `open_next` carries 7 entries and largely duplicates the priority doc's `open_next` comparison list. Per `retrieval-metadata.md` bloat controls ("prefer `open_next` over long source lists when the next controlling source is enough"), this is slightly heavy but defensible as a deliberate comparison pack. Optional trim only; not a defect.

## Explicit Non-Findings (ruling out plausible material failures)

- **N-01 (axis 1, lineage discipline)**: completeness is **not** membership-based. `extracted`→`complete` requires `source_backed_complete` at read time (`ig_reels_behavioral_lake.py:255-259`, `silver_lineage.py:283-287,349-351`); reproducing 12 complete items therefore implies 12 source-backed records. Verified concretely on `DaLBRQiMJhQ`.
- **N-02 (axis 1, DaLBRQiMJhQ)**: the "already behavior-complete via an earlier source-backed `codex-operator-assisted-v0` record, so no duplicate `codex-extraction-v0` record was created" claim is **true and source-backed** — the record exists with a valid `derived_ref`; it was re-rendered to `transcribed` (record `…3d0acddf…`) after the canonical receipt's `render_unavailable` pass (record `…354900b9…`). Its appearance under `pending_default_model` is correct: pending for the default `codex-extraction-v0` token, complete via the operator token.
- **N-03 (axis 2, counts)**: final counts and residual prefixes reproduced **exactly** against the live lake (read-only). No fabricated or stale count detected in the receipt's Final Behavioral Read.
- **N-04 (axis 4, remaining items)**: all 7 non-complete items are enumerated in prose with reasons that match the live read — grid-absent (`DaA8n7EhqTR`), grid-absent + stale render-unavailable transcript (`DZ69knlsDb1`, `DaK3va8MYT_`), no_audio_handle (`DaKeK7vMoR0`), no_speech (`DaK3uKxBlKy`, `DaKeXcVM0sx`, `DaKkwCiB_2B`). Stale/duplicate failed source is flagged, not hidden.
- **N-05 (axis 6, scope)**: no scope expansion. Both docs carry explicit non-claims; the deep-capture runner uses a transient `TemporaryDirectory` media handle (never persisted) (`run_source_capture_ig_reels_deep_capture.py:11,260-267`); the operator path is subscription/manual JSON, no provider API (`run_ig_reels_operator_product_extract.py:1-7`). No shared-core, scheduler, media-preservation, historical-rewrite, or gold/Judgment surface touched.
- **N-06 (axis 7, green-as-readiness)**: neither doc treats parser/import green as validation/readiness/proof; both carry "Not validation of full IG lane readiness" and "Not proof that every public IG Reel yields…" non-claims. (The `rejected_count=0` nuance is F-02, not an overclaim.)
- **N-07 (axis 8-9, live-source risk & merge posture)**: receipt names public-page/transient-media/ASR posture, matching the playbook's owner-authorized pre-commercial public-content posture. The docs make **no** merge-readiness or CI-pass claim; CI `orca-harness-tests` passed fresh; PR #474 is currently a **draft** — a state the reviewer notes for the adjudicator, not a doc defect.
- **N-08 (axis 10, retrieval metadata)**: both targets carry contract-compliant headers (`retrieval_header_version: 1`, role, scope, `use_when`, `authority_boundary: retrieval_only`) and well-used triggered fields (`open_next`, `stale_if`, and `superseded_by` on the priority doc). No forbidden header field (no approval/validation/readiness/lifecycle state). Headers are adequate to route the next agent; the only retrieval weakness is reproducibility-of-counts (F-01), not a header field.

## Residual Risk

- The before-state in the priority doc Fresh Read (observed at `origin/main aa7b45d9`) is historical and **not independently reproducible now** (the lake has moved forward). The before→after delta's "before" leg rests on the receipt author's contemporaneous reading, cross-checked only against the priority doc (which agrees: complete=2). The "after" leg is fully verified.
- Live verification corroborates the receipt **as of this read**; the lake can change, which `stale_if` already covers.
- The harness code (projection/lake/runners/silver_lineage) was read as source authority for claim verification, **not** formally reviewed for implementation correctness; the `no_speech` no-residual-token behavior (F-03) is flagged as an implementation observation for that separate lane.
- Provenance: `reviewed_by: claude-opus-4.8` reflects the session runtime self-identification (observed, not fabricated); `authored_by: unrecorded` because the authoring model/version was not operator-supplied (the `codex/` branch prefix is an inference, deliberately not recorded as provenance).

## Review-Use Boundary

These findings are decision input for the PR #474 adjudicator, not mandatory instructions. Nothing here is approval, validation, readiness, source promotion, or executor-ready patch authority. All four findings are minor and non-blocking; the docs are accurate enough to merge as-is, and remediation becomes mandatory or executor-ready only if a separate patch, acceptance, or implementation lane binds it. This review edited no source file, ran no capture/extraction/import/network, and performed only read-only lake reads.

## Next Authorized Step

- **Land (batched, rote)**: commit and push this report on the lane; mark PR #474 ready-for-review and merge per the per-lane PR flow when the owner intends.
- **Material moves (optional, minor)**: (1) tighten the receipt's Final Behavioral Read provenance + reproduction recipe (F-01) — compounds because the receipt is the canonical IG behavioral inventory other lanes will re-read; main risk: none beyond a small doc edit. (2) Stamp the priority doc's executed priorities as superseded (F-04) — cheap guard against a skimmer re-running done work.
