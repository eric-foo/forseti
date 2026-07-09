# Anti-Blocking HTTP Ladder — Daimler Rung-Resolution Closeout — Delegated Artifact Review: CA Adjudication v0

```yaml
retrieval_header_version: 1
artifact_role: Orca review-output (delegated review-and-patch adjudication record)
scope: >
  Home-model (CA) adjudication of the de-correlated delegated adversarial ARTIFACT
  review-and-patch pass on the Daimler anti-block-ladder rung-resolution closeout
  (the honesty/overclaim surface of a durable toolbox finding).
use_when:
  - Checking what the delegated artifact review found and what the CA kept.
authority_boundary: retrieval_only
open_next:
  - forseti/product/spines/capture/core/source_capture_toolbox/source_capture_anti_blocking_http_ladder_daimler_rung_resolution_closeout_v0.md
  - docs/prompts/reviews/source_capture_anti_blocking_http_ladder_daimler_closeout_delegated_adversarial_artifact_review_and_patch_prompt_v0.md
```

## Commission

- Prompt: `docs/prompts/reviews/source_capture_anti_blocking_http_ladder_daimler_closeout_delegated_adversarial_artifact_review_and_patch_prompt_v0.md`
  (sha256 `572168EF3C10D1E59F6D8F3BF2A1E2C5BF532E3B9D1A6D01377B845CF0FA74FB`).
- Target: the Daimler rung-resolution closeout (worktree `feat/anti-block-http-ladder` @ `3ca8090`, untracked).
- Lane: provisional delegated review-and-patch convention (`.agents/workflow-overlay/delegated-review-patch.md`), artifact lane. **Decision-input only** — not validation, not readiness, not a formal verdict.
- De-correlation: **satisfied** — delegate reported a different, non-Opus family; author/home is Claude, Opus-class. Who-constraint only.

## Delegate result (claims adjudicated, not inherited)

- Verdict: "patched diff recommended for CA adjudication." Not overclaiming badly, but "well-formed PDF container," "container validity," and set-level "beats the 403" left an avoidable fake-pass surface.
- Findings: **AR-01** (major — discriminator language could launder `2xx + application/pdf + %PDF-` into structural validity / content authenticity); **AR-02** (minor — "beats the 403 / all three DSUs" over-reads a DSU-001-only rung-0 control).
- The delegate also applied its edits to the working tree (the file arrived modified, not just diffed).

## CA adjudication: ACCEPT (one MODIFY); no reverts

**Adjudication meta-finding.** The couriered unified diff's `-`/context lines were **paraphrased, not byte-faithful** quotes of the artifact (expected for a no-repo-access delegate). The CA therefore adjudicated the **intent** of each change and verified against the **actual working-tree state** (which already carried the applied edits), rather than applying the diff literally. This is the de-correlation/adjudication seam doing its job.

- **AR-01 — ACCEPT.** "well-formed PDF container" / "container validity" → "container-level retrieval evidence"; added explicit "does **not** establish PDF structural validity beyond these discriminator checks"; decoy/challenge caveat retained; discriminator point 6 → "recorded body bytes are hash-honest as delivered." Safe-direction (under-claim + preserve + flag); the six-check discriminator is unchanged.
- **AR-02 — ACCEPT** (applied version exceeds the couriered intent): result heading → "sufficient rung, with DSU-001 lowest-rung control"; lead scopes "lowest demonstrated sufficient rung" to the DSU-001 control and calls 002/003 retrieval; table rung-0 cells for 002/003 → "not independently run; DSU-001 same-origin control only"; a **new dedicated same-origin non-claim bullet**; and "The wall" reworded to "consistent with request-profile/header sensitivity … not an isolated User-Agent-only change … for this run" — which directly closes the UA-vs-full-profile non-isolation the review focus raised.
- **use_when bullet — MODIFY.** The applied edit over-narrowed reusable toolbox guidance to the DSU-001 case. CA restored a reusable-but-honest framing: "Choosing an anti-block rung against a header/UA-keyed 403 wall like the observed Daimler/Akamai DSU-001 case (a full browser-like header profile sufficed there)."
- Receipt linkage + `downstream_consumers` — ACCEPT (hedged: "candidate next pass" / "needs a separate reconciliation decision" rather than "now unblocked / now true").

No hunk reverted. Every accepted change is safe-direction (tighten / hedge / under-claim); none removed a true finding — the core result survives, properly scoped: **rung-1 is the lowest *demonstrated* sufficient rung on the DSU-001 rung-0 control, and the rung that retrieved PDF-container candidates for all three DSUs.**

## Final state

- The closeout reflects the adjudicated content (delegate edits accepted + one CA modify). Worktree `feat/anti-block-http-ladder`; the closeout remains **untracked**; the committed arm `3ca8090` is untouched; `_test_runs/` scratch remains gitignored.

## Residuals (accepted; honest limits of the finding)

- Container-level retrieval evidence only — no PDF structural validity beyond the six checks, no content authenticity, no pre-cutoff version identity, no independent DSU-002/003 rung-0 blockage, no general rung-1 Akamai capability. These are now prominent in the closeout's Non-claims.

## Non-claims

- Not validation, readiness, acceptance, or a formal review verdict. Decision-input only.
- Does not certify any returned body as authentic source content.
- One live Akamai configuration/date; "rung-1 anti-block capability settled" is not claimed and would require cross-family review plus more targets/wall-classes.
