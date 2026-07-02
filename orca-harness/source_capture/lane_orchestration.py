"""Small shared lane-run receipt contract for vertical capture orchestrators.

The contract records what each lane attempted and observed. It deliberately does not
standardize acquisition method, priority, metric shape, or platform-specific payloads;
those stay inside the IG/YT/TikTok adapters.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Literal

LaneStatus = Literal[
    "not_requested",
    "succeeded",
    "failed",
    "skipped",
    "incomplete",
    "blocked_operator_action_required",
    "not_attempted",
]


@dataclass(frozen=True)
class LaneReceipt:
    lane: str
    status: LaneStatus
    message: str = ""
    outputs: dict[str, Any] = field(default_factory=dict)
    residuals: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        out: dict[str, Any] = {"lane": self.lane, "status": self.status}
        if self.message:
            out["message"] = self.message
        if self.outputs:
            out["outputs"] = dict(self.outputs)
        if self.residuals:
            out["residuals"] = list(self.residuals)
        return out


@dataclass(frozen=True)
class LaneRunSummary:
    platform: str
    target: str
    receipts: tuple[LaneReceipt, ...]

    @property
    def complete(self) -> bool:
        return all(receipt.status in {"succeeded", "skipped"} for receipt in self.receipts)

    def to_dict(self) -> dict[str, Any]:
        return {
            "platform": self.platform,
            "target": self.target,
            "complete": self.complete,
            "receipts": [receipt.to_dict() for receipt in self.receipts],
        }
