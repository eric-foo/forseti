from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from harness_utils import as_dict


TIKTOK_BLOCKER_CLASS_NO_BLOCKER = "no_blocker"
TIKTOK_BLOCKER_CLASS_BENIGN_DISMISSIBLE_OVERLAY = "benign_dismissible_overlay"
TIKTOK_BLOCKER_CLASS_INFRASTRUCTURE_RELOAD = "infrastructure_reload"
TIKTOK_BLOCKER_CLASS_CHALLENGE_OR_SECURITY = "challenge_or_security"
TIKTOK_BLOCKER_CLASS_AMBIGUOUS = "ambiguous_stop"

TIKTOK_BLOCKER_ACTION_CONTINUE = "continue"
TIKTOK_BLOCKER_ACTION_DISMISS_ONCE_CANDIDATE = "dismiss_once_candidate"
TIKTOK_BLOCKER_ACTION_RELOAD_ONCE_CANDIDATE = "reload_once_candidate"
TIKTOK_BLOCKER_ACTION_STOP = "stop"

_CHALLENGE_MARKERS = (
    "verify to continue",
    "drag the slider",
    "captcha",
    "security check",
    "too many attempts",
    "maximum number of attempts",
    "unusual traffic",
    "your account might be at risk",
    "account might be at risk",
    "log in to comment",
)
_BENIGN_OVERLAY_MARKERS = (
    "open app",
    "get the app",
    "continue in browser",
    "not now",
    "maybe later",
    "log in to follow creators",
    "log in to like videos",
    "accept all",
    "got it",
    "press ok",
    "tap ok",
    "click ok",
    "scroll, use the",
    "browse your feed",
)
_DISMISS_MARKERS = (
    "not now",
    "maybe later",
    "continue in browser",
    "accept all",
    "got it",
    "press ok",
    "tap ok",
    "click ok",
)
_RELOAD_MARKERS = (
    "reload",
    "retry",
    "retry again",
    "try again",
    "something went wrong",
    "couldn't load",
    "could not load",
    "failed to load",
)


@dataclass(frozen=True)
class TikTokBlockerTriage:
    blocker_class: str
    action: str
    reason: str
    challenge_marker_seen: bool = False
    hydration_present: bool | None = None
    item_struct_present: bool | None = None
    visible_surface_ready: bool | None = None
    dismiss_candidate_count: int = 0
    reload_candidate_count: int = 0
    marker_family: str | None = None
    matched_marker: str | None = None
    challenge_kind: str | None = None

    def to_receipt(self) -> dict[str, object]:
        receipt: dict[str, object] = {
            "blocker_class": self.blocker_class,
            "action": self.action,
            "reason": self.reason,
            "challenge_marker_seen": self.challenge_marker_seen,
            "dismiss_candidate_count": self.dismiss_candidate_count,
            "reload_candidate_count": self.reload_candidate_count,
        }
        if self.hydration_present is not None:
            receipt["hydration_present"] = self.hydration_present
        if self.item_struct_present is not None:
            receipt["item_struct_present"] = self.item_struct_present
        if self.visible_surface_ready is not None:
            receipt["visible_surface_ready"] = self.visible_surface_ready
        if self.marker_family is not None:
            receipt["marker_family"] = self.marker_family
        if self.matched_marker is not None:
            receipt["matched_marker"] = self.matched_marker
        if self.challenge_kind is not None:
            receipt["challenge_kind"] = self.challenge_kind
        return receipt


def classify_tiktok_capture(
    capture_result: object,
    *,
    item_struct_present: bool | None = None,
    visible_surface_ready: bool | None = None,
    dismiss_candidate_count: int = 0,
    reload_candidate_count: int = 0,
) -> TikTokBlockerTriage:
    dom_observation = as_dict(getattr(capture_result, "dom_observation", {}))
    hydration_present = bool(_first_str(dom_observation.get("hydration_json_text")))
    return classify_tiktok_blocker(
        final_url=_first_str(getattr(capture_result, "final_url", None)) or "",
        title=_first_str(getattr(capture_result, "title", None)) or "",
        visible_text=_first_str(getattr(capture_result, "visible_text", None)) or "",
        hydration_present=hydration_present,
        item_struct_present=item_struct_present,
        visible_surface_ready=visible_surface_ready,
        dismiss_candidate_count=dismiss_candidate_count,
        reload_candidate_count=reload_candidate_count,
    )


def classify_tiktok_blocker(
    *,
    final_url: str,
    title: str,
    visible_text: str,
    hydration_present: bool | None,
    item_struct_present: bool | None,
    visible_surface_ready: bool | None = None,
    dismiss_candidate_count: int = 0,
    reload_candidate_count: int = 0,
) -> TikTokBlockerTriage:
    haystack = "\n".join((final_url, title, visible_text)).lower()
    dismiss_count = max(0, int(dismiss_candidate_count))
    reload_count = max(0, int(reload_candidate_count))

    if "/login" in final_url.lower():
        return TikTokBlockerTriage(
            blocker_class=TIKTOK_BLOCKER_CLASS_CHALLENGE_OR_SECURITY,
            action=TIKTOK_BLOCKER_ACTION_STOP,
            reason="login_or_auth_wall_observed",
            challenge_marker_seen=True,
            hydration_present=hydration_present,
            item_struct_present=item_struct_present,
            visible_surface_ready=visible_surface_ready,
            dismiss_candidate_count=dismiss_count,
            reload_candidate_count=reload_count,
            marker_family="login_or_auth_wall",
            matched_marker="/login",
            challenge_kind="login_or_auth_wall",
        )
    challenge_marker = _first_contained_marker(haystack, _CHALLENGE_MARKERS)
    if challenge_marker is not None:
        return TikTokBlockerTriage(
            blocker_class=TIKTOK_BLOCKER_CLASS_CHALLENGE_OR_SECURITY,
            action=TIKTOK_BLOCKER_ACTION_STOP,
            reason="platform_challenge_observed",
            challenge_marker_seen=True,
            hydration_present=hydration_present,
            item_struct_present=item_struct_present,
            visible_surface_ready=visible_surface_ready,
            dismiss_candidate_count=dismiss_count,
            reload_candidate_count=reload_count,
            marker_family="challenge_or_security",
            matched_marker=challenge_marker,
            challenge_kind=_challenge_kind_from_text(haystack),
        )

    reload_marker_seen = _contains_any(haystack, _RELOAD_MARKERS) or reload_count > 0
    if item_struct_present is False and visible_surface_ready is not True:
        return TikTokBlockerTriage(
            blocker_class=TIKTOK_BLOCKER_CLASS_INFRASTRUCTURE_RELOAD,
            action=TIKTOK_BLOCKER_ACTION_RELOAD_ONCE_CANDIDATE,
            reason="missing_item_struct_or_empty_shell",
            hydration_present=hydration_present,
            item_struct_present=item_struct_present,
            visible_surface_ready=visible_surface_ready,
            dismiss_candidate_count=dismiss_count,
            reload_candidate_count=reload_count,
            marker_family="reload_or_empty_shell",
        )
    if (
        reload_marker_seen
        and item_struct_present is not True
        and visible_surface_ready is not True
    ):
        return TikTokBlockerTriage(
            blocker_class=TIKTOK_BLOCKER_CLASS_INFRASTRUCTURE_RELOAD,
            action=TIKTOK_BLOCKER_ACTION_RELOAD_ONCE_CANDIDATE,
            reason="reload_marker_observed",
            hydration_present=hydration_present,
            item_struct_present=item_struct_present,
            visible_surface_ready=visible_surface_ready,
            dismiss_candidate_count=dismiss_count,
            reload_candidate_count=reload_count,
            marker_family="reload_or_empty_shell",
        )

    benign_marker_seen = _contains_any(haystack, _BENIGN_OVERLAY_MARKERS)
    dismiss_marker_seen = _contains_any(haystack, _DISMISS_MARKERS) or dismiss_count > 0
    if benign_marker_seen and dismiss_marker_seen:
        return TikTokBlockerTriage(
            blocker_class=TIKTOK_BLOCKER_CLASS_BENIGN_DISMISSIBLE_OVERLAY,
            action=TIKTOK_BLOCKER_ACTION_DISMISS_ONCE_CANDIDATE,
            reason="benign_overlay_marker_with_dismiss_control",
            hydration_present=hydration_present,
            item_struct_present=item_struct_present,
            visible_surface_ready=visible_surface_ready,
            dismiss_candidate_count=dismiss_count,
            reload_candidate_count=reload_count,
            marker_family="benign_overlay",
        )
    if dismiss_marker_seen:
        return TikTokBlockerTriage(
            blocker_class=TIKTOK_BLOCKER_CLASS_AMBIGUOUS,
            action=TIKTOK_BLOCKER_ACTION_STOP,
            reason="unclassified_dismiss_control",
            hydration_present=hydration_present,
            item_struct_present=item_struct_present,
            visible_surface_ready=visible_surface_ready,
            dismiss_candidate_count=dismiss_count,
            reload_candidate_count=reload_count,
            marker_family="ambiguous_dismiss",
        )
    if (
        hydration_present is False
        and item_struct_present is not True
        and visible_surface_ready is not True
    ):
        return TikTokBlockerTriage(
            blocker_class=TIKTOK_BLOCKER_CLASS_INFRASTRUCTURE_RELOAD,
            action=TIKTOK_BLOCKER_ACTION_RELOAD_ONCE_CANDIDATE,
            reason="missing_hydration",
            hydration_present=hydration_present,
            item_struct_present=item_struct_present,
            visible_surface_ready=visible_surface_ready,
            dismiss_candidate_count=dismiss_count,
            reload_candidate_count=reload_count,
            marker_family="reload_or_empty_shell",
        )
    return TikTokBlockerTriage(
        blocker_class=TIKTOK_BLOCKER_CLASS_NO_BLOCKER,
        action=TIKTOK_BLOCKER_ACTION_CONTINUE,
        reason="no_blocker_markers_observed",
        hydration_present=hydration_present,
        item_struct_present=item_struct_present,
        visible_surface_ready=visible_surface_ready,
        dismiss_candidate_count=dismiss_count,
        reload_candidate_count=reload_count,
    )


def _contains_any(text: str, markers: tuple[str, ...]) -> bool:
    return _first_contained_marker(text, markers) is not None


def _challenge_kind_from_text(haystack: str) -> str:
    if "account might be at risk" in haystack:
        return "account_risk"
    if "log in to comment" in haystack:
        return "logged_out_or_auth_wall"
    if "drag the slider" in haystack:
        return "slider"
    if "captcha" in haystack:
        return "captcha"
    if "security check" in haystack:
        return "security_check"
    if any(
        marker in haystack
        for marker in ("too many attempts", "maximum number of attempts", "unusual traffic")
    ):
        return "rate_limit_or_traffic"
    if "verify to continue" in haystack:
        return "verification_gate"
    return "unknown_platform_challenge"

def _first_contained_marker(text: str, markers: tuple[str, ...]) -> str | None:
    for marker in markers:
        if marker in text:
            return marker
    return None


def _first_str(*values: Any) -> str | None:
    for value in values:
        if value is None:
            continue
        if isinstance(value, str):
            stripped = value.strip()
            if stripped:
                return stripped
        elif isinstance(value, (int, float, bool)):
            return str(value)
    return None


__all__ = [
    "TIKTOK_BLOCKER_ACTION_CONTINUE",
    "TIKTOK_BLOCKER_ACTION_DISMISS_ONCE_CANDIDATE",
    "TIKTOK_BLOCKER_ACTION_RELOAD_ONCE_CANDIDATE",
    "TIKTOK_BLOCKER_ACTION_STOP",
    "TIKTOK_BLOCKER_CLASS_AMBIGUOUS",
    "TIKTOK_BLOCKER_CLASS_BENIGN_DISMISSIBLE_OVERLAY",
    "TIKTOK_BLOCKER_CLASS_CHALLENGE_OR_SECURITY",
    "TIKTOK_BLOCKER_CLASS_INFRASTRUCTURE_RELOAD",
    "TIKTOK_BLOCKER_CLASS_NO_BLOCKER",
    "TikTokBlockerTriage",
    "classify_tiktok_blocker",
    "classify_tiktok_capture",
]
