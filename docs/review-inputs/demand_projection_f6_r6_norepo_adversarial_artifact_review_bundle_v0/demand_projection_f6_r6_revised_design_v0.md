# Demand-Projection Revised Architecture Decision — F6 Multi-Adapter Dispatch + R6 Conflict-Loud Dedup (v0, DRAFT UNDER REVIEW)

```yaml
retrieval_header_version: 1
artifact_role: Review input artifact (Review prompt role binding, docs/review-inputs/)
scope: >
  Revised, pre-build architecture decision for the demand-projection layer's two unresolved
  holes (F6 single-winner adapter dispatch; R6 value-blind dedup) plus the contract-closure
  survivor set, produced by the 2026-06-11 three-lens focused architecture pass and home-CA
  synthesis. Prepared as the verbatim target of a no_repo de-correlated adversarial artifact
  review. NOT an accepted decision record; supersedes nothing.
use_when:
  - Performing the commissioned de-correlated adversarial artifact review of this design.
  - Adjudicating that review's findings before any build authorization.
authority_boundary: retrieval_only
status: DRAFT — authored design awaiting de-correlated cross-vendor review; nothing herein is
  built, ratified, merged, validated, or accepted.
authored_by: claude-fable-5 (Anthropic) — home/CA lane, 2026-06-11
```

## 0. What this artifact is

The capture-then-project demand-projection lane ran a de-correlated cross-vendor review that
left two unresolved holes: **F6** (single-winner adapter dispatch can produce a FALSE review-
velocity GAP) and **R6** (value-blind dedup silently drops a conflicting value). A three-lens,
read-only focused architecture pass (one lens per: dispatch, dedup, contract closure) was run
on 2026-06-11; the home CA verified every load-bearing citation directly against the lane
worktree and synthesized this revised design. The commissioning gate requires this design to
survive one more de-correlated cross-vendor check **before any build**. This document is the
review target for that check.

## 1. Fitness reference (goal + observable success signal — attack this too)

**Goal:** make the demand-projection THREE-VALUED HONESTY CONTRACT actually hold on the proven
path, at smallest-complete scope: every `(entity, signal_type, period)` coordinate resolves to
exactly one of **OBSERVATION** (real extracted value, including a genuine zero) / **typed GAP**
(coordinate addressed, no value, typed `no_data` carrier reflected in JSON + receipt + counts) /
**REFUSAL** (no artifact at all, loud failure) — with **no silent fourth outcome** (silent drop,
silent zero, fabricated value, partial artifact) and **no FALSE GAP** (a GAP emitted when the
value was present in the captured bytes but the pipeline never looked).

**Observable success signal:** the invariant set I1–I7 (§6.3) holds as testable properties over
the emitted artifacts, and the six commissioned pass signals (§2–§7 here) are each answered
with cited evidence. The reviewer must also attack whether this goal and signal are themselves
right — never treat them as a pass-if-matches bar.

## 2. System under design, doctrine, and already-accepted constraints

**System:** a capture-then-project engine projects a preserved web-capture packet (raw bytes +
manifest) into dated demand observations (e.g. reviewCount at a Wayback snapshot timestamp),
feeding a "durable vs hollow demand" persistence signal: 4–6 archived snapshots differenced
into a quarterly review-count curve. **Honesty doctrine:** a miss FAILS LOUD — no fabrication,
no fake-success artifact, no silent zero; "emitted" = internally-consistent-as-served; NO LLM
in the projection core. **Proven path:** Target retailer product pages, JSON-LD
`aggregateRating`, single adapter, 4–6 Wayback snapshots. **Multi-surface ambition:** the
embedded (Apollo-style) + trend adapters on additional surfaces.

**Already-accepted (this design sits WITHIN them; the review must not relitigate them but may
flag conflicts with them):**
- **D1:** discriminated ExtractionResult union + typed `no_data` GAP carrier reflected in
  JSON + receipt + counts; zero-extraction → typed GAP (not REFUSAL); OBSERVED-status-with-
  empty-drafts → raise.
- **D2:** first-party import-closure walk + literal-dynamic detector + narrowed no-LLM claim.
- **P1+:** atomic JSON+receipt write.
- **F4:** flagged observations stay in the record but non-relocated/low-confidence points are
  ENFORCED-excluded from `_series_summary` (curve-eligibility filter) + a central
  flag→confidence floor.
- **M-8:** jsonld empty-string fix.

## 3. Signal 1 — decisive sub-question, VERIFIED: does the proven path contend?

**Code level: YES — contention is constructible (home-verified citations).** Dispatch is
first-match-wins with no trace of other claimants (`projector.py:255-265`); registry order is
jsonld → trend → embedded (`registry.py:22-26`). The F6 premise is verbatim in source: the
jsonld adapter claims a page on a Product node with `"offers" in node or "aggregateRating" in
node` (`adapters/jsonld_demand.py:53-55`), so an offers-only Product + embedded-cache page is
claimed by jsonld and the embedded adapter never runs — a FALSE review GAP under D1 if the
count lives only in the cache. Three overlap pairs exist: jsonld×embedded (a real page carrying
both anchor families is documented in the lane's own Ulta recon — decision record lines
166-171, 193-203), trend×embedded and trend×jsonld via the trend adapter's predicate, which is
a bare substring check `"timelineData" in sample_text` over full multi-MB page text
(`anchors.py:43-45`, `adapters/trend_series_demand.py:30-32`). Aggravating present-tense fact:
trend claiming an HTML page yields `parse_json_lenient(html) → None → []`
(`trend_series_demand.py:38-40`), which today writes a **zero-observation success artifact**
(no emptiness check between extract and write, `projector.py:147-183`) — a doctrine violation
that exists before any Target evidence. The registry's "adapters bind to disjoint anchor
vocabularies… order is not contended" comment (`registry.py:4-6`) is stale and contradicted by
its own lines 19-21 and by the Ulta recon.

**Proven path (Target/jsonld/Wayback): UNGROUNDED — and structurally bounded.** No Target
capture, fixture, or spec exists anywhere in the lane worktree (grep for
`target.com`/`TARGET_SPEC`/`__PRELOADED_QUERIES__`: zero hits; `PRODUCT_SPECS = [ULTA_SPEC]`,
`specs.py:32`; the live validation packets were throwaway probes, decision record line 332).
Structure bounds exposure: an archive packet has exactly ONE extractable candidate
(`archive_snapshot_body.bin`; metadata files excluded, `projector.py:474-476`, archive runner
lines 97/151-164), and for the embedded adapter to contend, the snapshot must carry both a
state marker (`locators.py:32-49`) and ULTA_SPEC's key-form `"productId":`/`"productName":`
signature (`recognition.py:160-171`). Whether any Target snapshot era satisfies that — or
contains the literal `timelineData` — is NOT decidable from the worktree, and is deliberately
not asserted. **Deciding evidence (named, not yet captured):** one real Target hero-SKU packet
per snapshot era, grepped for the three marker families and the JSON-LD nesting shape.

## 4. Signal 2 — F6 dispatch design: LOUD-ON-CONTENTION GUARD (claim-matrix form), union deferred

**Choice rationale, tied to §3:** the guard is correct under BOTH outcomes of the ungrounded
empirical question — if Target never contends, the guard never fires; if it does, the run
refuses loudly and the recorded claim matrix IS the evidence that sizes the union. Two further
grounds: **(a)** full multi-adapter union is dishonest-by-construction today — cross-adapter
coordinate identity does not exist (jsonld identity = display name, `jsonld_demand.py:131`;
embedded identity = productId, `recognition.py:99`; entity canonicalization is an explicit
NON_CLAIM, `projector.py:48`), so a union conflict-merge would systematically miss true
collisions and fabricate false ones; **(b)** per-signal arbitration is the wrong cut — both
jsonld and embedded emit BOTH signal families (`jsonld_demand.py:131/216`;
`recognition.py:103/143`), so an ownership map is hand-maintained config that recreates F6 as a
config-induced false GAP.

**Mechanics (no adapter changes; the `DemandSignalAdapter` Protocol is untouched):**
- Replace `_select_adapter` with a claim-matrix resolver probing each adapter × each candidate
  file (single-entry `samples` dicts — API-compatible with all three `match()`
  implementations).
- **0 claims** → `no_eligible_adapter` REFUSAL (unchanged). **Exactly 1 claim** → proceed;
  artifact + receipt gain a `dispatch` block `{mode: single_uncontended, claims, not_run}`.
  **≥2 claims** → raise `DemandProjectionFailure("adapter_dispatch_contention")` enumerating
  every (adapter, file) claim — a clean REFUSAL, since adapter selection (`projector.py:135`)
  precedes `mkdir` (line 160) and both artifact writes (lines 176-177; ordering home-verified).
- **Operator pin:** a new `--adapter` runner flag onto the existing, already-documented
  `adapters=` parameter (decision record lines 170-171) → proceed under contention with
  `mode: operator_pinned`, the FULL claim matrix still recorded, and every D1 GAP emitted by a
  pinned run carrying a `gap_under_operator_pin_with_suppressed_claims` flag. The pin
  authorizes proceeding; it never erases the record.
- **GAP semantics narrowed:** a typed GAP means "no value found by the winning adapter under
  uncontended (or pinned-and-recorded) dispatch among registered adapters" — never "value
  absent from the captured bytes".
- Registry comment rewrite (order is iteration order, never a semantic tiebreaker; overlap
  refuses loudly); `DEMAND_PROJECTION_SCHEMA_VERSION` bump; contention fixtures written as
  dispatch-mode tests (asserting the typed code) so the union phase flips expectations without
  rewriting fixtures.

**Files touched:** `projector.py` (resolver + dispatch block + receipt section + NON_CLAIMS
line), `registry.py` (comments only), `models.py` (schema version), `run_demand_projection.py`
(`--adapter` flag), `tests/unit/test_demand_projection.py` (two-anchor fixture → refusal;
pinned → recorded matrix; single-anchor → `single_uncontended`; jsonld page containing literal
`timelineData` → contention).

**Named honest residual:** the guard polices BETWEEN adapters only — within-winner
under-extraction is H2/H6 territory (§6). **Lock-in:** deliberately low; union later replaces
one resolver function and extends the `dispatch` block (mode/claims/not_run kept minimal).
**Rejected alternatives:** full union (wins when a real contended surface is demonstrated, or
when the second spec/surface lands — at which point identity bridging must be solved first);
per-signal ownership map (wins only if signal families ever become one-producer-per-surface
and the map is derivable from specs rather than asserted).

## 5. Signal 3 — R6 dedup design: centralized conflict-loud draft resolution, typed conflict record

**Current state (home-verified):** two value-blind silent-drop sites — the recognizer's `seen`
set skips a duplicate-identity node BEFORE its review value is even read, with the winner
determined by a LIFO stack walk, i.e. traversal-arbitrary (`recognition.py:78, 88-90,
174-185`); and the embedded adapter's `(signal_type, identity)` set
(`adapters/embedded_product_demand.py:40, 48-51`) — both leaving ZERO trace. Mirror hazard:
jsonld and trend have NO dedup at all (`jsonld_demand.py:63-82`), so duplicate Product blocks
emit unmarked twin observations at one coordinate. The finalized `DemandObservation` DROPS
`identity` (`models.py:120-136` vs draft `models.py:177`; `projector.py:311-326`), so the draft
level is the last identity-bearing point.

**Design:**
- **Site:** one canonical `_resolve_drafts((adapter_name, draft)…)` step in the projector,
  between extract (`projector.py:147`) and finalize (`projector.py:148-158`). The
  adapter-local `seen` sets are REMOVED — they destroy the conflicting evidence before the
  central step can see it; adapters become pure emitters. This covers jsonld/trend for free
  and natively covers cross-adapter collisions under any future union.
- **Identity key:** `(identity, signal_type, timestamp)` — identity not entity (preserves
  DP-005: two products sharing a display name are two products); timestamp keeps trend series
  points apart.
- **Comparison:** exact equality on the payload tuple `(entity, value, value_kind, unit,
  granularity)` — NO comparator-side normalization (normalization already happened once at
  extraction; the M-8 empty-string history is exactly a normalization edge biting). The chosen
  failure direction: a false CONFLICT is loud and recoverable; a false EQUAL is silent and
  prohibited.
- **Representation:** same identity + same payload → suppress duplicate, counted in
  `counts.duplicates_suppressed` (aggregate only; deliberately NO informational flag on kept
  observations so F4's flag→confidence floor cannot misread bookkeeping as a quality defect).
  Same identity + DIFFERENT payload → a **typed `conflict` record**, a discriminated sibling of
  D1's `no_data`, carrying ALL competing payloads with per-competitor provenance (including
  per-competitor snippet relocation reusing the `_finalize` logic). The coordinate yields NO
  observation.
- **Why not the alternatives:** flag+downgrade still serves an arbitrary winner inside
  `observations` — a fabricated choice; and the differencer must read raw observations because
  `_series_summary` rows carry NO values (home-verified, `projector.py:387-400`), so F4's
  series-level exclusion cannot fence the curve by itself. Refusal annihilates a whole
  snapshot's honest coordinates (the live Ulta projection carried 43 observations) for one
  stale cache slot, and conflates per-coordinate data ambiguity with projection-integrity
  failure, which D1 already separates.
- **Visibility:** `counts.conflicts` (coordinate count) + `counts.duplicates_suppressed`;
  receipt headline + `## Conflicts` section; runner stdout `conflicts=N`.
- **Named boundary:** cross-vocabulary aliasing (the same physical product as jsonld name-key
  vs embedded productId-key) is NOT detected — that is entity resolution, an explicit
  non-claim of this layer. Receipt wording must scope "conflicts: 0" to identity-key
  collisions.
- **Integration constraints:** land the `conflict` variant TOGETHER with D1's union
  serialization (one schema rev, not two); D1's OBSERVED-with-empty-drafts raise must key on
  pre-resolution drafts so "all drafts conflicted → 0 observations + N conflicts" is a valid
  loud artifact, not a fake-empty success.

**Files touched:** `models.py` (conflict carrier as D1-union sibling), `projector.py`
(`_resolve_drafts` + `_finalize_conflict` + counts + receipt), `recognition.py` (delete seen
set, docstring), `adapters/embedded_product_demand.py` (delete seen set),
`tests/unit/test_demand_projection.py` (conflict fixtures; existing equal-value Ulta fixture
keeps its counts with `duplicates_suppressed: 2`), `run_demand_projection.py` (stdout line).

## 6. Signal 4 — contract closure: does NOT yet hold; survivor set (worst first)

F6+R6 close the two commissioned holes, but closure fails without the following. H1, H3, H5,
H6, H7 chains and the dedup/dispatch mechanics were verified by the home CA by direct read;
test-file line citations are lens-reported (marked †).

- **H1 — CRITICAL (fully home-verified): archive observations are dated to FETCH time, not the
  Wayback snapshot time.** Chain: the jsonld adapter dates every draft from
  `packet.timing.capture_time` (`jsonld_demand.py:240-244`); the archive runner sets that from
  `metadata["capture_timestamp"]` (`runners/run_source_capture_archive_packet.py:119`,
  `310-314`); that metadata field is `utc_now_z()` at HTTP-fetch time
  (`source_capture/adapters/direct_http.py:164`, `anti_blocking_http.py:216`). The snapshot's
  own timestamp survives only as prose (`"Archive.org snapshot timestamp {ts}"`, runner
  258-261) and in metadata files the projector EXCLUDES from candidates
  (`projector.py:474-476`). Net: 4–6 snapshots spanning years all emit HIGH-confidence
  observations stamped ~fetch-date — the quarterly curve collapses to one period, silently.
  This is the proven path's stated purpose failing by construction, and NONE of
  D1/D2/P1+/F4/M-8/F6/R6 touches it. **Fix shape:** a typed snapshot-time field in the packet
  (archive-runner side — crosses into the capture lane) + mode-aware dating in the projection
  layer (ARCHIVE_HISTORY → snapshot time, else typed dating-GAP/refusal). **Open question for
  this review:** which side of the lane boundary the typed field lands on.
- **H2 — HIGH: no coordinate-universe enumerator.** Partial extraction returns `None` and the
  coordinate silently never exists (`jsonld_demand.py:110-121, 184-188`;
  `recognition.py:130-134`; trend per-point `trend_series_demand.py:88-95`) — one case is even
  locked by a test that must be inverted under D1 (†test_demand_projection.py:258-264). D1
  needs an owner for "expected": adapter-declared universe (jsonld: per matched Product ×
  {review, presence}; embedded: per recognized product × presence + review-iff-spec; trend:
  per timeline index); the projector enforces exactly-one-record-per-coordinate.
- **H3 — HIGH (home-verified): the proven-path adapter silently truncates floats.** jsonld's
  `_as_int_string` does `str(int(raw))` for every float (`jsonld_demand.py:253-254`) —
  `1234.9 → "1234"`, high confidence, no flag — while the recognizer's copy carries
  non-integral floats verbatim + flag (`recognition.py:225-230`). DP-003 fixed only the
  embedded copy. Fix: one shared helper with the recognizer's semantics.
- **H4 — HIGH: F4 as scoped cannot protect the differencer.** `_series_summary` rows carry no
  values (`projector.py:387-400`), so the value-consumer must read raw `observations`, where
  flagged points sit by design. Eligibility must be a SERIALIZED per-observation
  `curve_eligible` computed only at the central `_finalize` floor; conflict/gap records never
  enter series rows or `by_signal_type` counts.
- **H5 — HIGH (home-verified): P1+ needs a both-or-neither definition.** Today: two sequential
  `write_text` calls (`projector.py:176-177`) with an `output_exists` refusal (lines 163-165)
  that makes a crash-orphan PERMANENT and rerun-blocking. Concrete shape: temp + `os.replace`
  per file, receipt last, receipt embeds the JSON's sha256, reader rule
  pair-valid-iff-hash-match; keep all raisable work (e.g. the manifest re-read at line 339)
  ahead of the first byte written.
- **H6 — MEDIUM proven (pending Target evidence) / HIGH multi-surface (home-verified):**
  `iter_json_objects` never descends dict-valued properties (`anchors.py:76-86`) — a Product
  under `WebPage.mainEntity` is unreachable in match AND extract → false GAP on multi-block
  pages. Target's nesting shape is decided by the same evidence packet as the contention
  check.
- **H7 (home-verified):** identity is dropped at finalize and series group by
  `(entity, signal_type)` (`projector.py:383-385`), so a DP-005 same-name pair MERGES into one
  series row — a curve-integrity error already present today. Fix: serialize identity; key
  series on it.
- **H8 — MEDIUM: GAP reason taxonomy.** Verified swallow sites (`locators.py:59-62, 81-85`;
  `anchors.py:64-67`; `jsonld_demand.py:65-66`) mean an undecodable anchor would surface as a
  bare "no data" GAP — a false GAP by the contract's own definition, since `match()` required
  the anchor's presence. Minimal taxonomy: {anchor_absent, anchor_present_undecodable,
  value_unparseable, undatable}.
- **Minor:** H9 manifest-referenced-but-missing preserved ids silently skipped
  (`projector.py:239-241`); H10 `errors="replace"` decode unflagged (lines 146, 470-471); H11
  latent empty-snippet auto-relocation (lines 289-290); H12 first-offer-only availability
  (`jsonld_demand.py:229-236`).

**Variant dependency, explicit:** these closure conclusions hold under guard (c). Under union
(a), identity serialization becomes mandatory immediately and the pre-merge `seen` sets would
have destroyed union evidence; under arbitration (b), closure additionally requires an
ownership-totality proof. Choosing (c) keeps the closure surface smallest.

### 6.3 The invariant set (the testable enforcement contract)

- **I1 Coordinate completeness:** an explicit addressed-universe U per packet, adapter-declared;
  `len(observations) + len(gaps) + len(conflicts) == |U|`; counts equal array lengths; receipt
  renders the same three numbers.
- **I2 Structural discrimination:** gap/conflict records carry a discriminator and NO value
  field; every observation `value` is a non-empty string; `value == "0"` only via a genuine
  extracted zero; no record carries `timestamp == ""` — undatable is a typed reason, never a
  sentinel; every gap reason from a closed set.
- **I3 Dating integrity per capture mode:** every observation timestamp derives from a typed
  packet timing fact consistent with `capture_mode`; for archive/history packets the timestamp
  equals the snapshot's own declared time from a TYPED field, or the coordinate is a typed
  dating-gap/refusal — never the fetch time.
- **I4 Value fidelity:** `value` is verbatim or flagged-normalized; a non-integral numeric is
  never truncated; one shared int-normalization helper, property-tested once.
- **I5 Artifact-pair atomicity:** after any terminated run, the output dir holds nothing or a
  complete pair; receipt embeds the JSON's sha256 and it matches; temp+replace per file,
  receipt last; rerun refusal names an invalid pair.
- **I6 Serialized curve eligibility, single floor:** every observation carries
  `curve_eligible`, computed only by the central flag→confidence floor; series point_count
  equals curve-eligible members; gaps/conflicts contribute to neither series nor
  `by_signal_type`.
- **I7 Identity carriage + conflict-loud uniqueness:** every observation serializes its
  namespaced identity; same `(identity, signal_type, timestamp)` + equal payload collapses to
  one with a dedup count; different payload yields a typed conflict — enforced at one
  projector-level pass regardless of producing adapter; series grouping keys on identity.

Each invariant maps one-to-one onto a named hole (I1↔H2, I2↔serialization traps/H8, I3↔H1,
I4↔H3, I5↔H5, I6↔H4, I7↔H7/R6); deleting any one reopens it.

## 7. Signals 5–6 — smallest-complete boundary and severity

**NOW (proven path):** F6 guard; R6 central conflict-loud resolution (including removing both
seen-sets; conflict variant landed WITH D1); **H1 archive dating** (gates everything — highest
priority of this set); H3 shared int-helper; H2 restricted to the jsonld universe ("anchor
absent at this snapshot" is itself the hollow-demand signal → typed GAP with reason); H4
serialized `curve_eligible`; H5 concretized P1+; H7-lite (serialize identity; series keyed on
it); H8's four-reason minimum; I1–I7 as the test contract. Plus the single risk-first probe:
capture ONE real Target hero-SKU packet per snapshot era and grep it — it simultaneously
decides guard-suffices-vs-union-now and H6-deferred-vs-now.

**DEFERRED (multi-surface phase — each a documented limitation recorded in NON_CLAIMS, the
registry header, and the lane decision record's "Deferred (explicitly, not silently)" section;
never a silent gap):** multi-adapter union + per-observation `extracted_by` attribution +
cross-adapter conflict adjudication + identity crosswalk (required before/with the second
spec — the guard is the tripwire enforcing that ordering); H6 traversal (unless Target
evidence promotes it); H12 first-offer-only; the full H8 taxonomy; trend per-point gap records
(trend is spike NO-GO); H9/H10 typed upgrades. Tightening trend's bare-substring predicate is
a cheap adjacent fix, explicitly flagged as a scope addition for the CA — not bundled.

**Severity (proven path / multi-surface):**

| Finding | Proven path | Multi-surface |
|---|---|---|
| F6 dispatch | MODERATE (blindness, not demonstrated contention; → LOW with guard) | HIGH (blocks second spec/surface) |
| R6 dedup | MEDIUM (jsonld twin-block dual emission possible, unverified) | HIGH (verified arbitrary-winner mechanics; union multiplies) |
| H1 dating | **CRITICAL** | HIGH |
| H2 universe | HIGH | HIGH |
| H3 truncation | HIGH | MEDIUM |
| H4 eligibility | HIGH | HIGH |
| H5 atomicity | HIGH | HIGH |
| H6 traversal | MEDIUM (pending Target evidence) | HIGH |
| H7 identity/series | MEDIUM | HIGH (CRITICAL under union) |
| H8 gap reasons | MEDIUM | MEDIUM |
| H9–H12 | LOW–MEDIUM | LOW–MEDIUM |

## 8. Evidence basis and citation caveat for the repo-blind reviewer

All `file:line` citations refer to the demand-projection lane worktree
(`orca-demand-projection-wt`, branch `capture-demand-projection`, HEAD
`3e42ebc6d0792ee4b0c7f175a2d0418db4186e1b`) **as read in the home-CA session of 2026-06-11
against a DIRTY working tree** — the cited source files were locally modified (in-flight lane
work), so line numbers are evidentiary for that read session, not durable pins. Every claim
marked "home-verified" was confirmed by the home CA reading the primary source directly in
that session; claims marked † are lens-subagent citations the home CA spot-checked for
consistency but did not independently re-read line-by-line. You (the reviewer) have NO repo
access: treat every citation as an authored evidence claim — attack the reasoning,
consistency, completeness, and closure logic; label anything that can only be settled by
reading the repository as `unverifiable from provided sources` rather than assuming it either
way.

## 9. Non-claims and standing gate

Not validation, not readiness, not a build authorization, not an accepted decision record, not
entity canonicalization or Cleaning/Judgment design, not capture-lane redesign (H1's runner-
side fix shape is a flagged cross-lane proposal, not an executed change). The commissioning
gate stands: nothing is built, ratified, or merged until this design survives the de-correlated
cross-vendor check this document was prepared for, and the home CA adjudicates that review's
findings.

## 10. Questions this review should pressure-test (non-exhaustive — do not stop here)

1. Is loud-on-contention (c) actually smallest-COMPLETE, or does the ungrounded Target
   contention question make the guard an under-fix that merely defers a required union?
2. Is the typed `conflict` record the right honesty representation vs flag+downgrade, given
   the differencer consumes raw observations? Does it create schema lock-in D1 will regret?
3. Does the H1 fix shape (typed snapshot-time field + mode-aware dating) belong runner-side,
   projection-side, or both — and does fixing it runner-side break the "operates only on
   already-captured packets" boundary for EXISTING packets (re-capture vs re-derive)?
4. Is the I1–I7 set sufficient AND minimal? Is any invariant untestable as stated, or any
   named hole left uncovered by the set?
5. Is anything in the DEFERRED list actually load-bearing NOW for the proven path (especially
   H6 traversal and H12 first-offer-only)?
6. Is the operator-pin path (`operator_pinned` + flagged GAPs) an honesty hole — does it
   reintroduce the silent fourth outcome under operator habit?
7. Does the fitness reference itself (§1) miss a failure mode the three-valued contract cannot
   express (e.g. wrong-value observations, which are neither GAP nor REFUSAL)?
