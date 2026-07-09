# Core Spine v0 Method Validation Cutoff Source-Visibility Verification Report

```yaml
retrieval_header_version: 1
artifact_role: Review report
scope: Cutoff timing and broad public source-family visibility verification for the five locked Core Spine v0 method-validation cases.
use_when:
  - Deciding whether the Core Spine v0 method-validation replay prompt can be prepared.
  - Checking which locked cases need cutoff or source-family timing patches before replay prompting.
authority_boundary: retrieval_only
open_next:
  - forseti/product/case_families/product_learning/other_verticals/core_spine_v0_method_validation_case_locks_v0.md
  - forseti/product/case_families/product_learning/other_verticals/core_spine_v0_method_validation_case_frame_lock_contract_v0.md
  - forseti/product/case_families/product_learning/other_verticals/core_spine_v0_method_validation_case_frame_locks_v0.md
input_hashes:
  docs/prompts/product-planning/core_spine_v0_method_validation_cutoff_source_visibility_verification_prompt_v0.md: A51534E692BB2E3C9543241212B5E194F83EB9DB568180F68AE40A0E50C69A6D
  docs/product/core_spine_v0_method_validation_case_locks_v0.md: 5782C9E809269A783B73E29E733CFFF9D9C4BC9E0F95F2C365886CCD387FC4E5
  docs/product/core_spine_v0_method_validation_case_frame_lock_contract_v0.md: F5633E834BE599C1C5ACFDBB9A65DC281F7AF72F18CC19E48A51FE57C4EFC1F0
  docs/product/core_spine_v0_method_validation_case_frame_locks_v0.md: 4C8CFE49D8BB2FDDE650C99FEBB7BFE5F0CF76125057BD1B992431027D541785
  docs/review-outputs/method-validation/core_spine_v0_method_validation_case_frame_locks_adversarial_review_v0.md: 749DDCB3FFCBBA81A0F2253A3F1BD76948793B451DA528B67B998BDAF982195A
branch_or_commit: main @ 3bf5c45cfa6879ae65c8f822eff9c185dcba8b3c
downstream_consumers:
  - future Core Spine v0 method-validation replay prompt
stale_if: Any locked case identity changes, case-frame locks change, evidence replay is authorized before this report is consumed, or a later accepted cutoff/source-family verification supersedes this report.
```

## 1. Repository State Checked

`git status --short --branch`:

```text
## main...origin/main [ahead 11]
 M .agents/workflow-overlay/README.md
 M .agents/workflow-overlay/artifact-folders.md
 M .agents/workflow-overlay/artifact-roles.md
 M .agents/workflow-overlay/communication-style.md
 M .agents/workflow-overlay/prompt-orchestration.md
 M .agents/workflow-overlay/review-lanes.md
 M .agents/workflow-overlay/source-of-truth.md
 M .agents/workflow-overlay/validation-gates.md
 M docs/STRUCTURE.md
 M docs/prompts/README.md
 M docs/prompts/reviews/core_spine_v0_proof_packet_preparation_adversarial_review_gpt55_prompt_v0.md
 M docs/review-outputs/README.md
?? .agents/workflow-overlay/retrieval-metadata.md
?? docs/product/core_spine_v0_method_validation_case_frame_lock_contract_v0.md
?? docs/product/core_spine_v0_method_validation_case_frame_locks_v0.md
?? docs/product/core_spine_v0_method_validation_case_locks_v0.md
?? docs/product/core_spine_v0_method_validation_mv01_intercom_zendesk_replay_v0.md
?? docs/product/core_spine_v0_method_validation_mv03_stack_overflow_chatgpt_replay_v0.md
?? docs/product/core_spine_v0_method_validation_mv04_unity_runtime_fee_replay_v0.md
?? docs/product/core_spine_v0_method_validation_mv05_reddit_api_pricing_replay_v0.md
?? docs/product/core_spine_v0_method_validation_mv09_thomson_reuters_casetext_replay_v0.md
?? docs/product/core_spine_v0_method_validation_replay_packet_v0.md
?? docs/product/core_spine_v0_method_validation_rubric_v0.md
?? docs/prompts/deep-thinking/
?? docs/prompts/hygiene-queue/
?? docs/prompts/product-planning/
?? docs/prompts/reruns/
?? docs/prompts/reviews/core_spine_v0_method_validation_case_frame_locks_adversarial_review_gpt54_prompt_v0.md
?? docs/prompts/wrappers/
?? docs/review-outputs/method-validation/
?? docs/review-outputs/proof/
```

`git log --oneline -6`:

```text
3bf5c45 docs: add first proof run packet
8cdfe8f docs: reconcile proof lock review gate
b7d3395 docs: lock SH-01 shadow case
7492093 docs: lock Shutterstock backtest case
f596149 docs: add AI-era proof case discovery refresh
c43cfc6 docs: add proof case discovery results
```

Required local sources were present. The required full prompt hash and required input hashes matched the wrapper and prompt pins. Dirty and untracked Orca docs were treated as allowed current workspace evidence under the wrapper and full-prompt dirty-state allowance. No clean-worktree requirement was imposed.

The public-source checks below were narrow timing checks only. They were used to establish cutoff and source-family visibility at the broad family level, not to collect evidence pools, source maps, source inventories, or evidence units.

## 2. Case-by-Case Cutoff Status

| Case | Cutoff checked | Cutoff status | Timing-level rationale |
| --- | --- | --- | --- |
| `MV-01` Intercom Fin pressure on Zendesk | Provisional 2024-09-30 to 2024-10-08 | `NEEDS_CUTOFF_PATCH` | The window is clean if the excluded outcome is Zendesk's October 9, 2024 AI Summit surface and Intercom's October 10, 2024 Fin 2 surface. It is not clean as currently worded against "Zendesk's 2024 AI-agent announcement surface" because Zendesk publicly launched AI agents at Relate on April 16, 2024. The case can likely remain usable, but the cutoff and outcome-exclusion language must specify whether the outcome is the October 2024 AI Summit expansion, not Zendesk AI agents generally. Representative timing checks: Zendesk Relate 2024, April 16, 2024, `https://www.zendesk.com/au/newsroom/articles/relate-2024/`; Zendesk AI Summit, October 9, 2024, `https://www.zendesk.com/newsroom/press-releases/zendesk-ai-summit/`; Intercom Fin 2, October 10, 2024, `https://www.intercom.com/blog/announcing-fin-2-ai-agent-customer-service/`. |
| `MV-03` Stack Overflow response to ChatGPT | 2023-07-26 | `VERIFIED_FOR_REPLAY` | The cutoff is immediately before Stack Overflow's public OverflowAI announcement on July 27, 2023. It is late enough for official AI policy, developer-survey AI sentiment, community moderation conflict, and pre-announcement developer-behavior analysis to be visible, while excluding the OverflowAI roadmap itself. Representative timing checks: Stack Overflow Developer Survey AI material, June 12 and June 14, 2023; preprint on generative AI and software Q&A submitted July 19, 2023; OverflowAI announcement July 27, 2023. |
| `MV-04` Unity Runtime Fee | 2023-09-11 | `VERIFIED_FOR_REPLAY` | The cutoff is before Unity's September 12, 2023 Runtime Fee announcement and excludes the post-announcement backlash. It is late enough for Unity public business, pricing, platform, investor, and monetization material, plus public developer trust and monetization-friction commentary around Unity's ecosystem, to be visible. Runtime-fee-specific backlash remains post-cutoff and excluded. Representative timing checks: Unity Q2 2023 shareholder letter, August 2, 2023; developer-public concern around Unity and ironSource, July 2022; Runtime Fee announcement and backlash beginning September 12, 2023. |
| `MV-05` Reddit API and data pricing | 2023-05-30 | `VERIFIED_FOR_REPLAY` | The cutoff is after Reddit's April 18, 2023 public API/data-access direction and before the broad May 31, 2023 Apollo pricing fallout and June protest wave. It is late enough for official API direction, developer-terms changes, moderator-tool promises, third-party developer concern, and community/governance concern to be publicly visible, while excluding concrete Apollo pricing and shutdown-wave evidence. Representative timing checks: Reddit API update, April 18, 2023, `https://redditinc.com/news/2023apiupdates`; Apollo pricing coverage, May 31, 2023, `https://techcrunch.com/2023/05/31/popular-reddit-app-apollo-may-go-out-of-business-over-reddits-new-unaffordable-api-pricing/`. |
| `MV-09` Thomson Reuters / Casetext legal AI response | 2023-06-25 | `VERIFIED_FOR_REPLAY` | The cutoff is before Thomson Reuters' June 26, 2023 definitive agreement to acquire Casetext. It is late enough for Casetext CoCounsel launch material, Thomson Reuters legal-AI survey and Microsoft/Copilot legal drafting material, practitioner legal-AI enthusiasm, and professional-risk signals to be visible. Representative timing checks: Casetext CoCounsel launch, March 1, 2023; Thomson Reuters legal-AI survey, April 18, 2023; Thomson Reuters Microsoft/Copilot legal drafting material, May 2023; Mata v. Avianca sanctions coverage, June 22, 2023; acquisition announcement, June 26, 2023. |

## 3. Case-by-Case Source-Family Visibility Status

### `MV-01` - Intercom Fin pressure on Zendesk

First-order public source-family visibility: visible before the checked window. Intercom Fin launch and product material were public from March 2023, with further Fin/AI material before October 2024. Zendesk AI and AI-agent material was also public before the checked window, including the April 16, 2024 Relate announcement.

Second-order public source-family visibility: visible before the checked window at broad source-family level. Public customer-support/operator discussions, Zendesk community and Reddit discussion, marketplace-adjacent AI-support alternatives, and Intercom-versus-Zendesk comparison surfaces existed before October 2024.

Source-family caution: because Zendesk's April 2024 AI-agent announcement is pre-cutoff, the current frame cannot treat the September/October cutoff as "before Zendesk's 2024 AI-agent announcement surface" without contaminating the timing logic. The case is not blocked, but the cutoff/outcome label needs a patch before replay prompting.

### `MV-03` - Stack Overflow response to ChatGPT

First-order public source-family visibility: visible before 2023-07-26. Stack Overflow public AI policy/help material and official Developer Survey AI material were public before the cutoff. Official OverflowAI material is post-cutoff and remains excluded.

Second-order public source-family visibility: visible before 2023-07-26. Public moderator-strike coverage, developer community discussion, third-party analysis of developer AI use and trust, and preprint/academic source families about generative AI and software Q&A were public before the cutoff.

Source-family caution: post-July-27 traffic retrospectives and post-OverflowAI community reaction must remain outside at-cutoff reasoning. The pre-cutoff source-family visibility is broad enough for replay prompting.

### `MV-04` - Unity Runtime Fee

First-order public source-family visibility: visible before 2023-09-11. Unity public investor, pricing, terms, platform, Create/Grow Solutions, ads, and monetization strategy materials were available before the Runtime Fee announcement.

Second-order public source-family visibility: visible before 2023-09-11. Developer-public commentary around Unity monetization, ironSource, trust, terms, engine dependence, and alternative-engine comparison existed before the cutoff.

Source-family caution: runtime-fee-specific objections, install-count ambiguity, retroactivity debate, immediate migration claims, and policy revisions are post-cutoff and must stay excluded. The pre-cutoff source-family visibility is broad enough for replay prompting.

### `MV-05` - Reddit API and data pricing

First-order public source-family visibility: visible before 2023-05-30. Reddit's April 18, 2023 official API/data-access update made the data/API monetization direction, developer-terms changes, premium-access path, and moderator-tool promises public before the cutoff.

Second-order public source-family visibility: visible before 2023-05-30. Third-party developer concern, moderator-tool concern, API-dependence discussion, NSFW/API-access concern, and user/community governance discussion were public before the cutoff.

Source-family caution: the concrete Apollo pricing figure, third-party app shutdown statements, June blackout, accessibility carve-outs, and post-cutoff moderator escalation are excluded. The cutoff is verified as a clean pre-fallout boundary, provided the future replay does not use May 31 or later pricing fallout as at-cutoff evidence.

### `MV-09` - Thomson Reuters / Casetext legal AI response

First-order public source-family visibility: visible before 2023-06-25. Casetext CoCounsel launch and product material were public from March 1, 2023. Thomson Reuters public legal-AI survey, AI investment, Microsoft/Copilot legal drafting, Westlaw, Practical Law, and legal-workflow positioning material were public before the cutoff.

Second-order public source-family visibility: visible before 2023-06-25. Legal-practitioner, legal-tech analyst, professional-risk, law-firm, and court/legal-AI-risk source families were public before the cutoff, including June 22, 2023 public coverage of sanctions for ChatGPT-generated fake cases in legal filings.

Source-family caution: the June 26 acquisition announcement, acquisition valuation commentary, closing, integration, and later CoCounsel adoption claims are post-cutoff and must remain excluded. The pre-cutoff source-family visibility is broad enough for replay prompting.

## 4. Any Cutoff Patches Needed

`MV-01` needs a cutoff/outcome-language patch before replay prompting.

- Affected case: `MV-01` - Intercom Fin pressure on Zendesk.
- Affected fields: cutoff date or cutoff window; fair-cutoff rationale; post-window exclusion rule; expected outcome-comparison window if it depends on the October 2024 outcome surface.
- Why a patch is needed: Zendesk announced AI agents publicly on April 16, 2024, before the current 2024-09-30 to 2024-10-08 cutoff window. The current frame is still usable if the excluded outcome is the October 9, 2024 Zendesk AI Summit expansion or comparable October response surface, but the present wording is too broad and can be read as excluding all 2024 Zendesk AI-agent material.
- Minimum owner decision or docs change required: decide whether `MV-01` is testing the decision moment before the October 9, 2024 Zendesk AI Summit expansion, or whether the cutoff should move before the April 16, 2024 Relate AI-agent launch. If the October decision moment is intended, patch the frame to say so explicitly and treat April 2024 Zendesk AI-agent material as pre-cutoff first-order evidence, not post-window outcome material.

No cutoff patch is needed for `MV-03`, `MV-04`, `MV-05`, or `MV-09` based on this verification pass.

## 5. Any Blocked Cases And Role-Preserving Replacement Requirement

No case is blocked by this verification pass.

If a later run blocks any case, replacement must preserve the blocked validation role:

- `MV-01`: competitor narrative pressure case.
- `MV-03`: AI disruption and developer workflow case.
- `MV-04`: reverse pricing and ecosystem-trust case.
- `MV-05`: business-model, platform, and data-monetization case.
- `MV-09`: positive-action legal AI case.

No replacement case identities are proposed or authorized by this report.

## 6. Explicit Non-Claims

Evidence replay was not run and remains unauthorized.

No evidence units, source maps, source inventories, data spine, feature plan, implementation plan, software, tooling, automation runtime, package, test, generated artifact, commit, push, or pull request were created.

No at-cutoff recommendation is made for any case. This report does not recommend that any company should watch, probe, test, hold, build, buy, partner, move, commit, narrow, phase, reposition, or take any other action.

This report verifies only cutoff timing and broad first-order and second-order public source-family visibility for replay-prompt preparation.

## 7. Current Verdict

Current verdict: `NEEDS_CUTOFF_PATCH_BEFORE_REPLAY`

`MV-03`, `MV-04`, `MV-05`, and `MV-09` are `VERIFIED_FOR_REPLAY`.

`MV-01` is `NEEDS_CUTOFF_PATCH` because its current cutoff can work only after the excluded outcome surface is narrowed to the October 2024 Zendesk AI Summit or an equivalent October response surface. Evidence replay remains unauthorized.
