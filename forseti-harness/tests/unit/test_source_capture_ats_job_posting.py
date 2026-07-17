from __future__ import annotations

import argparse
import json
from pathlib import Path

import pytest

from source_capture.adapters.ats_job_posting import (
    AtsBoardCaptureFailure,
    AtsBoardCaptureSuccess,
    AtsCaptureFailureKind,
    AtsHttpResponse,
    AtsTransportError,
    AtsVendor,
    ashby_board_url,
    fetch_ashby_board,
    fetch_greenhouse_board,
    fetch_lever_board,
    fetch_workday_board,
    greenhouse_board_url,
    lever_board_url,
    workday_jobs_url,
)
from source_capture.ats_job_posting_projection import (
    build_ats_job_posting_projection_from_packet_directory,
)
from runners.run_source_capture_ats_job_posting_packet import (
    run_source_capture_ats_job_posting_packet,
)


# --- fake transport seam (no live network) ----------------------------------


def _resp(status: int, obj, *, url: str = "https://x", headers: dict | None = None) -> AtsHttpResponse:
    body = obj if isinstance(obj, bytes) else json.dumps(obj).encode("utf-8")
    return AtsHttpResponse(status=status, body=body, final_url=url, headers=headers or {})


class _FakeTransport:
    def __init__(self) -> None:
        self.get_map: dict[str, object] = {}   # url-substring -> AtsHttpResponse | Exception
        self.post_queue: list[object] = []      # sequential AtsHttpResponse | Exception
        self.calls: list[tuple[str, str, dict, bytes | None]] = []

    def get(self, *, url: str, headers) -> AtsHttpResponse:
        self.calls.append(("GET", url, dict(headers), None))
        for key, val in self.get_map.items():
            if key in url:
                if isinstance(val, list):  # per-URL queue: distinct response per call
                    val = val.pop(0)
                if isinstance(val, Exception):
                    raise val
                return val  # type: ignore[return-value]
        raise AssertionError(f"unexpected GET {url}")

    def post(self, *, url: str, headers, body) -> AtsHttpResponse:
        self.calls.append(("POST", url, dict(headers), body))
        val = self.post_queue.pop(0)
        if isinstance(val, Exception):
            raise val
        return val  # type: ignore[return-value]


def _noop_sleep(_seconds: float) -> None:
    return None


# --- per-vendor happy paths --------------------------------------------------


def test_greenhouse_happy_path_parses_verbatim_fields():
    transport = _FakeTransport()
    transport.get_map[greenhouse_board_url("acme")] = _resp(
        200,
        {
            "jobs": [
                {
                    "id": 123,
                    "title": "Senior Cosmetic Chemist",
                    "location": {"name": "New York, NY"},
                    "content": "<p>Formulate <b>lipstick</b></p>",
                    "absolute_url": "https://boards.greenhouse.io/acme/jobs/123",
                    "first_published": "2026-07-01T00:00:00Z",
                }
            ]
        },
    )
    result = fetch_greenhouse_board(company="Acme Beauty", board_token="acme", transport=transport)
    assert isinstance(result, AtsBoardCaptureSuccess)
    assert result.vendor is AtsVendor.GREENHOUSE
    (posting,) = result.postings
    assert posting.ats_job_id == "123"
    assert posting.title == "Senior Cosmetic Chemist"
    assert posting.description == "Formulate lipstick"
    assert posting.location_raw == "New York, NY"
    assert posting.location_country is None  # greenhouse exposes no reliable structured country
    assert posting.posted_date == "2026-07-01T00:00:00Z"
    assert posting.source_url == "https://boards.greenhouse.io/acme/jobs/123"


def test_greenhouse_entity_encoded_html_is_stripped_to_text():
    # Greenhouse returns `content` as ENTITY-ENCODED HTML; the description must
    # come out as plain text, not literal "<h3>" tags (regression: unescape first).
    transport = _FakeTransport()
    transport.get_map[greenhouse_board_url("acme")] = _resp(
        200,
        {
            "jobs": [
                {
                    "id": 9,
                    "title": "Esthetician",
                    "location": {"name": "Remote"},
                    "content": "&lt;h3&gt;&lt;strong&gt;Overview&lt;/strong&gt;&lt;/h3&gt;&lt;p&gt;Do skin &amp;amp; care&lt;/p&gt;",
                    "absolute_url": "https://x/9",
                }
            ]
        },
    )
    result = fetch_greenhouse_board(company="Acme", board_token="acme", transport=transport)
    assert isinstance(result, AtsBoardCaptureSuccess)
    (posting,) = result.postings
    assert posting.description == "Overview Do skin & care"
    assert "<" not in (posting.description or "")


def test_lever_uses_structured_country_not_location_string():
    transport = _FakeTransport()
    transport.get_map[lever_board_url("acmebeauty")] = _resp(
        200,
        [
            {
                "id": "abc-1",
                "text": "Perfumer",
                "categories": {"location": "Paris, France"},
                "country": "FR",
                "descriptionPlain": "Blend fine fragrances",
                "hostedUrl": "https://jobs.lever.co/acmebeauty/abc-1",
                "createdAt": 1_700_000_000_000,
            }
        ],
    )
    result = fetch_lever_board(company="Acme Beauty", board_token="acmebeauty", transport=transport)
    assert isinstance(result, AtsBoardCaptureSuccess)
    (posting,) = result.postings
    assert posting.title == "Perfumer"
    assert posting.location_raw == "Paris, France"
    assert posting.location_country == "FR"  # structured country, per jb's verified finding
    assert posting.posted_date is not None and posting.posted_date.endswith("Z")


def test_ashby_extracts_structured_country_and_is_listed():
    transport = _FakeTransport()
    transport.get_map[ashby_board_url("acme")] = _resp(
        200,
        {
            "jobs": [
                {
                    "id": "j1",
                    "title": "Brand Marketing Manager",
                    "location": "New York, NY (HQ)",
                    "descriptionPlain": "Own the brand narrative",
                    "publishedAt": "2026-06-01T00:00:00Z",
                    "jobUrl": "https://jobs.ashbyhq.com/acme/j1",
                    "isListed": True,
                    "address": {"postalAddress": {"addressCountry": "USA"}},
                }
            ]
        },
    )
    result = fetch_ashby_board(company="Acme Beauty", job_board_name="acme", transport=transport)
    assert isinstance(result, AtsBoardCaptureSuccess)
    (posting,) = result.postings
    assert posting.location_country == "USA"
    assert posting.is_listed is True
    assert posting.description == "Own the brand narrative"


def test_workday_paginates_list_and_fetches_detail_description():
    transport = _FakeTransport()
    jobs_url = workday_jobs_url("acme", "wd1", "External")
    transport.post_queue = [
        _resp(
            200,
            {
                "total": 1,
                "jobPostings": [
                    {"title": "QA Analyst", "externalPath": "/job/QA_123", "locationsText": "Austin, TX"}
                ],
            },
        )
    ]
    transport.get_map["/job/QA_123"] = _resp(
        200,
        {
            "jobPostingInfo": {
                "jobDescription": "<p>Test cosmetics QA</p>",
                "startDate": "2026-05-01",
                "externalUrl": "https://acme.wd1.myworkdayjobs.com/External/job/QA_123",
                "country": {
                    "descriptor": "United States of America",
                    "id": "country-id",
                },
            }
        },
    )
    result = fetch_workday_board(
        company="Acme Beauty",
        tenant="acme",
        wd_server="wd1",
        site="External",
        transport=transport,
        sleep=_noop_sleep,
    )
    assert isinstance(result, AtsBoardCaptureSuccess)
    (posting,) = result.postings
    assert posting.title == "QA Analyst"
    assert posting.description == "Test cosmetics QA"
    assert posting.location_raw == "Austin, TX"
    assert posting.location_country == "United States of America"
    assert posting.posted_date == "2026-05-01"
    assert jobs_url in {call[1] for call in transport.calls if call[0] == "POST"}
    envelope = json.loads(result.raw_board_document)
    assert json.loads(envelope["list_page_documents"][0])["total"] == 1
    (detail_slot,) = envelope["job_detail_documents"]
    assert detail_slot["external_path"] == "/job/QA_123"
    assert (
        json.loads(detail_slot["response_body"])["jobPostingInfo"]["country"]["descriptor"]
        == "United States of America"
    )


def test_workday_duplicate_external_paths_keep_distinct_ordered_detail_bodies():
    # F8: detail responses are ordered slots, never a path-keyed map — two postings
    # sharing an externalPath must retain DISTINCT ordered bodies (no dedupe/overwrite),
    # and each posting pairs positionally with its own detail.
    transport = _FakeTransport()
    path = "/job/DUP_1"
    transport.post_queue = [
        _resp(
            200,
            {
                "total": 2,
                "jobPostings": [
                    {"title": "First listing", "externalPath": path},
                    {"title": "Second listing", "externalPath": path},
                ],
            },
        )
    ]
    transport.get_map[path] = [
        _resp(200, {"jobPostingInfo": {"jobDescription": "first body", "startDate": "2026-01-01"}}),
        _resp(200, {"jobPostingInfo": {"jobDescription": "second body", "startDate": "2026-02-02"}}),
    ]
    result = fetch_workday_board(
        company="Dup",
        tenant="acme",
        wd_server="wd1",
        site="External",
        transport=transport,
        sleep=_noop_sleep,
    )
    assert isinstance(result, AtsBoardCaptureSuccess)
    slots = json.loads(result.raw_board_document)["job_detail_documents"]
    assert [s["external_path"] for s in slots] == [path, path]
    assert [
        json.loads(s["response_body"])["jobPostingInfo"]["jobDescription"] for s in slots
    ] == ["first body", "second body"]
    assert [p.description for p in result.postings] == ["first body", "second body"]
    assert [p.posted_date for p in result.postings] == ["2026-01-01", "2026-02-02"]


def test_workday_failed_detail_is_explicit_gap_slot():
    # A non-2xx detail is an explicit gap slot (never silently dropped); the posting
    # still projects, falling back to list-level fields with no detail description.
    transport = _FakeTransport()
    transport.post_queue = [
        _resp(200, {"total": 1, "jobPostings": [{"title": "Gapped", "externalPath": "/job/G_1"}]})
    ]
    transport.get_map["/job/G_1"] = _resp(503, {"error": "unavailable"})
    result = fetch_workday_board(
        company="Gap",
        tenant="acme",
        wd_server="wd1",
        site="External",
        transport=transport,
        sleep=_noop_sleep,
    )
    assert isinstance(result, AtsBoardCaptureSuccess)
    (slot,) = json.loads(result.raw_board_document)["job_detail_documents"]
    assert slot["external_path"] == "/job/G_1"
    assert "response_body" not in slot
    assert "gap_reason" in slot
    (posting,) = result.postings
    assert posting.description is None
    assert any("HTTP 503" in note for note in result.limitation_notes)


def test_workday_csrf_retry_does_not_consume_page_budget():
    transport = _FakeTransport()
    board_base = "https://acme.wd1.myworkdayjobs.com/External"
    transport.post_queue = [
        _resp(403, {"error": "csrf required"}),
        _resp(
            200,
            {
                "total": 1,
                "jobPostings": [
                    {"title": "Chemist", "externalPath": "/job/C_1"}
                ],
            },
        ),
    ]
    transport.get_map[board_base] = _resp(
        200,
        b"<html></html>",
        headers={"Set-Cookie": "CALYPSO_CSRF_TOKEN=token-value; Path=/"},
    )
    result = fetch_workday_board(
        company="Acme",
        tenant="acme",
        wd_server="wd1",
        site="External",
        transport=transport,
        sleep=_noop_sleep,
        max_pages=1,
        fetch_details=False,
    )
    assert isinstance(result, AtsBoardCaptureSuccess)
    assert [posting.ats_job_id for posting in result.postings] == ["/job/C_1"]
    assert not any("max_pages" in note for note in result.limitation_notes)


# --- failure kinds -----------------------------------------------------------


def test_transport_error_maps_to_typed_failure():
    transport = _FakeTransport()
    transport.get_map[ashby_board_url("acme")] = AtsTransportError(
        "boom", failure_kind=AtsCaptureFailureKind.NETWORK_ERROR
    )
    result = fetch_ashby_board(company="Acme", job_board_name="acme", transport=transport)
    assert isinstance(result, AtsBoardCaptureFailure)
    assert result.failure_kind is AtsCaptureFailureKind.NETWORK_ERROR


def test_http_404_is_access_failed_and_429_is_rate_limited():
    transport = _FakeTransport()
    transport.get_map[greenhouse_board_url("missing")] = _resp(404, {"error": "no board"})
    result = fetch_greenhouse_board(company="X", board_token="missing", transport=transport)
    assert isinstance(result, AtsBoardCaptureFailure)
    assert result.failure_kind is AtsCaptureFailureKind.ACCESS_FAILED
    assert result.http_status == 404

    transport2 = _FakeTransport()
    transport2.get_map[greenhouse_board_url("busy")] = _resp(429, {"error": "slow down"})
    result2 = fetch_greenhouse_board(company="X", board_token="busy", transport=transport2)
    assert isinstance(result2, AtsBoardCaptureFailure)
    assert result2.failure_kind is AtsCaptureFailureKind.RATE_LIMITED


def test_malformed_json_is_typed_failure():
    transport = _FakeTransport()
    transport.get_map[ashby_board_url("acme")] = _resp(200, b"this is not json")
    result = fetch_ashby_board(company="X", job_board_name="acme", transport=transport)
    assert isinstance(result, AtsBoardCaptureFailure)
    assert result.failure_kind is AtsCaptureFailureKind.MALFORMED_RESPONSE


@pytest.mark.parametrize(
    ("vendor", "payload"),
    [
        (AtsVendor.GREENHOUSE, {"jobs": [{"title": "Missing id"}]}),
        (AtsVendor.LEVER, [{"text": "Missing id"}]),
        (AtsVendor.ASHBY, {"jobs": [{"title": "Missing id"}]}),
    ],
)
def test_missing_vendor_job_id_is_typed_malformed_failure(vendor, payload):
    transport = _FakeTransport()
    if vendor is AtsVendor.GREENHOUSE:
        transport.get_map[greenhouse_board_url("acme")] = _resp(200, payload)
        result = fetch_greenhouse_board(
            company="Acme", board_token="acme", transport=transport
        )
    elif vendor is AtsVendor.LEVER:
        transport.get_map[lever_board_url("acme")] = _resp(200, payload)
        result = fetch_lever_board(
            company="Acme", board_token="acme", transport=transport
        )
    else:
        transport.get_map[ashby_board_url("acme")] = _resp(200, payload)
        result = fetch_ashby_board(
            company="Acme", job_board_name="acme", transport=transport
        )
    assert isinstance(result, AtsBoardCaptureFailure)
    assert result.failure_kind is AtsCaptureFailureKind.MALFORMED_RESPONSE


def test_workday_missing_external_path_is_typed_malformed_failure():
    transport = _FakeTransport()
    transport.post_queue = [
        _resp(200, {"total": 1, "jobPostings": [{"title": "Missing path"}]})
    ]
    result = fetch_workday_board(
        company="Acme",
        tenant="acme",
        wd_server="wd1",
        site="External",
        transport=transport,
        sleep=_noop_sleep,
    )
    assert isinstance(result, AtsBoardCaptureFailure)
    assert result.failure_kind is AtsCaptureFailureKind.MALFORMED_RESPONSE


def test_empty_board_is_success_with_limitation_note():
    transport = _FakeTransport()
    transport.get_map[greenhouse_board_url("empty")] = _resp(200, {"jobs": []})
    result = fetch_greenhouse_board(company="X", board_token="empty", transport=transport)
    assert isinstance(result, AtsBoardCaptureSuccess)
    assert result.postings == ()
    assert any("zero postings" in note for note in result.limitation_notes)


# --- no secrets: Workday CSRF token never enters the preserved raw ----------


def test_workday_csrf_token_never_leaks_into_raw_document():
    secret = "SUPER_SECRET_CSRF_9f2a"
    transport = _FakeTransport()
    board_base = "https://acme.wd1.myworkdayjobs.com/External"
    # First list POST 403 (no token) -> csrf GET -> retry POST 200.
    transport.post_queue = [
        _resp(403, {"error": "csrf required"}),
        _resp(200, {"total": 1, "jobPostings": [{"title": "Chemist", "externalPath": "/job/C_1"}]}),
    ]
    transport.get_map[board_base] = _resp(
        200, b"<html></html>", headers={"Set-Cookie": f"CALYPSO_CSRF_TOKEN={secret}; Path=/"}
    )
    transport.get_map["/job/C_1"] = _resp(200, {"jobPostingInfo": {"jobDescription": "desc"}})
    result = fetch_workday_board(
        company="Acme",
        tenant="acme",
        wd_server="wd1",
        site="External",
        transport=transport,
        sleep=_noop_sleep,
    )
    assert isinstance(result, AtsBoardCaptureSuccess)
    # The token WAS sent as a request header on the retry...
    retry_headers = [h for (m, u, h, b) in transport.calls if m == "POST"][1]
    assert retry_headers.get("X-Calypso-Csrf-Token") == secret
    # ...but never appears in the preserved raw document or any result field.
    assert secret.encode() not in result.raw_board_document
    assert secret not in json.dumps(result.warning_notes + result.limitation_notes)


# --- runner -> packet -> projection end-to-end (no network) -----------------


def _ashby_args(tmp_path: Path) -> argparse.Namespace:
    return argparse.Namespace(
        vendor="ashby",
        company="Acme Beauty",
        decision_question="Which roles is Acme Beauty hiring for as of today?",
        board_token=None,
        job_board_name="acme",
        tenant=None,
        wd_server=None,
        site=None,
        output=tmp_path / "packet",
        data_root=None,
        session_id="test-session",
        timeout_seconds=25.0,
        max_bytes=25_000_000,
        delay_seconds=0.0,
    )


def test_runner_writes_packet_and_projection_yields_rows(tmp_path: Path):
    transport = _FakeTransport()
    transport.get_map[ashby_board_url("acme")] = _resp(
        200,
        {
            "jobs": [
                {
                    "id": "j1",
                    "title": "Brand Manager",
                    "location": "New York, NY",
                    "descriptionPlain": "Own brand",
                    "publishedAt": "2026-06-01T00:00:00Z",
                    "jobUrl": "https://jobs.ashbyhq.com/acme/j1",
                    "isListed": True,
                    "address": {"postalAddress": {"addressCountry": "USA"}},
                },
                {
                    "id": "j2",
                    "title": "Fragrance Evaluator",
                    "location": "Remote - US",
                    "descriptionPlain": "Evaluate scents",
                    "publishedAt": "2026-06-02T00:00:00Z",
                    "jobUrl": "https://jobs.ashbyhq.com/acme/j2",
                    "isListed": True,
                    "address": {"postalAddress": {"addressCountry": "USA"}},
                },
            ]
        },
    )
    args = _ashby_args(tmp_path)
    exit_code, output_dir = run_source_capture_ats_job_posting_packet(
        vendor=AtsVendor.ASHBY,
        company=args.company,
        decision_question=args.decision_question,
        args=args,
        output_directory=args.output,
        transport=transport,
    )
    assert exit_code == 0
    packet_dir = Path(output_dir)
    assert (packet_dir / "manifest.json").is_file()

    projection = build_ats_job_posting_projection_from_packet_directory(
        packet_or_manifest_path=packet_dir
    )
    assert projection.ats_vendor == "ashby"
    assert projection.company == "Acme Beauty"
    assert len(projection.rows) == 2
    assert projection.loss_ledger.preserved_posting_rows == 2
    first = projection.rows[0]
    assert first.ats_job_id == "j1"
    assert first.location_country == "USA"
    assert first.title == "Brand Manager"
    assert first.captured_at  # populated from capture metadata
    assert projection.rows[0].raw_ref.slice_id == "slice_0001"
    assert projection.rows[1].raw_ref.slice_id == "slice_0002"
    # fixed row schema => no free field dict => nowhere for a Judgment field to land
    assert not hasattr(first, "source_visible_fields")

    manifest = json.loads((packet_dir / "manifest.json").read_text(encoding="utf-8"))
    assert [
        source_slice["timing"]["source_publication_or_event"]["value"]
        for source_slice in manifest["source_slices"]
    ] == ["2026-06-01T00:00:00Z", "2026-06-02T00:00:00Z"]


def test_projection_rejects_posting_slice_count_mismatch(tmp_path: Path):
    transport = _FakeTransport()
    transport.get_map[ashby_board_url("acme")] = _resp(
        200,
        {
            "jobs": [
                {"id": "j1", "title": "One", "jobUrl": "https://x/j1"},
                {"id": "j2", "title": "Two", "jobUrl": "https://x/j2"},
            ]
        },
    )
    args = _ashby_args(tmp_path)
    exit_code, output_dir = run_source_capture_ats_job_posting_packet(
        vendor=AtsVendor.ASHBY,
        company=args.company,
        decision_question=args.decision_question,
        args=args,
        output_directory=args.output,
        transport=transport,
    )
    assert exit_code == 0
    packet_dir = Path(output_dir)
    manifest_path = packet_dir / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["source_slices"] = manifest["source_slices"][:1]
    manifest_path.write_text(json.dumps(manifest), encoding="utf-8")

    with pytest.raises(
        ValueError,
        match="exactly one raw-referencing source slice per posting",
    ):
        build_ats_job_posting_projection_from_packet_directory(
            packet_or_manifest_path=packet_dir
        )


def test_workday_csrf_token_never_enters_packet_files(tmp_path: Path):
    secret = "SUPER_SECRET_CSRF_PACKET_7d1a"
    transport = _FakeTransport()
    board_base = "https://acme.wd1.myworkdayjobs.com/External"
    transport.post_queue = [
        _resp(403, {"error": "csrf required"}),
        _resp(
            200,
            {
                "total": 1,
                "jobPostings": [
                    {"title": "Chemist", "externalPath": "/job/C_1"}
                ],
            },
        ),
    ]
    transport.get_map[board_base] = _resp(
        200,
        b"<html></html>",
        headers={"Set-Cookie": f"CALYPSO_CSRF_TOKEN={secret}; Path=/"},
    )
    transport.get_map["/job/C_1"] = _resp(
        200, {"jobPostingInfo": {"jobDescription": "desc"}}
    )
    args = _ashby_args(tmp_path)
    args.tenant = "acme"
    args.wd_server = "wd1"
    args.site = "External"
    exit_code, output_dir = run_source_capture_ats_job_posting_packet(
        vendor=AtsVendor.WORKDAY,
        company=args.company,
        decision_question=args.decision_question,
        args=args,
        output_directory=args.output,
        transport=transport,
    )
    assert exit_code == 0
    for path in Path(output_dir).rglob("*"):
        if path.is_file():
            assert secret.encode() not in path.read_bytes(), path


def test_runner_empty_board_still_writes_one_slice(tmp_path: Path):
    transport = _FakeTransport()
    transport.get_map[ashby_board_url("acme")] = _resp(200, {"jobs": []})
    args = _ashby_args(tmp_path)
    exit_code, output_dir = run_source_capture_ats_job_posting_packet(
        vendor=AtsVendor.ASHBY,
        company=args.company,
        decision_question=args.decision_question,
        args=args,
        output_directory=args.output,
        transport=transport,
    )
    assert exit_code == 0
    projection = build_ats_job_posting_projection_from_packet_directory(
        packet_or_manifest_path=Path(output_dir)
    )
    assert projection.rows == []
    assert "ats_board_zero_postings" in projection.residuals
