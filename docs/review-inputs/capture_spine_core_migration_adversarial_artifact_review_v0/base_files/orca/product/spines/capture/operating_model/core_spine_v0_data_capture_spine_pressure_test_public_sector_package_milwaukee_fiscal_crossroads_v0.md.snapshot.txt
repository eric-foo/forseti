# Core Spine v0 Data Capture Spine Pressure Test: Public-Sector Package, Milwaukee Fiscal Crossroads

```yaml
retrieval_header_version: 1
artifact_role: Product artifact
scope: Narrow Milwaukee Data Capture pressure test for preserving public-sector bundled-offer structure outside threaded-source capture.
use_when:
  - Checking whether Data Capture obligations preserve public-sector package structure.
  - Distinguishing bundle preservation from Judgment Spine packaging-as-signal inference.
  - Reviewing source gaps before any stronger Milwaukee source-level capture claim.
authority_boundary: retrieval_only
branch_or_commit: 5e999c1
input_hashes:
  - path: docs/product/core_spine_v0_data_capture_spine_obligation_contract_v0.md
    sha256: 4F27F8D2A1099A03FC2E13457502F126DA73009B5E485F5B7B43F994D01128E5
  - path: docs/product/core_spine_v0_data_capture_context_preservation_note_v0.md
    sha256: DE0A5B1FD8C67B715B468FDEFD8B374D8BEF2DD67632AAC9A315ADE4B815427D
  - path: docs/product/core_spine_v0_data_capture_spine_architecture_blueprint_v0.md
    sha256: 102424795FEB30B5380C7A7A6659A31A877DED06125B7165890A3D4E5E1B478B
  - path: docs/product/core_spine_v0_data_and_cleaning_spine_boundary_v0.md
    sha256: 0FCC5DD4048EB3B03B96F644B3EF545D82C6F5EEC212301B4C0F28E34F04B166
  - path: docs/research/judgment-spine/cases/milwaukee-fiscal-crossroads/reveal_readout_v0.md
    sha256: 6C932EFF8F00C9034A23592024F504347CC441EE1D4B8C550B7E3665E869389F
stale_if:
  - Any listed input hash changes.
  - A raw Milwaukee source packet, source map, draft, vote record, memo, or package text is added or promoted.
```

## Start Preflight Receipt

```text
orca_start_preflight:
  agents_read: yes
  overlay_read: yes
  source_pack: custom S0 plus targeted Data Capture Spine and Milwaukee reveal readout sections
  edit_permission: docs-write
  target_scope: docs/product/core_spine_v0_data_capture_spine_pressure_test_public_sector_package_milwaukee_fiscal_crossroads_v0.md
  dirty_state_checked: yes
  blocked_if_missing: AGENTS.md, Orca overlay README, retrieval metadata rule, validation gate rule, named Data Capture source pins, Milwaukee reveal targeted sections
```

Workspace note: the repository was dirty and included modified and untracked files at read time. The source hashes below matched the current-turn pins, but this artifact does not convert modified or untracked inputs into accepted authority.

## Source Context

| Source | Sections read | Git/source status at read time | SHA256 | Use in this pressure test |
| --- | --- | --- | --- | --- |
| `AGENTS.md` | Full project instruction | Tracked, not listed dirty | `59114DFF5D1572CB7003212BBE5BD4B4AE43C18F73366425D4BC1E3FC35BF6DD` | Orca docs-write and overlay binding rule. |
| `.agents/workflow-overlay/README.md` | Full overlay entrypoint | Modified | `C473801F6B7E1883BDD59F35F0B25752DD8636DD04E2A3AA20367CC1A7B10EBC` | Overlay binding and missing-authority behavior. |
| `.agents/workflow-overlay/source-loading.md` | Source-loading rule, start preflight, targeted read protocol, not-proven boundaries | Modified | `A89279A9C546165D8F32C795644563B8AE0AF783F8E039470914A8A259A73415` | Bounded read pack and preflight receipt. |
| `.agents/workflow-overlay/artifact-folders.md` | Accepted folders and product artifact placement | Modified | `A65A950459F4865D9DC5F47437FB8699BFA522D92F9EF273E83CBD28D28755D0` | Confirms `docs/product/` placement. |
| `.agents/workflow-overlay/artifact-roles.md` | Product artifact role and permissions | Modified | `10E506688BF98DF35B6D09DB1E837C429EAE9BC96D62890D545F1E803F2D8A00` | Confirms product artifact docs-write role. |
| `.agents/workflow-overlay/retrieval-metadata.md` | Retrieval header contract | Tracked, not listed dirty | `8380105F1E60D0CD613072B8C69816DC9DC7D33D853A34081949BE6775901C1F` | Header shape and triggered fields. |
| `.agents/workflow-overlay/validation-gates.md` | Current gates and non-claim boundaries | Modified | `129AFD0C6CBAE10B3C49EA44BA08423D66678DDDCC4A5B2807C4D07884D84035` | Completion evidence and no-readiness boundaries. |
| `docs/product/core_spine_v0_data_capture_spine_obligation_contract_v0.md` | Raw Observable Preservation; Related Context Preservation; Bundled-Offer Structure Observables; Capture Failure And Blocker Visibility; Categorical Handoff Sufficiency; Pressure-Test Requirement; Non-Claims | Untracked; hash matched current-turn pin | `4F27F8D2A1099A03FC2E13457502F126DA73009B5E485F5B7B43F994D01128E5` | Primary Data Capture obligation contract under test. |
| `docs/product/core_spine_v0_data_capture_context_preservation_note_v0.md` | Core Context Rule; Bundled Offers And Multi-Term Proposals; Core Vs Satellite Reading; Non-Claims | Modified; hash matched current-turn pin | `DE0A5B1FD8C67B715B468FDEFD8B374D8BEF2DD67632AAC9A315ADE4B815427D` | Context-preservation interpretation of bundled offers. |
| `docs/product/core_spine_v0_data_capture_spine_architecture_blueprint_v0.md` | Core Obligations; Context Preservation; Deferred; Non-Claims | Untracked; hash matched current-turn pin | `102424795FEB30B5380C7A7A6659A31A877DED06125B7165890A3D4E5E1B478B` | Architecture-level placement and deferred runtime boundary. |
| `docs/product/core_spine_v0_data_and_cleaning_spine_boundary_v0.md` | Decision; Layer Rules; Core Vs Satellite; Future Work Boundaries; Non-Claims | Untracked; hash matched current-turn pin | `0FCC5DD4048EB3B03B96F644B3EF545D82C6F5EEC212301B4C0F28E34F04B166` | Confirms Data Capture versus ECR, Cleaning, and Judgment boundaries. |
| `docs/research/judgment-spine/cases/milwaukee-fiscal-crossroads/reveal_readout_v0.md` | Tactical Reads; Reusable Lessons; Non-Claims | Untracked under `docs/research/`; hash matched current-turn pin | `6C932EFF8F00C9034A23592024F504347CC441EE1D4B8C550B7E3665E869389F` | Milwaukee fixture signal: WRS/new-hire pension reform appeared inside a broader state package and packaging mattered to Judgment. |

No contaminated archive bodies were read. No public web research was performed.

## Purpose And Non-Goals

Purpose: pressure-test whether the current Data Capture Spine contract preserves WRS/new-hire pension reform as part of the Milwaukee state package-as-presented, including bundle membership, source framing, dependencies, sequence, and visible packaging cues, without inferring state motive.

This artifact tests the capture obligation need. It does not prove that a full Milwaukee source-level capture has already met that obligation.

Non-goals:

- rerun the Milwaukee Judgment Spine analysis;
- rerun the Reddit/API threaded-source pressure test;
- perform public web research;
- create source maps;
- design Evidence Candidate Record fields;
- design Cleaning transformations;
- design runtime capture, APIs, scrapers, storage, dashboards, tests, automation, or packages;
- infer state motive unless directly source-visible;
- claim buyer validation, repeatability proof, product readiness, feature readiness, implementation readiness, data-pipeline readiness, model-training readiness, source-of-truth promotion, or product-method hardening.

## Case Boundary

This is not a Judgment Spine rerun. The Milwaukee reveal readout supplies a bounded fixture showing why package structure can matter: WRS/new-hire pension reform was discussed as part of a broader state package, and the tactical read treated packaging as a signal.

Data Capture's job is narrower. It must preserve what the source visibly presented: which terms appeared together, how the source framed them, what dependencies or acceptance constraints were visible, what sequence was visible across drafts/votes/memos, and what packaging cues carried meaning.

Judgment may later read packaging as signal or counterparty concession evidence. Capture must not decide that inference, price concessions, recommend negotiation moves, or assert the state's motive as fact.

## Core Finding

The current Data Capture contract appears to cover the Milwaukee pressure-test need at the obligation level. The obligation contract explicitly requires preserving bundled-offer structure for a public-sector deal or counterparty package, including bundle membership, source-visible framing, dependencies, visible packaging cues, and sequence. The context note and architecture blueprint reinforce the same atomic-unit rule: preserve the bundle as presented before term-level extraction.

Milwaukee is useful because it is not another threaded-source fixture. It pressures the contract from a public-sector package/concession angle: flattening WRS/new-hire pension reform into an isolated term would lose why its placement beside revenue authority, oversight, and governance constraints mattered to the later Judgment primitive.

The source-level sufficiency claim remains not proven. The targeted Milwaukee reveal readout sections establish the need for the capture obligation, but they do not provide enough raw source text, package headings, bullet ordering, draft/vote/memo sequence, or dependency language to prove that a full source-level capture would succeed.

## Obligations Tested

| Data Capture obligation | Milwaukee pressure question | Pressure-test result | Boundary |
| --- | --- | --- | --- |
| Raw Observable Preservation | Would capture preserve the state package's own language for WRS/new-hire pension reform rather than Orca's summary of it? | Obligation need confirmed. The contract requires preserving what the source showed or said and separating source claim from Orca interpretation. Source-level performance is not proven because the reveal readout is not raw package text. | Capture may add short context notes, but must not replace source language with interpretation. |
| Related Context Preservation | Would capture keep enough surrounding package context for WRS/new-hire pension reform to be inspected fairly? | Obligation need confirmed. WRS only matters for this pressure test because the reveal readout places it inside a broader state bargain. | Capture should preserve the smallest fair context, not an entire archive or all Milwaukee history. |
| Bundled-Offer Structure Observables | Would capture preserve WRS/new-hire pension reform as part of the package-as-presented, including membership, framing, dependencies, visible packaging cues, and sequence? | Core test passed at the contract level. The obligation contract directly covers public-sector deals and multi-term proposals and says the atomic unit is the bundle as presented. | Capture records observed structure and framing. Judgment decides whether packaging supports a counterparty-concession read. |
| Capture Failure And Blocker Visibility | Would missing raw package text be visible rather than silently flattened? | This artifact records the blocker. The reveal readout can support the obligation need, but not full source-level sufficiency. | Failure is allowed. Silent failure is not. |
| Categorical Handoff Sufficiency | Would ECR, Cleaning, and Judgment receive enough categorical context without re-collecting source history? | The contract requires enough handoff context for later layers to inspect bundle structure and capture limits. This pressure test does not design ECR fields or Cleaning transformations. | Data Capture must not become ECR, Cleaning, or Judgment by stealth. |
| Pressure-Test Requirement | Does Milwaukee add a non-Reddit fixture type? | Yes. Milwaukee tests public-sector package/concession framing rather than threaded forum capture. | This single case does not harden the contract or prove repeatability. |
| Non-Claims | Does the pressure test avoid readiness, validation, and implementation claims? | Yes, by construction. | No acceptance, validation, source-of-truth promotion, product readiness, implementation readiness, or buyer proof is claimed. |

## Milwaukee Package-Structure Pressure Notes

For Milwaukee, Data Capture should preserve the state package as an atomic bundle-as-presented before term extraction. WRS/new-hire pension reform should not be captured only as an isolated pension-policy term if the source presented it inside a broader package.

Minimum capture pressure points:

- Bundle membership: preserve that WRS/new-hire pension reform appeared in the same state package, draft, vote, memo, or negotiation artifact as the neighboring terms visible in source.
- Source framing: preserve whether the source framed WRS/new-hire pension reform or adjacent terms as a concession, requirement, safeguard, restriction, condition, fallback, oversight term, governance constraint, revenue authority, or another source-visible category.
- Dependencies and acceptance constraints: preserve what the source showed as linked, severable, conditional, expiring, fallback-only, or required to be accepted together.
- Sequence: preserve when WRS/new-hire pension reform appeared, changed, moved, or disappeared across drafts, votes, memos, public statements, or negotiations if the source makes that visible.
- Packaging cues: preserve headings, labels, bullet order, nesting, emphasis, table placement, grouping, and proximity where those cues affect inspection.
- Source language: preserve the package's own words for WRS/new-hire pension reform and the state's or city's visible framing when available.

The Judgment primitive is different. Packaging-as-signal asks whether putting a useful mechanism beside constraints changes how a client should evaluate the deal. That is a Judgment read, not a Capture conclusion. Capture should preserve the structure that makes the read inspectable without asserting that the state intended to reveal a preference model or concession price.

## Source Gaps And Not-Proven Boundaries

The targeted Milwaukee reveal readout sections do not contain enough raw source material to prove full capture sufficiency. They show that WRS/new-hire pension reform was treated as inside the broader state package and that package structure mattered to the later read, but they do not expose:

- the raw package text;
- source headings, labels, ordering, tables, or emphasis;
- the complete neighboring term set;
- source-visible acceptance dependencies or severability language;
- draft, vote, memo, or public-statement sequence;
- direct source language for why WRS/new-hire pension reform was included;
- enough raw source evidence to distinguish all source framing from Orca's Judgment interpretation.

Therefore, this artifact can say Milwaukee confirms a capture-obligation need. It cannot say the current contract has been fully source-tested against Milwaukee raw materials, that WRS package structure has been captured adequately, or that the Data Capture Spine is hardened.

## Bottom Line

Milwaukee is a useful non-Reddit pressure-test fixture because it shows why Data Capture must preserve a public-sector package as a package: WRS/new-hire pension reform should remain visibly tied to the state bundle, neighboring constraints, source framing, dependencies, sequence, and packaging cues when those are visible. The obligation is supported; full source-level capture sufficiency is not proven from the reveal readout alone.

## Explicit Non-Claims

- This artifact does not rerun Milwaukee Judgment Spine.
- This artifact does not claim the state had any motive unless directly source-visible.
- This artifact does not decide whether WRS/new-hire pension reform was good, oversight was bad, or any negotiation move was correct.
- This artifact does not prove a reusable rule from Milwaukee.
- This artifact does not prove full Milwaukee source-level capture sufficiency.
- This artifact does not harden, validate, accept, or promote the Data Capture Spine contract.
- This artifact does not create or authorize source maps, ECR fields, Cleaning transformations, runtime capture, APIs, scrapers, storage, dashboards, tests, automation, packages, commits, pushes, PRs, deployment, or proof runs.
- This artifact does not claim buyer validation, willingness to pay, repeatability proof, product readiness, feature readiness, implementation readiness, data-pipeline readiness, model-training readiness, commercial readiness, source-system feasibility, data rights, Core Spine validation, Judgment Spine validation, Evidence Candidate Record completion, Evidence Unit design completion, or source-of-truth promotion.
