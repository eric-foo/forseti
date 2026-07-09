# Capture Spine

```yaml
retrieval_header_version: 1
artifact_role: Spine front-door
scope: Retrieval-only entry point for the legacy Capture spine product corpus and live harness adjacency.
use_when:
  - Starting capture, source-access, source-family, packet, or obligation work.
  - Choosing between Capture product doctrine and forseti-harness implementation files.
  - Checking whether a source-access task is authorized or only planned.
authority_boundary: retrieval_only
open_next:
  - docs/workflows/forseti_repo_map_v0.md
  - docs/workflows/data_capture_spine_consolidation_map_v0.md
  - forseti/product/spines/capture/core/source_capture_toolbox/README.md
  - forseti/product/spines/capture/core/contracts/obligation_contracts/core_spine_v0_data_capture_spine_obligation_contract_v0.md
  - forseti/product/spines/capture/core/operating_model/data_capture_harness_operating_model_architecture_v2.md
  - forseti/product/spines/capture/core/packet_schema
stale_if:
  - The Capture spine corpus migrates from forseti/product/ into forseti/product/.
  - The Data Capture consolidation map is superseded.
  - The legacy forseti-harness runtime root is migrated or replaced.
```

## Load Order

1. Open the Forseti repo map for identity and legacy-root posture.
2. Open the Data Capture consolidation map for detailed route selection.
3. Open the Source Capture Armory README for source-access tooling, packet
   boundaries, implemented components, and hard stops.
4. Open the obligation contract before changing capture obligations or handoff
   vocabulary.
5. Open the operating model only when capture-lane workflow shape is
   load-bearing.
6. Inspect `forseti-harness/` only after the product route shows implementation is
   in scope and the target runtime file is known.

## File Classes

| Class | Files | Use |
| --- | --- | --- |
| Route map | `docs/workflows/data_capture_spine_consolidation_map_v0.md` | Detailed Capture route selection. |
| Source access / Armory | `core/source_capture_toolbox/README.md` | Source-access tooling, packet, adapters, and implemented component status. |
| Contracts | `core/contracts/**` | Capture obligations, candidate/corpus intake, source boundaries. |
| Operating model | `core/operating_model/**` | Capture workflow architecture and lane history. |
| Source families | `core/source_families/**` | Instagram, YouTube, Retail/PDP, and other source-family rules. |
| Harness implementation | `forseti-harness/**` | Legacy runtime files after implementation is explicitly authorized. |

## Boundary

This is a legacy physical path under `forseti/product/`. It does not authorize live
capture, broad crawling, anti-blocking, API use, storage, dashboards,
production runtime, ECR, Cleaning, Judgment, or buyer proof. Use `forseti-harness/`
only for live harness files until a separate migration creates a replacement.
