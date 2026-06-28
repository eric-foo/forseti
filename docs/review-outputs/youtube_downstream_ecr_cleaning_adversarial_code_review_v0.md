# YouTube Downstream ECR Cleaning — Adversarial Code Review v0

```yaml
retrieval_header_version: 1
artifact_role: Review output (advisory implementation/code review)
scope: >
  De-correlated adversarial implementation/code review of the YouTube caption ->
  ECR source-side receipts -> CleaningPacket smoke-runner wiring and the YouTube
  transcript product-mention cleaning validation.
use_when:
  - Adjudicating whether to keep the YouTube downstream ECR-cleaning diff.
  - Checking what this cross-vendor review verified, found, and did not claim.
authority_boundary: retrieval_only
commission_prompt: docs/prompts/reviews/youtube_downstream_ecr_cleaning_adversarial_code_review_prompt_v0.md
reviewed_by: claude-opus-4.8        # actual reviewing model; prompt templated this operator_to_fill
authored_by: gpt-family-codex
de_correlation_bar: cross_vendor_discovery   # author=OpenAI/GPT-family, reviewer=Anthropic/Claude (provably different vendor lineage)
same_vendor_rationale: not_applicable        # required only for same_vendor_sanity
reviewer_verdict: NOT_CLAIMED       # no bound Orca review lane supplied; advisory findings-only
branch: codex/youtube-downstream-ecr-cleaning
reviewed_commit: 014eeb77339665e4d7885d53b8fc2fdf195a62b5   # implementation under review
observed_head: 64006f4440351fed1b172734072ead23aa08efd6     # HEAD = reviewed_commit + the filed review prompt only
```

## Source Context

**Declaration: `SOURCE_CONTEXT_READY`.**

All required Orca authority/routing sources, both validation targets, and the
relevant adjacent implementation sources were read from the target worktree
(`C:\Users\vmon7\Desktop\projects\orca\worktrees\youtube-downstream-ecr-cleaning`)
at the reviewed commit.

**Branch/head note (benign, non-blocking).** The prompt's `expected_head` is
`014eeb77`; the actual `HEAD` is `64006f44`. Verified: `64006f44`'s parent **is**
`014eeb77`, and the only diff between them is the addition of this review prompt
file (`docs/prompts/reviews/youtube_downstream_ecr_cleaning_adversarial_code_review_prompt_v0.md`).
No target implementation file changed after the prompt was filed
(`git diff 014eeb77 HEAD -- orca-harness/` is empty). This is exactly the
`dirty_state_allowance` case ("continue only if [changes] are exactly the filed
prompt artifact"). The implementation under review (`014eeb77`) is intact and
byte-identical to the diff the prompt describes (3 files, +231/-3).

### Source-read ledger

| Source | Role | Read |
|---|---|---|
| `AGENTS.md` (+ overlay README/source-loading via prior context) | Orca behavior kernel / scope | yes (kernel in session context) |
| `.agents/workflow-overlay/review-lanes.md` | review authority, findings-first, provenance fields, two-bar de-correlation | yes |
| `.agents/workflow-overlay/delegated-review-patch.md` | route decision (multi-file diff → read-only code review, not single-artifact patch) | yes |
| `.agents/workflow-overlay/safety-rules.md` | reviewer source-read-only, no commit/push/edit | yes |
| `docs/prompts/handoffs/youtube_downstream_ecr_cleaning_lane_handoff_v0.md` | upstream commission; success signal + Drift Guard (fitness reference) | yes |
| `orca-harness/runners/run_capture_ecr_cleaning_smoke.py` | **target** — the wired runner | yes (full) |
| `orca-harness/tests/unit/test_capture_ecr_cleaning_smoke_runner.py` | **target** — smoke test | yes (diff + youtube grep) |
| `orca-harness/tests/unit/test_transcript_product_lake.py` | **target** — cleaning validation | yes (full) |
| `orca-harness/ecr/deriver.py` | the four source-agnostic ECR derivers | yes (full) |
| `orca-harness/ecr/models.py` | posture/receipt schemas + clears invariant | yes (full) |
| `orca-harness/cleaning/models.py` | CleaningInputHandle / RawAnchor / EcrRef / Packet uniqueness | yes (full) |
| `orca-harness/cleaning/transcript_product_extractor.py` | CE5+CE9 quote-locate → timestamp fusion | yes (full) |
| `orca-harness/source_capture/transcript/caption_packet.py` | caption packet shape + hardcoded postures | yes (full) |
| `orca-harness/source_capture/transcript/asr_packet.py` | ASR sibling shape (cross-family question) | yes (full) |
| `orca-harness/source_capture/models.py` (VisibleFactStatus) | confirms `not_applicable` is a non-KNOWN status | yes (targeted) |
| Product/contract spines (ECR frame, data/cleaning boundary, extraction spec, medallion) | boundary claims | resolved via handoff Drift Guard + code; spine docs not re-opened (boundary already decisive from code + handoff) |

Disclosure: the five product/contract spine docs listed "only to resolve
boundary claims" were **not** re-read in full; the boundary questions (Q8) were
resolved decisively from the code, the cleaning models' Judgment-token guards,
the `test_no_llm_imports` pass, and the handoff's Drift Guard. If the home model
wants the spine-level fitness reference attacked directly, that is a named
not-run gap below.

## Method & Authority

- Route (confirmed against `delegated-review-patch.md`): this is a **multi-file
  implementation/code diff**, so it is correctly routed as **read-only
  adversarial code review**, not the single-artifact delegated review-and-patch
  convention. No patch is authored; no `patch_queue_entry` is emitted.
- De-correlation: author = OpenAI/GPT-family Codex; reviewer = Anthropic/Claude
  (Opus 4.8). These are provably different vendor lineages, so the
  **cross-vendor discovery** bar is satisfied for *who* ran the pass. This does
  not create formal verdict authority — no bound Orca review lane was supplied,
  so the review stays **findings-only / advisory** (`reviewer_verdict:
  NOT_CLAIMED`).
- `workflow-deep-thinking` / `workflow-code-review` were applied as the
  framing/finding method after source readiness, per the Source-Gated Method
  Contract. Strict review claims are `NOT_CLAIMED`.

## Findings

Findings lead. Severity (`blocker` / `major` / `minor`) is **prioritization
only**, not formal Orca verdict authority. No `blocker` found.

---

### F1 — `major` — YouTube entry's own fail-closed guards have zero negative-test coverage

- **target:** `orca-harness/runners/run_capture_ecr_cleaning_smoke.py:239-266`
  (the three YouTube-specific guards) and
  `orca-harness/tests/unit/test_capture_ecr_cleaning_smoke_runner.py` (only the
  happy-path youtube test, line 211).
- **evidence:** `_process_youtube_entry` adds three fail-closed guards:
  (a) `if packet.source_family != "youtube": raise ValueError(...)` (line 239) —
  the cross-family false-positive defense; (b) the absent-preserved-file
  `raise ValueError` (line 255); (c) integrity verification via
  `_verified_preserved_file` (line 260, hash/path recompute). A grep of the test
  file for `youtube` returns only the happy-path test
  `test_runner_writes_ecr_receipts_and_cleaning_packet_for_youtube` (line 211)
  and the empty-manifest regex update (line 792). **None** of the three guards is
  exercised by a YouTube test. By contrast, retail/reddit/instagram each carry
  negative tests (anchor-unverified, packet_id mismatch, capture-validity).
- **authority/evidence basis:** Review Q4 (cross-family false positives) and Q7
  (missing negative tests); the handoff success signal requires the YouTube test
  to mirror "the reddit/instagram cases," and those cases include negative
  coverage.
- **impact:** the guards are presently correct (verified by reading; the
  happy-path test and the full-suite re-run are green), so this is a
  **durability / regression-protection** gap, not a live defect. But a future
  change that weakened the cross-family guard (e.g. accepted any `source_family`,
  or dropped the absent-file/hash check on this path) would pass the entire
  suite — the cross-family false-positive defense (the explicit subject of Q4)
  is unprotected.
- **minimum closure condition:** the YouTube path's three guards each have at
  least one test asserting `ValueError` — (a) a non-youtube `source_family`
  packet placed in the `youtube` manifest slot, (b) a slice referencing an absent
  preserved `file_id`, (c) (ideally) a tampered/hash-mismatched preserved file.
- **next authorized action:** author/owner decision to add the negative tests
  (advisory; not mandatory remediation).
- **validation expectation:** each new test fails if its guard is removed and
  passes with the guard present.

---

### F2 — `minor` — Every slice-referenced preserved file is elevated to a Cleaning input handle, including harness-authored `capture_metadata.json`

- **target:** `run_capture_ecr_cleaning_smoke.py:250-286`;
  `source_capture/transcript/caption_packet.py:110` (the single slice references
  both the raw `*.captions.*.json3` **and** `capture_metadata.json`); test
  assertion `handle_count == 2` / `preserved_file_count == 2` (lines 281-282).
- **evidence:** the handle loop builds one `CleaningInputHandle` per
  `(slice, preserved_file_id)` with no content-vs-metadata distinction. The
  caption packet's `slice_01` references both preserved files, so
  `capture_metadata.json` — a harness-generated `json.dumps(identity)` blob, not
  captured source content — becomes a first-class Cleaning input handle.
- **authority/evidence basis:** the review objective asks that Cleaning input
  handles be "file-level and source-backed rather than invented row/projection
  anchors." Both handles **are** file-level and source-backed (real
  `file_id`/`relative_packet_path`/`sha256`/`hash_basis`, hash-verified), so the
  stated bar is met — this is a semantic-scope question, not a contract
  violation. Contrast: the reddit path anchors handles to the raw HTML file only;
  retail/IG anchor to projection rows.
- **impact:** downstream Cleaning receives a handle pointing at capture metadata
  rather than source content, which can inflate the handle count and create
  downstream noise. It is inert in *this* smoke (no transform runs unless
  `--include-cleaning-transform-smoke`), but it shapes the durable
  `cleaning_packet.json` artifact and the YouTube CleaningPacket contract shape.
- **minimum closure condition:** the home model decides whether the YouTube entry
  should restrict handles to content files (e.g. the `.json3` captions) or
  whether metadata-as-handle is intended; if intended, it is documented so
  downstream Cleaning does not treat it as cleanable source text.
- **next authorized action:** owner/author design decision.
- **validation expectation:** if restricted to content files, the youtube test's
  `handle_count`/`preserved_file_count` assertions update to reflect the chosen
  contract.

---

### F3 — `minor` — YouTube entry gates only `source_family`, not `source_surface`; ASR breadth is silent and untested

- **target:** `run_capture_ecr_cleaning_smoke.py:239-242`;
  `source_capture/transcript/asr_packet.py:104-105`.
- **evidence:** the guard checks only `packet.source_family != "youtube"`. The
  ASR sibling builds packets with `source_family="youtube"` and
  `source_surface="youtube_audio"` (captions use `"youtube_captions"`). So an ASR
  audio packet dropped into the `youtube` manifest slot would be **silently
  accepted** and processed identically (file-level handles over the audio bytes +
  `capture_metadata.json`).
- **authority/evidence basis:** Review Q4 (manifest/family consistency tight
  enough to prevent cross-family false positives). The handoff scopes "wire the
  **caption** surface first; ASR/audience-post are fast-follow" — leaving the
  caption-vs-transcript-family breadth of the `youtube` slot unstated.
- **impact:** ambiguity about whether the `youtube` slot is caption-only or
  transcript-family-wide. Either intent is defensible, but neither is asserted by
  a test nor documented, so a future ASR wiring could silently double-handle or
  diverge from the intended contract.
- **minimum closure condition:** state the intent — if caption-only for now,
  gate `source_surface == "youtube_captions"` (or name it a known limitation); if
  transcript-family-wide, add a note/test so ASR acceptance is deliberate.
- **next authorized action:** owner/author decision.
- **validation expectation:** a test pins whichever contract is chosen.

---

## Strengths Verified (no defect; recorded so the home model can rely on them)

- **ECR postures derive through the shared, source-agnostic path — no YouTube
  override.** `_process_youtube_entry` calls the same `_derive_ecr_receipt`
  (which calls all four derivers `derive_identity/inspectability/timing/
  source_visibility_postures`) that retail/reddit/instagram use. This matches the
  handoff's Frozen Decision ("ECR derivers are source-family-agnostic; YouTube
  reuses them unchanged").
- **Honest non-clears (the handoff's central instruction).** For the caption
  packet: `identity` clears (resolved youtube/canonical_url) and `inspectability`
  clears (verifiable sha256), but **`timing` does not clear** (residual
  `status: not_applicable`, since `cutoff_posture=not_applicable` is non-KNOWN and
  only `pre_cutoff` clears) and **`source_visibility` does not clear** (value
  `current_capture_only`, not in the `{archive_only, not_applicable}` clearing
  set). The implementation **did not force a clear** — exactly what the handoff
  demanded ("surface a posture gap rather than forcing an ECR clear"). The
  orientation-map claim that `not_applicable` *clears* SP-3 was wrong; the code
  is correct.
- **File-level, source-backed raw anchors, no projection refs.** `anchor_kind="file"`,
  real hash-verified anchors, `projection_ref is None`, and
  `ecr_ref.packet_id == raw_anchor.packet_id` (enforced by the
  `CleaningInputHandle` model validator and asserted by the test).
- **Boundary (Q8) honored — no overclaim.** No Pass-2/gold verdict, no
  projection/`derived_retrieval`, no live LLM transport (the `cleaning/`-only
  LLM zone holds; `tests/contract/test_no_llm_imports.py` passed on my re-run),
  no IG edits (diff touches only the smoke runner + 2 tests). `NON_CLAIMS` are
  written into both the ECR and summary artifacts.
- **Cleaning validation is genuinely strengthened.** The product-lake test now
  asserts the meaningful silver fields: `mention_count`, `video_id`,
  `transcript_source == "caption"`, the `source_pointer` quote, **and both**
  `start_ms == 3000` / `end_ms == 6000` mapped to the covering cue — exercising
  the CE5+CE9 fusion (`locate_quote` proves the quote is a real substring and
  assigns the timestamp from the cue; the model cannot fabricate either).

## Review Questions — direct answers

1. **Mirrors the right shape?** Yes — reddit-shaped (packet → `source_slices` →
   file-level handles), not retail/IG projection. No projection assumptions
   inherited.
2. **`source_slices` → Cleaning handles with file anchors, no projection refs,
   valid ECR refs?** Yes (see Strengths). Caveat F2 on *which* files become
   handles.
3. **SP-3/SP-6 residuals honest, not forced clear?** Yes — both surfaced as
   non-clearing in the receipt. Strength, not a finding.
4. **Family/manifest validation tight enough vs cross-family false positives?**
   Partially: `source_family` is checked (blocks retail/reddit/IG), but only
   family not surface (F3), and the guard is **untested** (F1).
5. **Summary distinguishes YouTube files/handles for future inspectors?** Yes —
   `source_surface`, `slice_count`, `preserved_file_count`, `handle_count`,
   `youtube_sources` count.
6. **Product-lake test asserts meaningful silver fields?** Yes — strengthened
   (see Strengths).
7. **Missing negative tests?** Yes → **F1** (wrong source_family, absent
   preserved source, hash mismatch on the youtube path).
8. **Any implied validation/readiness/gold/live-transport/projection overclaim?**
   No — boundary honored.

## Open Questions & Residual Risk

- **O1 (latent):** a preserved file referenced by *no* slice silently produces no
  handle and no finding. Not reachable by the current caption producer
  (slice_01 references both files), and the summary exposes
  `preserved_file_count` vs `handle_count` so a mismatch is inspectable — but no
  warning fires.
- **O2 (weaker cross-check, not a defect):** on the YouTube path,
  `_verified_preserved_file`'s `expected_*` arguments are read from the **same**
  packet manifest it then validates against, so the "consolidation vs manifest"
  cross-check that makes the function meaningful for reddit collapses to a
  tautology here. Recompute-against-manifest integrity still holds; there is just
  no second source to reconcile.
- **O3 (defensible):** the YouTube entry has no `findings` channel (cannot emit
  smoke `findings`). Acceptable for a raw-preserved caption packet — there is no
  projection/anchor to verify, and the non-clearing postures are carried in the
  ECR receipt.
- **Not-run fitness check:** the five product/contract spine docs were not
  re-read; the SP-1/2/3/6 semantics were verified against `ecr/deriver.py` +
  `ecr/models.py` + the handoff rather than against the spine architecture plan
  directly. If the home model wants the spine-level fitness reference attacked,
  that is open.

## Validation Evidence

**Inspected — and independently re-run (not merely author-supplied):**

```powershell
cd orca-harness
python -m pytest -p no:cacheprovider -q `
  tests/unit/test_capture_ecr_cleaning_smoke_runner.py::test_runner_writes_ecr_receipts_and_cleaning_packet_for_youtube `
  tests/unit/test_transcript_product_lake.py::test_runner_extracts_caption_transcript `
  tests/contract/test_no_llm_imports.py
# observed: ...  [100%]  (3 passed)
```

I re-ran the targeted subset (the YouTube smoke test, the caption-transcript
cleaning test, and the no-LLM-imports contract test) and it passed `[100%]`,
independently confirming the author's reported `[100%]` for that subset.

**Validation not run / not independently revalidated:**
- The **full** `orca-harness` suite (`python -m pytest`) — author reported green
  (`...[100%]` with one unrelated `PytestUnknownMarkWarning`); I did **not**
  re-run the whole suite, so the broader green is author-supplied.
- The author's "one test-regex correction" between runs was not reproduced.

## Review-Use Boundary

These findings are **decision input only**. They are **not** approval,
validation, readiness, acceptance, merge safety, mandatory remediation, or
executor-ready patch authority, and carry **no** formal Orca review verdict
(`NOT_CLAIMED`), until separately accepted or authorized. Severity labels are
prioritization only. No source file was edited; nothing was staged, committed, or
pushed.

---

```yaml
review_courier:
  output_mode: filesystem-output
  report_path: docs/review-outputs/youtube_downstream_ecr_cleaning_adversarial_code_review_v0.md
  commission: adversarial implementation/code review of YouTube downstream ECR-cleaning diff
  target:
    - orca-harness/runners/run_capture_ecr_cleaning_smoke.py
    - orca-harness/tests/unit/test_capture_ecr_cleaning_smoke_runner.py
    - orca-harness/tests/unit/test_transcript_product_lake.py
  authority: advisory implementation/code review; formal review verdict NOT_CLAIMED
  decision_criteria: YouTube packet-to-ECR traceability, honest residual visibility, Cleaning silver validation, no scope drift
  evidence_summary: >
    ECR receipt derived via the shared source-agnostic derivers (no YouTube override);
    timing + source_visibility honestly do NOT clear (no forced clear); file-level
    hash-verified raw anchors with no projection_ref and matching ecr_ref; product-lake
    test asserts mention_count/video_id/transcript_source/quote/start_ms/end_ms via CE5+CE9.
    Targeted tests independently re-run green. Main gaps: no negative tests for the YouTube
    guards (F1), capture_metadata.json elevated to a Cleaning handle (F2), only source_family
    gated not source_surface (F3).
  reviewer_verdict: NOT_CLAIMED
  de_correlation_bar: cross_vendor_discovery
  reviewed_by: claude-opus-4.8
  authored_by: gpt-family-codex
  source_context: SOURCE_CONTEXT_READY
  finding_ids: [F1, F2, F3]
  finding_severities: {F1: major, F2: minor, F3: minor}
  minimum_closure_conditions:
    - F1: negative tests asserting ValueError for wrong source_family, absent preserved file, and hash mismatch on the YouTube path
    - F2: decide+document whether capture_metadata.json should be a Cleaning input handle or handles restrict to content files
    - F3: state caption-only vs transcript-family intent for the youtube slot; gate source_surface or note the breadth
  next_authorized_action: home model adjudicates findings before keeping any change
  non_claims:
    - not approval
    - not validation
    - not readiness
    - not patch authority
    - not live transport
    - not projection
    - not derived retrieval
    - not gold or Judgment output
```
