# Summer Fridays p05/p06 Decision-Usefulness Opposing-Family Review Prompt v1

```yaml
retrieval_header_version: 1
artifact_role: Review prompt
scope: >
  Read-only A/B comparison of two Summer Fridays Turn A evidence sets on
  downstream decision usefulness only.
use_when:
  - Comparing the completed p05 observational control with the p06 best-output treatment.
  - Judging whether the p06 Understanding acquisition produces a materially better decision substrate.
authority_boundary: retrieval_only
input_hashes:
  set_a_acquisition_record: 997d1fd9155d69278f56b47536a8b623cfc6281c1dd50954b70c58bc173e292a
  set_a_company_core: 2ca0ff7791d7c060ab8a176d70f65f35c1119d45d76029a1f57191ae71dbd357
  set_a_retail_corpus: 8aff1b624526fa7f5bd92691a6179c4722dc226a02fa14ce8e23298144de62dc
  set_a_customer_community: d12d1073c37437a49c1d9940f35534c40e716d9dc17f9c2d2b5e6ba9cc9cb1ab
  set_b_acquisition_record: 12d89a4b5fe11439d2c54c03d2a539a120f9e552c760f6b968655525c55c7697
  set_b_company_core: 3bc436e8f40169ac7f57c029117ad051b5fc8e75f3543046097bdccd5a16f8c4
  set_b_retail_corpus: 9001d8c39e71c5362940785eeda5dd41cf78d3c8ab034de0089a591d5b6f2a34
  set_b_customer_community: fc91461440552a583bfcecbe3d87a9de5a825b41d5e544da22a9514dd07b95df
stale_if: Any listed input hash changes.
```

You are performing a read-only, opposing-family adversarial artifact review
for Forseti.

```yaml
output_mode: paste-ready-chat
template_kind: adversarial-artifact-review
edit_permission: read-only
targets: the eight exact hash-pinned files listed below
input_prompt_source: docs/prompts/reviews/summer_fridays_p05_p06_decision_usefulness_opposing_family_review_20260724_v1.md
review_response_destination: current review task chat
doctrine_change: none
preflight_defaults: docs/prompts/templates/shared/forseti_preflight_defaults_v0.md v0 - constants bound; deltas stated inline.
```

## What this is for

**Goal:** Decide which evidence set gives a fresh downstream Deliver or
Problem-Framing consumer more useful understanding of Summer Fridays.

**Done looks like:** A forced `SET_A_PREFERRED`, `SET_B_PREFERRED`, `TIE`, or
`INCOMPARABLE` verdict with confidence, a dimension-by-dimension ledger,
file-and-line citations for every decisive claim, and explicit residual gaps.
This is an output-value comparison, not a causal claim about orchestration,
topology, capture route, model quality, or run chronology.

The only review axis is **decision usefulness**. Phase A aims for complete,
decision-useful understanding. Compactness, token cost, and smallest-complete
economy belong to later delivery work and must not influence this comparison.

## Binding and source sequence

1. Read `AGENTS.md`, `.agents/workflow-overlay/README.md`,
   `.agents/workflow-overlay/review-lanes.md` (Current Lanes, Review Doctrine,
   Rules), and `.agents/workflow-overlay/communication-style.md` (Chief
   Architect Review Consumption and Adversarial Review Summary Pattern).
2. REFERENCE-LOAD `workflow-adversarial-artifact-review`. Do not apply it yet.
3. Hash all eight targets with SHA-256. Any mismatch returns
   `BLOCKED_INPUT_HASH_MISMATCH`; do not substitute another checkout, summary,
   prior review, or recreated source.
4. SOURCE-LOAD all eight targets in full. Declare `SOURCE_CONTEXT_READY`, or
   `SOURCE_CONTEXT_INCOMPLETE` with the exact missing or unreadable files.
5. Only after source readiness, APPLY
   `workflow-adversarial-artifact-review` to this comparison.

If the required review skill is unavailable or cannot be applied after source
readiness, return advisory-only critique and do not emit the bound comparison
verdict.

## Evidence Set A

| Artifact | Exact path | SHA-256 |
| --- | --- | --- |
| Integrated acquisition record | `C:\Users\vmon7\.codex\worktrees\6bbc\orca\docs\research\summer_fridays_understanding_dogfood_20260723_p05\coordinated\turn_a_acquisition_record.md` | `997d1fd9155d69278f56b47536a8b623cfc6281c1dd50954b70c58bc173e292a` |
| Company/high-yield core | `C:\Users\vmon7\.codex\worktrees\6bbc\orca\docs\research\summer_fridays_understanding_dogfood_20260723_p05\coordinated\specialists\co1_company_core.md` | `2ca0ff7791d7c060ab8a176d70f65f35c1119d45d76029a1f57191ae71dbd357` |
| Retail portfolio corpus | `C:\Users\vmon7\.codex\worktrees\6bbc\orca\docs\research\summer_fridays_understanding_dogfood_20260723_p05\coordinated\specialists\co2_retail_corpus.md` | `8aff1b624526fa7f5bd92691a6179c4722dc226a02fa14ce8e23298144de62dc` |
| Customer/community and depth | `C:\Users\vmon7\.codex\worktrees\6bbc\orca\docs\research\summer_fridays_understanding_dogfood_20260723_p05\coordinated\specialists\co3_customer_community_depth.md` | `d12d1073c37437a49c1d9940f35534c40e716d9dc17f9c2d2b5e6ba9cc9cb1ab` |

## Evidence Set B

| Artifact | Exact path | SHA-256 |
| --- | --- | --- |
| Integrated acquisition record | `C:\tmp\forseti-sf-understanding-dogfood-20260724-p06-worktree\docs\research\summer_fridays_understanding_dogfood_20260724_p06\coordinated\turn_a_acquisition_record.md` | `12d89a4b5fe11439d2c54c03d2a539a120f9e552c760f6b968655525c55c7697` |
| Company/high-yield core and identity | `C:\tmp\forseti-sf-understanding-dogfood-20260724-p06-worktree\docs\research\summer_fridays_understanding_dogfood_20260724_p06\coordinated\specialists\co1_company_core_identity.md` | `3bc436e8f40169ac7f57c029117ad051b5fc8e75f3543046097bdccd5a16f8c4` |
| Authorized retail portfolio | `C:\tmp\forseti-sf-understanding-dogfood-20260724-p06-worktree\docs\research\summer_fridays_understanding_dogfood_20260724_p06\coordinated\specialists\co2_retail_portfolio.md` | `9001d8c39e71c5362940785eeda5dd41cf78d3c8ab034de0089a591d5b6f2a34` |
| Customer/community and category depth | `C:\tmp\forseti-sf-understanding-dogfood-20260724-p06-worktree\docs\research\summer_fridays_understanding_dogfood_20260724_p06\coordinated\specialists\co3_customer_community_depth.md` | `fc91461440552a583bfcecbe3d87a9de5a825b41d5e544da22a9514dd07b95df` |

## Blinding boundary

Treat `A` and `B` as opaque evidence-set labels. Do not read either run's
commission, handoff, commission board, acquisition seal, task transcript,
prior comparison, control metrics, or sibling-arm output. Do not ask which set
is the control, treatment, newer route, or preferred outcome.

The absolute source paths necessarily expose run identifiers, so this is
**partial label blinding**, not perfect blinding. Do not infer merit from the
run number or artifact naming. If that exposure materially affects judgment,
state how.

## Decision-usefulness criteria

Judge what a fresh consumer can actually learn and act on from each set:

1. Material events, ownership, leadership, and chronology.
2. Correct product identity: parent products and families are distinguished
   from shade, flavor, size, bundle, set, and other variants.
3. Portfolio, category, price, claims, and launch architecture.
4. Current official US retailer authorization and the decision value of the
   admitted retailer assortment, overlap, PDP facts, and meaningful gaps.
5. Customer/community language, pain points, purchase drivers, objections,
   response patterns, and category-balanced review/Q&A depth across lip,
   skincare, fragrance, and body or newer products where the evidence permits.
6. Actionability for downstream Problem Framing or Deliver: clear implications,
   bounded next questions, and honest uncertainty.
7. Navigability and traceability for a fresh reader.
8. Completeness and specificity of the evidence that supports the above.

Do **not** score seal correctness, readiness, topology compliance, task count,
stopping rules, route typing, official-first sequencing, VPN use, ZIP handling,
capture mechanics, compactness, token cost, or elapsed time as independent
dimensions. Mention a process fact only when it directly changes what a
downstream consumer can learn or do.

Do not treat terminal seal state as the answer. Do not claim that the preferred
output is sufficient for Deliver, that the route caused the difference, or
that the result generalizes beyond this one comparison.

## Provenance-accuracy check

These are evidence-bearing artifacts. For each claim that materially changes
the preference:

- dereference its cited internal pointer when the referenced row or artifact is
  within the eight-file review set and verify semantic match;
- recompute decisive counts, sums, overlaps, and ranges from the rows they
  summarize;
- trace decisive prices or figures to the cited excerpt, or label them
  untraceable;
- distinguish event dates from page-read, retrieval, or publication dates;
- distinguish source absence from route failure and nationwide absence from
  bounded US-facing surface observations.

Do not expand into the raw capture lakes or public-web recapture. If a decisive
claim depends on a pointer outside the eight-file set, label that claim
`provenance_not_checked` and reflect the limitation in confidence. State any
unperformed provenance check rather than implying it occurred.

## Required output

Start with the compact Forseti `review_summary` YAML shape from
`.agents/workflow-overlay/communication-style.md`, using
`review_location: chat_only_current_thread`. Record the actual `reviewed_by`;
use `authored_by: unrecorded` because exact author model versions were not
captured. Record `de_correlation_bar: cross_vendor_discovery` only if the
reviewer is genuinely from a different upstream vendor family; otherwise state
the observed bar and do not claim cross-vendor discovery.

Then return, in this order:

1. `comparison_result`
   - `verdict`: `SET_A_PREFERRED | SET_B_PREFERRED | TIE | INCOMPARABLE`
   - `confidence`: `high | medium | low`
   - one-sentence decisive reason.
2. A compact criterion ledger with columns: criterion, Set A, Set B, edge,
   and decisive `file:line` citations.
3. Findings-first usefulness deficits for each set, using the review doctrine's
   severity, confidence, `minimum_closure_condition`, and
   `next_authorized_action` fields. Do not emit `patch_queue_entry`.
4. `considered_and_defended`.
5. Residuals:
   - more useful does not mean sufficient;
   - no topology, route, model, chronology, or causal-method claim;
   - partial-label-blinding limitation;
   - any unperformed provenance check.
6. A one-line read-budget audit.
7. Review-use boundary: decision input only, not approval, validation,
   readiness, mandatory remediation, or executor-ready authority.

The final answer must be self-contained and courier-ready. Do not edit any
source, write a report file, perform Turn B, or take Git lifecycle actions.
