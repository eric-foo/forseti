# Open Decision — Decision-Frame cutoff commissioning (how captured data acquires a real cutoff)

```yaml
retrieval_header_version: 1
artifact_role: Cross-lane open-decision record (decision-needed; judgment-model/owner-owned)
scope: The judgment-model/owner decision on how a commissioned capture acquires a real cutoff posture from a Decision Frame, so captured data CLEARS ECR for an actual decision instead of residualizing. The source-side (ECR) half is already decided (keep commissioning generic; no per-source path); this is the remaining owner/judgment half.
use_when:
  - Picking up the Decision-Frame / commissioned-capture question (how real captures get a cutoff for a real decision).
  - Resuming the judgment lane and deciding what unblocks a cleared real-case run (e.g. Canoo/Walmart).
  - Resolving where the cutoff posture is authored (operator-at-commissioning vs derived).
authority_boundary: retrieval_only
open_next:
  - docs/hygiene/precompact_judgment_spine_v2.md
  - docs/workflows/reddit_capture_to_ecr_consumption_probe_finding_v0.md
  - docs/product/core_spine_v0_data_capture_spine_obligation_contract_v0.md
downstream_consumers:
  - The judgment-model/owner decision that frames a real case and supplies its cutoff.
stale_if:
  - A Decision Frame model + cutoff-authoring rule is decided/authored.
  - The capture -> ECR cutoff contract changes.
```

**For:** the judgment-model / owner lane that owns the Decision Frame.
**From:** the ECR source-side lane (the derivers), 2026-06-09.
**Status:** advisory / decision-needed — NOT a decision made here, NOT implementation, NOT a readiness or JSG-01-unfreeze claim. JSG-01 stays FROZEN.

## The crisp question

When a real decision is judged, **how does a commissioned capture acquire that decision's cutoff posture**, so the captured data CLEARS ECR instead of residualizing as `unknown_with_reason`? Three sub-decisions:

1. **What a Decision Frame is, and who/what creates it** — the record that commissions a capture for a specific decision and carries its cutoff. (Per the obligation contract: "if there is no Decision Frame, Data Capture Spine has not started.")
2. **Who authors the cutoff posture, and how** — operator-set at commissioning time (an attested `pre/post_cutoff`), or **derived** (computed from the decision's date against captured-content timestamps)? Different trust and error properties; an owner policy choice.
3. **How the cutoff threads Decision Frame -> capture -> ECR** — the capture path already *accepts* a `cutoff_posture` (`run_source_capture_http_packet` / `source_capture.writer`); what is unauthored is the Decision Frame that *supplies* it.

## Already settled (context — do not relitigate)

- **ECR is source-agnostic and its clearing path fires on real data.** Verified 2026-06-09: a real archive.org packet drives all four source-side derivers and SP-6 emits `archive_only` (clears) on a real artifact. So no source-specific producer is needed — only a supplied cutoff.
- **The source-side half is decided (ECR lane):** keep commissioned capture (and the cutoff it supplies) a **uniform, cross-source** concern via the existing generic path — **no per-source (e.g. Reddit) commissioned path.** Rationale: lower lock-in; the capability is already generic and source-agnostic.
- **The residual is by design** (Ob.9): `unknown_with_reason` when no Decision Frame supplies a cutoff is the prescribed, honest outcome. The Reddit calibration runner's `cutoff_posture=None` is correct for a calibration tool — not a defect. The capture lane stays wrapped.
- **The cutoff is a property of the DECISION** (when it was made / what could fairly be known by then), not of the source — which is why authoring it belongs to the Decision-Frame owner, not the source-side derivers (the derivers only *read* it).

## Why this matters

This is the gate to a **cleared** real-case run end-to-end. ECR and the clearing path already work; the one missing piece for a real decision (e.g. the Canoo/Walmart case) is a Decision Frame supplying the cutoff. Same neighborhood as the cleaning-lane-vs-ECR sequencing question (already sent to the judgment lane) and the eventual real-case eval.

## Non-goals

- Not a capture-lane change (wrapped; no defect).
- Not an ECR source-side build (the source-side half is decided; derivers only read the cutoff).
- Not a JSG-01 readiness/unfreeze claim.
