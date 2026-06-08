# Reddit Candidate Intake Old Reddit HTML Projection Delegated Adversarial Code Review v0

```yaml
retrieval_header_version: 1
artifact_role: Delegated adversarial code review report
scope: >
  De-correlated adversarial review-and-patch of the old Reddit HTML
  static-projection and Reddit .json refusal slice of Candidate URL Intake.
authority_boundary: retrieval_only
stale_if:
  - Any target implementation file or test changes after this report is written.
  - The Candidate URL Intake parent contract, Reddit architecture, or
    default-policy decision changes.
```

---

## 1. Commission, Lane Binding, and Actor / Model-Family Receipt

```yaml
commission:
  source_prompt: docs/prompts/reviews/reddit_candidate_intake_old_reddit_html_projection_delegated_adversarial_code_review_prompt_v0.md
  scope: >
    De-correlated adversarial review-and-patch of the old Reddit HTML
    static-projection and Reddit .json refusal slice of Candidate URL Intake.
  target_branch: ecr-sp3-timing-deriver-slice1
  target_head: 14490ce878946f5f2073cabd27c5be0389ee147f

lane_binding:
  overlay_status: provisional_opt_in
  operating_contract_pointer: .agents/workflow-overlay/delegated-review-patch.md
  review_lanes_invoked:
    - workflow-code-review (implementation, tests, package boundary)
    - workflow-adversarial-artifact-review (product/decision-doc claims governing this slice)
  mode: base-subagent (controller receiving and executing the commission)
  patch_authority: bounded target files only

actor_model_family_receipt:
  author_home_model_family: OpenAI/Codex current lane
  controller_model_family: Anthropic/Claude (claude-sonnet-4-6)
  current_receiving_actor_role: controller
  dispatch_mode: external-controller-courier
  de_correlation_status: satisfied
  de_correlation_basis: >
    Anthropic/Claude != OpenAI/Codex. Who-constraint satisfied.
    Not a model quality recommendation. Not runtime model routing.
```

---

## 2. Source Context Status

`SOURCE_CONTEXT_READY`

Authority sources loaded:
- `AGENTS.md` (via system context)
- `.agents/workflow-overlay/README.md`
- `.agents/workflow-overlay/delegated-review-patch.md`
- `.agents/workflow-overlay/source-of-truth.md`
- `.agents/workflow-overlay/review-lanes.md`
- `.agents/workflow-overlay/validation-gates.md`
- `.agents/workflow-overlay/decision-routing.md`
- `.agents/workflow-overlay/source-loading.md`
- `.agents/workflow-overlay/prompt-orchestration.md`
- `docs/product/data_capture_spine_candidate_url_intake_contract_v0.md`
- `docs/product/data_capture_spine_reddit_candidate_url_intake_crawler_architecture_v0.md`
- `docs/decisions/data_capture_spine_reddit_candidate_url_intake_default_policy_decision_v0.md`
- `docs/decisions/reddit_candidate_intake_no_live_access_delegated_review_adjudication_decision_v0.md` (present; read)

Target files loaded:
- `orca-harness/capture_spine/reddit_candidate_intake/validation.py`
- `orca-harness/capture_spine/reddit_candidate_intake/projection.py`
- `orca-harness/capture_spine/reddit_candidate_intake/__init__.py`
- `orca-harness/tests/unit/test_reddit_candidate_intake.py`
- `orca-harness/tests/contract/test_reddit_candidate_intake_contract.py`

Adjacent reads (minimal, needed to understand import boundary):
- `orca-harness/capture_spine/reddit_candidate_intake/models.py`
- `orca-harness/capture_spine/reddit_candidate_intake/writer.py`

Prior review context: `reddit_candidate_intake_no_live_access_delegated_review_adjudication_decision_v0.md`
confirmed that an earlier `no_live_access` slice review was adjudicated `ACCEPT_WITH_DEFERRED_MINORS` and
three changes were kept: extended `FORBIDDEN_OUTPUT_FIELDS`, added `selftext`/`selftext_html`/`body_html`
regression test, added `http`/`subprocess`/`pycurl`/`websocket`/`websockets`/`ftplib` to forbidden import
roots. Current working tree includes those accepted patches plus projection-slice additions (projection
function, three new unit tests). Dirty-state allowance: permitted by commission.

Input file state at time of review (working tree): differs from commission's pinned hashes because the
prior adjudication's patches and the projection slice additions are present. This is the expected and
explicitly permitted dirty-state.

---

## 3. Cynefin Routing Result

Commission's expected routing confirmed:

```
Smallest complete outcome: review the old Reddit HTML static-projection and Reddit .json refusal slice
  for boundary leaks, fake-pass tests, and doc/code mismatch; patch missing undeclared-surface test
  and extend FORBIDDEN_OUTPUT_FIELDS with author field names.
Regime: complicated.
Why: all implementation can be reasoned from current sources; no live access or design-level unknowns.
Decomposition: risk-first mixed code/doc review.
Current bottleneck: proving the projection helper cannot smuggle in live access, raw HTML persistence,
  body/comment/user leakage, or undeclared surfaces.
Riskiest assumption: tests pass because the happy-path fixture is narrow, not because forbidden
  input surfaces and outputs are mechanically impossible.
Stop or pivot condition: if a correct fix requires live Reddit access, CloakBrowser, .json intake,
  broad traversal, or source-access doctrine change → NEEDS_ARCHITECTURE_PASS.
Allowed next move: review and bounded patch of the listed target files only.
Disallowed next move: live Reddit access, .json intake, thread body/comment retrieval,
  user/profile capture, CloakBrowser/proxy execution, Source Capture Packet generation,
  ECR/Cleaning/Judgment work, fixture admission, Data Capture handoff claims.
```

No `NEEDS_ARCHITECTURE_PASS` triggered. All findings are patch-level or deferred-minor.

---

## 4. Findings

Ordered by severity: critical → major → minor.

### Critical Findings

**None.**

All primary boundary checks verified:
- Reddit `.json` URL refusal at every intake input surface: present and mechanically enforced
- Thread-page refusal at intake input: present and tested
- No live HTTP/browser/socket/Armory imports anywhere in the package: enforced by contract test
- Forbidden output field denylist covering body/comment/profile/packet/ECR/Cleaning/Judgment: present
- Projection accepts only `html_text: str` parameter; never performs network calls
- Projection emits only `list[CandidateThreadUrlRow]` typed output
- No raw HTML, parser output, screenshots, cookies, session state in any output path
- `source_surface` allowlist enforcement present in projection function
- Cap uses `max_threads_per_subreddit` and does not carry completeness language
- Empty results and blocked/refused inputs are honest outcomes

---

### Major Findings

---

**M-1: Missing test for `source_surface` allowlist enforcement in `project_old_reddit_html_listing`**

- **Location:** `orca-harness/tests/unit/test_reddit_candidate_intake.py` — no existing test for
  `undeclared_candidate_surface` error path
- **Issue:** `projection.py:30-34` enforces that `source_surface` must be in
  `envelope.candidate_surface_allowlist` and raises
  `RedditCandidateIntakeError("undeclared_candidate_surface", ...)`. This check has no unit test.
  The commission review criteria explicitly states: *"Tests fail on … undeclared source surfaces."*
  The enforcement can be accidentally removed without any test catching the regression.
- **Evidence:**
  - `projection.py:30`: `if source_surface not in envelope.candidate_surface_allowlist:`
  - `projection.py:32`: `raise RedditCandidateIntakeError("undeclared_candidate_surface", ...)`
  - No test in `test_reddit_candidate_intake.py` calls `project_old_reddit_html_listing` with a
    surface not in the allowlist or asserts `undeclared_candidate_surface`.
  - Commission criteria: *"source_surface is enforced against the declared run-envelope allowlist"*
    and *"Tests fail on … undeclared source surfaces."*
    (`reddit_candidate_intake_old_reddit_html_projection_delegated_adversarial_code_review_prompt_v0.md`)
- **Impact:** A key boundary guard — the only mechanism preventing a caller from projecting via
  an undeclared surface — has no regression test. A future refactor could silently remove or
  bypass the check.
- **Minimum closure condition:** A test must exist that calls `project_old_reddit_html_listing` with a
  `source_surface` not in `candidate_surface_allowlist` and asserts
  `RedditCandidateIntakeError` with `code == "undeclared_candidate_surface"`.
- **Next authorized action:** Patch within the bounded target scope. ✓ **Patched.**
- **Patched:** Yes — see unified diff below.

---

### Minor Findings

---

**m-5-new: `FORBIDDEN_OUTPUT_FIELDS` missing Reddit canonical author-identity field names**

- **Location:** `orca-harness/capture_spine/reddit_candidate_intake/validation.py:41-73`
- **Issue:** `FORBIDDEN_OUTPUT_FIELDS` covers body/comment/profile/session/packet fields but does
  not include `author` or `author_fullname`, which are Reddit's canonical API field names for
  post and comment author identity. The architecture explicitly states "user names, author rows"
  as non-outputs. The typed dataclass output path (`CandidateThreadUrlRow` etc.) is the primary
  protection and correctly excludes author fields. However, the secondary denylist check
  (applied to arbitrary output mappings via `assert_no_forbidden_output_fields`) would not catch
  an `author` key injected into an untyped dict. The prior review extended the denylist with
  `selftext`/`selftext_html`/`body_html`; this is the same class of gap.
- **Evidence:**
  - `validation.py:41-73`: `FORBIDDEN_OUTPUT_FIELDS` does not contain `"author"` or `"author_fullname"`.
  - Reddit crawler architecture, Explicit Non-Outputs: *"user profile data; ordinary-person dossier data"*
    (`data_capture_spine_reddit_candidate_url_intake_crawler_architecture_v0.md`)
  - Prior adjudication residual-risk note: *"The accepted denylist hardening is not a full design
    guarantee for arbitrary hand-built dictionaries."*
    (`reddit_candidate_intake_no_live_access_delegated_review_adjudication_decision_v0.md`)
- **Impact:** Low. Typed output path is the primary guard. The denylist is secondary. However,
  the gap is inconsistent with the prior review's stated approach of extending the denylist with
  Reddit-specific field names that aren't covered by generic terms.
- **Minimum closure condition:** `author` and `author_fullname` present in `FORBIDDEN_OUTPUT_FIELDS`.
- **Next authorized action:** Patch within bounded target scope. ✓ **Patched.**
- **Patched:** Yes — see unified diff below.

---

**m-1 [DEFERRED — no change]: Dead no-op `return` in `validate_run_envelope` after outbound check**

- **Location:** `validation.py:105-107`
- Code: `if CandidateSurface.OUTBOUND_LINKS in envelope.candidate_surface_allowlist: return`
- Already identified and deferred by prior adjudication. Confirmed still present unchanged.
  No new evidence warranting escalation.
- **Next authorized action:** Owner policy decision (deferred per prior adjudication).

**m-2 [DEFERRED — no change]: Dead no-op `return` in `validate_promotion_receipt`**

- **Location:** `validation.py:173-174`
- Code: `if receipt.decision_frame_or_capture_unit_authority and receipt.capture_not_yet_authorized: return`
- Already identified and deferred by prior adjudication. Confirmed still present unchanged.
- **Next authorized action:** Owner policy decision (deferred per prior adjudication).

**m-3 [DEFERRED / OUT OF SCOPE]: `ValueError` instead of `RedditCandidateIntakeError` in `writer.py`**

- **Location:** `writer.py:50`
- Code: `raise ValueError("outbound URL candidates require separate source-family intake")`
- Already identified and deferred by prior adjudication. `writer.py` is not in the bounded
  target patch scope for this commission. Flag only.
- **Next authorized action:** Owner cleanup decision; `writer.py` patch requires a separate commission.

**m-4 [DEFERRED — no change]: No upper cap ceiling enforcement in `validate_run_envelope`**

- **Location:** `validation.py:88-104`
- Caps are validated as positive but not checked against `DEFAULT_CAPS` maxima. Already
  identified and deferred by prior adjudication. Confirmed still present unchanged.
- **Next authorized action:** Owner policy decision (deferred per prior adjudication).

---

## 5. Unified Diff

```diff
diff --git a/orca-harness/capture_spine/reddit_candidate_intake/validation.py b/orca-harness/capture_spine/reddit_candidate_intake/validation.py
--- a/orca-harness/capture_spine/reddit_candidate_intake/validation.py
+++ b/orca-harness/capture_spine/reddit_candidate_intake/validation.py
@@ FORBIDDEN_OUTPUT_FIELDS set (validation.py:41-73) @@
     "source_quality_score",
+    "author",
+    "author_fullname",
 }

diff --git a/orca-harness/tests/unit/test_reddit_candidate_intake.py b/orca-harness/tests/unit/test_reddit_candidate_intake.py
--- a/orca-harness/tests/unit/test_reddit_candidate_intake.py
+++ b/orca-harness/tests/unit/test_reddit_candidate_intake.py
@@ after test_thread_pages_are_not_intake_input_surfaces @@
+def test_projection_rejects_undeclared_candidate_surface() -> None:
+    with pytest.raises(RedditCandidateIntakeError) as exc_info:
+        project_old_reddit_html_listing(
+            html_text="<html></html>",
+            envelope=_envelope(
+                candidate_surface_allowlist=(CandidateSurface.SUBREDDIT_LISTING,)
+            ),
+            source_url="https://old.reddit.com/r/orca_test/top/",
+            timestamp="2026-06-06T00:00:00Z",
+            source_surface=CandidateSurface.REDDIT_SEARCH_LISTING,
+        )
+
+    assert exc_info.value.code == "undeclared_candidate_surface"
+
```

---

## 6. Per-Change Source Citations

**Change 1: Add `author` and `author_fullname` to `FORBIDDEN_OUTPUT_FIELDS`**

Citation sources (neutral, decision-sufficient):

- Reddit crawler architecture, Explicit Non-Outputs section:
  *"This lane must not output, preserve, derive, or imply: [...] user profile data; ordinary-person
  dossier data"* — `data_capture_spine_reddit_candidate_url_intake_crawler_architecture_v0.md`
- Parent contract, Explicit Non-Outputs section: *"user profile data; ordinary-person dossier data"*
  — `data_capture_spine_candidate_url_intake_contract_v0.md`
- Prior adjudication accepted pattern: extended `FORBIDDEN_OUTPUT_FIELDS` with Reddit-specific
  body field names (`selftext`, `selftext_html`, `body_html`).
  — `reddit_candidate_intake_no_live_access_delegated_review_adjudication_decision_v0.md`
- `author` and `author_fullname` are Reddit's canonical API field names for post/comment author
  identity. They are not covered by the existing `user_profile`/`user_data` entries, which
  describe broader profile objects rather than the author string field on posts and comments.

**Change 2: Add `test_projection_rejects_undeclared_candidate_surface`**

Citation sources (neutral, decision-sufficient):

- Default policy decision, Access-Method Default section: *"The first no-live implementation
  surface is old Reddit HTML listing/search projection from static fixtures."* Confirms that
  `source_surface` governs which surfaces are in scope for a given run.
  — `data_capture_spine_reddit_candidate_url_intake_default_policy_decision_v0.md`
- Default policy decision, Default Candidate Surfaces section: surfaces are explicitly divided
  into default-on and default-off, requiring the operator to declare surfaces in
  `candidate_surface_allowlist`.
- `projection.py:30-34` implements `source_surface` enforcement against allowlist.
  The review criteria: *"source_surface is enforced against the declared run-envelope allowlist"*
  and *"Tests fail on … undeclared source surfaces."*
  — Review commission prompt.
- No existing test in `test_reddit_candidate_intake.py` covers the `undeclared_candidate_surface`
  error path. Gap confirmed by direct file inspection.

---

## 7. Controller Verdict and Residual-Risk Note

**Verdict: PASS_WITH_DEFERRED_MINORS**

The old Reddit HTML static-projection and Reddit `.json` refusal slice satisfies all stated
boundary requirements after the two bounded patches:

1. Reddit `.json` URLs are mechanically refused at every intake input surface. The
   `_is_reddit_json_url` check is called at the head of both `validate_old_reddit_html_listing_input_url`
   and `validate_old_reddit_thread_url` before any other check, including the thread-page guard.
   The `.json` check applied to HREFs extracted from HTML during projection occurs via
   `validate_old_reddit_thread_url` being called on every canonical URL produced by
   `_canonical_old_reddit_thread_url` — `.json` thread HREFs that survive canonicalization are
   refused with `reddit_json_input_forbidden`.

2. Thread pages are refused as intake input via the explicit `/comments/` guard in
   `validate_old_reddit_html_listing_input_url` (checked after `.json`, before the regex).

3. Old Reddit thread URLs are valid candidate thread outputs and are produced correctly by
   `_canonical_old_reddit_thread_url` → `validate_old_reddit_thread_url`.

4. Projection is purely static: `html.parser.HTMLParser` on `html_text: str`. No imports from
   HTTP, browser, socket, Armory, or any network module anywhere in the package.

5. Projection emits `list[CandidateThreadUrlRow]` only. The parser extracts only `href` and
   `title` from `<a class="title">` links. Author links (`<a class="author">`), `data-selftext`
   attributes, comment trees, and profile data are not captured at the parser level.

6. `source_surface` enforcement is present in `projection.py` and now tested (M-1 patched).

7. Contract test (`test_reddit_candidate_intake_has_no_network_browser_or_armory_imports`)
   performs static AST analysis over all `.py` files in the package against
   `FORBIDDEN_IMPORT_ROOTS`. This is a mechanical proof that the package cannot invoke network
   or Armory code even if a future contributor inadvertently adds an import.

**Residual risks:**

- The `FORBIDDEN_OUTPUT_FIELDS` denylist is not a complete enumeration of all possible user-data
  field names. It is a secondary check for untyped dict output; the primary protection is the
  typed dataclass output path (`CandidateThreadUrlRow` etc.). If a future runner produces
  arbitrary dicts, the denylist will need further extension. The CA's prior note on this remains
  accurate.
- The deferred minors (m-1 through m-4) are confirmed still present. None of them create a live
  boundary leak in the current projection slice. They represent implementation tidiness items.
- `writer.py:50` raises bare `ValueError` for the outbound-row non-intake guard. This is out of
  the bounded patch scope. A future caller relying on `RedditCandidateIntakeError` for unified
  error handling would need a separate patch.

---

## 8. Validation Run Status

**Command run:**
```
python -m pytest -p no:cacheprovider tests/unit/test_reddit_candidate_intake.py tests/contract/test_reddit_candidate_intake_contract.py -v
```

**Run location:** `orca-harness/` working directory, `ecr-sp3-timing-deriver-slice1` branch.

**Result:**
```
============================= test session starts =============================
platform win32 -- Python 3.12.7, pytest-8.4.2, pluggy-1.6.0
collected 14 items

tests\unit\test_reddit_candidate_intake.py ............                  [ 85%]
tests\contract\test_reddit_candidate_intake_contract.py ..               [100%]

14 passed in 0.09s
```

**Count context:** 10 tests were present at prior adjudication. Three additional tests were added
in the projection implementation slice (`test_builds_candidate_rows_and_provenance_only`,
`test_projects_static_old_reddit_html_listing_to_candidate_rows_only`,
`test_same_run_traversal_is_rejected`). This review adds 1 (`test_projection_rejects_undeclared_candidate_surface`).
Total: 14.

**Validation status:** PASS. All 14 tests pass post-patch.

**Validation gaps:**
- No live-Reddit integration test is present or expected at this no-live-access slice.
- No test directly exercises the case of a `.json` HREF that includes `/comments/` (e.g.,
  `/r/sub/comments/abc.json`). Static analysis confirms this would be caught by
  `validate_old_reddit_thread_url` → `reddit_json_input_forbidden`, but the test corpus does not
  include this specific case. Not a current blocker; the code path is mechanically covered.
- Numeric cap ceiling not enforced (m-4, deferred). No test for this.

---

## 9. Off-Scope Flags

The following items were identified during review but are outside the bounded patch scope:

- **`writer.py:50` — bare `ValueError`**: `writer.py` is not in the target list. See m-3 above.
  Requires a separate commission scoped to `writer.py`.
- **Dead-branch tail in `validate_run_envelope`** (m-1) and **`validate_promotion_receipt`** (m-2):
  Both are in `validation.py` (in scope), but were explicitly deferred by the prior adjudication
  decision as owner-policy items. This controller does not re-escalate them.
- **Numeric cap ceiling unenforced** (m-4): In `validation.py` (in scope), but deferred by prior
  adjudication. This controller does not patch it.

---

## 10. CA Adjudication Packet

```yaml
ca_adjudication_packet:
  status: awaiting_chief_architect_adjudication
  non_claim: >
    This diff, these citations, and this verdict are claims to adjudicate, not
    premises to inherit. Nothing in this report is owner acceptance, validation
    proof, readiness, deployment, live Reddit authorization, Source Capture Armory
    authorization, Data Capture handoff authorization, or permission to keep any
    patch without Chief Architect adjudication.

  proposed_changes:

    - id: PC-01
      target: orca-harness/capture_spine/reddit_candidate_intake/validation.py
      change: >
        Add "author" and "author_fullname" to FORBIDDEN_OUTPUT_FIELDS.
      citation: >
        Reddit crawler architecture Explicit Non-Outputs ("user profile data;
        ordinary-person dossier data"); prior adjudication pattern of extending
        denylist with Reddit-specific field names.
      intended_closure: >
        FORBIDDEN_OUTPUT_FIELDS includes Reddit canonical author-identity field
        names, consistent with the non-output requirement and the prior denylist
        extension pattern.
      adjudication_readiness: ready for CA accept / modify / reject

    - id: PC-02
      target: orca-harness/tests/unit/test_reddit_candidate_intake.py
      change: >
        Add test_projection_rejects_undeclared_candidate_surface: calls
        project_old_reddit_html_listing with a source_surface not in the envelope's
        candidate_surface_allowlist; asserts RedditCandidateIntakeError with
        code == "undeclared_candidate_surface".
      citation: >
        Default policy decision Default Candidate Surfaces section (surfaces require
        explicit allowlisting); commission review criteria ("Tests fail on ...
        undeclared source surfaces"); projection.py:30-34 check has no prior test.
      intended_closure: >
        The undeclared_candidate_surface enforcement is regression-tested.
      adjudication_readiness: ready for CA accept / modify / reject

  deferred_findings_not_patched:
    - id: m-1
      description: Dead no-op return in validate_run_envelope after outbound check
      status: deferred per prior adjudication; no change recommended here
    - id: m-2
      description: Dead no-op return in validate_promotion_receipt
      status: deferred per prior adjudication; no change recommended here
    - id: m-3
      description: ValueError instead of RedditCandidateIntakeError in writer.py
      status: out of bounded patch scope; flag for separate commission
    - id: m-4
      description: No upper cap ceiling enforcement in validate_run_envelope
      status: deferred per prior adjudication; no change recommended here

  design_level_blocker: none
  needs_architecture_pass: false
```

---

## 11. Review-Use Boundary

This delegated review-and-patch result is decision input only. The controller's diff, citations,
and verdict are claims to adjudicate, not premises to inherit.

This report is **not**:
- owner acceptance
- validation proof or readiness
- deployment, staging, or commit authorization
- live Reddit authorization
- Source Capture Armory authorization
- Data Capture handoff authorization
- fixture admission
- permission to keep any patch without Chief Architect adjudication
