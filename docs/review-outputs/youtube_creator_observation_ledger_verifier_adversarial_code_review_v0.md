---
retrieval_header_version: 1
artifact_role: Orca adversarial implementation/code review report (decision input; read-only)
scope: >
  Read-only de-correlated adversarial implementation/code review of the YouTube
  creator observation ledger verifier hardening commit at diff
  77f0ade5..5295778e (new reusable verifier package + hardened unit tests + spec
  and propagation-doc updates). Findings are decision input only; not approval,
  validation, readiness, or patch authority.
use_when:
  - Deciding whether the verifier/test hardening commit catches the material
    false-success and scope-drift risks before the YouTube creator observation
    ledger is relied on as a static source-backed creator observation substrate.
  - Checking which of the four intended hardening goals (H-01..H-04) are closed,
    partially closed, or not closed, with evidence.
authority_boundary: retrieval_only
review_type: adversarial_implementation_code_review
output_mode: review-report
edit_permission: read-only
target_branch: codex/creator-ledger-static-fixture
target_base_commit: 77f0ade583b84acfd300385fa02037364508b74f
target_implementation_commit: 5295778eb024a3ba5ffe280df163a4c555390b52
commission_prompt: docs/prompts/reviews/youtube_creator_observation_ledger_verifier_adversarial_code_review_prompt_v0.md
authored_by: gpt-family-codex (OpenAI lineage)
reviewed_by: claude-opus-4-8 (Anthropic lineage)
de_correlation_bar: cross_vendor_discovery
recommendation: advisory_findings__hardening_partially_closed__3_major_3_minor
---

# YouTube Creator Observation Ledger Verifier — Adversarial Implementation/Code Review v0

> **Decision input only.** This review is read-only advisory critique. It is
> **not** approval, validation, readiness, a formal PASS, mandatory remediation,
> or executor-ready patch authority. Severity labels (`blocker`/`major`/`minor`)
> are **finding priority only**, not an Orca formal-verdict authority. The
> commissioning CA adjudicates what (if anything) to act on. No source file was
> edited; the only write is this durable report.

## Commission / Provenance Receipt

- **Commission:** `docs/prompts/reviews/youtube_creator_observation_ledger_verifier_adversarial_code_review_prompt_v0.md` — a filed `workflow-delegated-review-patch` route-out that, because the target is a **multi-file implementation/code packet**, is correctly routed to **read-only implementation/code review** (per `.agents/workflow-overlay/delegated-review-patch.md`: a multi-file code diff is not stretched into the single-target patch convention). No patch authored.
- **Target range:** `77f0ade5..5295778e` on `codex/creator-ledger-static-fixture`. Worktree HEAD is `aa991ff1` (a later **prompt-only** commit that adds only the commission prompt, +370 lines). I verified the seven target files are **byte-identical** between `5295778e` and HEAD (`git diff 5295778e..HEAD -- <targets>` empty), so the implementation surface still equals the pinned `5295778e`. Worktree clean. **No `stale_if` trip.**
- **Authority (read-only):** no patch authority, no working-tree source edits, no `patch_queue_entry`, no runtime-model recommendation, no validation/readiness/approval/no-new-seam claim. Findings-first advisory review (`workflow-code-review` zero-config semantics; no Orca formal implementation-review lane was bound by the commission).
- **`authored_by`:** `gpt-family-codex` (OpenAI lineage) — from the commission's actor receipt.
- **`reviewed_by`:** `claude-opus-4-8` (Anthropic lineage) — reviewer self-disclosed (the model+version that performed this review; the commission left it `operator_to_fill`). Factual, not fabricated; operator/CA may confirm on the durable record. Not a runtime-model recommendation, ranking, or selection.
- **`de_correlation_bar`:** `cross_vendor_discovery` — factual who-descriptor (author vendor OpenAI ≠ reviewer vendor Anthropic; both lineages disclosed) and full-diff discovery was performed. **Caveat:** this is a read-only *advisory* lane; it asserts **no** no-new-seam / PASS / readiness / validation standard regardless of the bar. The bar records who ran it, not a strict outcome.

## Source Context Status — `SOURCE_CONTEXT_READY`

**Method sequence (Source-Gated Method Contract).** (1) REFERENCE-LOADed `workflow-deep-thinking` and `workflow-code-review` (both available in this runtime; not applied before readiness). (2) Read the required Orca authority + target + context sources. (3) Declaring readiness here. (4) Applied deep-thinking to frame failure modes, then `workflow-code-review` findings-first semantics. (5) `workflow-code-review` was available, so strict-claim suppression is by the **commission's advisory scope**, not by tool unavailability.

**Source-read ledger:**

| Source | Read | Note |
| --- | --- | --- |
| `AGENTS.md` | full (session-resident copy; target branch head `b79f2c39`) | behavior kernel, smallest-complete, decision priority |
| `.agents/workflow-overlay/README.md`, `review-lanes.md`, `delegated-review-patch.md`, `safety-rules.md` | full | review lane boundary, output destination, de-correlation, read-only/no-network |
| `.agents/workflow-overlay/validation-gates.md` | binding-scope (targeted grep on review/validation-claim gates) | confirmed advisory work supported; strict PASS/readiness require binding; findings-first |
| `.agents/workflow-overlay/source-loading.md`, `prompt-orchestration.md` | binding-scope only (consumed via the commission's preflight: `source_pack: custom`, all listed sources read) | govern source-pack selection / prompt authoring — activities the commission already performed; **not** full-body read (disclosed, not claimed) |
| `orca-harness/capture_spine/youtube_creator_observation/validation.py` | full (431 lines) | **primary review object** |
| `orca-harness/capture_spine/youtube_creator_observation/__init__.py` | full | re-export surface |
| `orca-harness/tests/unit/test_youtube_creator_observation_ledger.py` | full | hardened tests |
| `orca-harness/capture_spine/creator_public_handle_linkage/validation.py` | full | `assert_no_forbidden_output_fields` (imported guard) |
| `.../youtube/youtube_creator_observation_ledger_spec_v0.md` | full | contract under review |
| `.../youtube/youtube_shorts_fragrance_creator_observation_ledger_v0.json` | structural + targeted (5,414 lines) | the seed ledger; sub-object shapes inspected |
| `docs/review-inputs/youtube_shorts_fragrance_creator_ledger_v0.json` | structural (1,893 lines) | rebuild source-of-truth; confirmed test loads it (non-circular) |
| `docs/workflows/orca_repo_map_v0.md`, `data_capture_spine_consolidation_map_v0.md`, `source_capture_toolbox/README.md` | diff-scope | propagation/overclaim check |

**Conflicts / unavailable tools / target drift:** none blocking. No live data lake (`F:\orca-data-lake`) available to this reviewer, so the live-lake reconciliation path was **not** independently exercised (see Validation Status). No network, live capture, installs, DB writes, or external calls performed.

---

## Calibration (read before severity)

The commit is **substantively solid engineering** for the current census. The verifier applies closed allow-lists at every named structural level, recomputes all `counts` from the observations, detects duplicate observation/video/packet ids, enforces 1:1 packet↔video alignment and packet→channel consistency, performs a **real, non-circular** source-rebuild against the committed source ledger (I proved it catches a drifted compared field), and offers an optional live-lake reconciliation. The propagation docs are **conservative and do not overclaim readiness**. My portable test rerun reproduced the author's result exactly.

The findings below are therefore about (a) the verifier's **guarantee against adversarial/future ledgers** and (b) **negative-test coverage of the hardening guards** — both directly in scope because the artifact is explicitly positioned as a trustworthy reusable substrate and the commission asks me to attack false-confidence and boundary preservation. All `major` findings are **partially-closed-hardening** issues, not "the committed fixture is wrong" issues.

---

## Findings (findings-first)

### F-01 — `major` — Nested-field smuggling bypasses the cross-platform / transcript / metric boundary the ledger most loudly disclaims

- **Target:** `orca-harness/capture_spine/youtube_creator_observation/validation.py` — `_validate_observations` (lines ~257-283) applies `_reject_unknown_keys` / `_require` only to the observation **top level**; observation-level `identity_boundary` and `niche_scope` (allow-listed at lines 64, 73) are **never content-validated** (only `wrapper["niche_scope"]` is, line 138). The closed allow-list is **non-recursive** into allowed sub-objects. The backstop `assert_no_forbidden_output_fields` (`creator_public_handle_linkage/validation.py` lines 235-249, denylist 117-169) recurses but its `_FORBIDDEN_OUTPUT_FIELDS` set **omits** cross-platform-handle names (`tiktok_*`, `instagram_*`, …) and transcript-body names (`transcript_body`, `transcript_text`, `caption_text`).
- **Evidence (reviewer probe, portable, in-memory mutation of the committed fixture):**
  - Control A: `tiktok_public_handle` at observation **top level** → `[REJECT unknown_field]` ✓ (closed allow-list works at the top level).
  - Control B: `{"email": …}` nested under `identity_boundary` → `[REJECT forbidden_output_field]` ✓ (denylist works for **listed** names, recursively).
  - **GAP1:** `identity_boundary = {"tiktok_public_handle": "@same", "instagram_url": "https://…"}` → `[ACCEPT]` under both `validate_youtube_creator_observation_ledger` **and** `validate_source_rebuild`.
  - **GAP2:** `niche_scope = {"label": "fragrance", "transcript_body": "copied transcript …"}` → `[ACCEPT]` (base validate).
  - **GAP3:** `identity_boundary = {"average_views": 12345, "engagement_rate": 0.07}` → `[ACCEPT]` (base validate).
- **Authority basis:** spec lines 130-132 ("transcript bodies are not copied into the ledger"; "per-video metrics are not smuggled"); spec Non-Claims (cross-platform identity linkage); ledger `non_claims`; boundary test `test_..._boundaries` (lines 98-109) asserts only **top-level** absence (`"transcript_body" not in observation`).
- **Impact:** the three boundary classes the artifact disclaims most loudly can be carried in a hand-edited or future ledger while the **primary gate returns success** — false boundary confidence for any downstream consumer that reads "verifier passed" as "boundary held." `identity_boundary`/`niche_scope` are the cleanest vectors because source-rebuild never compares them (GAP1 passes rebuild too).
- **minimum_closure_condition:** the verifier rejects cross-platform-handle / transcript-body / metric fields **wherever they appear**, via any of: (a) closed allow-list/type validation of `identity_boundary` and `niche_scope` (and the other allowed sub-objects), (b) recursive application of the closed allow-list, or (c) extension of the recursive denylist to those name classes — **and** a negative test pins it.
- **next_authorized_action:** CA decision — request a bounded verifier-hardening patch authorization, **or** accept as a documented residual and soften the docs from "the verifier guarantees no cross-platform/transcript/metric" to "the committed fixture has none; the verifier enforces this at the top structural level."
- **verification_expectation:** red-green — a nested-smuggle test expects a reject code; it fails against `5295778e` (proven: ACCEPT today) and passes after the fix.

### F-02 — `major` — Source-rebuild does not bind the primary channel identity and does not enforce the declared source `sha256`

- **Target:** `validation.py` `validate_source_rebuild` (lines 146-187) compares ~16 source-owned fields but **not** `platform_subject_key` (the row's primary YouTube channel id) or `public_profile_url`. `source_inputs[].sha256` (allow-listed line 53; present in the fixture, e.g. `abc788fa…`, `e1d74fe1…`) is **never read or verified** against file bytes. `_source_root_uuid` (lines 375-379) is consulted only in the **optional** live-lake path.
- **Evidence (reviewer probe):**
  - **GAP5:** fabricated `platform_subject_key = "UC0000…FAKE"` (kept internally consistent with packet-ref channels + recomputed `resolved_lake_channel_ids`) → `[ACCEPT]` under base validate **and** source-rebuild.
  - **GAP4:** `source_inputs[0].sha256 = "0"*64` → `[ACCEPT]` under base validate **and** source-rebuild.
  - Positive control: drifted `creator_handle_query = "DRIFTED"` → source-rebuild `[REJECT source_rebuild_mismatch]`, base-validate `[ACCEPT]` — confirming rebuild **does** bind the fields it compares, and base-validate alone is not a source gate.
- **Authority basis:** spec "Source Requirements" (a row needs "at least one stable YouTube channel id"); the presence of a `sha256` field implies a source pin; H-02 ("source-owned fields can be rebuilt … and compared").
- **Impact:** in **portable mode** (the default and CI mode — live-lake is skipped), the row's most identity-critical field (its primary subject channel) and its public URL are **not** bound to the source ledger; a wrong/fabricated channel id passes. The declared `sha256` is decorative, so a swapped source file is caught only field-by-field for the compared fields, and **not at all** for uncompared ones. This narrows H-02 from "source rebuild" to "partial source rebuild."
- **minimum_closure_condition:** bind `platform_subject_key` (and `public_profile_url`) to a source field or to `source_observed_channel_ids` membership; **either** enforce `sha256` against the source bytes **or** drop the field so it stops implying an unenforced pin; negative tests for both.
- **next_authorized_action:** CA decision / bounded patch-authorization request.
- **verification_expectation:** red-green — fabricated-subject-key and corrupted-sha tests fail post-fix-design pre-fix (proven ACCEPT today).

### F-03 — `major` — The hardening commit lacks negative tests for its own headline guards

- **Target:** `orca-harness/tests/unit/test_youtube_creator_observation_ledger.py`. Negative tests exist only for `duplicate_video_id_in_row` (130-136), `packet_ref_count_mismatch` (139-144), `packet_ref_channel_mismatch` (147-152), and three `unknown_field` top-level smuggles (155-173). **No** test exercises: `source_rebuild_mismatch` (drift), any live-lake reconciliation failure, `duplicate_creator_observation_id`, `duplicate_video_id_across_ledger`, `duplicate_packet_id_across_ledger`, `packet_ref_video_alignment`, `invalid_packet_id` / `invalid_packet_relpath`, `admitted_count_mismatch`, `invalid_metric_rollup_status` / `metric_absence_zero_forbidden`, or the nested smuggling in F-01.
- **Evidence:** enumerated test functions (the file's full test set); to demonstrate that `validate_source_rebuild` actually catches drift I had to supply the missing red case in my probe — the **suite never does**. The only rebuild test (`test_..._rebuilds_from_source`, 112-113) is positive-only, so a refactor that silently no-op'd `validate_source_rebuild` (or the live-lake recon) would leave the suite green.
- **Authority basis:** commit subject "test: harden youtube creator observation ledger"; H-01/H-02/H-03 are stated hardening claims; `workflow-code-review` red-green proof expectation; review-lanes red-green preference. A guard not pinned by a failing-without-it test is unproven against regression.
- **Impact:** for a commit whose stated purpose is hardening against false success, the **negative-coverage gap is the load-bearing risk** — the guards are present but not regression-pinned, and the most consequential ones (source-rebuild, live-lake, cross-ledger duplicate/alignment) have zero red coverage.
- **minimum_closure_condition:** add red-green negative tests for at least the source-rebuild drift path, the cross-ledger duplicate + packet-alignment paths, the metric-policy violations, and a marked/xfail live-lake failure case.
- **next_authorized_action:** CA decision / bounded patch-authorization request (test-only).
- **verification_expectation:** each added test must fail against `5295778e` behavior for the failure mode it covers, then pass.

### F-04 — `minor` — Live-lake reconciliation is optional, unreproduced, and misreports its failure domain; `metadata_relpath` is unvalidated

- **Target:** `validation.py` `validate_youtube_creator_observation_ledger_against_live_lake` (190-219); test gates on `ORCA_DATA_ROOT` and **skips** when unset (116-121); `_assert_equal` emits the generic code `source_rebuild_mismatch` for **live-lake** field mismatches (218-219 → 420-422); `metadata_relpath` is `_require`d but — unlike `packet_relpath` (regex `_RAW_RELPATH_RE`, line 308) — **never format-validated**, then used as `root / ref["metadata_relpath"]` (208).
- **Evidence:** my portable rerun shows this test **skipped** (`1 skipped`); the author-supplied live run (`32 passed`) was **not** independently revalidated (no lake; not fabricated). Code read shows the shared error code and the missing relpath validation.
- **Impact:** H-03 is positive-only and environment-dependent; a live-lake channel/video mismatch is reported as `source_rebuild_mismatch`, mis-routing a lake-recon defect to a source-rebuild diagnosis (answers the commission's "non-silent failures / error messages too broad" question: the **codes** are too coarse here even though messages differ); the unvalidated `metadata_relpath` is a weak (read-only, local) path-format gap.
- **minimum_closure_condition:** distinct error codes for live-lake mismatches; validate `metadata_relpath` format; add a marked live-lake negative case or no-lake stub.
- **next_authorized_action:** advisory; CA may fold into the F-03 test pass.
- **verification_expectation:** live-lake positive path **not independently revalidated** by this reviewer (author-supplied).

### F-05 — `minor` — Forbidden-field rejection raises a different exception type than the verifier's own errors

- **Target:** `validation.py` imports `assert_no_forbidden_output_fields` from the linkage module, which raises **`CreatorPublicHandleLinkageError`**; every other rejection in this verifier raises **`YoutubeCreatorObservationLedgerError`**. The test helper `_raises_code` (124-127) catches only the latter.
- **Evidence:** probe Control B surfaced `CreatorPublicHandleLinkageError:forbidden_output_field` (initially uncaught by a handler expecting the YouTube error type).
- **Impact:** a caller or future test that catches only `YoutubeCreatorObservationLedgerError` will **not** catch a forbidden-field rejection — a latent error-handling / test-robustness inconsistency. The current boundary test avoids it by calling `assert_no_forbidden_output_fields` directly, so the suite is green, but the cross-module type leak is real.
- **minimum_closure_condition:** translate/wrap forbidden-field rejections into `YoutubeCreatorObservationLedgerError` (or document the dual type and broaden callers/tests).
- **next_authorized_action:** advisory.
- **verification_expectation:** a test asserting the verifier's single error type on a forbidden-field input.

### F-06 — `minor` — Verifier enforces only 2 of the ledger's 11 `non_claims`; spec describes branches the verifier does not implement

- **Target:** `validation.py` `_validate_required_non_claims` (412-417) requires only `"not cross-platform identity linkage"` + `"not metric rollup"`. The spec's "Source Requirements" (lines 124-132) describe an "explicitly marked unresolved" channel branch and an "explicit missing-packet residual" branch that the verifier does **not** implement (it requires a `UC`-prefixed `platform_subject_key`, line 272, and strict 1:1 packet alignment, line 295).
- **Evidence:** probe GAP6 (`non_claims` reduced to the two enforced strings) → `[ACCEPT]`; code paths show no unresolved/missing-packet handling.
- **Impact:** minor — the two enforced `non_claims` are the load-bearing ones and the boundary test asserts four against the fixture; the rest are declarative. The unimplemented spec branches make the verifier **stricter than spec in the safe direction**, but the spec/impl divergence will mislead whoever next adds an unresolved or missing-packet row.
- **minimum_closure_condition:** either enforce the fuller `non_claims` set the ledger declares (or explicitly mark them declarative), and reconcile the spec's unresolved / missing-packet language with the verifier (implement, or annotate "not yet supported").
- **next_authorized_action:** advisory.
- **verification_expectation:** n/a (documentation/contract reconciliation) unless enforcement is added, then a red-green `non_claims` test.

---

## Intended Hardening Closure Check (H-01..H-04)

| ID | Goal | Status | Evidence / residual |
| --- | --- | --- | --- |
| **H-01** | Portable verifier validates without live lake and rejects known false-success patterns | **partially_closed** | Portable operation + strong top-level rejection confirmed (my rerun: `31 passed, 1 skipped`; closed allow-lists, recomputed counts, duplicate/alignment/channel checks). **Residual:** F-01 — nested cross-platform/transcript/metric fields under `identity_boundary`/`niche_scope` pass the primary gate. |
| **H-02** | Source-owned fields rebuild from the source ledger and compare against the static ledger | **partially_closed** | Rebuild is **real and non-circular** (test loads `docs/review-inputs/…json`) and catches drift in compared fields (positive control proven). **Residual:** F-02 (primary `platform_subject_key`/`public_profile_url` unbound; `sha256` unenforced) + F-03 (no negative drift test). |
| **H-03** | With `ORCA_DATA_ROOT`, packet/video/channel refs reconcile to lake metadata | **partially_closed / positive-path not_assessed by reviewer** | Code reconciles marker UUID + manifest (`packet_id`/`source_family`/`source_surface`) + metadata (`platform_video_id`/`channel_id`) on read. **Residual:** F-04 — optional + skipped in portable runs, no negative test, coarse error codes, unvalidated `metadata_relpath`; author's `32 passed` not independently revalidated (no lake). |
| **H-04** | No metric rollups, cross-platform linkage, transcript bodies, private/contact/person data, or dashboard claims admitted | **partially_closed** | Denylist blocks PII/contact/legal/follower-graph/secret **names** recursively (Control B proven); metric-policy + 2 required `non_claims` enforced; docs conservative. **Residual:** F-01 (the cross-platform/transcript/metric classes are smuggleable by nesting) + F-06 (only 2 of 11 `non_claims` enforced). |

No goal is assessed `closed`; none is `not_closed`. Each is `partially_closed` with a concrete, demonstrated residual and a stated minimum closure condition.

---

## Commission Scope-Question Answers (condensed)

- **Fail-closed on unknown/forbidden fields incl. nested/optional/future?** At every **named structural level**: yes (closed allow-lists). In **allow-listed-but-unvalidated sub-objects** (`identity_boundary`, observation `niche_scope`, and base-validation `source_artifact_counts`/`observed_author_names`/`known_label_status_counts_…`): **no** — see F-01.
- **Prevents metric smuggling while keeping the explicit non-claim?** Top-level yes (`unknown_field` + `metric_rollup_policy` enforced); nested no (F-01/GAP3).
- **Prevents cross-platform identity smuggling (TikTok/IG/email/contact/legal/private/transcript/social-graph)?** PII/contact/legal/social-graph **names**: yes (recursive denylist). **TikTok/Instagram handle names + transcript-body names**: no when nested (F-01) — they are absent from the denylist and the allow-list doesn't recurse.
- **Source-rebuild proves source-owned fields, or can they drift?** Compared fields are bound (drift → `source_rebuild_mismatch`, proven). **Primary `platform_subject_key`, `public_profile_url` can drift** in portable mode; declared `sha256` unenforced (F-02).
- **Live-lake reconciles the right refs, or too easy to skip?** Reconciles the right refs **when run**, but it is fully optional/skippable and unproven negatively (F-04).
- **Duplicate ids / alignment / channel mismatch fail for the right reasons?** Yes in the code (distinct codes), but **only channel-mismatch, within-row dup video, and packet-count have tests**; cross-ledger dups, alignment, packet-id format are untested (F-03).
- **Tests mutate deeply enough?** They mutate top-level wrappers and a few row fields; they do **not** reach source-rebuild drift, live-lake, nested smuggling, or cross-ledger structure (F-03/F-01).
- **Non-silent, debuggable failures?** Mostly yes (specific codes/messages); **two coarseness issues**: live-lake mismatches and internal packet-consistency asserts both surface as `source_rebuild_mismatch` (F-04), and forbidden-field hits raise a foreign exception type (F-05).
- **Docs accurately state the static-observation boundary without overclaiming readiness/metrics/linkage/SQLite/live capture?** **Yes — docs are conservative and accurate to the fixture.** Repo map, consolidation map, and toolbox README consistently disclaim cross-platform linkage, metric rollups, transcript bodies, SQLite, and live capture; the DCP trigger fix (`product_contract`→`product_doctrine`) is present. **One residual:** the docs reference the verifier as the guarantor of those boundaries, which F-01 shows it only partially is — fold into F-01's doc-softening option.
- **Package placement sensible?** Yes — reusable verifier in `orca-harness/capture_spine/youtube_creator_observation/` (sibling to `creator_public_handle_linkage/`, matching the repo-map line this commit updates), product spec/JSON under the YouTube source-family surface, review artifacts under `docs/`. I did **not** independently rerun `check_placement.py`; on the documented structure no new target file appears to create a material placement blocker (author-supplied hook result: pre-existing repo-wide debt only).
- **Design-level blocker (different entity model / metric home / SQLite / identity boundary)?** **No design blocker.** The one-platform observation model is coherent for the current evidence and correctly defers metrics/linkage/SQLite. The findings are code/test-level hardening, not an architecture re-home. (If the CA intends the verifier — not just the fixture — to be the **durable boundary guarantee** for future ledger edits, F-01 is the item to weigh for possible escalation.)

---

## Validation Rerun Status

- **Independently re-derived by reviewer (portable; `ORCA_DATA_ROOT` unset):**
  `python -m pytest -q --rootdir <target> orca-harness/tests/unit/test_youtube_creator_observation_ledger.py orca-harness/tests/unit/test_creator_public_handle_linkage.py` →
  **`31 passed, 1 skipped in 0.24s`** — **matches** the author's portable result. The skip is the live-lake test.
- **Reviewer adversarial probe (read-only, in-memory mutation of the committed fixture, no writes):** reproduced Controls A/B and demonstrated GAP1-GAP6 and the positive rebuild control as quoted in the findings.
- **Live-lake suite (`ORCA_DATA_ROOT=F:\orca-data-lake`):** author-supplied **`32 passed`**; **NOT independently revalidated** — no data lake available to this reviewer; result not fabricated.
- **`py_compile`, `git diff --check`, retrieval-header / header-index / map-links / dcp-receipt / repo-map-freshness / placement hooks:** **author-supplied; NOT independently rerun** by this reviewer (out of advisory scope; placement hook author-reported as failing only on pre-existing repo-wide debt).

---

## Open Questions / Residual Risk

1. **Is the verifier intended to be the durable boundary guarantee, or only a check on the committed fixture?** This determines whether F-01 is `major`-to-escalate or an accepted residual. The commission frames the ledger as a "static source-backed creator observation substrate" others rely on — which leans toward "guarantee," raising F-01's weight.
2. **Portable vs live-lake assurance split.** Because live-lake is optional and CI-skipped, the *default* assurance level is portable, where F-02 (unbound primary channel id) and F-01 (nested smuggling) are live. Anyone treating a green portable run as full reconciliation is over-trusting.
3. **Residual not turned into a finding:** in base validation the source-owned sub-objects (`source_artifact_counts`, `observed_author_names`, `known_label_status_counts_100_pool_only`) are only key-constrained via the recursive denylist; they are bound to source **only** through `validate_source_rebuild`, which the suite exercises only positively (subsumed by F-01/F-03).

## Strict-Claim Boundary & Non-Claims

- This is **read-only advisory** implementation/code review. **Not** a formal PASS/FAIL, acceptance, readiness, validation verdict, no-new-seam claim, mandatory remediation, or `patch_queue_entry`. Severity labels are **priority only**.
- **NOT_CLAIMED (strict):** formal implementation-review authority; validation pass/fail; live-lake positive-path revalidation; independent rerun of compile/static hooks; readiness for metric rollup, cross-platform linkage, SQLite, or live capture.
- No source file edited; no commit, push, PR, or live capture performed. The only write is this report (uncommitted; owner-gated per `AGENTS.md` / branch-protection doctrine).
- **Output-destination note:** the commission pinned `docs/review-outputs/<slug>.md` (root); `docs/review-outputs/README.md` says new reports *default* to `adversarial-artifact-reviews/` but **both locations are valid** — I honored the commission's explicit pin. No collision (path was absent at write).

---

```text
DELEGATED_CODE_REVIEW_RETURN_FOR_HOME_MODEL

Here is the delegated code review result. Adjudicate it under the delegated-review-patch return contract.

- original commission / review target:
    docs/prompts/reviews/youtube_creator_observation_ledger_verifier_adversarial_code_review_prompt_v0.md
    target: 77f0ade5..5295778e on codex/creator-ledger-static-fixture (multi-file verifier/test/spec/doc hardening packet),
    routed to READ-ONLY implementation/code review (not the single-target delegated patch convention).

- implementation context, diff, reviewed files:
    NEW orca-harness/capture_spine/youtube_creator_observation/{__init__,validation}.py (reusable verifier, 431 lines);
    MOD orca-harness/tests/unit/test_youtube_creator_observation_ledger.py (+hardened tests);
    MOD youtube_creator_observation_ledger_spec_v0.md (DCP trigger -> product_doctrine; +validation.py pointers);
    MOD orca_repo_map_v0.md, data_capture_spine_consolidation_map_v0.md, source_capture_toolbox/README.md (propagation).
    Worktree HEAD aa991ff1 adds only the commission prompt; target files byte-identical to 5295778e (no drift).

- findings & implementation evidence (priority labels only, NOT formal verdict):
    F-01 (major) nested-field smuggling: identity_boundary / observation niche_scope are allow-listed but never
        content-validated and the allow-list is non-recursive; the recursive denylist omits tiktok_*/instagram_*/
        transcript_* names. PROBE: nested tiktok+instagram, transcript_body, average_views all ACCEPT (base + rebuild);
        top-level + denylisted controls correctly REJECT. Defeats the cross-platform/transcript/metric boundary.
    F-02 (major) partial source binding: validate_source_rebuild never compares platform_subject_key / public_profile_url;
        source_inputs.sha256 never enforced. PROBE: fabricated subject_key ACCEPT (base+rebuild); corrupted sha256 ACCEPT;
        positive control drifted creator_handle_query -> REJECT source_rebuild_mismatch (rebuild binds compared fields only).
    F-03 (major) negative-test gap: no red test for source-rebuild drift, live-lake failures, cross-ledger duplicate/
        alignment, count/metric-policy violations, or nested smuggling; only positive rebuild + 6 narrow negatives exist.
    F-04 (minor) live-lake optional/unreproduced; live-lake mismatches surface as generic source_rebuild_mismatch;
        metadata_relpath unvalidated. Author 32-passed not revalidated (no lake).
    F-05 (minor) forbidden-field rejection raises CreatorPublicHandleLinkageError, not YoutubeCreatorObservationLedgerError;
        _raises_code helper catches only the latter.
    F-06 (minor) only 2 of 11 non_claims enforced; spec's unresolved-row / missing-packet-residual branches unimplemented.

- intended hardening closure statuses:
    H-01 partially_closed (F-01) | H-02 partially_closed (F-02,F-03) |
    H-03 partially_closed, reviewer-not-assessed positive path (F-04,F-03) | H-04 partially_closed (F-01,F-06).

- proposed patch / diff / exact edits:
    NONE authored — read-only code-review lane, no patch authorization. Advisory remediation direction only
    (per-finding minimum_closure_condition); a bounded verifier+test hardening patch would need separate CA authorization.

- citations:
    validation.py (_validate_observations ~257-283; validate_source_rebuild 146-187;
    validate_..._against_live_lake 190-219; _validate_required_non_claims 412-417; _assert_equal 420-422);
    creator_public_handle_linkage/validation.py (assert_no_forbidden_output_fields 235-249; _FORBIDDEN_OUTPUT_FIELDS 117-169);
    test_youtube_creator_observation_ledger.py (98-109, 112-121, 124-173);
    youtube_creator_observation_ledger_spec_v0.md (124-160); fixture sub-object shapes (identity_boundary/niche_scope strings,
    source_inputs[].sha256 present).

- reviewer verdict (advisory, decision input only):
    Substantively solid for the current census; hardening goals are PARTIALLY CLOSED, not closed. 3 major-priority residuals
    (F-01 boundary bypass, F-02 partial source binding, F-03 missing negative tests) bear directly on the false-confidence
    risk the commission asked me to attack. No design-level blocker; no formal PASS / readiness / validation asserted.

- validation evidence & not-run checks:
    Reviewer-rerun portable suite = 31 passed, 1 skipped (matches author). Live-lake 32-passed = author-supplied, NOT revalidated.
    py_compile + git/header/map/dcp/repo-map/placement hooks = author-supplied, NOT rerun. Adversarial probe = read-only, no writes.

- residual risk:
    Default assurance is portable mode, where F-01 + F-02 are live; live-lake (the stronger reconciliation) is optional/skipped.
    Treating a green portable run as a full boundary+source guarantee over-trusts the verifier.

- blockers / off-scope flags / not-proven boundaries:
    No blocker. Did NOT widen beyond the touched scope + named context. NOT proven: live-lake positive path; independent hook reruns;
    any readiness/validation/no-new-seam claim. de_correlation_bar = cross_vendor_discovery (author OpenAI != reviewer Anthropic).
```
