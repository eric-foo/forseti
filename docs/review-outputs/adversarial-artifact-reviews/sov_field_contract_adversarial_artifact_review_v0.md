# Adversarial Artifact Review + Adjudication — Share-of-Voice Field Contract (v0)

```yaml
retrieval_header_version: 1
artifact_role: Reviewer findings report + home-CA adjudication record (docs/review-outputs/)
scope: >
  Durable record of the commissioned repo-mode cross-vendor delegated
  review-and-patch of
  core_spine_v0_data_lake_metric_family_share_of_voice_field_contract_v0.md
  and the home-CA adjudication that closed it: reviewer identity, the four
  findings, per-hunk accept/reject decisions, the applied amendments, and the
  CA closure checks that discharge the independent-review gate.
use_when:
  - Checking what the SoV field-contract review found and what the CA kept or rejected.
  - Verifying the de-correlation and gate-discharge provenance behind the contract's amendment pass.
authority_boundary: retrieval_only
review_provenance:
  authored_by: Anthropic claude-fable-5
  reviewed_by: OpenAI GPT-5 Codex (reviewer-stated identity; operator-couriered return)
  de_correlation_bar: cross_vendor_discovery
  access_mode: repo (pinned commit cf43db5f26f2eebc91854ce88f1c4678bb9a360c; target
    SHA256 33C7F793AB049A9EE3655A7194FF39B8E3B83307D8B1C63E1A3D97FB24792F4B confirmed by reviewer)
  dispatch: docs/prompts/reviews/sov_field_contract_repo_adversarial_artifact_review_patch_commission_prompt_v0.md
  reviewer_recommendation: patchable (no NEEDS_ARCHITECTURE_PASS)
  findings: 3 major + 1 minor
non_claims: >
  Advisory review + CA adjudication only — not validation, readiness, formal
  lane verdict, acceptance, or view-build execution. The residual named by the
  reviewer stands: a future view builder must still prove it implements these
  fields from committed records and manifests.
```

## Adjudication (per finding: claim → verification → decision)

1. **Mention refs are record-level only; counts not mechanically recomputable
   (major) — ACCEPTED.** Citation verified: the mention model carries
   `mention_id`, `source_pointer`, `start_ms`, `end_ms`
   (`orca-harness/schemas/product_mention_models.py:97-111`), and the
   incumbent `by_mention` builder does dedupe one record ref per key.
   Applied: mention-LEVEL refs required; `mention_count == len(mention_refs)`
   exactly.
2. **Publication-time window inclusion rules unbound; silent denominator
   shrinkage possible (major) — ACCEPTED.** Real ambiguity in the original
   text (surfacing missing publication evidence without saying whether such
   records stay in the denominator). Applied: basis-specific inclusion rule —
   missing-basis records excluded from numerator AND denominator, counted
   under `coverage.window_basis_missing`; all-missing scopes go
   `unavailable_with_reason`.
3. **Cohorts not reconstructable; zero rows can cherry-pick comparison sets
   (major) — ACCEPTED.** Applied: `cohort.member_refs | cohort_manifest_ref`
   reconciling to `coverage.source_objects_in_scope`;
   `selection_policy_versions.cohort_selection`; zero rows only under a
   declared source-backed `comparison_set` — absence of a row is not a zero.
4. **Lineage-gate token drift: prose hyphenation vs live literal (minor) —
   ACCEPTED.** `silver_lineage_gate` bound to the live literal
   `"source_backed_complete"` (`silver_lineage.py:46`).

**Hunk dispositions:** hunks 1–4 accepted (applied by the CA to the single
target file, wording-aligned). **Hunk 5 rejected** — it rewrote the target's
original direction_change_propagation receipt; receipts are append-only
history, so the amendment carries its own appended receipt instead.

## CA closure checks (gate discharge)

- **Byte/scope check:** the delegate's diff was confined to the single
  commissioned target; the CA applied the accepted hunks itself, so the
  applied delta touches only the target contract (+ this report).
- **Class sweep (F4's leak class, token drift):** repo-wide sweep for the
  hyphenated token found it in literal position ONLY in the target's
  `selection_policy_versions` (fixed). Remaining occurrences are prose
  adjectives or the already-correct code constant
  (`SOURCE_BACKED_COMPLETE_STATUS`) — no further class members.
- **Class sweep (F1's leak class, ref-granularity):** the incumbent
  `by_mention` view deduplicates record refs by design (it is a reverse-lookup
  index, not a counting readout); the mention-level ref rule binds SoV
  readouts only. No other counting surface exists yet.
- Per the delegated-review-patch overlay, this repo-mode discovery pass plus
  the checks above **discharge the independent-review gate** for the patched
  artifact; no separate post-patch cross-vendor re-scan is required. The named
  residual: a novel cross-vendor-shared leak class outside the swept set
  remains bounded and acceptable below buyer-proof tier.

## Reviewer read-budget audit (as returned)

Target full; seam contract targeted→expanded; Silver Vault targeted→expanded
(header/acceptance); derived-layout targeted; `silver_record.py`,
`transcript_product_lake.py`, `derived_retrieval_views.py` full (short,
controlling); `AGENTS.md` full; extra targeted reads of the extractor, mention
models, lineage helper, and overlay source-of-truth.
