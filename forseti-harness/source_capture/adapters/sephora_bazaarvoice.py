"""Compatibility import for the shared Bazaarvoice API transport."""

from source_capture.adapters.bazaarvoice_api import (
    BAZAARVOICE_API_HOST,
    ApiFetcher,
    ApiRequestSpec,
    ApiResponse,
    BazaarvoiceApiCaptureError,
    BazaarvoiceReadConfig,
    fetch_bazaarvoice_api_response,
)

__all__ = [
    "ApiFetcher",
    "ApiRequestSpec",
    "ApiResponse",
    "BAZAARVOICE_API_HOST",
    "BazaarvoiceApiCaptureError",
    "BazaarvoiceReadConfig",
    "fetch_bazaarvoice_api_response",
]
