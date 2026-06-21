# Source Capture Armory — Weapon & Pipe README Templates v0

```yaml
retrieval_header_version: 1
artifact_role: Product artifact
scope: Reusable README templates for Source Capture Armory components — weapons (capture tools) and pipes (access routes). Each armory component gets one succinct-but-complete README from these shapes.
use_when:
  - Adding or documenting a Source Capture Armory weapon (a capture tool) or pipe (an access route).
  - Checking the standard README shape for an armory component.
authority_boundary: retrieval_only
open_next:
  - orca/product/spines/capture/core/source_capture_toolbox/README.md
  - orca/product/spines/capture/core/source_capture_toolbox/weapon_anti_block_http_ladder_v0.md
  - orca/product/spines/capture/core/source_capture_toolbox/pipe_block_wall_escalation_v0.md
stale_if:
  - The armory component model (weapon vs pipe; welded vs cross-cutting pipe) materially changes.
  - The fires_via cell convention or the data-capture distillation binding's node ids change.
```

## Model

The armory holds two kinds of component, each with its own succinct-but-complete README:

- **Weapon** — a capture *tool* that produces a `SourceCapturePacket` (CapturePacket) (e.g. the anti-block HTTP ladder, cloakbrowser, archive.org, media-asset, reddit old-HTTP).
- **Pipe** — an *access route / surface principle* (e.g. block-wall escalation, an unwalled-surface shortcut). A **welded** pipe — a tool's hardcoded route — is documented inside that weapon's README; a **cross-cutting** pipe — a route that spans weapons — gets its own pipe README.

Recurring access *lessons* are **not** documented here. They become one-line distillation **cells** at a decision node (in the data-capture distillation binding). A README references its governing cell by node id via `fires_via:`; it never restates the firing rule (that would be non-firing prose). `fires_via` node ids are **proposed** until admitted to the binding, which is prepare-only and not yet on `main`.

## Template — Weapon README

```md
# Weapon: <name>
- Purpose: <one line — what it captures>
- Rung / cost: <position on the cost-ordered ladder>
- Input -> Output: <what you give it> -> SourceCapturePacket (<what's preserved>)
- Built-in behavior (code-pole): <deterministic facts the tool enforces by construction>
- Boundaries / non-claims: <what it does NOT do or certify>
- Build status + ref: <implemented? where — main / branch; CA-verified?>
- fires_via: <node:id(s) of cells governing its use>
```

## Template — Pipe README

```md
# Pipe: <name>
- Principle: <one line — the route/surface idea this pipe provides>
- Wall-signature it targets: <the block pattern>
- Pairs with: <weapon(s)>
- Applies / doesn't: <judgment boundary>
- Honest limits: <what it can't promise>
- fires_via: <node:id>
```

## Non-claims

Template + model doc only — not validation, readiness, a firing cell, or a distillation-binding edit. The referenced cells and their node ids are proposed and advisory until admitted to the data-capture binding under its own (owner-gated) authority.
