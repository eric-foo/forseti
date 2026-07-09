# Quora B2B Post-Merge Capture Calibration v0

```yaml
retrieval_header_version: 1
artifact_role: Workflow record
scope: Post-merge Quora B2B capture calibration, candidate extraction summary, and enforcement-placement distillation after PR #816.
use_when:
  - Checking whether the PR #816 profile-backed CloakBrowser route produced real Quora B2B details after merge.
  - Reusing Quora B2B search candidates for answer-strategy planning.
  - Deciding whether similar capture failures belong in code, playbook, or doctrine.
authority_boundary: retrieval_only
open_next:
  - .agents/workflow-overlay/validation-gates.md
  - docs/review-outputs/quora_cloakbrowser_pr816_delegated_adversarial_code_review_patch_v0.md
branch_or_commit: 9039903b8176cc019d1e4447d2159d02079d3156
stale_if:
  - PR #816 capture runner behavior changes.
  - The local packet directory is deleted or replaced with a different packet ID.
```

## Status

`POST_MERGE_CAPTURE_SUCCEEDED`

This record covers one post-merge calibration run after PR #816 landed. It is a
workflow record, not buyer proof, source-quality proof, Quora policy guidance,
or broad scraping authorization.

## Isolation

- Worktree: `orca-worktrees/quora-cloakbrowser-patch`
- Branch: `codex/quora-postmerge-calibration`
- HEAD: `9039903b8176cc019d1e4447d2159d02079d3156`
- Reason: the warmed Quora profile is an ignored local browser profile rooted in
  this worktree. Running here avoids copying session data into a fresh worktree.

## Gate Ledger

| Gate | Result | Evidence |
| --- | --- | --- |
| PR #816 landed | Pass | GitHub PR #816 is merged; local merge commit `9039903b8176cc019d1e4447d2159d02079d3156` exists. |
| Profile label resolves | Pass | Preflight printed `browser_user_data_profile=present`, with `proxy_profile=absent`. |
| Live capture can launch | Pass after escalation | The sandboxed run failed before browser launch with Windows access denied; the escalated rerun succeeded. |
| Detail sufficiency | Pass | Receipt includes `source_detail_sufficiency_passed`; metadata records `access_blocked=false`. |
| Candidate extraction | Pass | Visible text preserves question-result rows with line references listed below. |

## Live Packet

- Local packet path: `_test_runs/source_capture_quora_b2b_search_postmerge_cloak_profile_sufficiency_20260710`
- Packet ID: `01KX3XAS9T04NG7GE9FCN546YK`
- Receipt generated at: `2026-07-09T17:03:15Z`
- Source locator: `https://www.quora.com/search?q=B2B%20questions`
- Final URL: `https://www.quora.com/search?q=B2B+questions`
- Visible mode changes:
  - `cloakbrowser_persistent_profile_postmerge_sufficiency_run`
  - `source_detail_sufficiency_passed`
  - `cloakbrowser_persistent_profile_loaded:client_provided_session:quora_client_provided_20260709`
- Metadata:
  - `access_blocked: false`
  - `persistent_profile_loaded: true`
  - `profile_persistence: local_ignored_profile`
  - `proxy_used: false`
  - `rendered_access_classification: no_block_marker`
  - `visible_text_byte_count: 12374`
  - `rendered_dom_byte_count: 706741`
  - `title: Search`
- Limitations in receipt: none
- Packet non-claims include: not raw cookie, storage-state, or profile path disclosure; not CAPTCHA solving; not session effectiveness proof.

## Candidate Extraction

These are extracted from the packet's preserved visible text. Candidate labels
below are concise paraphrases tied to packet line numbers; use the local packet
for exact wording when needed.

| Packet lines | Candidate surface | Answer-strategy value |
| --- | --- | --- |
| 30, 37 | B2B customer-discovery questions; answer snippet includes success measurement, money impact, and daily-workflow fit. | Strong seed for "questions to ask B2B customers" content. |
| 41 | B2B questions for productive feedback. | Demand signal, but no answer in visible packet. |
| 48, 55 | B2B salesperson interview evaluation and interview-question framing. | Sales-hiring angle; useful for a recruiting or sales-leadership answer. |
| 59, 66 | First B2B SaaS sales-hire questions; answer snippet includes product understanding and outbound cadence. | Strong seed for B2B SaaS sales-hiring content. |
| 71 | B2B SaaS NPS question variations. | Product/customer-success angle; no answer in visible packet. |
| 78, 85 | Validating a B2B idea by calling businesses when survey participation is low. | Strong seed for customer-discovery objections and validation workflow. |
| 89 | Instagram for B2B marketing. | Social-channel content angle; no answer in visible packet. |
| 96, 103 | Senior B2B SaaS sales interview questions. | Sales-leadership angle; answer snippet includes metrics, references, and B2B-vs-B2C judgment. |
| 106 | B2B direct-user Q&A product idea. | Product-opportunity signal; no answer in visible packet. |
| 113, 120 | Pricing a SaaS B2B offering. | Pricing/monetization angle; answer snippet ties price to productivity gain and value. |
| 124, 131 | CMO questions about sales and marketing alignment. | Strong seed for RevOps or CMO answer strategy. |
| 134 | Questions B2B buyers need answered. | Buyer-journey demand signal; no answer in visible packet. |
| 141, 148 | Questions to ask a managing director at a large B2B enterprise. | Executive-discovery angle; answer snippet suggests priorities, business outlook, leadership, and values. |
| 153, 160 | Questions to ask the interviewer for a B2B sales role. | Sales-career angle; answer snippet emphasizes compensation, commission, clawbacks, and payment mechanics. |
| 164, 171 | How B2B content marketing generates new business. | Strong seed for funnel-stage content strategy. |
| 174, 181 | Assessing B2B marketing maturity. | Strong seed for marketing-diagnostic content; answer snippet centers target market, sales channel, and why customers buy. |
| 185 | Startup-entrepreneur questions for B2B meetings with established entrepreneurs, including investor expectations. | Founder/advisory angle; no answer in visible packet. |
| 192, 199 | B2B SaaS brand-name evaluation. | Naming/positioning angle; answer snippet discusses memorability and B2B brand experience. |
| 203 | Common outside B2B sales-position questions. | Sales-career demand signal; no answer in visible packet. |
| 210 | Market-research question for validating a B2B marketplace idea. | Marketplace-validation demand signal; answer not visible in the extracted range. |

## Enforcement Placement

| Finding | Enforce By Code | Enforce By Playbook / Doctrine | Placement |
| --- | --- | --- | --- |
| Packet-write success is not content success. | Required. Runners must preserve packets but return nonzero when caller-supplied details fail sufficiency. | Also state in the capture playbook: "success means details, not 200." | Code primary, doctrine secondary. |
| Required details must be caller-bound per run. | Required. The runner flag surface must accept required visible/DOM details and fail closed. | Playbook must require the operator to name details before live runs. | Split: code enforces, doctrine selects. |
| Lower rungs may be worth probing, but Quora lower rungs failed here. | Not as a global forced ladder. Code should expose comparable rung outcomes and failure reasons. | Required. The capture playbook owns rung discipline and stop/pivot rules. | Doctrine primary, code evidence support. |
| Profile-backed capture must disclose session posture without exposing raw secrets. | Required. Label indirection, visible mode changes, non-claims, and no raw path/cookie disclosure belong in code. | Required for operator handling: do not paste raw cookies or profile paths into artifacts. | Code primary, doctrine handling. |
| Persistent profile plus proxy profile can create false provenance. | Required. Reject the combination at CLI/runner/adapter boundaries. | Doctrine can explain why, but should not be the only guard. | Code primary. |
| Worktree-local profile roots can block fresh-worktree reruns. | Optional future code if repeated: a safe root override or importless profile-root binding that never records raw paths in packets. | Required now: do not copy session directories by default; prefer the profile-holding worktree or an explicit owner-authorized profile setup. | Doctrine now; code only if repeated friction. |
| Quora has unusually strong bot-detection pressure for this target. | No global code rule from one source. | Record as a source-specific operational finding; do not generalize to every site. | Playbook note only. |
| Candidate extraction from failed packets creates fake progress. | Required where extraction is automated: extractor must require sufficiency-pass markers or explicit override. | Required when extraction is manual: do not extract from failed packets except as failure analysis. | Code if automated; doctrine for manual runs. |

## Residuals

- The raw packet remains a local `_test_runs/` artifact and is not promoted as a
  durable repository artifact by this record.
- This run proves only this specific profile-backed Quora search capture at the
  recorded time. It does not prove session durability, ongoing Quora access, or
  broad source reliability.
- Candidate rows are useful demand-signal inputs, not buyer proof or accepted
  answer strategy.
- No new code change is justified by this run alone. The only near-term code
  candidate is a safe profile-root override if repeated post-merge calibration
  needs to run from fresh worktrees without copying browser profile data.

## Validation Commands And Readbacks

- `git status --short --branch` in the worktree showed branch `codex/quora-postmerge-calibration` at the run point with only `_test_runs/` untracked before this record was added.
- `git rev-parse HEAD` returned `9039903b8176cc019d1e4447d2159d02079d3156`.
- Preflight command returned: `source capture CloakBrowser preflight passed; no network capture attempted; proxy_profile=absent; browser_user_data_profile=present; old_reddit_only=False; block_heavy_assets=False`.
- Live capture command returned the packet path above after escalated execution.
- Receipt and metadata readback produced the packet ID, `source_detail_sufficiency_passed`, `access_blocked=false`, and `visible_text_byte_count=12374`.
