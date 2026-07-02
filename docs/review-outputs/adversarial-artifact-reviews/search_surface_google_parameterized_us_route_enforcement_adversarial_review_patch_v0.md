# Search-Surface Google Parameterized-US Route Enforcement — Adversarial Code/Artifact Review v0

```yaml
retrieval_header_version: 1
artifact_role: Adversarial review output
scope: >
  De-correlated adversarial code/artifact review of the parameterized Google
  search-surface route guard, its doctrine record, and repository wiring on
  branch codex/search-param-us-enforcement.
use_when:
  - Adjudicating whether the Google search-surface route enforcement patch is effective.
  - Checking which checker/doctrine defects were found and their minimum closure conditions.
authority_boundary: retrieval_only
open_next:
  - docs/decisions/search_surface_google_parameterized_us_capture_route_v0.md
  - .agents/hooks/check_search_surface_google_route.py
  - .agents/workflow-overlay/validation-gates.md
stale_if:
  - The branch changes materially after this review.
  - The Google search-surface route decision or its enforcement placement changes.
```

Non-claim (also keeps this report inside the route shape it reviews):
**US-parameterized is not physically US-local.** This report is route-shape and
code-correctness review only. It is not validation, readiness, source
sufficiency, demand proof, Judgment evidence, Product Lead evidence, or
physical-locality proof.

## 1. Provenance

- `reviewed_by`: Anthropic / Claude (Opus 4.8), de-correlated controller.
- `authored_by`: OpenAI / Codex (branch author per commission receipt).
- Workspace: `C:\Users\vmon7\Desktop\projects\orca\worktrees\search-param-us-enforcement`
- Branch: `codex/search-param-us-enforcement` @ `91bfce53` (base `c4cc9e3e`).
- Branch state: committed; working tree clean. The committed branch diff is the review target.

## 2. Actor / Model-Family Receipt

```yaml
actor_model_family_receipt:
  author_home_model_family: OpenAI/Codex
  controller_model_family: Anthropic/Claude (Opus 4.8)
  current_receiving_actor_role: controller
  dispatch_mode: external-controller-courier
  access_mode: repo            # repo access present; repo PATCH mode NOT operator-selected -> findings-only per prompt default
  de_correlation_bar: cross_vendor_discovery
  same_vendor_rationale: n/a
  de_correlation_status: satisfied   # author OpenAI/Codex != controller Anthropic/Claude
```

Cross-vendor discovery is satisfied (author and controller vendors differ), so
the no-new-seam discovery bar is claimable for the read scope below.

## 3. Source Context

`SOURCE_CONTEXT_READY` — with disclosed exclusions.

Loaded in full: the checker `check_search_surface_google_route.py`; the decision
record; the full diffs of all 9 changed files; `.github/workflows/ci.yml`;
`.claude/settings.json`; `.agents/workflow-overlay/validation-gates.md`
(enforcement-placement + new gate); `.agents/workflow-overlay/delegated-review-patch.md`;
overlay `README.md`. Executed the checker (`--selftest`, `--strict --base`,
`--changed --strict`) and crafted-input probes; validated both JSON files.

Disclosed exclusions (read-only context not separately opened):
`decision-routing.md`, `source-of-truth.md`, `source-loading.md`,
`retrieval-metadata.md`, `artifact-roles.md`, `review-lanes.md`,
`prompt-orchestration.md`. None of the findings below depend on these; lane and
de-correlation framing was taken from `delegated-review-patch.md` and the
overlay README index. No source conflicts observed.

## 4. Findings (severity order)

Illustrative URLs below are written **without** the `https://` scheme on
purpose, so this report does not itself match the checker's URL detector.

### F1 — MAJOR — IP-leak detector misses real Google block pages (false negative on the highest-stakes rule)

- Where: `.agents/hooks/check_search_surface_google_route.py:137-143` (`has_google_sorry_ip_leak`).
- Evidence: the rule fires only when **all three** substrings are present, including the literal `google.com/search`. Executed probe — unusual-traffic banner + an IP-address line + a `google.com/sorry/index` URL (i.e. **no** `/search`) → `[]` (no finding). The contrasting probe with a `/search` URL present → `GOOGLE_SORRY_IP_LEAK` fires. Real Google block pages are served from `google.com/sorry/…`, not `/search`, so the exact dangerous artifact — a preserved block page exposing an exit IP — is the case that escapes detection.
- Risk: the rule whose entire purpose is to stop exit-IP leakage into durable docs fails open on the most realistic capture. This is a capture-efficacy hole, not a cosmetic one.
- Minimum closure: detect Google block context **without** requiring `/search` — key on the unusual-traffic marker and/or the `/sorry/` path — and pair it with a real IP signal (see F3). Keep scope to in-scope durable docs; `_scratch`/`snapshots` stay excluded (they are the doctrine's sanctioned quarantine for such pages, correctly handled).
- Patched: no. Next authorized action: apply within editable scope on patch-mode selection; re-run `--selftest` with a `/sorry/`+IP fixture.

### F2 — MAJOR — correctly-parameterized URLs flagged as missing params when inline-coded (false positive → CI false-block)

- Where: `check_search_surface_google_route.py:54-57` (`_GOOGLE_SEARCH_URL_RE`) and `:108` (`rstrip(".,;")`).
- Evidence: the URL char class `[^\s<>)\"']*` does not exclude a backtick or `]`. Executed probe — a fully parameterized URL wrapped in backticks → `GOOGLE_SEARCH_ROUTE_PARAMS`. The trailing backtick is captured into the query, so the last param parses as `pws=0` + backtick and the exact `pws=0` match fails. Inline-coding URLs in backticks is standard in durable markdown; under the `--strict` CI gate this fails an otherwise-correct doc.
- Risk: this is precisely the efficacy bar's "ineffective if … too broad and likely to block ordinary durable docs" mode. A correct author gets a red CI.
- Minimum closure: add a backtick and `]` (consider `|` and `*`) to the regex exclusion class, or strip trailing markdown punctuation alongside `.,;`. Add a backtick fixture to `--selftest`.
- Patched: no.

### F3 — MODERATE — IP-leak detector requires the literal `IP address:` string

- Where: `check_search_surface_google_route.py:137-143`.
- Evidence: executed probe — "Your IP address is 12.34.56.78" (no colon) → no `GOOGLE_SORRY_IP_LEAK`. Real block pages and screenshots vary in phrasing/localization. The detector keys on one fixed substring.
- Risk: compounds F1 — the IP rule is brittle on two of its three AND-conditions, so even a `/search`-referencing block page can slip past on phrasing alone.
- Minimum closure: detect an IPv4 (and/or IPv6) literal by regex as the IP signal; keep the block-context marker as the gating signal. Beware over-broadening (see Residual).
- Patched: no.

### F4 — MODERATE — recommended `--changed --strict` smoke is vacuous on a committed/clean tree (validation-sufficiency gap; Review Q12)

- Where: the review prompt's `Required Validation` block; operationally `changed_paths` / `run_changed` (`:218-226`, `:317-327`).
- Evidence: `--changed` diffs the working tree vs `HEAD` plus untracked files. This branch's work is committed and the tree is clean, so `--changed --strict` returned `OK (0 findings)` **vacuously — it analyzed nothing**. Only `--strict --base c4cc9e3e…` exercised the committed diff (also `OK (0 findings)`, confirming the branch's own docs genuinely pass).
- Risk: a reviewer/CI relying on `--changed --strict` as the branch smoke gets false confidence; the meaningful local check for a committed branch is `--strict --base <merge-base>` or `--check <file>`.
- Minimum closure: in the decision record / prompt validation list / hook README, recommend `--strict --base <merge-base>` (or `--check` on the changed docs) for verifying a committed branch; reserve `--changed` for pre-commit working-tree use. CI already uses `--strict`, so CI itself is correct.
- Patched: no.

### F5 — MINOR — `gl=US` (uppercase) false positive and internal casing inconsistency

- Where: `:113-121` (`missing_required_params`, case-sensitive value compare) vs `:124-130` (`has_us_parameterized_google_surface`, which lowercases `gl`).
- Evidence: executed probe — `gl=US` → `GOOGLE_SEARCH_ROUTE_PARAMS` (flagged missing `gl=us`). Google treats `gl` case-insensitively, and the two functions disagree on casing.
- Risk: minor false-block; partly defensible because the decision literally specifies lowercase `gl=us`, but the inconsistency is a latent smell.
- Minimum closure: pick one rule — normalize param values to lowercase before compare (accept `gl=US`) or document exact-lowercase intent — and align both functions.
- Patched: no.

### F6 — MINOR / RESIDUAL — live PostToolUse advisory misses shell-written docs (CI backstops)

- Where: `.claude/settings.json:38` matcher `Write|Edit|MultiEdit`; Codex `apply_patch|Edit|Write`.
- Evidence: a doc written via a `Bash`/`PowerShell` heredoc does not trigger the PostToolUse advisory; the `--strict` CI gate still catches it in the diff. This matches the sibling hooks' advisory-live + strict-CI design.
- Risk: low; the live nudge is best-effort by design, and CI is the real gate.
- Minimum closure: none required; optionally note the live/CI split in the hook README.
- Patched: no.

## 5. What is sound (recorded so the CA sees the solid base)

- `--selftest` passes 8/8; `.claude/settings.json` and `.codex/hooks.json` are valid JSON.
- The branch's own in-scope committed docs pass `--strict --base` (0 findings) — the patch does not self-trip its own gate.
- CI uses `actions/checkout@v4` with `fetch-depth: 0`, and the gate's base resolution (`origin/$GITHUB_BASE_REF` on PR, else `origin/main`) plus fail-open-on-unavailable **matches the sanctioned forward-only pattern** documented for `header_index --strict` (`validation-gates.md:243-249`). Review Q7 → correct and consistent.
- Scope prefixes + `EXCLUDED_PARTS` correctly exclude `_inbox`/`_scratch`/`snapshots`, code, and non-`.md` files; `_scratch`/`snapshots` exclusion is consistent with the decision's quarantine path. Review Q1 → sound.
- The decision record states the route, the required boundary, and the non-claims sharply; `intentionally_not_updated` justifies leaving `AGENTS.md`, the overlay README, and the capture playbook untouched. Review Q11 → no broader Capture/Scanning/Judgment/Product-Lead/playbook/prompt-orchestration update is required for this pilot; doing so would be scope creep.
- The decision record `open_next` capture-playbook path (`orca/product/spines/capture/core/source_capture_toolbox/source_capture_playbook_v0.md`) exists — no broken pointer.

## 6. Patch Summary

None. Findings-only: repo access is present, but the operator did not select
repo patch mode, so per the prompt's default no diff was authored.

## 7. Unified Diff

None (see §6).

## 8. Validation Commands And Observed Outputs

Run from the target workspace; checker derives repo root from its own path.

| Command | Observed |
| --- | --- |
| `check_search_surface_google_route.py --selftest` | `SELFTEST OK`, 8/8 PASS, exit 0 |
| `check_search_surface_google_route.py --strict --base c4cc9e3e…` | `OK (0 findings)`, exit 0 (real committed diff) |
| `check_search_surface_google_route.py --changed --strict` | `OK (0 findings)`, exit 0 — **vacuous** (clean tree; see F4) |
| `python -m json.tool .claude/settings.json` | valid |
| `python -m json.tool .codex/hooks.json` | valid |
| crafted-input probes via `analyze_text(...)` | F1 (`/sorry/`→`[]`), F2 (backtick→PARAMS), F3 (no-colon IP→no leak), F5 (`gl=US`→PARAMS) reproduced |

Not run (out of scope by commission): live Google, web, proxy, VPN, browser,
capture-packet commands. The broader gate suite
(`check_prompt_provenance`, `check_repo_map_freshness`, `header_index`,
`check_map_links`, `git diff --check`) was not run because no patch was authored;
they are owed after any patch.

## 9. Residual Risk

- Shape enforcement cannot prove what Google returned, logged-out state, localization, physical locality, or sufficiency — the decision record already states this; F1/F3 fixes do not change it.
- Broadening the IP/sorry detector (F1/F3) risks new false positives on docs that legitimately discuss an IP or describe the rule (including this report). Any patch must scope to the block-page context and be re-run against this report and the decision record to confirm no self-trip.
- `--strict` fails open if diff-scoping is unavailable; a CI history misconfig would silently skip the gate. This is consistent with sibling gates but is a shared latent risk worth one explicit owner acknowledgement.

## 10. Verdict

`ADVISORY_ONLY` (findings-only). Clearly marked: **repo access is present** (so
not `NO_REPO`), and **F1–F5 are patchable defects** (so not
`NO_PATCH_NEEDED`). No diff was authored because repo patch mode was not
operator-selected. None of the findings require `NEEDS_ARCHITECTURE_PASS` — F1–F5
are smallest-complete edits inside the editable scope (checker logic/regex and
the documented validation command), applyable on patch-mode selection.

These findings, and any later diff, are decision input only. The Chief
Architect / home lane adjudicates what is kept.

## 11. Home-Lane Patch Disposition - 2026-06-25

This section was added by the OpenAI/Codex home lane after the owner supplied the
findings-only delegated report back to Codex and selected action via the current
"read and act" request. The original delegated review above remains preserved as
findings-first decision input; this addendum records the follow-up patch and
validation disposition.

Patch authority used: home-lane patch on the existing
`codex/search-param-us-enforcement` branch. No Google, web, proxy, VPN, browser,
or capture-packet command was run.

Closure summary:

- F1 closed: block-page detection no longer requires `google.com/search`; it
  recognizes the route's block context and a nearby labeled IP signal.
- F2 closed: Google Search URL detection now stops before common Markdown
  delimiters, including backticks, brackets, emphasis markers, and pipe-table
  separators.
- F3 closed: IP detection now accepts labeled IP wording without requiring the
  exact colon form.
- F4 closed: the filed review prompt and hook README now use
  `--strict --base main` for committed-branch verification instead of relying on
  clean-tree `--changed --strict`.
- F5 closed: required route parameter comparison normalizes values before
  comparing, so `gl=US` is treated consistently with the route detector.

Validation observed after patch:

| Command | Observed |
| --- | --- |
| `python .agents/hooks/check_search_surface_google_route.py --selftest` | `SELFTEST OK`; includes block-path, labeled-IP, inline-code URL, uppercase-`gl`, and IP-without-block-context fixtures. |
| `python .agents/hooks/check_search_surface_google_route.py --changed --strict` | `OK (0 findings)`; includes this untracked report in the changed-file scan. |
| `python .agents/hooks/check_search_surface_google_route.py --strict --base main` | `OK (0 findings)` for the committed branch diff plus current tracked modifications. |
| `python -m json.tool .claude/settings.json` | valid JSON. |
| `python -m json.tool .codex/hooks.json` | valid JSON. |
| `python .agents/hooks/check_prompt_provenance.py --selftest` | `SELFTEST OK`. |
| `python .agents/hooks/check_repo_map_freshness.py --changed` | exit 0, no findings printed. |
| `python .agents/hooks/check_retrieval_header.py --changed --strict` | exit 0, no findings printed. |
| `python .agents/hooks/check_map_links.py --strict` | `OK (0 findings)`; 33 annotated nonresolving entries remain debt, not failures. |
| `git diff --check` | exit 0, no findings printed. |

Current verdict: `PATCHED_FOR_CA_ADJUDICATION_BY_HOME_LANE`. This is not a
validation, readiness, physical-locality, demand-proof, Judgment, or Product
Lead claim. US-parameterized is not physically US-local.
