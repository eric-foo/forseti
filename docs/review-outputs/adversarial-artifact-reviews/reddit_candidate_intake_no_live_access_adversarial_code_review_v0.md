# Reddit Candidate Intake No-Live-Access Delegated Adversarial Code Review v0

```yaml
retrieval_header_version: 1
artifact_role: Delegated adversarial code review-and-patch report
scope: De-correlated adversarial review of the no-live-access Reddit Candidate URL Intake implementation slice (capture_spine.reddit_candidate_intake) plus its unit and contract tests.
authority_boundary: retrieval_only
review_target_commit: 7d2d2310af3d72f70e326542515f2439932d52b7
review_branch: ecr-sp3-timing-deriver-slice1
open_next:
  - docs/prompts/reviews/reddit_candidate_intake_no_live_access_adversarial_code_review_prompt_v0.md
  - .agents/workflow-overlay/delegated-review-patch.md
  - orca/product/spines/capture/core/contracts/candidate_intake/data_capture_spine_candidate_url_intake_contract_v0.md
  - orca/product/spines/capture/core/contracts/candidate_intake/data_capture_spine_reddit_candidate_url_intake_crawler_architecture_v0.md
  - docs/decisions/data_capture_spine_reddit_candidate_url_intake_default_policy_decision_v0.md
stale_if:
  - Any target file changes after the post-patch hashes recorded below.
  - The parent contract, Reddit architecture, or default-policy decision changes.
  - The Chief Architect adjudicates (accept/modify/reject) the proposed diff.
```

## 1. Commission, Lane Binding, And Actor/Model-Family Receipt

**Commission.** Delegated, de-correlated adversarial code review-and-patch of the
no-live-access Reddit Candidate URL Intake implementation slice, commissioned by
`docs/prompts/reviews/reddit_candidate_intake_no_live_access_adversarial_code_review_prompt_v0.md`.

**Lane binding.** `workflow-delegated-review-patch` in `base-subagent` mode
(`.agents/workflow-overlay/delegated-review-patch.md`), executing
`workflow-code-review` as the review lane. This is a commissioned
bounded-executor lane, not one of the source-read-only review lanes; patch
authority is the commission's bounded target only. All output is decision input
for Chief Architect adjudication; it is not acceptance, validation, or readiness.

**Actor / model-family receipt.**

```yaml
actor_model_family_receipt:
  author_home_model_family: OpenAI/Codex current lane
  controller_model_family: Anthropic / Claude Opus 4.8
  current_receiving_actor_role: controller
  dispatch_mode: external-controller-courier
  de_correlation_status: satisfied
```

De-correlation is satisfied: the controller family (Anthropic) differs from the
author home family (OpenAI/Codex). The receipt is recorded before any
implementation source was read for review purposes. Review lane was applied; no
`BLOCKED_*` condition was triggered.

**Pinned source state verified before review.**

- HEAD `7d2d2310af3d72f70e326542515f2439932d52b7` matches the prompt pin.
- Branch `ecr-sp3-timing-deriver-slice1` matches the prompt pin.
- All six pre-patch input hashes matched the prompt retrieval header exactly
  (`models_py`, `validation_py`, `writer_py`, `unit_test_py`, `contract_test_py`,
  `pyproject_toml`) — source state was **not stale** at review start.

## 2. Source Context Status

`SOURCE_CONTEXT_READY`.

Authority sources read: `AGENTS.md` (supplied), `.agents/workflow-overlay/`
README, decision-routing, delegated-review-patch, source-of-truth,
source-loading, review-lanes, prompt-orchestration, validation-gates. Controlling
product/decision sources read in full: the parent Candidate URL Intake contract,
the Reddit Candidate URL Intake crawler architecture, and the Reddit default
policy decision. Target sources read in full: `capture_spine/__init__.py`,
`capture_spine/reddit_candidate_intake/{__init__,models,validation,writer}.py`,
`tests/unit/test_reddit_candidate_intake.py`,
`tests/contract/test_reddit_candidate_intake_contract.py`, and the
`capture_spine` package-discovery block of `pyproject.toml`.

Deliberately not loaded (not decision-bearing for this bounded review):
`source_capture` adapters, Reddit consolidation/planning threads beyond the named
contracts, packet assembly, ECR/Cleaning/Judgment, source-quality, `_inbox`, and
historical review outputs. Dirty-state allowance from the commission applied: the
implementation target is untracked; `pyproject.toml` is modified and only its
`capture_spine` package-discovery addition is in scope; the `cloakbrowser`
optional-dependency diff is out of scope and was not assessed beyond confirming
it does not corrupt `capture_spine` discovery.

## 3. Cynefin Routing Result

- **Smallest complete outcome:** review the no-live-access slice for boundary
  enforcement and fake-pass risk; apply only bounded guardrail-completeness
  patches inside the target.
- **Regime:** complicated.
- **Decomposition:** risk-first code review over a small source slice.
- **Current bottleneck:** proving the package cannot smuggle live access, Armory
  capture, packet-shaped output, same-run traversal, or broader `source_capture`
  coupling — and that the tests fail on those behaviors rather than passing on
  labels.
- **Riskiest assumption:** tests pass because labels are present rather than
  because forbidden behaviors are mechanically refused. **Confirmed partially
  true** for two secondary denylist guardrails (Findings M1, M2).
- **Stop/pivot condition:** if the slice required live execution to be
  meaningful, belonged in Source Capture Armory, or exposed a design-level
  defect, return `NEEDS_ARCHITECTURE_PASS` with no kept partial diff. **Not
  triggered** — the lane architecture is sound; the defects are patch-level
  guardrail completeness.
- **Allowed next move taken:** bounded patch of two denylist guardrails plus one
  regression test, inside the target files only.
- **Disallowed moves avoided:** no live Reddit access, no CloakBrowser/proxy
  invocation, no packet generation, no ECR/Cleaning/Judgment/source-quality work,
  no unrelated `pyproject` dependency change.

Verdict on escalation: **`NEEDS_ARCHITECTURE_PASS` not returned.**

## 4. Findings (Severity-Ordered)

### Critical

None. The slice has no live-access code path, emits no Source Capture Packet, and
captures no body/comment/profile content. The typed row models are frozen
dataclasses with fixed fields, forming a structural allowlist: a `body`,
`selftext`, screenshot, or session field cannot be attached to a
`CandidateSubredditRow`, `CandidateThreadUrlRow`, or `OutboundUrlCandidateRow`
through the typed path.

### Major

#### M1 — Forbidden-output denylist omits the canonical Reddit body field names (PATCHED)

- **Location:** `orca-harness/capture_spine/reddit_candidate_intake/validation.py`,
  `FORBIDDEN_OUTPUT_FIELDS` (pre-patch lines 41–67) and
  `assert_no_forbidden_output_fields` (recursive key check, pre-patch lines
  127–137).
- **Issue:** `assert_no_forbidden_output_fields` is the package's exported,
  defense-in-depth backstop against forbidden output. It is applied to an
  arbitrary `output: dict[str, Any]` in both `build_candidate_intake_output` and
  `write_candidate_intake_output`, so it also guards **hand-built** dicts that do
  not flow through the typed dataclasses. It matches field **names** against a
  fixed denylist by exact lowercased key. The denylist contained `body`,
  `comment*`, `raw_html`, `html`, `screenshot*`, but **omitted Reddit's canonical
  post-body field `selftext`** (and `selftext_html`, `body_html`), and the
  contract's explicitly-listed non-outputs "rendered DOM" and "parser output".
- **Evidence:** Reddit's listing/thread JSON returns post body under `selftext`
  and `selftext_html`, and comment-body HTML under `body_html`. Pre-patch,
  `assert_no_forbidden_output_fields({"selftext": "..."})` returned cleanly. The
  contract `Explicit Non-Outputs` lists "source body text", "raw HTML", "rendered
  DOM", and "parser output"
  (`data_capture_spine_candidate_url_intake_contract_v0.md` lines 327–351;
  Reddit architecture lines 386–408).
- **Impact:** The advertised mechanical backstop — the one whose job is exactly
  "no body capture" — had a predictable hole at the single most likely real-world
  Reddit body field name. No current code path emits these fields, so this is a
  guardrail-completeness defect, not a live leak; it is the highest-priority
  fake-pass risk because it maps directly to the commission's riskiest
  assumption.
- **`minimum_closure_condition`:** the exported forbidden-output check rejects
  the canonical Reddit body/HTML/DOM field names a hand-built output dict could
  realistically carry, and a regression test proves it.
- **`next_authorized_action`:** Chief Architect adjudication of the proposed diff.
- **Patched:** yes — added `selftext`, `selftext_html`, `body_html`,
  `rendered_dom`, `dom`, `parser_output` to `FORBIDDEN_OUTPUT_FIELDS`; added unit
  regression `test_reddit_post_body_field_selftext_is_rejected`.

#### M2 — No-live-access import guardrail omits `http` and other fetch-capable roots (PATCHED)

- **Location:**
  `orca-harness/tests/contract/test_reddit_candidate_intake_contract.py`,
  `FORBIDDEN_IMPORT_ROOTS` (pre-patch lines 8–23), consumed by
  `test_reddit_candidate_intake_has_no_network_browser_or_armory_imports`.
- **Issue:** The contract test is the mechanical proof of "no live-access
  imports". It listed `urllib`, `socket`, `requests`, `httpx`, `aiohttp`,
  browser/driver roots, and `source_capture`, but **omitted `http`** — the
  stdlib `http.client` is a fully capable live HTTP/HTTPS client and the direct
  sibling of the already-listed `urllib`. It also omitted `subprocess` (shell-out
  to `curl`/`wget`/a browser), `pycurl`, `websocket`/`websockets`, and `ftplib`.
- **Evidence:** Pre-patch, a future edit adding `from http.client import
  HTTPSConnection` (or `import subprocess` to invoke `curl`) to a target file
  would still pass the import guardrail. The commission review criteria require
  "no live Reddit, HTTP, browser, ... socket, or webbrowser imports" and "tests
  would fail on ... live-access imports".
- **Impact:** The guardrail asymmetry (`urllib` forbidden, `http` allowed) is a
  clear oversight that leaves the most idiomatic stdlib HTTP path and the
  shell-out path uncovered. No target file currently imports these, so this is
  guardrail completeness, not a live leak.
- **`minimum_closure_condition`:** the import guardrail covers the stdlib HTTP
  client and the obvious shell-out/alternate-fetch roots, so a future live-fetch
  import in a target file fails the contract test.
- **`next_authorized_action`:** Chief Architect adjudication of the proposed diff.
- **Patched:** yes — added `http`, `subprocess`, `pycurl`, `websocket`,
  `websockets`, `ftplib` to `FORBIDDEN_IMPORT_ROOTS` (alphabetical order
  preserved). Existing import tests still pass (no target file imports these).

### Minor (flag-only — not patched)

#### m1 — Dead/no-op tail branches in two validators

- **Location:** `validation.py` `validate_run_envelope` final
  `if CandidateSurface.OUTBOUND_LINKS in ...: return` (post-patch ~lines 98–101)
  and `validate_promotion_receipt` final
  `if receipt.decision_frame_or_capture_unit_authority and
  receipt.capture_not_yet_authorized: return`.
- **Issue:** Both branches are the last statement in their function and `return`
  `None` exactly as the implicit fall-through would; they perform no validation.
  The outbound branch's comment implies an opt-in/cap check that is not present.
- **Impact:** No correctness bug; misleading because it reads like an enforced
  check. Quality only.
- **`minimum_closure_condition`:** either remove the no-op branches or implement
  the implied check (e.g., outbound opt-in cap enforcement) intentionally.
- **`next_authorized_action`:** owner/CA decision; optional cleanup, not required.
- **Patched:** no (kept diff minimal and boundary-focused).

#### m2 — Outbound-row failure raises bare `ValueError`, not the module error type

- **Location:** `writer.py` `build_candidate_intake_output`, the outbound loop
  `raise ValueError("outbound URL candidates require separate source-family
  intake")` (lines 49–50).
- **Issue:** Every other refusal in the package raises
  `RedditCandidateIntakeError(code, message)` with a stable error code; this one
  path raises a bare `ValueError` with no code, breaking the module's error
  contract and the "clear error codes / stable shape" review criterion.
- **Impact:** Callers cannot branch on `.code` for this refusal; inconsistent
  error surface. Reachable when an `OutboundUrlCandidateRow` is constructed with
  `requires_separate_source_family_intake=False`.
- **`minimum_closure_condition`:** the outbound refusal raises
  `RedditCandidateIntakeError` with a dedicated code consistent with the rest of
  the module.
- **`next_authorized_action`:** owner/CA decision; optional consistency fix.
- **Patched:** no.

#### m3 — Numeric cap ceilings are not enforced against the default-policy maxima

- **Location:** `validation.py` `validate_run_envelope` (cap positivity checks,
  post-patch ~lines 87–94).
- **Issue:** The validator enforces `cap >= 1` and the `coverage_claim`↔`cap_type`
  binding, but not the per-`cap_type` maximums in `DEFAULT_CAPS`. A `probe` run
  can declare `max_subreddits=50` (high-recall-sized) while keeping
  `coverage_claim: bounded_probe_only`.
- **Impact:** Advisory. The default-policy decision frames its caps as "maximum
  default limits ... Exceeding these caps requires an explicit scope amendment or
  later owner decision" (default policy lines 145–148), and the envelope carries
  no scope-amendment field. The code comment treats numeric ceilings as owner
  policy. This weakens the honesty of `coverage_claim` but does not breach a hard
  stop, and the policy permits exceeding via amendment, so enforcing a hard
  ceiling here is a policy choice, not a defect under the current decision.
- **`minimum_closure_condition`:** owner decides whether the lane should reject
  caps above the `cap_type` maxima absent a recorded scope amendment, or whether
  ceilings remain owner-policy-only.
- **`next_authorized_action`:** owner/CA policy decision; no code change without
  it.
- **Patched:** no.

### Non-findings checked and clear

- **Old-Reddit-first URL validation is a strict anchored allowlist.**
  `_OLD_REDDIT_LISTING_RE` / `_OLD_REDDIT_THREAD_RE` anchor `^https://old\.reddit\.com/r/...`
  with the dots escaped. Host-spoofing variants (`old.reddit.com.evil.com/...`,
  userinfo `...com@evil.com`, `new.`/`np.`/`m.` subdomains, `http://`) do not
  match and are refused. New Reddit (`www.reddit.com` / `reddit.com`) is refused
  with the explicit `new_reddit_non_default` code for threads and
  `non_old_reddit_*` for any non-old shape. No false-positive acceptance of
  non-old-Reddit URLs was found.
- **`coverage_claim` cannot mismatch `cap_type`** — enforced against `DEFAULT_CAPS`.
- **Same-run traversal is refused** — `same_run_traversal_authorized=True` raises
  `same_run_traversal_forbidden`; outbound rows carry
  `requires_separate_source_family_intake=True` and are not fetched.
- **Promotion receipt** requires `known_limitations`, `capture_not_yet_authorized`,
  and forbids `source_capture_armory_execution_happened`.
- **`empty_result` / `blocked_result`** remain valid terminal `StopReason`s; no
  retry-escalation logic exists.
- **No mutable-default pitfalls** — frozen dataclasses, tuple defaults, and the
  `x = x or []` pattern in the writer.
- **Stable JSON shape** — `json.dumps(..., sort_keys=True)`.
- **No broad package export** — `capture_spine/__init__.py` does not import the
  subpackage; the subpackage imports stdlib only; both contract import tests pass.
- **`caps_reached` is not represented as completion/sufficiency** — recorded as a
  neutral `StopReason` with caps and `coverage_claim`; the receipt prints the
  stop reason plainly with non-claims.

## 5. Unified Diff (target files only)

All three target files were untracked in the working tree, so no git baseline
diff exists; the following reconstructs the exact edits applied against the
hash-pinned originals.

```diff
--- a/orca-harness/capture_spine/reddit_candidate_intake/validation.py
+++ b/orca-harness/capture_spine/reddit_candidate_intake/validation.py
@@ FORBIDDEN_OUTPUT_FIELDS = {
     "body",
     "body_text",
+    "selftext",
+    "selftext_html",
+    "body_html",
     "comment",
     "comments",
     "comment_body",
     "comment_text",
@@
     "raw_html",
     "html",
+    "rendered_dom",
+    "dom",
+    "parser_output",
     "screenshot",
     "screenshot_path",
```

```diff
--- a/orca-harness/tests/contract/test_reddit_candidate_intake_contract.py
+++ b/orca-harness/tests/contract/test_reddit_candidate_intake_contract.py
@@ FORBIDDEN_IMPORT_ROOTS = {
     "aiohttp",
     "bs4",
     "cloakbrowser",
+    "ftplib",
+    "http",
     "httpx",
     "patchright",
     "playwright",
     "praw",
+    "pycurl",
     "requests",
     "scrapy",
     "selenium",
     "socket",
     "source_capture",
+    "subprocess",
     "urllib",
     "webbrowser",
+    "websocket",
+    "websockets",
 }
```

```diff
--- a/orca-harness/tests/unit/test_reddit_candidate_intake.py
+++ b/orca-harness/tests/unit/test_reddit_candidate_intake.py
@@
     assert exc_info.value.code == "forbidden_output_field"
 
 
+def test_reddit_post_body_field_selftext_is_rejected() -> None:
+    # selftext / selftext_html / body_html are Reddit's canonical body field names.
+    for field in ("selftext", "selftext_html", "body_html"):
+        with pytest.raises(RedditCandidateIntakeError) as exc_info:
+            assert_no_forbidden_output_fields({field: "not allowed"})
+        assert exc_info.value.code == "forbidden_output_field"
+
+
 def test_same_run_traversal_is_rejected() -> None:
```

**Post-patch hashes (changed files):**

- `validation.py`: `a970f14e664c104493b28f63bdfe3fd9c59f91c839f83f7d6a93f1b02f683e43`
- `tests/unit/test_reddit_candidate_intake.py`: `c2ee3d5b1082e173aaef9fc020258ede2f18b8944632398ae5a1144f7a31db66`
- `tests/contract/test_reddit_candidate_intake_contract.py`: `ef4a251e69d61b30bd92a6571c0f897871d246963fcad62c303784265c42d0ae`

**Unchanged target files (still match prompt pins):** `models.py`
(`a8a008e4…`), `writer.py` (`79e779ca…`), `pyproject.toml` (`7f7aaab7…`).

## 6. Per-Change Neutral Source Citations

- **M1 patch (validation.py forbidden-output names).**
  `data_capture_spine_candidate_url_intake_contract_v0.md` `Explicit Non-Outputs`
  (lines 327–351) lists "source body text", "comment, reply, or discussion body
  text", "raw HTML", "rendered DOM", and "parser output" as prohibited outputs.
  `data_capture_spine_reddit_candidate_url_intake_crawler_architecture_v0.md`
  `Explicit Non-Outputs` (lines 386–408) repeats "thread body text", "comment
  body text", "raw HTML", "parser output". The added field names
  (`selftext`/`selftext_html`/`body_html` = Reddit body/body-HTML;
  `rendered_dom`/`dom` = rendered DOM; `parser_output` = parser output) are
  realistic key names for those prohibited categories.
- **M2 patch (contract test import roots).** The same two contracts forbid
  "live Reddit/HTTP/browser" access by implication, and the commission prompt's
  review criteria require "no live Reddit, HTTP, browser, CloakBrowser, proxy,
  Reddit API, archive, parser, socket, or webbrowser imports". `http` is the
  stdlib HTTP client and the direct sibling of the already-listed `urllib`;
  `subprocess`/`pycurl`/`websocket(s)`/`ftplib` are additional fetch-capable
  roots.
- **Regression test.** Validates the M1 closure condition directly by asserting
  the canonical Reddit body field names raise `forbidden_output_field`.

Citations are neutral source evidence; the controller's argument is in the
verdict and residual-risk note below.

## 7. Controller Verdict And Residual-Risk Note

**Verdict.** The slice is architecturally in-bounds for a no-live-access
Candidate URL Intake lane: candidate-rows-plus-provenance output, a structural
typed-row allowlist, refused new-Reddit and same-run-traversal, a
non-authorizing promotion receipt, and no `source_capture`/network/browser
coupling. The two material defects were **guardrail completeness** in the
secondary denylists, not design defects and not live leaks; both are patched with
the smallest additive change. No `NEEDS_ARCHITECTURE_PASS`. Recommendation:
**accept the proposed diff, subject to CA adjudication.**

**Residual risk.**

1. A name-denylist (`FORBIDDEN_OUTPUT_FIELDS`) is structurally non-exhaustive: it
   can never enumerate every possible smuggling key for hand-built dicts. The
   real guarantee for the typed path remains the frozen dataclass fields. The M1
   patch closes the most predictable gap; a durable fix for arbitrary hand-built
   dicts would be an allowlist of permitted keys per row shape — that is a design
   change, deferred to CA, not taken here.
2. `http`/`subprocess` are coarse roots; in a different package they could flag
   benign uses, but for this no-live-access slice that strictness is appropriate
   and no current target file imports them.
3. Minors m1–m3 remain open (flag-only) and are CA/owner decisions.
4. This review covers the bounded target only at the recorded post-patch hashes;
   it is not whole-harness, not runtime, and not legal/rights review.

## 8. Validation Run Status

- **Tooling:** Python 3.x via `python -m pytest`, run from `orca-harness/`. No
  dependency installation, no network access, no browser/CloakBrowser/proxy, no
  runner dispatch.
- **Baseline (pre-patch), exact command run:**
  `python -m pytest -p no:cacheprovider tests/unit/test_reddit_candidate_intake.py tests/contract/test_reddit_candidate_intake_contract.py`
  → `9 passed in 0.05s`.
- **Post-patch, exact command run (same command):** → `10 passed in 0.06s`
  (the +1 is the new `test_reddit_post_body_field_selftext_is_rejected`).
- **Not run:** whole-suite pytest, live Reddit access, any
  network/browser/archive/parser execution — all out of scope and disallowed by
  the commission.

## 9. Off-Scope Flags

- **`pyproject.toml` `cloakbrowser` optional-dependency diff:** out of scope per
  commission; confirmed it does not corrupt `capture_spine`/`capture_spine.*`
  package discovery. Not assessed further, not changed.
- **Denylist → per-row-shape allowlist refactor for hand-built dicts:** a
  design-level improvement, larger than the smallest complete patch; flagged for
  CA, not applied.
- No parent-architecture-doc, Source Capture Armory, `source_capture` adapter,
  runner, source-access, or product-policy change was required or made.

## 10. CA Adjudication Packet

The diff, citations, and verdict below are **claims to adjudicate, not premises
to inherit.** No change is kept, accepted, validated, or ready until the Chief
Architect adjudicates it.

```yaml
ca_adjudication_packet:
  proposed_changes:
    - id: M1
      change: add selftext, selftext_html, body_html, rendered_dom, dom, parser_output to FORBIDDEN_OUTPUT_FIELDS
      file: orca-harness/capture_spine/reddit_candidate_intake/validation.py
      citation: candidate_url_intake_contract Explicit Non-Outputs (327-351); reddit architecture Explicit Non-Outputs (386-408)
      closure_condition: exported forbidden-output check rejects canonical Reddit body/HTML/DOM field names; regression proves it
      ready_for_adjudication: accept | modify | reject
    - id: M1-test
      change: add test_reddit_post_body_field_selftext_is_rejected
      file: orca-harness/tests/unit/test_reddit_candidate_intake.py
      citation: validates M1 closure condition
      closure_condition: selftext/selftext_html/body_html raise forbidden_output_field
      ready_for_adjudication: accept | modify | reject
    - id: M2
      change: add http, subprocess, pycurl, websocket, websockets, ftplib to FORBIDDEN_IMPORT_ROOTS
      file: orca-harness/tests/contract/test_reddit_candidate_intake_contract.py
      citation: review criteria "no live Reddit, HTTP, ... socket, or webbrowser imports"; http is sibling of listed urllib
      closure_condition: future live-fetch import in a target file fails the contract test
      ready_for_adjudication: accept | modify | reject
  flagged_not_patched:
    - id: m1
      note: dead/no-op tail branches in validate_run_envelope and validate_promotion_receipt; remove or implement intentionally
    - id: m2
      note: outbound-row failure raises bare ValueError instead of RedditCandidateIntakeError with a code
    - id: m3
      note: numeric cap ceilings not enforced vs DEFAULT_CAPS maxima; owner policy decision
  off_scope_or_design_level:
    - cloakbrowser optional-dependency diff in pyproject.toml (out of scope, not corrupting discovery)
    - denylist -> per-row allowlist refactor for hand-built dicts (design-level, deferred)
  validation_evidence: "pre-patch 9 passed; post-patch 10 passed (named command)"
  non_claims:
    - not owner acceptance
    - not validation or readiness
    - not live Reddit / CloakBrowser / proxy / Source Capture Armory authorization
    - patch not kept until Chief Architect adjudicates
```

## 11. Review-Use Boundary

This delegated review-and-patch result is **decision input only.** The
controller's diff, citations, and verdict are claims to adjudicate, not premises
to inherit. It is not owner acceptance, validation proof, readiness, deployment,
source-access authorization, live Reddit authorization, Source Capture Armory
authorization, or permission to keep any patch without Chief Architect
adjudication. The proposed diff currently sits in the working tree (untracked,
unstaged, uncommitted) and must not be treated as kept until the Chief Architect
accepts it.
