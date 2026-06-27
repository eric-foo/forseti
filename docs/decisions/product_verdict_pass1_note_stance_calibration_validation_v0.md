# Pass-1 Note-Adjective Stance Calibration — Validation Result (v0)

```yaml
retrieval_header_version: 1
artifact_role: Calibration validation record (non-circular blind re-extraction; in-repo audit table; raw corpus off-repo; not buyer-proof, not judgment-quality)
scope: >
  Records the corpus-validation outcome of the Pass-1 note-adjective actionable-stance + SCOPE
  rubric fix (extractor rubric 0.1 -> 0.4) on the claude/calibrate-pass1-note-stance lane: what was
  tested, the non-circular blind result, the evidence-durability gap, and the downstream un-defer
  trigger it fires.
use_when:
  - Checking whether the Pass-1 note-adjective stance calibration is validated and on what evidence.
  - Deciding whether the IG creator-gender demographic lane's un-defer trigger has fired.
  - Upgrading from the committed audit table to a fully re-derivable record (committing the off-repo corpus + labels).
authority_boundary: retrieval_only
open_next:
  - orca-harness/cleaning/transcript_product_extractor.py   # the rubric-0.4 fix this validates
  - docs/decisions/pass1_actionable_stance_calibration_v0.md  # full methodology + per-product audit table
  - docs/workflows/product_verdict_calibration_labeling_protocol_v0.md  # the corpus + blind-label procedure
  - docs/decisions/ig_creator_gender_demographic_signal_lane_scope_defer_v0.md  # the deferred lane this unblocks
branch_or_commit: claude/calibrate-pass1-note-stance (rubric-0.4 fix; SHA churns on rebase)
stale_if:
  - The extraction rubric is changed again (rubric version past 0.4) — re-validate.
  - The owner commits the off-repo corpus + raw labels — upgrade to a fully re-derivable record.
  - The Pass-2 fusion DEFAULT constants change — the verdict-agreement instrument is no longer the v0 default.
```

## Status

`BLIND-VALIDATED — AUDIT TABLE IN-REPO; RAW CORPUS OFF-REPO`. The Pass-1 rubric-0.4 fix is
validated by an INDEPENDENT, non-circular blind re-extraction (see "Result"). The per-product
audit table (gold + machine verdict under each stance set) is committed at
`docs/decisions/pass1_actionable_stance_calibration_v0.md`; the raw per-creator transcripts and the
owner-filled blind-label worklists remain off-repo (local data lake + label files). It is not
buyer-proof, judgment-quality evidence, or a Pass-2 fusion calibration claim.

## Claim tier

Per `orca/product/spines/judgment/claim_ladder/judgment_spine_evidence_ladder_architecture_v0.md`:
product-learning / calibration input. It makes no buyer-proof, judgment-quality,
blind-use-readiness, or Pass-2-calibration claim. A per-product audit table IS committed in-repo;
the raw corpus + blind labels are off-repo and owner-held. Fully re-derivable status requires
committing those raw artifacts (see "Evidence-durability gap").

## What was validated

The Pass-1 actionable-stance rule added to the extraction rubric (extractor rubric version
0.1 -> 0.4). note / accord / scent-profile descriptors ("terrific fresh", "sweet mango") are NOT
stance (the per-mention stance vote falls to ~0); a non-zero stance requires an actionable
product-worth judgment (recommend / prefer / rate / hit/favorite/best/must-have / would-buy). The
final rule (0.4) adds a SCOPE test: a flattering adjective on a NOTE ("a beautiful jasmine note")
is description; only a verdict on the FRAGRANCE AS A WHOLE is stance. This is Pass-1 EXTRACTOR
(rubric) calibration ONLY. The Pass-2 deterministic fusion (`scoring/product_fusion.py`,
`FusionConfig`) was held FROZEN at its uncalibrated v0 default and used only as a fixed measuring
instrument — no fusion constant was changed — per the lane's Pass-1-only Drift Guard.

## Result (non-circular)

- Corpus: 40 records, 10 real IG creators, all four verdict classes (positive / negative / mixed /
  unknown). Owner-authored blind gold labels (judged from the verbatim quote, independent of system output).
- Verdict agreement vs gold: rubric 0.1 = 32/40 (author re-derivation, gold-aware -> CIRCULAR, not
  sufficient). Closed by an INDEPENDENT blind re-extraction (a separate agent re-scored all 42
  mentions with no access to the gold or the author stances): 37/40 at rubric 0.3
  (describing-vs-evaluating), 40/40 at rubric 0.4 (with the scope clause).
- Mechanism: the 8 rubric-0.1 misses were note-description mentions smuggled into a confident
  verdict; under rubric 0.4 they correctly fall to `unknown`.
- No regression (overfit guard): the 25 positive / 4 negative / 1 mixed gold verdicts all held under
  every stance set.
- Provenance: independent non-circular blind re-extraction; per-product audit table committed at
  `docs/decisions/pass1_actionable_stance_calibration_v0.md`. A de-correlated (non-Anthropic) review
  drove the 0.2 -> 0.4 rework, rejecting the initial gold-aware 40/40 as circular and confirming the
  blind methodology and the scope rule.

## Evidence-durability gap (what would make this fully re-derivable)

The committed audit table fixes the per-mention stances + verdicts, so the 32 -> 37 -> 40 agreement
is reconstructable. What remains off-repo: the raw per-creator product-mention transcripts and the
owner-filled blind-label worklists (the `scoring/calibration_corpus.py` worklist shape; under
`ORCA_DATA_ROOT` + local label files). Committing (a) the per-creator mention sets and (b) the
owner-filled blind worklists upgrades this to a fully end-to-end re-derivable record recomputable
via `fuse_product_verdicts` (frozen v0 default) against the gold labels.

## Downstream: un-defer trigger (condition met; not an authorization)

The IG creator-gender demographic signal lane
(`docs/decisions/ig_creator_gender_demographic_signal_lane_scope_defer_v0.md`, status
`SCOPE_CAPTURED — DEFERRED — NOT_AUTHORIZED`) was deferred behind "the Pass-1 note-adjective stance
fix + its corpus validation." With that validation now blind-confirmed, the un-defer trigger
CONDITION is met. Un-deferring still requires explicit bounded owner authorization per `AGENTS.md`;
this record does not authorize that lane.
