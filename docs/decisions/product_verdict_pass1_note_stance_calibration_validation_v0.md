# Pass-1 Note-Adjective Stance Calibration — Validation Result (v0)

```yaml
retrieval_header_version: 1
artifact_role: Calibration validation record (owner-attested result; off-repo evidence; not in-repo-reproduced, not buyer-proof, not judgment-quality)
scope: >
  Records the owner-attested corpus-validation outcome of the Pass-1 note-adjective
  actionable-stance rubric fix (extractor rubric 0.1 -> 0.2) on the
  claude/calibrate-pass1-note-stance lane: what was tested, the attested result, the
  evidence-durability gap, and the downstream un-defer trigger it fires.
use_when:
  - Checking whether the Pass-1 note-adjective stance calibration is validated and on what evidence.
  - Deciding whether the IG creator-gender demographic lane's un-defer trigger has fired.
  - Upgrading this attestation to an independently re-derivable record (committing the off-repo corpus + labels).
authority_boundary: retrieval_only
open_next:
  - orca-harness/cleaning/transcript_product_extractor.py   # the rubric-0.2 fix this validates
  - docs/workflows/product_verdict_calibration_labeling_protocol_v0.md  # the corpus + blind-label procedure
  - docs/decisions/product_verdict_fusion_calibration_surface_v0.md  # Pass-2 fusion (frozen v0 instrument; separate track)
  - docs/decisions/ig_creator_gender_demographic_signal_lane_scope_defer_v0.md  # the deferred lane this unblocks
branch_or_commit: claude/calibrate-pass1-note-stance (rubric-0.2 fix; first committed 18aca1fc, SHA churns on rebase)
stale_if:
  - The extraction rubric is changed again (rubric version past 0.2) — re-validate.
  - The owner commits the off-repo corpus + labels — replace this attestation with the re-derivable record.
  - The Pass-2 fusion DEFAULT constants change — the verdict-agreement instrument is no longer the v0 default.
```

## Status

`OWNER-ATTESTED — NOT IN-REPO-REPRODUCED`. The Pass-1 rubric-0.2 fix is reported
VALIDATED by the owner on a real owner-labeled corpus (see "Attested result"). The
corpus, blind labels, and agreement readout are held off-repo and are NOT committed
here, so this record is an owner attestation, not an independently re-derivable in-repo
validation. It is not buyer-proof, judgment-quality evidence, or a Pass-2 fusion
calibration claim.

## Claim tier

Per `orca/product/spines/judgment/claim_ladder/judgment_spine_evidence_ladder_architecture_v0.md`:
product-learning / calibration input. It makes no buyer-proof, judgment-quality,
blind-use-readiness, or Pass-2-calibration claim. In-repo durable evidence for the run
is absent (`no_durable_evidence` in-repo); the attested evidence is off-repo and
owner-held. Upgrading the tier requires committing the corpus + labels so the result is
re-derivable (see "Evidence-durability gap").

## What was validated

The Pass-1 actionable-stance rule added to the extraction rubric (extractor rubric
version 0.1 -> 0.2): note / accord / scent-profile descriptors ("terrific fresh",
"sweet mango") are NOT stance (the per-mention stance vote falls to ~0); a non-zero
stance requires an actionable product-worth judgment (recommend / prefer / rate /
hit/favorite/best/must-have / would-buy). This is Pass-1 EXTRACTOR (rubric) calibration
ONLY. The Pass-2 deterministic fusion (`scoring/product_fusion.py`, `FusionConfig`) was
held FROZEN at its uncalibrated v0 default and used only as a fixed measuring
instrument — no fusion constant was changed — per the lane's Pass-1-only Drift Guard.

## Attested result (owner; provenance: the rubric-0.2 fix commit message)

- Corpus: 40 records, 10 real IG creators, all four verdict classes (positive /
  negative / mixed / unknown). Owner-authored blind gold labels.
- Verdict agreement vs gold: rubric 0.1 = 32/40; rubric 0.2 = 40/40.
- Mechanism: the 8 rubric-0.1 misses were note-description mentions smuggled into a
  confident verdict; under rubric 0.2 they correctly fall to `unknown`.
- No regression (overfit guard): the 25 positive / 4 negative / 1 mixed gold verdicts
  all held.
- Provenance: owner-authored, recorded in the rubric-0.2 fix commit message on this
  lane. NOT re-derived in this record.

## Evidence-durability gap (what would make this re-derivable)

The captured per-creator mentions and the filled blind-label worklists are off-repo
(local data lake under `ORCA_DATA_ROOT` + local label files) and are not committed. To
upgrade this attestation to an independently re-derivable record, commit: (a) the
per-creator product-mention sets at rubric 0.1 and 0.2, and (b) the owner-filled
blind-label worklists (the `scoring/calibration_corpus.py` worklist shape). The 32/40
-> 40/40 agreement is then recomputable via `fuse_product_verdicts` (frozen v0 default)
against the gold labels. The repo's receipt-field provenance gate
(`.agents/workflow-overlay/validation-gates.md`) does not clear a self-asserted result,
so until those artifacts are committed this stays an owner attestation, not a cleared
in-repo validation.

## Downstream: un-defer trigger (condition met; not an authorization)

The IG creator-gender demographic signal lane
(`docs/decisions/ig_creator_gender_demographic_signal_lane_scope_defer_v0.md`, status
`SCOPE_CAPTURED — DEFERRED — NOT_AUTHORIZED`) was deferred behind "the Pass-1
note-adjective stance fix + its corpus validation." With that validation now
owner-attested, the un-defer trigger CONDITION is met. Un-deferring still requires
explicit bounded owner authorization per `AGENTS.md`; this record does not authorize
that lane, and the attestation strengthens to a cleared validation only when the
off-repo evidence above is committed.
