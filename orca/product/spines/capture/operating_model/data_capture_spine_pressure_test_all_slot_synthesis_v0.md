# Data Capture Spine Pressure-Test All-Slot Synthesis v0

```yaml
retrieval_header_version: 1
artifact_role: Product artifact
scope: All-slot pressure-test synthesis across Slots 1-3 for recurring Data Capture obligation pressure, visible limits, and the next bounded owner decision.
use_when:
  - Checking what the first authorized three-slot Data Capture pressure-test batch did and did not establish.
  - Comparing recurring obligation pressure across Slots 1, 2, and 3 before any contract hardening or source-access scoping decision.
  - Routing the next bounded owner decision without authorizing runtime, tooling, ECR, Cleaning, or Judgment work.
authority_boundary: retrieval_only
input_hashes:
  docs/product/core_spine_v0_data_capture_spine_obligation_contract_v0.md: B06BD6722F76D223E7A122B7F97B967431BDEEE5D4E41AD6DCCEF81903DAC8C5
  docs/product/data_capture_spine_pressure_test_commissioning_plan_v0.md: 3D9AC208A8AF68160A43F3EB3512082BF0F9B10D3840331FE82F544E307820EB
  docs/product/data_capture_spine_pressure_test_execution_authorization_v0.md: BCA50C80A7EAA889DC0B01377FFB80635BAC6DDC30F3A4FA654B42CC319CACA3
  docs/product/data_capture_spine_pressure_test_slot1_mi_biws_capture_session_v0.md: 8FE4C42018A93F758FFD0EF95763DC126B360A614508105EB6BB1BD52B12508E
  docs/product/data_capture_spine_pressure_test_slot2_teal_capture_session_v0.md: 1BCDCDF7F60942E8BC270709225733276FA21EEF890B1BBA66313C0ED367FC94
  docs/product/data_capture_spine_pressure_test_slot3_interim_evidence_synthesis_v0.md: 8CBD026A4BD4954921F7EF4EE2769A9948600701257D7797163DBD57ACB2A051
  docs/product/data_capture_spine_pressure_test_slot3_combined_handoff_v0.md: E41C96D7FFD1C8F90187DD30AD4F7F4E70C82A717B7B89FEF78C08926608BB00
stale_if:
  - Any named source artifact or pinned hash changes.
  - A later all-slot synthesis supersedes this artifact.
  - The obligation contract, commissioning plan, or execution authorization is materially amended before the next owner decision.
```

## Status

Status: `DATA_CAPTURE_PRESSURE_TEST_ALL_SLOT_SYNTHESIS_V0`.

This artifact synthesizes the first authorized three-slot Data Capture
pressure-test batch at the all-slot level only. It preserves recurring pressure,
visible limits, and a bounded next-decision route. It does not validate the
Data Capture Spine, discharge the pressure test, harden the obligation
contract, or authorize runtime/tooling work.

```text
orca_start_preflight:
  agents_read: yes
  overlay_read: yes
  source_pack: custom all-slot Data Capture pressure-test synthesis pack
  edit_permission: docs-write for one all-slot synthesis Markdown artifact
  target_scope: docs/product/data_capture_spine_pressure_test_all_slot_synthesis_v0.md
  dirty_state_checked: yes
  blocked_if_missing:
    - AGENTS.md
    - .agents/workflow-overlay/README.md
    - docs/product/core_spine_v0_data_capture_spine_obligation_contract_v0.md
    - docs/product/data_capture_spine_pressure_test_commissioning_plan_v0.md
    - docs/product/data_capture_spine_pressure_test_execution_authorization_v0.md
    - docs/product/data_capture_spine_pressure_test_slot1_mi_biws_capture_session_v0.md
    - docs/product/data_capture_spine_pressure_test_slot2_teal_capture_session_v0.md
    - docs/product/data_capture_spine_pressure_test_slot3_interim_evidence_synthesis_v0.md
```

Repo-state note:

- Expected branch `main` matched.
- Expected HEAD short SHA `fb7f1a1` matched.
- The worktree was materially dirtier than the task's narrow expectation,
  including modified overlay/control-plane files and unrelated untracked docs.
  This synthesis treats that state as visible context, not as proof that the
  named source pack is invalid.

## Source Basis

The required source hashes matched the expected values at synthesis time.

| Source artifact | SHA256 | Role in this synthesis |
| --- | --- | --- |
| `docs/product/core_spine_v0_data_capture_spine_obligation_contract_v0.md` | `B06BD6722F76D223E7A122B7F97B967431BDEEE5D4E41AD6DCCEF81903DAC8C5` | Controlling obligation and vocabulary surface. |
| `docs/product/data_capture_spine_pressure_test_commissioning_plan_v0.md` | `3D9AC208A8AF68160A43F3EB3512082BF0F9B10D3840331FE82F544E307820EB` | Batch intent, slot shape, and threshold logic. |
| `docs/product/data_capture_spine_pressure_test_execution_authorization_v0.md` | `BCA50C80A7EAA889DC0B01377FFB80635BAC6DDC30F3A4FA654B42CC319CACA3` | Bounded execution and non-authorization boundary. |
| `docs/product/data_capture_spine_pressure_test_slot1_mi_biws_capture_session_v0.md` | `8FE4C42018A93F758FFD0EF95763DC126B360A614508105EB6BB1BD52B12508E` | Slot 1 formal capture session. |
| `docs/product/data_capture_spine_pressure_test_slot2_teal_capture_session_v0.md` | `1BCDCDF7F60942E8BC270709225733276FA21EEF890B1BBA66313C0ED367FC94` | Slot 2 formal capture session. |
| `docs/product/data_capture_spine_pressure_test_slot3_interim_evidence_synthesis_v0.md` | `8CBD026A4BD4954921F7EF4EE2769A9948600701257D7797163DBD57ACB2A051` | Slot 3 recurring-pressure summary. |
| `docs/product/data_capture_spine_pressure_test_slot3_combined_handoff_v0.md` | `E41C96D7FFD1C8F90187DD30AD4F7F4E70C82A717B7B89FEF78C08926608BB00` | Slot 3 final combined handoff posture. |

All-slot source-read boundary for this artifact:

- `AGENTS.md` and `.agents/workflow-overlay/README.md` were read for Orca
  authority.
- This synthesis does not reopen Slot 3 sub-artifacts directly; it relies on
  the required Slot 3 interim synthesis and combined handoff as the named source
  pack for this pass.

## Non-Claims

This artifact does not claim:

- validation;
- readiness;
- pressure-test discharge;
- buyer proof;
- market-launch readiness;
- contract hardening;
- source-of-truth promotion;
- ECR design;
- Cleaning implementation;
- Judgment design;
- runtime/source-system authorization;
- scraper/API/browser/tooling authorization;
- schema/storage/dashboard/test authorization.

This artifact also does not convert Teal WebSearch snippets into verified Teal
source claims, and does not convert Reddit or WSO limits into downstream
Judgment conclusions.

## Slot-Level Summary

| Slot | What the slot captured | Inspectable vs pointer-only vs access-failed | Final capture posture |
| --- | --- | --- | --- |
| Slot 1 - M&I / BIWS | Current pricing facts, bundle names, savings claims, redirect relationships, resume/coaching price points, and archive snapshot availability for a finance-specialized substitute-pricing frame. | Inspectable at fact level: current prices, bundle membership, redirects, and archive-availability dates. Pointer-only or not faithfully preserved: verbatim source language, visible structure, packaging cues, and archive snapshot bodies. | `visible_stop` with `re-capture_posture`. |
| Slot 2 - Teal | Failure posture for Teal live pages and archive pages, URL inventory across product/help/app surfaces, archive-availability dates, and flagged non-verbatim search-summary pointers. | Inspectable: host block, access limits, URL inventory, archive-availability posture, and conflicting non-verbatim pointers. Access-failed: live Teal page bodies and archive snapshot bodies. Pointer-only: search-summary fragments that are not source-backed evidence. | `visible_blocker` with `re-capture_posture`. |
| Slot 3 - Reddit + WSO | Mixed venue pain-language capture, raw/projection-backed Reddit slices, bounded WSO source-language anchors, mixed direct/adjacent/counter-signal context, and final combined venue posture. | Inspectable: current mixed venue posture, Reddit raw/projection-backed text slices, bounded WSO anchors, and visible venue limitations. Pointer-only or incompletely preserved: Reddit image/gallery-dependent meaning, some preview-image slices, WSO raw envelope/screenshots/archive posture, and full comment-graph coverage. | Combined Slot 3 posture: `re-capture_posture`. |

## Cross-Slot Obligation Pattern

| Obligation area | Cross-slot pattern |
| --- | --- |
| #1 Commissioning Gate | Held across all three slots. Each slot stayed tied to a real decision frame rather than free-floating collection. |
| #2 Boundary Compliance | Held across all three slots. None of the slots relied on out-of-bound access; failures were treated as in-bound access limitations, not as excuses to widen boundary. |
| #3-#5 Provenance / mode disclosure / mode-change visibility | Mostly held. Sessions disclosed operator/mode posture, but Slot 3 still shows weaker acquisition-receipt granularity than ideal. |
| #6 Raw Observable Fidelity | Repeatedly strained across all three slots. Slot 1 lost verbatim language and visible structure, Slot 2 lost the source body entirely, and Slot 3 stayed strongest on text anchors but still showed media/raw-envelope gaps. |
| #8-#10 Timing / cutoff / archive posture | Cutoff posture stayed visible, but archive/history remained limited across the batch. Slot 1 and Slot 2 could only capture archive availability, not archive content; Slot 3 kept archive posture visible but did not complete archive lookup. |
| #11 Visibility / access limits | Held as a visibility surface rather than a success surface. All three slots made source-access posture visible enough to inspect, even when the source itself was not fully preserved. |
| #12 Related Context Preservation | Repeatedly strained. Slot 1 preserved related context only at paraphrase/fact level, Slot 2 lost related context with the blocked page bodies, and Slot 3 preserved mixed context but with media and venue-envelope limits still visible. |
| #13 Bundled-Offer Structure Observables | Materially stressed by Slots 1 and 2. Slot 1 captured bundle facts but not visible packaging; Slot 2 could not preserve inspectable bundle structure because the source body never arrived. Slot 3 did not materially test this obligation. |
| #14 Failure / blocker visibility | Held across the batch. The captures did not hide failures; they surfaced them explicitly as limitations, blockers, access failures, or recapture posture. |
| #16 Categorical Handoff Readiness | Repeatedly below clean closure. Slot 1 was partial, Slot 2 was assessed not met, and Slot 3 stayed mixed enough to preserve `re-capture_posture`. |

## What Held

- The amended obligation contract was able to keep failures visible rather than
  letting the slots collapse into generic success/failure language.
- Boundary discipline held. None of the slots solved source difficulty by
  smuggling in forbidden access or downstream reconstruction.
- Capture-mode disclosure held strongly enough that later readers can see
  whether evidence came from live fetches, paraphrase-rendered pages, local raw
  files, bounded source-language anchors, archive-availability queries, or
  search-summary pointers.
- Failure visibility held. Slot 1 did not pretend paraphrase was faithful raw
  capture, Slot 2 did not pretend WebSearch snippets were Teal evidence, and
  Slot 3 did not pretend venue/media gaps were cleaned away.
- Capture-to-downstream boundary discipline mostly held. The artifacts stayed
  out of ECR schema, Cleaning transformations, and Judgment conclusions even
  when the captured surface was weak.

## What Broke Or Stayed Limited

- Raw observable fidelity was the strongest recurring pressure point. The batch
  repeatedly showed that capture is fragile when verbatim text, visible
  structure, archive body content, app/page state, or media binaries are not
  preserved.
- Archive/history posture stayed visible but underpowered. Slot 1 and Slot 2
  could name snapshot existence and dates, but not retrieve the historical body;
  Slot 3 kept mutable-forum archive posture visible without turning it into a
  completed historical packet.
- Related context preservation repeatedly stopped short of fully inspectable
  fairness. Slot 1 was paraphrase-limited, Slot 2 was source-body-empty, and
  Slot 3 remained mixed by design with adjacent and counter-signal context still
  attached.
- Clean categorical handoff did not hold across the batch. Even where parts of
  the evidence were useful, the final slot-level outcomes stayed below a clean
  all-slot handoff standard.
- Slot-specific one-offs remained visible and should not be over-generalized:
  Slot 1 had M&I-to-BIWS redirects and unresolved relationship between legacy
  coaching tiers and current BIWS resume services; Slot 2 had full Teal host
  blocking plus conflicting search-summary pricing; Slot 3 had Reddit
  gallery/image dependence and WSO bounded-anchor-only coverage.

## Source-Access Requirements Surfaced

These are surfaced requirements only. They are not build authorization.

1. Verbatim and source-structure preservation recurred across the batch. Slot 1
   needed it explicitly, Slot 2 could not do anything useful without first
   retrieving the source body, and Slot 3 showed that bounded source-language
   anchors materially improve inspectability.
2. Archive snapshot content retrieval recurred across the batch. Slot 1 and
   Slot 2 both had snapshot-availability evidence without snapshot bodies, and
   Slot 3 kept archive posture visible as a still-open requirement on mutable
   venue surfaces.
3. Multimodal or screenshot-grade preservation recurred where layout or media
   carried meaning. Slot 1 needed it for packaging cues; Slot 3 needed it for
   gallery/image-dependent slices; Slot 2 would likely need it if Teal app or
   pricing-page layout becomes material after access is restored.
4. Public-host access handling surfaced as a real requirement family. Slot 2's
   in-bound Teal 403 pattern is too severe to dismiss as a one-off annoyance if
   broader public-source capture is expected to work.
5. Source-language anchors from the start look materially useful for forum/text
   captures. Slot 3 showed that artifact-internal checking becomes more
   inspectable when the capture keeps bounded source-language anchors visible.

## Contract / Vocabulary Pressure

- The amended nine-state discharge vocabulary absorbed a real earlier pressure.
  Slot 2's old missing-state problem now lands cleanly in
  `access_failed`, `cannot_assess`, and `assessed_not_met` instead of forcing
  vague blocker language.
- The contract's distinction between obligation state, checker token, and
  handoff state remains load-bearing. Slot 1 showed that
  `capture_closure_blocker` is easy to misread as obligation-state `blocked` or
  as a mandatory rerun verdict if the glossary is not kept explicit.
- The separation between Capture-owned handoff readiness and actual ECR receipt
  also remains load-bearing. Slot 1 and Slot 2 both depended on that split to
  avoid pretending that absent downstream machinery is itself a capture-state
  label.
- WSO checker posture deviated from the commissioning plan: the WSO checker was
  artifact-internal Codex, not the separate manual GPT-5.5 UI invocation
  specified for the LLM capture-visibility checker. Under the commissioning
  plan's coupled-hypothesis recording rule, this should be diagnosed separately
  from architecture evidence. Current classification: `patchable` diagnostic
  gap. It does not invalidate the WSO capture by itself, but the next batch
  should either enforce the specified separate-checker posture or explicitly
  authorize an alternate checker posture before treating checker evidence as
  comparable.
- This synthesis does not patch the contract. A later owner decision may choose
  to review checker-posture comparability or acquisition-receipt granularity,
  but this artifact treats those as candidates for later decision, not as
  contract amendments.

## Patchable / Architecture-Threatening Classification

The execution authorization requires post-execution synthesis to classify
findings as `patchable` or `architecture-threatening` before contract
hardening. This artifact applies that classification only for routing the next
owner decision; it does not amend the contract.

| Recurring finding | Cross-slot count | Classification | Rationale |
| --- | --- | --- | --- |
| Raw observable fidelity pressure (#6) | 3 of 3 slots strained | `patchable` within current v2, with source-access scoping needed | The recurrence is severe, but the failure shape is access/fidelity capability rather than a collapse of Capture's layer boundary. Slot 1 needed verbatim/structure preservation, Slot 2 needed in-bound source-body retrieval, and Slot 3 needed media/raw-envelope completeness. The operators did not need ECR schema, Cleaning, Judgment, or runtime semantics to decide the state; they needed better source preservation and access paths. |
| Related context preservation pressure (#12) | 3 of 3 slots strained | `patchable` within current v2, with source-access and capture-format support needed | Context remained visible as a limitation rather than hidden or downstream-reconstructed. The recurrence points to better raw/context preservation mechanics, not to a need for Capture to own Judgment, Cleaning, or ECR design. |
| Archive/history content gap (#8-#10) | 3 of 3 slots limited or incomplete | `patchable` source-access requirement | The batch repeatedly captured archive posture or availability without historical bodies. This is an archive-access/content-retrieval gap, not an architecture breach. |
| Categorical handoff readiness below clean closure (#16) | 3 of 3 slots below clean closure | `patchable` pressure-test outcome; not contract hardening evidence | The current contract made non-clean closure visible across all slots. The right next move is not to pretend handoff succeeded, but to scope the source-access and capture-preservation requirements that would let future captures reach cleaner handoff. |
| WSO checker-posture deviation | 1 of 3 slots, WSO-specific | `patchable` diagnostic/comparability gap | The WSO checker did not follow the commissioning-plan posture of a separate manual GPT-5.5 UI invocation. This affects comparability of checker evidence, not the raw capture evidence itself. It should be fixed or explicitly authorized in the next batch before checker behavior is treated as comparable across venues. |

Classification result: no recurring finding in this batch is classified as
`architecture-threatening` on this record. The 3-of-3 fidelity/context pressure
does meet the count threshold for deliberate classification, but not the
criterion that v2's layer boundary is failing: the pressure is concentrated in
source-access and source-observable preservation, and the artifacts preserved
failure visibility without requiring Capture to take over ECR, Cleaning,
Judgment, schema, or runtime responsibilities. If a later batch shows operators
cannot complete the same classifications without downstream schema/runtime
support, this classification should be reopened under the commissioning plan's
Re-Architecture Trigger logic.

## Capture-To-Downstream Boundary Check

- The batch did not justify letting downstream layers reconstruct source history
  because capture was weak. The recurring lesson is the opposite: if downstream
  would need to reconstruct source history, that is capture pressure.
- Slot 2 stayed on the correct side of the boundary by preserving search-summary
  fragments as pointers only rather than elevating them into Teal evidence.
- Slot 3 stayed on the correct side of the boundary by preserving mixed venue
  context, adjacent pain, and counter-signal material without converting them
  into customer synthesis, credibility ranking, or signal-use conclusions.
- Slot 1 stayed on the correct side of the boundary by marking pricing and
  bundle facts as inspectable-but-limited rather than silently treating
  paraphrase capture as a downstream-ready record.

## Batch-Level Synthesis

The first three-slot batch does not say "Data Capture failed everywhere." It says
something narrower and more useful: the current Data Capture Spine can expose
failure visibly, preserve boundary discipline, and hold off downstream drift,
but it remains materially constrained when the source observable itself is not
preserved with enough fidelity for later inspection.

Across the batch, the repeated pressure is not generic operator confusion and it
is not primarily a boundary-compliance problem. The repeated pressure is source
observability: faithful source language, visible structure, archive body access,
media/layout preservation, and public-host retrieval remain decisive for whether
the capture can travel beyond a pressure-test learning artifact.

That recurring pattern is broader than a one-slot anomaly. Slot 1 shows
fact-level usefulness without faithful packaging capture. Slot 2 shows a full
in-bound access failure where only failure posture survives. Slot 3 shows the
strongest current text-anchor capture, yet still keeps mixed recapture pressure
visible because media/raw-envelope coverage is uneven across venue units.

This is enough evidence to support one bounded next decision. It is not enough
to claim validation, contract hardening, source-of-truth promotion, or runtime
authorization.

## Recommended Next Decision

The evidence record is sufficient to support one bounded owner decision about
the next source-observability step. That is not a claim that the current Data
Capture Spine is adequate for production use, clean capture use, validation, or
broad implementation.

Recommended next decision:

- Decide whether to write a separate owner authorization artifact for a
  docs-only scoping pass aimed only at these recurring cross-slot
  source-observability requirements:
  - verbatim and source-structure preservation;
  - archive snapshot content retrieval;
  - multimodal or screenshot-grade capture where layout/media carries meaning;
  - in-bound public-host access handling for cases like Teal 403;
  - source-language anchors from the start where forum/text capture depends on
    artifact-internal inspection.

Why this is the next decision rather than immediate tooling authorization:

- the repeated pressure is now cross-slot, not isolated to one venue;
- the pressure is concentrated in source-access and source-observable
  preservation rather than in basic contract invisibility;
- the recurring findings have been classified here as `patchable` rather than
  `architecture-threatening` on this record;
- the batch still does not authorize build, runtime, scraper, browser, API, or
  schema work.

If the owner believes checker-posture comparability or acquisition-receipt
granularity must be stabilized before any source-access scoping, the alternative
next move is one narrow docs-only patch-planning step first. This synthesis
does not treat that alternative as the default because the WSO checker-posture
deviation is classified as a `patchable` comparability gap, while the larger
repeated pressure is access/fidelity.

## Validation

- Source-pack hash check: passed for all seven required source artifacts.
- Artifact write-seal hash command: run at closeout; final SHA is reported in
  the operator closeout instead of embedded here.
- Stale/overclaim scan: passed after one non-claim wording cleanup; no hits
  remained.
- Diff hygiene: `git diff --check -- docs\product\data_capture_spine_pressure_test_all_slot_synthesis_v0.md` passed with no reported errors.

These validation steps are artifact-hygiene evidence only. They are not
validation of the Data Capture Spine, pressure-test discharge, or authorization
for downstream work.
