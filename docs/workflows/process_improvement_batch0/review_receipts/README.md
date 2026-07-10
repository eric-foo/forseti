# Batch 0 Review-Economics Receipts

This directory contains one JSON completion receipt per material adversarial
review after Chief Architect adjudication. Files beginning with `_` are examples
and are ignored by the counter.

Before committing a receipt, copy `_template.json`, choose a descriptive unique
filename, fill every field, and run:

```powershell
python .github/scripts/batch0_process_tracker.py --json
```

Counting rules:

- `status` and `ca_adjudication_status` must both be `completed`.
- `material_review` must be `true`.
- `review_id` and `review_report_path` must each be unique across the sample.
- `review_report_path` and every `evidence_pointers` entry must exist in the repository.
- `reviewed_by` and `authored_by` may be `unrecorded`; never fabricate them.
- Invalid or duplicated receipts fail validation and do not count.

The tenth valid receipt merged to `main` makes the sample notification-eligible.
The workflow creates exactly one historical issue titled
`Batch 0 review sample reached 10 completions` and assigns/mentions the repository
owner. A pre-existing exact-title issue prevents a duplicate notification.
