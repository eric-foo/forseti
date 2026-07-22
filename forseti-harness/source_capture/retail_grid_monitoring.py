from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Literal, Mapping
from urllib.parse import urlparse

from pydantic import Field, field_validator, model_validator

from harness_utils import generate_ulid, utc_now_z
from schemas.case_models import StrictModel
from source_capture.retail_grid_projection import RetailGridProjectionPacket


MONITOR_MANIFEST_VERSION = "retail_grid_monitor_manifest_v0"
MONITOR_RECEIPT_VERSION = "retail_grid_monitor_receipt_v0"
MONITOR_ROUND_REPORT_VERSION = "retail_grid_monitor_round_report_v0"
MONITOR_RETAILERS = ("sephora", "ulta", "target", "amazon")

Retailer = Literal["sephora", "ulta", "target", "amazon"]

_BRAND_ID_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
_ROUND_ID_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
_PROFILE_BY_RETAILER: dict[Retailer, str] = {
    "sephora": "sephora_grid_aggregate",
    "ulta": "ulta_grid_aggregate",
    "target": "target_grid_aggregate",
    "amazon": "amazon_grid_aggregate",
}
_HOST_BY_RETAILER: dict[Retailer, str] = {
    "sephora": "www.sephora.com",
    "ulta": "www.ulta.com",
    "target": "www.target.com",
    "amazon": "www.amazon.com",
}


class RetailGridMonitorRoute(StrictModel):
    url: str
    page_count: int | None = Field(default=None, ge=1)
    series_version: int = Field(default=1, ge=1)

    @field_validator("url")
    @classmethod
    def require_https_url(cls, value: str) -> str:
        parsed = urlparse(value)
        if parsed.scheme != "https" or not parsed.hostname:
            raise ValueError("retail-grid monitor URLs must be absolute https URLs")
        return value


class RetailGridMonitoredBrand(StrictModel):
    brand_id: str
    name: str
    retailers: dict[Retailer, RetailGridMonitorRoute]

    @field_validator("brand_id")
    @classmethod
    def validate_brand_id(cls, value: str) -> str:
        if not _BRAND_ID_RE.fullmatch(value):
            raise ValueError("brand_id must be a lowercase hyphenated identifier")
        return value

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("brand name must not be blank")
        return value.strip()

    @model_validator(mode="after")
    def validate_routes(self) -> "RetailGridMonitoredBrand":
        if not self.retailers:
            raise ValueError("a monitored brand requires at least one retailer route")
        for retailer, route in self.retailers.items():
            hostname = (urlparse(route.url).hostname or "").lower()
            if hostname != _HOST_BY_RETAILER[retailer]:
                raise ValueError(
                    f"{retailer} monitor route requires hostname "
                    f"{_HOST_BY_RETAILER[retailer]}; got {hostname or 'none'}"
                )
            if retailer == "amazon":
                if route.page_count is None:
                    raise ValueError("amazon monitor routes require page_count")
            elif route.page_count is not None:
                raise ValueError(f"page_count is supported only for amazon, not {retailer}")
        return self


class RetailGridMonitorManifest(StrictModel):
    manifest_version: Literal["retail_grid_monitor_manifest_v0"] = MONITOR_MANIFEST_VERSION
    brands: list[RetailGridMonitoredBrand]

    @model_validator(mode="after")
    def validate_unique_brand_ids(self) -> "RetailGridMonitorManifest":
        ids = [item.brand_id for item in self.brands]
        if not ids:
            raise ValueError("retail-grid monitor manifest requires at least one brand")
        if len(ids) != len(set(ids)):
            raise ValueError("retail-grid monitor manifest brand_id values must be unique")
        return self


class RetailGridMonitorReceipt(StrictModel):
    receipt_version: Literal["retail_grid_monitor_receipt_v0"] = MONITOR_RECEIPT_VERSION
    receipt_id: str
    round_id: str
    attempted_at: str
    completed_at: str
    series_id: str
    route_signature: str
    brand_id: str
    brand_name: str
    retailer: Retailer
    requested_url: str
    status: Literal["success", "failure"]
    raw_sample_requested: bool
    projection_path: str | None = None
    raw_packet_path: str | None = None
    runner_exit_code: int
    runner_message: str
    comparison: dict[str, object] | None = None

    @field_validator("round_id")
    @classmethod
    def validate_round_id(cls, value: str) -> str:
        if not _ROUND_ID_RE.fullmatch(value):
            raise ValueError("round_id must use YYYY-MM-DD")
        return value

    @model_validator(mode="after")
    def validate_status_paths(self) -> "RetailGridMonitorReceipt":
        if self.status == "success":
            if self.runner_exit_code != 0 or self.projection_path is None:
                raise ValueError("successful monitor receipts require exit 0 and projection_path")
        elif self.comparison is not None or self.projection_path is not None:
            raise ValueError("failed monitor receipts cannot claim projection comparison")
        return self


@dataclass(frozen=True)
class MonitorRoute:
    brand_id: str
    brand_name: str
    retailer: Retailer
    url: str
    page_count: int | None
    series_version: int

    @property
    def profile(self) -> str:
        return _PROFILE_BY_RETAILER[self.retailer]

    @property
    def series_id(self) -> str:
        return f"retail-grid:{self.brand_id}:{self.retailer}:v{self.series_version}"

    @property
    def qa_selector(self) -> str:
        return f"{self.brand_id}:{self.retailer}"

    @property
    def signature(self) -> str:
        body = json.dumps(
            {
                "page_count": self.page_count,
                "profile": self.profile,
                "series_id": self.series_id,
                "url": self.url,
            },
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
        return hashlib.sha256(body).hexdigest()


@dataclass(frozen=True)
class RetailGridCaptureAttempt:
    exit_code: int
    message: str
    projection_path: Path | None = None
    raw_packet_path: Path | None = None


CaptureRoute = Callable[[MonitorRoute, bool], RetailGridCaptureAttempt]


def load_monitor_manifest(path: Path) -> RetailGridMonitorManifest:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"unable to read retail-grid monitor manifest {path}: {exc}") from exc
    return RetailGridMonitorManifest.model_validate(payload)


def monitor_routes(manifest: RetailGridMonitorManifest) -> list[MonitorRoute]:
    routes: list[MonitorRoute] = []
    for brand in manifest.brands:
        for retailer in MONITOR_RETAILERS:
            route = brand.retailers.get(retailer)  # type: ignore[arg-type]
            if route is None:
                continue
            routes.append(
                MonitorRoute(
                    brand_id=brand.brand_id,
                    brand_name=brand.name,
                    retailer=retailer,  # type: ignore[arg-type]
                    url=route.url,
                    page_count=route.page_count,
                    series_version=route.series_version,
                )
            )
    return routes


def _series_directory(state_dir: Path, series_id: str) -> Path:
    key = hashlib.sha256(series_id.encode("utf-8")).hexdigest()[:20]
    return state_dir / "series" / key


def _load_receipts(
    state_dir: Path, route: MonitorRoute
) -> list[tuple[Path, RetailGridMonitorReceipt]]:
    directory = _series_directory(state_dir, route.series_id)
    if not directory.exists():
        return []
    loaded: list[tuple[Path, RetailGridMonitorReceipt]] = []
    for path in sorted(directory.glob("*.json")):
        try:
            receipt = RetailGridMonitorReceipt.model_validate_json(path.read_text(encoding="utf-8"))
        except (OSError, ValueError) as exc:
            raise ValueError(f"invalid retail-grid monitor receipt {path}: {exc}") from exc
        if receipt.series_id != route.series_id:
            raise ValueError(f"monitor receipt series mismatch at {path}")
        if receipt.route_signature != route.signature:
            if receipt.status == "success":
                raise ValueError(
                    "monitor route changed without a series_version bump: "
                    f"{route.qa_selector}"
                )
            # A failed attempt admitted no observation into this series. Keep its
            # diagnostic receipt, but do not let a corrected pre-success route typo
            # become either false longitudinal history or needless version ceremony.
            continue
        loaded.append((path, receipt))
    return loaded


def _write_json_create(path: Path, payload: Mapping[str, object]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    with path.open("x", encoding="utf-8", newline="\n") as handle:
        handle.write(text)
    return path


def _validate_projection_path(data_root: "DataLakeRoot", path: Path) -> Path:
    resolved = path.resolve()
    derived_root = (data_root.path / "derived").resolve()
    try:
        resolved.relative_to(derived_root)
    except ValueError as exc:
        raise ValueError(
            f"monitor projection path is outside the verified derived root: {path}"
        ) from exc
    if not resolved.is_file():
        raise ValueError(f"monitor projection path is not a file: {path}")
    return resolved


def _validate_raw_path(data_root: "DataLakeRoot", path: Path, packet_id: str) -> Path:
    resolved = path.resolve()
    raw_root = (data_root.path / "raw").resolve()
    try:
        resolved.relative_to(raw_root)
    except ValueError as exc:
        raise ValueError(f"monitor raw path is outside the verified raw root: {path}") from exc
    if not resolved.is_dir() or resolved.name != packet_id:
        raise ValueError(f"monitor raw sample path does not bind packet {packet_id}: {path}")
    return resolved


def _load_observation(
    *, data_root: "DataLakeRoot", path: Path, route: MonitorRoute, raw_sample_requested: bool
) -> tuple[RetailGridProjectionPacket, Path]:
    projection_path = _validate_projection_path(data_root, path)
    try:
        observation = RetailGridProjectionPacket.model_validate_json(
            projection_path.read_text(encoding="utf-8")
        )
    except (OSError, ValueError) as exc:
        raise ValueError(f"invalid retail-grid observation {projection_path}: {exc}") from exc
    if observation.projection_version != "v1" or observation.capture_event is None:
        raise ValueError("monitor requires a v1 retail-grid observation")
    if observation.capture_event.series_id != route.series_id:
        raise ValueError(
            "monitor observation series mismatch: "
            f"expected {route.series_id}, got {observation.capture_event.series_id}"
        )
    if observation.capture_event.capture_profile != route.profile:
        raise ValueError(
            "monitor observation profile mismatch: "
            f"expected {route.profile}, got {observation.capture_event.capture_profile}"
        )
    if any(row.retailer != route.retailer for row in observation.rows):
        raise ValueError("monitor observation contains rows from a different retailer")
    sample_packet_id = observation.capture_event.raw_sample_packet_id
    if raw_sample_requested and sample_packet_id is None:
        raise ValueError("requested monitor raw QA sample was not linked from the observation")
    if not raw_sample_requested and sample_packet_id is not None:
        raise ValueError("routine monitor success unexpectedly claims a raw QA sample")
    return observation, projection_path


def _row_summary(row: object) -> dict[str, object | None]:
    fields = row.source_visible_fields  # type: ignore[attr-defined]
    return {
        "source_product_id": fields.get("source_product_id"),
        "name": fields.get("name"),
        "product_url": fields.get("product_url"),
    }


def _placements(row: object) -> list[dict[str, int | None]]:
    return sorted(
        [
            {
                "grid_position": item.grid_position,
                "page": item.page,
                "page_position": item.page_position,
            }
            for item in row.placements  # type: ignore[attr-defined]
        ],
        key=lambda item: (
            item["grid_position"] or 0,
            item["page"] or 0,
            item["page_position"] or 0,
        ),
    )


def compare_observations(
    previous: RetailGridProjectionPacket,
    current: RetailGridProjectionPacket,
    *,
    intervening_failure_rounds: int,
) -> dict[str, object]:
    assert previous.capture_event is not None
    assert current.capture_event is not None
    previous_rows = {
        str(row.source_visible_fields["source_product_id"]): row for row in previous.rows
    }
    current_rows = {
        str(row.source_visible_fields["source_product_id"]): row for row in current.rows
    }
    previous_ids = set(previous_rows)
    current_ids = set(current_rows)

    placement_changes: list[dict[str, object]] = []
    price_changes: list[dict[str, object | None]] = []
    for product_id in sorted(previous_ids & current_ids):
        before_row = previous_rows[product_id]
        after_row = current_rows[product_id]
        before_placements = _placements(before_row)
        after_placements = _placements(after_row)
        if before_placements != after_placements:
            placement_changes.append(
                {
                    "source_product_id": product_id,
                    "name": after_row.source_visible_fields.get("name"),
                    "before": before_placements,
                    "after": after_placements,
                }
            )
        before_price = before_row.source_visible_fields.get("price_display")
        after_price = after_row.source_visible_fields.get("price_display")
        if before_price != after_price:
            price_changes.append(
                {
                    "source_product_id": product_id,
                    "name": after_row.source_visible_fields.get("name"),
                    "before": before_price,
                    "after": after_price,
                }
            )

    previous_completeness = previous.completeness.model_dump(mode="json")
    current_completeness = current.completeness.model_dump(mode="json")
    completeness_changes = {
        key: {"before": previous_completeness.get(key), "after": current_completeness.get(key)}
        for key in sorted(set(previous_completeness) | set(current_completeness))
        if previous_completeness.get(key) != current_completeness.get(key)
    }
    return {
        "comparison_status": "compared",
        "previous_capture_event_id": previous.capture_event.capture_event_id,
        "current_capture_event_id": current.capture_event.capture_event_id,
        "intervening_failure_rounds": intervening_failure_rounds,
        "products_added": [
            _row_summary(current_rows[item]) for item in sorted(current_ids - previous_ids)
        ],
        "products_removed": [
            _row_summary(previous_rows[item]) for item in sorted(previous_ids - current_ids)
        ],
        "placement_changes": placement_changes,
        "price_display_changes": price_changes,
        "completeness_changes": completeness_changes,
        "previous_completeness_residuals": list(previous.completeness.residuals),
        "current_completeness_residuals": list(current.completeness.residuals),
    }


def _receipt_result(
    path: Path,
    receipt: RetailGridMonitorReceipt,
    *,
    status: str | None = None,
) -> dict[str, object]:
    return {
        "series_id": receipt.series_id,
        "brand_id": receipt.brand_id,
        "retailer": receipt.retailer,
        "status": status or receipt.status,
        "receipt_path": str(path),
        "projection_path": receipt.projection_path,
        "raw_packet_path": receipt.raw_packet_path,
        "comparison": receipt.comparison,
        "runner_exit_code": receipt.runner_exit_code,
        "runner_message": receipt.runner_message,
    }


def run_monitor_round(
    *,
    manifest: RetailGridMonitorManifest,
    data_root: "DataLakeRoot",
    state_dir: Path,
    round_id: str,
    qa_samples: set[str],
    capture_route: CaptureRoute,
) -> tuple[int, Path, dict[str, object]]:
    if not _ROUND_ID_RE.fullmatch(round_id):
        raise ValueError("round_id must use YYYY-MM-DD")
    routes = monitor_routes(manifest)
    known_selectors = {route.qa_selector for route in routes}
    unknown_selectors = sorted(qa_samples - known_selectors)
    if unknown_selectors:
        raise ValueError(f"unknown QA sample selector(s): {', '.join(unknown_selectors)}")
    if (
        state_dir.resolve() == data_root.path.resolve()
        or data_root.path.resolve() in state_dir.resolve().parents
    ):
        raise ValueError("monitor state directory must be outside the data lake")

    started_at = utc_now_z()
    results: list[dict[str, object]] = []
    failures = 0
    for route in routes:
        history = _load_receipts(state_dir, route)
        successful = [(path, item) for path, item in history if item.status == "success"]
        same_round = [(path, item) for path, item in successful if item.round_id == round_id]
        force_sample = route.qa_selector in qa_samples
        if same_round and not force_sample:
            path, receipt = same_round[-1]
            results.append(_receipt_result(path, receipt, status="already_successful"))
            continue

        raw_sample_requested = not successful or force_sample
        attempted_at = utc_now_z()
        try:
            attempt = capture_route(route, raw_sample_requested)
        except Exception as exc:  # noqa: BLE001 - convert a capture crash into a visible gap
            # One route's crash must stay one route's failure receipt; it must not
            # abandon the remaining routes or the round report that makes the gap
            # visible. Route-history errors raised above deliberately still abort.
            attempt = RetailGridCaptureAttempt(
                exit_code=3,
                message=f"monitor_capture_raised: {type(exc).__name__}: {exc}",
            )
        receipt_id = generate_ulid()
        completed_at = utc_now_z()
        status: Literal["success", "failure"] = "failure"
        projection_path: str | None = None
        raw_packet_path: str | None = None
        comparison: dict[str, object] | None = None
        message = attempt.message
        exit_code = attempt.exit_code
        if attempt.raw_packet_path is not None:
            try:
                verified_raw_path = _validate_raw_path(
                    data_root,
                    attempt.raw_packet_path,
                    attempt.raw_packet_path.name,
                )
                raw_packet_path = str(verified_raw_path)
            except ValueError as exc:
                message = f"{message}; monitor_raw_path_validation_failed: {exc}"
                if exit_code == 0:
                    exit_code = 4

        if exit_code == 0 and attempt.projection_path is not None:
            try:
                observation, verified_projection_path = _load_observation(
                    data_root=data_root,
                    path=attempt.projection_path,
                    route=route,
                    raw_sample_requested=raw_sample_requested,
                )
                assert observation.capture_event is not None
                if raw_sample_requested:
                    if attempt.raw_packet_path is None:
                        raise ValueError("successful QA sample did not report a raw packet path")
                    _validate_raw_path(
                        data_root,
                        attempt.raw_packet_path,
                        observation.capture_event.raw_sample_packet_id or "",
                    )
                if successful:
                    previous_path, previous_receipt = successful[-1]
                    if previous_receipt.projection_path is None:
                        raise ValueError(
                            f"successful prior receipt lacks projection path: {previous_path}"
                        )
                    previous, _ = _load_observation(
                        data_root=data_root,
                        path=Path(previous_receipt.projection_path),
                        route=route,
                        raw_sample_requested=previous_receipt.raw_sample_requested,
                    )
                    previous_index = history.index((previous_path, previous_receipt))
                    failed_rounds = {
                        item.round_id
                        for _path, item in history[previous_index + 1 :]
                        if item.status == "failure" and item.round_id != round_id
                    }
                    comparison = compare_observations(
                        previous,
                        observation,
                        intervening_failure_rounds=len(failed_rounds),
                    )
                else:
                    comparison = {
                        "comparison_status": "baseline",
                        "current_capture_event_id": observation.capture_event.capture_event_id,
                        "intervening_failure_rounds": 0,
                        "current_completeness_residuals": list(
                            observation.completeness.residuals
                        ),
                    }
                status = "success"
                projection_path = str(verified_projection_path)
            except ValueError as exc:
                exit_code = 4
                message = f"monitor_projection_validation_failed: {exc}; runner={attempt.message}"

        receipt = RetailGridMonitorReceipt(
            receipt_id=receipt_id,
            round_id=round_id,
            attempted_at=attempted_at,
            completed_at=completed_at,
            series_id=route.series_id,
            route_signature=route.signature,
            brand_id=route.brand_id,
            brand_name=route.brand_name,
            retailer=route.retailer,
            requested_url=route.url,
            status=status,
            raw_sample_requested=raw_sample_requested,
            projection_path=projection_path,
            raw_packet_path=raw_packet_path,
            runner_exit_code=exit_code,
            runner_message=message,
            comparison=comparison,
        )
        receipt_path = _write_json_create(
            _series_directory(state_dir, route.series_id) / f"{receipt_id}.json",
            receipt.model_dump(mode="json"),
        )
        results.append(_receipt_result(receipt_path, receipt))
        if status == "failure":
            failures += 1

    completed_at = utc_now_z()
    report = {
        "report_version": MONITOR_ROUND_REPORT_VERSION,
        "report_id": generate_ulid(),
        "round_id": round_id,
        "started_at": started_at,
        "completed_at": completed_at,
        "status": "complete" if failures == 0 else "partial_failure",
        "configured_series_count": len(routes),
        "failure_count": failures,
        "results": results,
    }
    report_path = _write_json_create(
        state_dir / "rounds" / f"{round_id}__{report['report_id']}.json", report
    )
    return (0 if failures == 0 else 4), report_path, report


from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from data_lake.root import DataLakeRoot


__all__ = [
    "CaptureRoute",
    "MonitorRoute",
    "RetailGridCaptureAttempt",
    "RetailGridMonitorManifest",
    "RetailGridMonitorReceipt",
    "compare_observations",
    "load_monitor_manifest",
    "monitor_routes",
    "run_monitor_round",
]
