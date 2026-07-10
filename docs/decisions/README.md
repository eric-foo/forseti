# Decisions

Store Forseti decision records here. Use explicit status vocabulary such as `DRAFT`, `PROPOSED_LOCK`, `LOCKED`, `DEFERRED`, or `SUPERSEDED` when a decision needs lifecycle tracking.

Find decisions through the router, not by scanning this folder:

- `docs/decisions/forseti_doctrine_index_v0.md` — doctrine index (router, not authority): one place to find every binding doctrine across kernel, overlay, decision records, and product lanes.
- `docs/decisions/dcp_receipts_archive_v0.md` — verbatim archive destination for doctrine-change-propagation receipts rotated out of overlay and product files.
