# Batch 0 Review-Economics Receipts

`historical_closed` on 2026-07-17.

This directory preserves the receipts filed during Batch 0. A final
pre-retirement tracker run observed 13 valid receipts and no schema errors. The
counter and notification automation were then retired.

Do not add new Batch 0 receipts. Files beginning with `_` are preserved
examples, not counted evidence.

Historical counting rules were:

- `status` and `ca_adjudication_status` must both be `completed`.
- `material_review` must be `true`.
- `review_id` and `review_report_path` must each be unique across the sample.
- `review_report_path` and every `evidence_pointers` entry must exist in the repository.
- `reviewed_by` and `authored_by` may be `unrecorded`; never fabricate them.
- Invalid or duplicated receipts fail validation and do not count.
- A single malformed or duplicated receipt anywhere in this directory zeroes
  the entire `completed_count`, not just its own slot — this is deliberate
  fail-closed behavior, not partial exclusion. If `--json` reports
  `completed_count: 0` unexpectedly, check `errors` before assuming no
  receipts have landed.
- `status`, `material_review`, and `ca_adjudication_status` are self-reported
  by the filer; the validator checks shape and pointer existence only, not
  that adjudication genuinely occurred. Treat the sample as a measurement of
  filed receipts, not an independently verified one.

The corpus is process-measurement evidence only. It creates no future receipt,
validation, counting, or notification obligation.
