# Desktop Sandbox Task-Local Circuit Delegated Review v0

```yaml
retrieval_header_version: 1
artifact_role: Review output
scope: Cross-vendor delegated adversarial review-and-patch of the Forseti task-local Desktop sandbox-stall circuit wording, plus home-model adjudication.
use_when:
  - Auditing why route freshness was separated from the small-worktree performance shape.
  - Checking the accepted residuals and landing evidence for the Desktop sandbox mitigation.
authority_boundary: retrieval_only
reviewed_by: claude-fable-5
authored_by: OpenAI GPT-5 Codex
de_correlation_bar: cross_vendor_discovery
review_use_boundary: >
  Findings are decision input only; they are not approval, validation,
  mandatory remediation, or executor-ready patch authority until separately accepted.
home_adjudication:
  adjudicated_by: OpenAI Codex / GPT-5
  status: completed
  accepted:
    - AR-01 route freshness was incorrectly entangled with the small-worktree launch shape; the delegate patch was kept unchanged.
  retained_residual:
    - AR-02 compaction that loses in-task stall context can cost one re-observed stall; no cross-context carriage obligation was restored.
  confirmed_intent:
    - AR-03 removal of the explicit alternate-mutation cap is intentional simplification; route retry limits, inspect-once, and stop conditions remain.
  deferred:
    - Live-unreferenced atomic helper cleanup and historical-log tense are outside this work unit.
```

## Commission and receiver

The operator commissioned a bounded review of the Operating Economy sandbox-stall bullet in `AGENTS.md` at worktree `C:\tmp\forseti-desktop-sandbox-mitigation`, authored revision `cbd0b7ee4eeac22625d1eb3fa69cb52fcc165f28`. Claude Fable 5 reported direct repository access, a clean intake tree, cross-vendor de-correlation, and no lifecycle action.

## Findings and adjudication

### AR-01 - accepted and closed

The original wording made a separate-small-worktree launch appear to be a condition for a fresh task to receive a fresh sandbox route. That contradicted `.agents/workflow-overlay/decision-routing.md`, where the worktree shape is performance containment rather than correctness or authority. The accepted patch states that every fresh task receives a new route, even when carried context mentions an earlier stall, and points the performance guidance back to its owning overlay.

```diff
-  stalls. A fresh task launched directly in a separate small worktree is a new
-  sandbox route and does not inherit the prior task's circuit. Verify the final
-  diff. Completion through an alternate route is mitigation, not proof that the
-  ordinary tool route is repaired.
+  stalls. A fresh task is a new sandbox route and does not inherit a prior
+  task's circuit, even when carried context reports the earlier stall; the
+  separate-small-worktree launch shape is performance containment owned by
+  `.agents/workflow-overlay/decision-routing.md`, not a route-freshness
+  condition. Verify the final diff. Completion through an alternate route is
+  mitigation, not proof that the ordinary tool route is repaired.
```

### AR-02 - residual accepted

The live rule does not define compaction as a durable circuit boundary. If compaction loses the current task's stall state, the bounded consequence is one repeated stall before the circuit reopens. Reintroducing packet or cross-task carriage would recreate the ceremony this correction removes, so no patch was accepted.

### AR-03 - intent confirmed

The compact rule no longer states a separate one-alternate-mutation cap. This is intentional: one retry through a distinct route, inspect-once after an uncertain mutation, final-diff verification, and explicit hard-stop conditions retain failure visibility without duplicating limits.

## Off-scope flags

The delegate noted that `.agents/tools/atomic_exact_edit.py` is now referenced mainly by historical artifacts, and that an older append-only incident entry describes superseded behavior in present tense. Neither observation changes the bound outcome, so neither was patched.

## Evidence

The delegate reported `git diff --check` clean, strict DCP receipt validation clean, the Codex guard adapter selftest passing, the focused hook-wiring suite at 17 passed, and zero matches in the commissioned stale-language sweep. Home adjudication freshly confirmed that the delegate changed only `AGENTS.md` and that its exact patch matched the accepted finding.

## Closure

One net-new material finding was accepted and closed. Two minor advisories were resolved by explicit residual acceptance and intent confirmation. The repository change remains containment for a Codex Desktop sandbox-route defect; it does not claim to repair the Desktop executor.
