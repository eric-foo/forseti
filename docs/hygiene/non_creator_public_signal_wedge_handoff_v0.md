# Non-Creator Public Signal Wedge Handoff v0

```yaml
retrieval_header_version: 1
artifact_role: Orca handoff packet
scope: Cold-lane packet for evaluating non-creator public signal families that can reveal a current painful company need and support a pitch case.
use_when:
  - Restarting the non-creator public-signal wedge investigation in a fresh lane.
  - Comparing CSB source-family routes, capture capability, and buyer pain outside creator signals.
  - Preventing drift into generic competitive intelligence, AlphaSense comparison, or creator-signal work.
authority_boundary: retrieval_only
open_next:
  - AGENTS.md
  - .agents/workflow-overlay/README.md
  - .agents/workflow-overlay/source-loading.md
  - .agents/workflow-overlay/source-of-truth.md
  - .agents/workflow-overlay/decision-routing.md
  - docs/workflows/orca_repo_map_v0.md
  - forseti/product/spines/commission_signal_board/README.md
  - forseti/product/spines/commission_signal_board/prompts/orca_commission_signal_board_prompt_v0.md
  - forseti/product/spines/commission_signal_board/workflows/commission_signal_board_playbook_v0.md
  - docs/workflows/data_capture_spine_consolidation_map_v0.md
  - docs/hygiene/precompact_linkedin_lane_signal_pivot_v0.md # nonresolving: checkpoint consumed or absent from live tree; handoff keeps provenance only
stale_if:
  - The Commission Signal Board source-family map changes.
  - The Capture Spine retail/PDP or fragrance purchase-review branches land, move, or are superseded.
  - The LinkedIn/org-motion lane changes its no-live, ATS/careers, or public-actor boundary.
  - The owner re-includes creator signals in this investigation.
```

## Load Contract

- packet_version: 1
- mode: max
- created_at: 2026-06-29T16:49:45+08:00
- created_by_lane: Codex current thread, for provenance only; not authority
- workspace: `C:\Users\vmon7\Desktop\projects\orca`
- handoff_path: `docs/hygiene/non_creator_public_signal_wedge_handoff_v0.md`
- expected_branch: `codex/ig-reels-capture-spine`
- expected_head: `310ee3cb02e9d01d5f5b57a7c0092ce815d7224c`
- expected_dirty_state_including_handoff_file: pre-write state already had many unrelated untracked files; after write this handoff file should also be untracked. Re-run `git status --short --branch` and compare before acting.
- source_loading_mode: repo-overlay-bound
- durable_destination_status: bound by `.agents/workflow-overlay/artifact-folders.md` and `docs/hygiene/README.md`; checkpoint artifacts are convenience copies, not source of truth.
- load_rule: confirm-don't-trust; re-verify every load-bearing fact against its compare target before acting; sender claims are hypotheses, not authority.

## Goal Handoff

- long_term_goal: Find a narrow, sellable Orca wedge outside creator signals by using public data to detect companies currently facing a painful, cash-consequence decision.
- anchor_goal: Compare non-creator public signal families that Orca can plausibly collect or route now, then identify the strongest source family or composite signal for current-company pitch cases.
- success_signal: A fresh lane returns a ranked recommendation naming the best non-creator data wedge, the painful decision it exposes, public phase indicators, source/capture feasibility, disqualifiers, and the first pitch-case search recipe.

## Open Decision / Fork

- decision:
  - options:
    - Focus on fragrance purchase-review and Retail/PDP posture as the first non-creator wedge.
    - Focus on ATS/careers plus public org-motion as the first non-creator wedge.
    - Focus on generic competitive intelligence across reviews, hiring, LinkedIn, news, search, and product pages.
    - Reject the non-creator wedge for now and keep only creator-led demand decisions.
  - already constrained / off the table:
    - Creator/social-video signals are excluded from this investigation except as explicit non-goals or counterevidence.
    - Do not frame this as "we can do AlphaSense except transcripts"; Orca is not yet an enterprise search platform or licensed-corpus product.
    - Do not run live capture, scraping, current web casefinding, LinkedIn access, or network probes from this handoff without separate authorization/tool approval.
  - trade-offs:
    - Retail/PDP and purchase reviews are closer to SKU, channel, positioning, inventory, quality, and merchandising decisions, but may need source-specific adapters and freshness checks.
    - ATS/careers and org-motion are good phase detectors for competitor strategy, but by themselves often reveal intent rather than buyer pain; they become sharper when tied to a visible product/channel move.
    - Generic competitive intelligence sounds larger but weakens the wedge, creates AlphaSense-category expectations, and makes the sales case diffuse.
  - owner of the call: user / Orca product owner.
  - recommendation and why: treat fragrance purchase reviews plus Retail/PDP posture as the leading candidate to test, with ATS/careers/org-motion as a targeting layer rather than the product wedge. This is a hypothesis, not a final decision, because the receiver still must compare current source capability and pitch-case evidence.

## Drift Guard

- invariant, non-goal, or scope boundary: Exclude creator signals.
  - why it matters: The owner is already carving out creator signals elsewhere; this lane should find a separate or supporting non-creator wedge.
  - what violating it would break: The output would collapse back into the existing creator-signal wedge and fail to answer whether another source family is worth pitching.
- invariant, non-goal, or scope boundary: Do not build an "all competitive intelligence" wedge.
  - why it matters: Public data breadth is not the same as painful decision relevance.
  - what violating it would break: It would position Orca against AlphaSense-like expectations before Orca has transcript/licensed-corpus/search/workflow parity.
- invariant, non-goal, or scope boundary: Publicly obtainable does not mean commercially defensible or currently authorized.
  - why it matters: Capture docs distinguish pre-commercial probes, manual/source routing, and commercial-scale sanctioned access.
  - what violating it would break: The lane could overclaim source access or produce a pitch based on data Orca should not collect commercially yet.
- invariant, non-goal, or scope boundary: A checkpoint is not source authority.
  - why it matters: `source-of-truth.md` says handoff/checkpoint artifacts are convenience copies.
  - what violating it would break: The receiver would trust stale branch, source, capability, or readiness claims.

## Inherited Context (does NOT flow to a new lane)

### Source-loading state to re-establish (follows overlay doctrine)

- overlay source-loading policy: `.agents/workflow-overlay/source-loading.md`
- targets to enter the ladder:
  - `orca/product/spines/commission_signal_board/prompts/orca_commission_signal_board_prompt_v0.md`
  - `orca/product/spines/commission_signal_board/workflows/commission_signal_board_playbook_v0.md`
  - `docs/workflows/data_capture_spine_consolidation_map_v0.md`
  - `docs/hygiene/precompact_linkedin_lane_signal_pivot_v0.md`
  - `docs/workflows/orca_pricing_first_method_validation_handoff_v0.md`
  - branch `codex/fragrance-purchase-review-probes`
- already loaded (weak orientation, freshness-marked; not authority): current-turn repo reads of AGENTS, overlay files, CSB README/prompt/playbook, Data Capture submap, LinkedIn signal-pivot checkpoint, pricing-first method-validation handoff, and a volatile focused fragrance review coverage MGT receipt that was readable during source loading but absent at final verification.
- must load first (before strict or actionable steps): `AGENTS.md`, overlay README, source-of-truth, source-loading, decision-routing, artifact-folders, `docs/hygiene/README.md`, then the CSB and Data Capture sources named above.
- load rule: receiver re-runs progressive source loading per overlay; this packet's loaded-set only seeds the ladder.

### Earlier-decided concepts and behaviors (inline gist plus verify pointer)

- decision, framing, profile, or convention: Orca's current product center is consumer-demand decision support, not generic research or source-volume monitoring.
  - decided in: `docs/decisions/orca_product_thesis_consumer_demand_v0.md`, `orca/product/spines/product_lead/offer/orca_offer_hypothesis_v0.md`, and `orca/product/spines/product_lead/buyer_proof/orca_buyer_proof_packet_v0.md`
  - compare target: reread-required
  - verify before: strict product positioning, offer, or pitch-case recommendation.
- decision, framing, profile, or convention: Competitive intelligence is usable as evidence inside a decision, not as the standalone core primitive.
  - decided in: `orca/product/spines/foundation/product_contract/core_spine_v0_product_contract.md`
  - compare target: reread-required
  - verify before: saying what Orca is or is not competing with.
- decision, framing, profile, or convention: CSB organizes source-family routes and classifier handoff rows; it does not retrieve, scrape, classify demand, forecast, or recommend.
  - decided in: `orca/product/spines/commission_signal_board/prompts/orca_commission_signal_board_prompt_v0.md`
  - compare target: SHA256 `5F6060E770E9A65AD9135E33723953C67BB4B66064D37ABF65CA478954A73073`
  - verify before: using CSB as the method for this investigation.
- decision, framing, profile, or convention: LinkedIn company dossier facts were owner-rejected; the useful target is key personnel plus company openings, with openings-first via public ATS/careers where possible.
  - decided in: `docs/hygiene/precompact_linkedin_lane_signal_pivot_v0.md`
  - compare target: SHA256 `C8ED39396AE3D62B19EB31DF56B1E7048C22C8F5259A7C8864081421D866A287`
  - verify before: using org-motion as a candidate source family.
- decision, framing, profile, or convention: Pricing/competitive signals must decide a move, not merely confirm a move the firm would make anyway.
  - decided in: `docs/workflows/orca_pricing_first_method_validation_handoff_v0.md`
  - compare target: SHA256 `40FB70531A7A5292E4499CFEC7A8C4A893CA0924BF2D815CA409C993714A8F51`
  - verify before: accepting competitive-signal use cases as painful and sellable.

## Active Objective

Produce a cold-lane investigation plan and then a ranked recommendation for the strongest non-creator public signal wedge. The output should answer: which data can reveal that a company is currently in a painful decision phase, can be observed publicly, is feasible for Orca to collect or route, and can support a credible pitch case.

## Exact Next Authorized Action

1. Re-run the confirm-don't-trust load checklist and re-read the load-bearing sources named in this packet.
2. Inspect branch `codex/fragrance-purchase-review-probes` for source-family capability, but label branch-only material as not-current-main unless it is present on the current branch. Treat focused fragrance review coverage MGT content summarized in this packet as volatile orientation only unless the receiver can re-find the file or a successor artifact.
3. Compare at least these non-creator source families: purchase reviews, Retail/PDP availability-price-review posture, ATS/careers/openings, public executive/founder/org-motion, forums/community, search/AEO, news/trade, and owned channels.
4. Score each family on: current painful phase detectability, cash-consequence decision linkage, public obtainability, Orca source/capture feasibility, pitch specificity, and disqualifier risk.
5. Return a concise recommendation memo with a ranked top 3, one primary wedge, observable phase triggers, public evidence checklist, disqualifiers, and a bounded next step for finding 3 current target companies. Do not run live web/capture unless separately authorized.

## Authority And Source Ledger

- Repository instructions:
  - `AGENTS.md`
    - Role: Project behavior kernel and Orca project trigger rules.
    - Load-bearing: yes
    - Compare target: SHA256 `4296E7617D8B2675881780CD7BE0704A00DCB17ADF7758243008DE956070940B`
    - Last checked: 2026-06-29T16:49:45+08:00
    - Reuse rule: Re-read before acting.
- Overlay or equivalent authority:
  - `.agents/workflow-overlay/README.md`
    - Role: Overlay entrypoint.
    - Load-bearing: yes
    - Compare target: SHA256 `7A30709D6011BD3F6458E926570B7164B91C7F3BF8BAE7DBD5A612A08DE81FDA`
    - Last checked: 2026-06-29T16:49:45+08:00
    - Reuse rule: Re-read before acting.
  - `.agents/workflow-overlay/source-of-truth.md`
    - Role: Source hierarchy and checkpoint lifecycle.
    - Load-bearing: yes
    - Compare target: SHA256 `04DAF7979FDA605A2E7CF334DBC7ECADB02F8C1F1B40A432E14B4F3503235D0C`
    - Last checked: 2026-06-29T16:49:45+08:00
    - Reuse rule: Re-read before strict claims.
  - `.agents/workflow-overlay/source-loading.md`
    - Role: Source pack and handoff/source-loading rules.
    - Load-bearing: yes
    - Compare target: SHA256 `58994CA788F1754DEA49277750B64C592DE0A4B7B19DBF495CE675DDB9C08181`
    - Last checked: 2026-06-29T16:49:45+08:00
    - Reuse rule: Re-read before source expansion.
  - `.agents/workflow-overlay/decision-routing.md`
    - Role: Cynefin router for this cross-lane ambiguous work.
    - Load-bearing: yes
    - Compare target: SHA256 `8CA8069E20C5803A1B645921ABBD986656739C943ED0996572E26A4B9430092E`
    - Last checked: 2026-06-29T16:49:45+08:00
    - Reuse rule: Re-run router if the investigation expands.
  - `.agents/workflow-overlay/artifact-folders.md`
    - Role: Durable destination authority.
    - Load-bearing: yes
    - Compare target: SHA256 `42D4F554DAF4BE6F0A4A9BCBE3C67FD74EEFCC063FC72B03E53E11242EDC7AE9`
    - Last checked: 2026-06-29T16:49:45+08:00
    - Reuse rule: Re-read before moving or writing artifacts.
  - `.agents/workflow-overlay/artifact-roles.md`
    - Role: Role binding for hygiene/workflow artifacts.
    - Load-bearing: yes
    - Compare target: SHA256 `56C85D5FFDDA47FD3259E17509652541C2D9EDAD3D802C833FAB01F058433013`
    - Last checked: 2026-06-29T16:49:45+08:00
    - Reuse rule: Re-read before role claims.
  - `.agents/workflow-overlay/retrieval-metadata.md`
    - Role: Header contract.
    - Load-bearing: yes
    - Compare target: SHA256 `8380105F1E60D0CD613072B8C69816DC9DC7D33D853A34081949BE6775901C1F`
    - Last checked: 2026-06-29T16:49:45+08:00
    - Reuse rule: Re-read before materially editing durable workflow artifacts.
- User constraints:
  - Exclude creator signals.
  - Look at CSB and collectable public data, including competitive-intelligence-adjacent sources.
  - Identify which data type reveals strongest current painful company need and can support a pitch case.
  - Load-bearing: yes
  - Compare target: current user instruction in this thread; no filesystem hash.
  - Last checked: 2026-06-29T16:49:45+08:00
  - Reuse rule: Confirm with latest user message before expanding.
- Source-read ledger:
  - `docs/hygiene/README.md`
    - Role: Accepted hygiene-folder boundary.
    - Load-bearing: yes
    - Compare target: SHA256 `E771C08C03B5B355FE7B5BB390F22911D94A0BE8B585CBAE2DAC66ED6D5881C4`
    - Last checked: 2026-06-29T16:49:45+08:00
    - Reuse rule: Re-read before relying on hygiene retention.
  - `docs/hygiene/commission_signal_board_lane_handoff_v0.md`
    - Role: Prior CSB lane checkpoint; orientation only.
    - Load-bearing: no
    - Compare target: SHA256 `733E05110323742ABEAC055FD92E58BD00C4C8AC7190FCD1617795A746F92749`
    - Last checked: 2026-06-29T16:49:45+08:00
    - Reuse rule: Use only to find current CSB sources, not as authority.
  - `orca/product/spines/commission_signal_board/README.md`
    - Role: Current CSB spine entrypoint.
    - Load-bearing: yes
    - Compare target: SHA256 `014D3E82C7C4C2506198BE0001D224709C6E8501FE172EC7806E2306F76207A0`
    - Last checked: 2026-06-29T16:49:45+08:00
    - Reuse rule: Re-read before CSB claims.
  - `orca/product/spines/commission_signal_board/workflows/commission_signal_board_playbook_v0.md`
    - Role: CSB run sequence and validator boundary.
    - Load-bearing: yes
    - Compare target: SHA256 `04CFA2FFBCDF2BD59F1509338BA90F1EFA5B82809A43C21F6F5D12AAD4FDB2CF`
    - Last checked: 2026-06-29T16:49:45+08:00
    - Reuse rule: Re-read before dispatching or validating a board.
  - `docs/workflows/data_capture_spine_consolidation_map_v0.md`
    - Role: Data Capture / Source Capture Armory navigation and capability boundaries.
    - Load-bearing: yes
    - Compare target: SHA256 `CCC30BDA9A17266D2F1510C1D0AF016DECA1278A5458929FB50A5954D45EDF23`
    - Last checked: 2026-06-29T16:49:45+08:00
    - Reuse rule: Re-read before capability claims.
  - `docs/workflows/orca_repo_map_v0.md`
    - Role: Repo navigation.
    - Load-bearing: no
    - Compare target: SHA256 `B62390E9F64077FD66EA7BBC1E0203BF77F52F9EB3D5EF5E411F20BCF5DBDB3C`
    - Last checked: 2026-06-29T16:49:45+08:00
    - Reuse rule: Use as map only; owner sources decide.
  - `codex/fragrance-purchase-review-probes`
    - Role: Branch containing fragrance purchase-review and retail/PDP capture-route docs.
    - Load-bearing: yes for branch target identity, no for current-main capability unless merged.
    - Compare target: branch HEAD `2ca5682a4424773a386717c02c1e88eb52e7d90c`; blob `fragrance_purchase_review_retailer_recon_v0.md` = `90bf7b546154ef05435ae80faa28ea65b5a115a0`; blob `fragrance_purchase_review_row_contract_v0.md` = `be265a0ca41920ef3cc0e909321b6166a32fd6f9`
    - Last checked: 2026-06-29T16:49:45+08:00
    - Reuse rule: Inspect with `git show`/`git grep`; do not claim current-branch presence unless files exist in the current worktree or branch has landed.
- Source gaps:
  - No branch literally named "competitive intelligence" was found by `git branch --all --list "*compet*"`. Treat "competitive intelligence branch" as an owner label until a concrete ref is identified.
  - `orca/product/spines/capture/core/source_families/retail_pdp/fragrance_purchase_review_focused_coverage_mgt_v0.md` was readable and hashed during source loading, but final verification showed it absent: `Test-Path` returned `False`, `git status` for the path returned no entry, and `git ls-files --error-unmatch` reported the path is not known to Git. Treat summarized content as volatile orientation only unless re-derived.
  - Current web/current-company casefinding was not run. Any claim that a specific company is currently in a painful phase requires fresh public source verification.
  - Product-anchor files from earlier strategy work were not all re-read in this handoff turn; strict product claims require re-reading the product thesis, offer, buyer-proof packet, and ICP wedge files.
- Strict-only blockers:
  - Cannot claim source readiness, commercial access, runtime availability, product proof, buyer proof, or validation from this packet.
  - Cannot claim the focused review coverage MGT content is available, accepted, or landed.
- Not-proven boundaries:
  - No live capture run.
  - No web search.
  - No target-company case selected.
  - No source-family winner proven.

## Current Task State

- Completed:
  - Loaded `workflow-handoff` and produced this cold-lane packet.
  - Refreshed branch/head/status and source hashes.
  - Confirmed CSB source-family map includes non-creator families such as reviews, retail/PDP, search/AEO, news/trade, professional/org-motion, and owned channels.
  - Confirmed the Data Capture submap routes Retail/PDP, LinkedIn planning, Reddit/forums, and capture capability boundaries.
  - Confirmed branch material exists for fragrance purchase-review probes; a focused fragrance review coverage MGT receipt was read during source loading but was absent at final verification.
- Partially completed:
  - Candidate leading wedge hypothesis: fragrance purchase reviews plus Retail/PDP posture, with ATS/careers/org-motion as a targeting layer.
  - Branch/source comparison has not been completed by the receiver.
- Broken or uncertain:
  - "Competitive intelligence branch" is not resolved to an exact Git ref.
  - Branch-only review-route docs may not be merged into the current branch.
  - Current-company pitch cases require fresh public evidence and likely web access.
  - The focused fragrance review coverage MGT source is not available at final verification time.

## Workspace State

- Branch: `codex/ig-reels-capture-spine...origin/codex/ig-reels-capture-spine`
- Head: `310ee3cb02e9d01d5f5b57a7c0092ce815d7224c`
- Dirty or untracked state before handoff:
  - `.codex/hooks/run_orca_guard.py`
  - `_scratch/`
  - multiple untracked `docs/hygiene/*handoff*` and `*precompact*` files
  - multiple untracked prompt files under `docs/prompts/`
  - `docs/workflows/data_lake_r2_continuation_handoff_v0.md`
  - `docs/workflows/ig_reels_projection_to_ecr_consumption_decision_v0.md`
  - `worktrees/`
- Dirty or untracked state after writing the handoff file:
  - same as before, plus this new untracked handoff file. Receiver must verify with `git status --short --branch`.
- Target files or artifacts:
  - this handoff under `docs/hygiene/`
  - CSB prompt/playbook
  - Data Capture submap
  - LinkedIn signal-pivot checkpoint
  - fragrance purchase-review branch docs
  - volatile focused-review coverage MGT content observed during source loading
- Related worktrees or branches:
  - `codex/fragrance-purchase-review-probes`
  - `codex/fragrance-native-live-probe`
  - `codex/scanning-csb-first-followup`
  - `remotes/origin/codex/scanning-fragrance-commission`
  - `remotes/origin/codex/commission-gate`
  - `remotes/origin/codex/commission-spine-structure`

## Changed / Inspected / Tested Files

- `docs/hygiene/non_creator_public_signal_wedge_handoff_v0.md`
  - Status: added by this handoff creation.
  - Role: cold-lane checkpoint.
  - Important observations: non-authoritative, retrieval-only; receiver must delete/retire after consumption per checkpoint lifecycle.
  - Symbols or sections: full handoff packet.
- `orca/product/spines/commission_signal_board/prompts/orca_commission_signal_board_prompt_v0.md`
  - Status: inspected.
  - Role: CSB source-family map and board boundaries.
  - Important observations: CSB can route reviews, retail/PDP, search/AEO, news/trade, professional/org-motion, and owned channels; it does not retrieve, scrape, classify, forecast, or recommend.
  - Symbols or sections: Source-Family Map, Final Rules, Non-Claims.
- `docs/workflows/data_capture_spine_consolidation_map_v0.md`
  - Status: inspected.
  - Role: capture capability map.
  - Important observations: Retail/PDP, LinkedIn planning, Reddit/forums, CloakBrowser, and armory boundaries are routed here; commercial/source-access and runtime claims remain bounded.
  - Symbols or sections: Fast Route, Current Reality Snapshot, Areas.
- `docs/hygiene/precompact_linkedin_lane_signal_pivot_v0.md`
  - Status: inspected.
  - Role: prior competitive-intelligence/LinkedIn lane checkpoint.
  - Important observations: owner rejected generic company dossiers; useful signal target is key personnel plus company openings; openings-first via public ATS/careers.
  - Symbols or sections: Frozen Decisions, Exact Next Authorized Action.
- `orca/product/spines/capture/core/source_families/retail_pdp/fragrance_purchase_review_focused_coverage_mgt_v0.md`
  - Status: inspected during source loading; absent at final verification; not tracked.
  - Role: volatile focused review-coverage receipt; orientation only.
  - Important observations: the read copy argued for focused review coverage rather than all public review rows; pinned Luckyscent Judge.me route reportedly returned 14 deduped review rows and selected 10 under policy. Receiver must re-find or re-derive this before relying on it.
  - Symbols or sections: Decision, Luckyscent Pinned Route Probe, Focused Selection Policy, Non-Claims.

## Frozen Decisions

- Decision: This handoff should produce a separate lane, not solve the whole wedge in this thread.
  - Evidence: User explicitly invoked `workflow-handoff`; skill contract requires a durable, cold-reader packet.
  - Consequence: Receiver owns the ranked recommendation and any current-company casefinding.
- Decision: Creator signals are excluded.
  - Evidence: User said "everything except creator signals."
  - Consequence: Creator/social-video rows in CSB are non-goals for this investigation.
- Decision: Generic competitive intelligence is not the default product wedge.
  - Evidence: Prior product-lead reasoning and current drift guard; AlphaSense-like positioning creates breadth and workflow expectations.
  - Consequence: Receiver should rank decision-tied source families, not write "Orca competitive intelligence" positioning.
- Decision: Leading hypothesis is purchase reviews plus Retail/PDP posture, not ATS-only.
  - Evidence: Review/PDP branch docs, volatile focused-coverage receipt content observed during source loading, and direct linkage to SKU/channel/quality/allocation decisions.
  - Consequence: Receiver should test this first, not accept it without comparison.

## Mutable Questions

- Question: Is fragrance purchase-review plus Retail/PDP posture the strongest non-creator source family?
  - Why still mutable: It has strong local evidence, but branch material may not be merged and current-company pitch fit is not proven.
  - What would resolve it: Ranked comparison against ATS/org-motion, forums/community, search/AEO, and news/trade using the scoring dimensions above.
- Question: Is org-motion a product wedge or only a targeting/qualification layer?
  - Why still mutable: ATS/openings reveal phase and intent, but may not expose enough buyer pain alone.
  - What would resolve it: Cases where public openings point to a near-term budget decision a company would pay to de-risk.
- Question: Which buyer decision should the non-creator wedge sell to?
  - Why still mutable: Purchase reviews map to product/retail/allocation decisions; org-motion maps to competitor response/strategy decisions.
  - What would resolve it: Three current public case candidates with named decision phase and public evidence.
- Question: What exact Git ref did the owner mean by "competitive intelligence branch"?
  - Why still mutable: No `*compet*` branch name was found except unrelated names.
  - What would resolve it: Owner names the branch or receiver discovers a concrete ref through broader branch/file search.

## Superseded / Dangerous-To-Reuse Context

- Stale instruction, idea, artifact, or finding: "We can pretty much do everything AlphaSense does except transcripts."
  - Why stale or dangerous: Orca can perform public-source decision intelligence, but AlphaSense implies licensed corpora, transcripts, enterprise search, alerts, workflow, and commercial source-rights posture.
  - Current replacement: Position Orca around constrained decision recommendations over public origin/source evidence, not platform parity.
- Stale instruction, idea, artifact, or finding: Generic company dossier as competitive intelligence.
  - Why stale or dangerous: The LinkedIn signal-pivot packet says the owner rejected static commodity company facts.
  - Current replacement: Dynamic key personnel plus company openings, especially public ATS/careers, as phase/intent indicators.
- Stale instruction, idea, artifact, or finding: All public review rows should be captured.
  - Why stale or dangerous: The volatile focused-coverage MGT content observed during source loading argued the mini god-tier shape is focused coverage, not full archives, but the source is absent at final verification.
  - Current replacement: Focused review coverage with aggregate context, row metadata, priority row selection, skipped-row receipt, and residuals.

## Commands And Verification Evidence

- Command:
  ```powershell
  git status --short --branch
  ```
  Result:
  - Passed.
  - Important output: `## codex/ig-reels-capture-spine...origin/codex/ig-reels-capture-spine` with many unrelated untracked files. A focused review coverage MGT receipt was readable during source loading but absent at final verification.
  - Re-run target so the receiver can confirm rather than trust: same command.
- Command:
  ```powershell
  git rev-parse HEAD
  ```
  Result:
  - Passed.
  - Important output: `310ee3cb02e9d01d5f5b57a7c0092ce815d7224c`.
  - Re-run target so the receiver can confirm rather than trust: same command.
- Command:
  ```powershell
  git branch --all --list "*compet*" --verbose --no-abbrev
  ```
  Result:
  - Passed.
  - Important output: no branch literally named competitive intelligence was found; only unrelated `competent-*` branch names.
  - Re-run target so the receiver can confirm rather than trust: same command plus broader branch/file search if needed.
- Command:
  ```powershell
  git rev-parse codex/fragrance-purchase-review-probes
  ```
  Result:
  - Passed.
  - Important output: `2ca5682a4424773a386717c02c1e88eb52e7d90c`.
  - Re-run target so the receiver can confirm rather than trust: same command.
- Command:
  ```powershell
  Get-FileHash -Algorithm SHA256 <source files>
  ```
  Result:
  - Passed.
  - Important output: hashes recorded in the source ledger.
  - Re-run target so the receiver can confirm rather than trust: rerun for the exact sources the receiver uses.
- Validation not run:
  - No CSB validator, tests, web search, live capture, or source-capture run was executed. This is a handoff creation only.

## Blockers And Risks

- Blocker or risk: Source-family breadth could dilute the wedge into generic competitive intelligence.
  - Evidence: User mentioned product reviews, ATS, LinkedIn, and AlphaSense-style competitive intelligence.
  - Likely next action: Force ranked source-family comparison against painful-decision criteria.
- Blocker or risk: Review/PDP route evidence is partly branch-only and partly volatile.
  - Evidence: `fragrance_purchase_review_*` docs are visible on `codex/fragrance-purchase-review-probes`; focused-coverage MGT content was observed during source loading but is missing at final verification.
  - Likely next action: Receiver must inspect current branch versus branch-only docs before capability claims.
- Blocker or risk: Current-company pitch cases require live public evidence.
  - Evidence: This handoff did not browse or run source capture.
  - Likely next action: After selecting the source family, ask for or use bounded authorization/tool approval for fresh public casefinding.
- Blocker or risk: LinkedIn live/commercial posture.
  - Evidence: Data Capture submap and LinkedIn checkpoint preserve no-live/planning-only and ToS-gray boundaries, with ATS/careers preferred.
  - Likely next action: Prefer public ATS/careers pages for org-motion; treat LinkedIn as planning-only unless explicitly routed.

## Confirm-Don't-Trust Load Checklist

- Load-bearing facts the receiver must re-verify before acting:
  - Current branch and HEAD.
  - Dirty/untracked state, especially whether any focused review coverage MGT receipt can be re-found.
  - Source hashes for overlay, CSB, Data Capture, LinkedIn, and repo map files.
  - Branch existence and HEAD for `codex/fragrance-purchase-review-probes`.
  - Whether the `fragrance_purchase_review_*` branch docs are current-main, branch-only, or superseded.
  - Whether any exact "competitive intelligence branch" exists under a different name.
- Compare target for each:
  - Use the hashes, HEADs, blob IDs, and commands in this packet.
- Load outcomes and what each means:
  - `REUSE`: all required load-bearing facts reverified; continue from Exact Next Authorized Action.
  - `PARTIAL_REUSE`: optional orientation sources drifted; reuse verified sources and re-derive drifted context.
  - `STALE_REREAD_REQUIRED`: branch/head/source hashes drifted but can be re-read safely.
  - `BLOCKED_DRIFT`: drift conflicts with source authority, target source identity, or owner constraints.
  - `BLOCKED_MISSING_PACKET`: this file is absent or unreadable.
  - `BLOCKED_UNVERIFIABLE`: a load-bearing claim cannot be re-derived.
- Sources that must be reread if drift is detected:
  - `AGENTS.md`
  - `.agents/workflow-overlay/source-of-truth.md`
  - `.agents/workflow-overlay/source-loading.md`
  - `orca/product/spines/commission_signal_board/prompts/orca_commission_signal_board_prompt_v0.md`
  - `docs/workflows/data_capture_spine_consolidation_map_v0.md`
  - `docs/hygiene/precompact_linkedin_lane_signal_pivot_v0.md`
  - branch `codex/fragrance-purchase-review-probes`

## Do Not Forget

- Strong pushback to preserve: "publicly collectable" is not the same as "sellable"; the winning wedge must reveal a current painful decision.
- Leading hypothesis to test: purchase reviews plus Retail/PDP posture are closest to cash decisions; ATS/careers/org-motion is likely a targeting layer unless tied to a concrete allocation or competitor-response decision.
- The final recommendation must name disqualifiers. Examples: generic market monitoring, "what's happening in fragrance," company dossier facts, dashboards, no 30-90 day decision, no public current-phase evidence, or source access requiring commercial/legal posture not yet bound.
- If current-company cases are requested, browse or source-check fresh public evidence with citations; do not invent "currently facing" from repo docs.
