# Cross-Family Adversarial Re-Review (Patch Recheck) — STEP-03 Credential Store

```yaml
artifact_role: Cross-family adversarial patch-recheck prompt (bounded rerun)
review_lane: independent adversarial re-check (DIFFERENT model family from the author, which is Claude; read-only; reviewer does NOT patch)
prior_review: the first cross-family pass returned blocking-issues (4 findings). This recheck verifies the patches and scans only the touched scope.
decisive_criterion: are the 4 prior findings closed, and did the patches introduce any NEW blocker/major issue in the touched scope?
load_rule: confirm-don't-trust — read the named files at their current state before any firm claim.
authority_boundary: independent signal for owner adjudication only — not a completion gate that clears itself.
workspace: C:\Users\vmon7\Desktop\projects\orca
expected_branch: main
dirty_state: STEP-03 is uncommitted working-tree edits plus untracked files; read it in place; do not switch or create worktrees.
output: return findings in chat to the owner; write no files.
scope: BOUNDED. Verify the 4 findings below are closed, then scan ONLY the touched files for patch-caused or newly-visible blocker/major issues. Do NOT re-litigate the architecture or re-review untouched, previously-clean areas. Minor/nit findings outside the patched scope are out of scope.
```

## Frozen (do not re-open unless you find a NEW blocker)

- The shared-core architecture (`local_secret_store.py` + the `auth_state.py` and `reddit_credentials.py` specializations) is accepted for this recheck.
- Areas not touched by these patches are out of scope.

## The 4 prior findings — verify each is CLOSED

1. **(was blocking) `client_id` reached `__repr__`/`str()`.** `RedditCredentials.__repr__` must now redact **both** `client_id` and `client_secret`; `repr()`, `str()`, and f-string interpolation must leak neither value. Confirm in `orca-harness/source_capture/reddit_credentials.py` and `orca-harness/tests/unit/test_source_capture_reddit_credentials.py::test_reddit_credentials_repr_redacts_both_values`. Try to make a secret surface anyway.
2. **(was major) lax credential-file shape.** `_validate_credential_shape` must reject unexpected keys (`refresh_token`, `password`, user-context tokens) — accepting exactly `client_id` + `client_secret`. Confirm in `reddit_credentials.py` and `::test_validate_rejects_unexpected_keys`. Probe for a bypass (case, nesting, type confusion, the load path vs the bootstrap path).
3. **(was major) symlinked store root.** `assert_under_root` must reject a store root that is itself a symlink. Confirm in `orca-harness/source_capture/local_secret_store.py` and `orca-harness/tests/unit/test_local_secret_store.py::test_assert_under_root_rejects_symlinked_root`. **The test skips where the host cannot create symlinks — judge the code guard by reading it, not by the test running.** State whether covering only the final root component (intended; symlinked ancestors like a macOS `/tmp` are deliberately allowed) leaves any residual gap you consider blocking.
4. **(was minor) behavior-preservation claim.** The reserved-sidecar-suffix label rejection is now framed as **intentional** security hardening (pinned by `::test_label_to_filename_rejects_reserved_sidecar_suffix`), not pure behavior-preservation. Confirm the framing is consistent and the browser-lane tests still pass (`tests/unit/test_source_capture_authenticated_browser_snapshot.py`).

## Touched scope to scan for NEW blocker/major issues

- `orca-harness/source_capture/reddit_credentials.py` (the `__repr__`; `_validate_credential_shape`)
- `orca-harness/source_capture/local_secret_store.py` (`assert_under_root`)
- `orca-harness/tests/unit/test_source_capture_reddit_credentials.py`, `orca-harness/tests/unit/test_local_secret_store.py`

Ask: did any patch introduce a regression, a new leak, a confinement gap, or a false-passing/circular test? Did rejecting extra keys break any legitimate credential-file flow? Is the symlink guard sound and complete enough for a credential store?

## Output (return in chat to the owner)

- **VERDICT:** `closed-clean` | `closed-with-new-minor` | `not-closed-or-new-blocking`.
- For **each** of the 4 findings: `CLOSED` or `NOT-CLOSED`, with `file:line` evidence.
- Any **NEW** blocker/major issue in the touched scope: `file:line`, severity, real-vs-theoretical, one-line fix.
- Anything you could not verify (e.g. symlink behavior on the host) and why.

Keep it concrete and source-grounded. Authority boundary: your output is an independent signal for the owner, not an authorization or a completion gate.
