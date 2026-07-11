from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from typing import Sequence


SOURCE_DETAIL_SUFFICIENCY_EXIT_CODE = 4


@dataclass(frozen=True)
class SourceDetailSufficiencyRequirements:
    require_not_access_blocked: bool = False
    min_visible_text_bytes: int | None = None
    visible_text_contains: tuple[str, ...] = ()
    visible_text_regexes: tuple[str, ...] = ()
    rendered_dom_contains: tuple[str, ...] = ()
    rendered_dom_regexes: tuple[str, ...] = ()

    @property
    def enabled(self) -> bool:
        return (
            self.require_not_access_blocked
            or self.min_visible_text_bytes is not None
            or bool(self.visible_text_contains)
            or bool(self.visible_text_regexes)
            or bool(self.rendered_dom_contains)
            or bool(self.rendered_dom_regexes)
        )


@dataclass(frozen=True)
class SourceDetailSufficiencyResult:
    requirements: SourceDetailSufficiencyRequirements
    failure_reasons: tuple[str, ...]

    @property
    def enabled(self) -> bool:
        return self.requirements.enabled

    @property
    def passed(self) -> bool:
        return not self.failure_reasons


def add_source_detail_sufficiency_arguments(parser: argparse.ArgumentParser) -> None:
    group = parser.add_argument_group(
        "source detail sufficiency",
        (
            "Optional post-capture admission checks. The packet is still preserved, but "
            "the command fails closed if the captured artifacts do not contain the required details."
        ),
    )
    group.add_argument(
        "--require-not-access-blocked",
        action="store_true",
        help="Fail post-capture sufficiency when the rendered snapshot is classified as access-blocked.",
    )
    group.add_argument(
        "--require-min-visible-text-bytes",
        type=int,
        default=None,
        help="Fail post-capture sufficiency unless visible text has at least this many UTF-8 bytes.",
    )
    group.add_argument(
        "--require-visible-text",
        action="append",
        default=[],
        help="Literal visible-text fragment required for post-capture sufficiency. May be repeated.",
    )
    group.add_argument(
        "--require-visible-regex",
        action="append",
        default=[],
        help="Regular expression that must match visible text for post-capture sufficiency. May be repeated.",
    )
    group.add_argument(
        "--require-rendered-dom-text",
        action="append",
        default=[],
        help="Literal rendered-DOM fragment required for post-capture sufficiency. May be repeated.",
    )
    group.add_argument(
        "--require-rendered-dom-regex",
        action="append",
        default=[],
        help="Regular expression that must match rendered DOM for post-capture sufficiency. May be repeated.",
    )


def build_source_detail_sufficiency_requirements(
    args: argparse.Namespace,
) -> SourceDetailSufficiencyRequirements:
    requirements = SourceDetailSufficiencyRequirements(
        require_not_access_blocked=bool(args.require_not_access_blocked),
        min_visible_text_bytes=args.require_min_visible_text_bytes,
        visible_text_contains=tuple(args.require_visible_text or ()),
        visible_text_regexes=tuple(args.require_visible_regex or ()),
        rendered_dom_contains=tuple(args.require_rendered_dom_text or ()),
        rendered_dom_regexes=tuple(args.require_rendered_dom_regex or ()),
    )
    validate_source_detail_sufficiency_requirements(requirements)
    return requirements


def validate_source_detail_sufficiency_requirements(
    requirements: SourceDetailSufficiencyRequirements,
) -> None:
    if requirements.min_visible_text_bytes is not None and requirements.min_visible_text_bytes < 0:
        raise ValueError("--require-min-visible-text-bytes must be non-negative")
    for label, values in (
        ("--require-visible-text", requirements.visible_text_contains),
        ("--require-visible-regex", requirements.visible_text_regexes),
        ("--require-rendered-dom-text", requirements.rendered_dom_contains),
        ("--require-rendered-dom-regex", requirements.rendered_dom_regexes),
    ):
        for value in values:
            if not value:
                raise ValueError(f"{label} must not be blank")
    for label, patterns in (
        ("--require-visible-regex", requirements.visible_text_regexes),
        ("--require-rendered-dom-regex", requirements.rendered_dom_regexes),
    ):
        for pattern in patterns:
            try:
                re.compile(pattern)
            except re.error as exc:
                raise ValueError(f"{label} is not a valid regex: {pattern!r}: {exc}") from exc


def evaluate_source_detail_sufficiency(
    *,
    requirements: SourceDetailSufficiencyRequirements | None,
    access_block_reason: str | None,
    visible_text: str,
    rendered_dom: str,
) -> SourceDetailSufficiencyResult:
    active = requirements or SourceDetailSufficiencyRequirements()
    failure_reasons: list[str] = []

    if active.require_not_access_blocked and access_block_reason is not None:
        failure_reasons.append(f"access blocked: {access_block_reason}")

    if active.min_visible_text_bytes is not None:
        visible_text_bytes = len(visible_text.encode("utf-8"))
        if visible_text_bytes < active.min_visible_text_bytes:
            failure_reasons.append(
                "visible text too small: "
                f"{visible_text_bytes} bytes < required {active.min_visible_text_bytes}"
            )

    failure_reasons.extend(
        _missing_literals(
            haystack=visible_text,
            values=active.visible_text_contains,
            label="visible text",
        )
    )
    failure_reasons.extend(
        _missing_regexes(
            haystack=visible_text,
            patterns=active.visible_text_regexes,
            label="visible text",
        )
    )
    failure_reasons.extend(
        _missing_literals(
            haystack=rendered_dom,
            values=active.rendered_dom_contains,
            label="rendered DOM",
        )
    )
    failure_reasons.extend(
        _missing_regexes(
            haystack=rendered_dom,
            patterns=active.rendered_dom_regexes,
            label="rendered DOM",
        )
    )

    return SourceDetailSufficiencyResult(
        requirements=active,
        failure_reasons=tuple(failure_reasons),
    )


def source_detail_sufficiency_mode_change(result: SourceDetailSufficiencyResult) -> str | None:
    if not result.enabled:
        return None
    if result.passed:
        return "source_detail_sufficiency_passed"
    return "source_detail_sufficiency_failed"


def source_detail_sufficiency_limitation(result: SourceDetailSufficiencyResult) -> str | None:
    if not result.enabled or result.passed:
        return None
    return "source_detail_sufficiency_failed: " + "; ".join(result.failure_reasons)


def source_detail_sufficiency_failure_message(
    *, output_directory: str, result: SourceDetailSufficiencyResult
) -> str:
    return (
        "source_detail_sufficiency_failed after packet write: "
        f"{output_directory}; "
        + "; ".join(result.failure_reasons)
    )


def _missing_literals(*, haystack: str, values: Sequence[str], label: str) -> list[str]:
    return [f"missing {label} literal: {value!r}" for value in values if value not in haystack]


def _missing_regexes(*, haystack: str, patterns: Sequence[str], label: str) -> list[str]:
    missing: list[str] = []
    for pattern in patterns:
        if re.search(pattern, haystack) is None:
            missing.append(f"missing {label} regex: {pattern!r}")
    return missing
