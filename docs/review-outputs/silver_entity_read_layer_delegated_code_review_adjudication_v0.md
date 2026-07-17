# Silver Entity Read Layer Delegated Code Review Adjudication v0

```yaml
retrieval_header_version: 1
artifact_role: Chief Architect review adjudication record
scope: >
  Adjudication of the cross-vendor delegated code review-and-patch return for
  the Silver entity read layer (PR #1031), plus the owner-ratified identity
  hardening folded into the same landing batch.
use_when:
  - Checking what was kept from the DRL-001..DRL-004 delegate working-tree patch.
  - Checking why by_creator moved to schema v2 in the same batch.
stale_if:
  - A later adjudication supersedes this record.
authority_boundary: retrieval_only
reviewed_by: OpenAI GPT-5 Codex (openai-gpt-5-codex)
authored_by: Claude Fable 5 (claude-fable-5)
adjudicated_by: Claude Fable 5 (claude-fable-5), home Chief Architect
```

## Commission And Target

- Commission: `docs/prompts/reviews/silver_entity_read_layer_repo_delegated_code_review_and_patch_prompt_v0.md`.
- Reviewed diff: `039171df173dbeedc9ed8cba6ec183b8ecee7219...ca3b8c3a10a5d5fe91bddc1431bae80f7565bd2f`.
- Delegate report: `docs/review-outputs/adversarial-artifact-reviews/silver_entity_read_layer_delegated_code_review_v0.md` (verdict `issues_found`, 3 major + 1 minor, all patched in the working tree, no scope breach, lifecycle hard stop observed).
- Author vendor: Anthropic. Controller vendor: OpenAI. De-correlation bar: `cross_vendor_discovery`, satisfied.

## Verification Before Adjudication

- The report-embedded diff was compared against the actual working tree:
  identical after per-line trailing-whitespace normalization; the only
  differences were stripped trailing spaces on blank unified-diff context
  lines (a Markdown transcription artifact, content-neutral).
- Independent re-run of the focused view suite plus the inventory,
  reader-selection, and policy-pin contract gates: exit 0 (42 tests).
- Independent full harness suite after adjudication and the folded identity
  hardening: exit 0. Doc gates 23/23.

## Finding Adjudication

### DRL-001 — normalized substring matching can route the wrong brand or line

Decision: accepted and kept as patched. Exact normalized brand / line /
combined-identity matching is the correct lookup contract; the `grand` →
`Ariana Grande` red-green regression proves the misrouting class is closed.
The deliberate loss of fuzzy lookup is an acceptable residual; any future
fuzzy search is a separately governed disambiguation design.

### DRL-002 — incomplete or tampered generated view pairs served as successful data

Decision: accepted and kept as patched. Fail-closed manifest-pair, identity,
schema, and `view_sha256` verification plus honest 0/1/2 exit mapping
(unbuilt or invalid views exit 2, never "entity absent") matches the
generated-read-model obligation. Hash verification detecting tampering but
not staleness is a correctly stated residual — freshness stays with
`stale_if` and prove-rebuildability.

### DRL-003 — native product identity fabricated from partial rows or split across conflicting keys

Decision: accepted and kept as patched. No fabricated `unknown` brand;
rows missing brand or line are residual-only; one native
`(anchor, source site, site id or canonical URL)` identity binds once and
conflicts become named residuals; contributing refs stay manifest-visible.

### DRL-004 — conflicting account aliases silently collapsed

Decision: accepted and kept as patched, then extended: the same batch
promotes the record-asserted identity kind into the by_creator card key
(schema v2), which removes the strongest silent-merge class entirely; the
delegate's `account_alias_conflict` residual (now carrying `identity_kind`)
remains the guard for contradictions within one key.

## Folded Identity Hardening (owner-ratified 2026-07-17)

Adjudicated into the same landing batch, per the owner-approved plan:

1. by_creator schema v2: card key is `(platform namespace, asserted identity
   kind, native id)`; `unspecified` when unasserted; distinct kinds never
   merge.
2. Unfileable account-describing subject shapes are named residuals
   (`unrecognized_account_subject_shape`, `unrecognized_platform_namespace`)
   — a wiring gap is always distinguishable from "not captured".
   `public_comment` remains a known non-account subject.
3. Native product-page identity sources are a closed in-code registry
   (`NATIVE_PRODUCT_PAGE_SOURCES`), Fragrantica sole entry.
4. Platform namespaces are a closed vocabulary
   (`KNOWN_PLATFORM_NAMESPACES = {instagram, tiktok, youtube}`), exact
   lowercase canonical, matching the Reddit venue registry posture.

## Review Use Boundary

The delegate's findings were decision input only — not approval, not
validation, not mandatory remediation, and not patch authority. Each finding
and working-tree hunk was kept only through this Chief Architect adjudication;
this record likewise grants no readiness, approval, or lifecycle authority
beyond documenting what was adjudicated and kept.

## Residual Risk

- Fuzzy/partial mention lookup is deliberately unsupported (DRL-001 residual).
- View-byte hash verification proves integrity, not freshness (DRL-002 residual).
- A creator whose records assert no identity kind files under `unspecified`;
  joining a handle-keyed card to an id-keyed card remains deferred to a
  record-asserted, time-scoped alias policy (recorded trigger).
- Cross-platform identity stays upstream (linkage ledger); the by_creator
  linked-cards overlay is a recorded trigger, not built.
