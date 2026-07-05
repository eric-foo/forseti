# Creator Discovery Scan Fragrance YouTube Public PR #725 Delegated Adversarial Artifact Review v0

```yaml
retrieval_header_version: 1
artifact_role: Review report
scope: >
  Delegated, de-correlated adversarial artifact review of PR #725
  (codex/fragrance-youtube-creator-scan), covering the fragrance YouTube
  creator discovery scan artifact, its candidate batch, its Creator Registry
  match-preflight receipt, and the repo-map entry change.
use_when:
  - Adjudicating PR #725 before merge.
  - Checking whether the first live receipt-bearing Creator Registry cold
    discovery scan improved toward the Mini God Tier Creator Ledger goal
    without overclaiming or silently weakening enforcement.
authority_boundary: retrieval_only
```

```yaml
review_summary:
  status: completed
  report_path: docs/review-outputs/adversarial-artifact-reviews/creator_discovery_scan_fragrance_youtube_public_pr725_delegated_adversarial_artifact_review_v0.md
  recommendation: accept_with_friction
  reviewed_by: Claude Sonnet 5 (claude-sonnet-5)
  authored_by: gpt-5-codex
  summary: "PR #725 replaces a cap-overrun-tainted candidate batch with a clean, verifiably-in-cap batch whose receipt content and hashes check out, but the artifact overclaims registry orientation as accounting for all 36 profiles when only 30 YouTube handles were actually enumerated, and the repo-map/commit description undersells that this is a full candidate-set replacement rather than a wording refresh."
  findings_count: 7
  blocking_findings: []
  advisory_findings:
    - AR-01: Registry orientation figure mismatch (36 profiles claimed enumerated, only 30 YouTube handles listed)
    - AR-02: "Refresh" framing understates a full candidate-set replacement
    - AR-03: Receipt generated_at_utc predates repo-map change commit but postdates candidate collection plausibly
    - AR-04: No re-declaration of exploratory-query discipline for the new run
    - AR-05: Registry freshness gap between rehearsal doc (33) and this scan (36) not reconciled anywhere
    - AR-06: Non-claims list omits an explicit "not a rerun of the prior scan's candidates" disclosure
    - AR-07: capture_request rows lack a `route_binding_state` field present in the schema's own checker requirements
  prior_findings_remediated:
    - "Cap-overrun process residual (previously named in the prior commit `docs: clarify fragrance scan cap residual` and the pre-PR artifact) is resolved by wholesale replacement with a batch whose own accounting (4/8 exact queries, 14/30 source reads) is internally consistent and verifiable."
  next_action: "Owner/CA decides whether AR-01 (registry-count overclaim) and AR-07 (missing route_binding_state field) need a same-lane patch before merge, or are acceptable residuals given the artifact's own non-claims; no other finding blocks merge."
```

## Review-Use Boundary

This review is decision input only. It is not approval, validation, mandatory
remediation, or executor-ready patch authority. Findings are reported for CA
or owner adjudication; only a separately authorized lane may accept, patch,
or merge.

## Source-Gated Method Contract

1. `workflow-deep-thinking` and `workflow-adversarial-artifact-review` were
   REFERENCE-LOADed via the Skill tool before any source-specific analysis.
   Neither method was APPLIED before source readiness.
2. All required authority sources and task sources named in the commissioning
   prompt were SOURCE-LOADed (see Source-Read Ledger below).
3. `SOURCE_CONTEXT_READY` is declared below with one named material gap
   (the registry-count/orientation cross-check, resolved in-review; see
   AR-01) and one accepted non-blocking gap (full read of
   `creator_profile_current_view_v0.json`, which exceeded the file-read tool's
   256KB limit; counts and a full YouTube-handle scan were obtained via
   `python -c` instead of a raw file read — see Source-Read Ledger).
4. `workflow-deep-thinking` was APPLIED to frame the boundary problem before
   findings (see Deep-Thinking Frame below).
5. `workflow-adversarial-artifact-review` was APPLIED to the loaded source
   context and the PR diff to produce the findings below.

## SOURCE_CONTEXT_READY

Declared `SOURCE_CONTEXT_READY` for this review's scope (the four changed
artifacts plus their reviewable task/authority context). One material gap
was investigated and resolved during review (AR-01, registry-count
cross-check); it is reported as a finding, not left as an open gap.

## Source-Read Ledger

Authority sources (all read in full):

| Source | Why read | Status |
| --- | --- | --- |
| `AGENTS.md` | Agent behavior kernel, Smallest Complete Intervention, MGT trigger | clean |
| `.agents/workflow-overlay/README.md` | Overlay entrypoint | clean |
| `.agents/workflow-overlay/source-of-truth.md` | Source hierarchy, DCP contract | clean |
| `.agents/workflow-overlay/source-loading.md` | Source-loading budgets | clean |
| `.agents/workflow-overlay/artifact-roles.md` | Role bindings for research/review artifacts | clean |
| `.agents/workflow-overlay/artifact-folders.md` | Accepted folders (docs/research, review-outputs) | clean |
| `.agents/workflow-overlay/retrieval-metadata.md` | Retrieval header contract | clean |
| `.agents/workflow-overlay/review-lanes.md` | Review doctrine, coverage-first find stage, provenance fields | clean |
| `.agents/workflow-overlay/prompt-orchestration.md` | Source-Gated Method Contract, review prompt defaults | clean |
| `.agents/workflow-overlay/validation-gates.md` | Current gates, review-routing/handoff-pointer/DCP gates | clean |
| `.agents/workflow-overlay/communication-style.md` | review_summary YAML shape, adjudication next-step | clean |
| `.agents/workflow-overlay/template-registry.md` | Template registry (adversarial-artifact-review template) | clean |
| `.agents/workflow-overlay/delegated-review-patch.md` | Delegated review-and-patch convention, de-correlation rule | clean |
| `docs/decisions/orca_mini_god_tier_doctrine_v0.md` | MGT lens, accepted-residuals requirement | clean |

Task sources:

| Source | Why read | Status |
| --- | --- | --- |
| `docs/prompts/handoffs/creator_registry_cold_creator_discovery_scan_handoff_prompt_v0.md` | Reusable launch-prompt contract for this scan family; output-contract and hard-boundary check | clean, on `origin/main` |
| `docs/workflows/creator_registry_operational_next_steps_handoff_v0.md` | Named in commission; absent on this branch, present via glob at repo root; not read in full (not decision-bearing for this bounded review; the cold-scan handoff prompt plus the artifact's own declared source context sufficiently bound the task contract per the commission's fallback instruction) | present but not opened; recorded as an available-not-read source per the fast-path/materiality rule |
| `docs/workflows/creator_registry_cold_agent_preflight_rehearsal_v0.md` | Behavioral example, registry counts at time of rehearsal (33 profiles) | clean |
| `forseti/product/spines/.../creator_registry_match_preflight_usage_v0.md` | Preflight usage contract, checker enforcement note | clean |
| `forseti/product/spines/.../creator_profile_current_view_v0.json` | Registry ground truth; too large (337KB) for the Read tool's 256KB cap, so counts, schema fields, and the full YouTube-handle set were extracted via `python -c` (documented commands, not paraphrase) | clean, verified via script, not raw-read |
| `orca-harness/runners/run_creator_registry_match_preflight.py` | Runner CLI contract, exit-code semantics | clean |
| `orca-harness/capture_spine/creator_profile_current/registry_match_preflight.py` | Match logic, identity-key construction, decision/action_status rules | clean |
| `.agents/hooks/check_csb_scanning_artifact.py` | Checker logic: CSB-first vs Creator Registry preflight artifact detection, receipt-content verification | clean, full read |
| The four changed artifacts (scan `.md`, candidates `.json`, receipt `.json`, repo map entry) | Review target | clean, diff-scoped against `origin/main` |
| Pre-PR version of the scan `.md` and candidates `.json` (`git show origin/main:...`) | Before/after comparison for attack #8 (erasure) | clean, via `git show` |
| Prior commit history for the scan artifact (`e1ae5f27`, `dfdb61b8`, `71a0bf70`) | Established that the cap-overrun residual was a previously-named, deliberate disclosure, not a hidden defect this PR is quietly burying | clean, via `git log`/`git show --stat` |

## Deep-Thinking Frame

**The actual question**: does PR #725 turn a previously self-disclosed,
cap-tainted scan into a materially better receipt-bearing scan, or does it
launder a defect by quietly swapping evidence while keeping the same claim
of "first live receipt-bearing scan"? The two candidate readings are: (a)
legitimate remediation — the author recognized the earlier batch could not
honestly claim clean caps and did a fresh, disciplined run; or (b) evidence
laundering — replacing suspect rows with rows that merely look cleaner while
reusing the same narrative frame and repo-map claim.

**Decisive evidence**: the new batch's own internal accounting (4 exact
queries of 8, 14 source reads of 30) is self-consistent, matches the
candidate count (10), and is checkable against the receipt's `input_index`
ordering. The new candidates additionally carry `platform_public_account_id_or_none`
(YouTube channel IDs) that the old batch never had — a strictly stronger
identity anchor for the exact-match preflight, not just cosmetic tidying.
Reading (a) is the better-supported one. This is not an erasure finding
under attack #8; it is a legitimate full-batch redo that happens to
overwrite the same file paths (which is expected, since the paths are
schema-fixed for this scan family).

**Failure modes actively checked**: cap-perfect-but-unsupported claims (checked:
supported, see Validation); known-registry accounts slipping through as
`new_candidate` (checked: zero handle/channel-ID collisions against the
current 36-profile registry); receipt/candidate/artifact disagreement
(checked: none found); stale/non-canonical receipt path (checked: matches
the exact path the checker's auto-detection and content-verification logic
resolve); capture-request rows phrased as authorization (checked: explicit
"handoff rows only... does not authorize capture" language present);
overclaim of fuzzy/cross-platform/buyer proof (checked: non-claims list
covers these); erasure of prior evidence (checked: this is redo, not
erasure — see Deep-Thinking Frame); stale registry-count handling (checked:
artifact explicitly prefers the JSON over the stale static-projection
count); repo-map inaccuracy (found — see AR-02); accepted-residuals adequacy
(found — see AR-01, AR-04, AR-06).

**Criteria that actually distinguish findings from non-findings**: (1) is the
claim independently checkable against a script/tool run, not just prose; (2)
does the artifact's own non-claims section already cover the gap, in which
case it is `considered_and_defended` rather than a finding; (3) does the gap
create a concrete downstream misroute (a future agent or checker reading the
wrong thing) versus a purely cosmetic imprecision.

## Fitness Reference (Alignment Axis)

Per the commission and `docs/decisions/work_unit_fitness_reference_v0.md`
convention: the goal is Creator-Ledger-memory efficacy toward the MGT target —
future creator-identity/observation/metric work should route through
additive sibling records with accepted residuals named, not remigration. This
PR is scoped only to the scan/receipt contribution to that target, not the
full Ledger goal. Judged against that axis: the PR's exact-match preflight
receipt is real, checkable, additive evidence (a candidate batch plus a
receipt file, not a remigration of the registry), which is consistent with
the additive-sibling-record shape the MGT goal wants. The PR does not itself
claim more than that narrow contribution, which is appropriate scoping.

## Findings

### AR-01 — Registry orientation figure overstates what was actually enumerated

- **Phase**: correctness
- **Confidence**: high
- **Location**: `docs/research/creator_discovery_scan_fragrance_youtube_public_v0.md`, "Registry Orientation" section (lines 61-77)
- **Issue**: The artifact states `profiles_total: 36` and `platform_account_profiles: 36` (both correct, verified against the live JSON), then immediately lists "YouTube handles observed in the current registry before filtering" — a list of exactly 30 handles. The prose implies these 30 handles are the full YouTube-relevant subset of the 36 total profiles, but it never states that 6 of the 36 profiles are non-YouTube platform accounts (the live registry has `platform_account_profiles: 36` across at least 3 platforms per the preflight module's `_ALLOWED_PLATFORMS = {instagram, tiktok, youtube}`). A reader skimming the section could believe 36 YouTube handles were checked, when only 30 were.
- **Evidence**: Live registry script run confirms exactly 30 YouTube handles among 36 total platform-account profiles (script: `python -c` over `creator_profile_current_view_v0.json`, counted `platform == 'youtube'`). The artifact's own list at lines 69-77 has exactly 30 names, matching the true YouTube subset, but the section never explains the 36-vs-30 gap.
- **Strongest defense considered**: the 30-name list is technically accurate (it does say "YouTube handles," not "all handles"), and a careful reader who counts the list would notice 30 ≠ 36. This defense is weak: the artifact spends the entire "Registry Orientation" section foregrounding the `profiles_total: 36` figure and then transitions straight into the YouTube list with no bridging sentence, which is exactly the kind of juxtaposition that produces an unintentional overclaim of coverage.
- **Impact**: Low-to-moderate. It does not change the preflight receipt's correctness (the receipt correctly checks the full registry index, not just the 30-name prose list), but it could mislead a future cold reader into believing this scan enumerated the whole registry rather than 30 of 36 accounts, weakening the "registry orientation is accurate" trust signal the section is meant to provide.
- **minimum_closure_condition**: The Registry Orientation section states the platform breakdown (e.g., "30 of 36 profiles are YouTube accounts; the remaining 6 are other platforms") before or alongside the handle list, so the 36-vs-30 relationship is explicit rather than implied.
- **next_authorized_action**: Owner/CA decision on whether to patch this prose in the same lane (docs-only, low-risk) or accept as a named residual.

### AR-02 — "Refresh" framing in commit message and repo-map entry undersells a full candidate-set replacement

- **Phase**: friction
- **Confidence**: high
- **Location**: commit `511a49ca` ("docs: refresh fragrance youtube creator scan receipt"); `docs/workflows/forseti_repo_map_v0.md` diff (single line changed)
- **Issue**: The commit message and repo-map wording change both read as a light touch-up ("refresh," dropping "a cap-overrun process residual" from the repo-map description). In fact this PR replaces all 10 candidate rows, the entire receipt content, and roughly 40% of the scan artifact's prose with a new self-consistent run. This is a legitimate and arguably better remediation (see Deep-Thinking Frame) than the alternative of patching prose around a tainted batch, but the framing available to a fast reader (commit message, repo-map one-liner) does not signal that scale of change.
- **Evidence**: `git diff origin/main...HEAD --stat` shows 392 insertions / 422 deletions across the scan `.md` and both JSON files — effectively a full rewrite of the data payload, not a "receipt refresh." `git show origin/main:...candidates_v0.json` confirms zero candidate-ID overlap between the old and new batches.
- **Strongest defense considered**: the repo-map entry's new wording ("carries candidate batch and receipt pointers plus capture-request handoff rows only, with no capture, registry mutation, metric refresh, or Silver write") is accurate for the artifact as it now stands, and repo-map entries are meant to describe current state, not diff history. This defense holds for the repo-map file itself (no finding there beyond noting the framing) but does not fully cover the commit message, which is the durable one-line summary of what changed and is somewhat thin for the size of the change.
- **Impact**: Low. No downstream mechanism actually depends on the commit message being descriptive (no checker parses it), but it is a hygiene/trust-signal gap: a future auditor scanning `git log --oneline` for scope would undercount this change's materiality.
- **minimum_closure_condition**: Not a hard closure requirement; this is process friction only. Optional: a fuller commit message or PR description noting "candidate batch and receipt fully replaced to resolve the prior cap-overrun residual" would close it.
- **next_authorized_action**: No action required; optional hygiene note for the owner if they want commit-message practice tightened for future full-batch redos.

### AR-03 — Receipt timestamp ordering is plausible but not cross-verified against actual collection time

- **Phase**: correctness
- **Confidence**: low
- **Location**: `docs/research/creator_discovery_scan_fragrance_youtube_public_preflight_receipt_v0.json`, `generated_at_utc: 2026-07-04T18:30:00Z`; commit timestamp `Sun Jul 5 01:30:51 2026 +0800` (= `2026-07-04T17:30:51Z`)
- **Issue**: The receipt's stated `generated_at_utc` (18:30:00Z) is about one hour *after* the commit's authored timestamp (17:30:51Z UTC+8 normalized). This is not necessarily wrong (the commit could have been authored, then amended, or the local clock used for `--generated-at-utc` could differ from the git author-date clock), but it is an inversion worth flagging since the review attack list asks about receipt provenance/staleness.
- **Evidence**: Simple timestamp arithmetic; `git log -1 --format=%ad` reports `Sun Jul 5 01:30:51 2026 +0800`, which converts to `2026-07-04T17:30:51Z`, one hour before the receipt's declared generation time.
- **Strongest defense considered**: a single commit can be authored after the receipt file content was generated locally (the receipt generation and the git commit are two separate operations that don't have to be monotonic in the direction assumed here) — this is very likely just the normal write-then-commit sequence with the receipt's `--generated-at-utc` flag set slightly ahead, or clock skew between the runner invocation and the eventual commit. This defense is plausible and likely correct.
- **Impact**: Negligible. This is a one-hour, single-commit timestamp curiosity, not a structural staleness problem. Downgraded to low confidence and low impact; included per coverage-first doctrine rather than filtered out.
- **minimum_closure_condition**: Not applicable; no closure needed absent further evidence of a real staleness problem.
- **next_authorized_action**: None required.

### AR-04 — No explicit statement that the new run avoided the prior exploratory-query overrun pattern

- **Phase**: correctness
- **Confidence**: medium
- **Location**: `docs/research/creator_discovery_scan_fragrance_youtube_public_v0.md`, "Scan Moves And Queries" section (lines 79-95)
- **Issue**: The new artifact reports "Exact public queries used: 4 of 8" and "Public source reads used: 14 of 30" as clean, in-cap numbers, but never explicitly states that this run avoided the previous run's untracked-exploratory-query pattern (the prior version's residual said the operator "ran broader exploratory web searches that exceeded the... cap" and "the exact count... was not tracked"). Silently not repeating the problem is good; not saying so leaves a reader unable to distinguish "the same discipline gap happened again but wasn't tracked this time either" from "the discipline gap was fixed."
- **Evidence**: Comparison of `Non-Claims And Residuals` sections between the old and new artifact versions: the old version names the process residual explicitly; the new version's residuals list omits any statement about query-tracking discipline at all.
- **Strongest defense considered**: the new artifact's accounted numbers (4 exact queries producing all candidates, per the query table at lines 84-88) are internally consistent with the candidate provenance (each candidate is explicitly attributed to one of the 4 listed queries), which is itself indirect evidence that no untracked exploration occurred — if it had, the candidates would not cleanly map to the 4 queries. This defense substantially weakens the finding but does not fully close it, since the artifact could still have started from a wider net and post-hoc attributed candidates to the nearest matching query.
- **Impact**: Low-moderate. This affects trust calibration for future scans in this family more than this scan's own correctness.
- **minimum_closure_condition**: A one-line explicit statement such as "unlike the prior run, no exploratory queries outside the 4 listed above were used" would close this residual concern definitively.
- **next_authorized_action**: Optional prose addition; not a blocker given the query-to-candidate mapping already provides indirect support.

### AR-05 — Registry-count discrepancy between the rehearsal record (33) and this scan (36) is never reconciled

- **Phase**: friction
- **Confidence**: medium
- **Location**: `docs/workflows/creator_registry_cold_agent_preflight_rehearsal_v0.md` (records `profiles_total: 33`, dated implicitly before 2026-07-04) vs. this scan's `profiles_total: 36`
- **Issue**: The rehearsal record (a required task source) documents the registry at 33 profiles. This scan correctly uses the live 36-profile registry and even flags that the *static projection* undercounts (33 vs 36), but it does not note that the rehearsal record itself — a sibling required-reading artifact in the same task family — is now stale on the same axis. This is not this PR's artifact to fix, but a future cold reader chaining through the required-sources list could be confused by three different counts (33 static projection undercount per this scan's own text, 33 rehearsal record, 36 live).
- **Evidence**: Rehearsal doc line 73: `profiles_total: 33`. This scan's Source Context line 59: "the current profile-current JSON below says 36 profiles." Both are accurate for their respective times; neither cross-references the other's staleness.
- **Strongest defense considered**: the rehearsal record is dated and explicitly a point-in-time rehearsal artifact (`REHEARSAL_RECORD_V0`), not a live-count source; it is reasonable for it to go stale and this scan is not obligated to patch a sibling artifact outside its own scope. This defense mostly holds — it is why this is a friction finding, not a correctness finding.
- **Impact**: Low. Purely a future-reader orientation cost, not a defect in this PR's own artifacts.
- **minimum_closure_condition**: Not required for this PR; could be closed by a future edit adding a `stale_if` trigger to the rehearsal record noting registry count drift, but that is out of this PR's scope.
- **next_authorized_action**: None required of this PR; optionally spawn a separate hygiene note for the rehearsal record.

### AR-06 — Non-claims list does not explicitly disclose that this is a full redo superseding the prior candidate batch

- **Phase**: friction
- **Confidence**: low
- **Location**: `docs/research/creator_discovery_scan_fragrance_youtube_public_v0.md`, "Non-Claims And Residuals" section (lines 321-340)
- **Issue**: Given the scale of replacement (see AR-02), a future reader diffing only the final artifact (without `git log`) has no signal inside the artifact itself that an entirely different candidate set was tried and discarded before this one. The residuals list covers scan-quality residuals well but not this provenance fact.
- **Evidence**: Absence check across the full Non-Claims And Residuals section; no mention of "supersedes" or "replaces prior candidate batch."
- **Strongest defense considered**: git history is the correct place for this kind of provenance, and the artifact's own retrieval header does not use a `supersedes` field because it is describing itself in its current, single accepted state, not narrating its own edit history — most Forseti research artifacts do not narrate their own prior drafts. This defense is reasonably strong; downgraded to low confidence/low impact accordingly rather than dropped, per coverage-first doctrine.
- **Impact**: Low.
- **minimum_closure_condition**: Not required; optional one-line addition if the owner wants in-artifact provenance continuity.
- **next_authorized_action**: None required.

### AR-07 — Capture-request YAML rows omit `route_binding_state`, a field the checker's schema treats as required

- **Phase**: correctness
- **Confidence**: high
- **Location**: `docs/research/creator_discovery_scan_fragrance_youtube_public_v0.md`, "Capture Requests" YAML block (lines 177-319)
- **Issue**: `.agents/hooks/check_csb_scanning_artifact.py` defines `REQUIRED_CAPTURE_REQUEST_FIELDS` to include `route_binding_state` (along with `capture_request_id`, `source_scan`, `screening_evidence_summary`, `uncertainty_or_access_limits`, `not_requested`, etc.), and `_validate_capture_requests()` checks for it. However, this artifact's capture_request rows only carry `capture_request_id`, `platform`, `public_profile_url`, `display_name`, `candidate_or_observation_ids`, and `creator_registry_match_preflight` — they do not include `source_scan`, `route_binding_state`, `screening_evidence_summary`, `uncertainty_or_access_limits`, or `not_requested` at all. The prior (pre-PR) version of this artifact *did* carry all of these fields (see the pre-PR capture_request block, which included `source_scan`, `route_binding_state: unknown`, `screening_evidence_summary`, `uncertainty_or_access_limits`, and `not_requested`). This PR's rewrite silently dropped that schema conformance.
- **Evidence**: Checker source lines 115-127 (`REQUIRED_CAPTURE_REQUEST_FIELDS`) and lines 867-873 (`_validate_capture_requests` missing-field check). Direct comparison of this PR's capture_request rows against the pre-PR version's capture_request rows (both retrieved via `Read`/`git show`) confirms the new rows are missing 5 of the 11 previously-present fields.
- **Strongest defense considered**: the checker did not actually fail (`check_csb_scanning_artifact.py --changed --diff origin/main` returned `PASS`), so in practice this gap has no enforcement consequence today. Investigating why: `_records(blocks, "capture_request_id")` only extracts YAML records that contain the `capture_request_id` key; `_validate_capture_requests()` is only called from `validate_text()`, which is only invoked when `looks_like_csb_first_scan_artifact()` returns true (line 1172) — and this artifact returns `False` for that check (confirmed live: `looks_like_csb_first_scan_artifact: False`) because it lacks the CSB-first markers (`commission_id:`, etc.). Since this artifact is classified purely as a `creator_registry_preflight_artifact` (not CSB-first), `validate_text()` and therefore `_validate_capture_requests()` never run against it at all — only `_validate_creator_registry_preflight_shapes()` and `_validate_creator_registry_receipt_rows()` run, which check the `creator_registry_match_preflight` sub-block only, not the outer capture_request field completeness. This defense holds completely: the missing fields are real but currently outside this checker's applied validation path for this artifact classification, so there is no false green here — the checker is correctly scoped, but the *artifact* has regressed on a schema that a CSB-first sibling artifact would enforce.
- **Impact**: Moderate. If this same scan/candidate content were ever reclassified as (or copied into) a CSB-first scan artifact, or if a future stricter checker version extends `_validate_capture_requests`-style field checks to Creator-Registry-only artifacts, these capture_request rows would fail. It also reduces this artifact's own internal completeness relative to its own prior version and relative to the handoff prompt's documented output contract (which asks for `source_scan`-equivalent and `uncertainty_or_access_limits`-equivalent fields per candidate row, albeit in a slightly different row shape).
- **minimum_closure_condition**: capture_request rows either (a) add the missing fields (`source_scan`, `route_binding_state`, `screening_evidence_summary`, `uncertainty_or_access_limits`, `not_requested`) to match the schema the checker enforces for CSB-first siblings and the prior version of this same artifact, or (b) the artifact explicitly notes that this simplified capture_request shape is intentional for Creator-Registry-only (non-CSB) scans and is not expected to satisfy `REQUIRED_CAPTURE_REQUEST_FIELDS`.
- **next_authorized_action**: Owner/CA decision on whether to patch the capture_request rows in the same lane (mechanical, low-risk addition of 5 fields per row) or accept as an explicitly named residual given the checker does not currently gate on it for this artifact class.

## Considered And Defended

- **Cap-perfect-but-unsupported claim** (attack #1): considered; the artifact's own accounting (4/8 queries, 14/30 reads, 10/10 candidates) is internally consistent, each candidate is attributed to one of the 4 named queries, and the receipt's `input_index` values line up 0-9 with the candidate batch's declaration order. No unsupported cap-perfect claim found.
- **Non-public or non-fragrance candidates** (attack #2): considered; spot-checked candidate metadata descriptions in the artifact's "Public metadata basis" column against the channel handles — all ten describe fragrance/perfume review content, and all URLs are public `@handle` YouTube channel pages (no login-gated content cited).
- **Known registry account slipping through as new_candidate** (attack #3): considered and checked mechanically — ran a script cross-referencing all 10 candidate handles and all 10 `platform_public_account_id_or_none` values against the live registry's 30 YouTube handles and their channel IDs; zero collisions found. The receipt's `existing_matches: 0` is correct.
- **Receipt/candidate/artifact disagreement on row ids, handles, totals** (attack #4): considered; cross-checked candidate_id, handle, platform_public_account_id_or_none, and decision/action_status/can_start_new_capture between the scan `.md` table, the candidate JSON, and the receipt JSON for all 10 rows — all agree.
- **Stale/non-canonical receipt path** (attack #5): considered; ran the actual checker's auto-detection and content-verification against this exact path and confirmed it is the path the checker resolves and validates (`--changed --diff origin/main` passes; `looks_like_creator_registry_preflight_artifact` returns True for this file).
- **Capture-request rows phrased as authorization** (attack #6): considered; the artifact explicitly states "These are handoff rows only. No capture was run" immediately before the YAML block, and the Non-Claims section reiterates "not capture execution." No authorization-phrasing defect found.
- **Overclaim of fuzzy identity, cross-platform identity, buyer proof, registry insertion, Silver write, capture execution, creator-memory efficacy** (attack #7): considered; the Non-Claims And Residuals section explicitly disclaims all of these categories, and the "Next Step" section explicitly defers to "owner adjudication" before any capture lane, not a claim of readiness.
- **Erasure of useful prior evidence rather than replacing a residual with a better receipt** (attack #8): considered at length (see Deep-Thinking Frame and AR-02); concluded this is a legitimate full redo with a strictly stronger receipt (channel-ID-anchored identity keys vs. handle-only), not an erasure of evidence that was itself sound — the erased batch was the one carrying the untracked cap-overrun taint, so replacing it is the correct remediation direction, not a violation.
- **Static-projection-as-source-truth** (attack #9): considered; the artifact explicitly states the static projection is stale (33 vs 36) and explicitly uses the live JSON as the counted source, exactly the correct orientation-vs-truth handling.
- **Repo-map inaccuracy/missing freshness-routing implication** (attack #10): considered; the repo-map one-line description was checked against the current artifact content and found accurate for current state (see AR-02 for the softer commit-message framing concern, which is friction, not inaccuracy).
- **Stale duplicate candidate/receipt paths or root-level receipt references misrouting future reviewers** (attack #11): considered; `check_map_links.py --strict` and `check_handoff_pointers.py --strict` both pass with 0 findings against `origin/main`; no duplicate or root-level receipt path was found.
- **Accepted residuals too weak for the MGT goal, especially prose-first enforcement and deferred receipt-content verification** (attack #12): considered; the checker's receipt-content verification is live and passing (not merely shape-only — confirmed by reading `check_csb_scanning_artifact.py`'s `_validate_creator_registry_receipt_rows` and `_compare_creator_registry_receipt_result` functions, which do field-by-field comparison against the actual receipt JSON), so the "deferred receipt-content verification" residual named in the *usage note's* DCP receipt is already resolved for this artifact class; the remaining accepted residuals (exact-match-only, no cross-platform identity, no source-adequacy proof) are consistent with the MGT accepted-residuals requirement and are named, not silently dropped.

## Validation Commands Run

| Command | Result |
| --- | --- |
| `git status --short --branch` | `## codex/fragrance-youtube-creator-scan...origin/codex/fragrance-youtube-creator-scan`; clean |
| `git diff origin/main...HEAD --stat` | 4 files changed, 392 insertions(+), 422 deletions(-) |
| `git diff origin/main...HEAD -- <4 files>` | Reviewed in full (see Source-Read Ledger) |
| `python .agents/hooks/check_csb_scanning_artifact.py docs/research/creator_discovery_scan_fragrance_youtube_public_v0.md --strict` | `PASS` |
| `python .agents/hooks/check_csb_scanning_artifact.py --changed --diff origin/main` | `PASS` (confirms actual CI-equivalent auto-detection path) |
| `python -m json.tool docs/research/creator_discovery_scan_fragrance_youtube_public_candidates_v0.json` | valid JSON |
| `python -m json.tool docs/research/creator_discovery_scan_fragrance_youtube_public_preflight_receipt_v0.json` | valid JSON |
| `python .agents/hooks/check_map_links.py --strict` | `OK (0 findings)`; 34 annotated nonresolving (pre-existing debt, not failures) |
| `python .agents/hooks/check_full_gt_claims.py --strict docs/research/creator_discovery_scan_fragrance_youtube_public_v0.md docs/workflows/forseti_repo_map_v0.md` | `OK -- no unballasted full-GT claim language in scope` |
| `python .agents/hooks/check_retrieval_header.py --changed --strict` | ran, no findings printed (silent pass) |
| `python .agents/hooks/header_index.py --strict --base origin/main` | `OK -- 1 changed durable .md file(s) all have headers and are map-reachable` |
| `python .agents/hooks/check_handoff_pointers.py --strict --base origin/main` | `OK (0 findings in 2 changed file(s))` |
| `python .agents/hooks/check_dcp_receipt.py --strict --base origin/main` | `OK -- every real receipt in the changed .md files is shape-valid` |
| sha256 cross-check of registry file vs. receipt's declared `sha256` | match confirmed (`a0998cb1...ac1e49`) |
| Handle/channel-ID collision cross-check (10 candidates vs. 30 live YouTube registry handles/IDs) | 0 collisions |

No validation command was skipped; none failed.

## Not-Proven Boundaries

- This review does not prove discovery search adequacy, fuzzy-duplicate absence, cross-platform person identity, buyer proof, or creator-memory efficacy at the Ledger level — none of these were claimed by the artifact and none are in scope for this review to certify.
- This review does not certify the actual real-world existence, activity level, or content quality of the 10 candidate YouTube channels; it only verifies internal artifact consistency, registry cross-reference correctness, and checker-pass status. Confirming the channels are genuinely active, English-language, no-login-visible fragrance-review channels would require live browsing, which was out of scope for a read-only review of recorded claims (and the commissioning prompt explicitly restricts this review from source scraping beyond reviewing recorded claims).
- `reviewed_by`/`authored_by` are operator-supplied factual provenance records per the commissioning instructions (`Claude Sonnet 5 (claude-sonnet-5)` / `gpt-5-codex`); this is not a runtime-model recommendation or ranking.
- De-correlation basis: this review runs under the commissioning session's confirmed de-correlation determination (Claude vs. the PR's OpenAI GPT-5 Codex authoring family), which this review accepts as already resolved per the delegated instructions; this review did not re-verify that determination independently.

## Closing Adjudication Note (For The Commissioning CA)

Per `.agents/workflow-overlay/communication-style.md` Review Adjudication Next
Step: none of the 7 findings here are blocking. AR-01 and AR-07 are the two
findings with concrete, cheap, self-closable fixes (prose addition; 5-field
YAML addition per capture_request row) that a commissioning CA could close
in the same turn if it chooses to patch rather than accept as residuals. The
remaining findings (AR-02 through AR-06) are process/friction observations
that do not require action. No unresolved material issue blocks merge;
recommended land step is the owner's standard commit/push/PR/merge flow for
this already-open PR, with material moves limited to the AR-01/AR-07
patch-or-accept decision.
