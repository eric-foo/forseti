# Creator Soft-Link Boundary PR431 Adversarial Artifact Review v0

```yaml
retrieval_header_version: 1
artifact_role: review_output
scope: >
  Read-only adversarial artifact review of PR #431's channel-neutral creator
  soft-link boundary patch (5 target spec files), commissioned via the
  delegated-review-patch route-out and run as adversarial artifact review.
authority_boundary: retrieval_only
verdict: patch_before_acceptance
reviewed_by: unrecorded
authored_by: OpenAI/Codex family, exact model unrecorded
de_correlation_bar: cross_vendor_discovery
controller_model_family: unrecorded
commission_prompt: docs/prompts/reviews/creator_soft_link_boundary_pr431_adversarial_artifact_review_prompt_v0.md
pr_url: https://github.com/eric-foo/orca/pull/431
```

## Commission

- **Commission:** read-only adversarial artifact review of PR #431
  ("Docs: define creator soft-link review boundary"), routed out of an invoked
  `workflow-delegated-review-patch` request because PR #431 is a multi-file
  docs/spec patch, not a single high-stakes authored artifact (a routing that
  `.agents/workflow-overlay/delegated-review-patch.md` lines 133-137 directly
  sanctions).
- **Target:** the five spec files modified by PR #431 (review targets below).
  All other repo files are read-only context — issues flagged, not patched.
- **Authority:** read-only for sources; write-only for this report. No formal
  approval/validation/readiness/merge authority. `patch_queue_entry` is excluded
  (adversarial artifact review may not emit executor-ready entries —
  `.agents/workflow-overlay/review-lanes.md` lines 86-90). Findings are decision
  input for CA adjudication only.
- **Method:** `workflow-deep-thinking` (framing) then
  `workflow-adversarial-artifact-review` (two-phase: correctness, then friction),
  both reference-loaded after source context, then applied.
- **Fitness reference (from the commission):** a future operator can open one
  current profile for an observed account or a linked creator/account cluster,
  move seamlessly from candidate to reviewed linkage, and still know which facts
  are account-scoped, which are creator-cluster-scoped, and which claims remain
  forbidden. This was attacked as an alignment axis, not treated as a
  pass-if-matches bar.

## Source Context Status

`SOURCE_CONTEXT_READY` (with the staleness and read-ledger qualifications below).

### Worktree / revision verification

| Check | Expected (pinned) | Observed | Result |
| --- | --- | --- | --- |
| Workspace | `…/worktrees/creator-ledger-static-fixture-clean` | same | OK |
| Branch | `codex/channel-neutral-creator-identity-architecture-prompt-pr412` | same | OK |
| HEAD | `d4343f8ab61a23fd981141ed516e35ddba3f891a` | `7e9c4ba7d7e5ebef3221b4ed4ec456d51fff9276` | **drift — benign (see below)** |
| Base (merge-base) | `f7d8de6381d0ec0b9ef926cd275127830a7f6036` | confirmed ancestor | OK |
| Tree status | clean | clean (`git status --porcelain` empty) | OK |
| PR state | open | OPEN, draft, head `7e9c4ba7`, base `codex/creator-ledger-static-fixture` | OK |

**HEAD drift is benign and does not trip the staleness gate.** The pinned
binding is target-file hashes (commission `dirty_state_allowance`), not HEAD. The
only commit between the pinned HEAD and the live HEAD is `7e9c4ba7`
*"docs: add soft-link boundary adversarial review prompt"* — i.e., the filing of
the review prompt being executed. It touches none of the five target files. All
five target SHA-256 hashes match the pinned values exactly:

| File | Pinned == Observed |
| --- | --- |
| `creator_profile_current_view_spec_v0.md` | `8157…23AF` ✓ |
| `creator_public_handle_linkage_ledger_spec_v0.md` | `23AD…23A1` ✓ |
| `ig_creator_roster_frontier_ledger_spec_v0.md` | `0693…0180` ✓ |
| `youtube_creator_observation_ledger_spec_v0.md` | `457A…B74A` ✓ |
| `creator_intelligence_profile_surface_v0.md` | `5E46…4F17A` ✓ |

The substance under review is byte-identical to what was pinned; the review proceeds.

### Source-read ledger

**Read fresh in target worktree (decisive):**

- The 5 target specs (full): `creator_profile_current_view_spec_v0.md`,
  `creator_public_handle_linkage_ledger_spec_v0.md` (full); the other three via
  full PR diff + surrounding context.
- Validator + model + tests:
  `orca-harness/capture_spine/creator_public_handle_linkage/validation.py`,
  `…/models.py`, `orca-harness/tests/unit/test_creator_public_handle_linkage.py`.
- Overlay authority: `.agents/workflow-overlay/review-lanes.md`,
  `delegated-review-patch.md`, `source-of-truth.md` (DCP contract),
  `validation-gates.md`.
- Upstream design intent: the PR-added
  `docs/prompts/architecture/channel_neutral_creator_identity_profile_architecture_prompt_v0.md`.
- PR change-set diff (`f7d8de63..HEAD`) and target-file hashes.

**Relied on from in-context / unchanged status (non-decisive):** `AGENTS.md`
(in session context; PR diff confirms `.agents/` and `AGENTS.md` unchanged;
target tree clean).

**Not fresh-read — judged unable to change any finding (named per commission
step 6):** `.agents/workflow-overlay/README.md`, `source-loading.md`,
`retrieval-metadata.md`, `prompt-orchestration.md`, and the three templates
(`adversarial_artifact_review_v0.md`, `orca_prompt_behavior_contract_v0.md`,
`orca_preflight_defaults_v0.md`). These govern prompt/source mechanics and
report shape; the findings are assessed against the specs + validator code
directly, and the report shape is bound by the commission. The one place a
convention read mattered — the DCP inline-receipt rule for AR-05 — was resolved
by fresh-reading `source-of-truth.md`, and AR-05 is marked advisory accordingly.

### Method / authority binding

- Trigger gate: adversarial artifact review explicitly commissioned. PASS.
- Lane-collision gate: mixed artifact (docs/specs + a backing Python validator).
  Reviewed only the **non-code artifact claims** in this lane; the validator was
  read solely to test the docs' claims about runtime enforcement (review
  question 8), not reviewed as an implementation-review target. No unresolved
  collision.
- Output binding: `filesystem-output`, bound `required_output_path` = this file
  (under `docs/review-outputs/adversarial-artifact-reviews/`, the lane default).
- Severity labels `critical`/`major`/`minor` and result vocabulary
  (`accept` | `accept_with_friction` | `patch_before_acceptance` | `reject` |
  `blocked`) are commission-bound and overlay-sanctioned
  (`review-lanes.md` lines 73-76).
- Deep-thinking discipline: applied (framing below). Both method skills were
  available and applied after source readiness.

## Deep-Thinking Risk Frame

**The real question.** A "soft link" (`candidate_public_account_link`) is a
reversible, human-unreviewed bundle of similar public accounts. The patch must
let an operator slide seamlessly from candidate to reviewed linkage **while the
hard boundary holds**: a candidate is never a final creator identity, never a
real-world-identity claim, never cross-platform rollup/outreach authority, never
a public person-level surface. The correctness question is not "does the patch
*say* the boundary" (it does, repeatedly) but "is the boundary expressed in the
**operative normative rules and the field/vocabulary contract** an implementer
will actually build from — or only in adjacent prose an implementer can comply
with while still building the leak?"

**Failure modes attacked.**

1. **Boundary stated in prose but not in the operative rule.** A separate
   "boundary" section forbids X, but the rule list / record shape that an
   implementer codes from does not encode the same exclusion. (→ AR-01)
2. **Vocabulary fork / drift.** A new state vocabulary partially overlaps an
   existing one, with the divergent term landing exactly on the state that most
   needs to stay distinct (candidate). Two state fields coexist with no stated
   mapping. (→ AR-02)
3. **Inconsistent subject modeling** on a "view over siblings" whose whole job
   is to join cleanly on subject. (→ AR-03)
4. **Docs claiming runtime enforcement the code does not (or no longer)
   guarantees.** (→ checked: validator genuinely enforces it; but the
   newly-documented rule is untested — AR-04)
5. **Accidental authorization leak** (real-world identity / outreach / capture /
   readiness). (→ checked: well-guarded — non-finding.)

**Decisive criteria.** (a) Every forbidden behavior must be blocked by a
single normative rule at the locus an implementer builds from, not only by prose
elsewhere. (b) State/ID vocabulary must be bound consistently across the contract
surface and to the validator's enums. (c) Any claim that the validator enforces a
rule must match the code, and a newly-documented enforcement claim should be
regression-locked. (d) Non-claims must cover every newly-opened capability.

**Anti-anchoring note.** The patch is substantially good: the boundary intent is
sound, the IG-roster ID disambiguation is clean and complete, the
anti-double-counting recompute rule is a genuine strength, and the validator
backing for the linkage rules is real and currently green. The findings below are
contract-precision gaps, not a rejection of the direction. Two of them, however,
land on the exact axis the fitness reference cares about (keeping account-scoped
vs creator-cluster-scoped facts and the candidate-vs-final distinction legible),
so they are material.

---

## Findings

Ordered `critical` → `major` → `minor`. No `critical` findings. Phase 1
(correctness): AR-01, AR-02, AR-03, AR-04. Phase 2 (friction): AR-05.

### AR-01 — Cross-platform rollups are not gated on a promoted link state (candidate clusters can be aggregated before review)

- **Severity:** major
- **Phase:** correctness
- **Location:** `creator_profile_current_view_spec_v0.md` — "Minimum rollup
  rules" lines 306-309 vs "Subject And Soft-Link Boundary" lines 197-198; record
  shape `creator_metric_rollup` line 230. Cross-ref
  `creator_public_handle_linkage_ledger_spec_v0.md` lines 95-98.
- **Issue:** The boundary prose says a candidate link "is not enough by itself
  for cross-platform aggregate rollups" (profile 197-198; linkage 95-98). But the
  operative rollup rule states: "After public-handle linkage, cross-platform
  aggregate influence attaches to `creator_record_id`…" (profile 308-309). A
  `candidate_public_account_link` **is** public-handle linkage: it lives in the
  linkage ledger, spans ≥2 platforms, and therefore has a `creator_record_id`
  (profile 189-191 defines a `creator_record` subject as existing "only when
  account-link evidence spans at least two platforms" — which a candidate
  satisfies). No normative rule restricts cross-platform rollups to a *promoted*
  (`probable`/`declared`) state.
- **Evidence:** `creator_metric_rollup.creator_record_id_or_none: …required only
  for cross_platform rollups` (profile 230) — a candidate cluster has a
  `creator_record_id`, so nothing in the record shape blocks a `cross_platform`
  rollup keyed to it. The architecture prompt's "Expected Starting Bias" inherits
  the same imprecision: "Metrics first attach to platform_account_id, then may
  roll up to creator_record_id" (architecture prompt line 229) — no candidate-vs-
  promoted distinction. The architecture prompt explicitly posed this as a
  Required Decision ("Where do … aggregate influence metrics attach before and
  after cross-platform linkage?" lines 202-203; "How do metric rollups avoid
  double-counting…" 204-205).
- **Strongest reading, and why it fails:** *Strongest defense* — the recompute
  rule (profile 310-312, "must not sum stored account-level rollups as if those
  were independent raw observations") plus the boundary section signal clear
  intent that candidates are excluded; an integrating reader gets it right.
  *Why it fails* — the "Minimum rollup rules" list is the natural locus an
  implementer codes rollups from, and it uses "after public-handle linkage"
  (which, by this spec's own definitions, includes candidates) as the trigger.
  The exclusion lives in a different section under softer "not enough by itself"
  phrasing, and no single normative rule ties `cross_platform` rollups to a
  promoted `link_state`. An implementer can satisfy every rule in the rollup list
  and still aggregate an unreviewed candidate cluster. The recompute rule
  addresses *how* to compute without double-counting, not *when* a cross-platform
  rollup is permitted — a different question.
- **Impact:** premature cross-platform aggregate influence for unreviewed,
  reversible candidate clusters — exactly the "accidental cross-platform summing
  before review" the patch's review question 4 asks it to prevent. Over-claims
  creator-cluster-scoped influence for a link a human has not accepted.
- **`minimum_closure_condition`:** the contract carries one normative rule that
  cross-platform aggregate rollups require a promoted link state
  (`probable_public_account_link` or `declared_public_account_link`) and
  explicitly exclude `candidate_public_account_link`; the "after public-handle
  linkage" trigger in the rollup rules is disambiguated to "after a human-reviewed
  (promoted) link." (End state, not implementation.)
- **`next_authorized_action`:** CA decision to authorize a bounded wording patch
  to the profile spec's rollup rules + boundary section (patch-level; no
  architecture pass required).
- **Advisory remediation direction (not executor-ready):** add a rollup rule such
  as "Cross-platform rollups require `link_state ∈ {probable_public_account_link,
  declared_public_account_link}`; a `candidate_public_account_link` cluster gets
  only per-`platform_account_id` rollups," and align the "after public-handle
  linkage" phrase to "after a promoted public-handle link."
- **Strict claims that remain `not proven`:** none asserted beyond the cited
  artifact text; this is an internal-contradiction finding, not a verdict on
  runtime behavior.

### AR-02 — `identity_state` vocabulary diverges from the ledger `link_state` with no stated mapping; `cross_platform_candidate` is an orphan term

- **Severity:** major
- **Phase:** correctness
- **Location:** `creator_profile_current_view_spec_v0.md` line 279 (`identity_state`
  enum) and lines 280-281 (`link_state_or_none` / `review_state_or_none`);
  consumed at `creator_intelligence_profile_surface_v0.md` line 81. Ledger enums:
  `orca-harness/capture_spine/creator_public_handle_linkage/models.py` lines 19-30.
- **Issue:** `creator_profile_current.identity_state` is the enum
  `{single_platform_observed, cross_platform_candidate, probable_public_account_link,
  declared_public_account_link, rejected_public_account_link}` (profile 279). The
  ledger `LinkState` is `{declared, probable, candidate, rejected}_public_account_link`
  (models.py 19-23). The profile enum reuses **three** ledger values verbatim,
  **renames** the candidate state to `cross_platform_candidate`, and **adds**
  `single_platform_observed`. The profile *also* carries `link_state_or_none`
  "from identity ledger" (profile 280) — so for a candidate creator_record subject
  the row holds `identity_state = cross_platform_candidate` **and**
  `link_state_or_none = candidate_public_account_link` simultaneously, with no
  stated relationship between the two fields and no mapping table.
- **Evidence:** `cross_platform_candidate` appears in only three places repo-wide
  — the profile enum (profile 279), the architecture prompt's open Required
  Decision "What field or state distinguishes: … `cross_platform_candidate` …"
  (architecture prompt 196-201), and the review prompt's own checklist (review
  prompt 255) — and **nowhere** is it bound to `candidate_public_account_link`.
  The patch's own propagation `stale_language_search` (profile 440) greps
  `creator_record_id|candidate_public_account_link|candidate_needs_review|profile_subject_kind|platform_account_id`
  — it does **not** include `identity_state` or `cross_platform_candidate`, so the
  new state vocabulary was never swept for consistency. The Creator Signal surface
  now requires `identity_state` **and** "link/review state when present"
  (surface 81), inheriting the dual-field ambiguity at the product surface.
- **Strongest reading, and why it fails:** *Strongest defense* — `identity_state`
  is deliberately a profile-view abstraction distinct from the raw ledger value,
  and three shared verbatim values make the correspondence obvious. *Why it fails*
  — a deliberately separate vocabulary would rename all five values, not three-
  verbatim / one-renamed / one-new; the partial overlap is the trap, because a
  reader cannot tell whether `cross_platform_candidate` *is*
  `candidate_public_account_link` or a distinct state. The architecture prompt
  itself flagged "what field or state distinguishes" these as an unanswered
  Required Decision; the spec named the states but never bound the mapping. The
  coexistence of `identity_state` and `link_state_or_none` with no stated relation
  compounds it. Secondary defect surfaced by the same lens:
  `rejected_public_account_link` as an `identity_state` implies a `creator_record`
  profile **subject** for a disconfirmed (non-)cluster, which contradicts
  "`creator_record` = a linked public account cluster" (profile 189-191; linkage
  64, 100-103).
- **Impact:** a downstream implementer — and the Creator Signal product surface,
  which the patch updates to consume `identity_state` — must map
  `identity_state`↔`link_state`/`review_state` with no spec guidance, and the
  divergent candidate naming invites mislabeling the very state (candidate) the
  patch most needs to keep distinct from final identity. Directly erodes the
  fitness reference ("know which facts are account-scoped, which are
  creator-cluster-scoped").
- **`minimum_closure_condition`:** the spec binds `identity_state` to the ledger
  vocabulary — either drop `cross_platform_candidate` and reuse
  `candidate_public_account_link`, or add an explicit mapping
  (`identity_state` ↔ `link_state`/`review_state`, per `profile_subject_kind`) —
  and resolves whether `rejected_public_account_link` is a valid profile-subject
  state; the Creator Signal surface points at that single mapping rather than
  re-listing states.
- **`next_authorized_action`:** CA decision. Because this answers an
  architecture-prompt Required Decision, the CA may either (a) authorize a bounded
  spec patch adding the mapping/aligning the vocabulary, or (b) route this one
  state-model question back to a short architecture-planning confirmation if the
  identity-state model has downstream storage/identity-graph implications it wants
  locked first.
- **Strict claims that remain `not proven`:** whether `cross_platform_candidate`
  is intended as identical to or distinct from `candidate_public_account_link` is
  **not determinable from the artifact** — that indeterminacy is the finding.

### AR-03 — Subject identification is modeled three different ways across the satellite record shapes

- **Severity:** minor
- **Phase:** correctness
- **Location:** `creator_profile_current_view_spec_v0.md` — `creator_metric_observation`
  205-208; `creator_metric_rollup` 228-231; `creator_ideal_audience_profile_snapshot`
  250-256; `creator_profile_current` 274-279.
- **Issue:** The contract is explicitly a "view over siblings" that joins on
  subject (profile 114-135), but the four shapes key the subject three different
  ways: the metric observation by `platform_account_id` (+ `creator_record_id_or_none`);
  the metric rollup by `platform_scope` + `creator_record_id_or_none` +
  `platform_account_ids` (no `profile_subject_kind`/`id`); the ideal-audience
  snapshot and `creator_profile_current` by `profile_subject_kind` +
  `profile_subject_id` (+ `platform_account_ids` + `creator_record_id_or_none`).
  The `profile_subject_kind`/`profile_subject_id` abstraction the patch introduces
  is applied to two of the four shapes.
- **Evidence:** lines cited above; `profile_subject_kind` occurs only at profile
  252-253 and 275-276 (audience snapshot and current view), not in the rollup or
  observation shapes.
- **Strongest reading, and why it (mostly) holds:** each shape carries enough to
  *derive* the subject (`platform_account_ids` + `creator_record_id_or_none`), so
  joins remain possible — which is why this is minor, not major. It remains a
  finding because "derivable" is not "consistent": a contract that introduces a
  subject abstraction should apply it uniformly or state why metric
  observations/rollups are exempt, else each consumer re-implements the subject
  join differently.
- **Impact:** avoidable join ambiguity and maintenance drift on the central
  contract; a leaky abstraction (`profile_subject_kind`) that exists in half the
  shapes.
- **`minimum_closure_condition`:** the spec either applies
  `profile_subject_kind`/`profile_subject_id` uniformly across the satellite
  shapes, or states explicitly why the metric observation/rollup shapes key on
  `platform_account_id`/`platform_scope` instead.
- **`next_authorized_action`:** CA decision — optional bounded spec patch
  (labeled optional hardening; not a blocker).
- **`not proven`:** none.

### AR-04 — The newly-documented "candidate link requires `candidate_needs_review`" validator rule is enforced in code but untested

- **Severity:** minor
- **Phase:** correctness
- **Location:** `creator_public_handle_linkage_ledger_spec_v0.md` line 212 (new
  validator-contract bullet); enforcement at
  `orca-harness/capture_spine/creator_public_handle_linkage/validation.py` lines
  480-482; test gap at `orca-harness/tests/unit/test_creator_public_handle_linkage.py`.
- **Issue:** PR #431 newly elevates "a candidate link whose review state is not
  `candidate_needs_review`" to a documented validator fail-closed requirement
  (linkage 212), and the profile spec's DCP receipt justifies *not* updating the
  validator on the grounds that it "already enforces candidate_needs_review for
  candidate links" (profile 432-434). The code claim is **true** (validation.py
  480-482 raises `candidate_link_review_state_mismatch`). But the test suite has
  no regression test for it: the only candidate reference in the tests is a
  happy-path assertion that `candidate_public_account_link` is among the fixture's
  link states (test 56-61). The 22-test suite passes (run below) without
  exercising the candidate fail-closed path.
- **Evidence:** `uv run pytest tests/unit/test_creator_public_handle_linkage.py`
  → 22 passed; grep of the test file for
  `candidate_needs_review|candidate_link_review_state_mismatch` returns only the
  happy-path link-state assertion (line 60). Negative tests exist for the
  *declared/probable/single-platform/llm-only/disconfirming* rules but not for the
  candidate review-state rule.
- **Strongest reading, and why it stands:** *Strongest defense* — the rule is
  enforced in code today, and a docs patch is arguably not the place to add tests.
  *Why it stands* — the patch newly **documents** this as a validator requirement
  and **leans on** "already enforces" as the explicit reason to leave the
  validator untouched; but the suite does not lock it, so "enforces" is a
  present-tense code fact, not a regression-protected guarantee. A future refactor
  could drop the candidate branch with no failing test.
- **Impact:** low-likelihood but in-scope erosion risk of a guarantee the patch
  now advertises in the spec.
- **`minimum_closure_condition`:** a regression test asserts that a candidate
  link with a non-`candidate_needs_review` review_state raises
  `candidate_link_review_state_mismatch` (same-check red-green: fails against a
  candidate-with-wrong-review-state mutation of the fixture, passes with the guard
  in place).
- **`next_authorized_action`:** CA decision — optional test addition in a
  separate implementation/test lane. This read-only artifact-review lane does not
  author it. Labeled optional hardening.
- **Red-green proof status:** `applicable` (testable). Not produced here (would
  require a source-changing test author, outside this read-only commission).

### AR-05 — Propagation-receipt hygiene: missing archive-pointer line (friction)

- **Severity:** minor
- **Phase:** friction
- **Location:** `creator_profile_current_view_spec_v0.md` "## Direction Change
  Propagation" section, lines 402-509.
- **Issue:** The DCP contract requires that "The inline receipts section must end
  with one pointer line to the archive" (`.agents/workflow-overlay/source-of-truth.md`
  line 110). The profile spec's DCP section now holds **two** receipts — which is
  itself **compliant** with the "at most the two most recent receipts inline" cap
  (source-of-truth 108) — but ends at the second receipt's closing fence with **no**
  archive-pointer line (compare source-of-truth's own line 347).
- **Evidence:** source-of-truth.md 106-111 (contract); profile 509 ends the file
  at the receipt fence with no pointer line.
- **Strongest reading, and why it is only advisory:** the archive-pointer / inline-
  cap rules are **explicitly not mechanically gated**
  (`validation-gates.md` 276-278: "The inline-receipt cap, archive pointer, and
  'no standalone receipt files' rules are deliberately NOT gated here … several
  controlling files already hold >2 inline receipts"), repo compliance is
  known-inconsistent, and the pointer is arguably only required once receipts are
  cycled *out* of a file (nothing has been archived from this file yet). So this
  is a literal-but-low-severity deviation, not a blocker.
- **Impact:** negligible routing/hygiene nicety; cheap to fix.
- **`minimum_closure_condition`:** the inline DCP section ends with one
  archive-pointer line, **or** the CA confirms the pointer is required only once
  receipts are archived from the file.
- **`next_authorized_action`:** CA decision — optional hygiene patch, or accept
  as-is under the un-gated convention.
- **`not proven`:** whether the pointer line is mandatory for a file that has not
  yet archived any receipt is **not proven** from the contract wording (it reads
  "must," but the un-gated status and repo variance leave the intent ambiguous).

---

## Non-Findings (review questions that survive inspection)

- **Q2 — candidate always needs `candidate_needs_review`; final/probable/declared
  need human + non-LLM evidence.** Validator enforces both: candidate →
  `candidate_needs_review` (validation.py 480-482); declared/probable require the
  matching human-reviewed review_state, strong/3-independent-weak evidence, no
  disconfirming evidence, and a non-LLM-only actor (validation.py 454-496). Spec
  text (linkage 199-201, 205-217) matches the code. **Survives** (see AR-04 for
  the test-coverage caveat on the candidate branch only).
- **Q3 — `platform_account` subject before linkage; `creator_record` only after
  ≥2 platforms.** Cleanly modeled (profile 144-148, 182-198) and code-enforced for
  the ledger side (validation.py 436-438, `single_platform_creator_record`).
  **Survives**, modulo the AR-02 naming gap.
- **Q4 — account-primary vs creator-cluster rollups separated to prevent
  cross-platform summing before review.** The *recompute / no-double-count* rule
  (profile 310-312) is a genuine strength. But the *when-permitted* gate is the
  open hole — see **AR-01**. Partial.
- **Q5 — Creator Signal surface labels account-scoped vs linked-cluster honestly.**
  Surface adds account-scoped claim shapes (surface 129-130), forbids candidate
  links presented as final identities (surface 154-156), and requires
  `profile_subject_kind`/`identity_state` (surface 81). **Survives**, but rides on
  the AR-02 vocabulary it consumes.
- **Q6 — IG roster ID no longer overloads the linkage `creator_record_id`.**
  Thorough, complete rename to `ig_roster_record_id` across semantics, headings,
  all four record shapes, invariants, ledger concepts, and checks. The four
  remaining `creator_record_id` references in the IG roster file (ig spec 144,
  184, 240, 520) are all **correct** cross-references to the *linkage ledger's*
  id, explicitly disambiguated. **Survives — clean.**
- **Q7 — no accidental authorization of identity proof / outreach / capture /
  SQLite / dashboard / readiness / validation.** Non-claims are comprehensive and
  the new wording adds none: profile 386-400 & 442-449; linkage 95-98 & 222-233;
  youtube adds "platform authority for cross-platform identity" to its non-claims;
  surface forbids candidate-as-final and inherits the dashboard forbidden set.
  **Survives.**
- **Q8 — validator sufficiency / no over-claimed runtime enforcement.** The
  validator genuinely enforces the three claimed linkage rules
  (candidate review-state, human+non-LLM final links, ≥2-platform creator_record);
  the receipt's `intentionally_not_updated` claim is **code-accurate**. The
  unimplemented view shapes are explicitly labeled "architecture contracts, not
  implemented schemas" (profile 202), so there is **no** runtime-enforcement
  over-claim for them. **Survives** (with the AR-04 test-gap note).
- **Q9 — stale/conflicting vocabulary.** The `creator_record_id` rename is clean
  (Q6). The live conflict is `identity_state`↔`link_state` — see **AR-02**; subject
  keying — see **AR-03**.
- **Q10 — design-level defect needing return to architecture.** AR-01 and AR-02
  trace to architecture-prompt Required Decisions. AR-01 is closable at patch
  level. AR-02 is patch-level *unless* the CA judges the identity-state model has
  downstream storage/graph implications worth a short architecture confirmation
  first.

## Validation / Static Checks

| Check | Result | Bucket |
| --- | --- | --- |
| `uv run pytest tests/unit/test_creator_public_handle_linkage.py -q` (in `orca-harness`) | 22 passed | GATE PASS (advisory) |
| Static read of `validation.py` vs the three claimed linkage rules | all three enforced (lines 436-438, 454-496, 480-482) | INFO |
| Target-file SHA-256 vs pinned hashes | 5/5 match | GATE PASS |
| Candidate fail-closed rule covered by a test? | No (only happy-path, test 56-61) | DEBT → AR-04 |

**Not run, with reasons:** broader `orca-harness` suite (out of scope — only the
linkage validator bears on a review question); live IG/TikTok/YouTube capture,
external service calls, SQLite migration (forbidden by commission). No
docs-artifact "validation gate" exists to pass/fail the spec text itself; the
specs carry compliant retrieval headers and a shape-valid, consolidated DCP
receipt (trigger `architecture_doctrine`; `related_triggers` valid; `non_claims`
non-empty) — assessed against `source-of-truth.md` 113-131 and the EP-09 shape
gate description (`validation-gates.md` 265-278).

## Residual Risk

- These are **docs-contract** findings on an explicitly **unimplemented** view
  layer; real risk materializes at implementation. The boundary intent is sound;
  the gaps are in precision, not direction.
- Closure wording for AR-01/AR-02 could itself reintroduce ambiguity; the CA
  should verify any patch states a **single** normative rule, not a second prose
  restatement competing with the first.
- The 4 non-profile target specs received no own-file DCP receipt; this is
  recorded via the profile spec's consolidated `controlling_sources_updated`
  receipt, which is an acceptable application of the DCP contract (not a finding),
  but the CA owns that judgment.
- Several required-context files were not fresh-read (named in the ledger). If the
  overlay's retrieval/propagation conventions differ materially from
  `source-of-truth.md` as read, only AR-05 could shift — and it is already marked
  advisory/`not proven`.
- De-correlation is **observed** cross-vendor (OpenAI/Codex author vs an
  Anthropic-family reviewer) but `reviewed_by` is operator-**unrecorded**; per
  `review-lanes.md` 115-121 that is a visible measurement gap, not an
  operator-captured cross-vendor measurement.

## Provenance

- **`reviewed_by`:** `unrecorded` — operator/tooling did not supply it; per
  `review-lanes.md` the reviewer is not required to self-emit, and the value is
  never fabricated. (Observation, not a durable claim: the executing reviewer was
  an Anthropic-family model, which makes the de-correlation cross-vendor *in
  fact*; the durable field stays `unrecorded`.)
- **`authored_by`:** OpenAI/Codex family (branch `codex/…`; commission-declared),
  exact model/version unrecorded. (Git committer of record is the owner;
  authorship per the commission is Codex.)
- **`de_correlation_bar`:** `cross_vendor_discovery` — **observed** by execution
  context, not operator-captured (see `reviewed_by` gap above).
- **`controller_model_family`:** unrecorded (not supplied).

## Recommendation

**`patch_before_acceptance`.**

The patch is substantially correct and a clear improvement (clean ID
disambiguation, real validator backing, a genuine anti-double-count rule, and a
well-guarded non-claims surface). But two **major** correctness gaps land on the
exact axis the patch exists to protect — keeping unreviewed candidate clusters
out of cross-platform aggregation (AR-01) and keeping the candidate-vs-final state
legible across the contract and to the validator's vocabulary (AR-02). Both are
closable with bounded spec edits; neither is a fake-success path or a reason to
reject the direction. They should be closed (or AR-02 briefly confirmed at
architecture level) before the soft-link boundary patch is relied on or promoted.
The three minor findings (AR-03, AR-04, AR-05) are optional hardening the CA may
fold into the same patch pass or defer.

- **Blocking (drive the recommendation):** AR-01, AR-02.
- **Advisory / optional hardening:** AR-03, AR-04, AR-05.

## Review-Use Boundary

This review is **decision input only** for the commissioning Chief Architect. It
is not approval, validation, readiness, mandatory remediation, product proof,
executor-ready patch authority, source promotion, or permission to merge PR #431.
No `patch_queue_entry` is emitted; remediation directions above are advisory
prose, not executor handoffs. Only a separately authorized patch, acceptance,
validation, or implementation lane can make any of this mandatory or
executor-ready. The CA decides what is kept, modified, or rejected.
