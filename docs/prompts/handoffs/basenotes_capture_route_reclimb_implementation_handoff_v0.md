# Basenotes Capture Route Re-Climb — Implementation Handoff v0

```yaml
retrieval_header_version: 1
artifact_role: Planning handoff prompt
scope: >
  Bounded implementation commission to replace Basenotes' presently unusable
  hard-coded proxy recipe with the cheapest newly proven public capture route,
  then retire the old recipe without breaking projection, Cleaning, or Silver.
use_when:
  - The owner dispatches the Basenotes capture-route repair to an isolated implementation lane.
  - Re-probing the pinned Basenotes route after its required proxy profile became unavailable.
stale_if:
  - The Basenotes runner, source surface, owning source-family index, or route evidence changes.
  - A fresh Basenotes capture has already replaced and retired the route named here.
authority_boundary: retrieval_only
```

## Commission status

This is a prepared cross-lane implementation commission. It is not dispatch-ready
until the dispatcher replaces `receiver_to_bind` with one verified receiver class
under `.agents/workflow-overlay/decision-routing.md`. Do not source-load or edit
from this artifact while that binding is unresolved.

```yaml
forseti_start_preflight:
  agents_read: required_by_receiver
  overlay_read: required_by_receiver
  source_pack: custom
  edit_permission: implementation-authorized
  target_scope: >
    Basenotes capture-route diagnosis, one bounded public proof capture, route
    pinning, retirement of the superseded combined recipe, and reconciliation of
    every directly coupled capture/projection/Cleaning/Silver contract and test.
  dirty_state_checked: receiver_to_verify
  blocked_if_missing: >
    A verified isolated receiver, fresh origin/main, public Basenotes access,
    or the local dependencies required by the selected route.

prompt_preflight:
  output_mode: file-write
  write_destination: receiver implementation lane and its per-lane PR
  template_kind: direct-implementation
  template_status: unbound_by_registry_but_explicitly_owner_authorized_here
  input_prompt_source: docs/prompts/handoffs/basenotes_capture_route_reclimb_implementation_handoff_v0.md
  edit_permission: implementation-authorized
  targets: Basenotes capture runner, route evidence/indexes, coupled consumers, and focused tests only
  branch: fresh codex/ branch in the verified receiver, based on fresh origin/main
  dirty_state_allowance: clean receiver only; preserve and stop on unexpected modified or untracked files
  reviews: findings-first if review is commissioned; no review is implied by this prompt
  doctrine_change: >
    yes — the pinned Basenotes capture route and possibly source-surface contract
    may change; apply the owning direction-change propagation contract.
  report_destination: receiver chat plus PR body/checks; no standalone completion report required
  external_source_boundary: public Basenotes only; jb and external workflow sources are not Forseti authority
  repo_map_decision: not_needed
  repo_map_reason: exact owning sources and implementation seams are named below

receiver_binding:
  receiver_class: receiver_to_bind
  binding_state: receiver_to_bind
  launch_checkout: receiver_to_observe
  managed_starting_ref: origin/main
  required_revision: fresh_origin_main_at_dispatch
  revision_mode: exact
  capability_proof: not_yet_proven
  no_concurrent_writer_state: not_yet_proven

thread_operating_target_continuity:
  carried_forward: no
  reason: different_workstream
  changed_from_input: no
  lifecycle_status: not_supplied
  if_changed_reason: not_applicable
```

## Owner outcome

Make one ordinary Basenotes product capture work again through the lowest-cost
route that the current page actually requires, preserve its bytes in a valid raw
packet, and prove the existing Basenotes projection → Cleaning → Silver chain
against that packet. Only after the replacement passes may the old combined
`CloakBrowser + reddit-res-01 proxy` recipe be deleted or converted to historical
evidence.

Target page for the single bounded proof:

`https://basenotes.com/fragrances/mojave-ghost-by-byredo.26143979`

## Facts to confirm, not inherit

At authoring time, `forseti-harness/runners/run_basenotes_mgt_capture.py`:

- uses CloakBrowser;
- hard-codes proxy label `reddit-res-01`;
- loads that profile before capture; and
- describes the proxy combination as the only reaching route.

The latest dogfood attempt failed before network access because that label had
no registered proxy-profile metadata. This proves the current recipe is not
operable in the observed environment. It does **not** prove that Basenotes still
requires a proxy, that CloakBrowser alone will work, or that the source is
uncapturable.

The owning capture playbook says the route catalog is a menu, not an ordered
escalation ladder. Re-read the returned substrate after each failure and choose
the next cheapest matching route. Its present maturity note says no-proxy
persistent-profile CloakBrowser is proven only for one Quora case; proxy/geo is
still unproven. Treat both as hypotheses for Basenotes.

## Required source loading

Before diagnosis or edits, read:

1. `AGENTS.md` and `.agents/workflow-overlay/README.md`.
2. `.agents/workflow-overlay/source-loading.md`, `decision-routing.md`, and the
   relevant implementation/lifecycle sections they route to.
3. `forseti/product/spines/capture/core/source_capture_toolbox/source_capture_playbook_v0.md`
   — especially access classification, substrate diagnosis, route selection,
   route maturity, and probe-then-pin.
4. `forseti/product/spines/capture/core/source_families/fragrance_native_database/README.md`.
5. `docs/research/orca_fragrance_native_database_live_probe_v0.md`, including
   PIN-003 and the Proxy Route Verification Addendum; treat old observations as
   evidence to retest, not permanent route truth.
6. `forseti-harness/runners/run_basenotes_mgt_capture.py` and the generic direct,
   browser, and CloakBrowser packet runners it can legitimately compose.
7. `forseti-harness/source_capture/basenotes_projection.py`,
   `forseti-harness/cleaning/basenotes.py`,
   `forseti-harness/cleaning/basenotes_lake.py`, their runners, lane registry,
   touchpoint inventory, producer-version pins, and directly affected tests.

Declare `SOURCE_CONTEXT_READY`, or `SOURCE_CONTEXT_INCOMPLETE` with the exact
missing source and the safe work that remains, before choosing the route.

## Frozen decisions

1. The present combined recipe is a **retirement candidate**, not a working
   fallback. Do not silently keep a hard-coded missing proxy as the default.
2. Do not delete it first. Prove the replacement packet and downstream chain,
   then retire the superseded executable route and reconcile its claims.
3. Start from the cheapest route matching current evidence. At minimum test a
   direct/public baseline before escalating. If bytes are sparse or blocked,
   diagnose that result and test the next matching browser/render route.
4. CloakBrowser without proxy is a legitimate candidate. Prefer it over a proxy
   when it produces sufficient source-visible evidence because it has lower
   setup, secret, and long-term maintenance cost.
5. Add proxy/geo only if fresh Basenotes evidence requires it and an explicitly
   registered, category-correct profile exists. No hard-coded unrelated label,
   secret, endpoint, credential, or exit IP may enter the repo or report.
6. No login-gate or CAPTCHA defeat, no mass crawl, no standing automation, and
   no human-rate bypass. A visible access-control gate is a stop/handoff.
7. Keep `source_family: fragrance_native_database`. Change `source_surface`
   only when the new route has materially different evidence semantics; if it
   changes, reconcile every exact-surface consumer in the same unit.
8. Do not loosen packet, projection, Cleaning, or Silver validation to make the
   proof pass. Real failure remains visible.

## Smallest-complete implementation route

1. Reproduce the current runner's no-network preflight and missing-profile
   failure. Record that failure in test evidence without persisting secrets.
2. Probe the target page once per matching route, stopping as soon as one route
   returns sufficient first-party product-page evidence. Do not walk unrelated
   catalog rows for ceremony.
3. Sufficiency must be caller-bound and mechanically checked. At minimum require
   a Basenotes product identity/URL marker and source-visible fragrance product
   content sufficient for the existing projector. A transport success or blank
   browser shell is failure.
4. Refactor the Basenotes wrapper to the proven route. Route dependencies must
   be explicit inputs/configuration, and no absent profile may be concealed by
   a fake default.
5. Preserve exactly one proof packet using the sanctioned packet writer. Run the
   Basenotes projection and Cleaning/Silver derivation from that exact packet.
   Confirm the Silver write physically resolves the raw and derived evidence.
6. After that proof, delete or archive-as-history the old executable combined
   recipe, its false current-route claims, and dead constants. Preserve historical
   receipts as history; do not rewrite past observations as if they never happened.
7. Update the source-family route map, research route posture, runner registry,
   inventory, policies/versions, contracts, and tests only where the new route
   actually changes their behavior or exact surface binding.

If no route succeeds, return the smallest honest blocker with the observed
substrate/failure receipt. Do not revive `reddit-res-01`, invent a proxy, or
claim the route repaired.

## Required proof

Tests must cover at least:

- current broken-profile behavior fails visibly and before packet publication;
- new runner preflight names its real dependencies;
- the selected route rejects blocked/challenge-only or insufficient output;
- one sufficient route result writes a valid packet;
- wrong source family/surface and missing preserved bytes still fail;
- packet → Basenotes projection → Cleaning audit/Silver succeeds in a temp lake;
- the resulting Silver record passes the shared physical-source verifier;
- any changed source-surface partition remains exclusive across Basenotes,
  Fragrantica, and Parfumo catch-up readers;
- capture-runner seam, lane-registry, touchpoint-inventory, and policy-version
  gates pass where affected;
- `git diff --check` and the full Forseti harness CI-equivalent suite pass.

Run at most one bounded live proof capture for the target page. Report live
capture, downstream derivation, and every command as `passed`, `failed`,
`blocked`, or `not_run`. Never translate a skipped or blocked live check into a
pass. Do not make broader capturability, reliability, scale, completeness,
production-readiness, or Mini God Tier claims from one page.

## Lifecycle and return

Use the per-lane protected workflow: commit, push, and open/update a draft PR
after local verification. Do not merge. Re-read the branch, remote SHA, PR
changed-file set, draft/merge state, and checks before reporting them.

Return:

```yaml
source_context_status:
route_diagnosis:
selected_route:
retired_route:
proof_packet:
downstream_proof:
files_changed:
validation:
  focused:
  full:
  live_capture:
lifecycle:
  branch:
  base_sha:
  commit_sha:
  pushed:
  pr:
  draft:
  checks:
  merged: false
accepted_residuals:
verdict: BLOCKED | ROUTE_REPAIRED_NOT_LANDED | READY_FOR_OWNER_LAND
exact_next_action:
```

Every load-bearing code/contract claim needs a neutral `file:line` citation;
every lifecycle value must come from a fresh read. This handoff authorizes the
bounded implementation and one proof capture, not deletion-before-proof,
credential acquisition, broad crawling, merge, or production-readiness claims.
