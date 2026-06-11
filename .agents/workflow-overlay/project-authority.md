# Project Authority

```yaml
retrieval_header_version: 1
artifact_role: Orca overlay authority
scope: Orca project identity, stage, boundary, relationship to jb, and unknown facts.
use_when:
  - Checking Orca project identity, stage, boundary, or relationship to jb.
  - Confirming a project fact before filling it from defaults.
authority_boundary: retrieval_only
```

## Identity

- Project/workspace: Orca
- Stage: bounded implementation permitted when explicitly authorized; otherwise docs/decision work remains the default
- Relationship to `jb`: separate workspace; no inherited project authority
- Product/domain purpose: outside-in strategic intelligence system for public market signals and evidence-backed allocation decisions
- Target users/operators: companies and teams making product, positioning, pricing, growth, and competitive decisions; `jb` is the first internal Client 0 for method validation
- Implementation status: bounded implementations may be authorized by current turn or accepted Orca decision; source-access tooling first tranche is currently authorized by `docs/decisions/data_capture_spine_source_access_tooling_build_authorization_v0.md`
- Current product thesis source: `docs/decisions/orca_product_thesis_consumer_demand_v0.md` (owner-ratified 2026-06-12; supersedes `turn_08_product_thesis_v0.md`)

## Authority Boundary

Orca owns its project-specific facts, artifact folders, review lanes, validation gates, output contracts, and safety rules. Reusable workflow skills may be used only when they defer project facts to this overlay or fail visibly when the overlay is incomplete.

## Forbidden Drift

- Do not import `jb` project-specific assumptions as Orca authority.
- Do not turn migration notes into Orca product requirements.
- Do not create implementation scope from unknown project facts.
- Do not treat installed skills or copied skills as canonical skill source.
