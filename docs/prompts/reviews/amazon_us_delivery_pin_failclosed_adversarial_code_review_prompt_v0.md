# Amazon US Delivery Pin Fail-Closed Adversarial Code Review Prompt v0

```yaml
retrieval_header_version: 1
artifact_role: Review prompt
scope: >
  Read-only adversarial code review of the Amazon delivery-location adapter and
  Capture Spine runner changes that reject currency-only confirmation, marketplace
  redirects, and final pages that lose the requested US ZIP pin.
use_when:
  - Commissioning the owner-requested delegated review of Amazon US pin hardening.
  - Checking whether failed pins remain preserved as typed packets without becoming admissible US evidence.
authority_boundary: retrieval_only
open_next:
  - .agents/workflow-overlay/review-lanes.md
  - .agents/workflow-overlay/prompt-orchestration.md
  - .agents/workflow-overlay/source-loading.md
branch_or_commit: 9b0026b8942c79e8b08ee9ee84225e494404a3c2
stale_if: >
  The implementation files change after the pinned commit or the Amazon
  delivery-location admission contract is superseded.
```

## Prompt Preflight

preflight_defaults: `docs/prompts/templates/shared/forseti_preflight_defaults_v0.md` v0 - constants bound; deltas stated inline.

```yaml
output_mode: chat-only
template_kind: none
edit_permission: read-only
workspace: C:\Users\vmon7\Desktop\projects\orca\.codex\worktrees\amazon-us-pin-failclosed
branch: codex/amazon-us-pin-failclosed
target_revision: 9b0026b8942c79e8b08ee9ee84225e494404a3c2
dirty_state_allowance: none_for_review_target
targets:
  - forseti-harness/source_capture/adapters/amazon_delivery_location.py
  - forseti-harness/runners/run_source_capture_cloakbrowser_packet.py
  - forseti-harness/tests/unit/test_durability_us_storefront_pin_wiring.py
  - forseti/product/spines/capture/core/source_families/retail_pdp/demand_durability_us_storefront_pin_recon_verdict_v0.md
  - forseti/product/spines/capture/core/source_families/retail_pdp/retail_pdp_sidecar_operator_playbook_v0.md
reviews: findings-first adversarial implementation review; confidence labels are bound; no formal approval, readiness verdict, patch queue, or runtime-model routing
doctrine_change: none
input_prompt_source: docs/prompts/reviews/amazon_us_delivery_pin_failclosed_adversarial_code_review_prompt_v0.md
output_destination: current reviewer chat for courier return to the implementation lane
```

## Commission

Review the implementation diff at exact commit
`9b0026b8942c79e8b08ee9ee84225e494404a3c2` against its parent. The branch may
advance only to add this prompt; exclude that prompt-only commit from the code
review target.

This is a read-only adversarial code-review commission. Do not edit files, run a
live Amazon capture, create or switch branches or worktrees, commit, push, open
or update a PR, merge, stash, reset, clean, or emit an executor-ready patch
queue. Findings may state the minimum end condition needed for closure, but
patch implementation remains with the home lane after adjudication.

The commissioned outcome is narrow: determine whether `--delivery-zip` now
fails closed whenever the requested ZIP is not continuously evidenced on the
final Amazon US page, while still preserving an honest typed packet for
diagnosis. Do not redesign session persistence, add cookies, profiles, VPNs,
proxies, schemas, adapters, crawlers, monitoring, or live-probe scope.

## Source and Method Order

1. Read `AGENTS.md` and `.agents/workflow-overlay/README.md`.
2. Read the targeted sections of:
   - `.agents/workflow-overlay/review-lanes.md` — Current Lanes, Review Doctrine, and Rules;
   - `.agents/workflow-overlay/source-loading.md` — Targeted Read Protocol;
   - `forseti/product/spines/capture/core/source_capture_toolbox/source_capture_playbook_v0.md` — access-control and typed-failure rules;
   - `forseti/product/spines/capture/core/source_capture_toolbox/capture_recon_index_v0.md` — Amazon route entry only.
3. Inspect `git show --no-ext-diff --find-renames
   9b0026b8942c79e8b08ee9ee84225e494404a3c2` and the five target files.
4. Declare `SOURCE_CONTEXT_READY`, or return
   `SOURCE_CONTEXT_INCOMPLETE` with the missing source and the claim it blocks.
5. Apply the resolver-visible `workflow-code-review` skill. If it is unavailable
   or cannot be applied, return `BLOCKED_REVIEW_LANE_UNAVAILABLE`; do not invent
   a formal review result.

## Review Axes

Attack at least these failure modes:

- A USD marker, dollar glyph, unrelated ZIP text, or split signals can still
  confirm delivery ZIP `10001`.
- The requested URL or final URL can leave `amazon.com` without producing a
  typed, nonzero failure.
- The homepage can redirect to another Amazon marketplace and the adapter can
  continue widget interaction as though it were still on the US storefront.
- Adapter setup failure, final-page confirmation failure, source-detail
  sufficiency failure, and packet writing interact in an order that loses raw
  evidence, hides the primary reason, or creates false success.
- `pin_confirmed` accepts truthy non-boolean values, stale metadata, or a
  confirmation derived from the wrong rendered page.
- Amazon-specific CLI validation or plugin exclusivity regresses Nordstrom,
  Luckyscent, Target, ordinary no-plugin captures, or `--preflight-only`.
- URL host validation is bypassable by subdomains, user-info, ports, malformed
  URLs, redirects, or case variants.
- Tests rely on fakes that cannot expose the real ordering or metadata failure,
  omit a load-bearing branch, or assert the implementation rather than the
  admission rule.
- Operator documentation still allows a historical USD-only receipt to be
  mistaken for current delivery-location proof.

Do not penalize the lane merely for retaining fresh anonymous per-packet
sessions. A bounded multi-PDP session and persistent cookies were explicitly
not commissioned. The required invariant is fail-closed admission, not
guaranteed Amazon routing success.

## Validation Evidence to Inspect

The implementation lane observed:

```text
focused Amazon pin suite: 40 passed
combined retailer/CloakBrowser regression suite: 156 passed
check_harness_coupling.py --selftest: SELFTEST OK
check_map_links.py --strict: OK (0 findings)
check_review_routing.py --strict: OK before the code commit existed
check_full_gt_claims.py --changed --strict: OK before the code commit existed
git diff --check: exit 0
```

Treat these as claims to inspect, not formal proof. The pre-commit
`--changed` gate results did not include the then-uncommitted diff and must not
be credited as post-commit coverage. If repository execution is available,
rerun at minimum:

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
python -m pytest -p no:cacheprovider -q --basetemp '.pytest_amazon_review' forseti-harness/tests/unit/test_durability_us_storefront_pin_wiring.py
```

If execution is unavailable, report `validation_not_run` and continue the
source review. Do not access Amazon or any other external site.

## Output Contract

Return findings first, ordered by materiality. Use `critical`, `major`, or
`minor` only as priority labels; they do not create approval or mandatory
remediation authority. Each finding must include:

- `finding_id`
- `severity`
- `confidence` (`high`, `medium`, or `low`)
- file and line or stable structural anchor
- concrete implementation evidence
- failure impact
- `minimum_closure_condition`
- `next_authorized_action` (normally home-lane adjudication)

Also return:

- `source_read_ledger`
- `validation_run_status`
- `considered_and_defended` entries for candidate failures defeated by the code
- open questions and residual risks
- explicit off-scope or not-proven boundaries
- provenance fields:

```yaml
reviewed_by: operator_or_reviewer_to_fill_or_unrecorded
authored_by: OpenAI/Codex GPT-5
de_correlation_bar: operator_to_fill_or_unrecorded
same_vendor_rationale: not_applicable_unless_same_vendor_sanity_is_claimed
```

Do not fabricate reviewer identity. Close with:

```text
DELEGATED_CODE_REVIEW_RETURN_FOR_HOME_MODEL

Target: Amazon US delivery pin fail-closed implementation at
9b0026b8942c79e8b08ee9ee84225e494404a3c2
Return: findings, evidence, validation status, considered-and-defended
candidates, residual risks, and blockers for home-lane adjudication.
```

Review findings are decision input only. They are not approval, validation,
readiness, mandatory remediation, or patch authority until separately
adjudicated and authorized.
