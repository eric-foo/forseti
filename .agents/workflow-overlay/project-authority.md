# Project Authority

```yaml
retrieval_header_version: 1
artifact_role: Forseti overlay authority
scope: Forseti project identity, stage, boundary, relationship to jb, and unknown facts.
use_when:
  - Checking Forseti project identity, stage, boundary, or relationship to jb.
  - Confirming a project fact before filling it from defaults.
authority_boundary: retrieval_only
```

## Identity

- Project/workspace: Forseti
- Legacy name: Orca; rename policy: `docs/decisions/forseti_rename_migration_policy_v0.md`
- Stage: bounded implementation permitted when explicitly authorized; otherwise docs/decision work remains the default
- Relationship to `jb`: separate workspace; no inherited project authority
- Product/domain purpose: institutional evidence adjudication and decision learning for consequential decisions; terminal market and first wedge are intentionally unselected pending the candidate-universe reset
- Target users/operators: decision owners who must weigh heterogeneous, conflicting, biased, incomplete, or differently timed evidence; exact buyer remains open pending candidate-universe regeneration
- Implementation status: bounded implementations may be authorized by current turn or accepted Forseti decision; source-access tooling first tranche is currently authorized by `docs/decisions/data_capture_spine_source_access_tooling_build_authorization_v0.md`
- Current product thesis source: `docs/decisions/forseti_product_thesis_evidence_adjudication_v0.md` (owner-ratified direction 2026-07-12; supersedes the consumer-demand thesis and beauty-first wedge as current direction)

## Authority Boundary

Forseti owns its project-specific facts, artifact folders, review lanes, validation gates, output contracts, and safety rules. Reusable workflow skills may be used only when they defer project facts to this overlay or fail visibly when the overlay is incomplete.

## Forbidden Drift

- Do not import `jb` project-specific assumptions as Forseti authority.
- Do not turn migration notes into Forseti product requirements.
- Do not create implementation scope from unknown project facts.
- Do not treat installed skills or copied skills as canonical skill source.
