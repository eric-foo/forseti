from __future__ import annotations

import json
from types import SimpleNamespace

from source_capture.adapters.nordstrom_country_preference import (
    NORDSTROM_REVIEW_POSTURES,
    NordstromCountryPreferencePlugin,
    observe_nordstrom_deep_review_window,
)
from source_capture import nordstrom_brand_corpus as nordstrom_corpus
from source_capture.nordstrom_brand_corpus import (
    NordstromDeepPdpReceipt,
    NordstromGridCard,
    NordstromGridProjection,
    NordstromPdpEvidence,
    NordstromReviewOrderReceipt,
    build_nordstrom_grid_projection,
    verify_nordstrom_corpus,
)
from source_capture.retail_capture_profiles import get_retail_capture_profile
from runners import run_nordstrom_brand_corpus as corpus_runner


def _grid_dom(*, declared: int = 2, duplicate: bool = False) -> str:
    second_id = "5124297" if duplicate else "5583442"
    return f"""
    <body><div>{declared} items</div>
      <article><a href="/s/ilia-limitless-lash-mascara/5124297?origin=category">
      </a><h3><a><strong>ILIA</strong> Limitless Lash Mascara</a></h3>
      <a aria-label="4.5 out of 5 stars">(6,450)</a></article>
      <article><a href="/s/ilia-super-serum-skin-tint-spf-40/{second_id}?origin=category">
      </a><h3><a><strong>ILIA</strong> Super Serum Skin Tint SPF 40</a></h3>
      <a aria-label="4.4 out of 5 stars">(12,794)</a></article>
    </body>
    """


def _order(sort: str) -> NordstromReviewOrderReceipt:
    return NordstromReviewOrderReceipt(
        requested_sort=sort,
        observed_sort=sort,
        source_url="https://www.nordstrom.com/s/x/5583442",
        source_total_count=12794,
        observed_row_count=102,
        retained_row_count=100,
        continuation_available=True,
        continuation_activations=16,
        rows=[],
        rendered_dom_sha256="a" * 64,
        status="complete",
    )


def test_grid_projection_reconciles_declared_cards_and_unique_ids() -> None:
    projection = build_nordstrom_grid_projection(
        rendered_dom=_grid_dom(),
        source_url="https://www.nordstrom.com/brands/ilia--47014323",
    )

    assert projection.status == "complete"
    assert projection.declared_count == len(projection.cards) == 2
    assert [card.product_id for card in projection.cards] == ["5124297", "5583442"]
    assert projection.cards[1].review_count == 12794


def test_grid_projection_fails_closed_on_duplicate_or_count_drift() -> None:
    projection = build_nordstrom_grid_projection(
        rendered_dom=_grid_dom(declared=3, duplicate=True),
        source_url="https://www.nordstrom.com/brands/ilia--47014323",
    )

    assert projection.status == "partial"
    assert "duplicate product ids" in " ".join(projection.residuals)
    assert "declared_count=3" in " ".join(projection.residuals)


def test_deep_observation_accepts_provider_batch_overrun_but_caps_retention() -> None:
    rows = "".join(
        f'<div id="review-{index}">review {index}</div>' for index in range(1, 103)
    )
    dom = f"""
    <script type="application/ld+json">
    {{"@type":"Product","url":"https://www.nordstrom.com/s/x/5583442",
      "aggregateRating":{{"reviewCount":12794}}}}
    </script>
    <section id="product-page-reviews">
      <button id="sort-by-filter-5583442-anchor">Sort by <strong>Most Helpful</strong></button>
      {rows}<a href="?page=18">Load 6 more reviews</a>
    </section>
    """

    observation = observe_nordstrom_deep_review_window(
        dom, requested_sort="Most Helpful", limit=100
    )

    assert observation["admitted"] is True
    assert observation["captured_review_count"] == 102
    assert observation["retained_review_count"] == 100
    assert observation["continuation_activations"] == 16


def test_review_order_admission_is_independent_of_retention_limit(
    tmp_path, monkeypatch
) -> None:
    rows = "".join(
        f'<div id="review-{index}">review {index}</div>' for index in range(1, 103)
    )
    dom = f"""
    <script type="application/ld+json">
    {{"@type":"Product","url":"https://www.nordstrom.com/s/x/5583442",
      "aggregateRating":{{"reviewCount":12794}}}}
    </script>
    <section id="product-page-reviews">
      <button id="sort-by-filter-5583442-anchor">Sort by <strong>Most Helpful</strong></button>
      {rows}<a href="?page=18">Load 6 more reviews</a>
    </section>
    """
    packet = SimpleNamespace(
        source_locator=SimpleNamespace(
            value="https://www.nordstrom.com/s/x/5583442"
        )
    )
    monkeypatch.setattr(
        nordstrom_corpus,
        "load_verified_rendered_dom",
        lambda _: (packet, dom, "a" * 64),
    )

    receipt = nordstrom_corpus.build_nordstrom_review_order_receipt(
        packet_directory=tmp_path,
        requested_sort="Most Helpful",
        limit=50,
    )

    assert receipt.observed_row_count == 102
    assert receipt.retained_row_count == len(receipt.rows) == 50
    assert receipt.shortfalls == []


def test_deep_review_failure_persists_partial_run_receipt(
    tmp_path, monkeypatch
) -> None:
    card = NordstromGridCard(
        position=1,
        product_id="5583442",
        product_url="https://www.nordstrom.com/s/x/5583442",
        brand_name="ILIA",
        product_name="Super Serum Skin Tint",
        review_count=12794,
    )
    grid = NordstromGridProjection(
        source_url="https://www.nordstrom.com/brands/ilia--47014323",
        brand_name="ILIA",
        brand_id="47014323",
        declared_count=1,
        cards=[card],
        status="complete",
    )
    monkeypatch.setattr(corpus_runner, "load_nordstrom_grid_packet", lambda **_: grid)
    monkeypatch.setattr(
        corpus_runner,
        "build_nordstrom_pdp_evidence",
        lambda **kwargs: NordstromPdpEvidence(
            product_id=card.product_id,
            source_url=card.product_url,
            final_url=card.product_url,
            brand_name=card.brand_name,
            product_name=card.product_name,
            seller="Nordstrom",
            packet_directory=str(kwargs["packet_directory"]),
            manifest_sha256="a" * 64,
            rendered_dom_sha256="b" * 64,
        ),
    )
    monkeypatch.setattr(
        corpus_runner,
        "build_nordstrom_review_order_receipt",
        lambda **_: (_ for _ in ()).throw(ValueError("invalid deep window")),
    )
    output_root = tmp_path / "run"

    exit_code, receipt = corpus_runner.run_nordstrom_brand_corpus(
        brand_url=grid.source_url,
        authorization_url="https://iliabeauty.com/official",
        authorization_statement="official",
        output_root=output_root,
        resume_grid_packet=tmp_path / "grid",
        capture_main=lambda _: 0,
    )

    persisted = json.loads((output_root / "run-receipt.json").read_text("utf-8"))
    assert exit_code == 3
    assert receipt.status == "partial"
    assert str(receipt.failure).startswith(
        "nordstrom_deep_review_failed:most-helpful:ValueError:invalid deep window"
    )
    assert receipt.captured_pdp_count == 1
    assert receipt.pdp_evidence_paths.keys() == {card.product_id}
    assert persisted == receipt.model_dump(mode="json")


def test_corpus_verifier_rejects_identity_or_candidate_perturbation() -> None:
    grid = build_nordstrom_grid_projection(
        rendered_dom=_grid_dom(),
        source_url="https://www.nordstrom.com/brands/ilia--47014323",
    )
    pdps = [
        NordstromPdpEvidence(
            product_id=card.product_id,
            source_url=card.product_url,
            final_url=card.product_url,
            brand_name="ILIA",
            product_name=card.product_name,
            seller="Nordstrom",
            packet_directory=f"C:/packets/{card.product_id}",
            manifest_sha256="a" * 64,
            rendered_dom_sha256="b" * 64,
        )
        for card in grid.cards
    ]
    deep = NordstromDeepPdpReceipt(
        product_id="5124297",
        source_url=grid.cards[0].product_url,
        selection_basis="perturbed",
        most_helpful=_order("Most Helpful"),
        most_recent=_order("Most Recent"),
        status="complete",
    )

    receipt = verify_nordstrom_corpus(grid=grid, pdps=pdps[:-1], deep=deep)

    assert receipt.status == "partial"
    assert "one-to-one" in " ".join(receipt.residuals)
    assert "highest-review" in " ".join(receipt.residuals)


def test_nordstrom_profile_is_product_generic_and_deep_postures_are_admitted() -> None:
    profile = get_retail_capture_profile("nordstrom_pdp_aggregate")
    serialized = repr(profile)

    assert "The Lip Balm" not in serialized
    assert "Nécessaire" not in serialized
    assert set(NORDSTROM_REVIEW_POSTURES) == {
        "recent_window_30d",
        "most_helpful_100",
        "most_recent_100",
    }
    deep_description = NordstromCountryPreferencePlugin(
        target_url="https://www.nordstrom.com/s/x/5583442",
        review_posture="most_helpful_100",
    ).describe()
    assert deep_description["nordstrom_review_window_days"] is None
    assert deep_description["nordstrom_review_minimum"] == 100
    assert deep_description["nordstrom_review_maximum"] == 100


def test_resume_revalidates_and_rejects_stale_pdp_before_any_new_capture(
    tmp_path, monkeypatch
) -> None:
    card = NordstromGridCard(
        position=1,
        product_id="5124297",
        product_url="https://www.nordstrom.com/s/x/5124297",
        brand_name="ILIA",
        product_name="Mascara",
        review_count=1,
    )
    grid = NordstromGridProjection(
        source_url="https://www.nordstrom.com/brands/ilia--47014323",
        brand_name="ILIA",
        brand_id="47014323",
        declared_count=1,
        cards=[card],
        status="complete",
    )
    resume_root = tmp_path / "prior"
    (resume_root / "pdp" / card.product_id).mkdir(parents=True)
    capture_calls: list[list[str]] = []
    monkeypatch.setattr(corpus_runner, "load_nordstrom_grid_packet", lambda **_: grid)
    monkeypatch.setattr(
        corpus_runner,
        "build_nordstrom_pdp_evidence",
        lambda **_: (_ for _ in ()).throw(ValueError("stale packet hash")),
    )

    exit_code, receipt = corpus_runner.run_nordstrom_brand_corpus(
        brand_url=grid.source_url,
        authorization_url="https://iliabeauty.com/official",
        authorization_statement="official",
        output_root=tmp_path / "new",
        resume_grid_packet=tmp_path / "grid",
        resume_from=resume_root,
        capture_main=lambda args: capture_calls.append(list(args or ())) or 0,
    )

    assert exit_code == 3
    assert receipt.status == "partial"
    assert "stale packet hash" in str(receipt.failure)
    assert capture_calls == []


def test_corpus_capture_args_never_request_proxy_profile_login_or_vpn(tmp_path) -> None:
    args = corpus_runner._capture_args(
        url="https://www.nordstrom.com/s/x/5583442",
        output=tmp_path / "packet",
        profile="nordstrom_pdp_aggregate",
        review_posture="most_helpful_100",
    )
    joined = " ".join(args).casefold()

    assert "--nordstrom-country us" in joined
    assert "--retention-mode raw" in joined
    assert "--proxy" not in joined
    assert "--browser-user-data" not in joined
    assert "no vpn, proxy, stored browser profile, login" in joined
