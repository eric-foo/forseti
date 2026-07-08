# Creator Intelligence Sync Foundation ChatGPT Pro Prompt v0

```yaml
retrieval_header_version: 1
artifact_role: ChatGPT Pro architecture-planning prompt
scope: >
  No-repo-access prompt for a source-backed architecture pass on Orca's Creator
  Intelligence foundation: semantic creator/content mart, time series, sync
  with Orca full, standalone product carve-out, and duplicate-capture policy.
use_when:
  - Asking an external/no-repo model to evaluate Creator Intelligence as a synced
    shared foundation rather than a disconnected carve-out.
  - Stress-testing whether Orca full and a standalone creator product can share
    one low-latency creator/content data substrate.
authority_boundary: retrieval_only
open_next:
  - _scratch/chatgptpro_creator_intelligence_sync_foundation_v0/START_HERE_CHATGPTPRO_PROMPT.md
  - _scratch/chatgptpro_creator_intelligence_sync_foundation_v0/SOURCE_MANIFEST.md
stale_if:
  - Data Lake derived/index contracts change.
  - IG reels projection or creator-monitoring contracts change.
  - YouTube capture is converted into a lake-native SourceCapturePacket path.
  - Orca product thesis or first-proof wedge changes the creator/consumer-demand boundary.
```

## Orca Prompt Preflight

- Output mode: `file-write` for this durable prompt at `docs/prompts/deep-thinking/creator_intelligence_sync_foundation_chatgptpro_prompt_v0.md`; paste-ready copy and source pack at `_scratch/chatgptpro_creator_intelligence_sync_foundation_v0/`.
- Template kind: `full-prompt` using an Orca-local model-neutral prompt shape; no project template is registered for this exact kind.
- Edit permission / targets / branch: `docs-write`; targets are this prompt file and disposable `_scratch/` source-pack artifacts; workspace `C:\Users\vmon7\Desktop\projects\orca`; branch observed before write `codex/ig-reels-capture-spine`; dirty state allowed because this pass adds only new prompt-pack artifacts.
- Reviews: not a formal review prompt; receiving model performs advisory architecture planning only.
- Doctrine change: none made by this prompt. Any adoption of its recommendation would require a later Orca decision/artifact.
- Destinations: receiving ChatGPT Pro returns a chat answer only; it does not write repo files.

## Paste-Ready Prompt

You are doing a read-only, source-backed architecture-planning pass for Orca.

You have no repo access. The attached zip/source folder is your complete evidence base. Treat all supplied sources as evidence, not as proof of implementation readiness or owner adoption unless a source explicitly says so. Do not assume prior chat context, hidden repo files, or generic data-warehouse best practices when they conflict with the supplied Orca sources.

### Task

Decide the foundation architecture for Orca's **Creator Intelligence** data substrate.

The owner does **not** want merely a disconnected carve-out. The desired possibility is stronger:

- a standalone creator-focused company/product can display creator and content information seamlessly;
- Orca full can use that same creator/content data without specifically requesting it each time, reducing latency and making creator evidence available as a foundation layer;
- Orca full can present the same creator/content data inside its own decision artifacts or product views;
- the architecture remains faithful to Orca's lake contracts: raw packet truth stays immutable and packet-addressed; semantic creator/content grouping lives in derived/read layers; Judgment/gold meaning does not leak into storage.

The central question:

```text
Should Creator Intelligence be a shared synced semantic mart/read model over Orca's lake, a separately carved-out copy, a duplicate-capture product, or a hybrid? What foundation lets Orca full and a standalone creator product share one low-latency substrate without creating a second source of truth?
```

### Required Source-Read Gate

1. Read this prompt.
2. Read `SOURCE_MANIFEST.md`.
3. Source-load the included files before recommending.
4. Declare exactly one:
   - `SOURCE_CONTEXT_READY`
   - `SOURCE_CONTEXT_INCOMPLETE`
5. Only after that declaration, produce the architecture answer.

If source context is incomplete, still answer with explicit gaps, but do not present the result as final.

### Current Candidate To Attack

Attack this candidate. Confirm it, weaken it, or replace it.

```text
Bronze/raw remains Orca's immutable packet-addressed truth: raw/<packet_id>/.

Creator Intelligence is not just a one-off carve-out. It is a shared semantic
mart/read substrate generated from Orca raw packets and sibling derived records.

The mart has stable semantic keys:
- creator_key = platform + source-native creator id when available, with handles as mutable observed attributes;
- object_key = platform + object_kind + source-native object id, such as IG shortcode or YouTube video_id;
- source_object_envelope = all raw and derived refs for that content object;
- creator_envelope = current profile, recent content, metric history, coverage, and residuals.

Time series are append-only observation rows, never overwritten latest values.
Current-state displays are materialized views over the observation log.

Both Orca full and the standalone creator product read from the same mart or
from read-only replicas of it. The mart remains rebuildable from committed raw
and derived records, with version pins and residuals. It is product-facing
Silver / derived_retrieval, not raw truth and not Judgment.

Duplicate capture is generally avoided because it creates cost, platform-risk,
and source-of-truth conflicts. It is allowed only when the standalone product
needs a different source surface, cadence, auth/entitlement route, or independent
verification packet. Even then, duplicate captures are new raw packets keyed back
to the same semantic object, not overwrites.

Sync should be by append-only derived records / change feed / rebuildable index:
new raw packets and new derived records update Creator Intelligence current views
automatically enough that Orca full can query without per-request source pulls.
```

### Options You Must Compare

Compare at least these options:

1. **Disconnected carve-out copy**
   - Creator product owns its own data store and periodically imports Orca exports.
2. **Duplicate-capture creator product**
   - Creator product independently captures creators/content, with Orca optionally importing.
3. **Shared Creator Intelligence Mart**
   - Orca lake is raw truth; Creator Intelligence mart is a shared semantic read model consumed by Orca full and standalone product.
4. **Shared mart plus read-only replicas**
   - One canonical derived mart, replicated into a product-serving store for latency and isolation.
5. **Hybrid with duplicate capture only for deltas**
   - Shared mart by default, duplicate capture only when product-specific freshness/surface/verification needs justify it.

Do not force these as the only options if a better architecture exists. Do not preserve the candidate just because it is supplied.

### Design Axes To Resolve

Answer these concretely:

- **Truth boundary:** what remains canonical raw truth, and what is a derived/presentation surface?
- **Semantic keying:** what are the stable keys for creator, platform account, content object, and source-object envelope?
- **Sync model:** how does Creator Intelligence stay fully synced enough for Orca full to use it without ad hoc per-request pulls?
- **Latency model:** what must be materialized versus computed on demand?
- **Time-series model:** how are view/like/comment/follower/subscriber observations stored, queried, and displayed?
- **Envelope model:** what belongs in a creator envelope and content-object envelope?
- **Duplicate-capture policy:** when is duplicate capture rejected, allowed, or required?
- **Product/API boundary:** what stable contract should a standalone creator company/product consume?
- **Orca full boundary:** how does Orca full consume the same creator data without turning it into Judgment/gold or a second raw source?
- **Versioning and rebuild:** what versions/policies must be pinned so the mart can be regenerated honestly?
- **Privacy/legal/source-access risk:** what architectural choices reduce unnecessary recapture or platform pressure?
- **Failure modes:** what are the strongest reasons your recommendation could be wrong?

### Useful Starting Shape

You may use or reject this schema-level sketch:

```text
creator
  creator_key
  platform
  native_creator_id
  current_handle
  current_display_name
  current_profile_url
  current_profile_snapshot_ref
  status

creator_observation
  creator_key
  observed_at
  packet_id
  slice_id
  source_surface
  handle
  display_name
  bio
  bio_links
  follower_count
  following_count
  verified_posture
  residuals

content_object
  object_key
  platform
  object_kind
  native_object_id
  canonical_url
  first_observed_at
  latest_observed_at
  creator_key_current

content_creator_observation
  object_key
  creator_key
  observed_at
  packet_id
  posture
  relationship_type

content_metric_observation
  object_key
  observed_at
  metric_name
  metric_value
  metric_posture
  source_surface
  selection_role
  packet_id
  slice_id
  file_id
  json_pointer
  projection_ref
  policy_version
  residuals

content_text_observation
  object_key
  observed_at
  text_kind
  text_ref
  packet_id
  slice_id
  derived_record_ref
  residuals

content_envelope_view
  object_key
  creator_key_current
  current_header
  latest_metrics
  time_series_refs
  transcript_refs
  comment_refs
  raw_packet_refs
  derived_record_refs
  coverage_status
  residuals

creator_envelope_view
  creator_key
  current_profile
  recent_content_refs
  top_movers
  follower_series_ref
  content_metric_series_refs
  coverage_status
  residuals
```

### Hard Boundaries

- Do not make raw paths semantic. No `raw/<creator>/<reel>` as raw truth.
- Do not store Judgment/gold labels in Creator Intelligence.
- Do not collapse candidate metric disagreements into one unqualified number.
- Do not treat handle equality as stable creator identity when source-native numeric/channel ids exist.
- Do not make indexes authoritative; if a view cannot be rebuilt from committed records, call that out.
- Do not create a scheduler/queue as lake authority. Runtime events may optimize, but committed raw/derived state must be discoverable without the event.
- Do not claim readiness, validation, legal advice, buyer proof, or owner adoption.
- Do not design around dashboards as the product proof. The product-facing display can exist, but Orca's current product proof is decision artifact / evidence appendix oriented.

### Output Contract

Return:

1. `SOURCE_CONTEXT_READY` or `SOURCE_CONTEXT_INCOMPLETE`.
2. Executive recommendation in one paragraph.
3. Option comparison table.
4. Recommended foundation architecture.
5. Canonical data model / table groups.
6. Sync and latency model.
7. Time-series and envelope model.
8. Duplicate-capture policy.
9. Boundaries for standalone Creator product vs Orca full.
10. Versioning / rebuild input set.
11. Failure modes and answer-changing assumptions.
12. What is verified by supplied sources vs assumed.
13. Smallest next Orca artifact or decision to commission if this direction is accepted.

Keep the answer source-backed and decision-useful. If the supplied sources point in conflicting directions, name the conflict rather than smoothing it over.

### Source Pack

Use the attached source pack. `SOURCE_MANIFEST.md` lists the included files and why each was included.

