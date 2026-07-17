# Forseti Code-Slop Taxonomy v0

```yaml
retrieval_header_version: 1
artifact_role: Decision record + reference model (code-slop taxonomy and catch-layer map)
scope: >
  The single reference for analysing code slop in the Forseti harness and hooks
  without reconstructing the authoring chat or invoking the slop-audit skill:
  the root cause, the seven observed slop forms, which defense layer catches
  each, and the deliberate decisions about what is gated, what is left to
  review, and what was dropped. Records the model that the landed duplication
  gate, the SCI kernel, and the cross-vendor review lane already embody; binds
  nothing new by itself.
use_when:
  - Analysing or triaging suspected code slop in forseti-harness/ or .agents/hooks/.
  - Deciding whether a slop class deserves a gate, review, or nothing.
  - Onboarding an agent or reviewer to what "smallest complete" means for code.
authority_boundary: retrieval_only
branch_or_commit: claude/code-slop-taxonomy-doc (base origin/main 65f113b3, authored 2026-07-18)
open_next:
  - AGENTS.md                                            # kernel: Smallest Complete Intervention (the tiebreaker; not restated here)
  - .agents/hooks/check_shared_helper_duplication.py     # the one mechanical gate + its coverage-boundary note
  - .agents/workflow-overlay/delegated-review-patch.md   # the review layer for judgment-class slop
  - docs/hygiene/hooks_smallest_complete_audit_ledger_v0.md   # toll-vs-defect ledger (enforcement-surface subtraction)
stale_if:
  - A new slop form is observed that no row in the taxonomy table covers.
  - The duplication gate's coverage boundary changes, or a mechanical gate is added/removed.
  - The AGENTS.md SCI kernel is amended in a way that changes the catch-layer decisions.
```

## What this is (and is not)

A reference model, not a new rule. Every decision below is already embodied in
landed machinery — the shared-helper duplication gate, the Smallest Complete
Intervention (SCI) kernel in `AGENTS.md`, and the cross-vendor delegated-review
lane. This record names the pattern in one place so future slop analysis does
not depend on tribal memory or on invoking the audit skill.

**Non-claim.** Registration in the doctrine index is discoverability, not a new
binding. `AGENTS.md` (SCI) and the gate remain the authority; on any conflict
they win and this record is the stale party.

## Root cause (why agents produce slop)

Cold agents do not write from doctrine; they **copy the nearest neighbour**, and
they are **additive by default** (making it work feels safe; deleting feels
risky). Observed evidence: after the copied-from exemplar files were fixed, 26
later agents adopted the shared home versus 4 who re-copied, and two cold-agent
probes reproduced the clean convention unprompted. Leverage therefore lives in
the *environment the agent copies from*, not in instructions it will not re-read
per edit.

## The defense layers (cheapest first; each catches what the last cannot)

| Layer | Catches | Cost |
| --- | --- | --- |
| 0. Clean exemplars + discoverable shared homes | most slop, before it is written | ~free |
| 1. Point-of-use signals (home docstrings "import me"; `# helper-delta:`; gate coverage note) | reuse-vs-copy; "this claim is load-bearing" | ~free |
| 2. Cheap mechanical gate (low false-positive classes only) | named-helper duplication | diff-scoped |
| 3. Review, ideally adversarial / cross-vendor | judgment classes: overclaims, oversizing, fail-silent-vs-safe | expensive |
| 4. SCI kernel (`AGENTS.md`) | the tiebreaker when the agent has a choice | ~free |

## The taxonomy (observed forms -> catch layer + decision)

| # | Slop form | Example hit | Caught by | Decision |
| --- | --- | --- | --- | --- |
| 1 | Duplicated **named** helper (shared home exists, copies never deleted) | `resolve_base_ref` / `parse_name_status` across ~14 hooks; projection readers | 0 + 2 | GATED (`check_shared_helper_duplication.py`); fix the **exemplar**, not every copy |
| 2 | Duplicated **inline block** / renamed / pre-fork copy | wave-6 Reddit-radar `canonical_old_reddit_thread_url` copies | 0 + 3 | NOT gate-able (a def-name backstop is structurally blind); coverage-boundary note + review |
| 3 | Oversized / multi-responsibility function | `_capture_video_cadence_rows` (434 lines) | 3 | REVIEW judgment — kept: one coherent state machine, proven behavior-identical across 57 tests |
| 4 | Overclaimed comment / docstring / status | "byte-identical" when divergent (W6-1); "unused" (CSB false-cut); "complete" decomposition | 3 + 4 | REVIEW + kernel "verify the durable target before claiming"; not gate-able (a claim is free to write) |
| 5 | Silent failure hiding (broad `except` that passes/defaults) | youtube JSON extractor swallowing `Exception` | 0 + 3 | narrow the genuine hides; NOT a gate (false-positives on every legit best-effort probe) |
| 6 | Magic-literal duplication | reddit domain strings (`old.reddit.com`) | — | DROPPED — probe showed all copies are tests, incidental, or already-justified `helper-delta` |
| 7 | Comment / pin accretion (notes stack, never collapse) | `POLICY_MODULE_PINS` stacked "Pin bumped" lines | 1 | COSMETIC — fold opportunistically on next real touch; no lane |

## The meta-rule

The anti-slop machinery must itself obey Smallest Complete Intervention. Every
gate is ceremony debt; every rule is a line someone carries. A layer earns its
place only against a real defect class whose recurring toll is worth paying —
which is exactly why duplication is gated but broad-`except` is not, magic-literal
was dropped, and comment-accretion is deferred. A long "anti-slop checklist"
would be the worst slop of all: nobody runs it, and it makes every edit heavier.

## The honest limit

No layer prevents judgment-class slop (overclaims, mis-sizing) at write time: an
agent confident it is "done" cannot audit its own confidence. That is the
permanent job of review, not a gap to close with more automation. The target is
not zero slop — it is: mechanical slop gated cheaply, judgment slop caught by a
reader, and neither the code nor the guardrails growing faster than they must.

## How to analyse code slop later (procedure)

1. Match the candidate to a form in the taxonomy table. If it is a **new** form,
   that is a `stale_if` trigger — add a row.
2. Route by catch layer: mechanical + low-false-positive -> consider a gate;
   judgment -> commission review; cosmetic -> defer.
3. Fix the **exemplar** (the nearest-neighbour source), not every copy — agents
   clone the neighbour.
4. Apply SCI: weigh subtraction equally with addition; name any ceremony debt a
   fix would install before adding it.
5. If a fix is behavior-bearing, prove behavior-preservation (tests are the
   proof) before landing.
