# Fragrantica Cleaning Adversarial Code Review v0

```yaml
retrieval_header_version: 1
artifact_role: Review report
scope: >
  Read-only adversarial code review of the Fragrantica projection-to-Cleaning
  adapter, its append-only derived-record lake writer, their focused tests, and
  the repo-map row that describes them. Findings-only; no patch, verdict,
  readiness, approval, or validation pass/fail claim.
use_when:
  - Home/CA adjudication of the Fragrantica Cleaning lane before assuming it is structurally ready.
  - Deciding which Cleaning-lane findings to accept, defer, or authorize a patch for.
authority_boundary: retrieval_only
branch_or_commit: codex/fragrantica-cleaning @ 4ec4eba6 (worktree HEAD f98294d4 adds only this review prompt file)
review_mode: zero_config_findings_only_advisory_with_bound_durable_output
```

## Provenance

```yaml
reviewed_by: Claude (Anthropic) / claude-opus-4-8, operator-couriered repo-bound review
authored_by: OpenAI/Codex
de_correlation_bar: cross_vendor_discovery
de_correlation_status: >
  The author home-model family is OpenAI/Codex; the receiving reviewer is
  Anthropic (Claude). Different vendor/model lineage, so cross-vendor review is
  recorded. This is a who-constraint receipt, not a model recommendation.
same_vendor_rationale: not_applicable_cross_vendor
patch_queue_entry_global: no (read-only workflow-code-review commission; multi-file code diff is not delegated-patch-eligible without separate patch-execution authority)
```

## Method And Source Loading

- Methods reference-loaded then applied per the commission's Method Order:
  `workflow-deep-thinking` (framing + a high-risk verification/anti-anchoring
  pass over each candidate finding) and `workflow-code-review` (findings-first,
  zero-config advisory; no formal verdict/patch-queue because no patch lane is
  bound).
- Anti-anchoring effect (disclosed because it materially changed the result):
  three initially-suspected defects — `content_hash` including `record_id`,
  header `raw_refs` collapsing to file granularity, and empty `derived_refs` —
  were **down-calibrated to contract-compliant** after reading the Silver Vault
  and Derived-Layout contracts. They are reported under "Considered And Cleared,"
  not as findings.

### Target SHA256 Verification

All five pinned targets matched their expected SHA256 exactly (recomputed
2026-06-29 via `Get-FileHash -Algorithm SHA256`):

| Target | Result |
| --- | --- |
| `orca-harness/cleaning/fragrantica.py` | MATCH `0299EF12…0258` |
| `orca-harness/cleaning/fragrantica_lake.py` | MATCH `2BE51947…B623` |
| `orca-harness/tests/test_fragrantica_cleaning_lake_pilot.py` | MATCH `EAEB0394…8908` |
| `orca-harness/tests/unit/test_fragrantica_cleaning_projection_integration.py` | MATCH `B0DA2BA9…4FE7` |
| `docs/workflows/orca_repo_map_v0.md` | MATCH `EDA96E22…1DFA` |

Worktree clean (`git status --porcelain` empty). HEAD (`f98294d4`) is one commit
ahead of the pinned implementation commit `4ec4eba6`; the only intervening
commit adds this review prompt file and touches none of the five targets
(`git diff --stat 4ec4eba6 HEAD -- <5 targets>` empty). The full branch diff
`origin/main...4ec4eba6` is exactly the five pinned files (773 insertions,
1 deletion). No `HASH_MISMATCH`; declaring **`SOURCE_CONTEXT_READY`**.

### Source-Read Ledger

| Source | Role | Basis |
| --- | --- | --- |
| `orca-harness/cleaning/fragrantica.py` | Target: adapter | full read + SHA pin |
| `orca-harness/cleaning/fragrantica_lake.py` | Target: lake writer | full read + SHA pin |
| `orca-harness/tests/test_fragrantica_cleaning_lake_pilot.py` | Target: lake test | full read + SHA pin |
| `orca-harness/tests/unit/test_fragrantica_cleaning_projection_integration.py` | Target: projection-integration test | full read + SHA pin |
| `docs/workflows/orca_repo_map_v0.md` | Target: repo map | read (lines 1-573 + targeted) + SHA pin + exact diff |
| `orca/product/spines/cleaning/contracts/core_spine_v0_cleaning_spine_foundation_v0.md` | Authority: Cleaning contract | full read |
| `orca/product/spines/data_lake/authority/…silver_vault_record_contract_v0.md` | Authority: Silver record | full read |
| `orca/product/spines/data_lake/authority/…derived_layout_index_rebuild_contract_v0.md` | Authority: derived placement | full read |
| `docs/workflows/fragrantica_capture_to_data_lake_projection_ecr_cleaning_handoff_v0.md` | Authority: lane boundaries | full read |
| `orca-harness/data_lake/root.py` | Authority: append-only + path grammar | full read |
| `orca-harness/source_capture/fragrantica_projection.py` | Context: projection input | full read |
| `orca-harness/cleaning/models.py` | Reviewer-added: preservation/transform/anchor semantics | full read (beyond prescribed basis; findings depend on it) |
| `orca-harness/cleaning/projection.py` | Reviewer-added: handle construction | full read (beyond prescribed basis) |
| `orca-harness/ecr/models.py` | Reviewer-added: ECR ref_id format | full read (beyond prescribed basis) |
| `AGENTS.md`, overlay README/source-loading/review-lanes/delegated-review-patch/prompt-orchestration | Context (supplied / governing) | referenced |

Reviewer-added reads (`cleaning/models.py`, `cleaning/projection.py`,
`ecr/models.py`) are not in the prompt's required basis but are load-bearing for
the preservation-truthfulness, handle-construction, and ECR-ref findings; they
are read-only context, not authority expansion.

### Validation Run Status

Reran the dispatcher-documented focused suite (`PYTHONPATH` set to
`orca-harness`, `--rootdir orca-harness`, Python 3.11.15):

```
python -m pytest -p no:cacheprovider tests\test_fragrantica_cleaning_lake_pilot.py tests\unit\test_fragrantica_cleaning_projection_integration.py tests\test_fragrantica_projection_lake_pilot.py
=> 11 passed in 0.83s   (exit code 0)
```

Matches the dispatcher-observed `...........`. `git diff --check origin/main...HEAD`
on the five targets: no output (confirmed). Tests pass — but several findings
below are precisely about what the passing tests do **not** exercise.

---

## Findings (ordered by materiality)

### FCR-01 — Normalization ledger entries record an already-normalized `original_value`, so the ledger cannot show what the transform changed (Medium)

- Commissioned target/purpose: verify transform-ledger semantics are genuinely
  non-destructive and truthful (adapter `fragrantica.py`).
- Location: `orca-harness/cleaning/fragrantica.py:129-151` (read fields through
  `_string_or_none`, then pass the result as `original_value`), `:223-231`
  (`_normalize_space` / `_string_or_none`); upstream at
  `orca-harness/source_capture/fragrantica_projection.py:611` and `:881-888`
  (`_text` already collapses `\s+`→` ` and strips). Test that masks it:
  `tests/unit/test_fragrantica_cleaning_projection_integration.py:89-90`.
- Implementation evidence: for review text,
  `review_text = _string_or_none(fields.get("review_text"))` then the ledger
  entry is built with `original_value=review_text,
  transformed_value=_normalize_space(review_text)`. `_string_or_none` itself
  calls `_normalize_space`, and `_normalize_space` is idempotent, so
  `original_value == transformed_value` **always**. The same pattern applies to
  `author_display_name` (`:141-151`). For review text the input is *already*
  whitespace-normalized upstream by the projection's `_text()`, so the Cleaning
  "whitespace normalization" is a double no-op. For author names (projection
  `_first_match` only `.strip()`s, not internal-collapse), the real collapse
  happens *inside* `_string_or_none` and is then hidden, because the
  already-collapsed value is what gets recorded as `original_value`.
- Authority/evidence basis: Cleaning Spine Foundation contract, Normalization
  row — required preservation is "**Original value**, normalized value,
  method/rule, raw anchor…" (`…cleaning_spine_foundation_v0.md:158`) — and the
  Non-Destructive Ledger purpose: let a reviewer answer "what changed, why it
  changed… what was preserved" (`:237-239`). `CleaningTransform` permits
  `original_value == transformed_value` (`cleaning/models.py:341-348` requires
  both non-null but not distinct), so this is a faithfulness/utility defect, not
  a schema violation.
- Impact (review confidence / contract traceability): the normalization entries
  assert a transform that the ledger can never evidence; when the transform does
  real work (author name with internal whitespace) the ledger actively hides it.
  The true original survives only via `raw_anchor` (raw HTML), so no evidence is
  lost, but the ledger's stated job — showing what Cleaning changed — is not met
  for normalization transforms. Review-text normalization is additionally
  redundant with the projection's upstream `_text()`.
- minimum_closure_condition: the normalization ledger captures the
  pre-transform field value (the raw/projection field as received, before
  `_string_or_none`) as `original_value`, with the normalized result as
  `transformed_value`, so `original_value != transformed_value` whenever the
  transform changes the string; and the team decides whether the review-text
  whitespace step is still warranted given upstream `_text()` normalization.
- next_authorized_action: home/CA adjudication; if accepted, authorize a bounded
  patch lane (not authorized by this review).
- verification expectation: a red-green fixture with internal/edge whitespace in
  `review_text` and `author_display_name` (e.g. `"  John   Doe "`) that fails
  against current behavior (`original_value == transformed_value`) and passes
  once `original_value` carries the pre-normalization string.
- patch_queue_entry: no.

### FCR-02 — ECR reference is attached unconditionally by convention, with a ref_id identical to a real ECR receipt and no `status` disclosure (Medium)

- Commissioned target/purpose: whether attaching an ECR reference by convention
  risks implying a persisted ECR set exists when the lane/lake may not contain
  one.
- Location: `orca-harness/cleaning/fragrantica.py:63-67` (`attach_ecr_ref: bool =
  True`), `:82` (`ecr_ref = _ecr_ref(projection.packet_id) if attach_ecr_ref`),
  `:244-249` (`_ecr_ref` builds `ref_id=f"ecr:{packet_id}:{ECR_SOURCE_SIDE_REF_KIND}"`,
  leaves `status` unset); `orca-harness/cleaning/fragrantica_lake.py:58`
  (`build_fragrantica_cleaning_packet(projection)` — never passes
  `attach_ecr_ref=False`, so persisted records always carry it).
- Implementation evidence: every handle in every persisted record gets
  `ecr_ref` with `ref_id = "ecr:<packet_id>:source_side_postures"` and
  `status=None`. There is no check that an ECR receipt exists.
- Authority/evidence basis: (1) Cleaning OD-1 says the handle attaches a
  projection and ECR reference "**when present**"
  (`…cleaning_spine_foundation_v0.md:141-143, 405-408`) — presence-gated, not
  unconditional. (2) The handoff treats ECR and Cleaning as **sibling** lanes
  that "consume only raw/projection refs" and may not have run
  (`…cleaning_handoff_v0.md:100, 110, 249`). (3) The synthesized `ref_id` is
  byte-identical to a real `EcrSourceSideReceipt.ref_id`, which `ecr/models.py:385`
  validates as exactly `f"ecr:{packet_id}:{ECR_SOURCE_SIDE_REF_KIND}"`
  (`ECR_SOURCE_SIDE_REF_KIND = "source_side_postures"`, `:33`). (4) The
  `CleaningEcrRef.status` field exists (`cleaning/models.py:222-226`) precisely
  to carry posture/resolution state and is unused.
- Impact (false-confidence / lineage): a downstream consumer cannot distinguish
  this by-convention pointer from a reference to an actually-persisted ECR
  source-side receipt; nothing in the record (no `status`, no existence check,
  `derived_refs=[]`) signals that the ECR may not exist. In a temp/test lake or
  an unsequenced lane this asserts a resolvable ECR that is absent.
- minimum_closure_condition: either gate ECR-ref attachment on a present/persisted
  ECR (and link it via `derived_refs` when it is a lake record), or set
  `CleaningEcrRef.status` to a value that discloses "referenced by convention,
  not resolved/asserted," or document the convention in the record contract so
  the ref is not read as an existence claim.
- next_authorized_action: home/CA adjudication of which disclosure path is
  intended; no patch authorized here.
- verification expectation: a test asserting the disclosed posture (e.g.
  `status` present, or ref omitted when no ECR exists), plus a test exercising
  the `attach_ecr_ref=False` path (currently never persisted).
- patch_queue_entry: no.

### FCR-03 — `observed_at` is set equal to `captured_at` and can be a contract-forbidden null on an observation record (Medium-low)

- Commissioned target/purpose: whether Silver envelope timing fields are correct
  and stable.
- Location: `orca-harness/cleaning/fragrantica_lake.py:84-88` (`capture_time` is
  `None` unless `packet.timing.capture_time.status == KNOWN`), `:103-104`
  (`"observed_at": capture_time, "captured_at": capture_time`).
- Implementation evidence: both header fields are bound to the same packet
  capture time; when capture time is not `KNOWN`, both become `null`.
- Authority/evidence basis: Silver Vault contract header invariants — `observed_at`
  = "Time the fact was observed at or about the source. **Nullable only for
  internal relationship records** with no source observation time"; `captured_at`
  = "Time Orca captured the source material"
  (`…silver_vault_record_contract_v0.md:161`). The record here is
  `record_kind="observation"`, not an internal relationship record, so a null
  `observed_at` violates the invariant. Separately, the projection carries
  per-review `date_published` (`fragrantica_projection.py:621`) that is discarded
  at the header grain.
- Impact (lake-contract / lineage): (a) latent contract violation — a packet
  whose `capture_time` is not `KNOWN` yields `observed_at: null` on an
  observation record; the current fixtures all supply a `KNOWN` capture time, so
  tests never reach this. (b) `observed_at` conflated with `captured_at` is a
  defensible "current-window observed at capture" choice at the packet grain, but
  it collapses a distinction the contract draws and discards available
  source-side review timing. Confidence: the null-on-observation case is firm;
  the conflation is a lower-confidence design observation.
- minimum_closure_condition: `observed_at` derivation either guarantees a
  non-null source-observation time for observation records (or routes the
  unknown case to a contract-permitted shape), and the team confirms whether
  packet-capture-time is the intended `observed_at` for current-window Cleaning
  records.
- next_authorized_action: home/CA adjudication against the Silver contract owner;
  no patch authorized here.
- verification expectation: a test with `capture_time` status != `KNOWN`
  asserting the contract-permitted `observed_at` shape on the observation record.
- patch_queue_entry: no.

### FCR-04 — `record_kind="observation"` carries a payload with no observation subject/posture/coverage (structural-fit open question) (Low)

- Commissioned target/purpose: whether the Silver record envelope fields
  (`record_kind`, `payload_kind`) are correct.
- Location: `orca-harness/cleaning/fragrantica_lake.py:98-100` (`record_kind:
  "observation"`, `payload_kind: "FragranticaCleaningPacket"`,
  `producer_row_kind: "fragrantica_cleaning_packet"`).
- Implementation evidence: the payload is a Cleaning packet (handles +
  transform_ledger), not an `observation` object; it carries no `subject`,
  `metric_posture`/`text_posture`, or `coverage_window`.
- Authority/evidence basis: Silver contract closes `record_kind` to
  `{entity, relationship, observation}` (`…silver_vault_record_contract_v0.md:157`)
  and its observation examples (MetricObservation/TextObservation) all carry an
  `observation` object with posture/value/coverage coupling (`:263-352`,
  acceptance criteria 6-7). `payload_kind` is, however, an open discriminator and
  "meaning lives inside the record" with a producer-owned `producer_schema_version`
  (`:51-63, 159`).
- Impact (contract-fit / review confidence): `observation` is the least-wrong of
  the three closed `record_kind` values for a Cleaning ledger, and a producer-owned
  payload is contemplated — so this is not a clear violation. But a Silver reader
  that dispatches on `record_kind="observation"` expecting an `observation` object
  will not find one. This is a genuine fit ambiguity that should be ruled on, not
  assumed.
- minimum_closure_condition: the Silver contract owner confirms that a Cleaning
  ledger packet is an acceptable `observation` payload_kind (or specifies the
  correct record_kind/treatment for Cleaning records).
- next_authorized_action: home/CA route to the Silver contract owner; no patch.
- verification expectation: not a testable correctness claim until the contract
  owner rules; documentation/contract clarification.
- patch_queue_entry: no.

### FCR-05 — `fragrantica_lake.py` module docstring describes the wrong derived path (omits `<anchor_shard>`) (Low)

- Commissioned target/purpose: whether the implementation accurately describes
  derived-lake placement.
- Location: `orca-harness/cleaning/fragrantica_lake.py:5-6` (docstring:
  "appends one lane-owned derived record at
  `derived/<packet_id>/cleaning_fragrantica/<record_id>.json`").
- Implementation evidence: the actual write path inserts the opaque anchor shard.
  `data_root.append_record` builds `<subtree>/<anchor_shard>/<raw_anchor>/<lane>/<record_id>`
  (`data_lake/root.py:559-575`), and the lake-pilot test asserts the parent is
  `derived / raw_shard(packet_id) / packet_id / cleaning_fragrantica`
  (`test_fragrantica_cleaning_lake_pilot.py:40`). The Derived-Layout contract and
  `root.py` module docstring both show `derived/<anchor_shard>/<raw-anchor>/<lane>/<record-id>`
  (`…derived_layout_index_rebuild_contract_v0.md:74`).
- Impact (review confidence / accuracy): docstring-only; no runtime effect. It
  misstates the lineage path and could mislead a maintainer reasoning about
  placement. (The behavior is correct; only the prose is wrong.)
- minimum_closure_condition: docstring shows the sharded path
  `derived/<anchor_shard>/<packet_id>/cleaning_fragrantica/<record_id>.json`.
- next_authorized_action: trivial doc correction under a bounded patch lane; not
  authorized here.
- verification expectation: none beyond text correction.
- patch_queue_entry: no.

### FCR-06 — Test fixtures do not exercise the source-family risks that matter (Medium, review confidence)

- Commissioned target/purpose: whether tests cover current-window residuals,
  review-card-only transforms, vote carry, non-claims, content-hash stability,
  append-only, and no-overwrite — and the risks above.
- Location: both target test files.
- Implementation evidence / gaps:
  - **No messy-whitespace fixture.** Review text `"This perfume died young."`
    and author `"Rimazy"` are already clean, so FCR-01's no-op `original_value`
    is masked; the suite cannot demonstrate that normalization ever changes
    anything (`…projection_integration.py:89-94`).
  - **Single review card only.** Real Fragrantica packets carry ~210 cards from
    one HTML file (`…cleaning_handoff_v0.md:141-143`). With one card the
    header `raw_refs` collapse (many handles → one file-level ref) and the
    length-bin spread are never exercised; only `chars_0000_0199` is tested,
    though real data spans all four bins (handoff `:146`).
  - **`raw_refs` content is never asserted** by any test (the lake-pilot test
    checks header fields but not `record["raw_refs"]`).
  - **`observed_at`-null path** (capture_time not `KNOWN`, FCR-03) is untested.
  - **`attach_ecr_ref=False` path** is never exercised — the lake writer always
    attaches the ECR ref (FCR-02).
- Authority/evidence basis: commission Review Axes (test coverage); Cleaning
  contract Non-Destructive Ledger purpose; the findings above.
- Impact (review confidence): the green suite (11 passed) provides weak evidence
  for exactly the behaviors most at risk; passing tests should not be read as
  evidence the normalization/ECR/timing semantics are correct.
- minimum_closure_condition: fixtures add (a) internal/edge whitespace in text
  and author fields, (b) multiple review cards across tabs and length bins, (c)
  an explicit `raw_refs` assertion, and (d) the unknown-capture-time and
  `attach_ecr_ref=False` paths.
- next_authorized_action: home/CA adjudication; test additions under a bounded
  patch lane, not authorized here.
- verification expectation: the new fixtures are the verification for FCR-01/02/03.
- patch_queue_entry: no.

### Minor robustness note (not a standalone finding)

- Empty projection → `CleaningPacket(handles=[])` raises a pydantic
  `ValidationError` (`cleaning/models.py:411`, `min_length=1`) inside
  `derive_fragrantica_cleaning_into_lake` rather than a typed Cleaning/domain
  error. This is fail-closed (no record written), so it is safe; flagged only as
  a possible diagnostic-clarity improvement, not a defect.
- `build_fragrantica_cleaning_packet` relies on a 1:1 row↔handle invariant
  (`fragrantica.py:93, 114`); a review-card row without a corresponding handle
  would `KeyError`. The handle builder makes this total in practice
  (`len(handles) == len(rows)`), so it is an internal invariant, not a live bug.

---

## Considered And Cleared (attacked, found contract-compliant — reported to prevent false findings)

- **`content_hash` includes `record_id`/producer fields → CORRECT.** The Silver
  contract frames `content_hash` as a "durable **integrity** hash for the
  canonical record content… must not include the `content_hash` field itself"
  (`…silver_vault_record_contract_v0.md:160`), not a content-identity/dedup key.
  `fragrantica_lake.py:128, 180-193` hash the whole record minus `content_hash`
  with the declared basis `canonical_json_excluding_content_hash`. Compliant.
  (Consequence noted: two re-derivations of identical content get different
  hashes because `record_id` differs — expected under "re-derive = fresh
  sibling," not a defect.)
- **Header `raw_refs` are file-granular and omit `anchor_kind`/`anchor_value` →
  COMPLIANT.** The contract requires each ref to "resolve packet/slice/file and
  carry `sha256` plus `hash_basis`" (`:163`); `_raw_refs`
  (`fragrantica_lake.py:157-177`) does exactly that. Per-row anchors
  (`html_selector` / `#parentNNNN`) are preserved in the payload handles
  (`cleaning/models.py:120-193`; confirmed by
  `…projection_integration.py:50-51`). Collapsing many same-file rows to one
  header ref is not prohibited. Informational only: header-level consumers cannot
  pinpoint a specific review without parsing the payload.
- **`derived_refs: []` → COMPLIANT.** `derived_refs` is "Required when a record…
  is generated from prior derived records" (`:164`). The Cleaning record
  re-derives projection from **raw** (`fragrantica_lake.py:52-58`,
  hash-verified via `load_raw_packet`), not from the sibling
  `projection_fragrantica` record. The Derived-Layout contract states each
  epistemic kind "stays a sibling… never a merged cross-kind blob"
  (`…derived_layout_index_rebuild_contract_v0.md:92-93`). So no derived-record
  edge is required. (Design observation, not a finding: the lineage graph has no
  cleaning→projection edge; projection method/version/certification are carried
  in the payload and `projection_ref`.)
- **Length-bin `counts_preserved=True` → defensible.** `CleaningPreservationCheck`
  *forces* all six preservation booleans to `True`
  (`cleaning/models.py:285-304`), so preservation here is structural (no
  rows dropped/merged, hierarchy/binding intact), not numeric precision. The
  exact count is retained in `original_value` ("24") with the bin as
  `transformed_value`, so the length-bin entry is the one normalization entry
  that correctly shows what changed.
- **Vote-field carry → authorized.** The handoff explicitly lists "source-visible
  rating/performance enum carry" as a Cleaning-lane activity
  (`…cleaning_handoff_v0.md:111`). Residual low-confidence nits only: the
  `PROPAGATION` class is described by the contract around warning/receipt
  propagation (`…cleaning_spine_foundation_v0.md:163`) and the carry duplicates
  source facts already addressable via the projection handle, with
  `original_value == transformed_value`. Non-destructive and sanctioned; not a
  finding.
- **Repo-map change → accurate and bounded.** The single changed row
  (`orca_repo_map_v0.md:536`) adds "source-family adapters/lake writers including
  Fragrantica projection→Cleaning and append-only Cleaning derived records" and
  preserves the non-claim "not the gated production Cleaning lane, acceptance, or
  readiness." It does not turn Cleaning into ECR/Projection/Judgment/product
  proof. Minor: the top-of-file "Refreshed:" changelog line (`:27`) was not
  updated to mention the Cleaning adapter (only the prior projection helper) —
  cosmetic, the structural row is covered.
- **Append-only enforcement → verified.** Enforced by the writer it delegates to:
  `append_record` → `_atomic_create` → `os.link`/`O_EXCL` → `FileExistsError` →
  `DataLakeRootError` (`data_lake/root.py:228-269, 559-575`). Tests cover both
  the default-ULID sibling case and the explicit-duplicate-id raise
  (`test_fragrantica_cleaning_lake_pilot.py:84-111`).
- **Non-claims / no-Judgment-smuggling → verified.** Record adds
  `not_archive_completeness/_demand_signal/_evidence_unit_binding/_judgment/_sentiment_analysis`
  atop `REQUIRED_NON_CLAIMS` (`fragrantica_lake.py:117-127`); coverage carries
  `current_window_only=True, full_archive_captured=False`
  (`:140-144`); models reject Judgment vocabulary in method/residuals
  (`cleaning/models.py:255-266, 316-327`); one handle per row, non-review rows
  untransformed (tests `:69, 131-152`).

---

## Strict-Only Blockers / Not-Proven Boundaries

- This is zero-config findings-only advisory review. No implementation-review
  lane, verdict vocabulary, severity taxonomy, or patch-queue authority is bound;
  the commission withholds them. No formal verdict, readiness, approval,
  validation pass/fail, or patch queue is claimed (`NOT_CLAIMED`).
- Severity labels (Medium/Low) are reviewer materiality ordering only, not an
  overlay-bound severity taxonomy.
- Not proven without a bound lane and live owner authority: that any finding is
  "must-fix," that the lane is or is not "ready," and any remediation ownership.
- Runtime/scale behavior at ~210 cards is reasoned from source + the handoff's
  recorded parse, not executed against a real multi-card packet (the test lake
  uses a 1-card fixture).

## Open Questions (for home/CA)

1. FCR-04: is a Cleaning ledger packet an acceptable Silver `observation`
   payload_kind, or does it need its own record_kind/contract treatment?
2. FCR-02: which disclosure is intended for the ECR ref — presence-gating,
   `status` disclosure, or a documented convention?
3. FCR-03: is packet-capture-time the intended `observed_at` for current-window
   Cleaning records, and what is the contract-permitted shape when capture time
   is not `KNOWN`?
4. FCR-01: keep the review-text whitespace transform despite upstream `_text()`
   normalization, or drop it as redundant?

## Residual Risk

- Highest residual risk is **silent ledger vacuity** (FCR-01) compounding with
  **thin fixtures** (FCR-06): the normalization ledger can look populated and
  green while never demonstrating a real transform, and the ECR ref (FCR-02) can
  read as resolvable provenance that may not exist. None destroys raw evidence
  (raw stays canonical and hash-verified), so all findings are recoverable, but
  they erode the inspectability the Cleaning layer exists to provide.

## Review-Use Boundary

Findings are decision input only. They are not approval, validation, readiness,
mandatory remediation, or executor-ready patch authority until separately
accepted or authorized by the home model / owner.

---

```text
DELEGATED_CODE_REVIEW_RETURN_FOR_HOME_MODEL

Here is the delegated code review result. Adjudicate it under the
delegated-review-patch return contract.

- original commission or review target:
    Read-only adversarial code review of the Fragrantica Cleaning implementation
    on codex/fragrantica-cleaning @ 4ec4eba6 — adapter (cleaning/fragrantica.py),
    lake writer (cleaning/fragrantica_lake.py), two focused tests, and the
    orca_repo_map_v0.md row. Read-only workflow-code-review, adversarial posture.
- implementation context, diff, and reviewed files:
    Branch diff origin/main...4ec4eba6 = exactly the 5 pinned files
    (773 insertions, 1 deletion). All 5 SHA256 pins matched exactly. Worktree
    clean; HEAD adds only this review prompt file.
- findings and implementation evidence:
    FCR-01 (Med) normalization ledger records post-normalization original_value
      (fragrantica.py:129-151,223-231; projection _text at fragrantica_projection.py:611,881-888)
      → original==transformed always; ledger can't show what changed; review-text step redundant.
    FCR-02 (Med) ECR ref attached unconditionally by convention, status=None,
      ref_id identical to real EcrSourceSideReceipt (fragrantica.py:63-67,82,244-249;
      fragrantica_lake.py:58; ecr/models.py:33,385) vs OD-1 "when present" + sibling-lane handoff.
    FCR-03 (Med-low) observed_at == captured_at == capture_time; null observed_at
      on an observation record when capture_time not KNOWN (fragrantica_lake.py:84-88,103-104)
      vs Silver contract :161.
    FCR-04 (Low) record_kind="observation" with no observation object — fit open question.
    FCR-05 (Low) fragrantica_lake.py:5-6 docstring omits <anchor_shard> in derived path.
    FCR-06 (Med) fixtures don't exercise messy whitespace, multi-card raw_refs collapse,
      length-bin spread, raw_refs assertion, null observed_at, or attach_ecr_ref=False.
    Considered-and-cleared (NOT findings): content_hash incl record_id (correct integrity hash),
      raw_refs file-granularity, derived_refs=[] (re-derived from raw), length-bin preservation,
      vote-carry (handoff-authorized), repo-map accuracy, append-only enforcement, non-claims.
- proposed patch, diff, or exact requested edits, if separately authorized:
    NOT_CLAIMED (no patch authority bound; multi-file code diff not delegated-patch-eligible).
- citations:
    cleaning_spine_foundation_v0.md:158,163,141-143,405-408; silver_vault_record_contract_v0.md:160-164,157,263-352;
    derived_layout_index_rebuild_contract_v0.md:74,92-93; cleaning_handoff_v0.md:100,110,111,141-143,249;
    data_lake/root.py:228-269,559-575; cleaning/models.py:222-226,285-304,341-348,411; ecr/models.py:33,385.
- reviewer verdict or recommendation:
    NOT_CLAIMED (zero-config findings-only advisory; no formal verdict authorized by this prompt).
- validation evidence and not-run checks:
    Reran focused suite: 11 passed in 0.83s, exit 0 (Python 3.11.15). git diff --check clean.
    Not run: real multi-card packet; unknown-capture-time path; attach_ecr_ref=False path.
- residual risk:
    Silent ledger vacuity (FCR-01) + thin fixtures (FCR-06) + undisclosed ECR ref (FCR-02);
    all recoverable (raw stays canonical, hash-verified).
- blockers, off-scope flags, and not-proven boundaries:
    No bound review lane / verdict vocab / severity taxonomy / patch queue (withheld by prompt).
    Off-scope: live capture, archive completeness, ECR redesign, Judgment, demand.
    De-correlation: cross_vendor (author OpenAI/Codex; reviewer Anthropic/Claude).
```
