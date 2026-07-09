from __future__ import annotations

from dataclasses import dataclass

from source_capture.adapters.direct_http import (
    DEFAULT_MAX_BYTES,
    DEFAULT_TIMEOUT_SECONDS,
    DirectHttpCaptureFailure,
    DirectHttpCaptureSuccess,
    fetch_direct_http_capture,
)


@dataclass(frozen=True)
class MediaAssetCaptureSuccess:
    asset_index: int
    asset_url: str
    http_result: DirectHttpCaptureSuccess


@dataclass(frozen=True)
class MediaAssetCaptureFailure:
    asset_index: int
    asset_url: str
    http_result: DirectHttpCaptureFailure


@dataclass(frozen=True)
class MediaAssetCaptureBatch:
    successes: list[MediaAssetCaptureSuccess]
    failures: list[MediaAssetCaptureFailure]


def fetch_media_assets(
    *,
    asset_urls: list[str],
    timeout_seconds: float = DEFAULT_TIMEOUT_SECONDS,
    max_bytes: int = DEFAULT_MAX_BYTES,
) -> MediaAssetCaptureBatch:
    if not asset_urls:
        raise ValueError("at least one --asset-url is required")

    successes: list[MediaAssetCaptureSuccess] = []
    failures: list[MediaAssetCaptureFailure] = []
    for index, asset_url in enumerate(asset_urls, start=1):
        result = fetch_direct_http_capture(
            url=asset_url,
            timeout_seconds=timeout_seconds,
            max_bytes=max_bytes,
        )
        if isinstance(result, DirectHttpCaptureFailure):
            failures.append(
                MediaAssetCaptureFailure(
                    asset_index=index,
                    asset_url=asset_url,
                    http_result=result,
                )
            )
            continue
        successes.append(
            MediaAssetCaptureSuccess(
                asset_index=index,
                asset_url=asset_url,
                http_result=result,
            )
        )

    return MediaAssetCaptureBatch(successes=successes, failures=failures)
