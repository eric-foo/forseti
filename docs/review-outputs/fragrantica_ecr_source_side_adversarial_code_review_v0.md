# Fragrantica ECR Source-Side Adversarial Code Review v0

```yaml
retrieval_header_version: 1
artifact_role: Review output (advisory implementation/code review)
scope: >
  Cross-vendor advisory implementation/code review of the Fragrantica
  source-side ECR structure and replayed data-lake materialization.
use_when:
  - Checking the adversarial review findings before Fragrantica ECR assumption-gate or Cleaning work.
  - Adjudicating whether the generic ECR sibling structure is acceptable for current Fragrantica packets.
authority_boundary: retrieval_only
commission: >
  Adversarial implementation/code review of the Fragrantica source-side ECR
  structure and the replayed data-lake materialization, before any Cleaning or
  assumption-gate work.
commission_prompt: docs/prompts/reviews/fragrantica_ecr_source_side_adversarial_code_review_prompt_v0.md
reviewed_by: claude-opus-4-8 (Anthropic)              # the model that performed this review; observed, not fabricated
authored_by: gpt-family-codex                          # per the commission de-correlation receipt (authoring lane)
de_correlation_bar: cross_vendor_discovery             # reviewer (Anthropic) != author (OpenAI/GPT) -> discovery bar satisfied
same_vendor_rationale: not_applicable                  # only required for same_vendor_sanity
review_authority: advisory_findings_only               # overlay granted no formal implementation-review authority to this prompt
reviewer_verdict: NOT_CLAIMED                          # no formal PASS/FAIL/readiness/acceptance
target_repo: C:\Users\vmon7\Desktop\projects\orca\worktrees\fragrantica-ecr-review-prompt
target_branch: codex/fragrantica-ecr-review-prompt
pinned_head: b2e0d638b903989713b69523d1dfe7c0ebb13202
observed_head: a3879a1a15f53ed77c92b31a1b2149e8dead6a94   # = pinned + one commit (the review prompt doc only); no ECR/Fragrantica source changed
source_context: SOURCE_CONTEXT_READY
data_lake: AVAILABLE (F:\orca-data-lake) -- direct record inspection performed, not author-summary substitution
```

---

## 1. De-Correlation Receipt (observed)

- **author_home_model_family:** OpenAI / GPT-family Codex (per the commission's Actor section).
- **controller_model_family:** Anthropic / Claude (this review). Different upstream vendor lineage from the author.
- **de_correlation_status:** `cross_vendor` — the discovery bar is satisfied (vendor = upstream model developer; Anthropic ≠ OpenAI, per `.agents/workflow-overlay/delegated-review-patch.md`). This review may therefore claim cross-vendor *discovery* strength.
- **Authority axis is separate from the de-correlation axis.** Cross-vendor discovery describes *who* reviewed, not *what authority* the review carries. The commission grants **findings-only advisory** authority (no formal implementation-review lane bound). So: discovery-grade de-correlation, advisory-grade authority, `reviewer_verdict: NOT_CLAIMED`.

---

## 2. Source Context Readiness

**Declared: `SOURCE_CONTEXT_READY`.**

- All commission-required Orca authority, ECR design authority, target implementation, Fragrantica producer context, validation evidence, and the replayed data-lake records were loaded. The external data lake at `F:\orca-data-lake` was **available**, so materialized records and frozen raw packets were inspected **directly** (the §"If the external data lake is unavailable" fallback did not trigger).
- **Benign pin delta (disclosed):** the prompt pins `b2e0d638`; the target worktree HEAD is `a3879a1a`. The single intervening commit is `a3879a1a docs: add Fragrantica ECR adversarial review prompt`, touching only the review prompt artifact itself (`git diff --name-only b2e0d638..a3879a1a` = the prompt file). No ECR or Fragrantica projection source file changed; the `stale_if` HEAD condition is technically tripped but materially benign — this is the prompt's anticipated "reviewing before it is merged" case. Working tree clean.
- **Sources read beyond the required-reads list (disclosed, with cause):**
  - `orca-harness/source_capture/models.py` — the ECR derivers bind these producer fields (`SourceCapturePacket`, `VisibleFact(Status)`, `CUTOFF_POSTURE_VALUES`, `archive_history_posture`, `PreservedFile`); required to judge the input boundary.
  - `orca-harness/data_lake/root.py` — `derive_ecr_into_lake` delegates all keying, path-containment, hashing, and completion-marker mechanics to `DataLakeRoot.{load_raw_packet, append_record_set, is_record_set_complete}`; the commission's path/bucket/record-id/hash/stale-record questions cannot be answered without it. This is lake mechanics, **not** Cleaning design (the §"do not widen into Cleaning" fence is respected).

---

## 3. Source-Read Ledger

| Source | How read | Supports |
|---|---|---|
| `orca-harness/ecr/models.py` (446 ln) | direct | posture schema, clear-conditions, receipt contract |
| `orca-harness/ecr/deriver.py` (367 ln) | direct | the four pure derivers (crux) |
| `orca-harness/ecr/lake.py` (93 ln) | direct | `derive_ecr_into_lake` materialization (crux) |
| `orca-harness/source_capture/models.py` | direct | input contract bound by derivers |
| `orca-harness/data_lake/root.py` | direct | keying / path-containment / hash / marker / re-derive mechanics |
| `orca-harness/runners/run_fragrantica_projection.py` | direct | projection entry boundary |
| `F:\...\930\...\manifest.json` (BR540 raw) | direct | raw input ground-truth (cutoff/archive/sha) |
| BR540 `ecr_set` + 4 posture records | direct | personal ground-truth of materialized output |
| Sauvage `ecr_set` + timing + source_visibility | direct | second independent ground-truth anchor |
| ECR design: frame+SP-6 plan, SP-1/2/3 plan, spine submap | direct | design intent for the two crux findings (verified vs primary) |
| `AGENTS.md`, overlay `README/source-loading/prompt-orchestration/review-lanes/delegated-review-patch/safety-rules` | via in-session gather-subagent synthesis (cited line refs spot-anchored) | verdict/output/authority/safety/non-claims bindings |
| All 6 packets: derived trees, `ecr_set` markers, 4 posture records each, projection records, raw manifests | via in-session extraction subagent; **cross-checked by my own direct reads on 2/6 (BR540, Sauvage) — exact match** | cross-packet honesty + sibling/keying/append-only |
| Fragrantica projection boundary + 10 test files | via in-session subagent (imports/grep + per-file inventory); **test suites independently rerun by me** | projection isolation + coverage gaps |

In-session subagent dispatches were **gather-and-summarize delegation** (read-only); load-bearing claims (INV-3 persistence, SP-6 grain, all clear/residual values for 2 packets, both test-suite pass counts) were re-verified by me against primary source / direct reads / direct test execution.

---

## 4. Executive Summary (bottom line)

**No blocker.** The generic ECR source-side posture set is the correct structure for Fragrantica capture packets, it is applied as integrity/provenance posture over the **raw** packet (never the projection), the residuals are honest and non-overclaiming, and the data-lake materialization is append-only, content-hash-marked, path-safe, and makes no downstream (EvidenceUnit / Cleaning / Judgment / readiness) claim. The replay is **sufficient to support "ECR structure is acceptable to review next"** and does **not** support assumption-gate, Cleaning, Judgment, buyer-proof, or live-capture-coverage claims.

Findings lead (5 total): **2 major** (both *latent / forward-looking*, with **zero current-data defect**) and **3 minor**. The two majors gate downstream durability and multi-source futures, not the current single-slice Fragrantica replay.

Independent revalidation: ECR suite **49 passed**, Fragrantica suite **10 passed** (both match author-reported; rerun by this reviewer at observed HEAD).

---

## 5. Findings (findings-first)

Severity is **priority only** (`blocker` / `major` / `minor`), not a formal Orca verdict.

### F-01 — SP-6 source-visibility is materialized per-packet **flat**, resolving the plan's `not_proven` grain refinement in code, with **no runtime guard** enforcing the single-source precondition that keeps the flat reduction honest — `major` (latent; no current-data defect)

- **Reviewed target / role:** SP-6 posture model + deriver (integrity posture).
- **Location:** `orca-harness/ecr/models.py:288-349` (`EcrSourceVisibilityPosture`, per-packet flat; docstring `:288-314` states it is "resolving the ratified field's `not_proven` vector-vs-flat refinement to *flat*"); `orca-harness/ecr/models.py:285` (`RESIDUAL_SLICE_DIVERGENT_VISIBILITY` declared but never emitted); `orca-harness/ecr/deriver.py:249-366` (`derive_source_visibility_postures` returns exactly one flat posture; reads packet-level `archive_history_posture` + first `archive_snapshot_body` slice + "any current body"; **no per-slice divergence pass, no slice-count guard**); `orca-harness/tests/test_ecr_lake_pilot.py` (`test_multi_slice_packet_preserves_slice_grain_for_per_slice_rows` asserts source_visibility yields one packet-grain entry — i.e. the flat behavior is *test-locked* for multi-slice input).
- **Evidence:** All 6 replayed packets are single-slice (`slice_01`), so flat == one-slice rollup → emitted value `current_capture_only` for all 6 (verified). For a multi-slice/multi-source packet the deriver would still emit one flat posture computed from packet-level inputs, and the per-slice no-hide residual would never fire.
- **Authority basis:** Frame plan §2.1 (`...frame_source_visibility_slice_architecture_plan_v0.md:156`): "evaluate **per relevant slice** → emit value-or-residual per slice → apply an **Ob.10 no-hide rollup**. Carry the per-slice vector; do **not** present a packet-flat single value." Rollup rule `:178`. **AF-3** (`:218`) rates a packet-flat enum a `major` consolidation-inconsistency. The flat-vs-vector shape is explicitly `not_proven` (`:283`). Per AF-7=B the owner ratified *the derivation contract (the 13-row spec) as the seed* — and that contract **includes** the Ob.10 rollup step (`:178`).
- **Impact:** Honesty of `source_visibility` for any future multi-source/multi-slice packet rests on an **unenforced precondition**. A divergent-visibility slice would be silently flattened (the exact failure the Ob.10 no-hide rollup exists to prevent), and an owner-reserved architecture refinement (flat vs vector) is resolved unilaterally in code. **No impact on the current Fragrantica replay** (single-slice).
- **Minimum closure condition:** One of — (a) add a fail-closed guard that residualizes (e.g. `RESIDUAL_SLICE_DIVERGENT_VISIBILITY`) or raises when a packet presents more than one visibility-relevant source slice, so the flat reduction can never silently hide divergence; (b) implement the per-slice vector + Ob.10 rollup; or (c) obtain and record explicit owner ratification of the flat shape (the plan left it `not_proven`).
- **Next authorized action:** Home model adjudicates; because flat-vs-vector is an owner-reserved refinement, route the chosen closure to the owner before multi-source onboarding, assumption-gate, or Cleaning.
- **Verification expectation:** A test that feeds a multi-slice packet with *divergent* per-slice visibility through `derive_source_visibility_postures` and asserts a no-hide residual (currently absent; existing multi-slice test only checks grain/count). Red-green: such a test would fail against the current flat deriver and pass once a guard/rollup lands.

### F-02 — No automated test exercises a real Fragrantica-shaped packet through the ECR derivers or `derive_ecr_into_lake`; the "ECR over Fragrantica" path is regression-unguarded (backed only by the one-time manual replay) — `major` (no current-correctness defect)

- **Reviewed target / role:** ECR test suite coverage vs the Fragrantica commission.
- **Location:** `orca-harness/tests/unit/test_ecr_identity_deriver.py`, `..._inspectability_deriver.py`, `..._timing_deriver.py`, `..._source_visibility_deriver.py`, `..._source_side_composition.py`, `orca-harness/tests/test_ecr_lake_pilot.py` — all use `source_family="reddit"` / `"test_family"` synthetic packets (`_ecr_builders.py` / local helpers). Fragrantica-shaped fixtures exist **only** in `tests/unit/test_fragrantica_projection.py` and `tests/test_fragrantica_projection_lake_pilot.py`, which never invoke any ECR code.
- **Evidence:** No test constructs `source_family="fragrance_native_database"` / `source_surface="fragrantica_product_page_direct_http"` and runs it through ECR. The realistic Fragrantica profile (`cutoff_posture=unknown_with_reason`, `archive_history_posture=not_attempted`, 2-file slice → all-residual timing + resolved identity + verifiable inspectability + `current_capture_only`) is exercised end-to-end only by the manual replay (the 6 on-disk record sets), not by any test.
- **Authority basis:** Commission review-scope question: "Do tests cover the Fragrantica raw-packet shape through the generic ECR derivers, not only generic fixtures detached from real Fragrantica packet structure?" `workflow-code-review` findings standard (validation evidence).
- **Impact:** The claim "ECR structure acceptable to review next *for Fragrantica*" rests on a manual artifact, not a regression guard. **Mitigants (material):** the derivers are genuinely producer-agnostic (they branch on field *values/statuses*, never on `source_family`), and each Fragrantica-triggered behavior *is* unit-tested with generic fixtures (timing `unknown_with_reason`→residual; `current_capture_only` non-clearing; identity `resolved`; inspectability `inspectable_verifiable`). So this is a durability/regression-guard gap, not a current defect — a future deriver change could regress Fragrantica handling with no failing test.
- **Minimum closure condition:** A lake-level test that commits a Fragrantica-shaped packet and runs `derive_ecr_into_lake`, asserting the expected posture profile (all-residual timing, resolved identity, verifiable inspectability, `current_capture_only` non-clearing) and 4-sibling marker integrity.
- **Next authorized action:** Home model adjudicates; the test addition is implementation work requiring separate bounded authorization (not this read-only review's to write).
- **Verification expectation:** Red-green — the new Fragrantica-through-ECR test passes at current HEAD and would fail under a deriver regression that mishandled the Fragrantica field profile.

### F-03 — The lake **persists** ECR records, in literal tension with the frame plan's INV-3 "derived, non-persisted" / AF-2 "block any proposal to persist SP-6 to … an ECR record"; reconciled only by the submap's invariant-4, which is not cited at the materialization boundary — `minor` (doctrine-traceability; no correctness impact)

- **Reviewed target / role:** lake materialization vs ECR frame doctrine.
- **Location:** `orca-harness/ecr/lake.py:54-89` (`derive_ecr_into_lake` writes `ecr_<kind>` records + an `ecr_set` marker). The module docstring cites `safety-rules.md` but not the authorizing *persistence* doctrine.
- **Evidence / authority basis:** Frame plan **INV-3** (`:101`): "ECR fields are derived projections, **not stored columns**"; §2.1 (`:153`): "derived, **non-persisted**"; **AF-2** closure (`:217`): "Block any proposal to persist SP-6 to a packet **or ECR record**." This is **reconciled** by the spine submap **invariant-4** (`ecr_spine_submap_v0.md:47`): "Derived / re-derivable — re-derive, never migrate. These are M2-style derived reads over the still-frozen raw observable, **not persisted-at-capture columns**" — i.e. the operative current doctrine reframes "non-persisted" to "re-derivable, not a *capture-time* column," and the submap names the whole thing the "derived-**record** spine."
- **Impact:** The implementation's *behavior* is consistent with invariant-4 — it honors re-derive-never-migrate (re-derive = fresh `record_id`, `lake.py:73`), is create-only/no-overwrite (`root.py` append_record_set preflight, `:624-629`), never mutates raw (`load_raw_packet` is read-only), and adds no column to `SourceCapturePacket`. The gap is **auditability**: a reviewer reconciling the lake records against the frame plan's literal "non-persisted / or ECR record" wording sees an apparent INV-3/AF-2 violation, because the authorizing doctrine (the data-lake mechanics map / submap invariant-4) is not cited where ECR is materialized. There is **no runtime/correctness defect**; do not read this as "the code violates INV-3."
- **Minimum closure condition:** Cite the authorizing persistence doctrine (data-lake mechanics map and/or submap invariant-4) at the `lake.py` boundary, and/or reconcile the advisory frame plan's stale "non-persisted / or ECR record" wording so the persisted-but-re-derivable record model is unambiguous.
- **Next authorized action:** Home model adjudicates; doc/citation reconciliation is owner/lane-doc work, not a code change.
- **Verification expectation:** N/A (documentation/traceability).

### F-04 — Append-only re-derive accumulates multiple derived record sets per packet with no recorded selection/supersession policy; downstream consumers must choose the authoritative set — `minor` (residual / forward risk)

- **Reviewed target / role:** lake re-derive semantics vs downstream consumption.
- **Location:** `orca-harness/ecr/lake.py:73` (re-derive = new `record_id`); `orca-harness/data_lake/root.py:577-653` (`append_record_set`), `:655-691` (`is_record_set_complete`), `:762-771` (`lane_dir`) — iteration + completeness checks exist, but **no "latest/current/authoritative" selection**.
- **Evidence:** Observed across **all 6** packets: the `projection_fragrantica` lane already holds **two** records (an older `01KW7Y…` and a newer `01KW99H…`); notably the older projection records are *less honest* (missing the three `fragrance_*_present_but_not_projected` residuals the newer ones added). ECR currently has one set per packet, but the design permits N.
- **Authority basis:** Submap invariant-4 (re-derive-never-migrate — correct for integrity); commission scope ("hidden … stale-record risks").
- **Impact:** Append-only is correct and intentional for source-side integrity, but it pushes set-selection downstream with no recorded convention. When EvidenceUnit binding / JSG-01 / Cleaning later consume ECR (or projection) records, "which complete set is authoritative" is undefined — and picking the wrong projection generation yields a less-complete residual ledger. Not a blocker for "acceptable to review next."
- **Minimum closure condition:** A recorded downstream selection/supersession convention (e.g. latest-by-`record_id`, or an explicit current pointer) before any consumer binds these records.
- **Next authorized action:** Home model records this as a downstream precondition; no source-side change required now.
- **Verification expectation:** A selection test when the downstream policy is authored.

### F-05 — Archive-slice identification keys on a free-string `slice_id` convention the producer schema does not enforce; a deviating producer would be silently misclassified — `minor` (latent; moot for Fragrantica)

- **Reviewed target / role:** SP-6 deriver archive detection.
- **Location:** `orca-harness/ecr/deriver.py:212-229` (`_ARCHIVE_SLICE_IDS = {"archive_snapshot_body","archive_availability"}`, `_archive_body_slice`, `_has_current_body`); `orca-harness/source_capture/models.py:202` (`slice_id` is a free `str`).
- **Evidence / authority basis:** Frame plan §2.3 (`:187`) flags the archive-date input as an "**Implemented convention, not a contracted field** (top delta-sensitivity)"; the code comment (`deriver.py:209-211`) acknowledges it.
- **Impact:** For Fragrantica this is **moot** — packets have a single non-archive `slice_01`, so `current_capture_only` is correct. Latent: a future archive-capable producer using different archive `slice_id`s would silently misclassify `source_visibility`.
- **Minimum closure condition:** When archive-mode producers are onboarded, contract the archive `slice_id` (closed token) or key archive detection on a contracted field rather than a `slice_id` string.
- **Next authorized action:** Note for the archive-producer lane; no Fragrantica-side change needed now.
- **Verification expectation:** N/A for the Fragrantica replay.

---

## 6. Commission Questions — Answers (confirmations)

Each is answered against directly-inspected evidence.

1. **Generic posture set fits Fragrantica without a Fragrantica-specific schema?** **Yes.** The derivers read only generic `SourceCapturePacket` fields and never branch on `source_family`; subagent-A synthesis of the design authority confirms no Fragrantica-specific ECR schema is designed or authorized. A Fragrantica packet is just a generic `SourceCapturePacket`.
2. **ECR kept as integrity/provenance posture, not content extraction / review-sentiment?** **Yes.** Postures derive from provenance fields (`source_family/surface/locator`, `PreservedFile.sha256`, `cutoff_posture`, `archive_history_posture`); no body content, review text, accords, notes, or ratings are read by any ECR path.
3. **Projection outputs and ECR postures true siblings under the same raw key?** **Yes.** Both write `derived/<anchor_shard>/<raw_anchor>/<lane>/…` with `raw_anchor = packet_id`. Verified on disk for all 6 (and personally for BR540 + Sauvage): `ecr_identity/inspectability/timing/source_visibility/ecr_set` + `projection_fragrantica` are co-located under the same raw packet directory; ECR and projection `record_id`s differ; not merged.
4. **Any code path using projection rows / review text / accords / notes / similarity / Cleaning content to satisfy ECR fields?** **No — structurally impossible.** `derive_ecr_into_lake` reads the raw packet via `load_raw_packet`; ECR modules contain **zero** `import` of `fragrantica_projection`, and the projection contains **zero** `import` of `ecr`. Accords / notes-pyramid / similarity appear only as projection-side residual strings (`fragrance_*_present_but_not_projected`), never as ECR inputs or clearance blockers.
5. **Timing & source-visibility residuals honest, or overclaiming freshness/archive/completeness/finality/readiness?** **Honest.** All 6: `ecr_timing` = `unknown_with_reason` residual, `clears_pre_cutoff=false` (carrying each packet's verbatim `cutoff_posture.reason` — M3 fidelity, no coining); `ecr_source_visibility` = `current_capture_only`, `clears_source_visibility=false` (no archive coverage claimed). Nothing clears freshness/archive/finality. Identity (`resolved`) and inspectability (`inspectable_verifiable`) clear, and both are supported by raw fields (source fully known; bytes preserved with real 64-hex sha256 **re-hashed and verified** by `load_raw_packet:876-881`).
6. **Materialization append-only with hashes + member refs, no raw mutation, no overwrite of prior projections?** **Yes.** `append_record_set` is create-only (`_atomic_create`, `os.link` no-overwrite / `O_EXCL` fallback), computes `member_sha256` from the bytes the lake itself writes (`root.py:632-639` — integrity-by-construction), and writes the `ecr_set` marker (`{record_id, member_lanes[4], member_sha256{4}}`) last. Raw is never mutated (`load_raw_packet` read-only). Prior projections are preserved (two generations coexist for every packet).
7. **Tests cover the Fragrantica raw-packet shape through the generic ECR derivers?** **No — see F-02.** ECR tests use generic Reddit/`test_family` fixtures; the Fragrantica-through-ECR path is covered only by the manual replay. (Behaviors are individually tested; the Fragrantica combination/integration is not.)
8. **Replay enough for "ECR structure acceptable to review next" but not downstream claims?** **Yes.** Structure is sound and honest; the implementation makes no EvidenceUnit/Cleaning/Judgment/SP-5/readiness/assumption-gate claim (`lake.py` boundary docstring; no such code; safety-rules separate-gates honored). The replay supports reviewability only — F-01/F-02 gate multi-source futures and regression durability; F-04 gates downstream binding.
9. **Hidden path-containment / Windows-path / bucket-key / record-id / hash / stale-record risks in `derive_ecr_into_lake`?** **Well-guarded**, with one residual. `record_id=f"{record}.json"` and all lane/anchor segments pass `_validate_segment` (rejects `.`/`..`/unsafe, `root.py:142-145`); `_within` resolves + asserts containment + rejects symlinks (`:493-506`); `packet_id` is Crockford-26 `fullmatch` (`:134-139`); shard is recomputed from the key, never stored (`:91-98`); a colliding explicit `record_id` fails closed before any write (`:624-629`); preserved-file paths are traversal-checked and byte-re-hashed (`:323-342`, `:842-881`). The **stale-record** item is the F-04 multi-set selection residual.

---

## 7. Open Questions & Residual Risk

- **R-1 (→F-01):** Is the flat SP-6 shape an owner-accepted resolution of the `not_proven` refinement, or an implicit one? The plan reserves it to the owner; no ratification record was found in the reviewed sources.
- **R-2 (→F-03):** The data-lake mechanics map (`core_spine_v0_data_lake_mechanics_map_v0.md`, referenced by the submap) was **not** read (out of the commission's read fence). It is the most likely home of the explicit "ECR records persist in the lake" authority; confirming it would fully close the INV-3 traceability tension.
- **R-3 (→F-04):** No downstream consumer of ECR/projection records was in scope; the multi-set selection risk is asserted from the lake API surface + the observed two-generation projection lanes, not from a consumer.
- **R-4 (SP-2 chain, low):** `derive_inspectability_postures` does not itself read `hash_basis`; `inspectable_verifiable` rests on (a) `PreservedFile.hash_basis` being a required closed token by schema and (b) `load_raw_packet`'s byte re-hash. This holds in the `derive_ecr_into_lake` path (always model-validated + lake-verified). It would not hold if the deriver were ever run on an unvalidated packet outside the lake path — verified-consistent today, noted as a path-dependency.
- **R-5:** Reproducibility of the materialized bytes (re-derive → identical `member_sha256`) was **not** re-executed — the commission forbids replaying ECR. It is implied by deterministic `_record_bytes` (`sort_keys=True`) but not independently proven this turn.

---

## 8. Validation Evidence Inspected & Not-Run Gaps

- **Independently revalidated (rerun by this reviewer at observed HEAD `a3879a1a`, `DataLakeRoot.for_test` tmp dirs only):**
  - ECR suite (`test_ecr_lake_pilot` + 4 unit deriver suites) → **49 passed** (matches author-reported).
  - Fragrantica suite (`test_fragrantica_projection` + cleaning-integration + projection-lake-pilot) → **10 passed** (matches author-reported).
  - The static test-*function* inventory (~46 across the 5 ECR files) is consistent with `49 passed` once pytest parametrization is counted — **no discrepancy asserted.**
- **Directly inspected materialized evidence:** all 6 `ecr_set` markers (4 member lanes + 4 `member_sha256` each), all 6 four-posture record sets, all 6 raw manifests, all 6 projection lanes (two generations each). BR540 (5 files + raw manifest) and Sauvage (3 files) read personally; the other four corroborated via the extraction subagent — my 2/6 personal reads matched the subagent byte-for-byte.
- **Not run / not proven:** ECR re-derivation reproducibility (forbidden by commission); any consumer-side binding behavior (out of scope); the full ECR test set beyond the two reported commands (e.g. `test_ecr_models.py`, `test_ecr_source_side_composition.py`) was inventoried but not separately rerun; the data-lake mechanics map was not read (R-2).

---

## 9. Review-Use Boundary & Non-Claims

These findings are **decision input only** — not approval, not validation, not readiness, not assumption-gate clearance, not mandatory remediation, and not executor-ready patch authority — until separately accepted or authorized by the appropriate Orca lane. This review:

- emits **no** formal PASS/FAIL/blocked/ready verdict (`reviewer_verdict: NOT_CLAIMED`);
- emits **no** `patch_queue_entry` and proposes no edits (read-only reviewer);
- performed **no** commit/push/PR, **no** live capture, **no** projection replay, **no** ECR replay, and started **no** Cleaning;
- does **not** assert EvidenceUnit binding, JSG-01/Judgment readiness, Cleaning readiness, buyer proof, live-capture coverage, or assumption-gate clearance.

`severity` labels (`blocker`/`major`/`minor`) are prioritization aids, not Orca verdict authority. Cross-vendor *discovery*-grade de-correlation describes reviewer independence, not granted review authority (which remains advisory).
