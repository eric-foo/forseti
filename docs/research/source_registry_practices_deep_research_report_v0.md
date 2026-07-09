# Source-Registry Practices — Deep Research Report v0 (Atlas lane input)

```yaml
retrieval_header_version: 1
artifact_role: Research artifact
scope: >
  Adversarially-verified deep-research findings on how mature practice
  communities build, govern, and keep fresh curated "where to look" source
  registries — commissioned as design ingredients and failure modes for a
  possible bounded STATIC Orca venue-atlas (pre-decision consumer-demand
  signal, beauty/personal-care first). Verified coverage: academic-library
  LibGuides + Bellingcat's OSINT toolkit only; five requested communities and
  the LLM-corpus bonus produced no surviving claims (open questions).
use_when:
  - Deciding whether/how to build the Orca venue-atlas lane (owner decision).
  - Designing per-entry metadata, governance, or review cadence for any Orca registry.
  - Commissioning a follow-up research pass on the unanswered communities.
authority_boundary: retrieval_only
open_next:
  - forseti/product/spines/foundation/vertical_exploration/orca_memorization_resistant_case_finder_frame_v0.md
  - docs/decisions/judgment_spine_backtest_batch1_ledger_declaration_v0.md
stale_if:
  - The owner chooses an Atlas lane (then the lane decision record supersedes this as the operative source).
  - A follow-up research pass covers the five unanswered communities or the LLM-corpus question.
```

## What this is

The preserved output of an owner-commissioned deep-research run (2026-06-11,
workflow run `wf_bdf220d8-95f`): 5 search angles, 25 sources fetched, 124 claims
extracted, top 25 adversarially verified by 3-vote panels (24 confirmed, 1
refuted), synthesized to 10 findings. Findings are **ingredients and failure
modes** for designing Orca's own lane — explicitly not a template to copy, and
not a lane decision. The finder frame's must-not boundary (no source maps,
monitors, scrapers, standing intake) is untouched by this artifact.

## Headline

Verified evidence survived for **two of seven** requested communities —
academic-library LibGuides (the default failure trajectory) and Bellingcat's
2024 OSINT toolkit (the deliberate counter-design) — and together they bracket
the design space. Load-bearing ingredients for a static venue-atlas: a hard
curation bound; per-entry freshness and ownership metadata; an enforced review
cadence with named owners; and delivery into the moment of decision (registries
are consulted episodically, never routinely).

## Verified findings

1. **Distributed authorship defaults to honor-system governance.** (high, 3-0 ×4)
   Fall-2019 survey of 120 academic libraries using LibGuides: 53% had content
   guidelines; 23% had any pre-publication review (only 4% used the CMS
   workflow) — 77% published unchecked; post-publication, 27% reviewed all
   guides systematically, 15% never, 84% author self-review. Authors conclude
   LibGuides run on an "honour system"; a 2024 source independently confirms no
   formal peer review is typical. Caveat: self-selected convenience sample,
   North-America-heavy. Sources: Logan & Spence 2021
   (sciencedirect.com/science/article/abs/pii/S0099133320301737); Moukhliss &
   McCowan 2024 (inthelibrarywiththeleadpipe.org/2024/proposed-library-guide-assessment-standards).

2. **Under honor-system governance, rot is rapid, pervasive, expensive — and
   tooling does not substitute for cadence.** (high, 3-0 ×3) 82% of 260
   analyzed subject guides across 101 ARL libraries (2011–13) contained dead
   links even though 94% of libraries used automated link-checkers — only 19%
   checked on a schedule. 21% of guides showed no last-revision date; max
   staleness 1,677 days (4.5+ years). A University of Michigan cleanup took ~60
   hours to unpublish/remove 42% of pages and reassign ownership of another 20%.
   Sources: as above + Jackson & Stacy-Bates, RUSQ 2016
   (journals.ala.org/rusq/article/view/5933).

3. **Bloat is the signature content failure and persists against the field's
   own doctrine.** (high, 3-0 ×3) Median links per guide roughly doubled
   2002→2011-13 (chemistry 43→88, journalism 56→105, philosophy 37→77) despite
   published "not a laundry list" guidance; the "kitchen sink" approach is
   documented; recurring usability failures: hard navigation, unnecessary
   content, insider jargon. Sources: RUSQ 2016; Lead Pipe 2024.

4. **Direct evidence that curated guides are valued is weak-to-negative;
   non-use is driven more by discoverability than content quality.** (high,
   3-0 ×4) 40% of one user survey rated guides not/little helpful; students
   rarely use them (unaware they exist; prefer familiar search; feel no need);
   2024 literature attributes underutilization "largely" to not knowing guides
   exist. Verifier nuance: among actual users, satisfaction can be high (97%
   rated useful in one study where two-thirds were unaware the guides existed)
   — the binding constraint is awareness/distribution into the workflow.
   Sources: RUSQ 2016; Ouellette 2011 (muse.jhu.edu/article/456406); Lead Pipe 2024.

5. **Usage is event-driven, never routine.** (medium, 3-0) Exactly three
   trigger conditions identified: stuck (last resort), unfamiliar discipline,
   or explicit referral by an instructor/authority. Small-N qualitative (n=11,
   2011) — treat as well-grounded hypotheses. Source: Ouellette 2011.

6. **Template standardization alone does not create usage; organization must
   match the consumer's task model.** (medium, 3-0 ×3) Kennesaw State usage
   stayed flat/declining for years after a standard template (2014); card sorts
   show users organize by research-process stage (every sort produced a
   "Getting Started" category), not curator source-type taxonomies; in
   usability testing (n=40) a most-common behavior was heading straight for a
   search box, rarely scrolling past mid-page. Source: Barker & Hoffman, C&RL
   82(1) 2021 (crl.acrl.org/index.php/crl/article/view/24754/32577).

7. **The library field's emerging countermeasure imports formal QA gates:**
   (medium, 3-0) the 2024 LGAS proposal sets an explicit pass gate (peer-review
   team must rate 85% of standards "Met"), operationalized at the University of
   North Florida — but with no published outcome data yet. Ingredient: an
   explicit numeric pass/fail quality gate. Source: Lead Pipe 2024.

8. **Bellingcat's 2024 toolkit is a current working model of per-entry registry
   structure.** (high, 3-0 ×2) Category taxonomy with alphabetical listing; a
   fixed per-entry template — URL, description, three-level cost grade
   (free/partially free/paid), difficulty, requirements, limitations, ethical
   considerations, linked guides; standardized "Details" pages (partial
   coverage so far); natural-language search. Structure derived from interviews
   with 40 practitioners; volunteer reviewers apply a fixed evaluation-category
   list. Sources: gijn.org/stories/bellingcat-new-online-investigations-toolkit;
   niemanreports.org/osint-open-source-investigations-bellingcat-volunteers;
   bellingcat.gitbook.io/toolkit (live-verified June 2026).

9. **Bellingcat's anti-rot governance = three named mechanisms.** (high, 3-0 ×3)
   (1) centralized editorial gatekeeping — staff check every entry
   pre-publication; non-compliant volunteers removed; (2) enforced cadence —
   deadlines for new AND updated reviews against a written consistency ruleset,
   monthly update commitments; (3) named ownership at two granularities —
   per-entry "Maintainers", per-category "Guardians". Boundary: designed,
   self-described governance; effectiveness not independently audited; toolkit
   ~21 months old at research time. Sources: as finding 8.

10. **Staleness is the empirically top-ranked abandonment driver — and
    registries are not practitioners' preferred discovery route.** (medium,
    3-0) In Bellingcat's 40-practitioner interviews, the #1 reason existing
    OSINT toolkits weren't used often was lack of regular updates; barely any
    interviewee preferred toolkits for tool discovery (search engines, blogs,
    peers won). Against-interest candor from a toolkit publisher strengthens
    credibility. Sources: as finding 8.

## Refuted — do not carry forward

- "Entry volatility (tool discontinuations, e.g. Twint/CrowdTangle) is the
  dominant documented failure mode for OSINT registries" — **refuted 0-3**.
  Staleness, not tool-death, is the evidenced top driver.

## Caveats (verbatim-faithful condensation)

- **Coverage gap dominates:** investigative-journalism source databases,
  competitive-intelligence maps, finance alt-data catalogs, PRISMA
  search-provenance documentation, and Archive Team wikis produced no surviving
  claims; the search/coverage-provenance axis is essentially unaddressed
  (PRISMA was its natural home). The LLM-training-corpus bonus produced nothing.
- **Dated samples:** library statistics are 2003–2019 vintage (RUSQ rot data
  2011–13; survey Fall-2019 convenience sample). The cross-study pattern (thin
  governance → rot, bloat, low awareness-driven use) is convergent, but
  individual percentages must not be quoted as current-state rates.
- **Bellingcat evidence is first-party** (toolkit lead's own accounts,
  corroborated against the live artifact): establishes designed governance and
  observable structure, not audited multi-year durability.
- Medium-confidence findings rest on a single verified source with
  corroboration, not multiple independent primaries.

## Open questions (follow-up candidates, owner's call)

1. How do PRISMA/PRISMA-S and Archive Team document search/coverage provenance
   and handle staleness? (The unanswered provenance axis — closest template for
   an atlas's "where we looked and why".)
2. Which venue types are over-/under-represented in LLM training corpora
   (Reddit vs paywalled trade press vs niche beauty forums), and what does that
   imply for memorization risk of cases sourced from each? (Nothing survived.)
3. Does Bellingcat's enforced-cadence + named-ownership model measurably
   outperform honor-system maintenance over multi-year horizons, or regress
   once launch energy fades? (No outcome data yet.)
4. Minimum viable governance at small scale: does a single-owner registry with
   a fixed review cadence dominate distributed authorship for an atlas of
   Orca's size? (The guideline-existence ≠ enforcement evidence suggests yes,
   unproven.)

## Provenance

Workflow run `wf_bdf220d8-95f` (deep-research harness), 2026-06-11; 107 agent
calls; 5 angles; 25 sources fetched; 124 claims extracted; 25 verified by
3-vote adversarial panels (24 confirmed, 1 killed); 10 findings after semantic
merge. Source list and full verification notes preserved in the run output
(task `wrbowbbk5`); this artifact is the durable copy of record.

## Non-Claims

- Research input only: not doctrine, not a lane decision, not finder-frame
  sign-off or amendment, not validation, not readiness.
- Does not authorize any build, crawler, monitor, source map, or capture run.
- The finder frame's must-not boundary stands until the owner amends it
  deliberately at sign-off.
