"""The fail-closed sibling-selection rule (``data_lake.sibling_selection``).

The contract under test (unit (c) spec): identical content collapses; within one
anchor the caller-declared derivation rank supersedes -- NEVER lexical order; across
anchors the newest parsed capture instant wins; ambiguous or unorderable siblings
raise ``SiblingSelectionError`` instead of silently picking one; observed counts and
record refs never order the choice (the F-IGRC-001 class).
"""
from __future__ import annotations

import pytest

from data_lake.sibling_selection import (
    SiblingCandidate,
    SiblingSelectionError,
    parse_capture_instant,
    select_current_record_per_subject,
)


def _candidate(
    *,
    subject: str = "creator",
    anchor: str = "packet_a",
    ref: str,
    content: str,
    instant: str | None = None,
    rank: int = 0,
) -> SiblingCandidate:
    return SiblingCandidate(
        subject_key=subject,
        raw_anchor=anchor,
        record_ref=ref,
        content_hash=content,
        capture_instant_or_none=parse_capture_instant(instant),
        derivation_rank=rank,
        payload=ref,
    )


# --- within-anchor rank ---------------------------------------------------------


def test_higher_rank_wins_even_when_it_sorts_lexically_below_the_lower_rank() -> None:
    # The F-IGRC-001 regression guard: the old rule tie-broke by lexically GREATEST
    # path. Here the higher-rank record ref sorts lexically BELOW the lower-rank
    # one, so a lexical rule would pick the stale record; the rank must win.
    stale = _candidate(ref="zz_stale_catalog.json", content="aaa", rank=0)
    catchup = _candidate(ref="aa_catchup_rederivation.json", content="bbb", rank=1)

    selection = select_current_record_per_subject([stale, catchup])

    assert selection["creator"].selected.record_ref == "aa_catchup_rederivation.json"
    assert [c.record_ref for c in selection["creator"].bypassed] == ["zz_stale_catalog.json"]


def test_same_anchor_same_rank_distinct_content_fails_closed() -> None:
    first = _candidate(ref="one.json", content="aaa")
    second = _candidate(ref="two.json", content="bbb")

    with pytest.raises(SiblingSelectionError) as excinfo:
        select_current_record_per_subject([first, second])

    assert excinfo.value.reason == "ambiguous_sibling_derivation"
    assert excinfo.value.subject_key == "creator"


def test_identical_content_collapses_without_error() -> None:
    # Same content within an anchor AND across anchors: identical bytes cannot
    # disagree, so no ambiguity; the representative is the lexically smallest ref
    # (pure determinism, not a content choice).
    a = _candidate(ref="b_copy.json", content="aaa", instant="2026-07-01T00:00:00Z")
    b = _candidate(ref="a_copy.json", content="aaa", instant="2026-07-01T00:00:00Z")
    c = _candidate(anchor="packet_b", ref="c_copy.json", content="aaa", instant="2026-07-01T00:00:00Z")

    selection = select_current_record_per_subject([a, b, c])

    assert selection["creator"].selected.record_ref == "a_copy.json"
    assert selection["creator"].bypassed == ()


# --- cross-anchor recency -------------------------------------------------------


def test_newest_capture_instant_wins_across_anchors() -> None:
    older = _candidate(anchor="packet_a", ref="older.json", content="aaa", instant="2026-07-01T00:00:00Z")
    newer = _candidate(anchor="packet_b", ref="newer.json", content="bbb", instant="2026-07-02T00:00:00Z")

    selection = select_current_record_per_subject([older, newer])

    assert selection["creator"].selected.record_ref == "newer.json"
    assert [c.record_ref for c in selection["creator"].bypassed] == ["older.json"]


def test_missing_capture_instant_fails_closed_when_ordering_is_required() -> None:
    dated = _candidate(anchor="packet_a", ref="dated.json", content="aaa", instant="2026-07-01T00:00:00Z")
    undated = _candidate(anchor="packet_b", ref="undated.json", content="bbb", instant=None)

    with pytest.raises(SiblingSelectionError) as excinfo:
        select_current_record_per_subject([dated, undated])

    assert excinfo.value.reason == "unorderable_capture_recency"


def test_single_candidate_succeeds_without_any_capture_instant() -> None:
    only = _candidate(ref="only.json", content="aaa", instant=None)

    selection = select_current_record_per_subject([only])

    assert selection["creator"].selected.record_ref == "only.json"


def test_equal_instants_distinct_content_fail_closed() -> None:
    a = _candidate(anchor="packet_a", ref="a.json", content="aaa", instant="2026-07-01T00:00:00Z")
    b = _candidate(anchor="packet_b", ref="b.json", content="bbb", instant="2026-07-01T00:00:00Z")

    with pytest.raises(SiblingSelectionError) as excinfo:
        select_current_record_per_subject([a, b])

    assert excinfo.value.reason == "unorderable_capture_recency"


def test_rank_then_recency_compose_and_all_bypassed_are_reported() -> None:
    # anchor_a: catch-up supersedes the catalog record; anchor_b: an older capture.
    # The anchor_a winner is newer -> selected; both distinct-content losers surface.
    catalog = _candidate(anchor="packet_a", ref="bronze_catalog.json", content="aaa", instant="2026-07-02T00:00:00Z")
    catchup = _candidate(anchor="packet_a", ref="zz_catchup.json", content="bbb", instant="2026-07-02T00:00:00Z", rank=1)
    older = _candidate(anchor="packet_b", ref="older.json", content="ccc", instant="2026-07-01T00:00:00Z")

    selection = select_current_record_per_subject([catalog, catchup, older])

    assert selection["creator"].selected.record_ref == "zz_catchup.json"
    assert sorted(c.record_ref for c in selection["creator"].bypassed) == [
        "bronze_catalog.json",
        "older.json",
    ]


def test_subjects_are_selected_independently() -> None:
    one = _candidate(subject="one", ref="one.json", content="aaa")
    two = _candidate(subject="two", anchor="packet_b", ref="two.json", content="bbb")

    selection = select_current_record_per_subject([one, two])

    assert selection["one"].selected.record_ref == "one.json"
    assert selection["two"].selected.record_ref == "two.json"


# --- observed-count exclusion (the removed bug) ----------------------------------


def test_observed_count_never_orders_the_choice() -> None:
    # The rule has no observed_count input at all; this proves the seed's old
    # "fuller-but-staler beats newer" behavior cannot re-enter through the rule:
    # recency alone decides between distinct-content anchor winners.
    fuller_older = _candidate(anchor="packet_a", ref="fuller_older.json", content="aaa", instant="2026-07-01T00:00:00Z")
    thinner_newer = _candidate(anchor="packet_b", ref="thinner_newer.json", content="bbb", instant="2026-07-03T00:00:00Z")

    selection = select_current_record_per_subject([fuller_older, thinner_newer])

    assert selection["creator"].selected.record_ref == "thinner_newer.json"


# --- parse_capture_instant --------------------------------------------------------


def test_parse_capture_instant_normalizes_z_and_treats_naive_as_utc() -> None:
    zulu = parse_capture_instant("2026-07-01T00:00:00Z")
    naive = parse_capture_instant("2026-07-01T00:00:00")

    assert zulu is not None and naive is not None
    assert zulu == naive
    assert zulu.tzinfo is not None


def test_parse_capture_instant_returns_none_for_empty_values() -> None:
    assert parse_capture_instant(None) is None
    assert parse_capture_instant("") is None
    assert parse_capture_instant("   ") is None
