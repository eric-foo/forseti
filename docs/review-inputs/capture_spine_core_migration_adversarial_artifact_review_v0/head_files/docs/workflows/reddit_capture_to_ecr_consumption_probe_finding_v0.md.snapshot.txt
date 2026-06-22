# Reddit Capture → ECR Consumption Probe Finding v0

```yaml
retrieval_header_version: 1
artifact_role: Workflow finding record
scope: Real-data probe finding — Reddit capture packets ingest into ECR source-agnostically but yield residual (not-proven) postures until source-side postures are supplied.
use_when:
  - Deciding whether and where the Reddit capture path should supply source-side postures (cutoff, publication/event, edit/version) for ECR.
  - Orienting on how Reddit capture output reaches ECR / judgment.
  - Picking up the queued source-side-posture-supply decision or handing it to the ECR lane.
authority_boundary: retrieval_only
open_next:
  - orca-harness/runners/run_reddit_old_http_batch.py
  - orca-harness/ecr/deriver.py
  - orca/product/spines/capture/core/source_capture_toolbox/reddit_capture_operator_playbook_v0.md
downstream_consumers:
  - The source-side-posture-supply decision (gap-vs-by-design) this finding tees up.
stale_if:
  - The Reddit capture path begins supplying a cutoff_posture (or other source-side postures).
  - ECR's source-side deriver contract changes how it reads packet source-slice postures.
```

## Status

`FINDING — advisory`. A real-data probe result plus an open question. Not a decision, validation, readiness, or proof claim.

## What was probed

Whether candidate Reddit data, once captured, is actually *consumed usefully* by ECR (the path toward judgment / buyer-proof): does a Reddit capture packet land in ECR at all, and does it yield a cleared judgment or a residual?

One bounded, owner-authorized probe drove the full chain on real data — a single-thread body capture that lifted the `body-retrieval-default-deferred` posture for that one operation only. Evidence artifacts were gitignored scratch and have been purged; the observed facts are recorded below.

## Observed facts (real data)

- **Discover** (prior live run): candidate URL intake of `old.reddit.com/r/b2bmarketing/` → 10 real candidate thread URLs (HTTP 200).
- **Capture**: `run_reddit_old_http_batch.py` on one real thread → HTTP 200, ~104 KB body, **14 comments** consolidated; a `SourceCapturePacket` (`manifest_version: source_capture_packet_manifest_v1`) written with `source_slices[].timing`.
- **ECR ingestion**: the real packet loaded into `source_capture.models.SourceCapturePacket` (pydantic `model_validate`) **with zero adaptation**, and `ecr.deriver.derive_timing_postures` returned **1 posture**.
- **Result**: that posture is a **residual** — `clears_pre_cutoff=False`, `status=UNKNOWN_WITH_REASON`, `reason="direct HTTP runner did not receive cutoff posture metadata"`.

## Finding

1. **ECR consumes Reddit capture output source-agnostically, with no Reddit-specific wiring.** Confirmed on a real captured packet: same `SourceCapturePacket` type, loads cleanly, deriver runs. There is no capture→ECR *integration* gap.
2. **Reddit captures currently land as not-proven residuals**, because the capture path supplies no source-side postures. In the real packet, every source-side field is `unknown_with_reason` or `not_attempted` (cutoff posture, publication/event timing, edit/version, actor/audience). `run_reddit_old_http_batch.py` passes `cutoff_posture=None`; `run_source_capture_http_packet` accepts a `cutoff_posture` but none is threaded through.

## Resolution (step 2 — by design)

Resolved against the Data Capture Spine obligation contract
(`docs/product/core_spine_v0_data_capture_spine_obligation_contract_v0.md`,
Obligation 9 + the commissioned-capture requirement): **by design.**

Cutoff posture is a first-class *capture* fact, but it is known only for capture
**commissioned against a Decision Frame** — which supplies the decision question,
cutoff posture, and intended downstream use. The contract treats standing or
opportunistic capture as out of scope ("if there is no Decision Frame, Data
Capture Spine has not started"), and Ob.9 prescribes recording `unknown` with a
reason when the posture cannot be stated.

The probe used the bounded *calibration* batch runner with **no Decision Frame**,
so `cutoff_posture` → `unknown_with_reason` → ECR residual is the
contract-prescribed, honest outcome — **not a defect**. The capability exists
(`run_source_capture_http_packet` accepts a `cutoff_posture`); the batch runner
intentionally passes `None`. To obtain *cleared* ECR postures from Reddit, run
commissioned capture against a Decision Frame — a larger owner / judgment-model
question (step 3), not a capture-path fix.

## Boundaries / non-claims

- This is a finding, not a decision, validation, readiness, or proof claim.
- The `body-retrieval-default-deferred` posture **resumes**: the probe was a one-operation lift, now complete; the captured body scratch was purged.
- No source code or capture/ECR contract was changed by this probe.

## Sequenced follow-ups (owner-directed)

1. **Done** — document the finding + wrap the capture lane (committed).
2. **Done** — decide gap-vs-by-design → **resolved by design** (Ob.9 / commissioned
   capture); no capture-path change warranted.
3. **Open** — hand the commissioned-capture / Decision-Frame question (how Reddit
   captures acquire a real cutoff posture for an actual decision) to the ECR /
   judgment-model lane that owns the Decision Frame.
