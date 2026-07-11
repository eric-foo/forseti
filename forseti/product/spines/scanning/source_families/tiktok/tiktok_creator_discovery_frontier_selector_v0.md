# TikTok Creator Discovery Frontier Selector v0

```yaml
retrieval_header_version: 1
artifact_role: Product architecture contract (scanning source-family helper)
scope: >
  Defines the advisory helper that ranks next TikTok creator-discovery targets
  from existing discovery frontier registers without becoming a validator,
  crawler, metric model, registry intake rule, or live-capture authorization.
use_when:
  - Choosing the next bounded creator profile to scout from TikTok suggested-account registers.
  - Comparing a newly captured suggested-account packet against prior frontier memory.
  - Avoiding repeated scans of already-graphed high-frequency suggested hubs.
authority_boundary: retrieval_only
open_next:
  - forseti/product/spines/scanning/source_families/tiktok/tiktok_creator_discovery_frontier_register_v0.md
  - forseti/product/spines/scanning/source_families/tiktok/tiktok_creator_discovery_enforcement_placement_v0.md
stale_if:
  - A dedicated graph database or scheduler becomes authorized.
  - Creator Registry adopts a first-class weak-edge intake lane.
  - The selector is promoted from advisory helper to enforced runner behavior.
```

## Status

Status: `ADVISORY_HELPER_MGT_FRONTIER_ADAPTER`.

The helper lives under
`forseti-harness/capture_spine/tiktok_creator_discovery_frontier/frontier_selector.py`.
It is not a source capture runner, validator, graph database, ranking model,
registry mutation path, or execution authorization.

## Behavior

The selector consumes only caller-supplied TikTok Creator Discovery Frontier
register mappings. It does not glob filesystem paths, launch browsers, read
TikTok, mutate registers, or decide which historical artifacts are canonical.

It returns:

- an advisory next-target list;
- each candidate's prior suggested frequency across distinct scanned roots;
- the roots and observed sections that exposed the candidate;
- whether the candidate is once-only;
- whether the candidate came from an expanded suggested surface such as
  `View all`;
- whether the handle or display name contains a fragrance-domain token;
- a transparent score and recommendation tier;
- a non-claiming overlap summary for a current register versus prior registers.

## Selection Semantics

The early scouting preference is:

1. prioritize once-only, fragrance-like, expanded-tail candidates;
2. consider candidates seen from two roots;
3. deprioritize candidates seen from three or more scanned roots as likely
   repeated hubs;
4. exclude handles that are already root seeds in the provided register set by
   default, because those creators have already been graphed as parents;
5. let the caller pass additional `already_scanned_handles`.

This is a duplicate-pressure heuristic, not creator quality. It is meant to
answer "what should we scout next to discover fresher adjacent candidates?"
rather than "which creator is good?"

## Non-Claims

- Not capture execution authorization.
- Not source-access authorization.
- Not Creator Registry identity proof.
- Not country/region evidence.
- Not metric rollup.
- Not account quality or roster readiness.
- Not evidence that a candidate is small, large, US-based, or cross-platform
  matched.
- Not a standing crawler, scheduler, queue, or monitor.
