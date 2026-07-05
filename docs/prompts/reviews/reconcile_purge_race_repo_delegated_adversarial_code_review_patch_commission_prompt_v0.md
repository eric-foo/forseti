# Repo-Mode Delegated Adversarial Code Review + Patch Commission — Reconcile Purge Race (v0)

```yaml
retrieval_header_version: 1
artifact_role: Review prompt artifact (delegated code review-and-patch commission, repo access mode)
scope: >
  Paste-ready repo-mode commission for the de-correlated cross-vendor
  adversarial CODE review AND bounded patch of the reconcile purge-phase
  hardening: data_lake/consumption.py's shared
  reconcile_availability_per_packet gains per-packet isolation in its
  delete/purge half (concurrently-removed entry = benign; undeletable entry =
  visible per-packet failure), plus two behavioral race tests. The special
  stake is SEAM-CONTRACT SOUNDNESS on the single-sourced helper every
  catch-up runner consumes: can the new tolerance ever let a no-work claim
  pass over an unreconciled surface, or hide a stale availability entry?
use_when:
  - Dispatching the commissioned reconcile-purge review to a repo-access-capable, non-Anthropic reviewer.
  - Re-dispatching unchanged (verify the pinned commit and hashes first).
authority_boundary: retrieval_only
```

## Pinned fields

- Repository: `https://github.com/eric-foo/orca`, branch
  `claude/reconcile-race-hardening` (lane head), pinned commit
  `5aaa3a1944bcafafc5dff680fe972b49b9ce62c2`.
- Review target (the explicitly named multi-file set; the ONLY patchable
  surface; LF git blob bytes at the pinned commit):
  - `[seam-helper]` `orca-harness/data_lake/consumption.py` — SHA256 `fb62e39364715e7b6f5b797934ebe1e83c8e0f96def29dcefd94ee9525775e95`
  - `[seam-tests]` `orca-harness/tests/test_data_lake_consumption.py` — SHA256 `db696f88ac1ad336e23c266c511760fd86119c694eb25887c8adea2814541b2d`
- Read-only / flag-only everywhere else — notably `data_lake/root.py`
  (`record_availability`, `rebuild_availability`, `read_availability`,
  `list_available` — the index's producer/consumer semantics), the seven
  catch-up runners and `runners/run_seam_cadence.py` (every consumer of this
  helper), the seam contract
  `orca/product/spines/data_lake/authority/core_spine_v0_data_lake_consumption_seam_contract_v0.md`,
  and the prior adjudications (F-ECR-001, F-CAD-001 under
  `docs/review-outputs/adversarial-artifact-reviews/`).
- Access mode: `repo` — inspect the pinned source in place.
- Patch authorship: the delegate AUTHORS the bounded patch and returns it as a
  unified diff in chat; no commits, pushes, or writes outside the named set.
- Named validation obligation:
  `python -m pytest orca-harness/tests/test_data_lake_consumption.py
  orca-harness/tests/contract/test_catchup_runner_seam_coverage.py
  orca-harness/tests/unit/test_ecr_catchup.py
  orca-harness/tests/unit/test_seam_cadence.py`
  (with `ORCA_DATA_ROOT` unset). Run if your runtime can; report real results
  either way — never assert a pass that was not run.
- Output mode: `paste-ready-chat` (body below). Durable report written by the
  home CA at ingestion to
  `docs/review-outputs/adversarial-artifact-reviews/reconcile_purge_race_delegated_adversarial_code_review_v0.md`.
- Workflow sequence (overlay-owned): repo-mode code-diff loop per
  `.agents/workflow-overlay/delegated-review-patch.md` ("Code-diff target
  kind"); home-CA adjudicates before anything is kept.

```text
forseti_start_preflight:
  agents_read: yes
  overlay_read: yes
  source_pack: custom (delegated-review-patch Code-diff section + the in-repo
    repo-mode commission pattern; targets pinned in-repo)
  edit_permission: docs-write (this prompt artifact only)
  target_scope: docs/prompts/reviews/reconcile_purge_race_repo_delegated_adversarial_code_review_patch_commission_prompt_v0.md
  dirty_state_checked: yes (lane claude/reconcile-race-hardening; implementation committed at 5aaa3a19)
  blocked_if_missing: none
repo_map_decision: not_needed
repo_map_reason: destination bound directly by the artifact-folders overlay file and the in-repo commission pattern.
```

## Paste-ready commission body

````markdown
You are the de-correlated external controller for a REPO-MODE DELEGATED
ADVERSARIAL CODE REVIEW AND BOUNDED PATCH commissioned by another lane.

WHO-CONSTRAINT — gate yourself first: the review target was authored by an
Anthropic (Claude-family) model. This commission requires a DIFFERENT vendor /
model lineage (vendor = upstream model developer, not host/reseller/wrapper).
If you are Anthropic/Claude-lineage, or your lineage is unknown or
undisclosable, reply ONLY `BLOCKED_DECORRELATION` and stop. Who-constraint
only, never a model recommendation. State your model identity if permitted.

REPOSITORY ACCESS — read the pinned repository directly:
- repo: https://github.com/eric-foo/orca
- branch: claude/reconcile-race-hardening, pinned commit 5aaa3a1944bcafafc5dff680fe972b49b9ce62c2
- REVIEW TARGET (review AND may patch — nothing else; label every finding):
  1. [seam-helper] orca-harness/data_lake/consumption.py
     (SHA256 fb62e39364715e7b6f5b797934ebe1e83c8e0f96def29dcefd94ee9525775e95)
  2. [seam-tests] orca-harness/tests/test_data_lake_consumption.py
     (SHA256 db696f88ac1ad336e23c266c511760fd86119c694eb25887c8adea2814541b2d)
If you cannot open the repository, reply ONLY `BLOCKED_REPO_UNREADABLE`. If
you cannot see the pinned commit, review the branch head and state the commit
you actually read.

WHAT THE CHANGE IS: reconcile_availability_per_packet is the seam's shared
per-packet availability reconcile (F-ECR-001 shape) consumed by all seven
catch-up runners and the seam cadence. Its rebuild half was already
per-packet loud, but its purge half (delete all indexes/availability/*.json,
then regenerate from committed raw) had NO isolation: a live cadence run
concurrent with the capture fleet crashed every entrypoint with
FileNotFoundError/PermissionError from the unlink loop (observed 2026-07-04,
recorded in docs/decisions/bronze_consumer_census_closure_record_v0.md).
The patch: FileNotFoundError on unlink = benign continue (a concurrent
writer already removed/replaced it — absent IS the purged state); any other
OSError = a visible per-packet availability_reconcile_failed entry (packet
id = file stem) instead of a whole-batch crash. Two tests pin the two race
cases via monkeypatched Path.unlink.

The failure modes that matter most:
- NO-WORK-CLAIM SOUNDNESS (the stake): the seam contract makes an empty
  pickup a valid no-work claim only over a fully reconciled surface. Attack
  the FileNotFoundError-continue: is there ANY interleaving where treating a
  vanished entry as benign leaves a STALE entry alive (e.g. the concurrent
  writer re-created the file with stale content AFTER our unlink raced) that
  the rebuild then fails to overwrite — letting list_available serve a
  packet state the purge never cleaned? Check record_availability's write
  pattern in data_lake/root.py (read-only) for overwrite semantics.
- FAILURE-ENTRY FIDELITY: packet_id from entry_file.stem — can an
  availability filename ever NOT be the packet id? Can a locked entry
  produce a DOUBLE failure entry (purge + rebuild) and does any caller
  misbehave on duplicates?
- EXCEPTION LATTICE: is `except OSError` the right breadth (WinError 5/433
  observed) — and is anything now swallowed that should crash (e.g. a
  programming error raising OSError-subclass from inside record-keeping)?
- TEST ADEQUACY: the monkeypatched unlink tests — do they actually exercise
  the shipped code paths (would the tests survive a mutant that re-raises
  in the FileNotFoundError arm)? Windows/POSIX portability of the
  monkeypatch approach?
- CONSUMER BLAST RADIUS: all seven runners + the cadence treat returned
  entries as loud failures — confirm none of them interprets an
  availability_reconcile_failed entry as completed work or acks on it.

TASK: (1) structured reasoning pass over the purge/rebuild/writer
interleavings; (2) maximally adversarial review of the named set; (3)
bounded patch (unified diff in chat, labeled hunks) for accepted-quality
findings; run the named tests if you can and report real results.
Design-level problem → `NEEDS_ARCHITECTURE_PASS`, findings only, NO diff.

RETURN, in order: review_summary YAML + labeled findings (severity /
file:line / issue / evidence / impact / minimum_closure_condition /
next_authorized_action); labeled unified diff with per-change citations;
verdict + residual-risk note (state explicitly whether any finding means an
empty pickup after this reconcile can be an INVALID no-work claim); real
test results or an explicit not-run statement; one-line read-budget audit;
adjudicator tail: your output is claims to adjudicate — the CA may veto any
change; nothing is kept until home-CA adjudication.

Your output is decision input only — no validation, readiness, approval, or
acceptance claims.
````

## Dispatch notes (operator)

- Paste into a non-Anthropic lane with the GitHub repo readable (repo mode;
  cross-vendor discovery bar).
- On return, courier the full output back for review-return adjudication.
- Non-claims: provisional convention; findings + diff are decision input only;
  no validation, readiness, formal verdict, or build authorization.
