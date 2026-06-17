# Foundation Layer v0 First Proof Run - BT2-04 Backtest Slice

- Status: SLICE_COMPLETE_DOCS_ONLY
- Artifact type: Historical backtest replay slice
- Scope: `BT2-04`, Shutterstock response to generative image AI
- Cutoff date: 2022-09-15
- Date context: 2026-05-21, Asia/Singapore
- Output mode: file-write
- Edit permission used: docs-write for this target artifact only
- Implementation authorized: no
- Feature planning authorized: no
- Source collection systems authorized: no
- Source maps authorized: no

## 1. Status, Scope, And Non-Authority

Decision: complete this bounded evidence slice as one docs-first artifact.

This artifact records a leakage-controlled replay for the locked historical
case `BT2-04`: Shutterstock response to generative image AI. It tests whether
public, inspectable, market-level evidence visible by 2022-09-15 could have
supported a useful at-cutoff decision memo before Shutterstock's later OpenAI
partnership, AI Image Generator launch, expanded data agreement, and later
copyright narratives were public.

Source basis:

- current owner instruction authorizing this bounded `BT2-04` proof evidence
  slice only;
- `AGENTS.md`;
- `.agents/workflow-overlay/README.md` and the Orca overlay files;
- `docs/decisions/turn_08_product_thesis_v0.md`;
- `docs/product/core_spine_v0_product_contract.md`;
- `docs/product/engagement_logic_registry_v0.md`;
- `docs/product/core_spine_v0_information_production_foundation_v0.md`;
- `docs/product/core_spine_v0_proof_protocol_v0.md`;
- `docs/product/core_spine_v0_proof_input_selection_v0.md`;
- `docs/product/core_spine_v0_proof_packet_preflight_v0.md`;
- `docs/product/core_spine_v0_first_proof_packet_preparation_v0.md`;
- `docs/product/core_spine_v0_first_proof_run_charter_v0.md`;
- `docs/product/core_spine_v0_first_proof_run_locks_v0.md`;
- `docs/product/core_spine_v0_heavyweight_proof_case_discovery_results_part_2_v0.md`;
- repository check: `git status --short --branch` reported
  `## main...origin/main [ahead 10]` and untracked
  `docs/prompts/hygiene-queue/`;
- recent log check: `git log --oneline -8` began with
  `8cdfe8f docs: reconcile proof lock review gate`.

Non-authority:

- This artifact is not a source map, source inventory, data spine, proof suite,
  feature plan, implementation plan, or marketing demo.
- This artifact does not stage, commit, push, create software, create tests,
  create generated artifacts, create automation, or authorize future proof
  expansion.
- This artifact does not claim Foundation Layer v0 works beyond this slice.
- This artifact does not import `jb` authority, lifecycle mechanics, paths,
  validation habits, or success logic into Orca.

Sequence note:

The pre-cutoff candidate pool and at-cutoff replay memo were completed before
the post-window outcome pool was inspected. Post-window sources are listed only
in section 9 and are excluded from sections 3 through 8.

## 2. Locked Backtest Frame

Case:

`BT2-04`, Shutterstock response to generative image AI.

Decision context:

Stock-image marketplace, contributor economics, licensing, customer creative
workflows, and partnership response to text-to-image AI after Stable Diffusion
and other generative-image tools made synthetic image supply publicly visible.

Cutoff date:

2022-09-15.

At-cutoff decision question:

Given only public evidence available on or before 2022-09-15, should
Shutterstock watch, probe, test, hold, move, or commit around generative image
AI in its stock-content marketplace, contributor model, licensing posture, and
creative workflow product surface?

Allowed action language:

`Watch`, `Probe`, `Test`, `Hold`, `Move`, or `Commit`, constrained by the
Foundation Layer v0 Action Ceiling.

Post-window exclusion rule:

The at-cutoff judgment excludes Shutterstock's 2022-10-25 OpenAI partnership
announcement, AI Image Generator launch, expanded OpenAI data agreement, later
Getty litigation or product moves, later copyright and artist-compensation
narratives, and retrospective coverage.

Fair-cutoff rationale:

The cutoff sits after the public release of Stable Diffusion and public
commercialization of DALL-E 2, but before Shutterstock publicly announced its
OpenAI partnership and contributor-fund posture. At cutoff, plausible
Shutterstock responses still included banning unmanaged AI uploads, licensing
content for model training, partnering with an AI lab, building a tool,
waiting for copyright clarity, or defending the existing marketplace.

## 3. Pre-Cutoff Candidate Evidence Pool

Capture/access timestamp for this pool: 2026-05-21, Asia/Singapore.

This pool is bounded to 15 candidates. It includes accepted, discounted, and
rejected candidates. Rejected timing candidates are retained to show the
cutoff boundary.

| ID | Source | Timing | Inclusion state | Decision-use note |
| --- | --- | --- | --- | --- |
| C-01 | Stability AI, [Stable Diffusion Public Release](https://stability.ai/news-updates/stable-diffusion-public-release) | 2022-08-22 | Accepted | Public release made high-quality text-to-image generation broadly visible before cutoff. |
| C-02 | Hugging Face, [CompVis/stable-diffusion model card](https://huggingface.co/CompVis/stable-diffusion) | Model release tied to August 2022 | Accepted with timing note | Shows model access, open tooling path, license, and training-data basis; live page may have later edits. |
| C-03 | OpenAI, [DALL-E now available in beta](https://openai.com/index/dall-e-now-available-in-beta/) | 2022-07-20 | Accepted | Shows paid credits, large waitlist invitation, and commercial-use rights for generated images. |
| C-04 | OpenAI, [DALL-E 2 Preview - Risks and Limitations](https://github.com/openai/dalle-2-preview/blob/main/system-card.md) | Up to date as of April 2022 | Accepted | Shows OpenAI's own risk framing around generated images, provenance, misuse, training data, and plausible commercial uses. |
| C-05 | PCWorld, [Midjourney beta opens to everyone](https://www.pcworld.com/article/820518/midjourneys-ai-art-goes-live-for-everyone.html) | 2022-07-26 | Accepted, source-limited | Secondary report that another paid image generator was publicly available and commercially usable in some plans. |
| C-06 | Shutterstock, [formation of Shutterstock.AI](https://investor.shutterstock.com/node/11566/pdf) | 2021-07-27 | Accepted | Shows preexisting AI/data strategy and stated intent to commercialize data assets from its content library. |
| C-07 | Shutterstock 2021 Form 10-K via Annual Statements, [annual report](https://annual-statements.com/company/shutterstock-inc/annual-report-2021-form-10k-61272) | Filed before cutoff for 2021 | Accepted | Shows marketplace scale, contributors, licensing model, enterprise workflow, royalties, and API/customer integration surfaces. |
| C-08 | Shutterstock, [Q2 2022 results](https://investor.shutterstock.com/news-releases/news-release-details/shutterstock-reports-second-quarter-2022-financial-results) | 2022-08-02 | Accepted | Shows current collection scale, revenue mix, paid downloads, and enterprise/e-commerce exposure before cutoff. |
| C-09 | Shutterstock, [Pond5 acquisition](https://investor.shutterstock.com/news-releases/news-release-details/shutterstock-acquires-pond5-worlds-largest-video-marketplace) | 2022-05-11 | Accepted | Shows active expansion of licensable content assets and creative workflow reach before the AI-image outcome window. |
| C-10 | TechCrunch, [commercial image-generating AI raises legal issues](https://techcrunch.com/2022/07/22/commercial-image-generating-ai-raises-all-sorts-of-thorny-legal-issues/) | 2022-07-22 | Discounted | Useful for public legal-risk framing; secondary source and not Shutterstock-specific. |
| C-11 | Axios, [AI-generated images open multiple cans of worms](https://www.axios.com/2022/09/12/ai-images-ethics-dall-e-2-stable-diffusion) | 2022-09-12 | Discounted | Useful for public creator, ethics, training-data, and open-source risk; secondary synthesis. |
| C-12 | New York Times mirror, [AI-generated art prize controversy](https://www.memorable.io/m/www.nytimes.com/2022/09/02/technology/ai-artificial-intelligence-artists.html) | 2022-09-02 | Discounted | Shows mainstream creative-market controversy, but not stock-photo buyer demand. |
| C-13 | Waxy.org, [Have I Been Trained?](https://waxy.org/2022/09/have-i-been-trained/) | 2022-09-14 | Discounted | Weak but timing-valid signal that artist opt-in/opt-out tooling was emerging before cutoff. |
| C-14 | Ars Technica/PetaPixel reports on AI images appearing on stock sites | 2022-09-16 | Rejected for at-cutoff use | One day after cutoff; not used to judge pre-cutoff Shutterstock response. |
| C-15 | Vice report on Shutterstock removing AI images | 2022-09-19 | Rejected for at-cutoff use | After cutoff; not used in the at-cutoff replay. |

Pool stop reason:

The pool is sufficient to test the at-cutoff decision frame. More source
collection would risk drifting into source-map creation or retrospective
evidence mining without changing the valid action ceiling.

## 4. Accepted Pre-Cutoff Evidence Units

### EU-01 - Stable Diffusion Public Release

- Decision-frame reference: `BT2-04` at-cutoff Shutterstock AI response.
- Source locator: Stability AI, [Stable Diffusion Public Release](https://stability.ai/news-updates/stable-diffusion-public-release).
- Source actor or audience type: AI model provider and public developer/user audience.
- Event or publication timestamp: 2022-08-22.
- Capture/access timestamp: 2026-05-21, Asia/Singapore.
- Pre-cutoff visibility: yes.
- Raw claim: Stability publicly released Stable Diffusion after a researcher release and described continued model and hardware optimization.
- Orca interpretation: High-quality image generation became public and broadly visible before the cutoff. This made stock-image marketplace disruption plausible, but did not prove Shutterstock buyer demand.
- Provenance: Found through public web search for Stable Diffusion public release.
- Transformation history: Summarized; no scoring or scraping.
- Relevance: Supports actor-strategy, attention, customer-workflow, and disruption-risk evidence.
- Inclusion state: included.
- Source limitations: Source is self-promotional and does not measure stock-image customer behavior.
- Signal Integrity: clean enough, source-limited.
- Integrity effect: usable for technology visibility, not demand.
- Signal Use: strong for public availability and disruption pressure; weak for buyer willingness to pay.

### EU-02 - Stable Diffusion Model Card, Access, License, And Training Basis

- Decision-frame reference: `BT2-04`.
- Source locator: Hugging Face, [CompVis/stable-diffusion](https://huggingface.co/CompVis/stable-diffusion).
- Source actor or audience type: model host/repository and developer audience.
- Event or publication timestamp: August 2022 release context; page is live and may have later edits.
- Capture/access timestamp: 2026-05-21, Asia/Singapore.
- Pre-cutoff visibility: usable with timing caution because it is tied to the August 2022 public model release.
- Raw claim: The page identifies Stable Diffusion version 1 checkpoints, access paths through Hugging Face or GitHub, a CreativeML OpenRAIL-M license, and LAION-derived training subsets.
- Orca interpretation: The model was not merely a press story; it had developer-accessible distribution and a training-data/licensing surface that stock-image platforms had reason to monitor.
- Provenance: Found through public web search for Stable Diffusion model card.
- Transformation history: Summarized from the live repository page.
- Relevance: Supports action pressure around model availability, provenance, licensing, and training-data risk.
- Inclusion state: included with timing caution.
- Source limitations: Live repository pages can change; exact cutoff page state was not separately archived in this slice.
- Signal Integrity: source-limited but decision-relevant.
- Integrity effect: lowers confidence from clean direct evidence to timing-cautioned evidence.
- Signal Use: strong for model-access and training-data risk; weak for customer demand.

### EU-03 - DALL-E 2 Beta, Pricing, And Commercial Use

- Decision-frame reference: `BT2-04`.
- Source locator: OpenAI, [DALL-E now available in beta](https://openai.com/index/dall-e-now-available-in-beta/).
- Source actor or audience type: AI model provider and creative users.
- Event or publication timestamp: 2022-07-20.
- Capture/access timestamp: 2026-05-21, Asia/Singapore.
- Pre-cutoff visibility: yes.
- Raw claim: OpenAI opened DALL-E beta access to a large waitlist, introduced paid credits, and granted users usage rights to commercialize generated images.
- Orca interpretation: Commercial creative use cases were already visible before cutoff. This created direct substitution and workflow pressure against stock-image licensing, but still did not prove stock customers were switching.
- Provenance: Found through public web search for official DALL-E beta announcement.
- Transformation history: Summarized; no quote bank created.
- Relevance: Supports buyer-workflow and product-strategy pressure.
- Inclusion state: included.
- Source limitations: OpenAI is an interested party and the source describes its own beta, not Shutterstock-specific behavior.
- Signal Integrity: clean enough, incentive-distorted.
- Integrity effect: usable for tool availability and commercial-rights signal; discounted for demand.
- Signal Use: strong for customer-workflow possibility; weak for Shutterstock-specific demand or revenue impact.

### EU-04 - DALL-E 2 Risk And Provenance Framing

- Decision-frame reference: `BT2-04`.
- Source locator: OpenAI, [DALL-E 2 Preview - Risks and Limitations](https://github.com/openai/dalle-2-preview/blob/main/system-card.md).
- Source actor or audience type: AI provider, researchers, and safety/policy audience.
- Event or publication timestamp: up to date as of April 2022.
- Capture/access timestamp: 2026-05-21, Asia/Singapore.
- Pre-cutoff visibility: yes.
- Raw claim: OpenAI documented risks and mitigations around generated images, including misuse, image authenticity, provenance, training data, and plausible commercial uses.
- Orca interpretation: Even the more controlled DALL-E path carried visible safety, provenance, and rights concerns. A stock marketplace could not responsibly infer that open uploading or immediate broad launch was low-risk.
- Provenance: Found through public web search for DALL-E system card.
- Transformation history: Summarized.
- Relevance: Supports caution, policy design, partner selection, and contributor/IP risk.
- Inclusion state: included.
- Source limitations: Focused on OpenAI's preview system and risk lens, not the whole market.
- Signal Integrity: clean enough, source-limited.
- Integrity effect: caps action above `Test` unless legal/provenance questions are handled.
- Signal Use: strong for risk and governance evidence; not valid for demand.

### EU-05 - Midjourney Open Beta And Paid Usage

- Decision-frame reference: `BT2-04`.
- Source locator: PCWorld, [Midjourney beta opens to everyone](https://www.pcworld.com/article/820518/midjourneys-ai-art-goes-live-for-everyone.html).
- Source actor or audience type: technology press reporting on public creative-tool access.
- Event or publication timestamp: 2022-07-26.
- Capture/access timestamp: 2026-05-21, Asia/Singapore.
- Pre-cutoff visibility: yes.
- Raw claim: Midjourney beta was open broadly, offered limited free usage, paid plans, and some commercial or ownership terms.
- Orca interpretation: DALL-E and Stable Diffusion were not isolated. Multiple text-to-image tools were visible to creative users before the cutoff.
- Provenance: Found through public web search for Midjourney open beta.
- Transformation history: Summarized.
- Relevance: Supports market-level availability and substitution pressure.
- Inclusion state: included but discounted.
- Source limitations: Secondary source and not stock-marketplace specific.
- Signal Integrity: source-limited.
- Integrity effect: contributes corroboration to tool availability only; cannot raise action ceiling alone.
- Signal Use: attention, customer-workflow, and market-availability evidence; weak for demand.

### EU-06 - Shutterstock.AI And Data-Asset Strategy

- Decision-frame reference: `BT2-04`.
- Source locator: Shutterstock, [formation of Shutterstock.AI](https://investor.shutterstock.com/node/11566/pdf).
- Source actor or audience type: Shutterstock official investor/public announcement.
- Event or publication timestamp: 2021-07-27.
- Capture/access timestamp: 2026-05-21, Asia/Singapore.
- Pre-cutoff visibility: yes.
- Raw claim: Shutterstock launched Shutterstock.AI, acquired AI platforms, and stated that it would commercialize data assets within its content library and partner around computer vision and content insights.
- Orca interpretation: Shutterstock had preexisting AI/data posture and did not need to discover AI as a category after Stable Diffusion. This increased the plausibility of a partner/data-licensing response by cutoff.
- Provenance: Found through public web search for Shutterstock.AI formation.
- Transformation history: Summarized.
- Relevance: Supports actor-strategy feasibility and response-path plausibility.
- Inclusion state: included.
- Source limitations: Company announcement; forward-looking and promotional.
- Signal Integrity: clean enough, incentive-distorted.
- Integrity effect: supports feasibility, not evidence of execution or customer pull.
- Signal Use: strong for actor strategy; weak for demand.

### EU-07 - Shutterstock Marketplace Scale, Contributor Model, And Licensing Exposure

- Decision-frame reference: `BT2-04`.
- Source locators: Shutterstock 2021 Form 10-K via [Annual Statements](https://annual-statements.com/company/shutterstock-inc/annual-report-2021-form-10k-61272) and Shutterstock [Q2 2022 results](https://investor.shutterstock.com/news-releases/news-release-details/shutterstock-reports-second-quarter-2022-financial-results).
- Source actor or audience type: public company reporting.
- Event or publication timestamp: 2021 annual report and 2022-08-02 Q2 results.
- Capture/access timestamp: 2026-05-21, Asia/Singapore.
- Pre-cutoff visibility: yes.
- Raw claim: Shutterstock reported a large image/video collection, contributor royalties, direct licensing, enterprise and e-commerce channels, integrations, subscriptions, and paid downloads.
- Orca interpretation: The relevant exposure was material: Shutterstock was a licensing marketplace with many contributors, customers, and workflow integrations. Generative AI pressure could affect supply, customer workflows, IP assurance, and contributor economics.
- Provenance: Found through public web search for Shutterstock financial results and annual report.
- Transformation history: Combined two official public-company sources into one evidence unit for marketplace exposure.
- Relevance: Supports consequence and action-threshold assessment.
- Inclusion state: included.
- Source limitations: Public filings do not show generative AI customer behavior by cutoff.
- Signal Integrity: clean enough.
- Integrity effect: raises consequence of being wrong, but not confidence in a specific response.
- Signal Use: strong for decision consequence and platform exposure; weak for demand.

### EU-08 - Pond5 Acquisition And Multi-Asset Content Expansion

- Decision-frame reference: `BT2-04`.
- Source locator: Shutterstock, [Pond5 acquisition](https://investor.shutterstock.com/news-releases/news-release-details/shutterstock-acquires-pond5-worlds-largest-video-marketplace).
- Source actor or audience type: Shutterstock official investor/public announcement.
- Event or publication timestamp: 2022-05-11.
- Capture/access timestamp: 2026-05-21, Asia/Singapore.
- Pre-cutoff visibility: yes.
- Raw claim: Shutterstock acquired Pond5, describing it as a large video-first content marketplace and a way to expand licensed video, music, and editorial content.
- Orca interpretation: Before the generative image outcome window, Shutterstock was still investing in content-scale and marketplace breadth. This makes data licensing and multi-asset workflow strategy plausible, but does not answer AI policy directly.
- Provenance: Found through public web search for Pond5 acquisition.
- Transformation history: Summarized.
- Relevance: Supports actor strategy and alternative response paths.
- Inclusion state: included.
- Source limitations: Not AI-specific.
- Signal Integrity: clean enough.
- Integrity effect: useful as context, not a primary AI signal.
- Signal Use: actor-strategy evidence; weak for AI-specific response.

### EU-09 - Public Creator/Artist Controversy Before Cutoff

- Decision-frame reference: `BT2-04`.
- Source locators: Axios, [AI-generated images open multiple cans of worms](https://www.axios.com/2022/09/12/ai-images-ethics-dall-e-2-stable-diffusion); New York Times mirror, [AI-generated art prize controversy](https://www.memorable.io/m/www.nytimes.com/2022/09/02/technology/ai-artificial-intelligence-artists.html); Waxy.org, [Have I Been Trained?](https://waxy.org/2022/09/have-i-been-trained/).
- Source actor or audience type: public technology/media coverage and creator-tool commentary.
- Event or publication timestamp: 2022-09-02 to 2022-09-14.
- Capture/access timestamp: 2026-05-21, Asia/Singapore.
- Pre-cutoff visibility: yes.
- Raw claim: Public coverage before cutoff showed creator backlash, questions about training data and compensation, online community moderation pressure, and emerging artist opt-in/opt-out tooling.
- Orca interpretation: Creator and rights-holder conflict was already visible before cutoff. A stock platform with a contributor base needed a compensation, licensing, and provenance posture, not just a pure customer-facing image generator.
- Provenance: Found through public web search for pre-cutoff AI art controversy.
- Transformation history: Summarized across weak/secondary sources.
- Relevance: Supports legal/reputational risk and contributor-economics pressure.
- Inclusion state: included but discounted.
- Source limitations: Secondary, creator-market oriented, and not direct evidence from Shutterstock buyers.
- Signal Integrity: source-limited and attention-heavy.
- Integrity effect: caps demand inference and supports `Hold` on unmanaged uploads.
- Signal Use: objection, buyer-belief, policy-risk, and weak market-perception evidence; not demand.

## 5. Discounted Or Rejected Pre-Cutoff Evidence

Discounted:

- Secondary legal and ethics coverage was used to identify public uncertainty,
  not to prove liability or buyer behavior.
- The Midjourney beta report was used only as corroboration that multiple
  public image generators existed before cutoff.
- The AI-art-prize controversy was used only as creator-market perception and
  not as stock-image demand evidence.
- `Have I Been Trained?` was used as a weak signal that opt-in/opt-out and
  training-data consent were becoming visible before cutoff.
- Hugging Face model-card evidence was used with a timing caution because live
  repository pages can change after publication.

Rejected from at-cutoff reasoning:

- Ars Technica/PetaPixel reports from 2022-09-16 about AI-generated images
  appearing on stock photography sites: rejected because they were published
  one day after the cutoff.
- Vice reporting from 2022-09-19 about Shutterstock removing AI images:
  rejected because it was after the cutoff.
- Getty's later AI-image ban, Getty litigation, Adobe AI-stock policy, and
  any later stock-platform comparison: rejected from sections 3 through 8
  because they are post-window.
- Current Shutterstock product, help, AI generator, and search pages: rejected
  from at-cutoff reasoning because current pages cannot establish 2022-09-15
  visibility without archived timing.
- Retrospective coverage about Shutterstock's later OpenAI partnership,
  contributor fund, AI Image Generator, or expanded training-data agreement:
  rejected from at-cutoff reasoning.

## 6. At-Cutoff Signal Integrity And Signal Use Summary

Signal integrity summary:

- Official, dated sources establish that text-to-image tools were public,
  commercial creative use was visible, and Shutterstock had preexisting
  AI/data and marketplace assets.
- Public-company sources establish meaningful consequence: Shutterstock had a
  large licensable content library, contributor royalty model, paid downloads,
  customer channels, and enterprise workflow integrations.
- Source limitations remain material. The pre-cutoff pool does not prove
  Shutterstock customers were switching to AI tools, does not show direct
  revenue pressure, and does not show a pre-cutoff stock-site AI-upload flood.
- Creator-rights and legal uncertainty were visible before cutoff, but mostly
  through secondary sources and public controversy rather than resolved legal
  outcomes.
- Integrity labels change the inference: the evidence can support a controlled
  partner/data-licensing probe or test, and a hold on unmanaged uploads, but it
  cannot support a full commit to broad AI-generated stock distribution.

Signal use summary:

| Signal use | At-cutoff strength | Rationale |
| --- | --- | --- |
| Actor strategy | Strong enough for `Probe`/`Test` | Shutterstock already had AI/data assets and a content library that could plausibly matter to model providers. |
| Customer-workflow pressure | Directional | DALL-E, Stable Diffusion, and Midjourney made image generation visible and usable, but switching behavior was not proven. |
| Contributor/IP risk | Directional to material | Creator backlash, training-data questions, and OpenAI's risk framing made unmanaged AI uploads risky. |
| Buyer-belief evidence | Weak to directional | Public narratives could affect beliefs about stock images, but buyer-level evidence was absent. |
| Demand evidence | Not established | No pre-cutoff evidence showed Shutterstock customers buying, switching, or demanding AI-generated stock at scale. |
| Manipulation or pollution risk | Directional | Open distribution and unclear provenance made library pollution and rights ambiguity plausible. |
| Exclusion evidence | Applies to post-cutoff timing leaks | Post-cutoff stock-site reports and later official outcomes are excluded from at-cutoff judgment. |

## 7. At-Cutoff Decision Strength And Action Ceiling

Decision strength:

Directional, not strong. The pre-cutoff evidence was enough to justify active
response work, but not enough to justify a broad public product launch or
irreversible strategic commitment.

Action Ceiling:

`Test`, with a paired `Hold`.

Ceiling-constrained action:

- `Probe` partner and licensing paths with model providers, especially where
  Shutterstock's owned/licensed library and metadata could create a cleaner
  training-data position than open web scraping.
- `Test` a controlled, bounded AI-generation or AI-assisted creative workflow
  path, with legal, provenance, contributor-compensation, and customer-safety
  gates.
- `Hold` unmanaged contributor uploads of AI-generated images until rights,
  provenance, labeling, and library-quality controls are defined.
- `Watch` direct customer demand, legal developments, creator response, and
  stock-platform policy divergence.

Unsupported at cutoff:

- `Commit` to broad AI-generated stock imagery distribution.
- `Move` as an immediate public repositioning unless bounded to a private or
  limited partner test.
- Demand claims about stock-image buyers replacing Shutterstock with AI.
- Claims that litigation, a ban, or a partnership was the only rational path.

## 8. At-Cutoff Replay Memo

Recommendation:

`Test` a controlled partner/data-licensing path for generative image AI while
`Hold`ing unmanaged AI-generated contributor submissions and `Probe`ing
provenance, licensing, and contributor-compensation mechanics.

Evidence basis:

By 2022-09-15, public image generation had crossed from research curiosity into
usable creative tooling. OpenAI had opened DALL-E 2 beta with paid credits and
commercial-use rights. Stability AI had publicly released Stable Diffusion,
creating a lower-friction and more open distribution path. Midjourney was also
publicly available in beta. These signals made generative image workflows
visible to creative users before the cutoff.

Shutterstock was exposed and potentially advantaged. It had a large content
library, many contributors, enterprise and e-commerce licensing channels, API
and workflow integrations, and a preexisting Shutterstock.AI/data strategy.
That combination made the company vulnerable to substitution and library
pollution, but also plausibly well-positioned to license data, partner with a
model provider, or offer a rights-managed AI workflow.

The evidence did not justify a stronger claim. The pool did not show
pre-cutoff Shutterstock customer switching, direct revenue displacement, or a
stable buyer request for AI-generated stock. The best evidence was technology
availability plus actor-strategy fit. Creator and legal concerns were public
enough to matter, but too unsettled to treat as resolved law or as proof that
all AI imagery should be rejected.

Alternatives considered:

- Ban or remove all AI-generated uploads: plausible as a risk-control move,
  but too narrow if customers begin expecting generative workflows and if
  Shutterstock can create a licensed-data advantage.
- Wait for copyright clarity: safer legally, but risks missing a partner/data
  window and gives model providers time to build around open data.
- Partner/license data/build controlled tool: best supported by the evidence,
  because it uses Shutterstock's existing assets while limiting unmanaged
  rights risk.
- Commit broadly to AI stock distribution: unsupported at cutoff because
  demand, rights, and provenance evidence were insufficient.

Uncertainty:

- Whether customers would actually substitute AI generation for stock licenses
  was not proven.
- Whether model training on public or licensed image datasets would withstand
  legal scrutiny was unresolved.
- Whether contributors would accept compensation models for training data was
  unknown.
- Whether open-source tools would flood stock libraries with low-quality or
  rights-ambiguous submissions was plausible but not yet timing-valid by the
  cutoff.

Kill criteria:

- Do not launch broad AI stock licensing if rights, provenance, labeling, and
  contributor compensation cannot be made inspectable.
- Do not count tool virality or creator controversy as buyer demand.
- Do not allow AI-generated contributor uploads to pollute the library without
  clear policy and review controls.
- Do not commit to a single partner path if licensing terms fail to protect
  Shutterstock's customers and contributors.

Update triggers:

- A public stock-platform AI-upload policy change.
- A direct AI data-licensing or model-provider partnership announcement.
- Evidence of Shutterstock customers asking for or using AI-generated stock.
- Copyright-office, court, or regulator movement on AI authorship/training.
- Contributor backlash or acceptance around AI training compensation.
- Competitor launch, ban, lawsuit, or indemnified AI-image product.

Boundary note:

This at-cutoff replay is a decision memo dry run, not a claim that the later
Shutterstock outcome was obvious. It supports a controlled `Probe`/`Test`
response and a `Hold` on unmanaged uploads, not a demand claim or full
commitment.

## 9. Post-Window Outcome Pool

Post-window evidence was inspected only after the at-cutoff replay memo above
was complete.

| ID | Source | Timing | Outcome note |
| --- | --- | --- | --- |
| O-01 | Shutterstock, [OpenAI partnership announcement](https://investor.shutterstock.com/node/12506/pdf) | 2022-10-25 | Shutterstock announced an expanded OpenAI partnership, planned customer image generation, and a contributor fund. |
| O-02 | Shutterstock, [AI Image Generator launch](https://investor.shutterstock.com/news-releases/news-release-details/shutterstock-introduces-generative-ai-its-all-one-creative) | 2023-01-25 | Shutterstock launched an AI image generation platform for customers globally. |
| O-03 | Shutterstock, [six-year OpenAI data agreement](https://investor.shutterstock.com/news-releases/news-release-details/shutterstock-expands-partnership-openai-signs-new-six-year) | 2023-07-11 | Shutterstock expanded the OpenAI partnership, including licensing access to additional Shutterstock training data and metadata. |
| O-04 | Getty Images litigation coverage, [Getty v. Stability AI report](https://gigazine.net/gsc_news/en/20230118-getty-images-suing-stability-ai) | 2023-01-17/18 | Getty pursued litigation against Stability AI, supporting the at-cutoff concern that stock-image AI strategy had material rights risk. |

## 10. Outcome Comparison

The at-cutoff replay would have been directionally useful.

Matched outcome:

- The replay's strongest valid action was a controlled partner/data-licensing
  probe or test rather than unmanaged AI upload acceptance.
- Shutterstock later announced an OpenAI partnership, contributor fund,
  customer-facing AI generation, and expanded training-data licensing.
- The replay's contributor/IP-risk concern also matched the later market
  pattern: Shutterstock leaned into contributor compensation and licensed-data
  framing, while Getty pursued litigation against Stability AI.

Missed or undercalled:

- The replay would not have recommended a public partnership announcement or
  customer-facing integration with high confidence by 2022-09-15.
- It would have treated the partnership path as `Probe`/`Test`, not `Move` or
  `Commit`, because direct Shutterstock buyer demand and rights clarity were
  not yet established.
- It did not identify OpenAI as the specific partner from pre-cutoff evidence,
  even though a partner path was plausible.

Not counted as proof:

- Later outcome similarity does not prove the pre-cutoff evidence was strong
  enough for a stronger action ceiling.
- Later Shutterstock language about responsible AI and contributor funds does
  not retroactively strengthen the pre-cutoff record.

## 11. Calibration Lesson

Foundation Layer should treat "technology availability plus incumbent asset fit" as
enough for `Probe` or bounded `Test` when the decision consequence is high and
the actor has obvious complementary assets.

Foundation Layer should not upgrade that pattern to `Move` or `Commit` without
independent evidence of customer behavior, clear rights/provenance controls,
or handled counterevidence.

For AI-era platform cases, the evidence standard should explicitly separate:

- public model availability;
- customer workflow substitution;
- contributor or rights-holder harm;
- actor-strategy feasibility;
- legal/provenance risk;
- later outcome similarity.

The useful lesson is not "Shutterstock's OpenAI deal was obvious." The lesson
is that the at-cutoff evidence was enough to avoid passive waiting and to frame
a controlled licensed-data/partner experiment before the later outcome was
public.

## 12. Blockers And Residual Risks

No stop-criteria blocker was hit for this slice.

Residual risks:

- Exact archived state of some live pages, especially Hugging Face, was not
  independently captured.
- The pre-cutoff pool is intentionally bounded and may omit sources that were
  publicly visible but not needed for this slice.
- No private customer data, platform analytics, contributor account records,
  or internal Shutterstock decision material was inspected.
- Public customer demand for AI-generated stock before cutoff remains not
  established.
- The at-cutoff action ceiling depends on current Foundation Layer qualitative
  Action Ceiling rules; no numeric scoring exists or is authorized.
- Post-window outcome comparison is calibration only and does not authorize a
  broader proof claim, feature planning, implementation, source maps, or data
  spine creation.

## 13. Slice Verdict

Slice verdict: `pass, useful, underconfident`.

Pass:

The slice preserved leakage controls, recorded source timing, excluded
post-window material from the at-cutoff replay, used inspectable public
market-level evidence, and stayed inside the authorized docs-first target file.

Useful:

The at-cutoff replay would have identified a controlled partner/data-licensing
path and contributor/IP-risk posture before Shutterstock's later public
OpenAI partnership outcome.

Underconfident:

The valid pre-cutoff ceiling was `Test` plus `Hold`, not a stronger public
`Move` or `Commit`. The later Shutterstock outcome moved faster and more
explicitly toward partnership/product launch than the at-cutoff evidence could
cleanly support.
