# Core Spine v0 Method Validation Fresh Replay Source-Loading Wrapper v0

```yaml
retrieval_header_version: 1
artifact_role: Thin wrapper prompt
scope: Fresh-context source-loading wrapper for the Core Spine v0 method-validation replay prompt.
use_when:
  - Launching a new fresh-context Core Spine v0 method-validation replay.
  - Preventing broad source loading, artifact echo, and contaminated-thread carryover before replay.
authority_boundary: retrieval_only
open_next:
  - docs/prompts/product-planning/core_spine_v0_method_validation_replay_packet_prompt_v0.md
  - orca/product/case_families/product_learning/other_verticals/core_spine_v0_method_validation_case_frame_locks_v0.md
input_hashes:
  docs/prompts/product-planning/core_spine_v0_method_validation_replay_packet_prompt_v0.md: 0506819EEBEB952AC8B40E2AF84A65873EFA88E52C5A08CCEB6A7FA432270469
  docs/product/core_spine_v0_method_validation_case_frame_locks_v0.md: 4C8CFE49D8BB2FDDE650C99FEBB7BFE5F0CF76125057BD1B992431027D541785
stale_if: Base replay prompt or accepted case-frame lock hash changes, launch context contains prior failed-run source evidence, or target replay output paths already exist without explicit overwrite/archive/versioning instruction.
```

## 1. Wrapper Status And Purpose

- Prompt family: Thin wrapper / fresh replay launch wrapper
- Workspace: `C:\Users\vmon7\Desktop\projects\orca`
- Expected branch at wrapper creation: `main`
- Expected HEAD at wrapper creation: `3bf5c45`
- Base full prompt: `docs/prompts/product-planning/core_spine_v0_method_validation_replay_packet_prompt_v0.md`
- Base prompt SHA256 at wrapper creation: `0506819EEBEB952AC8B40E2AF84A65873EFA88E52C5A08CCEB6A7FA432270469`
- Accepted frame artifact: `docs/product/core_spine_v0_method_validation_case_frame_locks_v0.md`
- Frame artifact SHA256 at wrapper creation: `4C8CFE49D8BB2FDDE650C99FEBB7BFE5F0CF76125057BD1B992431027D541785`
- Output mode for future replay: `file-write`, inherited from the base prompt after explicit launch authorization
- Edit permission for future replay: `docs-write` only for the target replay artifacts named in the base prompt, subject to output-collision handling below
- Public web/source research: not authorized by this wrapper alone; requires a later fresh launch turn explicitly authorizing the replay and public source research

This wrapper fixes the long-term source-loading failure mode from the
contaminated replay thread. It does not run the replay, validate the method,
accept any replay artifact, authorize implementation, or weaken anti-leakage
rules.

Use this wrapper only from a fresh context. Treat the contaminated thread as a
process failure signal, not as evidence, not as a source list, and not as an
orientation packet for case facts.

## 2. Fresh-Context Launch Rule

Before any source research or replay work, the receiving agent must check
whether the launch context contains:

- prior failed-run URLs;
- prior failed-run source titles;
- prior failed-run source notes;
- prior failed-run post-window observations;
- copied evidence units from the contaminated run;
- existing replay artifact prose offered as evidence.

If any are present, stop immediately as `BLOCKED_CONTAMINATED_CONTEXT` and ask
for a fresh launch context that includes only this wrapper, the base prompt, the
accepted frame artifact, and explicit owner authorization.

The existence of the previous contaminated run may be used only to justify this
source-loading contract. Its case facts, URLs, snippets, observations, and
draft artifacts are not admissible replay evidence.

## 3. Required Minimal Project Preflight

Read only this minimal project pack before the first case:

1. `AGENTS.md`
2. `.agents/workflow-overlay/README.md`
3. `.agents/workflow-overlay/source-of-truth.md`
4. `.agents/workflow-overlay/artifact-roles.md`
5. `.agents/workflow-overlay/validation-gates.md`
6. `.agents/workflow-overlay/safety-rules.md`
7. `.agents/workflow-overlay/prompt-orchestration.md`
8. `docs/prompts/product-planning/core_spine_v0_method_validation_replay_packet_prompt_v0.md`
9. `docs/product/core_spine_v0_method_validation_case_frame_locks_v0.md`

Then run narrow mechanical checks:

- `git status --short --branch`
- `git log --oneline -6`
- SHA256 for the base prompt and accepted frame artifact
- existence checks for the five target per-case artifacts and packet artifact

Do not read product thesis, product contract, proof packet, review reports, or
existing replay artifacts during preflight unless a specific missing rule would
materially change the replay boundary. If a broader read is needed, state the
exact missing rule and the exact file before reading it.

## 4. Output Collision Rule

The current workspace may contain existing untracked replay outputs from a prior
attempt. Existing target artifacts are output collisions, not source evidence.

If any target replay artifact already exists, stop before web/source research as
`BLOCKED_OUTPUT_DESTINATION_COLLISION` unless the owner explicitly chooses one
of:

- overwrite the existing target files;
- archive or move the existing target files under an accepted Orca docs folder;
- write new `v1` target artifact paths;
- treat existing outputs as review targets in a separate review lane.

To identify an output collision, the runner may inspect only file existence,
path, hash, and a narrow heading/status window. Do not read existing replay
artifact bodies as source for a fresh replay.

## 5. Context Budget

Context budget tier: `large`.

Reason: the replay spans five cases, public web/source research, per-case
artifacts, and final packet synthesis. It is not monorepo work, but it is too
large for one broad live context. The runner must use sealed case micro-runs
with compact summaries.

Live-context target:

- keep only current case frame, current case source ledger, current case
  at-cutoff reasoning, and a compact summary of completed prior cases;
- move detailed Evidence Units, source ledger rows, post-window comparison, and
  readback evidence into the written case artifact;
- after each case, retain no more than one compact case summary for packet
  synthesis.

## 6. Case-By-Case Source-Loading Sequence

Run exactly one case at a time in the accepted order from the base prompt.

For each case:

1. Read only that case frame from the accepted frame artifact.
2. Copy no other case frames into live context unless the base prompt requires
   portfolio-level ordering or packet synthesis.
3. Verify cutoff and pre-cutoff source visibility before interpretation.
4. Build first-order Evidence Units only from public sources verified as visible
   before cutoff.
5. Build second-order Evidence Units only from public sources inside the
   accepted source-family boundary and verified as visible before cutoff.
6. Write and seal the at-cutoff memo before opening any post-window outcome
   source for that case.
7. After sealing, inspect post-window outcome sources only for that same case.
8. Write the case artifact.
9. Mechanically read back only headings, status, anti-leakage ledger, source
   ledger counts, seal marker, and final verdict.
10. Emit a user-visible checkpoint before starting the next case.

Do not batch-open post-window materials across cases. Do not browse outcome
windows for later cases while working on an earlier case.

## 7. Source-Read Ledger Shape

Each case artifact must include a source-read ledger with this shape:

| Field | Required content |
| --- | --- |
| `source_id` | Stable case-local ID, such as `MV03-S07` |
| `source_family` | Accepted first-order or second-order family from the case frame |
| `authority_role` | `pre-cutoff evidence`, `post-window comparison`, `process source`, or `blocked source` |
| `title_or_locator` | Page title, source title, or durable locator |
| `url_or_path` | Public URL or Orca path |
| `publication_or_snapshot_date` | Date used for visibility reasoning |
| `searched_or_opened` | `search-snippet-only`, `opened`, `archive-opened`, or `not-opened` |
| `visibility_basis` | Why it is visible before cutoff, or why visibility is not proven |
| `used_status` | `used`, `excluded`, `blocked`, or `post-window-only` |
| `reason` | One concise reason |
| `leakage_note` | `none`, `snippet-noise`, `post-window-blocked`, or `blocked-by-leakage` |
| `excerpt_scope` | Short locator only; no long pasted source text |

The live thread should carry only compact ledger summaries. Full row detail
belongs in the case artifact.

## 8. Web Search And Open Caps

Before a case's at-cutoff memo is sealed:

- maximum 4 search queries per case;
- maximum 12 page opens per case;
- maximum 3 opened pages per source family;
- use date-limited queries, archived pages, or timestamped official pages when
  available;
- search only accepted source families from the case frame;
- do not use outcome search terms unless they are already part of a pre-cutoff
  accepted source family;
- do not open known post-window result pages;
- do not open search results whose visible title or snippet clearly identifies a
  post-window outcome.

If a search result snippet reveals outcome information, record only
`snippet-noise: yes` in the anti-leakage ledger. Do not preserve the revealed
fact in live context or in the source ledger.

After the at-cutoff memo is sealed:

- maximum 4 post-window outcome page opens per case;
- open only outcome sources for that same case;
- record post-window material as comparison evidence, never as at-cutoff
  evidence.

Escalate the caps only if a missing source could materially change the case
status. The escalation note must name the missing source family, the open count
so far, and why the result would change a `used`, `blocked`, or `not proven`
boundary.

## 9. Artifact Write And Readback Rules

Write each case artifact before moving to the next case. Do not keep full case
artifact prose in live context after writing.

After writing each case artifact, verify only:

- file path exists;
- SHA256 hash;
- required headings exist;
- source-read ledger exists;
- anti-leakage ledger exists;
- at-cutoff seal marker exists;
- post-window comparison appears after the seal marker;
- final status or blocked verdict exists.

Use line-window reads, heading searches, `rg`, `Select-String`, and hashes.
Do not full-echo the artifact. Do not paste long Evidence Units back into chat.

## 10. Checkpoint Cadence

After each case artifact is written and mechanically checked, return a compact
checkpoint before continuing:

```yaml
case_checkpoint:
  case_id:
  artifact_path:
  artifact_sha256:
  status:
  at_cutoff_sealed: true|false
  post_window_opened_after_seal: true|false
  leakage_status:
  source_visibility_blockers:
  open_counts:
    searches:
    pre_cutoff_page_opens:
    post_window_page_opens:
  retained_for_packet_synthesis:
    one_paragraph_summary:
    first_order_result:
    second_order_movement:
    calibration_label:
  next_case:
```

If the environment or UI cannot emit a checkpoint and continue, write the
checkpoint into the case artifact and stop for owner instruction rather than
silently continuing through all five cases.

## 11. Packet Synthesis Rules

After all five case artifacts exist, synthesize the packet only from:

- the base prompt's packet contract;
- the accepted case list;
- each case artifact path, hash, status, and compact summary;
- case-level method lessons and blocked states.

Do not reload full case artifacts unless a compact summary is missing or
contradictory. If full readback is needed for one case, use line windows around
the missing heading only.

## 12. Stop Conditions

Stop as `FAILED_UNBOUNDED_READ` if:

- whole-repo scanning replaces a targeted source question;
- the runner reads broad product/proof/review source families without naming
  the missing rule first;
- source-map construction replaces Evidence Units and ledgers;
- full artifact readback or full source dumps are pasted into live context;
- web/source research becomes open-ended beyond the per-case caps;
- broad loading is used to regain confidence rather than resolve a named
  material uncertainty.

Stop as `BLOCKED_BY_LEAKAGE` if post-window outcome material is opened before
that case's at-cutoff memo is sealed and the case cannot be restarted in a fresh
context without carrying the leaked content.

Stop as `BLOCKED_SOURCE_VISIBILITY` if source visibility cannot be proven
without opening post-window outcome material.

Stop as `BLOCKED_OUTPUT_DESTINATION_COLLISION` if target artifacts already
exist and no owner decision resolves overwrite, archive, or versioning.

Stop as `BLOCKED_CONTAMINATED_CONTEXT` if the launch context contains prior
failed-run evidence, URLs, source notes, or outcome observations.

## 13. Fresh Launch Prompt

Use the following in a new thread when the owner explicitly authorizes replay:

```text
Use `workflow-deep-thinking`.

You are launching a fresh-context Core Spine v0 method-validation replay for
Orca.

Workspace:
`C:\Users\vmon7\Desktop\projects\orca`

Required first read:
`docs/prompts/wrappers/core_spine_v0_method_validation_fresh_replay_source_loading_wrapper_v0.md`

Then follow the wrapper exactly. Do not use any prior failed-run URLs, source
lists, notes, observations, existing replay artifact prose, or contaminated
thread context as evidence.

Replay and public web/source research are authorized only under the wrapper's
case-by-case source-loading contract. Do not create software implementation,
source maps, data-spine designs, dashboards, scoring systems, automation,
packages, tests, commits, pushes, or PRs.

Before opening any public source, complete the wrapper preflight and stop if
there is an output collision, stale hash, contaminated launch context, missing
authority, or unbounded-read risk.
```

## 14. Explicit Non-Claims

This wrapper does not claim:

- the replay is complete;
- any case artifact is accepted;
- any existing replay artifact is valid;
- the current dirty worktree is acceptable for replay without a fresh launch
  preflight;
- public source visibility is sufficient;
- Core Spine v0 is validated;
- external buyer demand is proven;
- feature planning, implementation planning, source systems, data spine,
  dashboards, scoring systems, automation, packages, tests, commits, pushes, or
  PRs are authorized.
