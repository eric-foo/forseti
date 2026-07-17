"""Owning home for shared runner-CLI scaffolding (Shared Helpers convention,
forseti-harness/README.md).

Two blocks live here instead of being re-copied into each ``runners/`` script:

- ``resolve_output_root``: the ``--output`` / ``--data-root`` /
  ``FORSETI_DATA_ROOT`` / legacy ``ORCA_DATA_ROOT`` target-resolution block,
  parameterized by runner name so error messages stay byte-identical to the
  incumbent per-runner copies.
- ``exit_on_failure``: the ``try/except -> parser.exit`` exception-to-exit-code
  wrapper around a runner's main body.

A runner whose behavior genuinely diverges (preflight-only early exit before
resolution, JSON error reports on stdout, xor-after-resolve ordering) keeps its
local copy with a ``# helper-delta:`` comment naming the delta.

The 2-line ``if __package__ in {None, ""}`` sys.path shim is NOT shared: it
must run before any harness import, so it stays in every runner.
"""
from __future__ import annotations

import argparse
import contextlib
import os
from typing import Callable, Iterator

# Message details used by the incumbent copies; both render as
# "{runner_name} failed: {detail}\n" via parser.exit(status=2, ...).
EXACTLY_ONE_OUTPUT_DETAIL = (
    "exactly one of --output or --data-root/FORSETI_DATA_ROOT/ORCA_DATA_ROOT is required"
)
SUPPLY_ONLY_ONE_DETAIL = "supply only one of --output or --data-root"


def resolve_output_root(
    args: argparse.Namespace,
    parser: argparse.ArgumentParser,
    *,
    runner_name: str,
    both_supplied_detail: str = EXACTLY_ONE_OUTPUT_DETAIL,
):
    """Resolve the data-lake root for a runner with ``--output``/``--data-root``.

    Returns the resolved ``DataLakeRoot`` when lake mode is requested
    (``--data-root``, or ``FORSETI_DATA_ROOT``/legacy ``ORCA_DATA_ROOT`` with
    ``--output`` omitted); returns ``None`` when the runner should write to
    ``args.output``. Invalid target selection exits status 2 via
    ``parser.exit`` with the runner-named message. Callers that keep the
    incumbent "supply only one of --output or --data-root" wording pass
    ``both_supplied_detail=SUPPLY_ONLY_ONE_DETAIL``.
    """
    data_root = None
    data_root_requested = args.data_root is not None or (
        args.output is None
        and (os.environ.get("FORSETI_DATA_ROOT") or os.environ.get("ORCA_DATA_ROOT"))
    )
    if args.output is not None and args.data_root is not None:
        parser.exit(status=2, message=f"{runner_name} failed: {both_supplied_detail}\n")
    if args.output is None and not data_root_requested:
        parser.exit(status=2, message=f"{runner_name} failed: {EXACTLY_ONE_OUTPUT_DETAIL}\n")
    if data_root_requested:
        from data_lake.root import DataLakeRoot

        data_root = DataLakeRoot.resolve(explicit=args.data_root)
    return data_root


@contextlib.contextmanager
def exit_on_failure(
    parser: argparse.ArgumentParser,
    *,
    runner_name: str,
    expected: tuple[type[BaseException], ...] = (ValueError,),
    expected_status: int = 2,
    format_expected: Callable[[BaseException], str] | None = None,
    unexpected_status: int | None = 3,
    include_unexpected_type: bool = False,
) -> Iterator[None]:
    """Map exceptions from the wrapped body onto the incumbent exit codes.

    ``expected`` exceptions exit ``expected_status`` with
    ``"{runner_name} failed: {exc}"`` (or ``format_expected(exc)`` when given).
    Any other ``Exception`` exits ``unexpected_status`` with the same prefix,
    prepending ``"{type(exc).__name__}: "`` when ``include_unexpected_type`` is
    true; ``unexpected_status=None`` re-raises unexpected exceptions unchanged
    (for runners that deliberately have no catch-all). ``SystemExit`` -- e.g. a
    nested ``parser.exit`` -- always propagates untouched.
    """
    try:
        yield
    except expected as exc:
        message = (
            format_expected(exc)
            if format_expected is not None
            else f"{runner_name} failed: {exc}"
        )
        parser.exit(status=expected_status, message=f"{message}\n")
    except Exception as exc:  # noqa: BLE001 - surface capture/lake failures visibly
        if unexpected_status is None:
            raise
        detail = f"{type(exc).__name__}: {exc}" if include_unexpected_type else str(exc)
        parser.exit(status=unexpected_status, message=f"{runner_name} failed: {detail}\n")
