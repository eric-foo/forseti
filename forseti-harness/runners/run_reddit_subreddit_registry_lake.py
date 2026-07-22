"""Operate the lake-native Reddit Subreddit Registry.

The reviewed front door for registry state that used to require a data-only
pull request: migrate the committed registry once, add or retag a tracked
subreddit, and read the folded current view.  Grid observations are written by
``run_reddit_subreddit_registry_refresh.py``, not here.

Owner contract:
- forseti/product/spines/capture/core/source_families/social_media/reddit/reddit_subreddit_registry_lake_cutover_architecture_v0.md
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Sequence

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from data_lake.reddit_subreddit_registry import (
    RedditSubredditRegistryLakeError,
    append_roster_change,
    fold_subreddit,
    known_subreddits,
    load_current_registry,
    migrate_legacy_registry,
    semantic_parity,
)
from data_lake.root import DataLakeRoot
from harness_utils import utc_now_z
from source_capture.models import (
    CaptureModeCategory,
    PacketTiming,
    SourceCaptureSlice,
    known_fact,
    not_applicable,
    not_attempted,
)
from source_capture.packet_assembly import stage_and_write_packet, staged_file_id_map
from runners._scaffold import exit_on_failure

MIGRATION_SOURCE_FAMILY = "reddit_subreddit_registry"
MIGRATION_SOURCE_SURFACE = "reddit_subreddit_registry_legacy_baseline"
MIGRATION_LOCATOR = "forseti://reddit-subreddit-registry/legacy-baseline"

DEFAULT_REGISTRY_PATH = (
    Path(__file__).resolve().parents[2]
    / "forseti"
    / "product"
    / "spines"
    / "capture"
    / "core"
    / "source_families"
    / "social_media"
    / "reddit"
    / "reddit_subreddit_registry_v0.json"
)


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Migrate, edit, and read the lake-native Reddit Subreddit Registry."
    )
    parser.add_argument("--data-root", type=Path, default=None, help="Lake root (defaults to resolution).")
    sub = parser.add_subparsers(dest="command", required=True)

    migrate = sub.add_parser("migrate", help="One-time baseline migration from the committed registry.")
    migrate.add_argument("--registry", type=Path, default=DEFAULT_REGISTRY_PATH)
    migrate.add_argument("--migration-packet-pointer", default=None)
    migrate.add_argument("--dry-run", action="store_true")

    parity = sub.add_parser("parity", help="Compare the folded registry against the committed JSON.")
    parity.add_argument("--registry", type=Path, default=DEFAULT_REGISTRY_PATH)

    add = sub.add_parser("add", help="Add a tracked subreddit (its own genesis record).")
    add.add_argument("--subreddit", required=True)
    add.add_argument("--niche-path", action="append", dest="niche_paths", default=[])
    add.add_argument("--venue-role", action="append", dest="venue_roles", default=[])
    add.add_argument("--discovery-state", default=None)
    add.add_argument("--actor", required=True)
    add.add_argument("--note", default=None)
    add.add_argument("--dry-run", action="store_true")

    update = sub.add_parser("update", help="Retag or otherwise change non-grid row state.")
    update.add_argument("--subreddit", required=True)
    update.add_argument("--niche-path", action="append", dest="niche_paths", default=None)
    update.add_argument("--venue-role", action="append", dest="venue_roles", default=None)
    update.add_argument("--discovery-state", default=None)
    update.add_argument("--capture-state", default=None)
    update.add_argument("--actor", required=True)
    update.add_argument("--note", default=None)
    update.add_argument("--dry-run", action="store_true")

    show = sub.add_parser("show", help="Fold and print the current registry (or one subreddit).")
    show.add_argument("--subreddit", default=None)

    return parser


def _roster_changes(args: argparse.Namespace) -> dict[str, object]:
    changes: dict[str, object] = {}
    if args.niche_paths:
        changes["niche_paths"] = list(args.niche_paths)
    if args.venue_roles:
        changes["venue_roles"] = list(args.venue_roles)
    if args.discovery_state:
        changes["discovery_state"] = args.discovery_state
    if getattr(args, "capture_state", None):
        changes["capture_state"] = args.capture_state
    return changes


def write_migration_packet(*, data_root: DataLakeRoot, registry_path: Path) -> str:
    """Preserve the exact committed registry bytes as immutable lake evidence.

    The baseline records are the foldable authority; this packet is what keeps
    the original input bytes available once the Git copy is eventually removed
    in a later work unit.
    """
    staged = [(registry_path.name, registry_path.read_bytes())]
    file_ids = staged_file_id_map(staged)
    generated_at = utc_now_z()
    source_hash = hashlib.sha256(staged[0][1]).hexdigest()
    timing = PacketTiming(
        source_publication_or_event=not_applicable(
            "migration freezes current repository operational state"
        ),
        source_edit_or_version=known_fact(f"registry sha256: {source_hash}"),
        capture_time=known_fact(generated_at),
        recapture_time=not_applicable("one baseline migration"),
        cutoff_posture=not_applicable("not a time-window source"),
    )
    access = known_fact("local repository file read for owner-authorized lake migration")
    archive = not_attempted("migration does not query an archive")
    media = not_applicable("JSON registry document")
    relationship = not_applicable("one migration baseline")
    result = stage_and_write_packet(
        data_root=data_root,
        staged_artifacts=staged,
        source_slices=[
            SourceCaptureSlice(
                slice_id="reddit_subreddit_registry_baseline_01",
                locator=known_fact(MIGRATION_LOCATOR),
                timing=timing,
                access_posture=access,
                archive_history_posture=archive,
                media_modality_posture=media,
                re_capture_relationship=relationship,
                limitations=[
                    "migration baseline; later observations and roster changes are separate append-only records"
                ],
                warning_notes=[],
                preserved_file_ids=[file_ids[staged[0][0]]],
                metric_observations=[],
            )
        ],
        source_family=MIGRATION_SOURCE_FAMILY,
        source_surface=MIGRATION_SOURCE_SURFACE,
        source_locator=known_fact(MIGRATION_LOCATOR),
        decision_question="What exact Reddit Subreddit Registry state is being migrated out of Git?",
        capture_context="Owner-authorized one-time migration of the exact committed registry document.",
        actor_audience_context=not_applicable("registry migration, not audience capture"),
        capture_mode=CaptureModeCategory.AUTOMATED_EXTRACTION,
        operator_category="reddit_subreddit_registry_migration_cli_operator",
        session_identity=None,
        visible_mode_changes=["reddit_subreddit_registry_lake_cutover_v0"],
        source_publication_or_event=timing.source_publication_or_event,
        source_edit_or_version=timing.source_edit_or_version,
        cutoff_posture=timing.cutoff_posture,
        recapture_time=timing.recapture_time,
        access_posture=access,
        archive_history_posture=archive,
        media_modality_posture=media,
        re_capture_relationship=relationship,
        warnings=[],
        limitations=["one-time migration baseline"],
        receipt_summary="Reddit Subreddit Registry legacy baseline preserved for lake authority cut-over.",
        receipt_non_claims=[
            "not capture authorization",
            "not live Reddit access",
            "not demand proof",
        ],
    )
    return Path(result.output_directory).name


def _migrate(args: argparse.Namespace, data_root: DataLakeRoot) -> dict[str, object]:
    """Prove the migration before writing, then preserve bytes and write."""
    plan = migrate_legacy_registry(data_root, registry_path=args.registry, dry_run=True)
    if plan["status"] == "already_current":
        plan["parity"] = semantic_parity(
            legacy_registry_path=args.registry, folded=load_current_registry(data_root)
        )
        return plan
    if args.dry_run:
        return plan

    packet_id = args.migration_packet_pointer or write_migration_packet(
        data_root=data_root, registry_path=args.registry
    )
    written = migrate_legacy_registry(
        data_root,
        registry_path=args.registry,
        migration_packet_pointer=packet_id,
    )
    written["migration_packet_id"] = packet_id
    written["parity"] = semantic_parity(
        legacy_registry_path=args.registry, folded=load_current_registry(data_root)
    )
    return written


def _resolve_root(args: argparse.Namespace) -> DataLakeRoot:
    if args.data_root is not None:
        return DataLakeRoot.resolve(args.data_root)
    return DataLakeRoot.resolve()


def main(argv: Sequence[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)
    with exit_on_failure(
        parser,
        runner_name="reddit subreddit registry lake",
        expected=(RedditSubredditRegistryLakeError,),
        expected_status=3,
        format_expected=lambda exc: f"registry lake refused [{exc.code}]: {exc.message}",
        unexpected_status=2,
    ):
        data_root = _resolve_root(args)
        if args.command == "migrate":
            payload = _migrate(args, data_root)
        elif args.command == "parity":
            payload = semantic_parity(
                legacy_registry_path=args.registry,
                folded=load_current_registry(data_root),
            )
        elif args.command in {"add", "update"}:
            payload = append_roster_change(
                data_root,
                subreddit=args.subreddit,
                change_kind="add" if args.command == "add" else "update",
                changes=_roster_changes(args),
                actor=args.actor,
                note_or_none=args.note,
                dry_run=args.dry_run,
            )
        else:
            if args.subreddit:
                payload = fold_subreddit(data_root, args.subreddit)
            else:
                payload = load_current_registry(data_root)
                payload["known_subreddits"] = known_subreddits(data_root)
        print(json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
