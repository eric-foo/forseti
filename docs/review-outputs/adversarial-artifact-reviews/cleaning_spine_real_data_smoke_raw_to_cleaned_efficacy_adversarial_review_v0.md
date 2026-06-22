# Cleaning Spine Real-Data Smoke Raw-To-Cleaned Efficacy Adversarial Review v0

```yaml
retrieval_header_version: 1
artifact_role: Review output (adversarial evidence-trace review)
scope: >
  Read-only cross-vendor adversarial evidence-trace review of the 2026-06-21
  Cleaning spine real-data smoke: captured retail/reddit packets -> ECR
  source-side receipts -> CleaningPacket handles. Tests one bounded conclusion
  only: can an independent reviewer reconstruct the raw->ECR->handle chain from
  hash-verified bytes without the smoke fabricating success.
authority_boundary: retrieval_only
reviewed_by: claude-opus-4.8
authored_by: gpt-family-codex
de_correlation_bar: cross_vendor_discovery
same_vendor_rationale: n/a (cross-vendor: author OpenAI/GPT-family Codex; reviewer Anthropic/Claude)
commission_prompt: docs/prompts/reviews/cleaning_spine_real_data_smoke_raw_to_cleaned_efficacy_adversarial_review_prompt_v0.md
target_run_root: orca-harness/_test_runs/cleaning_spine_real_data_smoke_20260621/
branch_or_commit: codex/cleaning-spine-continuation at bc950cdfeeb3a02f33bf52217d71e049aa9093f2
non_claims:
  - not validation
  - not approval / readiness
  - not buyer proof / product proof / demand proof
  - not Judgment quality
  - not full live capture-to-Judgment E2E readiness
  - not patch authority / not mandatory remediation
```

## Commission

Adversarial review of the **product efficacy of the smoke**, where *efficacy* is bounded to a single question: can an independent reviewer trace the raw captured material, projection/consolidation outputs, ECR source-side receipts, and CleaningPacket handles well enough to reproduce or reject the conclusion — **the Cleaning spine can preserve source-visible real-data substrate through Source-Capture-shaped packets into ECR refs and Cleaning handles without fabricating success** — and nothing stronger. Buyer/demand/market/Judgment/readiness claims are out of scope.

Delegated cross-vendor reviewer: **Claude / Opus 4.8** (Anthropic), reviewing a smoke authored by **GPT-family Codex** (OpenAI). Cross-vendor discovery bar satisfied. This review is **read-only / advisory**; patch authority `NOT_CLAIMED`; findings are decision input for the home model to adjudicate.

## Preflight Receipt

```yaml
orca_start_preflight:
  agents_read: yes
  overlay_read: yes
  source_pack: custom (overlay S0 + real cleaning contracts + capture/ECR/cleaning harness code + smoke outputs)
  edit_permission: read-only (review-report write to docs/review-outputs only)
  target_scope: orca-harness/_test_runs/cleaning_spine_real_data_smoke_20260621 raw -> ECR -> Cleaning trace
  dirty_state_checked: yes
  workspace: C:\Users\vmon7\Desktop\projects\orca\.codex\worktrees\cleaning-spine-continuation
  branch: codex/cleaning-spine-continuation
  head: bc950cdfeeb3a02f33bf52217d71e049aa9093f2   # verified == pinned
  dirty_allowance: matches prompt-observed status (incl. modified orca-harness/cleaning/models.py)
  blocked_if_missing: none blocking; several prompt-named read paths are stale/absent and were substituted (see AR-04)
```

Method sequencing (Source-Gated Method Contract): `REFERENCE-LOAD` of `workflow-deep-thinking` and `workflow-adversarial-artifact-review` → required Orca authority + target source reads → `SOURCE_CONTEXT_READY` (below) → `APPLY` deep-thinking (failure-mode framing) → `APPLY` adversarial artifact review (findings-first). Both skills were available and invoked.

## SOURCE_CONTEXT_READY (with documented deviations)

**`SOURCE_CONTEXT_READY`** for the bounded raw-to-cleaned trace claim. The controlling sources (the actual in-repo Cleaning contracts, the capture/ECR/Cleaning implementation, and the smoke outputs) are all loaded and hash-verified. Several prompt-named read paths do not exist and were substituted with the real in-repo equivalents; these deviations did not block the trace but are recorded as a finding (AR-04).

Source-read ledger:

| Source | Why read | Status |
| --- | --- | --- |
| `AGENTS.md`, `.agents/workflow-overlay/README.md`, `source-loading.md`, `prompt-orchestration.md`, `review-lanes.md`, `delegated-review-patch.md`, `product-proof.md` | Authority, review-lane, de-correlation, source-gated method, non-claims | clean (read) |
| `orca/product/spines/cleaning/contracts/core_spine_v0_cleaning_spine_foundation_v0.md` | Cleaning layer boundary, handle/ledger contract, Judgment non-claims | clean (read) — **substitute** for prompt's absent `foundation/cleaning_spine_foundation_principles_v0.md` |
| `orca/product/spines/cleaning/contracts/core_spine_v0_cleaning_spine_readme_v0.md` | Cleaning purpose / build boundary | clean (read) |
| `orca-harness/runners/run_capture_ecr_cleaning_smoke.py` | The reviewed object (the stitcher) | **untracked** (in dirty allowance), read in working tree |
| `orca-harness/cleaning/models.py` | Handle / ref schema + structural coupling validators | **modified** (in dirty allowance), read in working tree |
| `orca-harness/cleaning/projection.py` | Projection-row → handle adapter | clean (read) — covers prompt's absent `cleaning_projection_doctrine_v0.md` |
| `orca-harness/source_capture/retail_pdp_projection.py` | Retail projection rows/bindings/`structure_preserved` logic | clean (read) |
| `orca-harness/ecr/deriver.py` | ECR source-side posture derivation | clean (read) |
| Smoke outputs: `stitched/{cleaning_packet,ecr_source_side_receipts,smoke_summary}.json`, `capture_ecr_cleaning_smoke_manifest.json`, `reddit_batch/batch_summary.json`, `retail/retail_capture_summary.json`, all 6 packet `manifest.json`, all 6 raw preserved files | The trace evidence | ignored `_test_runs/` (allowed as smoke evidence); all SHA-verified |

Sources **available-not-read** (not decision-bearing for this bounded trace): `core_spine_v0_corroboration_vs_amplification_discipline_v0.md` (no dedupe/clustering in this run), `source_capture_toolbox/source_capture_playbook_v0.md`, ECR `evidence_candidate_record/` + `signal_content/` plans, `reddit_candidates/*` intake JSON, `reddit_thread_urls.json`, screenshots/visible-text bytes (sizes only inspected).

Sources **absent** (prompt-named, do not exist): `docs/hygiene/cleaning_spine_lane_handoff_v0.md` (no equivalent located anywhere), `orca/product/spines/cleaning/boundaries/data_capture_to_cleaning_boundary_v0.md`, `orca/product/spines/cleaning/projection/cleaning_projection_doctrine_v0.md`, `orca/product/spines/ecr/README.md` (absence anticipated by the prompt). See AR-04.

## review_summary

```yaml
review_summary:
  trace_conclusion: bounded_raw_to_cleaned_trace_supported
  product_efficacy_claim_cap: evidence-plumbing efficacy for this bounded smoke only
  r_b2bmarketing_data_captured: yes
  limitation_handling: honest_for_flagged_residuals_with_a_gap   # variant_offer_absent + structure_not_preserved are carried honestly; the Amazon failed (404) capture is NOT flagged
  overclaim_risk: present_but_contained          # structure_preserved=true (Amazon) reads as capture quality; artifact non_claims are otherwise correct
  finding_ids: [AR-01, AR-02, AR-03, AR-04, AR-05]
```

`trace_conclusion` is `supported` because **both independent passes reproduce the same trace shape** (every handle resolves to real hash-matching bytes both directions; ECR coupling holds for all 6 packets). The findings below do **not** break trace fidelity; they bound how the result may be read and flag two upstream quality-signal overclaim vectors the smoke re-presents.

---

## Findings (Phase 1: correctness, then Phase 2: friction)

### AR-01 — `structure_preserved=true` over a failed (404) Amazon capture; the smoke emits no finding for it  · severity: **major** · phase: correctness

- **Target/role:** smoke quality signal (`smoke_summary.findings`, projection `loss_ledger.structure_preserved`) re-presented by the stitcher.
- **Anchor/evidence:**
  - `retail/amazon/packet/raw/01_cloakbrowser_rendered_dom.html` is **2,341 bytes** and is Amazon's **"Page Not Found"** 404 page (`<title>Page Not Found</title>`, "Sorry! We couldn't find that page", "Dogs of Amazon"). The companion `raw/02_cloakbrowser_visible_text.txt` is **1 byte**.
  - `retail/amazon/retail_pdp_projection.json`: `loss_ledger.structure_preserved: true`, `residuals: []`, with synthetic rows `retail_variant_offer` (sku/product_id/price/availability all `None`, `price_isolation: "absent"`) and `retail_review_substrate` (rating/review_count `None`).
  - `stitched/smoke_summary.json` `findings`: **only** the Sephora and Ulta `retail_structure_not_preserved` entries — **no Amazon entry**.
  - Mechanism — `orca-harness/source_capture/retail_pdp_projection.py`: the `amazon` branch of `_variant_offer_fields` calls `_amazon_variant_offer_fields`, which **always returns a truthy dict**, so a `retail_variant_offer` row + `sku_variant_price`/`variant_availability`/`series_locale_currency` bindings are emitted unconditionally; `_amazon_review_fields` likewise always returns a dict → `review_substrate_for_product` binding. `_retail_structure_preserved` then sees all four required binding types → `True`, regardless of whether any substrate was extracted.
- **Strongest defense, and why it fails:** "the trace is still honest — the handle points at the real 404 bytes." True, and that is why `trace_conclusion` stays `supported`. But the bounded conclusion includes *"without fabricating success,"* and `structure_preserved=true` + empty residuals + zero findings is a **green success signal with no substrate behind it**. The single retailer the smoke marks "fully structured" is the hardest capture failure; a reader using `structure_preserved` as a capture-quality signal would invert reality.
- **Impact:** `structure_preserved` is not a capture-validity signal and here actively masks a failed capture; the smoke's own honest-failure-visibility surface (`findings`) does not flag the 404. Decision-relevant overclaim vector.
- **minimum_closure_condition:** Either (a) the smoke/projection distinguishes "all binding *types* emitted" from "binding substrate actually extracted" (e.g., Amazon variant/review rows gated on non-null extraction), **or** (b) the smoke emits a capture-validity finding when a retail capture yields an error/empty page (tiny body, all-None variant+review, known block/404 markers), **or** (c) `structure_preserved` is documented as binding-shape-only and explicitly not a capture-quality signal wherever it is surfaced.
- **next_authorized_action:** home model adjudicates; owner decides (a)/(b)/(c). No patch authorized in this lane.
- **patch_queue_entry:** not authorized (advisory). **red-green proof:** would apply to (a)/(b) — a fixture of a 404/empty retail capture should fail a new capture-validity assertion before the fix and pass after. **not_proven:** that any product/readiness signal can be drawn from Amazon in this run.

### AR-02 — `variant_offer_absent` conflates "substrate absent" with "substrate present but not extracted" (Ulta)  · severity: **major** · phase: correctness

- **Target/role:** projection residual re-presented in `smoke_summary.findings[*].residuals`.
- **Anchor/evidence:**
  - `retail/ulta/retail_pdp_projection.json`: the `retail_embedded_structured_json` row (`apollo_state`) has `parse_status: "parsed"`; residual `cloakbrowser_snapshot_01:ulta:variant_offer_absent`; no `retail_variant_offer` row.
  - Independent raw probe of `retail/ulta/packet/raw/01_cloakbrowser_rendered_dom.html`: `window.__APOLLO_STATE__`×1, `skuId`×4, `salePrice`×4 — i.e. variant/price substrate **is present in the captured bytes**.
  - Mechanism — `_ulta_apollo_offer_fields` requires `skuId` **and** `productName` **and** (`listPrice` or `salePrice`) co-located on a single dict; `_structured_variant_offer_fields` requires an `@type` `Product`/`ProductGroup`. No qualifying node matched, so `variant_fields` was empty → `variant_offer_absent`. Sephora is the milder analogue: no `ld+json`/`apollo_state`/`data-comp="ProductPage"` price node, though `"offers"`×1 / `"price"`×3 tokens exist in raw.
- **Strongest defense, and why it fails:** "the residual is mechanically true — the projector bound no variant offer, and the raw `apollo_state` is preserved verbatim as a row for later." Correct, and the substrate is therefore **not lost**. But the residual *label* reads as substrate absence; for Ulta the cause is an **extraction co-location gap over present substrate**, which a downstream reader would mis-cause.
- **Impact:** limitation cause is under-described; risks an incorrect "the page had no offer" reading. Does not affect trace fidelity.
- **minimum_closure_condition:** residual vocabulary (or the limitation note) distinguishes "no offer substrate located in raw" from "offer substrate present in raw but not extracted by current recognizers."
- **next_authorized_action:** home model adjudicates; owner decides whether to refine the residual taxonomy / extractor co-location requirement. Advisory.
- **patch_queue_entry:** not authorized. **red-green:** applies to an extractor change (Ulta apollo fixture → variant row). **not_proven:** that a *complete* Sephora variant offer exists in raw (the `"offers"`/`"price"` tokens are not confirmed to be the product variant offer) — this remains **unknown** and is stated as such per the prompt's limitation-analysis requirement.

### AR-03 — The smoke exercises handle/anchor/ECR plumbing only; no Cleaning transform is performed  · severity: **minor** · phase: correctness

- **Anchor/evidence:** `run_capture_ecr_cleaning_smoke.py` builds `CleaningPacket(handles=handles)`; `stitched/cleaning_packet.json` has `transform_ledger: []` and `exact_identity_duplicate_groups: []`.
- **Impact:** none of the Cleaning *transform* mechanics (normalization/translation/summarization/dedupe), the preservation-check validators, or the Judgment-vocabulary guard (`_JUDGMENT_TOKENS` in `cleaning/models.py`) are exercised by this run. The positive conclusion must therefore be capped at **handle/anchor/ECR plumbing**; "Cleaning spine works" cannot be read as "Cleaning transforms validated."
- **Defense (holds, so this is a cap not a defect):** the prompt itself bounds efficacy to plumbing; this finding makes the cap explicit rather than alleging an error.
- **minimum_closure_condition:** the report/closeout states the smoke covers handle/anchor/ECR plumbing only; transform mechanics unexercised. (Satisfied by this report.)
- **next_authorized_action:** none required; advisory cap.

### AR-04 — Commission prompt's source pack has stale/absent named read paths (retrievability defect)  · severity: **minor** · phase: correctness

- **Anchor/evidence:** of the prompt's Required Reads + contract list, the following do not exist at the stated paths (verified against `git ls-files`): `docs/hygiene/cleaning_spine_lane_handoff_v0.md` (**absent everywhere** — the home-model lane-intent narrative is unavailable), `orca/product/spines/cleaning/foundation/cleaning_spine_foundation_principles_v0.md` (actual: `…/contracts/core_spine_v0_cleaning_spine_foundation_v0.md`), `…/cleaning/boundaries/data_capture_to_cleaning_boundary_v0.md` (absent), `…/cleaning/projection/cleaning_projection_doctrine_v0.md` (absent), `orca/product/spines/capture/source_capture_playbook_v0.md` (actual: `…/source_capture_toolbox/source_capture_playbook_v0.md`). (The ECR `README.md` absence was anticipated by the prompt.)
- **Impact:** a cold reviewer following the prompt literally cannot load its controlling sources and could wrongly land on `SOURCE_CONTEXT_INCOMPLETE` or skip controlling context. It did not block this review (real equivalents were trivially locatable and hash-verified), but it weakens reproducibility and is a prompt-quality / retrievability defect; the missing lane handoff means the smoke's intended-lane narrative could not be cross-checked.
- **minimum_closure_condition:** the prompt's source pack is corrected to the real in-repo paths, and the lane handoff is either located/created or its absence is acknowledged in the commission.
- **next_authorized_action:** home model / prompt author corrects the source pack. Advisory.

### AR-05 — Retail handle `anchor_value` is carried from projection without stitcher byte-verification; Amazon's variant anchor does not resolve in the captured bytes  · severity: **minor** · phase: correctness

- **Anchor/evidence:** for reddit, `run_capture_ecr_cleaning_smoke.py` (`_old_reddit_anchor_pattern`) **re-verifies** each handle's `data-fullname` substring is present in the raw bytes and downgrades to `anchor_kind:"file"` + emits a `reddit_row_anchor_downgraded` finding if not. For retail, `_verify_retail_projection_anchors` verifies the **file hash** but does **not** re-verify the row `anchor_value`. The Amazon `retail_variant_offer` handle carries `anchor_kind:"html_selector"`, `anchor_value:"#ASIN/#corePrice_feature_div/#availability"` — selectors that **do not resolve** in the 404 bytes (no `#ASIN`, no `corePrice`).
- **Strongest defense, and why it partially holds:** the projection derived these anchors from the bytes at capture time, and I independently confirmed the *literal* retail anchors present do appear (`"Ratings & Reviews"`×2 in Sephora, `window.__APOLLO_STATE__`×1 in Ulta). So real captures are fine. But for a failed/blocked capture the retail intra-file anchor can be **nominal/non-resolvable**, and the stitch does not detect this (unlike reddit).
- **Impact:** retail intra-file anchor precision is projection-asserted, not stitch-verified; low impact on genuine captures, but it is the same blind spot that lets AR-01's 404 pass without a finding.
- **minimum_closure_condition:** the stitcher optionally re-verifies retail `anchor_value` presence for literal-pattern anchor kinds (and downgrades/flags on miss, as reddit does), **or** the asymmetry is documented (retail intra-file anchors are projection-asserted, not stitch-verified).
- **next_authorized_action:** home model adjudicates. Advisory.

*Phase 2 (friction): no separate friction findings. The stitcher is lean; AR-04 is the only avoidable-friction item (a cold reviewer pays unnecessary search cost), already captured above.*

---

## Independent Trace Passes

Per the prompt, two independent passes were run by the reviewer (no subagents; both passes performed and reconciled in-thread). Cross-vendor de-correlation is between the GPT-family author and this Claude reviewer; intra-review subagents would not add vendor de-correlation.

### Pass A — raw-first (packets → handles)

For each of the 6 packet directories: read `manifest.json` (packet_id, source_family/surface, `source_slices` → `preserved_file_ids`, `preserved_files` paths/sizes/sha256, locator, archive posture, slice `cutoff_posture`), independently re-hashed the referenced raw file, then followed raw → projection/consolidation rows → `cleaning_packet.json` handles.

- **Retail** (`cloakbrowser_snapshot_01` / `file_01` / `raw/01_cloakbrowser_rendered_dom.html`): Sephora `01KVK3Z9…` (4 rows→4 handles), Ulta `01KVK3ZS…` (5→5), Amazon `01KVK40D…` (3→3). Projection `preserved_evidence_rows == len(rows)` and `preserved_bindings == len(binding_map)` (model-enforced by `RetailPdpProjectionPacket.validate_counts`); handle_count == rows. Each handle's `raw_anchor` (file_id/relative_packet_path/sha256/hash_basis) equals the projection row's; the stitcher hash-verifies the file against manifest **and** the projection-row expected sha.
- **Reddit** (`slice_01` / `file_01` / `raw/01_http_response_body.bin`): reddit_1 `01KVK3RH…` (post + 2 comments = 3), reddit_2 `01KVK3RM…` (post + 3 = 4), reddit_3 `01KVK3RQ…` (post + 7 = 8). The stitcher hash-verifies the raw HTML against manifest **and** the consolidation's `raw_html_sha256`, then locates each post/comment `data-fullname` in the bytes.
- **Result:** all 6 raw files exist and **hash-match** the SHAs carried in the handles (independent re-hash, not trusting the JSON):

| packet_id | raw file | size | sha match |
| --- | --- | --- | --- |
| 01KVK3Z96318Y0ZCJRE624CKG3 (sephora) | raw/01_cloakbrowser_rendered_dom.html | 1,206,748 | ✓ `2874bb42…` |
| 01KVK3ZSRP95CFFGH4WMHMQDE2 (ulta) | raw/01_cloakbrowser_rendered_dom.html | 1,209,863 | ✓ `ee854efd…` |
| 01KVK40DY7NX5ZW14N0F1Q59DM (amazon) | raw/01_cloakbrowser_rendered_dom.html | 2,341 | ✓ `0981cc6b…` |
| 01KVK3RHA2B0HDDKFT3MJ7328G (reddit_1) | raw/01_http_response_body.bin | 58,591 | ✓ `fed6f4c8…` |
| 01KVK3RMGG75NXWM9F2ZRCG1VY (reddit_2) | raw/01_http_response_body.bin | 62,246 | ✓ `64845dba…` |
| 01KVK3RQMNDBH7785V9B7GEQ1Z (reddit_3) | raw/01_http_response_body.bin | 74,583 | ✓ `3779aa33…` |

### Pass B — clean-first (handles → raw + ECR)

Starting from `stitched/cleaning_packet.json` (27 handles), grouped by `source_family`/`packet_id`, followed each `raw_anchor` (+ `projection_ref` for retail) back to the packet/raw file, and verified each `ecr_ref` resolves to a receipt for the same packet id.

- **ECR coupling:** every handle satisfies `ecr_ref.packet_id == raw_anchor.packet_id` (and retail `projection_ref.packet_id == raw_anchor.packet_id`). This is **structurally enforced** by `CleaningInputHandle.validate_refs_stay_keyed_to_raw` (`cleaning/models.py`), so it cannot silently drift. All 6 distinct `ecr_ref.ref_id` values resolve to a receipt in `stitched/ecr_source_side_receipts.json` (handle ref-id set ⊆ receipt ref-id set, 6 == 6).
- **Judgment-vocabulary check:** no handle field (`source_family`, `source_surface`, `handle_id`, anchor patterns such as `"Beauty Insider"`, `"points"`, `"Ratings & Reviews"`, `data-fullname="…"`) or ECR posture carries a `_JUDGMENT_TOKENS` term (credibility / demand / salience / independence / amplification / actionability / Signal-Use / Decision-Strength). `projection_ref.certification` is `view_only; not_cleaned; not_normalized; not_judgment_ready`. **No Judgment is smuggled into Cleaning handles or ECR refs.**
- **Reddit fullname presence (independent):** all **15/15** post/comment `data-fullname` anchor values are present in the hash-verified raw bytes; all anchors are `text_pattern` (none downgraded), consistent with the **zero** `reddit_row_anchor_downgraded` findings in `smoke_summary.json`.
- **Reconciliation:** Pass A and Pass B reproduce the **same trace shape** in both directions → `bounded_raw_to_cleaned_trace_supported`.

### Raw-to-cleaned sample trace table (representative; full 27 verified)

| handle_id | packet_id | raw anchor (file · kind · value) | sha256 | ecr_ref / projection_ref |
| --- | --- | --- | --- | --- |
| retail:sephora:…:sephora:pdp | 01KVK3Z9… | 01_cloakbrowser_rendered_dom.html · file | 2874bb42… | ecr:01KVK3Z9…:source_side_postures / retail_pdp_product |
| retail:sephora:…:sephora:review_substrate | 01KVK3Z9… | …html · text_pattern · "Ratings & Reviews" | 2874bb42… | same packet ✓ / retail_review_substrate |
| retail:ulta:…:ulta:structured:apollo_state:0 | 01KVK3ZS… | …html · script_index · "window.__APOLLO_STATE__" | ee854efd… | same packet ✓ / retail_embedded_structured_json (parse_status=parsed) |
| retail:amazon:…:amazon:variant:unknown | 01KVK40D… | …html · html_selector · "#ASIN/#corePrice_feature_div/#availability" (**does not resolve in 404 bytes — AR-05**) | 0981cc6b… | same packet ✓ / retail_variant_offer (all fields None — AR-01) |
| reddit:1:…:post | 01KVK3RH… | 01_http_response_body.bin · text_pattern · `data-fullname="t3_1tfz30e"` (present ✓) | fed6f4c8… | ecr:01KVK3RH…:source_side_postures / null |
| reddit:1:…:comment_0001 | 01KVK3RH… | …bin · text_pattern · `data-fullname="t1_omcv681"` (present ✓) | fed6f4c8… | same packet ✓ / null |
| reddit:2:…:post | 01KVK3RM… | …bin · text_pattern · `data-fullname="t3_1u6pyu9"` (present ✓) | 64845dba… | same packet ✓ / null |
| reddit:3:…:post | 01KVK3RQ… | …bin · text_pattern · `data-fullname="t3_1rjrvt9"` (present ✓) | 3779aa33… | same packet ✓ / null |
| reddit:3:…:comment_0007 | 01KVK3RQ… | …bin · text_pattern · `data-fullname="t1_o94vb84"` (present ✓) | 3779aa33… | same packet ✓ / null |

---

## Review Questions — answers

1. **Raw → cleaned (without trusting prose):** **Yes.** Every handle resolves to a real raw byte file whose sha256 I re-hashed independently; all 6 match.
2. **Cleaned → raw:** **Yes.** Retail via `projection_ref` + file-hash; reddit via `data-fullname` text patterns confirmed present in the bytes. All 27 reconcile.
3. **ECR coupling:** **Yes, and stronger than per-run luck** — `ecr_ref.packet_id == raw_anchor.packet_id` is enforced by a Pydantic `model_validator`; all 6 receipt ref-ids resolve.
4. **Limitation handling:** **Honest for what it flags, with one gap.** Sephora/Ulta `variant_offer_absent` and the two `retail_structure_not_preserved` findings are carried faithfully; raw substrate (e.g. Ulta apollo_state) is preserved verbatim. **But** the Amazon failed (404) capture is not flagged (AR-01), and `variant_offer_absent` under-describes the Ulta cause (AR-02).
5. **Reddit capture vs candidate intake:** **Distinguished, and real data was captured.** The `reddit_candidates/{fragrance,perfume,beauty}_marketing` intake is a *separate* candidate-search activity. The three *captured* threads are **r/b2bmarketing** thread bodies (`1tfz30e`, `1u6pyu9`, `1rjrvt9`), 58–74 KB of hash-verified HTML each, with every post and comment `data-fullname` present in the bytes and `observable_comment_node_count` (2/3/7) matching the handle counts. This is thread-body capture, not mere intake.
6. **Overclaim risk:** **Present but contained.** The artifacts' own `non_claims` are correct and present (`not_capture_execution`, `not_proof_run_readiness`, `not_judgment_scoring`, `not_cleaning_semantic_transform`, etc.); nothing claims E2E / buyer / product / production readiness. The live overclaim *vector* is reading `structure_preserved=true` (AR-01) or ECR `clears` as capture quality.
7. **Product-efficacy boundary:** Supports **evidence-plumbing efficacy only** (handle/anchor/ECR trace). It does **not** support any stronger product conclusion; transform mechanics are unexercised (AR-03). Stronger conclusions are rejected.

> **"r/b2bmarketing returned HTTP 200, but was any data captured?"** — **Yes.** For all three threads the preserved `raw/01_http_response_body.bin` is a full old-Reddit thread page (58,591 / 62,246 / 74,583 bytes), hash-matching the handle SHAs, and contains the post `t3_*` fullname plus every comment `t1_*` fullname carried into the handles (15/15 present). `batch_summary.json` records `capture_exit: 0` and `observable_comment_node_count` 2/3/7, matching the consolidations. The HTTP 200 here is backed by captured thread substrate, not candidate intake alone.

---

## Limitation Analysis (cause · impact · closure)

- **Sephora `variant_offer_absent` / `structure_not_preserved`:** *Cause* — the cloakbrowser rendered DOM carries no `ld+json` `Product`, no `apollo_state`, and no `data-comp="ProductPage"` `data-cnstrc-item-price` node, so all three recognizer paths returned empty (`"offers"`×1 / `"price"`×3 tokens exist but in unrecognized form; the review-substrate row also extracted rating/count `None`). *Evidenced:* projection-side **non-extraction over present-but-unrecognized substrate**. *Unknown:* whether a *complete* product variant offer is actually present in the raw bytes. *Impact:* no variant handle; structure flagged false (honest). *Closure:* see AR-02.
- **Ulta `variant_offer_absent` / `structure_not_preserved`:** *Cause* — apollo_state **parsed** and contains `skuId`×4 + `salePrice`×4, but the extractor requires `skuId`+`productName`+price co-located on one node and found none; `ld+json` `@type Product` absent. *Evidenced:* **projection-extraction gap over present substrate** (substrate not lost — preserved as the apollo_state row). *Impact/closure:* AR-02.
- **Amazon `structure_preserved=true`:** *Cause* — **not** a genuine structured capture; the raw is a 2,341-byte **404 page** and the Amazon projector branch emits variant+review rows (and thus all four bindings) unconditionally. *Evidenced:* parser artifact masking a failed capture. *Impact/closure:* AR-01. It is **not** a stitcher mishandling of residuals — the stitcher faithfully read `structure_preserved`/`residuals`; the defect is upstream (projection) and in the absence of capture-validity detection.
- **Reddit search HTTP 200 vs body capture:** candidate intake (fragrance/perfume/beauty) is separate; the captured b2bmarketing threads wrote real `SourceCapturePacket` directories with thread-body bytes + comment fullnames (verified). No downgrade findings.
- **Ignored `_test_runs`:** treated as smoke evidence only; **not** promoted/durable source truth (the directory is `.gitignore`d). No promotion claimed.
- **Web search for retail target selection:** out of band for this stitch; the smoke consumes only pre-captured packets/projections, and target URLs (`good-girl` PDPs) are recorded in `retail_capture_summary.json` as locators, not treated as source truth. (Not independently re-derived here.)
- **Cleaning scope:** Cleaning decided **no** credibility/demand/salience/independence/actionability/Judgment semantics — `transform_ledger: []`, no dedupe groups, ECR postures are source-side integrity only, no Judgment tokens anywhere (AR-03 caps this as plumbing-only).

## Validation Evidence Inspected / Not-Run Gaps

- **Inspected:** SHA256 of the 6 stitched/manifest/summary files (match the prompt's pinned hashes exactly); independent re-hash of all 6 raw preserved files (match handle SHAs); reddit fullname-presence in raw bytes (15/15); retail offer-substrate probes; ECR ref-id resolution (6/6); projection count invariants; packet-manifest slice/file/path alignment; HEAD == pinned `bc950cdf…`; dirty set == prompt-observed.
- **Not run (read-only review):** I did **not** execute the smoke runner, `tests/unit/test_capture_ecr_cleaning_smoke_runner.py`, or `tests/unit/test_cleaning_core.py`; I did **not** re-derive the projections (pre-existing artifacts — outputs and raw bytes verified, not re-built); I did **not** inspect screenshot/visible-text bytes beyond sizes, nor `reddit_candidates/*` / `reddit_thread_urls.json` contents. `orca-harness/cleaning/models.py` is **modified** in the working tree — read as-is (the version the smoke used); no claim is made that it equals any committed revision. Run timestamps are 2026-06-20 UTC while the dir label is `…20260621` (timezone/label artifact, not material).

## Strict-Claim Boundary / Not-Proven

`bounded_raw_to_cleaned_trace_supported` and "evidence-plumbing efficacy" are the **maximum** claims. **Not proven / not claimed:** validation, approval, buyer/demand/product proof, production acceptance, full live capture-to-cleaning or capture-to-Judgment E2E readiness, Judgment quality, patch authority, mandatory remediation. Cleaning *transform* correctness is **unexercised**, not validated (AR-03). Amazon carries **no** usable product/readiness signal (AR-01).

## Review-Use Boundary

These findings are **decision input only** for the home model / Chief Architect. They are not approval, validation, mandatory remediation, readiness, or executor-ready patch authority until separately accepted or authorized by a bound lane. Severity labels (`blocker`/`major`/`minor`) are prioritization only and confer no acceptance, rejection, or readiness authority.

---

```text
DELEGATED_ARTIFACT_REVIEW_RETURN_FOR_HOME_MODEL

Here is the delegated artifact review result. Adjudicate it under the
delegated-review-patch return contract.

- original commission: adversarial evidence-trace review of the 2026-06-21 Cleaning
  spine real-data smoke (raw -> ECR -> Cleaning handles), bounded to plumbing efficacy.
- reviewed artifact / scope: orca-harness/_test_runs/cleaning_spine_real_data_smoke_20260621/
  (multi-artifact smoke + ignored _test_runs outputs). Read-only; no single CA-named
  authored target file -> NOT patch-eligible; no patch authored.
- findings: AR-01 (major) structure_preserved=true over Amazon 404, no finding emitted;
  AR-02 (major) variant_offer_absent conflates absent vs present-but-unextracted (Ulta);
  AR-03 (minor) plumbing-only, transform_ledger empty; AR-04 (minor) stale/absent prompt
  source pack; AR-05 (minor) retail anchor_value not byte-verified by the stitcher.
- source evidence: hash re-verification (6/6 raw + 6/6 stitched), structural ECR coupling
  (model validator), 15/15 reddit fullname presence, Amazon 404 raw, Ulta apollo skuId/salePrice present.
- proposed patch / edits: none (not authorized; not a single authored target).
- reviewer verdict: bounded_raw_to_cleaned_trace_supported; product-efficacy cap = evidence-plumbing only.
- residual risk: structure_preserved / ECR clears are not capture-quality signals; a failed/blocked
  retail capture passes without a finding (novel block-page shapes not detected); transform mechanics unexercised.
- blockers / off-scope / not-proven: no patch authority; not validation/readiness/buyer-proof/Judgment-quality;
  lane handoff source absent (could not cross-check lane intent).
```

```yaml
review_courier:
  output_mode: filesystem-output
  report_path: docs/review-outputs/adversarial-artifact-reviews/cleaning_spine_real_data_smoke_raw_to_cleaned_efficacy_adversarial_review_v0.md
  commission: adversarial evidence-trace review of Cleaning spine real-data smoke raw-to-cleaned efficacy
  target_run_root: orca-harness/_test_runs/cleaning_spine_real_data_smoke_20260621/
  authority: advisory adversarial evidence-trace review; patch authority NOT_CLAIMED
  decision_criteria: raw/projection/consolidation/ECR/Cleaning traceability, limitation honesty, Reddit data-capture distinction, overclaim control
  reviewed_by: claude-opus-4.8
  authored_by: gpt-family-codex
  de_correlation_bar: cross_vendor_discovery
  trace_conclusion: bounded_raw_to_cleaned_trace_supported
  product_efficacy_claim_cap: evidence-plumbing efficacy only
  r_b2bmarketing_data_captured: yes
  finding_ids: [AR-01, AR-02, AR-03, AR-04, AR-05]
  next_authorized_action: home model adjudicates findings; no patch or readiness claim follows automatically
  non_claims:
    - not approval
    - not validation
    - not readiness
    - not patch authority
    - not buyer proof
    - not judgment quality
    - not full live E2E proof
```
