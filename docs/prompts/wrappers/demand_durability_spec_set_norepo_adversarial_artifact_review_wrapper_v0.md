# Thin Wrapper — Demand-Durability Spec Set No-Repo Cross-Vendor Adversarial Artifact Review

```yaml
retrieval_header_version: 1
artifact_role: Thin wrapper (no_repo cross-vendor adversarial artifact review courier)
scope: Courier prompt that points a repo-blind, cross-vendor reviewer at the in-bundle README for the demand-durability spec-set review.
authority_boundary: retrieval_only
```

- **Source bundle:** `docs/review-inputs/demand_durability_spec_set_norepo_adversarial_artifact_review_bundle_v0/`
- **Reviewer instruction set (full prompt):** the bundle `README.md` (guardrail-complete; carries the method, authority excerpts, per-target contracts, and output contract).
- **Attachments to deliver to the reviewer:** the 5 verbatim spec files (`01_…` through `05_…`) + `README.md`. `MANIFEST.md` is optional (hashes + commission receipt).
- **Who-constraint (operator-owned, NOT in the bundle):** the reviewer must be a **different vendor than Anthropic** (author = claude-opus-4.8); cross-vendor (discovery) bar. This is a commission who-constraint, not runtime model routing — do not let it migrate into the bundle, and the prompt names no model.
- **Output:** advisory `review_summary` + findings, returned in chat (operator couriers back). Reviewer writes no files.

---

## Paste-ready courier (paste into the cross-vendor model; attach the bundle files)

````markdown
You are a repo-blind, advisory-only adversarial artifact reviewer. The formal
review tooling of the authoring environment is not available to you — say so;
your result is advisory critique, not a formal verdict.

Attached is a self-contained review bundle. **Read `README.md` in full and follow
it exactly** — it is your complete instruction set: the five review targets
(`01_…` through `05_…`, attached verbatim), the authority excerpts they must
conform to, the review focus, the fitness reference, and the PORTABLE METHOD you
must follow (reasoning-before-findings, then a compact `review_summary` and
findings ordered critical → major → minor).

First REFERENCE-LOAD the method in the README (do not apply it yet); confirm you
can see all five attachments and the authority excerpts (SOURCE_CONTEXT_READY),
then APPLY the method. Review the envelope-delta (01) first — the four proxy
profiles forward-cite it.

Be maximally adversarial within the five named targets; do not retarget or widen.
Optionally confirm each attachment matches the SHA256 in `MANIFEST.md`. If a
claim depends on a source not in the bundle, label it `unverifiable from provided
sources` rather than assuming. Do not emit executor-ready patch steps; advisory
remediation direction only. Return your `review_summary` + findings in chat.
````

---

*Thin wrapper: does not restate Orca policy. The binding rules live in the bundle
README + MANIFEST. Provenance (`reviewed_by` / `authored_by`) and finding
adjudication are recorded by the Chief Architect on the durable review report
(`docs/review-outputs/adversarial-artifact-reviews/`) on return.*
