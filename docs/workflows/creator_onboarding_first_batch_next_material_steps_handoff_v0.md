# Creator Onboarding First Batch Next Material Steps Handoff v0

```yaml
retrieval_header_version: 1
artifact_role: workflow handoff packet
scope: >
  Cold-lane handoff for the next material creator-scanning steps after the
  Forseti data-lake rename and TikTok scanner hardening merges: first
  onboarding batch, PROMOTE receipt-evidence binding, deferred scanner
  executor, and the operator-only scheduled-task cleanup one-liner.
use_when:
  - Starting a fresh lane for the first creator onboarding batch.
  - Routing the PROMOTE preflight receipt-evidence binding design before registry mutations scale.
  - Deciding whether scanner volume now justifies a live scanner executor.
authority_boundary: retrieval_only
stale_if:
  - PR #843 or PR #847 is reverted or superseded.
  - TikTok Creator Discovery Frontier schema changes after b25eab5853453cc11c492e8f71c22ba562eefafa.
  - Creator Registry match-preflight receipt semantics change.
  - A live scanner executor is accepted or implemented.
```

## Forseti Start Preflight

```text
forseti_start_preflight:
  agents_read: yes
  overlay_read: yes
  source_pack: custom S3 target deepening
  edit_permission: docs-write
  target_scope: workflow handoff for next creator onboarding, PROMOTE binding, and scanner executor routing; no live capture or registry mutation
  dirty_state_checked: yes
  blocked_if_missing: AGENTS.md, overlay README, decision-routing, source-loading, TikTok frontier contract/code, Creator Registry preflight usage, PR #843/#847 merge evidence
```

## Cynefin Routing

Smallest complete outcome: provide a branch-visible handoff that lets a fresh
lane choose and start the next material work without inheriting stale lake-rename
or scanner-hardening context.

Regime: mixed. First onboarding batch is live-capture/operator-gated execution;
PROMOTE receipt binding is architecture/schema design; scanner executor is
deferred infrastructure; scheduled-task removal is operator-side system cleanup.

Current bottleneck: do not let registry onboarding scale on self-certified
preflight status strings. Bind PROMOTE to a receipt artifact before new registry
mutations become routine.

Allowed next move: start with the PROMOTE receipt-binding design pass or a
non-mutating onboarding preflight/ranking batch.

Disallowed next move: run live capture, unregister scheduled tasks, deep-capture
creators, or mutate Creator Registry from this handoff alone.

## Verified State

- PR #843 is merged: `docs: lake rename executed -- receipt, stale-doc refresh, lane closeout handoff`; merge commit `81ebcd48b1ae0d6b21b02e500332c79ea4833e6d`; merged at `2026-07-10T04:07:50Z`.
- PR #847 is merged: `feat(scanner): TikTok creator-scanner hardening P1-P5 (link-hub contract, CDP probe, lake writer, preflight gates)`; merge commit `b25eab5853453cc11c492e8f71c22ba562eefafa`; merged at `2026-07-10T15:45:16Z`.
- Current branch for this handoff was created from `origin/main` at `b25eab5853453cc11c492e8f71c22ba562eefafa`.
- Current worktree status before writing this file: branch `codex/creator-onboarding-next-material-handoff...origin/main`, untracked `_scratch/`, and permission-denied warnings for `pytest-cache-files-kpj82v99/`, `pytest-cache-files-v9c1b3mh/`, and `tmp1bgdt18q/`.

## What PR #847 Actually Gives Us

Current code now makes several prior silent-miss shapes fail closed at the
receipt/register boundary:

- scan receipts use `tiktok_creator_discovery_scan_receipt_v1`;
- parent-grid packet pointers and suggested-account packet pointers are checked;
- CloakBrowser/equivalent parent capture requires suggested-account attempt or
  blocked/empty outcome;
- link-hub outcome is required and `captured` requires an absolute HTTP(S) URL;
- screenshots in chat, candidate-profile opens, browser closes, follow/unfollow
  over one action, and metric/registry/contact/private-identity output fields are rejected;
- routine frontier-register writing defaults to the data lake through
  `run_tiktok_creator_discovery_register.py`, with explicit `--output` as the
  local escape;
- the lake writer requires a real `DataLakeRoot` and a committed parent-grid
  packet anchor;
- creator-profile materialization now requires a schema-valid preflight receipt
  that covers new public handles with non-blocking result rows;
- local CDP probe input validation rejects bad ports/timeouts and formats IPv6
  loopback correctly.

Do not overclaim this. The merged code still does not perform live TikTok scans.
`run_tiktok_creator_discovery_register.py` builds and persists a register from a
scan receipt plus suggested rows; it is not a scanner executor.

## Material Work Batches

### 1. PROMOTE Receipt-Evidence Binding

This should usually happen before registry mutations scale.

Problem: current `FrontierNode.registry_preflight_status_or_none` is still a
scalar status string. The validator rejects empty, non-string, and obvious
not-run markers for `PROMOTE`, but the field is still self-authored. That is
better than the original fake-pass, but it is not the receipt-evidence binding
the review wanted.

Target design decision:

- bind `PROMOTE` to a candidate-specific Creator Registry preflight receipt row;
- store a repo/lake pointer plus SHA-256 for the receipt artifact, not just a
  free-form status string;
- bind the selected node/candidate to receipt row fields:
  `candidate_id`, `intended_action`, `decision`, `action_status`, and
  `can_start_new_capture`;
- fail closed on missing receipt, wrong candidate, wrong platform/handle,
  malformed schema, blocking/ambiguous/invalid result, stale hash, or unrelated
  receipt;
- preserve exact-match scope: this still does not prove fuzzy duplicate absence
  or cross-platform identity.

Expected touched surfaces:

- `forseti-harness/capture_spine/tiktok_creator_discovery_frontier/models.py`
- `forseti-harness/capture_spine/tiktok_creator_discovery_frontier/validation.py`
- `forseti-harness/tests/unit/test_tiktok_creator_discovery_frontier.py`
- `forseti/product/spines/scanning/source_families/tiktok/tiktok_creator_discovery_frontier_register_v0.md`
- possibly a narrow decision record under `docs/decisions/` if the schema choice
  needs owner-visible rationale.

Validation expectation:

- focused red/green tests for missing, malformed, known-negative, unrelated,
  wrong-candidate, stale-hash, non-string, and genuine cleared receipt cases;
- `python -m pytest forseti-harness/tests/unit/test_tiktok_creator_discovery_frontier.py -q`;
- strict doc gates if a decision/spec artifact is touched.

### 2. First Onboarding Batch

This is the program payoff: preflight -> rank -> deep-capture top 20-25%.

Allowed without live capture:

- assemble candidate handles from existing TikTok frontier registers, opened
  creator profiles, and manually supplied creator handles;
- run exact-match Creator Registry preflight for candidates;
- preserve the preflight receipt artifact and hash;
- rank candidates for onboarding priority using source-visible, non-private
  evidence only;
- produce the candidate matrix and select the top 20-25% for owner approval.

Owner-gated live work:

- opening TikTok/IG/YT surfaces;
- capturing grids;
- deep-capturing selected videos/reels/Shorts;
- writing new live Source Capture packets;
- mutating Creator Registry.

Ranking guidance:

- prioritize source-visible US/core fragrance creators first;
- keep GB/non-US creators in discovery memory but deprioritize them for the
  current US roster unless the owner overrides;
- use registry status, source-visible region, fragrance-core fit, prior graph
  frequency, link-hub/sibling-channel evidence, and recent visible grid signal;
- do not use private identity/contact enrichment;
- do not treat link hubs as metric capture;
- do not deep-capture every visible grid video before ranking.

Deep-capture rule:

- grid/preflight/ranking first;
- deep-capture only the selected top 20-25% or event-triggered breakouts;
- deep-capture packets go to the data lake and remain metric/source packets,
  not registry truth.

### 3. Scanner Executor

The audit headline gap remains by design: validation fires when receipts are
validated, but no runner performs the full live scan.

Do not build a scanner executor just because it is architecturally neat. Revisit
only when scan volume makes agent-performed procedure the bottleneck.

If revisited, the executor should own this sequence:

1. local CDP/session probe;
2. warmed session selection, no browser close;
3. parent TikTok profile/grid packet capture;
4. suggested-account `View all` / modal capture;
5. bio region and link-hub capture outcome;
6. link-hub sibling account extraction;
7. lake packet/register write;
8. Creator Registry exact-match preflight;
9. candidate matrix output.

Hard stops:

- no bot evasion, account rotation, proxy plan, captcha solving, or standing
  crawler;
- no private contact/identity enrichment;
- no registry mutation without current preflight and explicit registry-write
  authorization.

### 4. Owner One-Liner

Operator-side cleanup, not run by this handoff:

```powershell
Unregister-ScheduledTask OrcaIGExtract -Confirm:$false
```

Do not run this from a fresh lane unless the user explicitly asks in that lane.
It removes a scheduled task and is an operator/system action, not a repo change.

## Exact Next Authorized Action

Recommended order:

1. Start the PROMOTE receipt-evidence binding pass on a fresh branch from
   `origin/main`. This is small, design/schema-bound, and reduces registry
   mutation risk before onboarding scales.
2. In parallel or after that pass, run a non-mutating first onboarding batch:
   candidate list -> exact-match preflight -> rank -> top 20-25% proposal.
3. Ask for explicit live-capture authorization before opening platforms or
   deep-capturing selected creators.
4. Defer scanner executor unless the onboarding batch proves manual procedure is
   now the bottleneck.
5. Leave the scheduled-task command as an owner one-liner unless explicitly
   instructed to run it.

## Source Ledger

- `AGENTS.md`
  - Role: project instruction entrypoint.
  - Load-bearing: yes.
  - SHA256: `0AE058B6E0E3BC75E43C3E93E8A0251A5A777CB5B3E6DC522414AA9AE08BA641`
- `.agents/workflow-overlay/README.md`
  - Role: overlay entrypoint.
  - Load-bearing: yes.
  - SHA256: `049403E4908C3FF5F0562893967897A4F754F2F771B843734D2DBCA57059DB11`
- `.agents/workflow-overlay/decision-routing.md`
  - Role: Cynefin routing.
  - Load-bearing: yes.
  - SHA256: `688AAC653FCE6AA5DBDD4D5050946509B998B1CAC6421520408E029719895C1E`
- `.agents/workflow-overlay/source-loading.md`
  - Role: start-preflight and source-pack rules.
  - Load-bearing: yes.
  - SHA256: `F25AF717E382BA183CE35A3422DBEC1B5FB7396312FDECD590E31F4AC53E5467`
- `.agents/workflow-overlay/prompt-orchestration.md`
  - Role: handoff/prompt contract and filing distinction.
  - Load-bearing: yes.
  - SHA256: `A53060E56BAFFBA401AE32C8F7985F0B186BC6F74F93254D0CB55DD7ADD52C95`
- `forseti/product/spines/scanning/source_families/tiktok/tiktok_creator_discovery_frontier_register_v0.md`
  - Role: TikTok frontier product architecture contract.
  - Load-bearing: yes.
  - SHA256: `F79FEEC35B46B8061E108691622933B833702C819DCA14E929505CB99F1D3017`
- `forseti/product/spines/capture/core/source_families/social_media/creator_registry/creator_registry_match_preflight_usage_v0.md`
  - Role: exact-match preflight contract.
  - Load-bearing: yes.
  - SHA256: `AA98B62AB4021C4A2EF4AAED8F60BDE6089269087709D7EA5A1317B14D05684E`
- `forseti-harness/capture_spine/tiktok_creator_discovery_frontier/models.py`
  - Role: current schema dataclasses.
  - Load-bearing: yes.
  - SHA256: `349B2921F66AFC7D174D8E38718E2FC5C547D48911330A257F2FC405D852138C`
- `forseti-harness/capture_spine/tiktok_creator_discovery_frontier/validation.py`
  - Role: current validators and PROMOTE gate.
  - Load-bearing: yes.
  - SHA256: `EF88063F6276738E96C898A0031480BC6DE163C2368BED493CDA3A90BBBA85C0`
- `forseti-harness/runners/run_tiktok_creator_discovery_register.py`
  - Role: register builder/persistence runner, not live scanner.
  - Load-bearing: yes.
  - SHA256: `AAF7AEF20DC7C9C3395F928ED3333C124FDF8B25A33B09D57F0356F7C42F9F54`
- `forseti-harness/runners/run_creator_profile_current_materialize.py`
  - Role: registry-current materialization preflight gate.
  - Load-bearing: yes.
  - SHA256: `43197D3B25C31A2FFA52C8EF5CC9603260DB10F8BBA966B2A04FD165D1F12F0B`
- `forseti-harness/capture_spine/tiktok_creator_discovery_frontier/register_lake_writer.py`
  - Role: lake writer for frontier registers.
  - Load-bearing: yes.
  - SHA256: `013E3E577C50074EB94A79E110CC9B196603064CDC369BF261F207FCA895F999`
- `forseti-harness/source_capture/adapters/browser_session_probe.py`
  - Role: local CDP probe.
  - Load-bearing: yes.
  - SHA256: `C9602E5FA48F986B3A2CCC69739FEE737A0CEF46AF6D4170D2FA1FE823B1C776`
- `docs/review-outputs/tiktok_scanner_hardening_delegated_adversarial_code_review_v0.md`
  - Role: review output naming F2/PROMOTE residual and scanner executor residual.
  - Load-bearing: yes for residual provenance, stale as review of pre-merge branch details.
  - SHA256: `CF33DCE403860E1761B3F9E0699CE31E9B80E4BB48527CF5A692050A3A39D097`

## Strict Non-Claims

- not live capture authorization;
- not Creator Registry mutation authorization;
- not proof that any creator is roster-ready;
- not metric validity;
- not proof that scanner executor exists;
- not approval to unregister the scheduled task;
- not proof that fuzzy duplicates are absent.

