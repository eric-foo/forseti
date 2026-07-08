# Full-System Name Aura Review Prompt v0

```yaml
retrieval_header_version: 1
artifact_role: Deep-thinking prompt artifact
scope: Second-opinion review prompt for choosing among Athanor, Lucerna, and Praetor as the full Orca-system name, with aura farming as the primary criterion.
use_when:
  - Asking a second reviewer to compare Athanor, Lucerna, and Praetor for the full Orca system.
  - Stress-testing whether Praetor should be the outer brand or remain the internal Judgment Spine / engine name.
  - Preserving the distinction between full-system naming and Orca Signal / creator-wedge naming.
authority_boundary: retrieval_only
open_next:
  - .agents/workflow-overlay/prompt-orchestration.md
  - docs/hygiene/orca_signal_naming_brand_architecture_handoff_v0.md
stale_if:
  - The owner selects a final company/product name.
  - A formal trademark clearance or attorney review changes the risk posture for Athanor, Lucerna, Praetor, or Orca.
  - The full system is renamed away from the Orca working architecture.
```

## Orca Prompt Preflight

- Output mode: `file-write` for this prompt artifact; `paste-ready-chat` copy may be sent to a second reviewer.
- Receiver output mode: `chat-only`; no durable report path is required from the second reviewer.
- Template kind: `deep-thinking`; no model-runtime route is implied.
- Edit permission: `read-only`; the receiver must not edit repo files, create naming artifacts, commit, push, file trademarks, or claim legal clearance.
- Target scope: full-system brand naming only. This is not Orca Signal / creator-wedge naming.
- Workspace/source posture: no repository access assumed for the receiver. Use the source capsule below as bounded context.
- Dirty-state allowance: current local repo is dirty; this prompt is a naming-review artifact only and must not make code, validation, readiness, or product-proof claims.
- Doctrine change: none. The prompt asks for advisory naming judgment only.
- Non-claims: not legal advice; not trademark clearance; not buyer validation; not product readiness; not final owner sign-off.

## Paste-Ready Prompt

```text
You are giving a second opinion on a full-system brand name. Be blunt. Push back hard if the favorite name is strategically wrong.

Decision to review:
Choose the best naming direction among Athanor, Lucerna, and Praetor for the full system currently working under the Orca umbrella.

This is NOT naming the narrow Orca Signal / creator-fit wedge. This is the full system: public/source capture, cleaning/classification, evidence transformation, and especially the Judgment Spine that decides what evidence can support, what claim is allowed, what action ceiling is justified, and what recommendation can be shown to a decision owner.

Priority order:
1. Aura farming is the top priority. The name should feel institution-grade, old-world, serious, almost inevitable before the product is fully explained. Think Anthropic / Palantir level gravity, but do not copy their style too literally.
2. Semantic fit with the actual system: bounded public evidence -> transformation -> judgment -> decision.
3. Buyer affect: premium, strategic, credible, not cute SaaS, not generic analytics, not surveillance-coded.
4. Brand architecture usefulness: can the name support subproducts, a judgment engine/spine, decision briefs, and future wedges?
5. Obvious clearance/search risk: do a quick current web/trademark sanity screen if you have browsing, but do NOT claim legal clearance.

Context:
- The system is not "capture all information." That phrase overclaims and creates surveillance/data-lake optics. The better truth is disciplined judgment from bounded, source-backed evidence.
- The product should not sound like generic influencer analytics, social listening, creator database software, a dashboard, or an OSINT tool.
- The product's real magic is converting messy public signals into decision-grade judgment: what to commit to, hold, avoid, narrow, test, or scale.
- The current internal preference is:
  - Athanor as the outer company/full-system brand.
  - Praetor as the internal Judgment Spine / adjudication engine name.
  - Lucerna as the buyer-facing artifact/output layer, e.g. a brief/deck/report.
- Challenge that stack. If Praetor should be the company name, say so. If Athanor is too mystical or obscure, say so. If Lucerna is actually the best outer brand, say so.

Candidate meanings:
- Athanor: alchemical furnace; transformation of raw material into something higher-grade.
- Lucerna: Latin lamp; illumination, clarity, light thrown on hidden structure.
- Praetor: Roman magistrate / authority; judgment, adjudication, command, legal/institutional force.

Questions to answer:
1. Rank Athanor, Lucerna, and Praetor for the outer full-system/company name.
2. Rank them separately for internal system components: judgment engine/spine, decision artifact, and signal/capture layer.
3. Which name maximizes aura without becoming cringe, cosplay, authoritarian, legalistic, or obscure?
4. Is "Praetor" actually too perfect to leave as an internal engine name, or should it own the whole brand?
5. What is the strongest brand stack using these three names?
6. What are the main risks for each name: buyer affect, meaning, pronunciation, category confusion, and obvious naming conflicts?
7. Give one final recommendation and the first tagline you would test.

Output format:
- Start with the final recommendation in one sentence.
- Then give rankings with short reasons.
- Then give the recommended brand stack.
- Then give risks and non-claims.
- End with 3 sharper alternative names only if all three candidates are materially weak.

Hard boundaries:
- Do not claim trademark availability or legal clearance.
- Do not use Orca Signal as the target name; this is the full-system name.
- Do not optimize for literal feature clarity over aura. Aura is priority #1.
- Do not give a polite compromise if one name is clearly stronger.
```
