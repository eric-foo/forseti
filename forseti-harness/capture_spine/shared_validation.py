"""Shared fail-closed validation primitives for capture_spine lanes.

Single home for the recursive forbidden-output-field walk + secret-value scan
(and the byte-equivalent key-allowlist / required-field helpers) that four
lanes had re-implemented: ``linkedin_lane.shared_validation``,
``creator_public_handle_linkage.validation``,
``reddit_candidate_intake.validation``, and
``tiktok_creator_discovery_frontier.validation``.

Lane semantics stay lane-owned and are passed in, never merged:

- ``forbidden_fields``: each lane's deliberately different forbidden-field set
  stays a per-lane constant in the lane module (the sets differ by design --
  e.g. Reddit forbids ``selftext``/``author`` body fields, TikTok forbids
  registry-mutation and metric-rollup fields).
- ``value_patterns``: the secret-VALUE pattern tuples also deliberately differ
  (LinkedIn/Reddit scan for ``set_cookie_header``; creator-handle-linkage and
  TikTok scan for ``email_address``/``phone_url`` instead) and stay per-lane.
- ``fail``: each lane passes its own fail callable so the lane error type and
  error codes are unchanged.
- ``value_message_prefix``: preserves each lane's existing failure wording.

Because everything lane-specific is a parameter, sharing the walk cannot
weaken, broaden, or re-word any lane's check. Imports no lane models, so any
lane validation module can import this without a cycle.
"""
from __future__ import annotations

import re
from collections.abc import Mapping, Sequence
from collections.abc import Set as AbstractSet
from typing import Any, Callable

# Raises the owning lane's error type with (code, message); never returns
# normally on failure.
FailFn = Callable[[str, str], None]


def assert_no_forbidden_output_fields(
    value: Any,
    *,
    forbidden_fields: AbstractSet[str],
    value_patterns: Sequence[tuple[str, re.Pattern[str]]],
    fail: FailFn,
    value_message_prefix: str = "forbidden value",
    path: str = "$",
) -> None:
    """Fail-closed recursive scan: forbidden key names (exact, case-insensitive
    match against ``forbidden_fields``) plus a secret-value scan of every string
    leaf against ``value_patterns``."""
    if isinstance(value, Mapping):
        for key, child in value.items():
            key_name = str(key)
            if key_name.lower() in forbidden_fields:
                fail("forbidden_output_field", f"forbidden output field at {path}.{key_name}")
            assert_no_forbidden_output_fields(
                child,
                forbidden_fields=forbidden_fields,
                value_patterns=value_patterns,
                fail=fail,
                value_message_prefix=value_message_prefix,
                path=f"{path}.{key_name}",
            )
        return
    if isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray)):
        for index, child in enumerate(value):
            assert_no_forbidden_output_fields(
                child,
                forbidden_fields=forbidden_fields,
                value_patterns=value_patterns,
                fail=fail,
                value_message_prefix=value_message_prefix,
                path=f"{path}[{index}]",
            )
        return
    if isinstance(value, str):
        for marker, pattern in value_patterns:
            if pattern.search(value):
                fail("forbidden_output_value", f"{value_message_prefix} ({marker}) at {path}")


def reject_unknown_keys(
    value_map: Mapping[str, Any],
    allowed_keys: frozenset[str],
    label: str,
    *,
    fail: FailFn,
) -> None:
    unknown = sorted(str(key) for key in value_map if str(key) not in allowed_keys)
    if unknown:
        fail("unknown_field", f"{label} contains unknown field(s): {unknown}")


def require_fields(
    value_map: Mapping[str, Any],
    field_names: Sequence[str],
    label: str,
    *,
    fail: FailFn,
) -> None:
    """Missing = absent key, explicit None, or blank string.

    Some lanes deliberately use different missing-field semantics (presence-only
    checks, or presence-required-but-None-allowed); those keep local copies
    marked with a ``helper-delta`` comment rather than adopting this one.
    """
    for field_name in field_names:
        value = value_map.get(field_name)
        if value is None or (isinstance(value, str) and not value.strip()):
            fail(f"missing_{field_name}", f"{label} missing required field: {field_name}")
