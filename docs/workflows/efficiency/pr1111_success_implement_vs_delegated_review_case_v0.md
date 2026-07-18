# PR #1111 Success Implement vs Delegated Review Case v0

```yaml
retrieval_header_version: 1
artifact_role: Review-method comparison case and measurement record
scope: >
  Records one prospective within-change comparison between the in-session
  Success Implement review used on PR #1111 and a later strict cross-vendor
  delegated review-and-patch of the same merged diff.
use_when:
  - Aggregating observed Success Implement review outcomes.
  - Deciding whether similar mixed classifier-and-evidence changes warrant a strict delegated patch pass.
  - Adjudicating the delegated return commissioned for PR #1111.
authority_boundary: retrieval_only
open_next:
  - .agents/skills/success-implement/SKILL.md
  - .agents/workflow-overlay/delegated-review-patch.md
  - docs/prompts/reviews/pr1111_kohls_access_diagnosis_delegated_code_review_and_patch_prompt_v0.md
stale_if:
  - A later adjudication changes the recorded AKM-1 or AKM-2 disposition.
```

## Case identity and currentness

This case is current as of **2026-07-19 Asia/Singapore**.

```yaml
case_id: PR1111_SUCCESS_IMPLEMENT_VS_DELEGATED_PATCH_V0
repository: eric-foo/forseti
pull_request: 1111
pull_request_url: https://github.com/eric-foo/forseti/pull/1111
merged_change:
  merge_commit: ab276fca3bdaf2735b6240fa67f089c943526888
  reviewed_head_after_success_implement_patch: 7f2b503237fe7c74077aafd5fac802cf0810fc63
  title: "fix: classify Akamai access denials and record Kohl's gap"
comparison_status: COMPLETE_ONE_UNIQUE_ACCEPTED_MATERIAL_FINDING
```

The unit of comparison is the five-file squash diff at
`ab276fca^..ab276fca`, not the whole repository and not the live retailer
probe process. The later delegate must review that same diff from a clean
worktree pinned to the merge commit. A review of later `main` is not comparable
unless it first isolates this exact diff.

This is one observational case. It does not establish that either method is
generally sufficient, mandatory, cheaper, or better.

## Observed baseline: in-session Success Implement review

The implementation and the in-session reviewer were both from OpenAI model
lineage. The reviewer used the `gpt-5.6-terra` model override in a separate
in-session agent. That is useful reviewer separation, but it does **not**
satisfy Forseti's strict delegated-review de-correlation bar, which requires a
different upstream vendor lineage.

```yaml
baseline_review:
  method: success_implement_in_session_review
  author_vendor: OpenAI
  reviewer_vendor: OpenAI
  reviewer_model: gpt-5.6-terra
  strict_cross_vendor_de_correlation: false
  initial_verdict: PATCH_REQUIRED
  findings_total: 1
  findings_by_formal_severity: not_assigned
  accepted_findings: 1
  rejected_findings: 0
  accepted_patch_required: true
  review_elapsed_time: not_captured
  review_token_use: not_captured
```

The accepted finding was an evidence-boundary overclaim: the results artifact,
pin registry, and recon index treated a wider, unpreserved hostname / AMP /
typeahead / application exploration matrix as supporting an exhaustion
verdict. Only the preserved ordinary Direct HTTP and header-complete HTTP
packets supported the durable anonymous-non-browser exhaustion claim.

The author accepted the finding and narrowed all three evidence artifacts.
The reviewer then returned `PASS` on exact head
`7f2b503237fe7c74077aafd5fac802cf0810fc63`. Required CI was observed green
before the PR was squash-merged. This record does not upgrade that chat verdict
into formal review authority.

## Prospective comparison protocol

The strict delegated pass is commissioned by
`docs/prompts/reviews/pr1111_kohls_access_diagnosis_delegated_code_review_and_patch_prompt_v0.md`.
To reduce anchoring:

1. The delegate reviews the exact five-file diff and freezes Phase A findings
   before reading this case record, PR discussion, commit body, or the prior
   reviewer result.
2. After freezing Phase A, the delegate reads this baseline and maps each
   finding as `overlap`, `unique_to_delegated`, or `baseline_only`.
3. The delegate may then apply only finding-supported edits inside the named
   patch scope and returns the diff for home-lane adjudication.
4. The home Chief Architect records which delegated findings and hunks were
   accepted, modified, or rejected. Delegate-proposed findings are not counted
   as defects until adjudicated.

The comparison records these fields. Use `not_captured` rather than estimates:

| Measure | Success Implement baseline | Delegated return | Adjudicated value |
| --- | ---: | ---: | ---: |
| Findings raised | 1 | 2 | 2 |
| Findings overlapping the baseline | 1 baseline candidate | 0 | 0 |
| Unique material findings | not applicable | 2 claimed | 1 accepted |
| Accepted findings | 1 | 1 patched / 1 owner-decision | 1 |
| Modified findings | 0 | 0 | 1 |
| Rejected / false-positive findings | 0 | 0 | 0 |
| Accepted patch hunks | 3 evidence-artifact wording edits | 1 | 1 |
| Architecture escalations | 0 | 0 | 0 |
| Elapsed time | `not_captured` | `not_captured` | `not_captured` |
| Token use | `not_captured` | `not_captured` | `not_captured` |

For this case, a **material** finding is one whose accepted closure changes
runtime classification correctness, test discrimination, evidence
admissibility, pin status, or a cross-artifact operating verdict. Spelling,
stylistic preference, and unrelated cleanup do not count as material.

## Decision interpretation after adjudication

- If the delegated pass produces at least one unique, accepted material
  finding, this case is evidence that the in-session review missed a defect in
  this mixed classifier-and-evidence change class.
- If it produces no unique accepted material finding, the case is evidence
  that the cheaper in-session review was sufficient **for this change**, not
  proof that strict delegation is unnecessary in general.
- Findings rejected during adjudication are recorded as reviewer false
  positives or scope errors, with the rejection reason.
- A `NEEDS_ARCHITECTURE_PASS` return is recorded separately; it is not converted
  into a patch success or counted as an implementation defect without
  adjudication.

Do not change the `success-implement` default or delegated-review convention
from this single case. Aggregate multiple comparable, adjudicated cases before
proposing a standing routing change.

## Adjudicated delegated return

The cross-vendor return is preserved at
`docs/review-outputs/adversarial-artifact-reviews/pr1111_kohls_access_diagnosis_delegated_code_review_v0.md`.
Its committed Git blob at adjudication was
`e9387a7a1af0e9d7558e420661974f1653452d3d`.

- **AKM-2 — accepted.** Mutation evidence showed that the pre-delegation suite
  stayed green when the required `all()` marker conjunction was weakened to
  `any()`. The two proposed tests separately bind the marker conjunction and
  exact-title gate, and the accepted hunk changes no runtime classifier logic.
- **AKM-1 — modified to a residual upgrade trigger.** A non-exact Akamai title
  could theoretically create a false negative, but no preserved failing title
  variant was observed. Broadening the match now would exchange known
  precision for hypothetical recall. Do not count this as a material defect or
  patch obligation. Re-open only when a retailer-owned capture preserves both
  Akamai markers with a non-exact title, or another bounded fixture establishes
  the variant.

The delegated pass therefore contributed **one unique accepted material
finding** beyond the in-session Success Implement review. For this case, the
strict pass added value by exposing a wrong-cause-green test gap. This single
case still does not establish a standing routing rule.

```yaml
delegated_return:
  status: adjudicated
  controller_vendor: Anthropic
  controller_model: Claude Sonnet 5
  strict_cross_vendor_de_correlation: true
  report_path: docs/review-outputs/adversarial-artifact-reviews/pr1111_kohls_access_diagnosis_delegated_code_review_v0.md
  report_git_blob_oid: e9387a7a1af0e9d7558e420661974f1653452d3d
  findings_total: 2
  overlap_findings: 0
  baseline_only_findings: 1
  unique_material_findings: 1
  accepted_findings: 1
  modified_findings: 1
  rejected_findings: 0
  accepted_patch_hunks: 1
  architecture_escalations: 0
  elapsed_time: not_captured
  token_use: not_captured
  dispositions:
    AKM-1: modified_to_residual_upgrade_trigger
    AKM-2: accepted_and_patch_kept
  adjudication_status: closed
```

## Non-claims

This case is not validation of Success Implement, not validation of delegated
review-and-patch, not a statistical conclusion, not a runtime model
recommendation, and not permission to dispatch a controller. The delegated
prompt remains operator-courier-only.
