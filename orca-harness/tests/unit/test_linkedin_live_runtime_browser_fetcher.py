"""Tests for the LinkedIn live BrowserFetcher + page extractor (slice 3c-2b).

The extractor (rendered DOM -> minimized CompanySignal) and the BrowserFetcher
composition (drive -> extract -> assemble bag -> [runtime] minimize / validate /
project) are exercised entirely offline with a SYNTHETIC company-page fixture (REAL
LinkedIn org-top-card structure, FAKE data) and a fake driver. The real
CdpAttachBrowserDriver -- the only part that attaches to a live logged-in browser --
is owner-validated on the attended run, not unit-tested here; its offline
fail-closed guards (bad endpoint / bad target) ARE.

Fake-success guard: the wiring test asserts the minted row passes
validate_candidate_row AND that the planted social-proof connection name is absent
from both the bag and the row -- the person / network data the lane forbids.
"""
from __future__ import annotations

import json

import pytest

from capture_spine.linkedin_lane.models import (
    CandidateClass,
    MethodMode,
    MinimizationRule,
    RunEnvelope,
    SourceSurface,
    StopReason,
)
from capture_spine.linkedin_lane.validation import validate_candidate_row
from capture_spine.linkedin_live_adapter import LiveAccessEnvelope, LiveAccessMode
from capture_spine.linkedin_live_runtime import (
    BrowserFetcher,
    CaptureTarget,
    CompanySignal,
    Fetcher,
    LinkedInLaneError,
    extract_company_signal,
    run_live_capture,
)
from capture_spine.linkedin_live_runtime.browser_driver import CdpAttachBrowserDriver


_LIVE_ACCESS_ID = "live-3c2b-0001"
_RUN_ID = "linkedin_lane_company_pilot_001"
_TARGET = "https://www.linkedin.com/company/acme-capital-partners/"
_FAKE_PERSON_NAME = "Jordan Fakename"

# SYNTHETIC fixture: the REAL LinkedIn company top-card structure (org-top-card),
# FAKE data ("Acme Capital Partners"). It plants a connection name in the
# secondary-content / social-proof region to prove the extractor never captures it.
# This is committed; the owner's real captured HTML is NOT.
_SYNTHETIC_COMPANY_PAGE = """\
<body class="ember-application nav-v2">
  <div class="org-top-card__primary-content org-top-card-primary-content--zero-height-logo">
    <div class="org-top-card-primary-content__logo-container">
      <img alt="Acme Capital Partners logo" class="org-top-card-primary-content__logo">
    </div>
    <div class="block mt4">
      <div>
        <h1 id="ember37" class="ember-view org-top-card-summary__title
            ZxQabc123 full-width inline" title="Acme Capital Partners">
          Acme Capital Partners
        </h1>
        <a id="ember38" class="ember-view" aria-label="Verified" href="/company/acme/about/"></a>
        <div class="org-top-card-summary-info-list">
          <div class="org-top-card-summary-info-list__info-item">
            Financial Services
          </div>
          <div class="inline-block">
            <div class="org-top-card-summary-info-list__info-item">
              Springfield, USA
            </div>
            <div class="org-top-card-summary-info-list__info-item">
              2M  followers
            </div>
            <a href="/search/results/people/?currentCompany=%5B%229999%22%5D"
               class="ember-view org-top-card-summary-info-list__info-item org-top-card-summary-info-list__info-item-link">
              <span class="t-normal t-black--light">1K-5K employees</span>
            </a>
          </div>
        </div>
      </div>
    </div>
  </div>
  <div class="org-top-card-secondary-content__insights">
    <div class="org-top-card-secondary-content__social-proof flex-column">
      <a class="org-top-card-secondary-content__insight" href="/company/acme/?showInNetworkFollowers=true">
        <img width="24" alt="Jordan Fakename" class="evi-image lazy-image">
        <h2 class="t-black text-body-small-bold">
          Jordan Fakename &amp; 2 other connections follow this page
        </h2>
      </a>
    </div>
  </div>
</body>
"""


class _FakeDriver:
    """Offline BrowserDriver: returns canned HTML per target; raises for unknown."""

    def __init__(self, dom_by_target: dict[str, str]) -> None:
        self._dom = dict(dom_by_target)

    def rendered_dom(self, target: str) -> str:
        if target not in self._dom:
            raise KeyError(target)
        return self._dom[target]


def _access_envelope(**overrides) -> LiveAccessEnvelope:
    fields = dict(
        live_access_id=_LIVE_ACCESS_ID,
        run_id=_RUN_ID,
        live_access_mode=LiveAccessMode.OWNER_PRESENT_ATTENDED_AUTOMATION,
        source_policy_posture="discoverable_or_entitled_disclosable",
        stop_condition="caps_reached",
        owner_presence_attested=True,
        attended_presence_check_method="owner present and supervising the attended browser session",
        caps={"max_company_pages": 10},
        optional_poc_risk_mode=True,
    )
    fields.update(overrides)
    return LiveAccessEnvelope(**fields)


def _run_envelope(**overrides) -> RunEnvelope:
    fields = dict(
        run_id=_RUN_ID,
        declared_theme_or_decision_context="competitor positioning and scale in our segment",
        run_purpose="map competitor company profiles for a planning review",
        candidate_classes=(CandidateClass.BUSINESS,),
        source_surface_allowlist=(SourceSurface.LINKEDIN_COMPANY_PAGE_OR_POST,),
        method_mode=MethodMode.OWNER_PRESENT_ATTENDED_AUTOMATION_OPTIONAL_POC_RISK,
        stop_condition=StopReason.CAPS_REACHED,
        source_policy_posture="discoverable_or_entitled_disclosable",
        minimization_rule=MinimizationRule.BUSINESS_ENTITY_ONLY,
        promotion_owner="eric",
        max_businesses=25,
        max_organizations=5,
        max_people=10,
        max_source_surfaces=5,
        time_window_days=30,
    )
    fields.update(overrides)
    return RunEnvelope(**fields)


def _browser_fetcher(dom: str | None = None, **overrides) -> BrowserFetcher:
    driver = _FakeDriver({_TARGET: dom if dom is not None else _SYNTHETIC_COMPANY_PAGE})
    kwargs = dict(
        driver=driver,
        live_access_id=_LIVE_ACCESS_ID,
        run_id=_RUN_ID,
        observed_source_surface=SourceSurface.LINKEDIN_COMPANY_PAGE_OR_POST.value,
    )
    kwargs.update(overrides)
    return BrowserFetcher(**kwargs)


# --- extractor: minimized signal, fail-closed, person-data exclusion ---

def test_extract_pulls_company_name_and_follower_band() -> None:
    sig = extract_company_signal(_SYNTHETIC_COMPANY_PAGE)
    assert sig is not None
    assert sig.display_name == "Acme Capital Partners"
    assert sig.visible_follower_count_or_none == "2M"


def test_extract_excludes_social_proof_person_data() -> None:
    sig = extract_company_signal(_SYNTHETIC_COMPANY_PAGE)
    assert sig is not None
    # the planted connection name (secondary-content / social-proof) is never captured
    assert _FAKE_PERSON_NAME not in sig.display_name
    assert _FAKE_PERSON_NAME not in (sig.visible_follower_count_or_none or "")


def test_extract_fail_closed_on_unrecognized_page() -> None:
    assert extract_company_signal("<body><div class='feed'>no company top-card</div></body>") is None
    assert extract_company_signal("") is None
    assert extract_company_signal("   ") is None


@pytest.mark.parametrize(
    "follower_text, expected",
    [
        ("2M  followers", "2M"),
        ("1,753,723 followers", "1,753,723"),
        ("10K followers", "10K"),
        ("523 followers", "523"),
        ("Financial Services", None),  # a recognized info-item that is not a follower count
    ],
)
def test_follower_band_normalization(follower_text: str, expected: str | None) -> None:
    item = (
        f'<div class="org-top-card-summary-info-list__info-item">{follower_text}</div>'
        if follower_text
        else ""
    )
    dom = (
        '<div class="org-top-card__primary-content">'
        '<h1 class="org-top-card-summary__title">Acme</h1>'
        f'<div class="org-top-card-summary-info-list">{item}</div>'
        "</div>"
    )
    sig = extract_company_signal(dom)
    assert sig is not None
    assert sig.visible_follower_count_or_none == expected


# --- BrowserFetcher: clean bag, wiring, fail-closed, Fetcher protocol ---

def test_browser_fetcher_is_a_fetcher() -> None:
    assert isinstance(_browser_fetcher(), Fetcher)


def test_browser_fetcher_assembles_clean_minimized_bag() -> None:
    bag = _browser_fetcher().fetch(_TARGET)
    assert bag["observed_display_name"] == "Acme Capital Partners"
    assert bag["observed_source_surface"] == "linkedin_company_page_or_post"
    assert bag["observed_source_locator"] == _TARGET
    assert bag["observed_entity_type"] == "business_entity"
    assert bag["visible_follower_count_or_none"] == "2M"
    assert bag["live_access_id"] == _LIVE_ACCESS_ID
    assert bag["run_id"] == _RUN_ID
    # the raw DOM + any person / network data never enter the bag
    serialized = json.dumps(bag)
    assert _FAKE_PERSON_NAME not in serialized
    assert "<" not in serialized  # no raw HTML smuggled into a field
    for forbidden_key in ("rendered_dom", "html", "dom", "screenshot", "profile_body"):
        assert forbidden_key not in bag


def test_browser_fetcher_wires_through_run_live_capture() -> None:
    rows = run_live_capture(
        access_envelope=_access_envelope(),
        run_envelope=_run_envelope(),
        targets=[
            CaptureTarget(
                locator=_TARGET,
                candidate_class=CandidateClass.BUSINESS,
                business_relevance_note="a directly competing firm in our segment",
            )
        ],
        fetcher=_browser_fetcher(),
        live_run_authorized=True,
        owner_present_confirmed=True,
        max_captures=5,
    )
    assert len(rows) == 1
    row = rows[0]
    validate_candidate_row(row)  # the minted row is a valid candidate row
    assert row["display_name"] == "Acme Capital Partners"
    assert row["run_id"] == _RUN_ID
    # the planted social-proof / person data never reaches the candidate row
    assert _FAKE_PERSON_NAME not in json.dumps(row)


def test_browser_fetcher_fail_closed_on_unrecognized_page() -> None:
    fetcher = _browser_fetcher(dom="<body><div class='feed'>not a company page</div></body>")
    with pytest.raises(LinkedInLaneError) as exc:
        fetcher.fetch(_TARGET)
    assert exc.value.code == "unrecognized_capture_page"


# --- CdpAttachBrowserDriver: offline fail-closed guards (live path owner-validated) ---

def test_cdp_driver_rejects_empty_endpoint() -> None:
    with pytest.raises(LinkedInLaneError) as exc:
        CdpAttachBrowserDriver(cdp_endpoint="")
    assert exc.value.code == "invalid_cdp_endpoint"


def test_cdp_driver_rejects_non_http_target() -> None:
    driver = CdpAttachBrowserDriver(cdp_endpoint="http://localhost:9222")
    # target is validated before any Playwright import, so this is deterministic offline
    with pytest.raises(LinkedInLaneError) as exc:
        driver.rendered_dom("file:///etc/passwd")
    assert exc.value.code == "invalid_capture_target"


# --- cross-vendor review hardening: F1 (blocked-region), F2 (fail-closed), F3, F4 ---

def test_blocked_region_tag_stack_survives_malformed_end_tags() -> None:
    # review F1: unmatched end tags inside the social-proof region must NOT prematurely
    # exit suppression; an info-item planted inside it must never be captured.
    from capture_spine.linkedin_live_runtime.extractor import _CompanyTopCardParser

    parser = _CompanyTopCardParser()
    parser.feed(
        '<div class="org-top-card-secondary-content__social-proof">'
        "<p>x</p></p></span>"  # stray unmatched end tags (depth-only counter would zero out)
        '<div class="org-top-card-summary-info-list__info-item">LEAK Person Name</div>'
        "</div>"
    )
    assert parser.info_items == []  # planted item stayed inside the blocked region


def test_extract_fail_closed_on_title_without_info_list() -> None:
    # review F2: a lone title class with no summary info-list is not a recognized top-card
    dom = (
        '<div class="org-top-card__primary-content">'
        '<h1 class="org-top-card-summary__title">Acme</h1>'
        "</div>"
    )
    assert extract_company_signal(dom) is None


def test_extract_fail_closed_on_ambiguous_duplicate_title() -> None:
    # review F2: more than one top-card title -> ambiguous page -> capture nothing
    dom = (
        '<div class="org-top-card__primary-content">'
        '<h1 class="org-top-card-summary__title">Acme</h1>'
        '<div class="org-top-card-summary-info-list">'
        '<div class="org-top-card-summary-info-list__info-item">2M followers</div></div>'
        '<h1 class="org-top-card-summary__title">Acme Imposter</h1>'
        "</div>"
    )
    assert extract_company_signal(dom) is None


@pytest.mark.parametrize(
    "endpoint",
    [
        "http://user:pass@localhost:9222",  # embedded credentials
        "http://10.0.0.5:9222",             # remote (non-local) endpoint
        "ftp://localhost:9222",             # unsupported scheme
        "not-a-url",                        # no scheme/netloc
    ],
)
def test_cdp_driver_rejects_unclean_endpoint(endpoint: str) -> None:
    # review F3: the CDP endpoint must be a local, credential-free CDP URL
    with pytest.raises(LinkedInLaneError) as exc:
        CdpAttachBrowserDriver(cdp_endpoint=endpoint)
    assert exc.value.code == "invalid_cdp_endpoint"


def test_cdp_driver_accepts_local_endpoint() -> None:
    # a clean local endpoint constructs without error (live path still owner-validated)
    CdpAttachBrowserDriver(cdp_endpoint="http://127.0.0.1:9222")
    CdpAttachBrowserDriver(cdp_endpoint="ws://localhost:9222/devtools/browser/abc")


def test_browser_fetcher_rejects_credentialed_target() -> None:
    # review F4: the fetcher self-validates the locator so a credentialed URL never
    # enters the bag, regardless of the injected driver
    fetcher = _browser_fetcher()
    with pytest.raises(LinkedInLaneError) as exc:
        fetcher.fetch("https://user:pass@www.linkedin.com/company/acme/")
    assert exc.value.code == "invalid_capture_target"
