# IG Reels Deep-Capture Anchoring — Owner Decision Input (v0)

```yaml
retrieval_header_version: 1
artifact_role: Operational decision-input record (docs/workflows/)
scope: >
  The owner decision the IG-reels seam-migration unit prepares but does not
  execute: what to do about the deep-capture route's shortcode anchoring —
  the structural fact that its silver record sets have NO committed bronze
  packet behind them, which orphans every downstream product-mention record
  (15 today) outside by-key discovery and outside the consumption seam.
  Presents the evidence, the three disposition options with their real
  constraints, and an advisory ordering. The owner decides; nothing here is
  executed.
use_when:
  - Deciding the disposition of the deep-capture route and its 15 legacy
    shortcode-anchored product-mention records.
  - Checking why IG deep-capture evidence is invisible to SoV readouts and
    every other availability-walking consumer.
stale_if:
  - The owner decides a disposition (record it as a decision artifact; this
    input is then consumed).
  - The deep-capture writer's anchoring changes.
  - New deep-capture batches materially change the orphan counts.
authority_boundary: retrieval_only
non_claims:
  - not a decision, not validation, not readiness; no disposition is executed
  - counts are the 2026-07-03 eval substrate; rerun the eval for fresh numbers
```

## The structural fact

`write_reel_deep_capture_into_lake` persists each reel's deep capture
(audience comments + ASR transcript) as a derived record set anchored on the
**reel shortcode** (`append_record_set(raw_anchor=result.reel_shortcode, ...)`,
`orca-harness/source_capture/ig_reels_deep_capture_lake.py`). No bronze packet
is ever written for a deep-capture render — the transient signed media URL is
deliberately not preserved, and neither are the audio bytes. Consequently:

- The shortcode anchors are **not committed availability**. By-key discovery
  (`DataLakeRoot.list_available`) — the storage contract's single discovery
  authority — never surfaces them.
- Seam pickup is defined over committed availability only (consumption seam
  contract), so the deep-capture route **structurally cannot ride the seam**:
  there is no committed anchor to fingerprint or acknowledge. The 2026-07-03
  seam-migration unit therefore migrated only the packet-backed route and left
  the deep-capture route on marker-based discovery, explicitly documented and
  never acked (no ack is written under a non-committed anchor).
- Every downstream product-mention record extracted from a deep-capture
  transcript inherits the shortcode anchor and is invisible to every
  availability-walking consumer: the SoV readout, the extraction-quality eval's
  in-scope substrate, and any future by-key metric view.

## Evidence (2026-07-03)

- Extraction-quality eval, finding F3
  (`docs/workflows/sov_extraction_quality_eval_report_v0.md`): **15 of 46
  on-disk mention records** are shortcode-anchored orphans (14 distinct
  shortcode anchors, e.g. `DF3CdyJv79A`) — outside committed availability,
  invisible to by-key consumers.
- The same 15 records hold **all** `captured_at` values observed on disk
  (F4): the orphans carry the only window-timing evidence the substrate has.
- The records are NOT unreadable or wasted: the shortcode-keyed behavioral
  projection (`source_capture/ig_reels_behavioral_lake.py`) reads them today
  by walking derived lanes directly. The blindness is specific to by-key
  discovery and therefore to metrics/seam consumers.

## Options

**A — Re-architect deep capture to commit a bronze packet per render
(forward fix).** The deep-capture runner writes a source-capture packet per
reel (preserved files: capture metadata, comments evidence, transcript cues;
optionally the rendered audio bytes if retention is acceptable) and anchors
the derived record set on the packet id. The route becomes seam-eligible and
future work is by-key visible. Cost: a capture-lane build unit (writer +
runner + tests + spec delta); does nothing for the 15 legacy records by
itself (pair with B or C for legacy).

**B — Backfill the 15 legacy records under committed anchors.** Two honest
sub-shapes: (B1) re-render the reels that are still publicly live through the
option-A packet path and retire the legacy records (fresh evidence, correct
anchors; loses nothing except reels that have since disappeared); (B2) write
retroactive metadata-only bronze packets from the surviving derived records.
Constraint on B2: the raw media was never preserved, so a backfilled packet
cannot carry source bytes — it would be bronze-by-position, not
bronze-by-evidence, and inherits weaker provenance permanently.

**C — Accept as out-of-lake-scope for metrics (documented residual).** The
records stay consumable by the shortcode-keyed behavioral projection; they
never enter by-key metrics. Cheapest; permanent blind spot — including the
only `captured_at` timing evidence currently on disk — and the blind spot
GROWS with every future deep-capture run while the route keeps its current
anchoring.

## Advisory ordering (not a verdict)

A (forward fix) first, with C as the explicit interim for the legacy 15 until
a re-render pass (B1) is worth its capture cost; B2 (metadata-only backfill)
is the weakest shape and worth taking only if the provenance downgrade is
consciously accepted. Rationale: A stops the orphan class from growing and is
the only option that makes the route seam-conformant; B1 upgrades legacy
evidence honestly; C alone leaves a growing hole under any future IG
monitoring. The choice interacts with the pilot-cohort decision: an IG pilot
cohort would need option A first, or its deep-capture evidence never reaches
the SoV denominator.

## What the seam-migration unit already did (context, not a choice)

Packet-backed route (committed `ig_reels_audio` packets) now rides the
consumption seam: obligation-fingerprint pickup, append-only acks under
`silver__cleaning__product_mentions`, acked-and-unchanged packets skipped
without raw loads. Deep-capture route unchanged and documented out-of-seam;
tests pin that no ack is ever written under a shortcode anchor.
