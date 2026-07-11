# Hooks `_hooklib` Refactor Delegated Adversarial Code Review v0

```yaml
retrieval_header_version: 1
artifact_role: Delegated code review output
scope: Cross-vendor repo-mode review-and-patch of the bounded hooks `_hooklib` refactor.
use_when:
  - Adjudicating the uncommitted hooks-refactor delegated patch.
  - Reviewing behavior-preservation, throttle, import, scope, and wiring evidence.
authority_boundary: retrieval_only
reviewed_by: OpenAI GPT-5
authored_by: Anthropic Claude (Fable 5)
de_correlation_bar: cross_vendor_discovery
review_use_boundary: Findings are decision input and not approval, validation, mandatory remediation, or patch authority.
```

## Commission receipt

- target kind / access / mode: `delegated_code_review_and_patch` / `repo` / `base-subagent`
- actor receipt: Anthropic Claude (Fable 5) author/home; OpenAI GPT-5 controller; cross-vendor de-correlation satisfied
- receiving role / dispatch: controller / external-controller-courier
- patch scope: the nine named hook/README files only; off-scope remained read-only
- doctrine change: none

The owner overrode the initial checkout mismatch. Work ran only in the named isolated clean worktree. Its observed head was `cea141474df77da4cba8d5e8c49d2cf09a2f6188`, containing `47d3beb0` and `876c068f`.

## Verdict and sub-verdicts

Overall: `PATCHED_WITH_MINOR_FINDINGS` — decision input only, not formal PASS, approval, readiness, or validation. No design-level defect triggered `NEEDS_ARCHITECTURE_PASS`.

- `[hooklib]`, `[retrieval-header]`, `[full-gt]`, `[prompt-preflight]`, `[repo-map]`, `[google-route]`, `[shared-dirty]`: no patch recommended; named residuals remain below.
- `[sci]`: patched incomplete verbatim authority mirror and added fail-capability.
- `[readme]`: patched incomplete Claude verification list.

## Findings

### FIND-01 — `[sci]` verbatim SCI reminder omitted the anti-over-slicing paragraph

- severity / confidence: minor / high
- location: `.agents/hooks/remind_sci.py:74`; owner `AGENTS.md:11`
- evidence: before patch, exact comparison returned `False` and listed seven missing lines beginning at `AGENTS.md:18`; the hook claimed a verbatim mirror. The patched lines begin at `.agents/hooks/remind_sci.py:78` and the drift check is at line 217.
- impact: durable-artifact commits received an incomplete advisory rule, omitting the explicit rejection of thin plumbing slices.
- minimum_closure_condition: embedded SCI text equals the owning section and future drift makes the selftest nonzero.
- next_authorized_action: Chief Architect adjudicates the `[sci]` hunk.
- verification: red probe `False`; post-patch probe `True`; `remind_sci.py --selftest` exit 0.

### FIND-02 — `[readme]` Claude verification omitted its wired SessionStart hook

- severity / confidence: minor / high
- location: `.agents/hooks/README.md:43`, `.agents/hooks/README.md:92`, `.claude/settings.json:96`
- evidence: table, wiring prose, and settings register `session_context_capsule.py`; the pre-patch Claude verify block omitted its available selftest. The added command is `.agents/hooks/README.md:127`.
- impact: the documented verification path could miss a broken wired SessionStart script.
- minimum_closure_condition: the Claude verify block exercises every documented wired script that exposes `--selftest`.
- next_authorized_action: Chief Architect adjudicates the `[readme]` hunk.
- verification: the added command exited 0.

## Unified uncommitted patch

Each diff is preceded by its commissioned label. Zero context avoids whitespace-only context lines.

```diff
# [readme]
diff --git a/.agents/hooks/README.md b/.agents/hooks/README.md
index 4afcd86d..c80ba2bc 100644
--- a/.agents/hooks/README.md
+++ b/.agents/hooks/README.md
@@ -126,0 +127 @@ python .agents/hooks/check_token_burn.py --selftest
+python .agents/hooks/session_context_capsule.py --selftest
# [sci]
diff --git a/.agents/hooks/remind_sci.py b/.agents/hooks/remind_sci.py
index 2381451c..0a1f003b 100644
--- a/.agents/hooks/remind_sci.py
+++ b/.agents/hooks/remind_sci.py
@@ -77,0 +78,8 @@ coherent, non-fragile completion.
+Prefer the biggest COMPLETE move you can still fully verify and the owner
+can still steer in one pass -- not a thin smoke-test slice that proves
+plumbing and defers the real capability. Over-slicing is its own
+compounding cost: the deferrals pile up and rot, and each slice burns a
+full plan/review/steer cycle. Slice deliberately only when the move is
+high-lock-in or irreversible (probe first) or you genuinely need real
+output to design the rest (harvest before cook) -- never just to look safe.
+
@@ -194,0 +203,16 @@ def selftest() -> int:
+    # The reminder promises a verbatim mirror of the owning SCI section. Keep
+    # that promise mechanically fail-capable when AGENTS.md changes again.
+    try:
+        agents_text = (root / "AGENTS.md").read_text(encoding="utf-8")
+        sci_source = (
+            agents_text.split("## Smallest Complete Intervention", 1)[1]
+            .split("### Problem Integrity", 1)[0]
+            .strip()
+        )
+        mirror_ok = _SCI_VERBATIM.strip() == sci_source
+    except (OSError, IndexError):
+        mirror_ok = False
+    if not mirror_ok:
+        ok = False
+    print(("PASS" if mirror_ok else "FAIL") + "  sci-verbatim mirror")
+
```

## Explicit non-findings

- Rooted `/docs/...` normalization is silence-preserving: old retrieval/SCI returned out-of-scope text, old repo-map produced no area trigger, full-GT already returned `None`; shared `to_relposix` remains silent.
- Repo-map’s shared parser adds `path`/`notebook_path`/`input`, but actual Claude and Codex matchers introduce no newly relevant event key. Google already used the full superset.
- Repo-map’s pre-gate at `.agents/hooks/check_repo_map_freshness.py:413` skips only default exclusions that old `structural_trigger` also skipped; map interrupt remains first and map-derived exclusions still apply.
- Import failure cannot synthesize exit 2. The hard guard remains import-free. No hook filename collides with `sys.stdlib_module_names`.
- `header_index.py` and `check_review_output_provenance.py` imported from an external cwd; retrieval re-exports remained available.
- Scope sets gained/lost nothing: retrieval equals the shared base; SCI retains its explicit `forseti/product/` addition; Google retains its documented delta.
- Full-GT monkeypatches the imported `_git` alias used by production. Migrated selftests exercise imported helpers, with live probes covering throttle/pre-gate paths.
- Settings parsed and README matcher prose agreed with actual wiring.

## Considered and defended

- `[hooklib]` SHA1-16 collision: theoretical 64-bit collision, retained as residual rather than material finding.
- `[prompt-preflight]` temp cleanup: deletion returns the next write to full, increasing tokens rather than causing silence.
- `[prompt-preflight]` missing session: live production probe emitted full and never used `nosession` throttling.
- `[repo-map]` widened keys: repository-visible matchers defeat the behavior-drift candidate.
- `[guard]` duplication: the standalone exception reduces hard-gate blast radius.

## Validation evidence

Post-patch exits were 0 for `_hooklib`, guard, retrieval, placement, full-GT, prompt-preflight, repo-map, Google-route, shared-dirty, token-burn, SCI, pre-push, review-output provenance, header-index, and session-capsule selftests. Focused pytest exited 0 with 45 tests. Settings JSON parse exited 0.

Live probes observed: full then short for one session; full with missing session; marker deleted; new top-level area advisory; `.claude/settings.json` silent with a raising map-read probe; both consumers imported from another cwd; exact SCI comparison `True`. `git diff --check` exited 0 before report creation.

## Residual risk

- Advisory hooks fail open by design. A shared import regression can degrade migrated advisories to silence rather than blocking; silence is the failure mode to bound.
- Throttling trades repeat-nudge coverage for tokens. If `/clear` reuses the same `session_id`, a short pointer may outlive visible context; repository evidence did not establish id rotation. Temp cleanup fails open to full.
- The 64-bit marker key has theoretical collision/corrupt-marker suppression risk; no observed evidence justified storing more persistent identity data.
- The approximately 7 ms import cost was measured on one machine only.

## Boundaries

No off-scope design defect or architecture-pass need was found. No off-scope file was patched. This report does not approve the branch, establish readiness, validate semantic correctness, mandate remediation, authorize extra patching, or decide what is kept.

## Review Adjudication Next Step

The Chief Architect should adjudicate both findings, both labeled hunks, the verdict, and residuals as claims. Close accept/modify/reject decisions inside the commissioned scope in the same turn and re-check. Route only a genuinely non-self-closable material issue. If clean enough to land, batch commit/push/PR administration into one land step. Then name 1–5 substantive next moves only when a visible active goal exists; otherwise record `no_visible_active_goal`.

DELEGATED_CODE_REVIEW_RETURN_FOR_HOME_MODEL

Adjudicate this report under the delegated-review-patch return contract. The working-tree diff is uncommitted and is decision input only.
