# Codex Tool-Stall Containment Delegated Code Review v0

```yaml
retrieval_header_version: 1
artifact_role: Review output
scope: Cross-vendor delegated code review-and-patch return for PR #996 tool-stall containment, plus home-model adjudication and replay boundary against main at 1d141a9c.
use_when:
  - Auditing why the packet-continuity and benign allow-path corrections were accepted.
  - Checking the evidence and residuals behind the tool-stall containment hardening patch.
authority_boundary: retrieval_only
reviewed_by: claude-fable-5
authored_by: unrecorded
de_correlation_bar: cross_vendor_discovery
review_use_boundary: >
  Findings are decision input only; they are not approval, validation,
  mandatory remediation, or executor-ready patch authority until separately accepted.
home_adjudication:
  adjudicated_by: OpenAI Codex / GPT-5
  status: completed
  accepted:
    - FND-1 packet continuity, adapted to the streamlined live circuit rule.
    - FND-2 benign allow-path coverage, adapted to the live protected-path test.
  retained_residual:
    - FND-3 future payload-schema drift remains an observed closure trigger, not a speculative patch.
  deferred:
    - FND-4 pre-existing flag-only surfaces are outside this correction.
  rejected:
    - FND-5 cosmetic cleanup closes no failure mode.
  replay_boundary: >
    The delegate validated its patch at 339fbda3. Main advanced to 1d141a9c and
    changed AGENTS.md plus the hook-wiring test before home replay, so current-branch
    validation governs landing; the delegate validation below is preserved as historical evidence.
```
Operator authorization received. I'll proceed with the defensible default I flagged: review at the current tip `339fbda3` (option 2), since the drift commit touches only overlay authority docs — none of the five writable targets, none of the flagged read-only targets — and the review target itself is the merged PR #996 diff, which is identical from either baseline. This keeps any patch landable on this branch without destructive git. Binding treated as amended: `required_revision: 339fbda3…`, clean tree re-verified this session.

Now executing the commission in order: load required authorities completely, then the two review methods, then the adversarial review.

Overlay README and source-loading read. Continuing with the remaining authorities — the commission binds full reads.

Authorities read. Now the `environment_baseline` constant from the preflight defaults template.

All required authorities are loaded. Source readiness reached — now applying the two required methods.

Diff captured. Now reading the adapter in full to attack `_check_apply_patch_paths` and its helpers.

Tree still clean at `339fbda3`. Receipt shape requirements confirmed. Now reading the exact edit regions before patching.

All edits applied. Running the commissioned validation sequence, focused first.

All validation is green and the receipt shape is confirmed. The commission is complete — findings, patch, and evidence follow.

---

# Delegated Code Review-and-Patch Return — PR #996 Codex Tool-Stall Containment

## 1. Actor / receiver receipt

```yaml
actor_model_family_receipt:
  author_home_model_family: OpenAI
  controller_model_family: Anthropic (claude-fable-5)
  current_receiving_actor_role: controller
  dispatch_mode: external-controller-courier
  de_correlation_status: VERIFIED_DIFFERENT (Anthropic vs OpenAI; direct repo access; not Codex-managed)
receiver_binding:
  receiver_class: external_direct_write (operator-provided checkout, Claude Code)
  binding_state: receiver_verified
  effective_target_worktree: .claude/worktrees/tiktok-zero-wheel-react-subs-3b0b3f
  observed_head: 339fbda31fb561eed6222a9bb3dc0d420f337a51
  revision_note: >
    Commissioned exact pin d037ed40 failed preflight (HEAD one merge ahead);
    BLOCKED_RECEIVER_REROOT_REQUIRED was returned and the operator authorized
    proceeding. Rebaselined to 339fbda3 (option 2): the drift commit touches only
    overlay authority docs, none of the writable or flag-only targets, and the
    review target diff (d037ed40^1..d037ed40) is identical from either baseline.
  tree_state_at_start: clean; no concurrent writer observed
```

Required authorities were read in full; `workflow-deep-thinking` and `workflow-code-review` were loaded after source readiness and applied (strict formal review; the commission supplied lane, packet, validation gates, and `paste-ready-chat` output binding).

## 2. Findings (severity-ordered)

**FND-1 — Circuit-state continuity fails across the repository's own preferred continuation route** (severity: major, confidence: high — **patched**).
[AGENTS.md:136-138](AGENTS.md:136) said an automatic continuation "does not reset an open circuit; if current context reports the stall, inherit it" — but nothing required the `sandboxed_tool_stall` record to travel in precompact or handoff packets, and [source-loading.md:576-584](.agents/workflow-overlay/source-loading.md:576) explicitly prefers a handoff packet plus fresh lane over `/compact`-and-continue at phase boundaries. A packet-booted lane whose packet omits the record silently reopens a route already observed stalled, defeating the commissioned done-bar ("stays quarantined across interruptions and continuations"). Closure: the record is now named packet content in the circuit rule (single-sourced at its owner); automatic-compaction loss is named as a bounded residual (one re-observed stall) rather than papered over.

**FND-2 — No allow-path coverage anywhere for `_check_apply_patch_paths`** (severity: minor, confidence: high — **patched**).
The #996 test asserts only denial ([test_ci_hook_wiring.py:186-208](forseti-harness/tests/unit/test_ci_hook_wiring.py:186)) and the adapter selftest's only apply_patch case is a protected-path denial ([forseti_guard_codex_adapter.py:282-307](.codex/hooks/forseti_guard_codex_adapter.py:282)). A regression that denies *every* apply_patch call — bricking the ordinary edit route — would pass the entire commissioned validation suite. Closure: benign same-root assertions across all three payload fields, which also exercises the previously untested `_run_guard` subprocess leg for the `patch` and `input` fields.

**FND-3 — Field enumeration plus silent non-string skip reproduces the original failure class** (severity: minor, confidence: medium — **documented residual, deliberately not patched**).
`_check_apply_patch_paths` skips any payload value that is not a non-empty string ([forseti_guard_codex_adapter.py:179-181](.codex/hooks/forseti_guard_codex_adapter.py:179)); the event then falls through to the portable guard, whose `decide()` ignores tool_name `apply_patch` entirely — allowed uninspected. That is the same class as the original wrong-root gap (patch text arriving in a field the adapter didn't inspect). Patching it (field-agnostic scanning of all string values, or fail-closed denial of uninspectable payloads) would be speculative hardening against an unobserved host schema and would change the adapter's documented fail-open-for-accidents posture — outside "confirmed defects." Minimum closure condition: observe the live host's apply_patch hook payload schema; adopt field-agnostic scanning only if a supported field is missed. Recorded in the incident log's residuals.

**FND-4 — Flag-only findings on read-only surfaces** (severity: minor, confidence: low–medium — no patch authority):
- [.codex/hooks.json:5](.codex/hooks.json:5) PreToolUse matcher omits `MultiEdit|NotebookEdit` although the adapter's `WRITE_TOOLS` handles them; if the host ever emits those names, direct-write nested-worktree checks never fire. Pre-existing, outside #996.
- `_registered_worktree_roots` returns `[]` on git probe failure/timeout ([adapter:104-120](.codex/hooks/forseti_guard_codex_adapter.py:104)), so the nested-worktree check silently passes on probe failure, while doctrine describes the registered-worktree denial as "fail-closed." Pre-existing accident-guard posture; changing it is a design decision.
- `_run_guard`'s `timeout=8` raises uncaught `TimeoutExpired` → adapter exits 1 with no denial JSON; host handling of that exit is unverified. Pre-existing.

**FND-5 — Cosmetic** (no action): `_check_apply_patch_paths` re-applies `_path_for_guard` to paths `_apply_patch_paths` already normalized — idempotent, pre-existing, no behavioral effect; a cleanup would close no finding.

**Positive verifications worth recording:** the fix is *not* dead code — the PreToolUse matcher includes `apply_patch` (this was attacked first); the stale-language sweep found no live turn-scoped circuit wording anywhere, confirming the #996 receipt's claim; dedup is safe-direction (exact post-normalization strings only; distinct spellings still checked); move/delete headers and multi-file patches are all captured; the new test exercises behavior via monkeypatched roots, not implementation wording.

## 3. Considered and defended (candidate → defense that held)

- Task/thread circuit is over-broad / goes stale (Q1) → alternate routes (escalated shell, atomic helper) are complete, so a stale-open circuit costs ~0 while a premature re-probe costs 80–265s; thread-bounded scope avoids durable standing state. Smallest complete boundary confirmed.
- "Tool plus permission route" imprecise (Q3) → the observed stall class spanned reads *and* patches on one substrate; distinct safe routes stay permitted, so no materially different safe operation is suppressed.
- "Use that working route for later shell calls" makes escalation standing (Q4) → per-operation harness approval remains the gate; the kernel's "never a standing rule" and the incident residual both restate it; wording pre-dates #996.
- New silent skip of non-string payloads weakens the old crash behavior → the old crash was an uncaught traceback with host-dependent effect, not designed fail-closed; not a confirmed regression (subsumed into FND-3).
- Relative patch paths anchor to hook ROOT, not a hypothetical workdir → deliberate "a command workdir cannot reroot this task" stance; no evidence apply_patch carries a workdir.
- #996's DCP receipt lists README/adapter only as downstream → the doctrine delta was the circuit rule; adapter/README are enforcement and documentation, not doctrine.
- Incident record blurs observation and inference (Q9) → observed/diagnosis/residuals/non-claims are correctly separated; "two focused hook-wiring tests passed" is a dated authoring-time observation.
- Unnecessary policy/mechanism added (Q10) → none found; the diff is tightly scoped to the incident.

## 4. Bounded working-tree diff

3 files changed, 68 insertions(+), 1 deletion(-) — all inside the commissioned writable set; `.agents/hooks/README.md` and the adapter needed no change.

```diff
diff --git a/AGENTS.md b/AGENTS.md
@@ -135,7 +135,9 @@
   be retried once through per-operation escalation; use that working route for
   later shell calls. A user interruption, follow-up message, or automatic
   continuation does not reset an open circuit; if current context reports the
-  stall, inherit it. After a stalled patch primitive, do not probe its launcher;
+  stall, inherit it. Carry an open circuit's `sandboxed_tool_stall` record in
+  any precompact or handoff packet so the receiving lane inherits it. After a
+  stalled patch primitive, do not probe its launcher;
```

Test file: adds the benign allow-path block (six-line benign patch, asserted `== ""` for each of `command`/`patch`/`input`) to `test_codex_apply_patch_guard_checks_all_payload_fields`. Incident log: appends "Delegated-review addendum — circuit-state continuity (2026-07-16)" with the two named residuals (compaction loss; payload-schema drift) and a shape-valid `direction_change_propagation` receipt (`trigger: workflow_authority`, controlling source AGENTS.md, stale-language search executed and recorded). The full diff was emitted verbatim in the validation step above.

## 5. Citations (neutral, per change)

- **AGENTS.md clause:** commission done-bar "stays quarantined across interruptions and continuations"; AGENTS.md:136-138 (context-conditioned inheritance); source-loading.md:576-584 (handoff-packet-over-compact preference); source-of-truth.md:32-46 (checkpoint packets carry lane state, point + re-confirm).
- **Test addition:** test_ci_hook_wiring.py:186-208 (deny-only assertions); adapter selftest lines 282-307 (deny-only apply_patch case); commission Q8.
- **Incident-log addendum:** source-of-truth.md Doctrine Change Propagation Contract (receipt required for doctrine-changing edits); review-lanes.md coverage-first doctrine (residuals named, not filtered).

## 6. Validation evidence (all run after the final edit)

| Command | Exit | Result |
|---|---|---|
| `python -m pytest -p no:cacheprovider forseti-harness/tests/unit/test_ci_hook_wiring.py -q` | 0 | 17 passed |
| `python .codex/hooks/forseti_guard_codex_adapter.py --selftest` | 0 | `CODEX ADAPTER SELFTEST OK` (embedded guard selftest OK, 67+5 cases) |
| `python -B .agents/tools/atomic_exact_edit.py --selftest` | 0 | `SELFTEST OK` (13 cases) |
| `git diff --check` | 0 | clean |
| `git diff --stat` / bounded `git diff` | 0 | 3 files, +68/−1, all in writable scope |
| Extra: `check_dcp_receipt.py --strict --base HEAD` | 0 | saw no files — diff-scoped over commits; uncommitted edits are invisible to it (reported, not claimed as coverage) |
| Extra: `check_dcp_receipt.py --check` (whole tree) | 0 | no findings on the touched files — new receipt is shape-valid |

Not run: full harness suite (not commissioned; the commission names the focused set).

## 7. Verdict

**`PATCHED_CONFIRMED_DEFECTS`**

Final characterization (Q12): **complete repository containment** — after this pass — with named residuals. PR #996 was correctly scoped containment, not an attempted host repair, and the incident record honestly separates the two. Its two real gaps were the packet-continuity hole (FND-1) and the untested allow path (FND-2), both now closed within the commissioned file set.

## 8. Residual risks / outside repository control

- The host `apply_patch` executor may still stall; only rerouting is repository-controllable.
- Automatic compaction that drops the stall record silently closes the circuit; bounded cost is one re-observed stall (now a named residual).
- A Codex payload-schema change could reopen the uninspected-field gap (FND-3 closure condition recorded).
- Hook-exit semantics for adapter crashes/timeouts are host-owned and unverified.
- Flag-only items in FND-4 remain open on read-only surfaces.

**Adjudicator notes (hard stop honored — nothing staged, committed, or pushed):** the landing change touches the `forseti-harness/` code root, so the landing commit needs a `review_routing_status` line or filed review artifact per the review-routing gate — this return is the commissioned review. Close per `communication-style.md` → Review Adjudication Next Step: adjudicate these findings/diff/verdict as claims, then batch the land step.

```yaml
DELEGATED_CODE_REVIEW_RETURN_FOR_HOME_MODEL:
  commission: PR #996 Codex tool-stall containment adversarial review-and-patch
  reviewed_by: claude-fable-5 (Anthropic)
  authored_by: OpenAI (per commission receipt)
  verdict: PATCHED_CONFIRMED_DEFECTS
  findings: [FND-1 patched, FND-2 patched, FND-3 documented-residual, FND-4 flag-only, FND-5 no-action]
  diff: 3 files, +68/-1 (AGENTS.md, test_ci_hook_wiring.py, technical_difficulties_log_v0.md)
  validation: focused pytest 17 passed; adapter selftest OK; atomic-edit selftest OK; git diff --check clean
  characterization: complete_repository_containment_with_named_residuals
  next: CA adjudication -> keep/veto -> single land step with review_routing_status
```