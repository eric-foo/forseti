"""Shared validation primitives for the LinkedIn discovery lane.

Single source of truth for the generic, slice-agnostic fail-closed helpers every
LinkedIn capture_spine slice uses (candidate intake, graph frontier, live
adapter, ...): the forbidden-output-field walk + secret-value scan, the
fail-closed key allowlist, the required-field check, the NEGATED non_claims
category check, and the excluded public-actor-basis markers.

Slice-specific validators import these and apply them; they no longer
re-implement them. Re-implementation had already drifted into inconsistent
enforcement -- slice-1's non_claims check was the weaker substring form (a
positive "live LinkedIn access" satisfied "live"), and the excluded-basis marker
lists had diverged (slice-2 carried "routine employer"; slice-1 did not). This
module reconciles to the STRONGER / SUPERSET behavior.

Generic + parameterized: callers pass their own allowed-key sets and (optionally)
required categories. Imports only ``LinkedInLaneError`` -- no slice records -- so
any slice's validation module can import it without a cycle (same import
direction the forbidden-walk already used).
"""
from __future__ import annotations

import re
from collections.abc import Mapping, Sequence
from typing import Any

from capture_spine.linkedin_lane.models import LinkedInLaneError


def fail(code: str, message: str) -> None:
    raise LinkedInLaneError(code, message)


def is_list(value: Any) -> bool:
    return isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray))


# --- Forbidden OUTPUT field names (exact, case-insensitive key match) + secret-
# value scan. Precision is load-bearing: follower/connection/commenter *lists and
# graphs* are forbidden, but the visible-influence *_count_or_none / *_band_or_none
# fields are allowed -- exact key matching keeps `follower_count_or_none` out of
# this set, and the per-validator key allowlist (reject_unknown_keys) closes
# aliasing.
FORBIDDEN_OUTPUT_FIELDS = {
    # contact acquisition
    "email", "emails", "email_address", "email_or_none",
    "phone", "phone_number", "phone_numbers", "phone_or_none", "phone_number_or_none",
    "contact", "contacts", "contact_info", "contact_details",
    "contact_route", "contact_routes", "private_contact_route", "private_contact_routes",
    "contact_graph", "enrichment", "enrichment_output",
    # follower / connection / commenter LISTS + GRAPHS (not counts)
    "followers", "follower_list", "follower_lists", "follower_graph",
    "connections", "connection_list", "connection_lists", "connection_graph",
    "commenters", "commenter_list", "commenter_lists", "commenter_graph",
    "network_graph", "relationship_graph", "relationship_list", "relationship_lists",
    # employment / org-chart graphs
    "employment_history", "employment_graph", "employment_history_graph",
    "org_chart", "org_charts", "org_chart_graph", "full_org_chart", "full_org_chart_graph",
    # lead lists
    "lead", "leads", "lead_list", "lead_lists", "lead_emails", "lead_contacts",
    # profile body / post content
    "profile_body", "profile_html", "profile_text", "about_section", "headline_text",
    "post_content", "post_text", "posts", "content",
    # raw capture / secrets
    "raw_html", "html", "rendered_dom", "dom", "parser_output",
    "screenshot", "screenshot_path",
    "cookie", "cookies", "session", "session_state", "hidden_session_state",
    "authorization_header",
    # downstream-stage leakage
    "source_capture_packet", "packet_manifest", "ecr", "cleaning", "judgment",
    "source_quality_score",
}


# Defense-in-depth on secret VALUES that could land in a legitimately named field.
# Each pattern anchors on an unambiguous credential marker, not entropy, so it does
# not false-positive on candidate vocabulary. Favors false negatives.
_FORBIDDEN_OUTPUT_VALUE_PATTERNS: tuple[tuple[str, re.Pattern[str]], ...] = (
    ("pem_private_key", re.compile(r"-----BEGIN [A-Z0-9 ]*PRIVATE KEY-----")),
    ("bearer_token", re.compile(r"\bBearer\s+[A-Za-z0-9._~+/=\-]{16,}")),
    ("credentialed_url_userinfo", re.compile(r"://[^/\s:@]+:[^/\s:@]+@")),
    ("set_cookie_header", re.compile(r"(?i)\bset-cookie:\s*[^=\s;]+=[^=\s;]+")),
)


def assert_no_forbidden_output_fields(value: Any, *, path: str = "$") -> None:
    if isinstance(value, Mapping):
        for key, child in value.items():
            lowered = str(key).lower()
            if lowered in FORBIDDEN_OUTPUT_FIELDS:
                fail("forbidden_output_field", f"forbidden output field at {path}.{key}")
            assert_no_forbidden_output_fields(child, path=f"{path}.{key}")
        return
    if isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray)):
        for index, child in enumerate(value):
            assert_no_forbidden_output_fields(child, path=f"{path}[{index}]")
        return
    if isinstance(value, str):
        _assert_no_forbidden_output_value(value, path=path)


def _assert_no_forbidden_output_value(value: str, *, path: str) -> None:
    for marker, pattern in _FORBIDDEN_OUTPUT_VALUE_PATTERNS:
        if pattern.search(value):
            fail("forbidden_output_value", f"forbidden secret-like value ({marker}) at {path}")


# --- visible influence values: minimized counts / coarse bands only ---
# The visible-influence ``*_count_or_none`` / ``*_band_or_none`` fields pass the
# forbidden-key walk (they are counts, not lists) and the secret-value scan only
# catches credentials, not narrative prose -- so nothing else stops a copied
# profile/body from landing in a field documented "counts / coarse bands only".
# Any slice that mints or accepts such a field enforces the count/band shape here
# (cross-vendor review F1). Fail-closed: a non-count/band value raises.
_MAX_VISIBLE_INFLUENCE_VALUE_LEN = 64
_VISIBLE_INFLUENCE_VALUE_RE = re.compile(
    r"^(?:"
    r"(?:\d{1,3}(?:,\d{3})+|\d+)(?:\.\d+)?[kKmM]?\+?"
    r"|(?:under|over|less than|more than) \d+(?:,\d{3})*[kKmM]?\+?"
    r"|(?:\d{1,3}(?:,\d{3})+|\d+)[kKmM]?\s*(?:-|to|–)\s*"
    r"(?:\d{1,3}(?:,\d{3})+|\d+)[kKmM]?"
    r")$"
)


def validate_visible_influence_value(field_name: str, value: Any) -> None:
    """Require a minimized count / coarse-band value (or None) -- never free text."""
    if value is None:
        return
    if not isinstance(value, str) or not value.strip():
        fail(
            "invalid_visible_influence_number",
            f"{field_name} must be a minimized count / coarse band string when present",
        )
    stripped = value.strip()
    if len(stripped) > _MAX_VISIBLE_INFLUENCE_VALUE_LEN:
        fail(
            "oversized_visible_influence_number",
            f"{field_name} exceeds the minimized count / coarse band length cap",
        )
    if not _VISIBLE_INFLUENCE_VALUE_RE.fullmatch(stripped):
        fail(
            "invalid_visible_influence_number",
            f"{field_name} must be a minimized count / coarse band, not free text",
        )


# --- key allowlist + required fields ---
def reject_unknown_keys(value_map: Mapping[str, Any], allowed_keys: frozenset[str], label: str) -> None:
    unknown = sorted(str(key) for key in value_map if str(key) not in allowed_keys)
    if unknown:
        fail("unknown_field", f"{label} contains unknown field(s): {unknown}")


def require_fields(value_map: Mapping[str, Any], field_names: Sequence[str], label: str) -> None:
    for field_name in field_names:
        value = value_map.get(field_name)
        if value is None or (isinstance(value, str) and not value.strip()):
            fail(f"missing_{field_name}", f"{label} missing required field: {field_name}")


# --- non_claims: NEGATED category check ---
# non_claims must DISCLAIM (negate) each hard-stop category -- a positive inverse
# claim like "live LinkedIn access" must NOT satisfy "live", and an expansive
# reversal ("not ONLY live access; it also authorizes it") must not either.
DEFAULT_REQUIRED_NON_CLAIM_CATEGORIES: tuple[str, ...] = (
    "live",
    "promotion",
    "source capture packet",
    "data capture",
    "outreach",
)

# A claim disclaims a category only if it LEADS with a negation ("not "/"no ")
# and is not an expansive reversal ("not ONLY X" / "not merely X" / "not just X"
# = "X and more"). Detecting the reversal by its LEADING construction -- not by a
# marker substring anywhere -- avoids false-positives on benign compound
# disclaimers like "not live access; only planning metadata" (cross-vendor F3).
# Lexical negation is still not fully robust (a mid-clause "not X but Y" inversion
# can evade); a canonical accepted-disclaimer allowlist would be the fully-robust
# form -- deferred. non_claims is the lane's weakest-stakes field (a declared
# posture, not an execution gate).
_REVERSAL_PREFIXES: tuple[str, ...] = ("not only ", "not merely ", "not just ", "no mere ")


def is_negated(claim: str) -> bool:
    if not (claim.startswith("not ") or claim.startswith("no ")):
        return False
    return not any(claim.startswith(prefix) for prefix in _REVERSAL_PREFIXES)


def validate_non_claims_categories(
    value: Any,
    label: str,
    required_categories: Sequence[str] = DEFAULT_REQUIRED_NON_CLAIM_CATEGORIES,
) -> None:
    if not is_list(value):
        fail("missing_non_claims", f"{label} requires non_claims")
    claims = [str(item).strip().lower() for item in value]
    missing = [
        category
        for category in required_categories
        if not any(category in claim and is_negated(claim) for claim in claims)
    ]
    if missing:
        fail(
            "incomplete_non_claims",
            f"{label} non_claims must DISCLAIM (negate) the required hard-stop categories; missing: {missing}",
        )


# --- excluded public-actor basis ---
# A person qualifies only on a concrete public-actor basis that stands OUTSIDE the
# employer org chart. These markers name bases the architecture disqualifies
# outright (the SUPERSET of the slice-1/slice-2 lists, incl. "routine employer").
EXCLUDED_PERSON_BASIS_MARKERS: tuple[str, ...] = (
    "org chart", "org-chart", "orgchart", "organization chart", "organisation chart",
    "reporting line", "reports to", "mentioned by", "tagged by", "mention/tag",
    "routine post", "routine employer", "routine work update", "routine update",
    "commenter", "follower", "connection",
)


def validate_public_actor_basis(basis: Any, label: str) -> None:
    """Require a concrete, non-empty, org-chart-independent public-actor basis."""
    if not isinstance(basis, str) or not basis.strip():
        fail(
            "missing_public_actor_basis",
            f"{label} requires a concrete org-chart-independent public-actor / senior-role basis",
        )
    lowered = basis.lower()
    for marker in EXCLUDED_PERSON_BASIS_MARKERS:
        if marker in lowered:
            fail(
                "excluded_public_actor_basis",
                f"{label} basis must stand outside the employer org chart and must not be a mention/tag, "
                f"routine post, commenter, follower, or connection (matched excluded basis: {marker!r})",
            )
