---
retrieval_header_version: 1
artifact_role: Orca delegated review-and-patch report (decision input; CA-adjudicated)
scope: >
  Delegated, de-correlated adversarial mixed implementation review-and-patch of the
  creator public-handle linkage ledger v0 static fixture/validator lane
  (commit ecfcee8f). Findings + applied working-tree patches for CA hunk-by-hunk
  adjudication before keep.
use_when:
  - Adjudicating the creator public-handle linkage ledger v0 branch before downstream
    ledger population or SQLite migration.
  - Checking whether the validator/fixture/tests/docs preserve the
    public-handle-only identity-stitching boundary.
authority_boundary: retrieval_only
review_type: delegated_adversarial_mixed_implementation_review_patch
commission_prompt: docs/prompts/reviews/creator_public_handle_linkage_ledger_delegated_adversarial_code_review_patch_prompt_v0.md
target_commit: ecfcee8f17c7b3c622b8620c10033aaf9347c4cf
de_correlation_bar: cross_vendor_discovery
authored_by: GPT-5 / Codex home model (OpenAI lineage)
reviewed_by: claude-opus-4-8 (Anthropic lineage)
verdict: PATCHED_FOR_CA_ADJUDICATION
home_adjudication_status: MODIFIED_AND_ACCEPTED_FOR_KEEP
adjudicated_by: Codex home model (OpenAI lineage)
---

# Creator Public-Handle Linkage Ledger — Delegated Adversarial Review-and-Patch v0

> Decision input only. This delegate diff, its citations, and its verdict are **not**
> validation, readiness, approval, or auto-keep. The commissioning Chief Architect /
> home model adjudicates every hunk against the branch intent before anything is kept.
> Commissioned under the provisional Orca delegated review-and-patch convention
> (`.agents/workflow-overlay/delegated-review-patch.md`), `repo` access mode.

## Home-Model Adjudication Addendum — 2026-06-27

Final disposition: **modified and accepted for keep**. The delegated diff was treated as decision input, not auto-kept.

- **CR-01 accepted with modification.** The delegate correctly found the scalar-field allowlist-envelope hole, but its returned patch did not type-check nullable account scalar fields. I extended the fix to validate `platform_public_account_id_or_none`, `public_display_name_or_none`, `display_name_source_pointer_or_none`, and `display_name_source_field_or_none` as either `null` or non-empty strings, and changed the display-name source requirement to fire whenever `public_display_name_or_none` is non-null.
- **CR-02 accepted as returned.** Probable links now require at least three distinct weak evidence types and at least three distinct `independence_key` families.
- **CR-03 accepted as returned.** Synthetic profile URLs now require `example.test` as the host or a subdomain, not a substring.
- **AR-01 accepted as returned.** The future-exploration doc now says the Tier-2-A aggregate-audience schema home is a separate architecture decision, not this public-handle linkage ledger.
- **Validation observed after adjudication:** focused ledger tests `21 passed`; adjacent regression set `93 passed`; selected red-green `6 failed` against the old `HEAD` validator and `6 passed` with the adjudicated validator; `check_retrieval_header --changed --strict` exit 0 after this addendum; `check_repo_map_freshness --changed --strict` exit 0 with an advisory about the new review-output file under the already described `docs/review-outputs/` area; `git diff --check` exit 0 with CRLF normalization warnings only.
- **Non-claims:** this is not runtime capture, SQLite migration, live social-media access, audience-demographics activation, deployment, merge, or readiness proof.

## Commission / De-Correlation Receipt

- **Commission:** `docs/prompts/reviews/creator_public_handle_linkage_ledger_delegated_adversarial_code_review_patch_prompt_v0.md`
- **Target commit:** `ecfcee8f17c7b3c622b8620c10033aaf9347c4cf` ("Add creator public-handle linkage validator"); worktree HEAD `7003889a` adds only the commission prompt; working tree otherwise clean before patching.
- **Author vendor:** OpenAI (GPT-5 / Codex home model). **Controller vendor:** Anthropic (claude-opus-4-8).
- **De-correlation:** author vendor ≠ controller vendor → `cross_vendor_discovery` bar satisfied (the discovery / no-new-seam tier). A who-constraint only; not a model recommendation or ranking.
- **Edit permission:** patch-only, within the commission's editable target files. No stage/commit/push/PR/deploy/install/live-capture/SQLite.
- **Both review skills available** in this runtime (`workflow-code-review`, `workflow-adversarial-artifact-review`); no `BLOCKED_REVIEW_LANE_UNAVAILABLE`.

## Source Context Status — `SOURCE_CONTEXT_READY`

**Controlling source loaded:** `AGENTS.md`; overlay `README.md`, `source-loading.md`,
`review-lanes.md`, `delegated-review-patch.md`, `prompt-orchestration.md`,
`safety-rules.md`; the linkage spec; `models.py`; `validation.py`; the synthetic
fixture; the unit tests; all 11 target files (verified to equal the `ecfcee8f`
change surface); the five propagation-doc diffs; and the authorizing decision
`docs/decisions/wind_caller_calibration_carveout_v0.md` (full).

**Methods:** `workflow-deep-thinking`, `workflow-code-review`,
`workflow-adversarial-artifact-review` REFERENCE-LOADed before source readiness;
APPLIED only after this declaration.

**Cross-cutting checks run:** grep across the new `creator_public_handle_linkage`
package — the only audience reference is the `audience_graph` entry in the
forbidden-field denylist; no import of / wiring to the ideal-audience or
audience-fusion surfaces (code-level separation confirmed).

**Available-not-read (background, not decision-bearing for the findings below):**
`ig_creator_ideal_audience_inference_spec_v0.md`, `orca-harness/schemas/audience_inference_models.py`,
`orca-harness/scoring/audience_fusion.py`, the cross-platform-identity deep-thinking
prompt, `.agents/workflow-overlay/validation-gates.md` (the commission already
enumerated the named gates). No strict claim below depends on these.

## Deep-Thinking Risk Frame (before findings)

This artifact is a **guardrail instrument**: its value is precisely that it makes a
same-creator link hard to fake and forbidden person/audience data hard to store. So
the decisive failure modes are not crashes — they are *guardrails that look enforced
but are not*, and *boundary holes that only an adversarial author would reach*:

1. **Allowlist envelope with a hole.** The validator fails closed on unknown keys at
   every *structured* level (wrapper/account/evidence/record allowlists) and deep-sweeps
   for a fixed denylist of forbidden key names + value patterns. The residual risk is a
   field that is *contractually scalar* but *type-unconstrained*: a nested object placed
   there is walked only by the exact-match denylist, so a metadata/audience/demographic
   blob under non-denylisted keys slips the envelope. → **CR-01.**
2. **Independence asserted, not enforced.** The spec requires "three **independent**
   weak evidence families" and ships `independence_key` to express family identity, but
   the validator counts only distinct evidence *types* and never reads `independence_key`.
   Three types from one family pass. → **CR-02.**
3. **Synthetic real-data guard bypass.** The synthetic-mode URL guard is a substring
   test, so a real host containing the marker string passes. → **CR-03.**
4. **Audience-absorption drift.** The carve-out (2026-06-23) council-confirms Tier-2-A
   aggregate audience demographics and names their *remaining* gate as a "schema home
   (the ledger currently forbids demographic fields)." The freshest adjacent schema is now
   this linkage ledger — inviting a future misread that it is that home. The branch keeps
   them separate (validator forbids demographic fields; docs gate Tier-2-A), so this is a
   *flag*, addressed by a small clarifying doc line, not a defect. → **AR-01.**
5. **Over-authorization in propagation prose.** Verified the load-bearing new claim —
   "Tier-2-A aggregate audience demographics are council-confirmed … aggregate/text-only" —
   against the carve-out's 2026-06-23 amendment: **accurate propagation, not over-auth.**
   No finding.

## Findings (severity order; `critical` > `major` > `minor`)

Severity labels are finding-priority only (per `review-lanes.md`); they confer no
approval, rejection, readiness, or mandatory-remediation authority.

### CR-01 — Type-unconstrained scalar fields let a nested blob bypass the allowlist envelope — `major` — PATCHED

- **Location:** `orca-harness/capture_spine/creator_public_handle_linkage/validation.py` — `_require` (presence-only) was the sole guard for scalar fields at wrapper L197-211 (`ledger_id`, `source_policy_posture`), account L267-278, evidence L314-329, creator-record L361-376; deep sweep `assert_no_forbidden_output_fields` L229-244.
- **Failure mode:** `_require` accepts any non-`None`, non-empty-if-string value, so a contractually-scalar field (e.g. `source_policy_posture`, `link_rationale`, `limitations`, source pointers, timestamps) may carry a nested object/array. The allowlist that fails closed on unknown keys is applied only at the four *structured* levels; it does not recurse into a nested object sitting inside an allowed scalar field. The only backstop there is the exact-match `_FORBIDDEN_OUTPUT_FIELDS` denylist + value patterns.
- **Evidence:** `_FORBIDDEN_OUTPUT_FIELDS` matches keys by exact lowercase equality (`lowered in _FORBIDDEN_OUTPUT_FIELDS`, L234). `age`/`gender`/`followers` are denylisted but `age_band_18_24_pct`/`gender_skew`/`followers_est` are not. The fixture uses `source_policy_posture` as a plain string (L10), confirming the field is contractually scalar.
- **Impact:** A demographic/audience/contact blob authored as `source_policy_posture: {"aggregate_audience": {"age_band_18_24_pct": 40, ...}}` (or under any free-text scalar) validates — directly defeating Validator-Contract items "fail closed on unknown fields" and "any … demographic, audience graph … field" (spec L171-183), and the project boundary that the linkage ledger stores no audience/person data. This is the precise "metadata blobs / nested structures / future platform extensions" vector in Review Question 1.
- **Closure (minimum_closure_condition):** every field the contract defines as a scalar string is validated as a string, so a nested object can appear only in the explicitly allowlisted container fields. (End state, not implementation.)
- **next_authorized_action:** CA adjudicates the applied patch.
- **Patch:** added `_require_str(...)` (present + `str` + non-empty; non-string → `non_string_<field>`, preserving the existing `missing_<field>` code for `None`/empty) and applied it to the scalar-string fields at all four levels; account & display blocks switched from `_require` to `_require_str`. Closes the class, not one instance.
- **Verification:** red-green — `test_nested_blob_in_wrapper_scalar_field_is_rejected` and `test_nested_blob_in_creator_record_free_text_is_rejected` FAIL on the reverted validator, PASS after.

### CR-02 — `independence_key` required but unused; "three independent weak evidence" enforced only as three distinct *types* — `major` — PATCHED

- **Location:** `validation.py` `_validate_link_state_evidence`, PROBABLE branch L416-424; required-but-unread `independence_key` at evidence L320-329.
- **Failure mode:** the probable-link gate computed `weak_types = {evidence_type … in _WEAK_EVIDENCE_TYPES}` and required `len(weak_types) >= 3`. `independence_key` is required on every evidence row but never read by any rule.
- **Evidence:** spec: probable = "at least three **independent** weak public evidence families" (L92-94) and `independence_key: required evidence-family key` (L139). Validator-Contract restates "fewer than three **independent** weak evidence types" (L178). The pre-patch code references no `independence_key`.
- **Impact:** three weak rows of distinct *types* but the same `independence_key` (one underlying family — e.g. handle, display-name, and bio overlap all derived from one scraped profile blob) satisfied a probable link. The "independent" guarantee — core to "hard to fake a same-creator link" — was unenforced, and a required field was dead weight (a false-success surface that reads as enforced). The existing test `test_probable_link_requires_three_independent_weak_evidence_types` over-claims "independent": it only collapses *types*.
- **Closure:** a probable link requires its weak evidence to span at least three distinct `independence_key` values (independent families), in addition to three distinct weak types.
- **next_authorized_action:** CA adjudicates the applied patch.
- **Patch:** added, after the existing type check, a `weak_independence_keys` set over the weak rows with `len(...) >= 3` else `_fail("probable_link_needs_three_independent_evidence_families", …)`. Spec is correct as written; only the validator was under-implementing it (no spec edit).
- **Verification:** red-green — `test_probable_link_requires_three_independent_evidence_families` (3 distinct types, 2 families) FAILS on the reverted validator, PASSES after. Fixture's probable record spans 3 families (`handle_family`, `bio_text_family`, `topic_family`) and still validates.

### CR-03 — Synthetic-fixture URL guard is a bypassable substring test — `minor` — PATCHED

- **Location:** `validation.py` `_validate_synthetic_account` L508-509.
- **Failure mode:** `if "example.test" not in str(url)` accepts any URL containing the marker as a substring, including a real host such as `https://example.test.evil.com/…` or a real URL with `?ref=example.test`.
- **Evidence:** pre-patch substring check at L508; synthetic-mode intent is to bar real profile URLs (spec Validator-Contract L183; Review Question 4).
- **Impact:** a synthetic fixture could carry a real-looking/real host URL — eroding the "synthetic fixtures cannot contain real-looking data" guard. Minor (synthetic mode only; requires a crafted lookalike host).
- **Closure:** the profile URL host must be `example.test` or a subdomain of it.
- **next_authorized_action:** CA adjudicates the applied patch.
- **Patch:** parse the host (`urlparse(...).hostname`) and require `host == "example.test" or host.endswith(".example.test")`.
- **Verification:** red-green — `test_synthetic_fixture_rejects_lookalike_host_url` (`example.test.evil.com`) FAILS on the reverted validator, PASSES after; the existing real-host test (`instagram.com`) and the fixture (`https://example.test/…`) are unaffected.

### AR-01 — Tier-2-A aggregate-audience schema home not explicitly disjoint from this linkage ledger — `minor` (optional hardening) — PATCHED (one doc line)

- **Phase:** correctness (boundary clarity). **Location:** `orca/product/spines/capture/core/operating_model/data_capture_spine_future_exploration_lanes_v0.md`, Future Exploration A.
- **Failure mode / strongest counter-reading:** the branch *already* keeps the surfaces separate — the linkage validator forbids demographic/audience fields and the doc gates Tier-2-A — so there is no live defect. The residual is future-misread risk: the carve-out (2026-06-23) names Tier-2-A's remaining gate as "a schema home (the ledger currently forbids demographic fields)," and this newly-added linkage ledger is the freshest adjacent schema.
- **Evidence:** carve-out L165-175 (council-confirmed Tier-2-A; remaining gate = schema home + base-rate data); linkage spec non-claims "not follower or audience graph" (spec L195-196); validator denylist includes `age`,`gender`,`audience_graph`,`follower_graph` (validation.py L116-168).
- **Impact:** if unstated, a later agent could wire Tier-2-A aggregate-audience attributes into linkage-ledger rows — the exact audience-absorption boundary the commission's Review Question 9 protects.
- **Closure:** the future-exploration doc states the Tier-2-A schema home is a separate decision and explicitly not the public-handle linkage ledger.
- **next_authorized_action:** CA adjudicates the one-line clarification, or drops it as optional. Per the commission, the Tier-2-A aggregate-audience schema home itself remains a **separate architecture decision** — it is **not** patched into this linkage ledger.
- **Patch:** added a "Schema-home boundary." note to Future Exploration A restating the disjointness. Clearly **optional / non-required** hardening.

## Non-Findings / Verified-Clean

- **Propagation wording is faithful, not over-authorizing.** All five doc diffs carry explicit non-claims ("static/validator only; no live capture, no contact/outreach, no SQLite, no person identity proof"). The large future-exploration rewrite keeps follower/connection/commenter/audience **graphs**, non-public-handle joins, and contact/outreach gated, and routes Tier-2-B through the linkage spec. The "Tier-2-A … council-confirmed … aggregate/text-only" claim matches the carve-out's 2026-06-23 amendment verbatim in substance (Review Questions 7, 8). No over-authorization of runtime capture, live identity resolution, SQLite, demographic inference, audience-graph storage, or commercial readiness.
- **`confirmed_public_account_link`, LLM-only final links, disconfirming-on-final, declared-needs-strong, probable-needs-human-review** are all enforced and tested (Review Question 2; CR-02 closes only the independence sub-gap).
- **Migration path is clean** (Review Question 5): stable required unique IDs, referential integrity (`evidence_ids`/`account_ids` ⊆ record accounts, ≥2 platforms), append-only evidence — each list maps to a SQLite table without semantic rewrite. No denormalized ambiguity blocker.
- **Ideal-audience lane stays separate at the code level** (Review Question 9): no import/wiring; the only audience token in the package is the denylist guard.
- **No `NEEDS_ARCHITECTURE_PASS`** (Review Question 10): the entity, evidence/provenance, and audience-home boundaries are sound; every finding is a local validator/test/doc fix. The Tier-2-A aggregate-audience schema home is a *separate* future decision the branch correctly defers, not a defect in this branch.

## Residual Risk (named; not patched)

- **Loose timestamps.** `created_at`/`updated_at`/`observed_at`/`handle_observed_at` are required strings (now string-typed by CR-01) but not format-validated. Acceptable for v0; a future ISO-8601 check is optional hardening, not required (IDs, not timestamps, carry the migration semantics).
- **`review_actor` human-review heuristic.** `_validate_not_llm_only_final_link` rejects a small set of LLM-ish actor names; a non-LLM-looking automated actor could still pass. Human review is primarily carried by `review_state`; inherent to a static fixture. Advisory only.
- **`public_handle_ledger` (real) mode** intentionally skips the synthetic real-data guards. Defensible (real handles are real), and the validator is shape-only — not capture authorization — but worth the CA noting that real-mode hygiene is weaker by design.
- **"legal review where required"** in Future Exploration A's still-gated graph preconditions slightly softens the carve-out's "hard legal gate" language for the *graph* lane (the aggregate slice's legal gate is genuinely cleared). Advisory wording nit; not patched to keep the diff focused.
- **Untested-but-correct negatives** (optional coverage, not patched): `evidence_strength`↔type mismatch, rejected-link-missing-disconfirming, missing authority pointer, forbidden value-pattern hits. Behavior is correct; tests are absent. Flagged as optional hardening only.
- **Line endings:** new lines are LF in a CRLF-normalized repo; `git diff --check` is clean with CRLF normalization warnings only — identical to the author's documented baseline. Git normalizes on commit; the CA's normal-git diff is the ~70-line semantic diff below, not a whole-file flip.

## Patches Applied (working tree only — not staged/committed)

| File | Change |
| --- | --- |
| `orca-harness/capture_spine/creator_public_handle_linkage/validation.py` | CR-01 `_require_str` helper + 4 call sites; CR-02 independence-family check; CR-03 URL host check; `urlparse` import. |
| `orca-harness/tests/unit/test_creator_public_handle_linkage.py` | +4 adversarial tests (red-green for CR-01 ×2, CR-02, CR-03). |
| `orca/product/spines/capture/core/operating_model/data_capture_spine_future_exploration_lanes_v0.md` | AR-01 "Schema-home boundary." note (optional). |

`git diff --stat`: 3 files changed, 110 insertions(+), 6 deletions(-).

### Precise changed-file summary (validator — repo-normalized semantic diff)

```diff
+from urllib.parse import urlparse
 # validate_creator_public_handle_linkage_ledger(): after wrapper _require(...)
+    _require_str(wrapper, ("schema_version","ledger_id","ledger_mode","source_policy_posture"), "ledger")
 # _validate_platform_accounts(): account required fields
-        _require( account, (platform_account_id, platform, public_handle, public_profile_url, handle_source_pointer, handle_observed_at), ...)
+        _require_str( account, (… same …), "platform_account")
 # display-name block
-            _require(account, (display_name_source_pointer_or_none, display_name_source_field_or_none), ...)
+            _require_str(account, (public_display_name_or_none, display_name_source_pointer_or_none, display_name_source_field_or_none), ...)
 # _validate_link_evidence(): after evidence _require(...)
+        _require_str(record, (evidence_id, evidence_type, evidence_strength, source_pointer, source_field, observed_at, review_actor, independence_key), "account_link_evidence")
 # _validate_creator_records(): after record _require(...)
+        _require_str(record, (creator_record_id, link_state, review_state, link_rationale, limitations, created_at, updated_at), "creator_record")
 # _validate_link_state_evidence(): PROBABLE branch
+        weak_rows = [row for row in evidence_rows if str(row["evidence_type"]) in _WEAK_EVIDENCE_TYPES]
+        weak_independence_keys = {str(row["independence_key"]) for row in weak_rows}
+        if len(weak_independence_keys) < 3: _fail("probable_link_needs_three_independent_evidence_families", …)
 # _validate_synthetic_account(): URL guard
-    if "example.test" not in str(account["public_profile_url"]): _fail("synthetic_fixture_url_required", …)
+    host = (urlparse(str(account["public_profile_url"])).hostname or "").lower()
+    if host != "example.test" and not host.endswith(".example.test"): _fail("synthetic_fixture_url_required", …)
 # new helper
+def _require_str(value_map, field_names, label):  # present + str + non-empty; non-string -> non_string_<field>
```

## Validation Run

- `python -m pytest -q tests/unit/test_creator_public_handle_linkage.py` → **19 passed** (15 prior + 4 new).
- `python -m pytest -q tests/unit/test_creator_public_handle_linkage.py tests/unit/test_reddit_graph_frontier.py tests/unit/test_linkedin_graph_frontier.py tests/unit/test_linkedin_lane.py` → **91 passed** (author baseline 87 + 4 new; no regression).
- **Red-green proof:** with `validation.py` reverted to `ecfcee8f` (other files unchanged), the four new tests → **4 failed, 15 deselected**; with the patch → all pass. (Validator restored via `git stash pop`.)
- `python .agents/hooks/check_retrieval_header.py --changed --strict` → exit 0.
- `git diff --check` → exit 0 (CRLF normalization warnings only).
- **Not run (out of commission scope):** network / live IG-TikTok-YouTube capture, browser automation, package installs, SQLite migration, external API calls. `check_placement.py` not re-run as a pass gate — the author reported it failing on pre-existing repository placement debt; this branch adds **no new files** (only edits to existing target files), so it introduces no new placement blocker.

## Verdict — `PATCHED_FOR_CA_ADJUDICATION`

Two `major` boundary findings (CR-01 allowlist-envelope hole; CR-02 unenforced
independence) and one `minor` synthetic-data guard (CR-03) were patched in the
validator with red-green proof; one `minor`/optional doc clarification (AR-01) was
added. No `NEEDS_ARCHITECTURE_PASS`. The diff and this verdict are **decision input**;
the CA adjudicates each hunk before keep and may modify or reject any change,
including an individually defensible one.

## Review-Use Boundary

These findings and patches are input for CA adjudication only. They are not approval,
validation, readiness, mandatory remediation, or executor-ready patch authority until
separately accepted. Keeping any hunk, committing, pushing, or promoting remains the
CA's decision under the per-lane PR flow.

## Provenance & Non-Claims

- `authored_by`: GPT-5 / Codex home model (OpenAI lineage) — from the commission.
- `reviewed_by`: claude-opus-4-8 (Anthropic lineage). `de_correlation_bar`: `cross_vendor_discovery`. Factual provenance only; never a runtime-model recommendation, ranking, or selection.
- **Non-claims:** no validation, no readiness, no approval, no auto-keep, no deployment, no runtime capture, no SQLite migration, no live social-media access, and no audience-demographics activation. The static validator is a shape gate, not capture authorization.

---

## DELEGATED_CODE_REVIEW_RETURN_FOR_HOME_MODEL

Here is the delegated review-and-patch result. Adjudicate it under the
delegated-review-patch return contract (`.agents/workflow-overlay/delegated-review-patch.md`).

- **Original commission / target:** harden the creator public-handle linkage ledger v0 (commit `ecfcee8f`) — validator, synthetic fixture, tests, and propagation docs — preserving the public-handle-only identity-stitching boundary before any SQLite/population work.
- **Implementation context / reviewed files:** `validation.py`, `models.py`, `__init__.py`, the synthetic fixture, the unit tests, the linkage spec, and the five propagation docs; authorizing decision `wind_caller_calibration_carveout_v0.md`.
- **Findings + evidence:** CR-01 `major` (type-unconstrained scalar fields → nested-blob bypass of the allowlist envelope); CR-02 `major` (`independence_key` required but unused → "three independent weak evidence" enforced only as three distinct types); CR-03 `minor` (substring synthetic-URL guard); AR-01 `minor`/optional (Tier-2-A schema-home not explicitly disjoint from the linkage ledger). Evidence cited inline with file:line.
- **Proposed patch (applied to working tree, not staged):** `validation.py` (+`_require_str` class fix, +independence-family check, +URL host check), `test_creator_public_handle_linkage.py` (+4 red-green tests), future-exploration doc (+1 optional boundary line). `git diff --stat`: 3 files, +110/−6.
- **Citations:** spec L92-94/L139/L171-183/L195-196; validation.py L116-168/L229-244/L416-424/L508-509; fixture L10; carve-out L165-175; future-exploration Future-Exploration-A.
- **Reviewer verdict:** `PATCHED_FOR_CA_ADJUDICATION`.
- **Validation evidence:** 19 passed (target file); 91 passed (broader set); red-green 4-failed-on-revert → all-pass-with-patch; retrieval-header hook exit 0; `git diff --check` clean (CRLF only). Not run: network/live-capture/SQLite/installs.
- **Residual risk:** loose timestamps; `review_actor` heuristic; weaker real-mode hygiene by design; "legal review where required" wording softening; untested-but-correct negatives (optional coverage); LF/CRLF normalization (benign, matches baseline).
- **Blockers / off-scope flags / not-proven:** none blocking. Off-scope (flagged, not patched): the Tier-2-A aggregate-audience schema home is a separate architecture decision, not for this linkage ledger. Not-proven: no validation/readiness/approval is asserted; the delegate diff is decision input only.
