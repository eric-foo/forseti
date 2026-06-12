# Company-Aggregate Forward-Signal EDGAR Slice — Cross-Vendor Code Review + CA Adjudication (v0)

```yaml
retrieval_header_version: 1
artifact_role: Review output (cross-vendor delegated code review + home-model adjudication)
scope: >
  Durable record of the cross-vendor (OpenAI/GPT-5-Codex) adversarial code review of the
  company-aggregate forward-signal EDGAR slice (STEP-01..06) and the CA (Claude) adjudication
  of its findings. Decision input only; not validation, readiness, or formal review authority.
use_when:
  - Reviewing what the cross-vendor pass found on the EDGAR slice and which findings the CA kept.
  - Before committing the slice (the remediation + bounded recheck gate lives here).
authority_boundary: retrieval_only
```

## Commission & provenance

- Lane: delegated review-and-patch (provisional, opt-in) — `.agents/workflow-overlay/delegated-review-patch.md`.
- Access mode: `repo`, source-read-only (reviewer read the real working tree in place; returned findings only; CA applies).
- De-correlation: cross-vendor **discovery** bar — `reviewed_by: gpt-5-codex` (OpenAI) vs `authored_by: claude-opus-4.8` (Anthropic). Who-constraint satisfied; not a runtime-model claim.
- Target: the 11 source + 9 test files of the slice (STEP-01..06), uncommitted on `ecr-sp3-timing-deriver-slice1`; confirmed by SHA256 (20/20).
- Source context: `READY`; reviewer independently re-ran the offline suite → `98 passed in 0.73s`.
- Output posture: advisory findings-only. No formal PASS/validation/readiness.

## Findings & CA adjudication

| ID | Reviewer severity | CA verdict | CA severity | File |
|----|------|--------|------|------|
| F-01 | critical | **ACCEPT** | critical | edgar_extraction.py |
| F-02 | major | **ACCEPT** | major | edgar_extraction.py |
| F-03 | major | **ACCEPT (fix modified)** | minor | projection.py |
| F-04 | major | **ACCEPT** | major | edgar_discovery.py |
| F-05 | major | **ACCEPT** | major (practical: low in single-thread CLI) | edgar_derivation.py |

All five verified against the actual code. The identity/honesty core was **not** breached — see Non-findings.

### F-01 — Extractor emits KNOWN headcount for non-headcount "N employees" phrases (ACCEPT, critical)
Confirmed: `_PATTERN` matches any `N [qualifier] <employee-noun>` with no workforce-total/as-of predicate, so `"During 2023, we hired 5,000 employees"` returns `found=True, count_int=5000`. A hiring/layoff/regional/segment/generic-"people" count is then mapped to a KNOWN `employee_count` — a **field-level breach of the VisibleFact honesty invariant** (the source stated the number, but not as the measured field). The surrounding non_claims/"not validated" labels do *not* rescue the field-level KNOWN claim. This is the slice's core value prop, so critical stands.
- **Fix (accepted):** make acceptance conservative — require a workforce-possession/as-of positive cue (had/have/employ(ed)/workforce/headcount/as of …) in the preceding clause AND exclude event verbs (hired/added/terminated/laid off/reduced/…) and scoping ("in our … segment/region/division", "represented by", benefit-plan) in the local window. Ambiguous/un-cued phrases become an **honest miss**, never a guessed KNOWN. This is the honest-miss direction the slice already espouses.
- **Trade-off (disclosed):** the extractor gets more conservative — some genuine totals in unusual phrasings become honest misses (recorded), and a few existing tests whose phrasings were bare or regional change meaning (e.g., two regional counts → not-found rather than "ambiguous", which is *more* honest).
- **minimum_closure_condition:** KNOWN only when the matched phrase is decision-sufficiently a workforce/headcount/as-of total; event/regional/segment/generic-people counts → named absence/ambiguity.

### F-02 — Basis misclassifies scoped full-time as total (ACCEPT, major)
Confirmed: `_detect_basis` scans a 50-char pre-window and checks `total` (priority 3) first, so `"a total of 5,200 full-time employees"` → `basis="total"` (the grammatical "a total of"), not `full_time`. Because basis drives AR-03 primary selection, a scoped full-time count can be promoted as the canonical total basis.
- **Fix (accepted):** derive basis from the matched qualifier/noun structure (the `between`+`noun` groups), and do not treat the grammatical "a total of N" as the `total` measurement basis (require `total` to qualify the noun, e.g. "total employees"/"N total employees").

### F-03 — Projection collapses quality-disagreeing observations (ACCEPT, fix modified → minor)
Confirmed: `_value_signature` omits `value_quality`, so same-period observations with equal int+basis but different quality (exact vs approximate) collapse to one point whose quality is whichever accession sorts first (order-dependent).
- **CA modification:** the reviewer's literal "add quality to the signature" would turn *agreeing values* into false conflicts (dropping a perfectly good value over an exact/approximate label) — net-negative. **Modified fix:** on collapse, set the point's `value_quality` deterministically to the most conservative (if any contributor is `approximate`, the point is `approximate`). This removes order-dependence and surfaces the disagreement honestly while preserving the agreed value. Downgraded to **minor** (the value agrees; only the quality label diverged).

### F-04 — Malformed submissions metadata coerced into durable stringified facts (ACCEPT, major)
Confirmed: `select_latest_filing` validates only `primaryDocument`; `accessionNumber/reportDate/filingDate/form` are copied as-is, then `discover_filing` does `str(row[...])` → `reportDate=None` becomes `period_of_report="None"`, which is non-blank so it **passes `EdgarObservationKey.reject_blank`** and enters the durable key + trend ordering as a fake period.
- **Fix (accepted):** in `select_latest_filing`, require `accession_number`/`period_of_report`/`filing_date` to be non-blank strings (and `period_of_report`/`filing_date` to be ISO-date-shaped); skip malformed rows rather than coercing — no `None`/garbage into a durable fact.

### F-05 — Re-hash vs parse TOCTOU window (ACCEPT, major; practical low)
Confirmed: `derive_edgar_headcount_observation` calls `hash_file(raw_path)` then a *separate* `raw_path.read_text(...)`, so the verified bytes and the parsed bytes are two reads — a concurrent mutation in between defeats the "parser trusts verified bytes" invariant. (The same pattern exists in out-of-scope `reddit_consolidation/consolidator.py` — flagged there, not edited.) Practical risk is low in the single-threaded local CLI, but the fix is cheap and makes the invariant actually hold.
- **Fix (accepted):** read the bytes **once** (`read_bytes`), hash those bytes, and decode *those same bytes* for extraction — binding verification and parse to identical bytes.

## Non-findings (reviewer-confirmed sound — cross-vendor corroboration)

- **AR-05 identity-leak guard enforced** in both `ResolutionOutcome` and `CompanyHeadcountProjection`: unresolved-with-`entity_key` rejected; resolved-without-nonblank-`entity_key` rejected.
- Default `PassthroughNullResolutionMap` authors no canonical identity; leaves projections unresolved.
- Derivation performs manifest conformance + current-version checks and has a path-escape guard.
- Observation key shape carries no `measurement_basis`; blocks a silent `employee_count_int` when `employee_count` is not KNOWN.

→ The high-lock-in identity/honesty architecture (AR-04/05/06/07) survived cross-vendor discovery. All defects are in the v0 extraction + plumbing.

## Not-proven boundaries

- Out-of-scope infra internals not audited beyond the slice's visible assumptions.
- No live SEC calls / real-filing extraction tested (offline by design).
- "98 passing" proves the current suite's expectations, not invariant completeness (F-01/F-03 were honesty gaps with no failing test — a test-adequacy gap the review closes).
- Concurrency beyond the static TOCTOU (F-05) not proven.

## Remediation status & gate

- **Applied (CA, claude-opus-4.8), owner-authorized "apply all 5 + recheck":**
  - F-01 → conservative `_is_workforce_total_context` + qualifier/possession/event/scoping gates in `edgar_extraction.py` (+6 guard tests).
  - F-02 → qualifier-based `_detect_basis(between, noun)` in `edgar_extraction.py` (+1 guard test).
  - F-03 → conservative, deterministic `_collapse_quality` in `projection.py` (+1 guard test).
  - F-04 → non-blank + ISO-date validation of durable facts in `edgar_discovery.py` `select_latest_filing` (+3 guard tests).
  - F-05 → read-once `read_bytes` → `sha256_bytes` + decode the same bytes in `edgar_derivation.py`.
  - 2 regional-phrasing ambiguity tests rewritten to clean conflicting-totals (the conservative extractor now correctly treats regional counts as honest misses).
- **Validation:** `108 passed` (98 + 10 new guard tests), `orca-harness/.venv`.
- **Bounded same-vendor recheck (required gate — SATISFIED):** a lower-tier same-vendor actor (`recheck_by: claude-sonnet`, mechanical-tier — a who-constraint, not a model recommendation) verified closure + scanned the touched delta. Verdict **ALL_CLOSED_NO_NEW_ISSUES**; `108 passed` re-confirmed; no new blocker/major. One F-01 residual noted (a possession cue admits a plain "N people" count, e.g. "our team has 5,000 people") — within the recorded regex residual, honest-miss-leaning, accepted for v0.
- **CA keep decision:** all 5 **kept**. The slice is hardened. **Commit is on the table at the owner's go** (owner drives commits); outstanding commit-time items: the decision record's "PROPOSED → built/green" status update, the repo-map entry / `repo-map-ack:` for the new units, and burning the consumed precompact packet.

## Review-use boundary / non-claims

Findings are decision input only — not approval, validation, readiness, mandatory remediation, or patch authority. `reviewed_by: gpt-5-codex`; `authored_by: claude-opus-4.8`; `de_correlation_bar: cross_vendor_discovery`. The vendor identities are factual provenance, never a runtime-model recommendation.
