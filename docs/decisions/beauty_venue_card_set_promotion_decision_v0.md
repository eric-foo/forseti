# Beauty Venue Card-Set Promotion — Owner Decision Record v0

```yaml
retrieval_header_version: 1
artifact_role: Decision record
scope: >
  Records the first promote-on-reuse execution: the trigger fired at beauty's
  third screen (2026-06-11) and the owner promoted the vertical's provenance
  trail into a bounded card-set under the survival ingredients. Takes over
  beauty venue scope from the registry rejection record per that record's own
  stale_if; the rejection stands unchanged for every other vertical.
use_when:
  - Checking why a beauty venue card-set exists despite the registry rejection.
  - Reading the card-set's binding parameters (owner, cap, review cadence, delivery).
  - Deciding a future vertical's promotion (this is the precedent shape).
authority_boundary: retrieval_only
open_next:
  - orca/product/satellites/beauty/beauty_venue_card_set_v0.md            # the promoted artifact
  - docs/decisions/orca_venue_registry_rejection_decision_v0.md    # the standing rejection (other verticals)
  - docs/decisions/beauty_subtle_decision_screen3_ledger_v0.md     # the trigger-firing screen
stale_if:
  - The owner retires or re-scopes the card-set (a later dated decision governs).
  - The card-set fails its survival terms (unreviewed past dates / cap breached) — route back to the owner.
```

## Decision (owner, 2026-06-11, in-thread)

PROMOTED: beauty/personal-care's three-screen provenance trail into a small
owned card-set. Owner acceptance: "i agree with 5 ... best way to proceed and
set up the durable one" — given in direct response to the trigger-firing
section that named the mandatory survival ingredients.

## Trigger Evidence (why this fired legitimately)

Three same-vertical screens on record, each with a provenance block on disk:

1. Batch-1 screen (2026-06-11) — `docs/decisions/judgment_spine_backtest_batch1_ledger_declaration_v0.md` ("Screen Provenance").
2. Proving screen 2 (2026-06-11) — `docs/decisions/venue_procedure_proving_screen_beauty_ledger_v0.md`.
3. Subtle-decision screen 3 (2026-06-11) — `docs/decisions/beauty_subtle_decision_screen3_ledger_v0.md` (trigger-firing screen).

## Bound Parameters (survival ingredients, mandatory)

- Named owner: Eric (sole operator). Accepting this record accepts the review
  obligation below.
- Hard size cap: 12 cards. Adding a 13th requires retiring one first.
- Review date: every card carries `review_by: 2026-12-11` (+6 months);
  amendable per entry by dated note. A card past its review date is a STALE
  HINT and says so.
- Delivery into the screen step: the venue procedure's Step 0 now reads a
  promoted vertical's card-set FIRST (dated amendment applied same turn).
- Scope: beauty/personal-care INCLUDING fragrance-adjacent venues (owner
  affirmed in-thread 2026-06-11: fragrance is adjacent to skincare/makeup and
  in scope).
- Source integrity: every card derives from the three ledgers' provenance —
  no model-memory venues; each card cites its ledger(s).

## What This Is Not

Not a reversal of the registry rejection (which stands for all other
verticals), not a general atlas, not a monitor, and not validation of any
venue's current state — cards are dated hints with review dates, fail-soft.
The card-set is the house's ONE deliberately-maintained venue asset, bounded
by the ingredients above; if its survival terms fail, this record's stale_if
routes the question back to the owner rather than letting it rot silently.

## Propagation

Surfaces updated this turn: the card-set artifact (created); the venue
procedure (dated delivery amendment); this record. The registry rejection
record is untouched — its own stale_if anticipated exactly this record taking
over the vertical's scope. Repo-map registration deferred (shared file carries
another lane's uncommitted edits; hygiene routing).
