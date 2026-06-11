# Adversarial Artifact Review + CA Adjudication — Demand-Projection F6+R6 Revised Design (v0)

```yaml
retrieval_header_version: 1
artifact_role: Review report (docs/review-outputs/adversarial-artifact-reviews/)
scope: >
  Durable record of the no_repo cross-vendor adversarial artifact review of
  demand_projection_f6_r6_revised_design_v0.md (couriered back 2026-06-11) plus the home-CA
  review-return adjudication: per-finding accept/modify/reject, kept-state decision, and the
  decision points routed to the follow-up architecture amendment pass.
use_when:
  - Running the F6+R6 architecture amendment pass (the accepted findings below are its inputs).
  - Checking what the 2026-06-11 de-correlated review found and what the CA kept.
authority_boundary: retrieval_only
reviewed_by: gpt-5.5-thinking (OpenAI) — operator-couriered; reviewer self-stated identity
authored_by: claude-fable-5 (Anthropic)
de_correlation_bar: cross_vendor_discovery
review_target: docs/review-inputs/demand_projection_f6_r6_norepo_adversarial_artifact_review_bundle_v0/demand_projection_f6_r6_revised_design_v0.md
review_target_sha256: 91ACE1B76852006A29A6AB4DF44D3DC108EDA3DF8B33F4C2373DF46D492B0C2F
reviewer_hash_confirmation: target and README pins both confirmed by the reviewer
commission: docs/prompts/wrappers/demand_projection_f6_r6_norepo_adversarial_artifact_review_wrapper_v0.md
  (no_repo mode, .agents/workflow-overlay/delegated-review-patch.md)
review_date: 2026-06-11
adjudication_date: 2026-06-11
```

## 1. Reviewer summary (returned verbatim in substance)

- status: `review_complete`; tooling boundary stated (no in-repo formal tooling; advisory only).
- recommendation: **`NEEDS_ARCHITECTURE_PASS` before amendment-level remediation; advisory only.**
- findings: 6 — two critical, three major, one minor.
- one-line summary (reviewer's): "The artifact is unusually candid, but its core contract is
  not closed: it adds a fourth outcome, leaves the highest-risk dating fix unowned, and keeps
  a pin path that can normalize suppressed-claim artifacts."

## 2. Findings and CA adjudication (each finding treated as a claim, checked against the target text)

### F1 — critical: typed `conflict` is a fourth emitted outcome contradicting the stated three-valued contract
Reviewer: target §1 defines exactly OBSERVATION / typed GAP / REFUSAL; §5 introduces `conflict`
(neither observation, nor no-data gap, nor refusal); §6.3 I1 counts `conflicts` beside
observations and gaps. The success bar is internally unstable. Minimum closure: define one
coherent result algebra. Next authorized action: owner decision / architecture pass.

**CA adjudication: ACCEPT — critical upheld.** Verified against the target text: §1 was carried
verbatim from the commission and was not recast when §5 adopted the typed-conflict
representation; the reconciliation that existed in the underlying lens design (conflict as a
typed, counted, addressed-no-usable-value outcome — "no SILENT fourth outcome" is not "no
fourth TYPED outcome") was dropped in synthesis and never made it into §1 or I1. As written the
artifact contradicts itself. Disposition: the result algebra is a contract-shape decision the
owner must ratify (the three-valued framing originates in the commission itself). Leading
candidate carried to the amendment pass: every addressed coordinate yields exactly one typed
record from the closed discriminated union {observation, no_data, conflict}; "three-valued"
names the consumer-facing value semantics (value present / no usable value, with typed reasons
/ no artifact); REFUSAL stays whole-artifact. Alternative: honestly rename to a four-outcome
algebra. Not patched unilaterally in this turn.

### F2 — critical: H1 declared NOW and gating while lane ownership and existing-packet semantics stay unresolved
Reviewer: the typed snapshot-time field has no bound owner (runner-side vs projection-side vs
both, target §10 Q3 left open) and there is no closed rule for already-captured packets lacking
the typed field (invalid vs re-derivable vs re-capture). Downstream executability fails.

**CA adjudication: ACCEPT — critical upheld.** The target flags the question but a NOW+gating
item with an unbound owner is not executable; the reviewer is right. Adjudication evidence
(home-verified this session, recorded for the amendment pass): the Wayback snapshot timestamp
IS preserved in existing packets — structured in `archive_availability_metadata.json`
(`_snapshot_metadata`, archive runner lines 245-255) and as prose in `source_edit_or_version`
(lines 258-261) — so existing packets are re-derivable in principle without re-capture; the
open decision is where the TYPED read lands (runner-side typed field forward-only +
projection-side derivation for existing packets / projection-side only / invalidate-and-
recapture). Disposition: cross-lane owner decision; routed to the amendment pass with the three
candidate shapes and the re-derivability evidence.

### F3 — major: operator pin reopens contention blindness as a sanctioned success path
Reviewer: only pinned-run GAPs carry a per-record flag; pinned-run OBSERVATIONS look ordinary
at record level, and consumers read raw observations (the target's own H4 logic), so
suppressed-claim runs can normalize. Minimum closure: pinned artifacts must not be consumable
as ordinary uncontended observations.

**CA adjudication: ACCEPT WITH MODIFICATION — major upheld.** The asymmetry is real and the
reviewer correctly turned the target's own H4 consumption argument against its §4 pin design.
Modification: the artifact-level `dispatch.mode` record stands (it is necessary, not
sufficient). Concrete candidates routed to the amendment pass: per-record extraction flag on
pinned-run observations (e.g. `observed_under_operator_pin_with_suppressed_claims`) feeding the
central F4 floor, and/or an explicit curve-eligibility policy for pinned runs (default
ineligible unless the owner accepts), i.e. pinned mode defined as an explicitly degraded
artifact state. Exact rule = micro-decision in the amendment.

### F4 — major: F6 guard treated as NOW-complete before the Target contention evidence exists
Reviewer: §3 admits the proven-path question is ungrounded; §7 simultaneously places the guard
in NOW and says the probe decides "guard-suffices-vs-union-now"; honesty-complete is not
capability-complete — if Target eras contend commonly, the guard refuses where the system is
supposed to produce curves. Minimum closure: bind the evidence before classifying guard-only as
NOW-sufficient, or explicitly scope the NOW claim to uncontended packets.

**CA adjudication: ACCEPT WITH MODIFICATION — major upheld.** The design's intent (probe
ordered first; union triggered by evidence) was stated ambiguously enough that the sufficiency
claim outruns the evidence. Modification adopted: the second closure arm — the amendment must
make the Target-era probe an explicit GATE inside NOW (probe precedes or accompanies the guard
build), and scope the guard's claim as: honesty fix unconditionally; proven-path CAPABILITY
sufficiency conditional on the probe; contended eras promote union into NOW. The
"honesty-preserving tripwire" vs "complete proven-path projection design" distinction is
adopted verbatim into the amendment inputs.

### F5 — major: coordinate identity inconsistent across goal, dedup key, conflict key, and series key
Reviewer: §1 uses (entity, signal_type, period); §5 dedups on (identity, signal_type,
timestamp); H7 keys series on identity; I1/I7 inherit the unresolved axis. Timestamp drift can
hide same-period conflicts; entity/identity drift can split or merge series. Minimum closure:
one canonical coordinate model used consistently.

**CA adjudication: ACCEPT — major upheld.** Genuinely unreconciled in the artifact: the
commission's consumer-level frame (entity, signal_type, period) and the projection-layer keys
were both used without the mapping ever being stated. Candidate model routed to the amendment:
canonical projection-layer coordinate = (adapter-namespaced identity, signal_type, timestamp);
consumer mapping = entity is the display label attached to an identity-keyed series, period is
the differencer's bucketing of timestamp; universe U, dedup, conflict formation, counts, and
series grouping all on the canonical key; the same-period/different-timestamp case is
explicitly the differencer's aggregation question, not a projection-layer conflict.

### F6 — minor: the "observable success signal" is not fully observable from emitted artifacts
Reviewer: I1 depends on |U|, I3 on typed timing facts, I5 on pair-validity rules, but the
artifact does not require the emitted pair to carry enough to test them independently.

**CA adjudication: ACCEPT — minor upheld.** Routed to the amendment: artifacts must serialize
the addressed-universe declaration (or make it unambiguously derivable from declared fields),
the capture-mode-consistent timing provenance actually used for dating, and the pair-validity
rule — "observable" tightened to "independently checkable from the artifact pair plus
explicitly named packet facts."

## 3. Adjudication verdict and kept state

- **Escalation ACCEPTED: `NEEDS_ARCHITECTURE_PASS`.** Findings F1, F2, F5 are contract/
  architecture-shape decisions (result algebra; H1 ownership + existing-packet rule; canonical
  coordinate model); F3 and F4 are design refinements; F6 is wording-tightening. With two
  accepted criticals on the contract shape, amendment-level patching now would force a patch
  onto an unsettled design — exactly what the escalation valve exists to prevent.
- **Nothing kept, nothing applied.** All six findings are ACCEPTED (three with modifications
  recorded above) as INPUTS to a bounded architecture amendment pass; no text of the review
  target was changed in this turn. Target hash unchanged:
  `91ACE1B76852006A29A6AB4DF44D3DC108EDA3DF8B33F4C2373DF46D492B0C2F`.
- **Reviewer output handled as claims:** each finding was checked against the target's actual
  sections before acceptance; no finding was inherited unexamined; none was rejected on the
  merits.

## 4. Validation evidence, gaps, and remaining risk

- Validation evidence this turn: hash confirmations (reviewer-side and home-side); per-finding
  textual verification against the target; the F2 re-derivability evidence is home-verified
  primary source from the 2026-06-11 session. No code, tests, or builds were run — none were
  in scope.
- Validation gaps: the Target-era evidence probe (decides F4's guard-vs-union and H6's
  boundary) remains uncaptured; the same-vendor bounded recheck is NOT owed yet (it attaches to
  a CA-applied patch, and none was applied).
- Remaining risk: the amendment pass could resolve the result algebra in a way that ripples
  into D1's serialization shape (land them together, per the target's own integration
  constraint); H1's owner decision crosses into the capture lane and may stall the proven path
  if unowned.

## 5. Next authorized steps (standing gate unchanged)

1. Bounded **architecture amendment pass** on the revised design, taking §2's six accepted
   findings as inputs; owner ratification required for the F1 result algebra and the F2
   lane-ownership/existing-packet rule.
2. The amended design (v1) re-enters a **de-correlated cross-vendor discovery check** — the
   amendments touch the contract shape, so the next pass is a fresh discovery-bar review, not
   a bounded same-vendor recheck.
3. Nothing is built, ratified, or merged until that clears. (Unchanged from the commissioning
   gate.)

## 6. Review-use boundary and non-claims

The reviewer's findings and this adjudication are decision input only — not approval,
validation, readiness, mandatory remediation, or executor-ready patch authority. The
delegated-review convention remains provisional; this record creates no strict review-lane
authority. `reviewed_by` is the reviewer's self-stated identity as couriered by the operator;
it selects, recommends, and ranks nothing.
