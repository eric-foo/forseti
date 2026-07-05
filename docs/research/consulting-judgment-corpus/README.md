# Consulting Judgment Corpus Research

This folder holds the public consulting-firm judgment-corpus research lane.

Purpose: identify public consulting case material that exposes enough real decision situation, diagnostic framing, recommendation or strategic choice, implementation/action, and outcome evidence to support later Forseti executive-judgment training and possible backtests.

Date boundary: prioritize AI-era cases where the decision/action/outcome window is on or after `2022-11-30`. If only publication date is known, record it separately and mark decision-window evidence as weak or `not_found`.

Core separation:

- `prompts/`: launch prompts for evidence-only deep-research lanes and later synthesis.
- `lane-outputs/`: raw or lightly normalized evidence-only lane outputs. These should not contain scoring, tiering, or recommendations unless the source lane was explicitly a synthesis lane.
- `candidate-screens/`: deduplicated candidate tables, field-completeness screens, and shortlist preparation notes.
- `synthesis/`: reasoning outputs that score, tier, compare, and recommend candidates from gathered evidence.
- `backtestability/`: external evidence hooks and pre-backtest notes. This folder does not execute backtests.
- `reject-patterns/`: maps of source types and queries that looked promising but failed the corpus criteria.

Non-claims:

- This research does not prove buyer validation, willingness to pay, product readiness, feature readiness, implementation readiness, or commercial readiness.
- Consulting-firm outcome claims are not externally verified unless paired with separate external evidence.
- Inclusion in this folder does not mean a case is selected for backtesting.
