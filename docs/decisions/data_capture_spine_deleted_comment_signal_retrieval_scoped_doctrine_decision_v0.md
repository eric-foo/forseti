# Data Capture Spine Deleted-Comment Signal Retrieval Scoped Doctrine Decision v0

```yaml
retrieval_header_version: 1
artifact_role: Dropped doctrine decision (considered and rejected; do-not-re-open record)
scope: >
  Records owner direction to pursue bounded retrieval of DELETED Reddit comments
  as anonymized market signal, the fenced design for it, and the capture-spine
  hard-stop amendment it would require. Direction and design only; not a build
  authorization, not a contract amendment, not live access.
use_when:
  - Stopping a re-exploration of deleted-comment retrieval on sight (dropped 2026-06-08).
  - Deciding whether and how to build deleted-comment signal retrieval.
  - Checking the consent, anonymization, and erasure posture for that capability.
  - Drafting the architecture contract or DCP receipt that would ratify it.
authority_boundary: retrieval_only
open_next:
  - orca/product/spines/capture/contracts/candidate_intake/data_capture_spine_reddit_candidate_url_intake_crawler_architecture_v0.md
  - docs/workflows/reddit_graph_frontier_b2b_marketing_traversal_record_v0.md
stale_if:
  - The capture-spine no-body/comment hard stop is formally amended (this becomes the ratified record).
  - The owner withdraws the deleted-comment direction.
  - The chosen archive source (PullPush) becomes unavailable, changing feasibility.
```

## Status

Status: `DROPPED`.

Dropped 2026-06-08 by owner decision. The capability (retrieving deleted Reddit
comments as market signal) is **not being pursued**. This file is retained as
the considered-and-rejected record so the idea is dropped immediately rather
than re-litigated if it resurfaces. Do not re-open without the "re-open guard"
conditions below being materially changed.

The original direction (now withdrawn) was: pursue bounded retrieval of deleted
Reddit comments as anonymized, aggregate market signal, fenced as a detachable
capability with a purgeable store. The design sections below are preserved as
the rejected record, not as live direction.

## Why dropped / re-open guard

1. **Poor effectiveness on the only viable public source.** A bounded,
   count-only probe of PullPush (the Pushshift successor) for r/SEO on
   2026-06-08 found: coverage exists historically and the comment tree is fully
   reconstructable, BUT ingestion is frozen at ~2025-05-19 (zero records after
   2025-09-01 or 2026-01-01) -- roughly 13 months stale, no fresh signal -- and
   the actual deleted-body recovery rate is unverified and likely low (about
   half the sampled records carried an author-deleted marker, hinting the
   archive may hold post-deletion state rather than pre-deletion originals).
2. **Cost/benefit fails.** The capability would amend the capture-spine
   no-body/comment-capture hard stop and carry privacy/consent and PDPA
   "deleted is not publicly available" baggage -- a high cost for thin, stale,
   historical-only, recovery-uncertain signal.
3. **Process note.** The probe itself was run as an ad-hoc live external call
   outside the governed source-access path and without the runbook's per-operation
   network-permission discipline. Any future re-exploration must use a governed
   probe method, not an ad-hoc call.

Re-open ONLY if all of these change: a source with fresh (not ~1yr-stale)
coverage AND verified high body-recovery exists; the privacy/consent posture for
deleted (especially self-deleted) content is resolved; and a governed live-probe
path is defined. Absent those, drop on sight.

## Why (signal rationale)

Deleted comments -- especially self-deleted -- carry market signal (what a poster
walked back, what a community reacts strongly to). Retrieval would sample that
signal from third-party archives that ingested comments before deletion.

## Design (fenced capability)

- Anonymize on ingest: keep comment text as aggregate signal; drop author
  identity and the re-identification path (not just the visible handle). Retain
  only engagement features -- the comment's own engagement (score, replies) is
  clean and anonymous; author-level reach (follower/karma) is profile-derived,
  availability-limited for deleted authors, and must be coarse-bucketed (a reach
  tier) so an outlier account cannot be re-identified from a distinctive comment.
  Treat author reach as best-effort only; it is likely often unavailable, so the
  design must not depend on it.
- Context: capture each deleted comment with its comment-tree context (at least
  its parent; ideally the local subtree). A deleted comment in isolation is
  low-signal; meaning comes from what it replied to and what replied to it. The
  tree skeleton comes from the live thread (deleted nodes appear as markers) and
  the archive backfills only the deleted nodes' content. Context comments are
  other users' -- anonymize them too. This widens the capture footprint from one
  comment to a subtree.
- Quarantine: deleted comments live in their own category, sub-split into
  self-deleted (kept; highest signal and highest sensitivity) and mod-removed
  (not needed; drop).
- Modular, two detach levers:
  - detachable engine: the retrieval capability can be switched off without
    touching the core capture path;
  - purgeable store: the quarantined data can be purged on demand.
- Erasure: bulk / container (thread, sub, time-window) purge -- not targeted
  per-person. The store carries no per-author tombstone, so there is no re-id
  surface to maintain or verify. See the resolved decision below.
- Non-canonical store: no promotion, no fixture admission, no Data Capture
  handoff. Modularity must not become a durable dossier.

## Resolved -- erasure granularity (Regime A, anonymous)

Owner-chosen 2026-06-08. The tension was: "anonymize on ingest" vs "honor
targeted per-person erasure" -- the latter needs a re-identification key, the
very linkage anonymization removes. Resolution: **Regime A (anonymous store +
bulk/container purge)**. The store keeps no per-author key, so it is not
personal data at the person level, targeted erasure is neither owed nor
possible, and erasure is served by bulk/container (thread, sub, time-window)
purge. This removes the store-schema/privacy lock-in and the verification
burden.

Per-person linkage (Regime B) is explicitly out of scope for this store. Its
value is analysis/audience surfacing, not the deletion mechanism; if ever
pursued it is separate "surface" work with its own boundary decision, and
deleted-comment data is a weak substrate for it (sparse, pseudonymous,
selection-biased).

## Boundary / amendment required

This capability is capture-side (comment bodies) and AMENDS the capture spine's
no-body/comment-capture and no-user/profile/dossier hard stops for a fenced
class. It is NOT Candidate URL Intake (URL/provenance only) and must not be
folded into it. Ratification requires:

1. an explicit hard-stop amendment in the controlling contract with a DCP
   receipt;
2. the erasure-granularity decision (resolved: Regime A -- anonymous + bulk/container purge);
3. a scoped architecture (source-adapter boundary, store schema, erasure
   mechanism, module fence, consent posture);
4. an effectiveness probe of the archive source for the target scope.

## Legal / consent posture (recorded, not legal advice)

- Public Reddit comments: PDPA publicly-available exception broadly covers
  collection/use without consent.
- Deleted comments: arguably no longer "publicly available," so that exception
  likely does not cover them; self-deleted is the sharpest (the author removed
  it). PullPush does not honor erasure on its own dumps.
- Operator is in Singapore: PDPA is the governing regime, not GDPR; GDPR's
  targeting limb could still apply on a future EU-facing commercial path.
- Mitigations (anonymize + bulk/container purge-on-demand) are the load-bearing
  protection, not a "retrievable means public" argument.

## Non-Claims

Not validation, not readiness, not a build authorization, not a contract
amendment, not live Reddit/archive access, not Source Capture Packet output, not
Data Capture handoff, not fixture admission, not legal advice, not commercial
authorization.
