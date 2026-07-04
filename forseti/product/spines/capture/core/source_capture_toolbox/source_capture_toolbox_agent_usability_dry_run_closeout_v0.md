# Source Capture Armory Agent Usability Dry Run Closeout v0

```yaml
retrieval_header_version: 1
artifact_role: Product artifact
scope: Closeout note for the Canoo/Walmart Source Capture Armory agent-usability dry run.
use_when:
  - Checking what the first fresh-agent Source Capture Armory dry run proved.
  - Distinguishing armory agent usability from source-quality improvement.
  - Deciding whether to patch the runbook, rerun a source-quality pass, or scope a next adapter.
authority_boundary: retrieval_only
open_next:
  - forseti/product/spines/capture/core/source_capture_toolbox/README.md
  - orca-harness/docs/source_capture_agent_runbook.md
  - docs/research/judgment-spine/cases/canoo-walmart/case_index.md
  - docs/research/judgment-spine/harness/v0_14/fixtures/canoo_walmart_2022_v0_14/source_acquisition_receipt_v0.md
stale_if:
  - The Source Capture Armory runner set materially changes.
  - The source-capture agent runbook materially changes runner selection, output reporting, or generated-packet lifecycle.
  - A later dry run supersedes this Canoo/Walmart dry-run result.
  - A later fixture-admission or source-quality decision admits generated packet outputs as durable evidence.
```

## Status

Status: `SOURCE_CAPTURE_ARMORY_AGENT_USABILITY_DRY_RUN_CLOSEOUT_V0`.

This closeout records the first bounded fresh-agent dry run of the Source
Capture Armory against the Canoo/Walmart case. The run tested whether an agent
could use the existing runbook and runners to produce inspectable packets and
report visible limitations.

## What It Proved

The dry run supports a narrow agent-usability claim:

- the local-file runner could package an already-local Canoo/Walmart source
  capture into a Source Capture Packet;
- the Direct HTTP runner could preserve one supplied public source URL after
  visible per-operation network escalation;
- the Archive.org runner could write a packet preserving failed archive
  availability/body posture rather than pretending body-capture success;
- the fresh executor used supplied inputs, inspected `manifest.json`,
  `receipt.md`, and `raw/`, avoided alternate-source search, and carried
  limitations forward.

This is a armory-usability win, not a source-quality win.

## What It Did Not Prove

The run did not prove historical source identity, source completeness, source
meaning sufficiency, fixture admission, participant-packet readiness, Judgment
quality, ECR receipt, Cleaning output, scoring, buyer proof, or commercial
readiness.

The generated packet directories were scratch dry-run outputs under
`orca-harness/_test_runs/`. They are not admitted fixtures or durable evidence
unless a later owner decision explicitly admits them.

## Dry Run Observations

Local-file packet:

- status: succeeded;
- packet written with one preserved local HTML file;
- no limitations were recorded, but manifest postures still needed to be read.

Direct HTTP packet:

- status: succeeded after per-operation network escalation;
- first sandboxed attempt reported `WinError 10061`;
- packet preserved response body and HTTP metadata.

Archive.org packet:

- status: completed with packet limitations after rerun using valid cutoff
  timestamp `20220701000000`;
- packet preserved availability metadata only;
- limitations recorded HTTP 503 availability/body failure and parse failure;
- no archive snapshot body was preserved.

## Durable Lesson

The dry run exposed two agent-facing runbook gaps that were patched in
`orca-harness/docs/source_capture_agent_runbook.md`:

- Archive.org cutoff timestamps must be exact 14-digit `YYYYMMDDhhmmss` values
  and must not be silently repaired by the agent.
- Agents must report manifest postures even when `limitations` is empty,
  because posture fields can carry current-capture, cutoff, archive, media,
  browser, or access caveats.

## Turning This Into A Source-Quality Win

The next source-quality pass should target one source unit and improve body or
version identity, not merely prove runner operation again.

Smallest complete target:

- choose one Canoo/Walmart source ID, preferably `CW-P1` or `CW-P4`;
- preserve an inspectable source body through the strongest in-bound path
  available for that source: historical archive body if available, otherwise
  current official/source body plus explicit version-identity limitation;
- record source publication/event timing, retrieval timing, cutoff posture,
  archive/history posture, access posture, and preserved file hashes;
- report whether the source-quality state improved from current/live or
  metadata-only posture to inspectable body posture;
- keep any failure as a visible limitation rather than switching methods
  silently.

This later pass should be scoped as source-quality improvement, not as another
agent-usability dry run.

## Next Authorized Step

If the goal is armory closure, commit the runbook lesson and this closeout.

If the goal is source-quality improvement, scope a single-source Canoo/Walmart
source-quality pass that attempts to upgrade one source from current/live or
archive-metadata posture to inspectable source-body posture.

## Non-Claims

- Not validation.
- Not readiness.
- Not source completeness.
- Not historical archive proof.
- Not fixture admission.
- Not participant-packet readiness.
- Not Judgment quality.
- Not ECR, Cleaning, or scoring.
- Not Reddit API authorization.
- Not buyer proof.
- Not commercial-readiness evidence.
