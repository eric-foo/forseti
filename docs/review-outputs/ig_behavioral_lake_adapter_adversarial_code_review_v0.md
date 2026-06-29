# IG Behavioral Lake Adapter — Delegated Adversarial Code Review v0

```yaml
retrieval_header_version: 1
artifact_role: Delegated adversarial code review report
scope: Review of PR #441 IG behavioral lake adapter against YouTube behavioral parity and failure-visibility expectations.
use_when:
  - Adjudicating or auditing PR #441 review findings and patch closure.
  - Checking why IG lake adapter failures now surface packet, grid, ASR, and product residuals.
authority_boundary: retrieval_only
branch_or_commit: codex/ig-behavioral-lake-adapter @ 0265c0275bd30e7309f6ef53b287149c730058c9
open_next:
  - orca-harness/source_capture/ig_reels_behavioral_lake.py
  - orca-harness/tests/unit/test_ig_reels_behavioral_lake.py
```

```yaml
review_summary:
  status: completed
  report_path: docs/review-outputs/ig_behavioral_lake_adapter_adversarial_code_review_v0.md
  recommendation: patch_before_acceptance
  reviewed_by: claude-opus-4.8
  authored_by: unrecorded   # commission recorded author family "OpenAI / GPT-family, operator_to_confirm"; no model+version supplied -> unrecorded, not fabricated
  de_correlation_bar: cross_vendor_discovery   # controller=Anthropic/claude-opus-4.8 (confirmed) vs recorded author=OpenAI/GPT (operator_to_confirm); CONTINGENT on operator confirming the recorded author family
  summary: "Adapter is correct and well-tested on the happy path, but silently swallows load/record failures (breaking the YouTube discovery-failed parity it targets) and leaves the grid input path entirely untested."
  findings_count: 5
  blocking_findings:
    - F-01: load_raw_packet failures swallowed with no discovery_failed residual (YouTube-parity divergence)
    - F-02: grid input path entirely untested; grid failures swallowed with no residual
  advisory_findings:
    - F-03: corrupt/unkeyable product-mention and ASR records silently dropped (misattributed, not surfaced)
    - F-04: bespoke SourceCapturePacket(**manifest) diverges from blessed model_validate reconstruction
    - F-05: product-mention lane constants hardcoded instead of imported (inconsistent with deep-capture imports)
  prior_findings_remediated: []
  next_action: "CA adjudicates F-01/F-02: commission a bounded patch to surface discovery/unreadable residuals + add grid coverage, OR record an explicit, documented accepted-residual decision (silent omission is not contract-permitted)."
```

## Commission And Boundary

- **Commission:** Independent, de-correlated adversarial implementation review of **PR #441 "Add IG behavioral lake adapter"** for material bugs, behavioral-regression risk, false completeness, missing tests, and source-boundary violations.
- **Goal under review (fitness anchor):** *behavioral completeness parity with the already-built YouTube behavioral lane* — not identical IG/YT capture mechanics, not a shared-core refactor.
- **Authority:** This is review (decision input) only. No files were edited; no executor-ready `patch_queue_entry` is emitted (not a patch-queue or patch-execution lane). Findings may carry advisory remediation direction; any patch requires a later CA-adjudicated execution assignment.
- **Recommendation `patch_before_acceptance` is reviewer decision-input, not a merge block.** It means the *parity claim* is not yet met for unreadable/failed inputs and the grid path is unverified; the CA may instead accept F-01/F-02 as **named, documented** residuals. What is not contract-permitted is leaving them as *silent* omissions (per the IG back-fix spec).

## De-correlation Receipt

- **Controller / reviewer:** Anthropic — `claude-opus-4.8` (confirmed; I am the reviewing model).
- **Author / home:** recorded in the commission as *OpenAI / GPT-family, operator_to_confirm*; the PR is git-committed by a human (`Eric <fooyuquan@gmail.com>`). No model+version was supplied → `authored_by: unrecorded` (never fabricated).
- **Bar:** Cross-vendor (Anthropic ≠ recorded OpenAI lineage) → **discovery** bar, **contingent** on the operator confirming the recorded author family. If that cannot be confirmed, this drops to the same-vendor sanity / advisory tier per the two-bar rule in `.agents/workflow-overlay/review-lanes.md`. The findings below stand regardless of the bar.

## Source Context

`SOURCE_CONTEXT_READY`. Method contract honored: `workflow-deep-thinking` then `workflow-code-review` reference-loaded before source load; applied only after readiness.

**Worktree preflight (passed):** `C:\Users\vmon7\Desktop\projects\orca\worktrees\ig-behavioral-lake-adapter`, branch `codex/ig-behavioral-lake-adapter`, HEAD `0265c0275bd30e7309f6ef53b287149c730058c9`, clean working tree (no local modifications in target files).

**PR diff (vs `origin/main`, merge-base `a79b9290`):** single commit `0265c027`. Three files: `A source_capture/ig_reels_behavioral_lake.py` (+379), `A tests/unit/test_ig_reels_behavioral_lake.py` (+140), `M tests/contract/test_ig_reels_behavioral_projection_no_runtime_imports.py` (+12/-4). The other source-pack files are pre-existing **adjacent context**, not part of the diff.

**Source-read ledger (target worktree @ 0265c027):**
- Authority/overlays: `AGENTS.md`, `.agents/workflow-overlay/{README,source-of-truth,source-loading,prompt-orchestration,review-lanes,delegated-review-patch,validation-gates,communication-style}.md`.
- Parity contracts: `docs/workflows/{ig_behavioral_sync_from_youtube_contract_handoff_v0, youtube_behavioral_contract_from_merged_main_v0, shared_capture_core_ig_youtube_tiktok_planning_v0, ig_backfix_against_youtube_behavioral_contract_spec_v0}.md`.
- Diff targets: `source_capture/ig_reels_behavioral_lake.py`, `tests/unit/test_ig_reels_behavioral_lake.py`, `tests/contract/test_ig_reels_behavioral_projection_no_runtime_imports.py`.
- Adjacent code: `source_capture/ig_reels_behavioral_projection.py`, `source_capture/ig_reels_grid_projection.py`, `source_capture/ig_reels_deep_capture_lake.py`, `source_capture/transcript/ig_reels_audio_packet.py`, `cleaning/transcript_product_lake.py`, `data_lake/root.py`, `source_capture/packet_assembly.py`, `source_capture/writer.py` (manifest write), `schemas/case_models.py` (StrictModel), `source_capture/models.py` (no aliases), `source_capture/ig_projection.py:_read_packet_directory`, `runners/run_source_capture_ig_reels_grid_packet.py` (surface constant).

## Failure-Mode Framing (deep-thinking)

The adapter is a read-only projection-feeder: it discovers already-persisted IG records (grid, deep-capture, standalone-audio ASR, product extraction) and feeds them into the existing `project_ig_reels_behavioral_item`. The high-risk surfaces for a *behavioral-completeness-parity* goal are therefore not the happy path but the **edges**:

1. **Failure visibility** — does an unreadable/corrupt/incomplete persisted record *surface as a residual*, or does it vanish? The whole point of the projection is "inspect partials and residuals without pretending"; an adapter that silently drops failures defeats it and breaks parity with YouTube, whose contract explicitly surfaces `discovery_failed`.
2. **Discovery fidelity** — does the manual lake walk find the real records at their real sharded paths, and are record IDs injected from path/metadata (durable) rather than body fields real writers don't emit?
3. **Completeness honesty** — can `behavioral_completeness.complete` ever read true while a real gap exists?
4. **Coverage** — do the tests use real writer shapes and exercise the failure edges, or only the happy path?
5. **Scope discipline** — does it avoid prematurely building a shared IG/YT core or copying YT mechanics?

Discovery fidelity (2), completeness honesty (3), and scope discipline (5) hold up well (see Non-Findings). Failure visibility (1) and coverage (4) are where the material findings concentrate.

## Findings (severity-ordered)

### F-01 — major — `load_raw_packet` failures are silently swallowed; no `discovery_failed` residual (direct YouTube-parity divergence)

- **Location:** `source_capture/ig_reels_behavioral_lake.py:108-119`, the `except Exception: continue` at lines **110-113** (`_collect_packet_backed_inputs`).
- **Evidence:** `data_root.load_raw_packet(packet_id)` fails closed on a missing/malformed/unreadable manifest, a size or sha256 mismatch, or a path escape (`data_lake/root.py:797-883`). On any such raise the adapter `continue`s — emitting **no residual and no source**. The availability index still lists the packet (`list_available`, `root.py:893-903`), so the packet is "known available" yet its content silently never reaches the projection.
- **Authority / parity basis:** The YouTube behavioral contract — the commission's named parity reference — specifies that on `load_raw_packet` failure the YT projection *"appends a fail-visible discovery source and continues"* and turns it into a source-level `discovery_failed` residual (`youtube_behavioral_contract_from_merged_main_v0.md:87,94,126-134,221`). The IG projection already wires the `discovery_failed` vocabulary into `EXTRACTION_PROBLEM_STATUSES` and `SOURCE_COMPLETION_PROBLEMS` (`ig_reels_behavioral_projection.py:16-27`), but the adapter never produces it. The IG back-fix spec requires the run receipt to *"preserve visible failure"* and correlation to *"not leave these surfaces discoverable only by human convention"* (`ig_backfix_against_youtube_behavioral_contract_spec_v0.md:173-183,200-201`). The handoff drift-guard / MGT lens forbids *"hidden completeness claims"* and requires failures to be *"visible"*. The code comment "discovery failure is not target-attributable here" is explicitly pre-rejected by the YT transfer note, which projects discovery failures onto the target even when the packet cannot prove its own id and names a *lane/global discovery residual channel* as the correct alternative (`youtube_behavioral_contract...:287`).
- **Impact:** A corrupt / sha-mismatched / unreadable IG audio or grid packet vanishes. A shortcode present *only* in that packet disappears from the index entirely with zero residual. A shortcode known elsewhere receives a misleading `ig_*_absent` residual ("nothing captured") instead of `discovery_failed` ("captured but unreadable") — actively **misattributing an integrity failure as absence**. This is the precise hidden-failure mode the module docstring and the parity contract exist to prevent.
- **minimum_closure_condition:** Every `load_raw_packet` failure is surfaced somewhere discoverable — a per-target `discovery_failed` source/residual when attributable, or an adapter/lane-level discovery residual carried onto projected items when not — matching the YouTube fail-visible behavior; with a test that commits an unreadable/sha-mismatched IG packet and asserts the residual. *Alternatively*, the CA records an explicit, documented accepted-residual decision (silent omission is not contract-permitted).
- **next_authorized_action:** CA decision — commission a bounded patch to emit discovery residuals, or record an explicit accepted-residual decision. (Advisory; no patch authority in this commission.)

### F-02 — major — Grid input path is entirely untested; grid reconstruction/projection failures are silently swallowed

- **Location:** `ig_reels_behavioral_lake.py:145-159` (`_collect_grid_packet_inputs`), the `except Exception: return` at lines **146-153**, and the `SourceCapturePacket(**loaded.manifest)` reconstruction at line **147**. The new `tests/unit/test_ig_reels_behavioral_lake.py` exercises audio + deep-capture + product-mentions + the fully-missing item, but **never a grid packet**.
- **Evidence:** No test writes an `ig_reels_grid_dom_passive_json` packet and asserts the adapter yields candidate rows, `ranking_basis`, or `persistence_correlation.grid_packet_ids/grid_row_ids`. The surface constant is correct (`_IG_GRID_SURFACE` == `run_source_capture_ig_reels_grid_packet.py:91`) and the reconstruction round-trips *today* (StrictModel is `extra="forbid", populate_by_name=True` with no field aliases — `schemas/case_models.py:11`, `source_capture/models.py`; manifest is `packet.model_dump(mode='json')` — `source_capture/writer.py:202`), so this is a coverage + failure-visibility gap, not a current functional break. But the inner `except Exception: return` drops **any** grid reconstruction/projection failure with no residual — the same hidden-state class as F-01, for the grid surface.
- **Authority basis:** The decision criteria explicitly flag "grid-derived inputs" as a material untested path; the back-fix spec acceptance criterion #2 requires grid ranking/limitations to be *explicit and testable* (`ig_backfix...:265-266`). The candidate/ranking half of "behavioral completeness parity" is therefore unverified through the adapter.
- **Impact:** A future manifest-schema or grid-projection-contract drift would silently disable IG candidate/ranking projection (every item → `ig_grid_candidate_absent`) with **no failing test**. A malformed grid packet today vanishes with no residual.
- **minimum_closure_condition:** A unit test that builds a real `ig_reels_grid_dom_passive_json` packet (via the real capture/writer path or a realistic fixture) and asserts the adapter yields candidate rows, `ranking_basis`, and grid persistence anchors for the shortcode; plus a test that a malformed grid packet surfaces a discoverable residual (ties to F-01).
- **next_authorized_action:** CA decision — commission grid coverage (and a grid load-failure residual), or accept the gap explicitly.

### F-03 — minor — Corrupt/unkeyable product-mention and ASR records are silently dropped (misattributed, not surfaced)

- **Location:** `_collect_product_extraction_results` lines **204-208** (non-dict body → `continue`; missing `video_id` → `continue`); `_collect_audio_packet_inputs` lines **139-141** (ASR record with no shortcode/video_id and no `meta_shortcode` → `continue`). `_read_json_file` returns `None` on `OSError`/`ValueError` (lines 334-338).
- **Evidence:** A present-but-corrupt product-mention record is skipped with no residual; the correlated standalone-audio source then shows `extraction_status="not_attempted"` (no result matched) rather than surfacing the corruption — i.e., "attempted but the record is unreadable" is reported as "not attempted." Likewise an ASR record that cannot be keyed to a shortcode never reaches the projection, so the projection's own `ig_transcript_source_shortcode_absent` residual never fires. The real writers always populate these fields (`audio_packet.py:294-295` writes shortcode+video_id; `transcript_product_lake.py:117` writes video_id), so this is a defensive / corrupt-on-disk path — hence **minor** — but the module's stated purpose is surfacing exactly these unreadable states.
- **Not a false-pass:** `behavioral_completeness.complete` stays `False` in these cases; this is a visibility/misattribution defect, not hidden completeness.
- **minimum_closure_condition:** An unreadable/corrupt product-mention record (and a `video_id`-less or shortcode-less record) yields a discoverable residual rather than a silent skip; covered by a test.
- **next_authorized_action:** Fold into the F-01 discovery-residual patch, or accept as a named residual. (CA decision.)

### F-04 — minor (optional hardening) — Bespoke `SourceCapturePacket(**loaded.manifest)` diverges from the blessed `model_validate` reconstruction

- **Location:** line **147** vs the canonical reader `_read_packet_directory` (`source_capture/ig_projection.py:272`, which uses `SourceCapturePacket.model_validate(...)`).
- **Evidence:** Functionally equivalent today (no aliases; `populate_by_name=True`; `extra="forbid"`). But `**`-construction would break — and then be swallowed by the F-02 broad `except`, silently dropping grid — if a future field alias is added or the manifest gains a non-identifier key. `model_validate(loaded.manifest)` is the single blessed, alias-safe entry already used elsewhere.
- **minimum_closure_condition:** Adapter reconstructs via `SourceCapturePacket.model_validate(loaded.manifest)` (or reuses the shared reader).
- **next_authorized_action:** Optional hardening (clearly optional, non-required).

### F-05 — minor (optional hardening) — Product-mention lane constants hardcoded instead of imported

- **Location:** lines **31-33** — `_PRODUCT_MENTIONS_LANE` / `_PRODUCT_MENTIONS_SET_LANE` duplicate the exported `PRODUCT_MENTIONS_LANE` / `PRODUCT_MENTIONS_SET_LANE` (`cleaning/transcript_product_lake.py:29-30`), while the adapter *imports* the deep-capture lane constants (lines 17-21). `_ASR_LANE="transcript_asr"` (line 31) also duplicates the writer's literal (`audio_packet.py:313`), though no shared constant exists there (symmetric; lower concern).
- **Evidence:** Drift risk if the canonical product-mention constants change; partially mitigated because the new test writes via the canonical import and reads back through the adapter literal, so a divergence would fail the test.
- **minimum_closure_condition:** Import the canonical `PRODUCT_MENTIONS_LANE` / `PRODUCT_MENTIONS_SET_LANE` from `cleaning.transcript_product_lake` instead of re-declaring literals.
- **next_authorized_action:** Optional hardening.

## Non-Findings Worth Recording For CA Adjudication

These were attacked and held; recorded so the CA does not re-spend the cycle:

1. **Sharded lake walk is correct.** `_iter_derived_lane_records` (lines 301-316) walks `derived/<anchor_shard>/<raw_anchor>/<lane>/<record>` with exactly two nested loops, so `anchor_dir.name` *is* the raw_anchor — matching `root.py:15` and the `append_record_set` write path (`root.py:563-573,618-623`). No off-by-one; the manual walk and the `record_path`/`lane_dir`/`is_record_set_complete` API agree on the anchor.
2. **Record IDs are injected from path / record-set metadata, not body fields writers don't emit.** Deep-capture id == the completion-marker filename == `deep_capture_record_id(result)` (`ig_reels_deep_capture_lake.py:31-42`); ASR id == the `transcript_asr` record filename `asr_<token>__<sha16>` (`audio_packet.py:309`); audio shortcode is taken from `capture_metadata.json`'s `platform_shortcode` (`audio_packet.py:199,206`). Satisfies that decision-criteria axis.
3. **`complete=True` with an `ig_grid_candidate_absent` residual is parity-consistent, not false completeness.** YouTube's `behavioral_completeness.complete` is *identically* transcript-extraction-rollup-only, carrying metadata/candidate absence as a residual (`youtube_behavioral_contract...:43,182`; `youtube_metadata_packet_absent`). The adapter inherits the projection's rule; it invents no new completeness rule.
4. **No premature shared IG/YT core; no YT mechanics copied.** The adapter imports only IG modules + the IG projection + the lake root. Satisfies the drift guard (`ig_behavioral_sync...:83-91`) and the thin-core boundary (`shared_capture_core...:210-225`; `ig_backfix...:73-86`).
5. **Deep-capture transcript correctly excluded from the extraction feed and residualized.** `extraction_feed_eligible=False` → `non_eligible_reason="deep_capture_not_in_extraction_feed"` → `ig_transcript_source_not_extraction_eligible` residual, and the happy-path test asserts the item is `complete_with_residuals` (not `complete`). This is a *named, discoverable* residual — the back-fix spec's accepted-residual condition (`ig_backfix...:294-296`).
6. **Contract test correctly extended.** `test_ig_reels_behavioral_projection_no_runtime_imports.py:24-33` now guards **both** the projection and the new adapter module against acquisition/LLM imports; the adapter's direct imports are clean at the AST level.
7. **`rebuild_availability` write is opt-in** (default `False`, gated) — matches the YT contract and the module docstring's write claim.
8. **The `complete_with_residuals` downgrade is coherent.** Lines 244-252 update `behavioral_completeness.status/complete` and the shared rollup object together; no internal inconsistency.

## Validation Evidence Inspected, And Gaps

**Independently reproduced** (this review, target worktree @ `0265c027`, Python 3.11.15):
- Broader IG set → **`91 passed in 2.38s`** (this set includes the three focused files).
- Focused 3-file set → 17 passing dots, `[100%]`, **0 failures** (matches lane-reported "17 passed").
- These corroborate the lane-reported `17 passed` / `91 passed`.

**Taken as reported, not re-run:** GitHub CI `orca-harness-tests` green on PR #441 (I did not re-trigger CI).

**Validation gaps (material):** The passing suite does **not** cover (a) grid input discovery (F-02), (b) discovery-failure / unreadable-packet residual surfacing (F-01), or (c) corrupt product-mention / unkeyable ASR record handling (F-03). Per `.agents/workflow-overlay/validation-gates.md` ("missing evidence is not a pass"), green tests are **not** evidence that the failure-visibility behavior the module claims as its purpose is actually exercised. The tests that exist do use **real writer shapes** (`write_ig_reels_asr_transcript`, `write_reel_deep_capture_into_lake`, `append_record_set` with canonical lane constants, `DataLakeRoot.for_test`) — good fidelity for the happy path; the gap is edge coverage, not synthetic-record fakery.

## Residual Risk

- **De-correlation contingency:** the discovery bar depends on the operator confirming the recorded author family (OpenAI/GPT, `operator_to_confirm`). Controller = Anthropic/`claude-opus-4.8` (confirmed). If unconfirmable cross-vendor, this is a same-vendor sanity / advisory result, not a no-new-seam discovery pass.
- **Scope of method:** static review + focused-test reproduction only. No live IG capture, no real-lake-at-scale data, no integration run. No readiness, merge-approval, or parity-complete claim is made.

## Review-Use Boundary

These findings are decision input only. They are not approval, validation, merge approval, mandatory remediation, or executor-ready patch authority until the Chief Architect / home model separately accepts or authorizes them. Severity labels (`major`/`minor`) are finding priority, not readiness verdicts. The CA/home model adjudicates what is kept.

---

```text
DELEGATED_CODE_REVIEW_RETURN_FOR_HOME_MODEL

Here is the delegated code review result. Adjudicate it under the
delegated-review-patch return contract.

- original commission: Adversarial implementation review of PR #441 "Add IG behavioral lake adapter"
  for behavioral completeness parity with the YouTube behavioral lane (not identical mechanics, not a
  shared-core refactor). Review-only; no patch authority commissioned.
- implementation context / diff / reviewed files: branch codex/ig-behavioral-lake-adapter @
  0265c0275bd30e7309f6ef53b287149c730058c9 (single commit). Diff vs origin/main (merge-base a79b9290):
  A source_capture/ig_reels_behavioral_lake.py (+379), A tests/unit/test_ig_reels_behavioral_lake.py
  (+140), M tests/contract/test_ig_reels_behavioral_projection_no_runtime_imports.py (+12/-4).
- findings + implementation evidence:
  - F-01 (major): ig_reels_behavioral_lake.py:110-113 swallows load_raw_packet failures (continue) with
    no residual; YouTube parity reference emits a fail-visible discovery_failed source/residual
    (youtube_behavioral_contract_from_merged_main_v0.md:87,94,126-134); IG projection already has the
    discovery_failed vocabulary (ig_reels_behavioral_projection.py:16-27) unused by the adapter.
  - F-02 (major): grid input path (ig_reels_behavioral_lake.py:145-159) is untested and its except:return
    swallows grid failures with no residual; SourceCapturePacket(**manifest) at line 147 round-trips today
    but is unverified.
  - F-03 (minor): lines 204-208 and 139-141 silently drop corrupt/unkeyable records (no false-complete).
  - F-04 (minor): line 147 uses **manifest vs the blessed model_validate (ig_projection.py:272).
  - F-05 (minor): lines 31-33 hardcode product-mention lane constants instead of importing canonical
    constants (transcript_product_lake.py:29-30).
- proposed patch / diff: none (review-only commission; advisory remediation direction only, in each finding's
  minimum_closure_condition).
- citations: see per-finding file:line references and the four parity contracts in docs/workflows/.
- reviewer verdict: patch_before_acceptance for the parity claim (F-01, F-02). The adapter is correct and
  well-tested on the happy path and introduces no false-completeness; the gap is failure-visibility parity
  and grid coverage. CA may instead accept F-01/F-02 as NAMED, DOCUMENTED residuals — but not as silent
  omissions (ig_backfix spec forbids silent omission).
- validation evidence + not-run: independently reproduced 91 passed (broader IG set incl. the 3 focused
  files) and 17/17 focused dots, 0 failures, @ 0265c027, Python 3.11.15. CI orca-harness-tests green:
  lane-reported, not re-run. Gaps: no test covers grid input, discovery-failure residuals, or corrupt-record
  handling.
- residual risk: de-correlation discovery bar contingent on operator confirming the recorded OpenAI/GPT
  author family; static + focused-test review only; no live capture / scale / integration.
- blockers / off-scope / not-proven: no patch authority in this commission; authored_by unrecorded (no
  model+version supplied); parity-complete / readiness / merge-approval NOT claimed.
```
