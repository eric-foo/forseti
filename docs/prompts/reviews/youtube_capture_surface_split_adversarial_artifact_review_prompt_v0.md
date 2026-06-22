# YouTube Capture Surface Split — Cross-Vendor Delegated Adversarial Artifact Review Prompt v0

```yaml
retrieval_header_version: 1
artifact_role: Orca review prompt (cross-vendor delegated adversarial artifact review; no_repo)
scope: >
  Operator-couriered, cross-vendor, no_repo adversarial artifact review of the chat-authored
  "YouTube Capture Surface Split Architecture/Scoping Memo v0" under the provisional
  delegated review-and-patch convention. Findings-only (advisory); the home/CA model applies
  any accepted change and runs the required same-vendor post-patch recheck before keep.
use_when:
  - The operator pastes this prompt into a DIFFERENT-VENDOR model (non-Anthropic) to harden the memo.
authority_boundary: retrieval_only
open_next:
  - .agents/workflow-overlay/delegated-review-patch.md
  - .agents/workflow-overlay/review-lanes.md
  - .agents/workflow-overlay/prompt-orchestration.md
output_mode: paste-ready-chat
filed_artifact: docs/prompts/reviews/youtube_capture_surface_split_adversarial_artifact_review_prompt_v0.md
downstream_report: docs/review-outputs/adversarial-artifact-reviews/youtube_capture_surface_split_adversarial_artifact_review_v0.md
```

## Orca Preflight (this prompt)

```text
orca_start_preflight:
  agents_read: yes
  overlay_read: yes
  source_pack: custom (S0 overlay + delegated-review-patch.md + review-lanes.md + prompt-orchestration.md; capture sources cited by the memo)
  edit_permission: read-only           # the reviewer is no_repo advisory; it edits nothing
  target_scope: the verbatim memo embedded below (chat-authored, not persisted)
  dirty_state_checked: yes              # home worktree tree clean at author time
  repo_map_decision: not_needed         # review target is embedded inline; reviewer is repo-blind
  workspace: C:\Users\vmon7\Desktop\projects\orca\.claude\worktrees\xenodochial-greider-ec61aa
  branch_head: claude/xenodochial-greider-ec61aa @ 6f79445e (origin/main-aligned)
  controlling_source_state: overlay delegated-review-patch.md / review-lanes.md / prompt-orchestration.md = clean (matches last-fetched origin/main)
  doctrine_change: no                   # the reviewed memo is not doctrine; this prompt creates no doctrine
  output_mode: paste-ready-chat (durable artifact filed; chat carries a copy)
  validation_gates: prompt validation gates (prompt-orchestration.md) applied to THIS prompt; the review returns findings only
  external_source_boundary: jb / external workflow source is NOT Orca authority and is read-only; no import
  blocked_if_missing: none (operator-couriered no_repo render does not block on a missing actor receipt)
```

## Commission (Lane Binding)

- overlay_status: **provisional_opt_in** — available only by explicit CA commission (this is one); not a bound or machine-routable review lane; not mandatory.
- operating_contract_pointer: `.agents/workflow-overlay/delegated-review-patch.md` (the controller treats this convention as its contract).
- review_lane: **artifact** → `workflow-adversarial-artifact-review` (the target is a non-code architecture/scoping memo).
- access: **no_repo** — the target is chat-authored and not persisted; the reviewer has no repository access. The reviewer is **advisory-only: it returns findings, NOT a diff, and patches nothing.** The home/CA model applies any accepted change within the bounded scope and then runs the **required bounded same-vendor post-patch recheck** before anything is kept.
- mode: base-subagent (single de-correlated controller; no split-executor).
- actor_model_family_receipt:
  - author_home_model_family: **Anthropic / Claude** (memo authored by `claude-opus-4-8` via three Claude planning subagents; the CA-adjudicator is also Claude — this is exactly why a same-vendor self-review is blind-spot-correlated).
  - controller_model_family: **a DIFFERENT vendor — non-Anthropic** (e.g., an OpenAI or Google-lineage model). `operator_to_fill`: record the exact model+version you paste into.
  - current_receiving_actor_role: **controller** (you, the pasted-into model). You do **not** dispatch or launch another reviewer.
  - dispatch_mode: external-controller-courier (human paste).
  - de_correlation_bar: **cross_vendor_discovery** (the discovery bar; required to claim the "survives an adversarial review with no new seam" standard).
  - de_correlation_status: **satisfied ONLY IF** the paste target is genuinely non-Anthropic. If you are a Claude-family model, de-correlation is **defeated**: drop to `same_vendor_sanity`, record `same_vendor_rationale`, and do **not** claim the no-new-seam standard.
- why_read_only_insufficient: the artifact author and the CA-adjudicator are the same vendor (Claude). Self-review structurally misses the author's own blind spots. The memo gates a high-stakes architecture decision (split vs. unified YouTube capture lane) and carries overclaim/underclaim risk on probe-hypothesis labelling. A cross-vendor adversarial pass before the CA commits is the value.
- off_scope: read-only — flag, don't act. You are reviewing **only** the embedded memo's claims, structure, and decision soundness. You cannot and must not assert repository facts; the home CA verifies every source citation against the live repo (see no_repo limitation).

## Roles (who-constraints, NOT model recommendations)

- **author / CA / home model** (Anthropic/Claude): authored the memo; adjudicates your findings; owns what is kept; holds final veto.
- **controller** (you, different vendor): judgment, findings, neutral-but-decision-sufficient citations to the memo's own text, a verdict *relative to the memo*, and a residual-risk note. Your verdict is decision input, **not** final over the CA.
- No patch executor (no_repo: nothing is patched by the reviewer).

This commission carries **no recommended-model block** and makes no runtime-model recommendation, ranking, or selection. The vendor difference is a who-constraint only.

## Source-Gated Method Contract (follow in order)

1. **REFERENCE-LOAD only — do not APPLY yet.** Read the two method blocks below as procedural guidance. Before source readiness, use them only to prepare a neutral source-reading lens. Do not produce a frame, finding, ranking, verdict, or recommendation yet.

   **(a) Deep-thinking framing method (REFERENCE-LOAD).** Before listing findings, frame: the memo's actual decision problem (split vs. unified YouTube capture lane), its material failure modes, and the decision criteria the memo should be judged against. This framing improves risk coverage; it does not widen scope, authorize any change, or turn the review into product planning.

   **(b) Adversarial artifact review method (REFERENCE-LOAD — portable, inlined because you are repo-blind).**
   - Treat the artifact as guilty until proven sound. Attack material, decision-relevant failure modes; do not soften a real failure mode because remediation would be awkward.
   - For each finding: state the claim under attack, the evidence in the artifact's own text, why it is a defect, severity (`critical` | `major` | `minor`, priority only — not approval/rejection authority), `minimum_closure_condition` (the required end state, not how to implement), and `next_authorized_action`.
   - Separate genuine defects from style/nits. Name non-findings you checked and cleared. Name not-proven boundaries.
   - You are findings-first. You may give **advisory remediation direction**, but you must **not** emit a diff, a `patch_queue_entry`, or executor-ready how-to (this is a no_repo advisory pass).
   - Citations are **neutral in tone but decision-sufficient in substance**: quote/point to the memo's own lines, no advocacy. Put your argument in the verdict and residual note, not the citations.

2. **SOURCE-LOAD.** Your source context is: the **verbatim review target** (the memo) plus the **commission context** (mission/fitness reference, hard boundaries, split policy, required-output structure) — all embedded below. The memo also asserts repository facts (e.g., "no YouTube folder exists," "migration plan reserves `youtube/`"); treat these as **the memo's claims to test for internal consistency and honest labelling**, not as facts you can independently verify (you have no repo). Source-citation byte-accuracy is the CA's verification job.

3. **Declare `SOURCE_CONTEXT_READY`** (or `SOURCE_CONTEXT_INCOMPLETE` naming what is missing).

4. **APPLY** the deep-thinking framing, then the adversarial method, to the loaded context. Synthesize and verify your findings against the memo's own text.

## Fitness Reference (alignment axis to ATTACK — not a pass-if-matches bar)

- **Goal (what the memo is for):** Adjudicate the YouTube capture split so Orca can gather enough source-native **public** YouTube creator/video/comment metadata to support creator-momentum and anti-bot / data-integrity analysis (views, engagement, cadence, commenters), while preserving receipts and limitations tightly enough that **Orca does not overclaim**.
- **Done looks like:** a source-backed memo that (1) correctly adjudicates current state, (2) gives a defensible default split decision with evidence and residual risk, (3) provides both surface route cards as honest probe hypotheses with live-probe gates, (4) defines a shared shape + receipts, and (5) names what it cannot prove — with no architecture fact smuggled in as a hypothesis and no probe-decidable fact left vaguely deferred.
- Pointer-preferred upstream: the commissioning handoff prompt's Mission + Split Policy; Orca split-trigger criteria (a)–(e) below. **You must also attack whether this goal/signal is itself right** — e.g., is "one lane, two cards" the correct frame, or is it over/under-structured?

## Embedded Commission Context (for the reviewer)

**Hard boundaries the memo had to honor (test whether it did):** read-only planning, no code, no live YouTube, no folder creation; do not plan scraping behind an auth/access-control wall; do not defeat auth; do not accept/echo cookies/storage-state/passwords/proxy creds/exit IPs; **do not claim bot/fake classification from comments alone** (allowed ceiling: "source data suitable for later corroboration, with limitations"); do not assume IG/TikTok route details transfer to YouTube; do not assume Shorts and long-form share a comments route until a probe proves it; label anything depending on an unobserved source field as a PROBE HYPOTHESIS.

**Split policy (default posture):** one YouTube platform family, one capture lane, two surface route cards. Recommend a code split only if a source-backed probe shows at least one of: (a) materially different source-native fields/timestamp semantics between surfaces; (b) comments fetched/paginated through incompatible route shapes; (c) anti-bot/login-wall behavior differing enough that one cooldown policy hides failures; (d) one surface GO while the other PARTIAL/NO-GO/CATALOG_GAP; (e) validation fixtures/receipts misleading if forced through one parser.

**Required output structure the memo claims to satisfy (1–8):** SOURCE_CONTEXT_READY/INCOMPLETE; ADJUDICATED_CURRENT_STATE; SPLIT_DECISION; SHARED_CAPTURE_SHAPE; LONG_FORM_ROUTE_CARD; SHORTS_ROUTE_CARD; SMALLEST_COMPLETE_PATCH_SEQUENCE; NON_CLAIMS_AND_RESIDUALS.

**Attack surfaces to consider (do not pre-accept; form your own findings):**
- Does the memo smuggle any architecture **fact** in under a probe-hypothesis label (overclaim), or call **probe-required** something that is well-established public knowledge (underclaim → wasted probe budget)?
- Is the SPLIT_DECISION ("one lane, two cards") genuinely supported, or does the cited evidence point to an earlier split — or to *less* structure than two full cards?
- Does `surface_type` discriminator + `MetricPosture` actually neutralize the (b)/(e) substrate/parser-split risk, or paper over it?
- Is the `watch_time` "likely not publicly capturable" tension resolved or hand-waved?
- Does `SMALLEST_COMPLETE_PATCH_SEQUENCE` step 1 (folder creation via the first recipe artifact) respect the migration-plan "reserved-only, create only with a recipe/recon/index artifact" convention, or overstep it?
- Are the verified current-state claims ("no YouTube harness code", "no recon card") correctly bounded as CA-must-reverify, given no_repo?
- Comments time-windowing (30/60-min) defensibility reasoning — sound?
- Is the cross-worktree residual (the unread dirty IG-comments patch @ a0f42467) adequately carried, or does the memo lean on IG comments precedent it cannot see?
- Are the hard boundaries (no behind-wall scraping; no bot-classification overclaim) actually held throughout?

## Review Target (VERBATIM — embedded; treat as the artifact under review)

===== BEGIN REVIEW TARGET =====

# YouTube Capture Surface Split — Architecture / Scoping Memo v0

*Read-only planning. Branch read: home worktree @ 6f79445e (origin/main-aligned), not the commissioning codex worktree @ a0f42467. No code, no live YouTube, no folder creation. Output mode: paste-ready chat.*

## 1. SOURCE_CONTEXT_READY

SOURCE_CONTEXT_READY — for current-state adjudication and architecture planning. Qualified: there is zero YouTube source-native route evidence in this repo, so every route/field/comments claim in the route cards is a PROBE HYPOTHESIS, and no GO/PARTIAL/NO-GO verdict can be issued from this task. Source method, structure, and design precedent are fully covered; YouTube live-surface facts are not.

Sources read & verified: AGENTS.md, overlay README/source-loading/decision-routing; capture playbook + recon index; IG monitoring-policy, momentum-pipeline, capture-shape contract, reel-viewcount recon, consolidated findings; projection doctrine; migration plan; creator-momentum landscape; plus targeted grep/glob of orca-harness/, docs/, and the capture spine.

## 2. ADJUDICATED_CURRENT_STATE

No YouTube capture exists in this repo, in any form — confirmed against primary source, not inherited from the commissioning pointers:

- Folder: No source_families/social_media/youtube/ exists (social_media/ holds only instagram/). Reserved-only — migration plan marks it "future reserved family; no current files" and "Create only with a future YouTube recipe/recon/index artifact or accepted placeholder convention" (migration plan L165/L179).
- Structure binding: YouTube is an accepted-as-named source family (not a peer spine, not a satellite) with zero current files; the social_media/ grouping is a proposed amendment to the flat member paths.
- Recon/recipe: No YouTube card in capture_recon_index_v0.md; the only social entries are IG (GO demonstrated) + a LinkedIn policy boundary. "No media/video capture recipe exists either." The playbook names TikTok, not YouTube, as the first intended probe.
- Harness: No YouTube-specific code. The 46 orca-harness/ "youtube" hits are all retail 02_archive_snapshot_body.bin archive snapshots (social-link footers).
- Monitoring policy: YouTube is a named-deferred profile seam — content unit = video, momentum metric = view_count + watch_time, curve window months-to-years, low (weekly) posting frequency; differences are "satellite values, not new machinery."
- Non-authorization (verbatim boundary): the migration plan is "Not authorization for IG, TikTok, YouTube, browser calibration, scraping, source access, live runs, harness code, tests, storage, scheduling, or production runtime"; the playbook "grants no capture/build/merge authority; per-operation network approval still required per probe."

Net: the authorized next artifacts are this memo and a future YouTube recon/recipe card. Nothing read authorizes a live probe, capture, folder creation, or harness work.

## 3. SPLIT_DECISION

Decision: ONE YouTube platform family / ONE capture lane, TWO surface route cards (surface_type in {long_form, shorts}). Do not split into two implementation paths now. This is the default posture, and the evidence supports holding it.

Evidence for unified:
- The platform-agnostic core (scheduler/allocator, MetricPosture enum + value-posture coupling, identity-metadata split, coverage claim, version-pinning, receipt obligations, raw-anchored projection) is surface-agnostic by construction — inherited from IG, not re-derived per surface.
- The candidate cross-surface differences (remix/save affordance, duration band, relative-vs-exact timestamp) read as profile values / surface-conditional fields, exactly what the monitoring-policy seam handles "without touching the core scheduler." YouTube is named the "sharpest proof of the seam."
- Criterion (e) — fixtures misleading if forced through one parser — is partly decidable now and resolves toward unified-by-design: a shared shape with a surface_type discriminator + MetricPosture (not_applicable for surface-absent metrics like long-form remix) structurally prevents a Shorts-absent metric being recorded as observed-0. The shape is safe to share; only a divergent substrate/parser would not be.

Residual split risk (both PROBE-GATED — a later authorized probe resolves them):
- (b) Incompatible comments route shape — highest-weight signal. The IG precedent shows the substrate (page DOM vs profile-feed JSON vs continuation API) determines route shape, and IG's reel view-count lived on a different surface than the permalink. If long-form comments come from one continuation and Shorts comments from an incompatible one (or only via a /watch?v= equivalent), that is the most likely forcing function for a code split.
- (d) Divergent per-surface verdict. Plausible that long-form reaches GO while Shorts lands PARTIAL (comments only via watch-equivalent) or CATALOG_GAP (player-only-no-metadata), or vice versa. Since "no media/video capture recipe exists," a video-substrate CATALOG_GAP is live for both surfaces simultaneously.

Structural consequence: keep one lane, but make the two route cards independently verdict-bearing and run two separate probes with separate receipts/fixtures — so a divergent GO/CATALOG_GAP per surface does not force a premature split and the merge-vs-split call is never made on conflated evidence. The split-to-two-runners decision is deferred to post-probe, triggered only if (b) proves field-level parser-incompatible or (d) is structural.

## 4. SHARED_CAPTURE_SHAPE

Proposed shape mirroring the frozen IG capture-shape contract; surface_type is the discriminator. [SI] shared-identical, [SC] surface-conditional, [PROBE] source-visibility unobserved.

- Packet identity/time metadata (no posture enum, mirrors IG AR-04): channel_id [SI], video_id [SI], capture_time [SI], manifest_version + identity/conflict-policy version [SI] (immutable rebuild inputs; unresolved id => identity-incomplete, not a metric).
- Creator/channel (momentum fields carry MetricPosture): handle/display name/channel URL/source timestamp [SI]; verification marker [SI][PROBE]; subscriber_count [SI][PROBE] (hideable — never store hidden as 0).
- Video identity: surface_type [SI]; canonical URL [SC] (/watch?v= vs /shorts/); title/caption [SI]; description [SI][PROBE]; publish timestamp [SI][PROBE] (exact-vs-relative is split-trigger a); duration [SC][PROBE] (Shorts band vs arbitrary); thumbnail + raw evidence anchors [SI].
- Engagement (each carries MetricPosture): view/play count [SI] as momentum metric, but [SC][PROBE] on "views"-vs-"plays" semantics; watch_time [SI][PROBE] — flagged tension: named in the YT profile but likely creator-analytics-only, not publicly capturable (expect unavailable/not_applicable); like_count/comment_count [SI][PROBE]; share/remix/save [SC][PROBE] (remix is Shorts-shaped => likely not_applicable on long_form); metric observation timestamp [SI].
- Comments (each carries MetricPosture; top source-returned set): commenter handle/display name/channel id [SI]; text [SI]; timestamp/relative-time [SI][PROBE]; like_count/reply_count [SI][PROBE]; creator heart/pin/reply markers [SI][PROBE]; top-comments set as a packet-level coverage claim [SI].
- Receipts (playbook Step-3 + IG coverage claim + projection raw-anchors, all [SI] except source URL [SC]): retrieval timestamp, HTTP status, rendered-DOM/embedded-state anchor, JSON-path anchor, raw body preservation (system-of-record), Step-0 access classification, routes-tried + skipped-with-reason, fidelity evidence, request-rate, packet-level coverage claim + per-metric coverage_window, limitations/non-claims, verdict.

Design precedent constraints honored: surface_type is a profile/field discriminator, not new scheduler machinery; the only deliberate lock-in is the capture-shape contract ("history cannot be re-captured"); projection stays a re-derivable view over raw (CHANNEL_PUBLIC_OUTPUT family) — any "views/engagement/anomaly" reading is Judgment, never a capture label; absence is residualized, never authored as 0.

## 5. LONG_FORM_ROUTE_CARD — /watch?v=<video_id>

- Substrate (hypothesis): JS-rendered SPA; load-bearing values most likely in an embedded page-state JSON blob and/or a browser-context internal continuation API, not static first-party HTML (IG: metric lived in continuation JSON, not the permalink DOM). Blob name/paths unobserved.
- Channel enumeration / Shorts deconfliction: hypothesis that long-form uploads sit on a separate channel surface ("Videos") from Shorts; confirm surface_type=long_form only when enumerated from that surface AND (/watch?v= resolves without /shorts/ redirect OR duration > Shorts ceiling). If surfaces can't be separated source-side => split-signal (a).
- Comments: separately-loaded continuation surface (cursor-paginated), almost certainly absent from initial HTML — a naive DOM read returns false-empty. Time-windowing (30/60-min) not defensible for long-form: timestamps likely relative-only, and the months-to-years curve makes early-minute windows architecturally mismatched.
- Route ranking: primary = embedded-state extraction (exact view count / full description / duration / publish time / channel id in one blob); fallback/companion = browser-context continuation (comments + non-inlined counts); rendered page for enumeration + access-diagnosis only; official API/vendor = needs-verification (do not assert terms); own-account not indicated for public data; PARTIAL/NO-GO/CATALOG_GAP as honest exits.
- Field highlight: watch_time (named momentum metric) is probably not publicly capturable => expect a field gap, not a route NO-GO.
- Failure markers: "Sign in to confirm you're not a bot" / consent interstitial (access gate); empty comments (lazy-load false-empty, escalate before verdict); abbreviated-only counts (PARTIAL on precision); 429/pace soft-wall (back off to human rate — IG showed pace, not volume, is the wall); Shorts-contaminated enumeration (split-signal a).
- Live-probe gate: Step-0 access classification -> substrate located -> exact-value fidelity for view/publish/duration -> Shorts deconfliction proven -> comments continuation + timestamp resolution recorded -> logged-out-first auth posture -> human-rate spacing -> no secrets in receipt -> claim ceiling honored.

## 6. SHORTS_ROUTE_CARD — /shorts/<video_id>

- Substrate (hypothesis): embedded ytInitialData/ytInitialPlayerResponse-style blob + internal continuation API. Watch-equivalence-by-id is a primary split test: does /watch?v=<same id> resolve the Short and expose richer/different fields or a different comments affordance? The IG reel precedent (same media id, field-empty permalink vs rich feed surface) makes asymmetry a serious possibility — must not be assumed equivalent.
- Creator enumeration: hypothesis of a dedicated /@handle/shorts tab distinct from /videos; separability and reliable surface_type inference are probe-required.
- Comments — heaviest risk: must first disambiguate whether the full paginated thread is reachable from the Shorts surface or only the watch-equivalent. Paginate via the source's own continuation token, not UI scroll (IG's false-wall lesson). Time-windowing defensible only if source-native absolute timestamps exist.
- Early-window divergence: Shorts discovery/posting dynamics may be faster than long-form's months-to-years profile => Shorts curve-window/heartbeat are unfilled satellite values; do not inherit long-form's.
- Route ranking: primary = embedded-state, paired with continuation for comments/enumeration; rendered fallback (Shorts is player-first — may be player-only-no-metadata); official API/vendor needs-verification; own-account only as an authorized soft-wall fallback; PARTIAL/NO-GO/CATALOG_GAP exits.
- Surface-specific fields: sound/remix metadata (Shorts-shaped, no precedent — probe-required); description often truncated/absent on the player surface.
- Failure markers: login/consent wall; consent.youtube.com redirect; 200-but-empty continuation (stale-token false NO-GO); pace-wall; Shorts-player-only-no-metadata => CATALOG_GAP if embedded-state + internal-API + rendered all miss; comments-on-watch-but-not-/shorts/ => PARTIAL + split-signal (b).
- Live-probe gate: adds a mandatory /shorts/<id> vs /watch?v=<id> field+comments equivalence diff for >=1 id — this artifact directly feeds the split decision.

## 7. SMALLEST_COMPLETE_PATCH_SEQUENCE (if later authorized — not authorized now)

Each step is independently gated; none is authorized by current sources.

1. Author the YouTube recon/recipe card (doc) — the first real file legitimately creates source_families/social_media/youtube/ per the migration-plan convention. Carries both surface route cards, shared-shape draft, non-claims. No code, no live run. Test area: header/retrieval-metadata + recon-index registration.
2. Run two authorized live probes (long-form, Shorts — separate receipts/fixtures), under the playbook with per-operation network approval, gated by the section 5/6 live-probe gates -> per-surface GO/PARTIAL/NO-GO/CATALOG_GAP verdicts + raw fixtures in gitignored scratch. This is where the merge-vs-split decision is finalized (triggers b/d).
3. Freeze the YouTube capture-shape contract (mirror IG: typed value + MetricPosture + coverage claim + version-pinning) — the one lock-in — only after probes pin the per-surface metric set/availability. Test area: posture-coupling + identity-incompleteness unit tests.
4. Implement the runner/module — default one runner with a surface_type switch + surface-specific parser functions; split to two runners only if step 2 fired trigger (b) field-level-incompatible or (d) structural. Harness code + fixture-replay parser tests per surface.
5. Wire YouTube profile values into the monitoring-policy seam (profile config: curve windows, content-unit bands, low posting prior, cap K, distinct Shorts early-window) — not new scheduler machinery.
6. Projection view over raw (CHANNEL_PUBLIC_OUTPUT), re-derivable; no stored derived momentum/tier.

## 8. NON_CLAIMS_AND_RESIDUALS

- No YouTube field or route is proven GO/PARTIAL/NO-GO/CATALOG_GAP — every route/field/comments claim is a PROBE HYPOTHESIS; no live probe was run.
- No authorization is created here for folder creation, recon authoring, live YouTube, sessions/auth-state, scraping, harness, storage, scheduling, or runtime.
- No bot/fake classification from comments or counts — the supportable claim ceiling is "source-native public data suitable for later corroboration, with limitations" (anomaly/independence reads are Judgment-owned).
- No IG/TikTok route detail is treated as transferable — IG is design precedent only; only the platform-agnostic core is inherited. Shorts<->long-form comments-route sharing is explicitly not assumed.
- Official-API/vendor terms are needs-verification from primary sources, not asserted.
- Worktree residual: read at 6f79445e, not the commissioning a0f42467. The IG capture-shape contract on this branch carries no comments object; the comment fields above derive from the prompt's field list + projection doctrine, not a frozen IG comment contract. The commissioning worktree's dirty IG-comments patch was not read and may already advance the comments-route precedent — re-verify against it before freezing the YouTube comments shape.
- Seam tension to resolve at probe time: the monitoring profile names watch_time a YouTube momentum metric, but it is likely not publicly capturable — the YouTube momentum metric may be view_count only, with watch_time residualized.

===== END REVIEW TARGET =====

## Review Output Contract (what you return)

Return, in this order:

1. **Framing (deep-thinking pass):** 3–6 lines — the decision problem, the material failure modes, the decision criteria you will judge against. No findings yet.
2. **`review_summary` (compact YAML, courier-ready):**
   ```yaml
   review_summary:
     target: youtube_capture_surface_split_architecture_memo_v0
     reviewed_by: <your model + version>        # operator_to_fill
     authored_by: claude-opus-4-8
     de_correlation_bar: cross_vendor_discovery   # or same_vendor_sanity if you are Claude-family
     same_vendor_rationale: <required only if same_vendor_sanity>
     access: no_repo
     findings_count: { critical: N, major: N, minor: N }
     overall_recommendation: <one line — decision input only, not a formal verdict>
   ```
3. **Findings (findings-first), each:** title + label tag `[yt-split-memo]`; severity (`critical`/`major`/`minor`, priority only); the claim under attack with a neutral citation to the memo's own text; why it is a defect; `minimum_closure_condition` (required end state); `next_authorized_action`. Advisory remediation direction is allowed; **no diff, no patch_queue_entry**.
4. **Non-findings checked & cleared**, and **not-proven boundaries** (especially anything that needs repo access you don't have).
5. **Residual-risk note.**
6. **Escalation:** if the memo's problem is design-level rather than fixable by bounded edits, return **`NEEDS_ARCHITECTURE_PASS`** with findings only.

Constraints on your output: findings-first; **no formal verdict, readiness, validation, or approval claim**; no runtime-model recommendation/ranking; severity labels carry no approval/rejection authority; you patch nothing (no_repo).

## Adjudication Contract (home / CA model — what happens after you return)

- Your findings, citations, and recommendation are **claims to adjudicate, not premises to inherit.** The CA accepts / modifies / rejects each, holds final veto (may reject even an individually-defensible point that adds no benefit), applies any kept change **within the bounded scope only**, and records `reviewed_by`/`authored_by` on the durable report.
- Because access is **no_repo**, the CA additionally (a) **verifies every source citation the memo makes against the live repo** (the one thing you cannot do), and (b) runs the **required bounded same-vendor post-patch recheck** (closure-of-findings + any new blocker/major in the touched delta) before anything is kept.

## Boundaries & Non-Claims

- This is a **provisional, advisory** convention pass. It is **not** validation, readiness, a formal verdict, severity authority, mandatory remediation, patch authority, or a bound/machine-routable review lane.
- **no_repo limitation (named):** the target is embedded verbatim, not a byte-hash-confirmable file attachment; you cannot independently verify the memo's repository claims. Source-citation accuracy and any kept change are the CA's responsibility.
- De-correlation is a **who-constraint** (vendor difference), never a model recommendation. If you are a Claude-family model, say so and drop to `same_vendor_sanity`.
- Do not import another project's paths, lifecycle labels, or policy. `jb` and external workflow source are not Orca authority.

## Output Destinations

- **Reviewer:** return the findings package above in chat (paste back to the commissioning CA).
- **CA durable report (when recorded):** `docs/review-outputs/adversarial-artifact-reviews/youtube_capture_surface_split_adversarial_artifact_review_v0.md`.
