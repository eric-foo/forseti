# Orca Judgment Spine Case 02 Daimler Preflight CA Prompt v0

```yaml
retrieval_header_version: 1
artifact_role: Planning handoff prompt
scope: Handoff prompt for a next CA to run a zero-spoiler Judgment Spine Case #2 preflight on the EY-Parthenon / Daimler carve-out candidate.
use_when:
  - Launching the next CA to decide whether the Daimler carve-out candidate is clean enough for a Judgment Spine blind case.
  - Testing whether the Milwaukee lesson pattern can transfer into a corporate restructuring case.
  - Preventing a premature consulting-case miner, skill, dataset, or product-readiness claim.
authority_boundary: retrieval_only
open_next:
  - .agents/workflow-overlay/source-loading.md
  - .agents/workflow-overlay/product-proof.md
  - docs/research/judgment-spine/README.md
  - docs/research/judgment-spine/manifest_v0.md
input_hashes:
  AGENTS.md: 59114DFF5D1572CB7003212BBE5BD4B4AE43C18F73366425D4BC1E3FC35BF6DD
  .agents/workflow-overlay/README.md: C473801F6B7E1883BDD59F35F0B25752DD8636DD04E2A3AA20367CC1A7B10EBC
  .agents/workflow-overlay/source-loading.md: A89279A9C546165D8F32C795644563B8AE0AF783F8E039470914A8A259A73415
  .agents/workflow-overlay/prompt-orchestration.md: 707EB21A0081BD95D9BA0F8511E7E8E980708F2E1801F3B5BA02BD112C1CD034
  .agents/workflow-overlay/product-proof.md: 0EB8A11DAA2A2BE1FC7F610AAA48004D97200A18D11679F9C8D45731EED61F21
  docs/research/judgment-spine/README.md: 142AEB0246DC6615370DC7FB9C05BD8F29C79B9C82462BA37F96790D9F0A807D
  docs/research/judgment-spine/manifest_v0.md: D168858B21590312E2E78D270D4D47CE2E44ECE05F8101E001B23007C58230B6
  docs/research/judgment-spine/cases/milwaukee-fiscal-crossroads/case_index.md: A41A30EDF23ABAD5003D079D350547DAC8CED80056D286DD9AC2A1F561AC0D69
```

## Preflight

```yaml
orca_start_preflight:
  agents_read: yes
  overlay_read: yes
  source_pack: S1 plus Judgment Spine, product-proof zero-spoiler, and prompt-orchestration rules
  edit_permission: docs-write
  target_scope: Select Case #2 from the user-stated consulting-corpus shortlist and prepare a next-CA handoff prompt.
  dirty_state_checked: yes
  blocked_if_missing: no
```

## Selection Decision

Selected candidate: EY-Parthenon / Daimler carve-out.

Reason: the Daimler candidate is the best Case #2 stress test after Milwaukee because it moves the Judgment Spine from public-sector fiscal survival into corporate restructuring while likely preserving source richness, a clear owner/incentive map, implementation complexity, and measurable public-company consequences. It is more structurally useful than another public-sector fiscal case and likely cleaner than Bain / Virgin Australia, where Bain's owner/acquirer role may blur consulting judgment, investment narrative, turnaround execution, and post-hoc success story.

Evidence boundary: the concrete shortlist is user-stated from the prior branch report, not yet saved as a candidate-screen artifact in `docs/research/consulting-judgment-corpus/`. Treat this selection as advisory sequencing, not verified backtest readiness.

Fallback if Daimler fails: Bain / Virgin Australia. Do not pivot to it without owner authorization.

## Prompt For Next CA

You are continuing Orca Judgment Spine work in `C:\Users\vmon7\Desktop\projects\orca`.

Your job is to run a narrow, zero-spoiler Case #2 preflight for the selected candidate:

> EY-Parthenon / Daimler carve-out

Do not run a full backtest. Do not create a sealed memo. Do not create a deck. Do not build a miner, scraper, dataset, skill, fine-tuning corpus, automation, software feature, or product plan.

### Required Method Use

REFERENCE-LOAD `workflow-deep-thinking` before source analysis. Do not APPLY it yet.

After the required source context is loaded and you declare `SOURCE_CONTEXT_READY` or `SOURCE_CONTEXT_INCOMPLETE`, APPLY `workflow-deep-thinking` to decide whether the Daimler candidate is clean enough for a Judgment Spine blind case.

If the method is unavailable, state that and continue with the same reasoning discipline.

### Required Reads

Read these first:

- `AGENTS.md`
- `.agents/workflow-overlay/README.md`
- `.agents/workflow-overlay/source-of-truth.md`
- `.agents/workflow-overlay/source-loading.md`
- `.agents/workflow-overlay/artifact-folders.md`
- `.agents/workflow-overlay/artifact-roles.md`
- `.agents/workflow-overlay/retrieval-metadata.md`
- `.agents/workflow-overlay/product-proof.md`
- `.agents/workflow-overlay/validation-gates.md`
- `docs/research/judgment-spine/README.md`
- `docs/research/judgment-spine/manifest_v0.md`
- `docs/research/judgment-spine/cases/milwaukee-fiscal-crossroads/case_index.md`
- this prompt

Do not bulk-read `docs/_inbox/`, contaminated replay outputs, method-validation replay bodies, all prompts, all product files, or all consulting-corpus folders.

### Public Source Boundary

This task requires public source research. Proceed with public web/source research only if the current receiving turn explicitly authorizes it. If public source research is not authorized, stop with:

```text
BLOCKED_PUBLIC_RESEARCH_AUTH_MISSING
```

Research unit: one candidate only, EY-Parthenon / Daimler carve-out. Do not expand to Virgin Australia, Ergon Retail, Societe Generale, or a broader McKinsey/Bain/BCG corpus.

### Zero-Spoiler Rule

Preserve blind judgment. Participant-facing material, preflight text, source lists, prompts, summaries, and reports must not reveal:

- actual decision made;
- consulting-firm recommendation or action;
- implementation status;
- post-cutoff facts;
- later outcome, result quality, success/failure label, or outcome metrics;
- source titles, snippets, URLs, or filenames that leak any of the above.

Preflight may check whether post-outcome evidence appears available, but participant-visible output may express that only as a non-spoiling admissibility state such as `available`, `not_found`, or `unclear`. Do not disclose what happened.

If leakage occurs, mark the preflight contaminated and do not use it for blind judgment. Return a blocked result and name the contamination boundary without pasting leaked details.

### Output Mode

Output mode: `file-write`.

Write exactly one preflight artifact unless blocked:

```text
docs/research/judgment-spine/cases/daimler-carve-out/case_02_preflight_v0.md
```

If the official case frame proves materially different, keep the parent folder as `daimler-carve-out` for now and explain the naming issue in the artifact. Do not rename folders or update the manifest unless the current turn explicitly authorizes that additional write.

### Required Artifact Shape

The preflight artifact must include:

1. Retrieval header.
2. `orca_start_preflight` receipt.
3. Spoiler-safe case identity.
4. Decision owner hypothesis and incentive map.
5. Candidate decision question.
6. Candidate cutoff options, stated without revealing actual action or outcome.
7. Clean pre-cutoff source-family inventory.
8. Facilitator-only source availability status expressed without leaking titles, URLs, snippets, or outcomes.
9. Learnability tier assessment under `docs/research/judgment-spine/README.md`.
10. Source sufficiency assessment:
    - decision reconstructability;
    - economics;
    - trust, psychology, or stakeholder pressure;
    - implementation burden;
    - timing and irreversibility;
    - owner/incentive clarity;
    - independent action or outcome availability;
    - leakage risk.
11. Go / no-go / hold recommendation for blind judgment.
12. If go: exact next artifact to create, normally `participant_packet_v0.md` plus `safety_receipt_v0.md`.
13. If hold or no-go: what single missing source class would change the answer.
14. Non-claims.

### Decision Standard

Classify the candidate as:

- `GO_TIER_0_CANDIDATE`: enough public pre-cutoff source material and clean spoiler separation exist to build a blind participant packet.
- `HOLD_TIER_1_CANDIDATE`: the case may teach judgment, but one material source gap or cutoff ambiguity must be resolved first.
- `NO_GO_TIER_2`: too anonymized, marketing-heavy, post-hoc, source-thin, outcome-light, or leakage-prone for blind use.
- `BLOCKED_CONTAMINATED`: leakage occurred before a clean participant path could be preserved.
- `BLOCKED_PUBLIC_RESEARCH_AUTH_MISSING`: public source research was not authorized in the receiving turn.

### What Not To Do

- Do not write a sealed memo.
- Do not write an outcome calibration.
- Do not write a deck.
- Do not create a consulting playbook.
- Do not create a miner, scraper, dataset, automation, or skill.
- Do not claim buyer validation, willingness-to-pay proof, repeatability proof, product readiness, feature readiness, implementation readiness, commercial readiness, or model-training readiness.
- Do not treat consulting-firm case-page claims as ground truth.
- Do not pivot to another case without owner authorization.

### Validation Evidence

After writing the artifact, read it back only enough to verify:

- the retrieval header exists;
- `orca_start_preflight` exists;
- the zero-spoiler rule was followed;
- the output path exists;
- missing fields are labeled;
- non-claims are present;
- `git status --short --branch` was checked;
- SHA256 was captured.

Return a concise human summary plus path, SHA256, status, decision classification, and next authorized step. Do not paste the full artifact.
