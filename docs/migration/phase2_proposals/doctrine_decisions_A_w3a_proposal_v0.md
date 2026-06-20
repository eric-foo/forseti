```yaml
retrieval_header_version: 1
artifact_role: Orca migration note
scope: >
  Phase-2 W3a deletion + ontology proposal for the alphabetical first half of
  docs/decisions/*.md (44 files, adversarial_review_routing_policy_v0.md through
  doctrine_change_propagation_restatement_integrity_decision_v0.md). Read-only
  scan; proposes candidates for owner adjudication only. Executes nothing.
use_when:
  - Owner adjudicating Phase-2 deletion candidates in the docs/decisions/ A-half.
  - Cross-referencing the sibling B-half proposal before executing any deletions.
authority_boundary: retrieval_only
open_next:
  - docs/migration/orca_second_pass_consolidation_plan_v0.md
stale_if:
  - Any file in the scanned set is deleted, moved, or superseded before execution.
  - The deletion-evidence register gains records for targets listed here.
```

# Phase-2 W3a Proposal — doctrine (docs/decisions A-half)

## Summary

Files scanned: 44
File range: `adversarial_review_routing_policy_v0.md` .. `doctrine_change_propagation_restatement_integrity_decision_v0.md`
(Sorted alphabetically by filename; README.md sorts into the B-half.)

Governed root check: `docs/decisions/` is OUTSIDE `GOVERNED_ROOTS = ("orca/product/",)` in
`.agents/hooks/check_deletion_evidence.py`. Every deletion candidate below is therefore
**ungated: human-review-only at execute** — the strict CI gate does NOT fire on docs/decisions/
deletions. A deletion-evidence register record is not mechanically required, but the audit-trail
rationale (these are governance records) makes human adjudication mandatory regardless.

Conservative posture applied throughout: decision records are the governance AUDIT TRAIL.
Only files that are (a) provably superseded by a named, existing successor, (b) duplicate
of a live record, or (c) explicitly dropped/retired with a named re-open guard qualify for
a deletion proposal. When uncertain, no proposal is made.

---

## A. Deletion Candidates

### Candidate A-1 — WITHDRAWN (de-duplicated; owned by doctrine-B)

> Cross-vendor 2nd-eyes (2026-06-19): this target sorts alphabetically into the
> **doctrine-B** range; the A-half subagent overreached its range. `turn_07_branch_casing.md`
> is owned by doctrine-B's Candidate 1, so this A-half listing is **withdrawn** to remove the
> duplicate. Evidence below is retained for reference only — do not double-count it.

```yaml
targets:
  - docs/decisions/turn_07_branch_casing.md
ungated: human-review-only at execute
evidence:
  reverse_ref_check: >
    Grep of full repo for "turn_07_branch_casing" returned 0 matches in any
    .md, .yaml, .py, or .json file. No inbound references found anywhere in
    docs/, orca/, .agents/, or .github/. Safe to remove from a ref-graph
    perspective. Also absent from docs/decisions/orca_doctrine_index_v0.md
    (not indexed as a doctrine or active record).
  successor: "none -- pure bloat"
  semantic_delta: >
    Records a one-time branch rename (Main -> main) made before the first
    commit on 2026-05-13. The fact is now encoded permanently in git history
    (the rename occurred; main is the branch name). No rule, policy, or
    ongoing constraint is expressed here that is not already visible in the
    live branch name and git log. Zero information loss to the governance
    audit trail on deletion.
  rollback: git revert <executing merge sha>
confidence: high
rationale: pure-bloat -- zero inbound refs; one-time infra trivia fully encoded in git history; no policy content
```

### Candidate A-2

```yaml
targets:
  - docs/decisions/data_capture_spine_deleted_comment_signal_retrieval_scoped_doctrine_decision_v0.md
ungated: human-review-only at execute
evidence:
  reverse_ref_check: >
    Grep found 3 inbound references:
    (1) docs/migration/repo_structure_phase2_consolidation_v0/reference_inventory.md:14
        -- listed as "historical" class (not a live routing pointer; inventory
        of old paths only).
    (2) docs/decisions/orca_doctrine_index_v0.md:84
        -- listed in the "Dropped" section: "DROPPED 2026-06-08 (re-open guard)".
        The index explicitly marks it Dropped and carries the re-open guard
        reminder; that row would stay in the index even after the file is deleted
        as a Dropped record.
    (3) orca/product/spines/capture/core/source_capture_toolbox/reddit_capture_operator_playbook_v0.md:290
        -- references the file by path to point operators to the re-open guard.
        This is a load-bearing reference: the playbook explicitly tells operators
        "see this decision for the dropped capability and its re-open guard."
        Deleting the target without preserving the re-open guard content elsewhere
        would break that reference.
  successor: "none -- pure bloat"
  semantic_delta: >
    The file carries the considered-and-rejected record for deleted-comment
    retrieval, the re-open guard (3 conditions that must ALL change before
    re-exploring), the erasure-granularity resolution (Regime A), and the
    design sections preserved as the rejected record. The re-open guard in
    the playbook reference is load-bearing: it stops re-exploration without
    a check. Deletion would break reddit_capture_operator_playbook_v0.md:290's
    pointer. Semantic loss is non-zero and the playbook reference is active.
  rollback: git revert <executing merge sha>
confidence: low
rationale: >
  DROPPED status makes this a deletion candidate in principle, but the load-bearing
  playbook reference at orca/product/spines/capture/core/source_capture_toolbox/
  reddit_capture_operator_playbook_v0.md:290 means deletion would break an active
  routing pointer. Owner must decide whether to (a) update the playbook to inline
  the re-open guard before deleting, or (b) retain this file. NOT proposed for
  deletion without that playbook update. Downgraded to low confidence / conditional.
```

### No further deletion candidates in the A-half.

The following categories were considered and explicitly NOT proposed:

- **All Daimler decision records** (daimler_v0_14_*, daimler_advisory_*): active governance
  audit trail for a live fixture work-track; all cross-referenced by probe receipts, runbooks,
  and open_next chains. No supersession.
- **All data_capture_spine_source_observability_* records**: active authorization chain;
  each record is referenced by the next step in the chain and by the reference_inventory.
- **All distillation_binding_* records**: PREPARE-ONLY but active; each is cross-referenced
  by distillation_doctrine_orca_spine_bindings_v0.md which is itself indexed.
- **adversarial_review_routing_policy_v0.md**: PROPOSED_DRAFT (pending cross-family review +
  owner acceptance) with active inbound refs from review-lanes.md, dcp_receipts_archive_v0.md,
  and ontology_runtime_drift_check_contract_v0.md. Not superseded; not dropped; not proposed.
- **dev_workflow_up_to_date_merge_enforcement_proposal_v0.md**: PROPOSAL not accepted, but
  has 0 inbound refs outside itself. However, it is a pending proposal that the owner has
  not rejected -- it is deferred, not dropped. Conservative posture: not proposed for deletion.
- **ci_registration_integrity_check_proposal_v0.md**: referenced by
  docs/hygiene/registration_integrity_review_README.md. Active proposal artifact.
- **company_aggregate_forward_signal_* records**: authorized and cross-referenced; active.
- **All company/org-motion records**: open_next chains from architecture to capture-lane scope.
- **dcp_receipts_archive_v0.md, deletion_evidence_doctrine_v0.md**: explicitly excluded by
  task instructions.

---

## B. Ontology / Doc-Term Findings

Scope of check: A-half files in docs/decisions/ scanned against ontology.yaml SSOT.

SSOT canonical types (17 adopted + 2 reserved): Vertical, Brand, Product, Venue, WindCaller,
Call, Observation, TrendVector, DecisionEvent, Reading, Memo, Case, Outcome, CapturePacket,
EvidenceUnit, Buyer, Org.

SSOT runtime aliases: SourceCapturePacket (-> CapturePacket), FacilitatorLedger (-> Case),
CaseReport (-> Case, composed_with).

Head nouns of multi-hump canonical types: Caller, Event, Packet, Unit, Vector.

### CamelCase terms found in A-half docs

| Token | File:line | Classification | Finding |
| --- | --- | --- | --- |
| EvidenceUnit | distillation_held_lessons_beautypie_pilot_v0.md:119; jsg01_unfreeze_decision_v0.md:59; jsg01_unfreeze_decision_memo_v0.md:32,41; ontology_runtime_drift_check_contract_v0.md:42 | SSOT canonical (adopted) | Correct usage. |
| FacilitatorLedger | distillation_held_lessons_beautypie_pilot_v0.md:133,166; ontology_runtime_drift_check_contract_v0.md:42 | SSOT runtime alias (-> Case) | Correct usage. |
| CaseReport | ontology_runtime_drift_check_contract_v0.md:42,117 | SSOT runtime alias (-> Case, composed_with) | Correct usage. |
| SourceCapturePacket | judgment_spine_backtest_batch1_ledger_declaration_v0.md:168; ontology_runtime_drift_check_contract_v0.md:41 | SSOT runtime alias (-> CapturePacket) | Correct usage. |
| CompanySignal | company_aggregate_forward_signal_architecture_decision_v0.md:49; company_aggregate_forward_signal_capture_lane_scope_decision_v0.md:178,319 | Runtime class from orca-harness/capture_spine/linkedin_live_runtime/ | NOT an ontology type nor an alias. Head noun "Signal" is not an ontology head noun. NOT a new-term candidate under the check_doc_terms.py predicate (head noun "Signal" not in {Caller, Event, Packet, Unit, Vector}). No SSOT mismatch; this is a harness-internal class name cited in context. No fix needed. |
| LiveObservation | company_aggregate_forward_signal_capture_lane_scope_decision_v0.md:320,346 | Runtime class from orca-harness/capture_spine/linkedin_live_runtime/ | Head noun "Observation" is single-hump -- does not trigger multi-hump rule. Not a new-term candidate. No fix needed. |
| PreToolUse | distillation_doctrine_orca_spine_bindings_v0.md:55; distillation_binding_overlay_governance_v0.md (inferred) | Claude Code hook event name | Not an ontology term. Head noun "Use" is not an ontology head noun. No SSOT mismatch. |
| PostToolUse | distillation_doctrine_orca_spine_bindings_v0.md:188 | Claude Code hook event name | Same as PreToolUse -- no SSOT mismatch. |
| BrowserFetcher | company_aggregate_forward_signal_architecture_decision_v0.md (inferred from grep) | Harness runtime class | Head noun "Fetcher" is not an ontology head noun. No SSOT mismatch. |

### Summary

Clean. No non-SSOT ontology-shaped coinages (terms with head nouns in {Caller, Event, Packet,
Unit, Vector} that are not in the SSOT) found in the A-half docs/decisions/ files.
All observed CamelCase ontology-type tokens are either SSOT canonical types, SSOT runtime
aliases, or harness-internal runtime class names that do not match the ontology head-noun
predicate. No proposed read-only fixes needed.

Note: check_doc_terms.py's scope is `orca/product/` (not `docs/decisions/`). The findings
above are a manual extension of the same predicate to the A-half decision records. They
are advisory only; the tool would not flag these files.

---

## Non-Claims

This proposal executes nothing. It proposes; the owner adjudicates. All deletion tags are
"ungated: human-review-only at execute" because docs/decisions/ is outside GOVERNED_ROOTS.
The low-confidence Candidate A-2 requires a playbook update before any execution is warranted.
No record is deleted, renamed, or modified by this artifact.
