# Cross-Family Adversarial Code Review — STEP-03 Reddit Credential Store + Shared Credential Core

```yaml
artifact_role: Cross-family adversarial code-review prompt
review_lane: independent adversarial check (DIFFERENT model family from the author, which is Claude; read-only; reviewer does NOT patch)
decisive_criterion: security correctness + behavior-preservation of the refactor
load_rule: confirm-don't-trust — read every named file before any firm claim; name anything you could not verify.
authority_boundary: independent signal for owner adjudication only — not a verdict that authorizes, validates, merges, or unblocks anything on its own.
workspace: C:\Users\vmon7\Desktop\projects\orca
expected_branch: main
dirty_state: the STEP-03 changeset is UNCOMMITTED working-tree edits plus new untracked files; that is the review target. Read it in place; do not switch or create worktrees.
output: return findings in chat (transcript) to the owner; write no files.
```

## Your job

You are an **independent reviewer from a different model family than the author** (the author is Claude). Your value is catching what a same-family reviewer would share a blind spot on. **A same-family review already ran; you are NOT given its findings — attack the code fresh and unanchored.** Be **adversarial**: your task is to *refute* the claim that this credential-store changeset is correct and safe. Default to skeptical. This is security-sensitive code (it handles API secrets) — hunt hard. If you cannot access a file, say so and mark which claims you could not verify.

## Background (enough to review; verify against the files)

A source-capture harness added a **local, ignored, label-indirected Reddit API credential store** as a "token variant" of an existing browser storage-state store. To avoid duplicating security-critical mechanics, the shared parts were **extracted into a new `local_secret_store.py` core** (directory confinement, label→filename sanitization, size-capped JSON read, `.meta.json` sidecar read/write), and the existing browser store (`auth_state.py`) was **refactored to build on that core**. A new `reddit_credentials.py` is a second specialization. Secrets are meant to live only in the ignored store and an in-memory credentials object; packets/sidecars record only a label + a mode.

## Files to read (read each fully)

- `orca-harness/source_capture/local_secret_store.py` — NEW shared security core.
- `orca-harness/source_capture/auth_state.py` — refactored onto the core.
- `orca-harness/source_capture/reddit_credentials.py` — NEW Reddit store (`RedditCredentialMode`, `RedditCredentials` with a custom `__repr__`, `load_reddit_credentials`).
- `orca-harness/runners/run_source_capture_reddit_credential_bootstrap.py` — NEW registration runner.
- `orca-harness/tests/unit/test_local_secret_store.py`, `orca-harness/tests/unit/test_source_capture_reddit_credentials.py` — NEW tests (judge whether they actually prove anything).
- `orca-harness/source_capture/__init__.py` — exports `RedditCredentialMode`.
- `.gitignore` — should ignore `orca-harness/_reddit_credentials/`.
- **Behavior spec to diff the refactor against:** `orca-harness/tests/unit/test_source_capture_authenticated_browser_snapshot.py` — the existing browser tests the refactor must not break. (If useful, diff `auth_state.py` against its committed/`HEAD` version.)

## Hard invariants — try to BREAK each

1. **Secrets never escape.** `client_id` / `client_secret` must never reach a Source Capture Packet, a log, an error message, a `__repr__`/`str()`, a traceback, or the metadata sidecar. The sidecar may contain only `{credential_file, credential_mode}`. Find any path that leaks a secret value.
2. **Directory confinement.** No label, suffix, or sidecar path may resolve **outside** the store root. Path traversal and separators must be rejected. Attack the label rules, the `.meta.json` sidecar derivation, the reserved-suffix guard, and `resolve()`/`relative_to()` against `..` and symlinks.
3. **No secret CLI flags.** The registration runner must expose no `--client-id`/`--client-secret`/`--token`/`--password`/etc., and no secret-named arg destinations.
4. **Behavior-preserving refactor.** The `auth_state.py` refactor must preserve ALL prior behavior — including behavior the browser tests do NOT pin (exact error-message strings, the order of existence/size/shape checks, the sidecar key names and file format). Diff it and name any divergence, pinned or unpinned.
5. **Network-free / offline.** The store modules must be stdlib-only (no `requests`/`httpx`/`praw`/`socket`/network I/O). Confirm there is no hidden transport.

## Attack surfaces (probe these and anything else)

- **Confinement & naming:** does `label_to_filename` anchor its regex, reject separators, and reject every filename that could collide with a sidecar? Does the `with_suffix`-based sidecar derivation ever produce a path that shadows another label's file or escapes root? Is `resolve()`-then-`relative_to()` sound if the store directory itself is a symlink?
- **Secret-leakage trace:** enumerate every site a secret could be rendered — the credentials `__repr__` (does `@dataclass(..., repr=False)` actually suppress the generated repr so the custom one wins? does `str()`/f-string/`!r` leak it?), exception messages, the sidecar payload, the bootstrap success/failure output, and any place the parsed payload dict is logged or echoed.
- **`load_*` correctness / TOCTOU:** does the load path validate file shape AND sidecar existence AND file-binding AND mode before returning secrets? Is there any ordering where it returns secrets despite a mismatch?
- **Refactor regression:** for each refactored `auth_state` function, compare against the browser test expectations and the un-pinned edges; flag any changed message, dropped check, or reordered validation.
- **Test quality:** are the new tests circular, shallow, or self-fulfilling? What real case is NOT covered (e.g., size-cap branch, non-dict payload, symlinked root, blank/whitespace secret, the file-binding-mismatch path)?
- **Cross-store consistency:** any way the two specializations diverge that creates a latent bug or a security gap in one but not the other.

## Output (return in chat to the owner)

- **VERDICT:** `clean` | `minor-issues` | `blocking-issues`.
- **FINDINGS:** numbered. For each: `file:line`, severity (`blocking`/`major`/`minor`/`nit`), the concrete problem, whether it is a **real** exploitable/observable issue or theoretical, and a one-line suggested fix.
- **BEHAVIOR-PRESERVATION:** an explicit statement on whether the `auth_state.py` refactor preserves all browser-test-pinned AND unpinned behavior, naming any divergence.
- **STRONGEST SINGLE CONCERN:** the one thing most worth fixing, or "none".
- **UNVERIFIABLE:** anything you could not confirm against source (e.g., symlink behavior on the host), and why.

Keep findings concrete and source-grounded; cite line numbers you actually read. Remember the authority boundary: your output is an independent signal for the owner, not an authorization or a completion gate.
