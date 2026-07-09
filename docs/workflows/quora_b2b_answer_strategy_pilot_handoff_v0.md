# Quora B2B Answer-Strategy Pilot Handoff v0

```yaml
retrieval_header_version: 1
artifact_role: Workflow handoff packet (answer-strategy pilot; not capture authorization)
scope: >
  Cold handoff for the next Quora B2B answer-strategy pilot after PR #825 landed
  and the capture playbook/recon index absorbed the bounded Quora capture lesson.
  The handoff preserves which captured Quora candidates are admissible, what the
  capture proves, and what the next lane must not overclaim.
use_when:
  - Continuing from Quora B2B capture calibration into answer-strategy drafting.
  - Re-verifying which captured Quora candidates may be used as demand-signal inputs.
  - Preventing a future lane from treating packet/HTTP/render success as content success.
authority_boundary: retrieval_only
open_next:
  - docs/workflows/quora_b2b_postmerge_capture_calibration_v0.md
  - docs/review-outputs/adversarial-artifact-reviews/quora_b2b_postmerge_capture_calibration_delegated_adversarial_review_patch_v0.md
  - forseti/product/spines/capture/core/source_capture_toolbox/source_capture_playbook_v0.md
  - forseti/product/spines/capture/core/source_capture_toolbox/capture_recon_index_v0.md
stale_if:
  - PR #825's calibration record is superseded or corrected.
  - The Quora packet is re-run and produces a different candidate set.
  - The capture playbook changes the caller-bound detail-sufficiency rule.
```

## Disposition (2026-07-10) — Active Objective executed once and DEFERRED by owner

Read this before acting on the packet. It supersedes the Active Objective and
Exact Next Authorized Action below for sequencing purposes; the packet's
capture facts, evidence boundary, candidate ledger, and drift guard remain
valid.

- The answer-strategy pilot named below **was executed once** on lane
  `claude/quora-b2b-answer-strategy-0439af` (2026-07-10): the load contract was
  completed (calibration record and delegated review re-read and hash-matched),
  the three recommended-default units were drafted and validated, and the owner
  then **dropped the draft before push** (recoverable on that lane's local
  history at `f2a8a84b`; never on `main`).
- Owner decision (user-stated): drafting real Quora answers is deferred until a
  proper **answering methodology ("answering meta")** exists — context
  requirements, non-generic depth-of-value bar, tone, and per-question approach.
  Generic answer drafts from the paraphrase table are not worth producing.
- What stands unchanged: the capture proof (PR #825 calibration + PR #829
  playbook lesson) and the admissible candidate table. Those needed no further
  work and this disposition does not weaken them.
- Re-entry condition: do **not** re-execute the answer-strategy pilot from this
  packet until (1) a channel goal for Quora answer content is owner-decided
  (which buyer it serves and what job the content does), and (2) the answering
  meta exists. The commissioning prompt for that methodology work is
  `docs/prompts/handoffs/quora_b2b_answering_meta_design_commission_prompt_v0.md`;
  open it instead of this packet's Active Objective.

## Load Contract

- packet_version: 1
- mode: max
- created_at: 2026-07-10
- created_by_lane: Codex GPT-5 in `codex/quora-playbook-handoff` (sender provenance only, not authority)
- workspace: `C:\Users\vmon7\Desktop\projects\orca\orca-worktrees\quora-playbook-handoff`
- handoff_path: `docs/workflows/quora_b2b_answer_strategy_pilot_handoff_v0.md`
- expected_branch_at_write: `codex/quora-playbook-handoff`
- expected_head_at_lane_start: `1a1f3007cd55a6caa2b87c7bc25d6c2344b0d9f7` (`origin/main` after PR #825 merge)
- expected_dirty_state_at_write: modified capture playbook, modified recon index, and this new handoff file; after this lane lands, re-read from current `main` and use the hashes below as compare targets, not as a substitute for reading.
- load_rule: confirm-don't-trust. Re-open the named sources before any strict or actionable claim; packet claims are restore pointers, not authority.

## Goal Handoff

- long_term_goal: use source-captured B2B question surfaces to produce answer-strategy content that is useful for Orca's B2B wedge without pretending a Quora capture is buyer proof.
- anchor_goal: draft a small answer-strategy pilot from two or three admissible Quora B2B candidates in the merged calibration record.
- success_signal: the pilot names selected candidates, preserves the evidence boundary, gives a concrete answer angle for each, and drafts or outlines answer content without using failed packets, invented exact wording, or buyer-proof claims.

## Open Decision / Fork

- decision: which candidate cluster should the answer-strategy pilot start with?
- recommended default: start with three high-signal business-operator angles that have visible answer snippets in the merged record:
  1. B2B customer-discovery questions (`packet lines 30, 37`).
  2. First B2B SaaS sales-hire questions (`packet lines 59, 66`).
  3. Pricing a SaaS B2B offering (`packet lines 113, 120`).
- alternate third seed if the owner wants marketplace/product-validation content: market-research question for validating a B2B marketplace idea (`packet lines 210, 215`).
- tradeoff: sales-hire/pricing/customer-discovery makes the first pilot more founder-operator focused; marketplace validation makes it more product-market-discovery focused. Both are admissible; do not widen beyond a small pilot unless the owner asks.
- owner of final content angle: human owner / Chief Architect.

## Drift Guard

- Do not run live Quora capture or scrape again from this handoff. The next action is answer-strategy planning from the merged record unless separately authorized.
- Do not claim Quora access is generally reliable. The capture lesson is one bounded CloakBrowser persistent-profile Quora B2B search success, with local ignored profile, no proxy, and caller-bound detail sufficiency.
- Do not claim buyer proof, market proof, source-quality proof, Quora policy guidance, or session durability.
- Do not extract candidates from failed packets except as failure analysis. Candidate extraction for answer strategy must come from the sufficiency-passed PR #825 calibration packet summarized in `docs/workflows/quora_b2b_postmerge_capture_calibration_v0.md`.
- Candidate labels in the calibration record are concise paraphrases tied to packet line numbers. If exact wording matters, re-open the local packet named by the calibration record; do not invent exact Quora wording from the paraphrases.
- Preserve the distinction between answer strategy and source capture. The pilot can draft angles and answer outlines; it is not a new source-capture run, code patch, or product-readiness claim.

## Inherited Context

### Source-loading state to re-establish

- Project entry: read `AGENTS.md` and `.agents/workflow-overlay/README.md` before project work.
- Capture-method authority for this lane: `forseti/product/spines/capture/core/source_capture_toolbox/source_capture_playbook_v0.md` plus `capture_recon_index_v0.md`.
- Calibration authority for admissible Quora candidates: `docs/workflows/quora_b2b_postmerge_capture_calibration_v0.md`.
- Review hardening authority: `docs/review-outputs/adversarial-artifact-reviews/quora_b2b_postmerge_capture_calibration_delegated_adversarial_review_patch_v0.md`.

### Earlier-decided facts to preserve

- PR #825 landed a post-merge Quora B2B capture calibration record.
- The live packet was `_test_runs/source_capture_quora_b2b_search_postmerge_cloak_profile_sufficiency_20260710` with packet ID `01KX3XAS9T04NG7GE9FCN546YK`.
- The packet recorded `source_detail_sufficiency_passed`, `access_blocked=false`, `persistent_profile_loaded=true`, `proxy_used=false`, `visible_text_byte_count=12374`, and `rendered_dom_byte_count=706741`.
- The mechanical sufficiency bar was caller-bound: command success required target Quora B2B result details and stable question-title markers visible in captured artifacts.
- The delegated adversarial review corrected the record so line `210, 215` is recognized as having a visible answer snippet, and so the bot-detection-pressure claim is tied to a separate lower-rung Cloudflare-blocked probe rather than the successful run itself.

## Active Objective

Produce the first Quora B2B answer-strategy pilot from the merged calibration record. The pilot should be a small strategy/content artifact, not a capture run and not a code change.

## Exact Next Authorized Action

1. Re-open the calibration record and delegated review report.
2. Pick two or three candidates from the recommended default set, or swap in the marketplace-validation seed if the owner prefers product-validation content.
3. For each selected candidate, write an answer-strategy unit with: source row, evidence boundary, likely searcher intent, recommended answer angle, key claims that are safe to make, claims to avoid, and a short draft/outline.
4. Stop before live capture, code edits, broad Quora route claims, or buyer-proof language unless the current user explicitly redirects.

## Authority And Source Ledger

- `forseti/product/spines/capture/core/source_capture_toolbox/source_capture_playbook_v0.md` — Role: capture method doctrine and newly installed success-means-details rule. Load-bearing: yes. SHA256 at handoff write: `1E39D351156754FF46E2AE7355AC778585B1A83D89C200E8C4BC2281DB3998C0`.
- `forseti/product/spines/capture/core/source_capture_toolbox/capture_recon_index_v0.md` — Role: recon-index row for the bounded Quora PR #825 calibration. Load-bearing: yes. SHA256 at handoff write: `441F3C40474A8EE5F8D00324BA609ECF93C2C51E9E385EACE5F3E66E21BED3C9`.
- `docs/workflows/quora_b2b_postmerge_capture_calibration_v0.md` — Role: merged calibration record and candidate table. Load-bearing: yes. SHA256 at handoff write: `80399574C4FED31B3D0732509FC580605171CE5C314787BA318DFBA393CD5B6F`.
- `docs/review-outputs/adversarial-artifact-reviews/quora_b2b_postmerge_capture_calibration_delegated_adversarial_review_patch_v0.md` — Role: de-correlated review findings and corrected evidence interpretation. Load-bearing: yes. SHA256 at handoff write: `C28566AA33EDE06B1DFDBA684D9EBF7EB25E4E5BEC3B9020FF4130A920A9A13E`.

## Candidate Seeds From The Calibration Record

Use the calibration record for the full table. Highest-value pilot candidates:

| Packet lines | Candidate surface | Use in pilot |
| --- | --- | --- |
| 30, 37 | B2B customer-discovery questions; snippet includes success measurement, money impact, and daily-workflow fit. | Founder/operator discovery answer. |
| 59, 66 | First B2B SaaS sales-hire questions; snippet includes product understanding and outbound cadence. | Founder sales-hiring answer. |
| 113, 120 | Pricing a SaaS B2B offering; snippet ties price to productivity gain and value. | Monetization/pricing answer. |
| 210, 215 | Market-research question for validating a B2B marketplace idea; snippet recommends feedback from existing customers, including negative experiences. | Product/marketplace validation answer. |

Secondary candidates worth later use: CMO sales/marketing alignment (`124, 131`), B2B marketing maturity (`174, 181`), and B2B content marketing new-business generation (`164, 171`).

## Optional Code Improvement Boundary

The optional code improvement discussed after the PR #825 calibration is not part of this answer-strategy handoff. If it becomes necessary later, the smallest coherent code change is to persist the exact caller-bound sufficiency requirements as a structured manifest/receipt field, so review does not have to infer them from mode tags and `capture_context`. Do not broaden that into runner redesign, profile-root management, or Quora-specific logic without a new authorization.

## Validation / Restore Notes

- This handoff is docs-only and non-authorizing.
- Expected local validation for this lane: `git diff --check`, retrieval-header check for changed durable docs, placement check if available, and a fresh read of touched sections.
- If the receiver needs exact Quora text, inspect the local packet named in the calibration record. Do not use the paraphrase table as exact quotation.

## Confirm-Don't-Trust Load Checklist

- Re-verify current branch and HEAD; this handoff was written on a short-lived docs branch and main moves quickly.
- Re-read the four ledger sources above before strict or actionable claims.
- Confirm that the candidate rows still match the calibration record.
- Confirm that any future code work has fresh explicit authorization; this packet authorizes answer-strategy planning only.

## Do Not Forget

- Success means details, not packet existence.
- The Quora finding is useful but narrow.
- Candidate rows are demand-signal inputs, not buyer proof.
- The next best move is a small answer-strategy pilot, not another capture ladder probe.
