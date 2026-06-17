# Orca Product Docs

Use this folder for docs-first product artifacts: Core Spine contracts, satellite notes, evidence standards, source maps, product proof plans, decision artifacts, memo substrates, evidence appendices, and executive-deck shape drafts.

Artifacts are organized by lane subfolder per
`docs/decisions/orca_repo_structure_binding_v0.md`: `core_spine/`,
`data_capture_spine/`, `judgment_spine/`, `signal_content/`, `ecr/`,
`product_lead/`, `source_capture_toolbox/`, and the `search/` lane
(demand-signal intelligence, search-led: search/answer-engine surfaces + the
demand-scan/read/gate method, bound by
`docs/decisions/orca_search_product_lane_binding_v0.md`). New product artifacts go
in the matching lane; pre-move paths in historical records resolve via
`docs/migration/repo_structure_phase2_consolidation_v0/moved_paths_index.md`.

Keep the Core + Satellite split explicit:

- Core Spine: market-agnostic evidence mechanics.
- Satellites: decision-specific and domain-specific context.

For the current first-proof direction, see
`docs/decisions/orca_icp_wedge_pricing_first_v0.md` — pricing-first / AI-monetization
beachhead on an outside-in competitive-intelligence engine (chosen, not validated;
decide-vs-confirm test pending). It supersedes
`docs/product/orca_product_lead_first_icp_wedge_decision_v0.md`. The product-proof
corpus (offer hypothesis, buyer-proof packet, proof-lead charter, discovery brief and
prompt) hangs off that wedge.

For Judgment Spine claim boundaries, use
`judgment_spine/judgment_spine_evidence_ladder_architecture_v0.md` to distinguish
Product-Learning, Buyer-Proof, and Judgment-Quality evidence before making
proof, validation, scoring, fixture-admission, or readiness claims.

For Source Capture Armory planning, use
`source_capture_toolbox/README.md` as the product-facing entrypoint. New
Source Capture Armory product docs should live under
`docs/product/source_capture_toolbox/` unless a later migration decision moves
existing controlling artifacts. Existing Data Capture source-access decisions,
method plans, and obligation contracts now live under `data_capture_spine/`
(moved by the Phase-2 consolidation) and are indexed from the armory README and
the moved-paths index.

Do not treat Client 0 `jb` material as core product authority unless a product artifact explicitly promotes the concept as generalizable.
