from __future__ import annotations

import hashlib
import json
import re
import subprocess
from collections import Counter
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any

from capture_spine.creator_public_handle_linkage.models import CreatorPublicHandleLinkageError
from capture_spine.creator_public_handle_linkage.validation import assert_no_forbidden_output_fields
from data_lake.root import LEGACY_ROOT_MARKER_FILENAME, ROOT_MARKER_FILENAME


YOUTUBE_CREATOR_OBSERVATION_LEDGER_SCHEMA_VERSION = "youtube_creator_observation_ledger_v0"
_WRAPPER_KEY = "youtube_creator_observation_ledger"

_ALLOWED_TOP_LEVEL_KEYS = frozenset({_WRAPPER_KEY})
_REQUIRED_WRAPPER_KEYS = frozenset(
    {
        "schema_version",
        "ledger_id",
        "ledger_mode",
        "compiled_at_utc",
        "source_policy_posture",
        "authority_pointers",
        "source_inputs",
        "niche_scope",
        "counts",
        "metric_rollup_policy",
        "creator_observations",
        "accepted_residuals",
        "non_claims",
    }
)
# operator_video_retirements is additive-optional on the v0 schema: existing
# ledgers without it stay valid; when present it is validated fail-closed.
_ALLOWED_WRAPPER_KEYS = _REQUIRED_WRAPPER_KEYS | {"operator_video_retirements"}
_ALLOWED_RETIREMENT_KEYS = frozenset(
    {"video_id", "reason", "retired_at_utc", "evidence_packet_ids"}
)
_ALLOWED_NICHE_KEYS = frozenset({"domain", "subdomain", "platform_surface", "membership_basis"})
_ALLOWED_COUNTS_KEYS = frozenset(
    {
        "creator_observations_total",
        "creator_or_channel_observed",
        "brand_or_platform_account_observed",
        "source_pool_rows_total",
        "unique_video_ids",
        "data_lake_youtube_packets_matched",
        "data_lake_youtube_caption_packets",
        "data_lake_youtube_audio_packets",
        "unique_youtube_channel_ids",
        "video_channel_id_missing_in_lake_metadata",
    }
)
_ALLOWED_METRIC_POLICY_KEYS = frozenset(
    {"current_status", "reason", "do_not_store_absence_as_zero", "open_next"}
)
_ALLOWED_SOURCE_INPUT_KEYS = frozenset(
    {"source_pointer", "sha256", "role", "root_uuid", "root_contract_version", "root_label"}
)
_ALLOWED_OBSERVATION_KEYS = frozenset(
    {
        "creator_observation_id",
        "platform",
        "platform_subject_key_type",
        "platform_subject_key",
        "public_profile_url",
        "creator_handle_query",
        "creator_classification",
        "identity_boundary",
        "niche_scope",
        "source_pool_id",
        "admitted_video_count",
        "observed_author_names",
        "source_observed_channel_ids",
        "resolved_lake_channel_ids",
        "lake_channel_id_missing_video_count",
        "source_artifact_counts",
        "pool_ids",
        "video_ids",
        "sample_shorts_urls",
        "data_lake_packet_refs",
        "transcript_word_count_min",
        "transcript_word_count_max",
        "known_label_status_counts_100_pool_only",
        "unlabeled_rows_in_pool200",
        "handle_source_pointer",
        "display_name_source_pointer",
        "video_membership_source_pointer",
        "lake_reconciliation_status",
        "limitations",
        "non_claims",
    }
)
_ALLOWED_PACKET_REF_KEYS = frozenset(
    {
        "video_id",
        "packet_id",
        "packet_relpath",
        "metadata_relpath",
        "source_surface",
        "channel_id_or_none",
        "caption_kind_or_none",
        "caption_lang_or_none",
        "duration_s_or_none",
        "publish_date_iso_or_none",
    }
)
_ALLOWED_CREATOR_CLASSIFICATIONS = frozenset(
    {"creator_or_channel_observed", "brand_or_platform_account_observed"}
)
_ALLOWED_SOURCE_SURFACES = frozenset({"youtube_captions", "youtube_audio"})
_YOUTUBE_FORBIDDEN_OUTPUT_FIELDS = frozenset(
    {
        "average_views",
        "caption_body",
        "caption_text",
        "comment_count",
        "comments",
        "engagement_rate",
        "full_transcript",
        "instagram_account_id",
        "instagram_handle",
        "instagram_profile_url",
        "instagram_public_handle",
        "instagram_url",
        "like_count",
        "likes",
        "raw_transcript",
        "share_count",
        "subscriber_count",
        "tiktok_account_id",
        "tiktok_handle",
        "tiktok_profile_url",
        "tiktok_public_handle",
        "tiktok_url",
        "transcript_body",
        "transcript_text",
        "view_count",
        "views",
    }
)
_PACKET_ID_RE = re.compile(r"[0123456789ABCDEFGHJKMNPQRSTVWXYZ]{26}")
_VIDEO_ID_RE = re.compile(r"[A-Za-z0-9_-]{11}")
_UTC_TIMESTAMP_RE = re.compile(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z")
_RAW_RELPATH_RE = re.compile(r"raw/[0-9a-f]{3}/[0123456789ABCDEFGHJKMNPQRSTVWXYZ]{26}")
_METADATA_RELPATH_RE = re.compile(
    r"raw/[0-9a-f]{3}/[0123456789ABCDEFGHJKMNPQRSTVWXYZ]{26}/raw/[0-9]{2}_[A-Za-z0-9_]+_metadata\.json"
)
_SHA256_RE = re.compile(r"[0-9a-f]{64}")


class YoutubeCreatorObservationLedgerError(ValueError):
    def __init__(self, code: str, message: str) -> None:
        super().__init__(message)
        self.code = code
        self.message = message


def load_youtube_creator_observation_ledger(path: str | Path) -> dict[str, Any]:
    value = json.loads(Path(path).read_text(encoding="utf-8-sig"))
    if not isinstance(value, dict):
        _fail("invalid_json_fixture", "YouTube creator observation ledger must be a JSON object")
    validate_youtube_creator_observation_ledger(value)
    return value


def validate_youtube_creator_observation_ledger(ledger: Mapping[str, Any]) -> None:
    _assert_no_youtube_forbidden_output_fields(ledger)
    try:
        assert_no_forbidden_output_fields(ledger)
    except CreatorPublicHandleLinkageError as exc:
        _fail(getattr(exc, "code", "forbidden_output_field"), str(exc))
    _reject_unknown_keys(ledger, _ALLOWED_TOP_LEVEL_KEYS, "ledger top-level")
    wrapper = _wrapper(ledger)
    _reject_unknown_keys(wrapper, _ALLOWED_WRAPPER_KEYS, "ledger")
    _require(wrapper, tuple(_REQUIRED_WRAPPER_KEYS), "ledger")
    if wrapper["schema_version"] != YOUTUBE_CREATOR_OBSERVATION_LEDGER_SCHEMA_VERSION:
        _fail("invalid_schema_version", "unexpected YouTube creator observation schema_version")
    if wrapper["ledger_mode"] != "source_backed_static_fixture":
        _fail("invalid_ledger_mode", "ledger_mode must be source_backed_static_fixture")
    _validate_str_list(wrapper["authority_pointers"], "authority_pointers", allow_empty=False)
    _validate_source_inputs(wrapper["source_inputs"])
    _validate_niche_scope(wrapper["niche_scope"])
    _validate_metric_policy(wrapper["metric_rollup_policy"])
    _validate_str_list(wrapper["accepted_residuals"], "accepted_residuals", allow_empty=False)
    _validate_required_non_claims(wrapper["non_claims"], "ledger")
    observations = _validate_observations(wrapper["creator_observations"])
    _validate_counts(wrapper["counts"], observations)
    _validate_operator_video_retirements(wrapper, observations)


def validate_source_rebuild(ledger: Mapping[str, Any], source_creator_ledger: Mapping[str, Any]) -> None:
    """Verify source-owned fields in the static ledger rebuild from the source ledger."""
    validate_youtube_creator_observation_ledger(ledger)
    wrapper = _wrapper(ledger)
    source_creators = source_creator_ledger.get("creators")
    if not _is_list(source_creators):
        _fail("invalid_source_creator_ledger", "source creator ledger must contain a creators list")
    _validate_source_input_hashes(wrapper)
    observations = wrapper["creator_observations"]
    if len(observations) != len(source_creators):
        _fail("source_rebuild_row_count_mismatch", "ledger row count does not match source creators")
    for index, (observation, source) in enumerate(zip(observations, source_creators, strict=True)):
        if not isinstance(source, Mapping):
            _fail("invalid_source_creator_row", f"source creators[{index}] must be a mapping")
        _assert_equal(observation["creator_handle_query"], source["creator_handle_query"], "creator_handle_query")
        _assert_equal(observation["creator_classification"], source["creator_classification"], "creator_classification")
        _assert_source_subject_key(observation, source)
        _assert_equal(observation["admitted_video_count"], source["admitted_rows_total"], "admitted_video_count")
        _assert_equal(observation["observed_author_names"], source["observed_author_names"], "observed_author_names")
        _assert_equal(
            observation["source_observed_channel_ids"],
            source["observed_channel_ids"],
            "source_observed_channel_ids",
        )
        _assert_equal(observation["source_artifact_counts"], source["source_artifact_counts"], "source_artifact_counts")
        _assert_equal(observation["pool_ids"], source["pool_ids"], "pool_ids")
        _assert_equal(observation["video_ids"], source["video_ids"], "video_ids")
        _assert_equal(observation["sample_shorts_urls"], source["sample_shorts_urls"], "sample_shorts_urls")
        _assert_equal(observation["transcript_word_count_min"], source["word_count_min"], "word_count_min")
        _assert_equal(observation["transcript_word_count_max"], source["word_count_max"], "word_count_max")
        _assert_equal(
            observation["known_label_status_counts_100_pool_only"],
            source["known_label_status_counts_100_pool_only"],
            "known_label_status_counts_100_pool_only",
        )
        _assert_equal(
            observation["unlabeled_rows_in_pool200"],
            source["unlabeled_rows_in_pool200"],
            "unlabeled_rows_in_pool200",
        )
        expected_pointer = f"docs/review-inputs/youtube_shorts_fragrance_creator_ledger_v0.json#/creators/{index}"
        _assert_equal(observation["handle_source_pointer"], expected_pointer + "/creator_handle_query", "handle_source_pointer")
        _assert_equal(observation["display_name_source_pointer"], expected_pointer + "/observed_author_names", "display_name_source_pointer")
        _assert_equal(observation["video_membership_source_pointer"], expected_pointer + "/video_ids", "video_membership_source_pointer")


def validate_youtube_creator_observation_ledger_against_live_lake(
    ledger: Mapping[str, Any], data_root: str | Path
) -> None:
    """Read-only reconciliation against an external Forseti data root."""
    validate_youtube_creator_observation_ledger(ledger)
    wrapper = _wrapper(ledger)
    root = Path(data_root)
    primary_marker_path = root / ROOT_MARKER_FILENAME
    legacy_marker_path = root / LEGACY_ROOT_MARKER_FILENAME
    marker_path = primary_marker_path if primary_marker_path.is_file() else legacy_marker_path
    if not marker_path.is_file():
        _fail(
            "live_lake_marker_missing",
            f"missing data-root marker: {primary_marker_path} (legacy fallback: {legacy_marker_path})",
        )
    marker = json.loads(marker_path.read_text(encoding="utf-8"))
    expected_uuid = _source_root_uuid(wrapper)
    if marker.get("root_uuid") != expected_uuid:
        _fail("live_lake_root_uuid_mismatch", "data-root marker UUID does not match ledger source input")
    for observation in wrapper["creator_observations"]:
        for ref in observation["data_lake_packet_refs"]:
            packet_dir = root / ref["packet_relpath"]
            manifest_path = packet_dir / "manifest.json"
            metadata_path = root / ref["metadata_relpath"]
            if not manifest_path.is_file():
                _fail("live_lake_manifest_missing", f"missing manifest for {ref['packet_id']}")
            if not metadata_path.is_file():
                _fail("live_lake_metadata_missing", f"missing metadata for {ref['packet_id']}")
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
            _assert_live_equal(manifest.get("packet_id"), ref["packet_id"], "live_lake_manifest_packet_id")
            _assert_live_equal(manifest.get("source_family"), "youtube", "live_lake_source_family")
            _assert_live_equal(manifest.get("source_surface"), ref["source_surface"], "live_lake_source_surface")
            _assert_live_equal(metadata.get("platform_video_id"), ref["video_id"], "live_lake_platform_video_id")
            _assert_live_equal(metadata.get("channel_id"), ref["channel_id_or_none"], "live_lake_channel_id")


def _validate_source_inputs(value: Any) -> None:
    if not _is_list(value) or not value:
        _fail("invalid_source_inputs", "source_inputs must be a non-empty list")
    for source_input in value:
        if not isinstance(source_input, Mapping):
            _fail("invalid_source_input", "source_inputs entries must be mappings")
        _reject_unknown_keys(source_input, _ALLOWED_SOURCE_INPUT_KEYS, "source_input")
        _require(source_input, ("source_pointer", "role"), "source_input")
        if "sha256" in source_input and not _SHA256_RE.fullmatch(str(source_input["sha256"])):
            _fail("invalid_source_input_sha256", "source_input sha256 must be lowercase hex sha256")


def _validate_niche_scope(value: Any) -> None:
    if not isinstance(value, Mapping):
        _fail("invalid_niche_scope", "niche_scope must be a mapping")
    _reject_unknown_keys(value, _ALLOWED_NICHE_KEYS, "niche_scope")
    _require(value, tuple(_ALLOWED_NICHE_KEYS), "niche_scope")


def _validate_metric_policy(value: Any) -> None:
    if not isinstance(value, Mapping):
        _fail("invalid_metric_rollup_policy", "metric_rollup_policy must be a mapping")
    _reject_unknown_keys(value, _ALLOWED_METRIC_POLICY_KEYS, "metric_rollup_policy")
    _require(value, tuple(_ALLOWED_METRIC_POLICY_KEYS), "metric_rollup_policy")
    if value["current_status"] != "not_present_in_current_caption_audio_lake_packets":
        _fail("invalid_metric_rollup_status", "metric rollups must remain absent for this seed ledger")
    if value["do_not_store_absence_as_zero"] is not True:
        _fail("metric_absence_zero_forbidden", "metric absence must not be represented as zero")


def _validate_observations(value: Any) -> list[Mapping[str, Any]]:
    if not _is_list(value):
        _fail("invalid_creator_observations", "creator_observations must be a list")
    observations: list[Mapping[str, Any]] = []
    observation_ids: set[str] = set()
    video_ids: list[str] = []
    packet_ids: list[str] = []
    for observation in value:
        if not isinstance(observation, Mapping):
            _fail("invalid_creator_observation", "creator_observation entries must be mappings")
        _reject_unknown_keys(observation, _ALLOWED_OBSERVATION_KEYS, "creator_observation")
        _require(observation, tuple(_ALLOWED_OBSERVATION_KEYS), "creator_observation")
        observation_id = str(observation["creator_observation_id"])
        if observation_id in observation_ids:
            _fail("duplicate_creator_observation_id", f"duplicate creator_observation_id: {observation_id}")
        observation_ids.add(observation_id)
        if observation["platform"] != "youtube":
            _fail("invalid_platform", "YouTube creator observation rows must use platform=youtube")
        if observation["platform_subject_key_type"] != "youtube_channel_id":
            _fail("invalid_platform_subject_key_type", "platform_subject_key_type must be youtube_channel_id")
        if observation["creator_classification"] not in _ALLOWED_CREATOR_CLASSIFICATIONS:
            _fail("invalid_creator_classification", "creator_classification is not allowed")
        subject_key = str(observation["platform_subject_key"])
        if not subject_key.startswith("UC"):
            _fail("invalid_youtube_channel_id", "platform_subject_key must be a YouTube channel id")
        _validate_public_profile_url(observation["public_profile_url"], subject_key)
        _validate_non_empty_str(observation["identity_boundary"], "identity_boundary")
        _validate_non_empty_str(observation["niche_scope"], "observation_niche_scope")
        _validate_required_non_claims(observation["non_claims"], "creator_observation")
        row_video_ids = _validate_str_list(observation["video_ids"], "video_ids", allow_empty=False)
        if len(row_video_ids) != observation["admitted_video_count"]:
            _fail("admitted_count_mismatch", "admitted_video_count must match video_ids length")
        if len(row_video_ids) != len(set(row_video_ids)):
            _fail("duplicate_video_id_in_row", "video_ids must be unique within a row")
        refs = _validate_packet_refs(observation, row_video_ids)
        video_ids.extend(row_video_ids)
        packet_ids.extend(str(ref["packet_id"]) for ref in refs)
        observations.append(observation)
    if len(video_ids) != len(set(video_ids)):
        _fail("duplicate_video_id_across_ledger", "video_ids must be unique across the ledger")
    if len(packet_ids) != len(set(packet_ids)):
        _fail("duplicate_packet_id_across_ledger", "data_lake packet ids must be unique across the ledger")
    return observations


def _validate_packet_refs(observation: Mapping[str, Any], row_video_ids: Sequence[str]) -> list[Mapping[str, Any]]:
    refs = observation["data_lake_packet_refs"]
    if not _is_list(refs):
        _fail("invalid_packet_refs", "data_lake_packet_refs must be a list")
    if len(refs) != len(row_video_ids):
        _fail("packet_ref_count_mismatch", "data_lake_packet_refs must align one-to-one with video_ids")
    subject_key = str(observation["platform_subject_key"])
    resolved_counter: Counter[str] = Counter()
    missing_channel = 0
    for expected_video_id, ref in zip(row_video_ids, refs, strict=True):
        if not isinstance(ref, Mapping):
            _fail("invalid_packet_ref", "data_lake_packet_refs entries must be mappings")
        _reject_unknown_keys(ref, _ALLOWED_PACKET_REF_KEYS, "data_lake_packet_ref")
        _require(ref, tuple(_ALLOWED_PACKET_REF_KEYS), "data_lake_packet_ref")
        _assert_equal(ref["video_id"], expected_video_id, "packet_ref_video_alignment")
        if not _PACKET_ID_RE.fullmatch(str(ref["packet_id"])):
            _fail("invalid_packet_id", "packet_id must be a Crockford-26 lake packet id")
        if not _RAW_RELPATH_RE.fullmatch(str(ref["packet_relpath"])):
            _fail("invalid_packet_relpath", "packet_relpath must be raw/<shard>/<packet_id>")
        if not _METADATA_RELPATH_RE.fullmatch(str(ref["metadata_relpath"])):
            _fail("invalid_metadata_relpath", "metadata_relpath must be raw/<shard>/<packet_id>/raw/<nn>_*_metadata.json")
        if ref["source_surface"] not in _ALLOWED_SOURCE_SURFACES:
            _fail("invalid_source_surface", "source_surface must be youtube_captions or youtube_audio")
        channel_id = ref["channel_id_or_none"]
        if channel_id is None:
            missing_channel += 1
        elif channel_id != subject_key:
            _fail("packet_ref_channel_mismatch", "packet ref channel_id must match row platform_subject_key")
        else:
            resolved_counter[str(channel_id)] += 1
    expected_resolved = sorted(
        [
            {"channel_id": channel_id, "count": count}
            for channel_id, count in resolved_counter.items()
        ],
        key=lambda item: item["channel_id"],
    )
    _assert_equal(observation["resolved_lake_channel_ids"], expected_resolved, "resolved_lake_channel_ids")
    _assert_equal(observation["lake_channel_id_missing_video_count"], missing_channel, "lake_channel_id_missing_video_count")
    return list(refs)


def _validate_counts(counts: Any, observations: Sequence[Mapping[str, Any]]) -> None:
    if not isinstance(counts, Mapping):
        _fail("invalid_counts", "counts must be a mapping")
    _reject_unknown_keys(counts, _ALLOWED_COUNTS_KEYS, "counts")
    _require(counts, tuple(_ALLOWED_COUNTS_KEYS), "counts")
    all_video_ids = [video_id for row in observations for video_id in row["video_ids"]]
    all_refs = [ref for row in observations for ref in row["data_lake_packet_refs"]]
    _assert_equal(counts["creator_observations_total"], len(observations), "creator_observations_total")
    _assert_equal(counts["source_pool_rows_total"], len(all_video_ids), "source_pool_rows_total")
    _assert_equal(counts["unique_video_ids"], len(set(all_video_ids)), "unique_video_ids")
    _assert_equal(counts["data_lake_youtube_packets_matched"], len(all_refs), "data_lake_youtube_packets_matched")
    _assert_equal(
        counts["data_lake_youtube_caption_packets"],
        sum(1 for ref in all_refs if ref["source_surface"] == "youtube_captions"),
        "data_lake_youtube_caption_packets",
    )
    _assert_equal(
        counts["data_lake_youtube_audio_packets"],
        sum(1 for ref in all_refs if ref["source_surface"] == "youtube_audio"),
        "data_lake_youtube_audio_packets",
    )
    _assert_equal(
        counts["unique_youtube_channel_ids"],
        len({row["platform_subject_key"] for row in observations}),
        "unique_youtube_channel_ids",
    )
    _assert_equal(
        counts["video_channel_id_missing_in_lake_metadata"],
        sum(1 for ref in all_refs if ref["channel_id_or_none"] is None),
        "video_channel_id_missing_in_lake_metadata",
    )
    classifications = Counter(str(row["creator_classification"]) for row in observations)
    _assert_equal(
        counts["creator_or_channel_observed"],
        classifications["creator_or_channel_observed"],
        "creator_or_channel_observed",
    )
    _assert_equal(
        counts["brand_or_platform_account_observed"],
        classifications["brand_or_platform_account_observed"],
        "brand_or_platform_account_observed",
    )



def _validate_source_input_hashes(wrapper: Mapping[str, Any]) -> None:
    for source_input in wrapper["source_inputs"]:
        sha256 = source_input.get("sha256")
        if sha256 is None:
            continue
        source_pointer = str(source_input["source_pointer"])
        source_path = _resolve_repo_relative_path(source_pointer)
        if source_path is None:
            _fail("source_input_hash_file_missing", f"source input is not a local file: {source_pointer}")
        actual = hashlib.sha256(_read_source_input_bytes(source_pointer, source_path)).hexdigest()
        if actual != sha256:
            _fail("source_input_hash_mismatch", f"source input sha256 mismatch for {source_pointer}")


def _read_source_input_bytes(source_pointer: str, source_path: Path) -> bytes:
    if Path(source_pointer).is_absolute():
        return source_path.read_bytes()
    try:
        root_result = subprocess.run(
            ["git", "-C", str(source_path.parent), "rev-parse", "--show-toplevel"],
            check=True,
            capture_output=True,
        )
        repo_root = Path(root_result.stdout.decode("utf-8").strip()).resolve()
        relpath = source_path.resolve().relative_to(repo_root).as_posix()
        return subprocess.run(
            ["git", "-C", str(repo_root), "cat-file", "blob", f"HEAD:{relpath}"],
            check=True,
            capture_output=True,
        ).stdout
    except (OSError, subprocess.SubprocessError, UnicodeDecodeError, ValueError):
        return source_path.read_bytes()


def _resolve_repo_relative_path(source_pointer: str) -> Path | None:
    candidate = Path(source_pointer)
    if candidate.is_absolute():
        return candidate if candidate.is_file() else None
    roots = [Path.cwd(), *Path.cwd().parents, Path(__file__).resolve().parents[3]]
    for root in roots:
        path = root / source_pointer
        if path.is_file():
            return path
    return None


def _assert_source_subject_key(observation: Mapping[str, Any], source: Mapping[str, Any]) -> None:
    observed = source.get("observed_channel_ids")
    if not _is_list(observed):
        _fail("invalid_source_creator_row", "source observed_channel_ids must be a list")
    source_channel_ids = {
        str(item.get("channel_id"))
        for item in observed
        if isinstance(item, Mapping) and item.get("channel_id") not in (None, "UNKNOWN")
    }
    subject_key = str(observation["platform_subject_key"])
    if subject_key not in source_channel_ids:
        _fail("source_platform_subject_key_mismatch", "platform_subject_key must match a source observed channel id")


def _validate_public_profile_url(value: Any, subject_key: str) -> None:
    expected = f"https://www.youtube.com/channel/{subject_key}"
    if value != expected:
        _fail("invalid_public_profile_url", f"public_profile_url must be {expected}")


def _validate_non_empty_str(value: Any, context: str) -> str:
    if not isinstance(value, str) or not value.strip():
        _fail(f"invalid_{context}", f"{context} must be a non-empty string")
    return value


def _assert_no_youtube_forbidden_output_fields(value: Any, *, path: str = "$") -> None:
    if isinstance(value, Mapping):
        for key, child in value.items():
            key_name = str(key)
            if key_name.lower() in _YOUTUBE_FORBIDDEN_OUTPUT_FIELDS:
                _fail("forbidden_youtube_observation_field", f"forbidden YouTube observation field at {path}.{key_name}")
            _assert_no_youtube_forbidden_output_fields(child, path=f"{path}.{key_name}")
        return
    if _is_list(value):
        for index, child in enumerate(value):
            _assert_no_youtube_forbidden_output_fields(child, path=f"{path}[{index}]")


def _source_root_uuid(wrapper: Mapping[str, Any]) -> str:
    for source_input in wrapper["source_inputs"]:
        if "root_uuid" in source_input:
            return str(source_input["root_uuid"])
    _fail("missing_source_root_uuid", "ledger source_inputs must include data-lake root_uuid")


def _wrapper(ledger: Mapping[str, Any]) -> Mapping[str, Any]:
    wrapper = ledger.get(_WRAPPER_KEY)
    if not isinstance(wrapper, Mapping):
        _fail("missing_ledger_wrapper", f"{_WRAPPER_KEY} wrapper is required")
    return wrapper


def _validate_operator_video_retirements(
    wrapper: Mapping[str, Any], observations: Sequence[Mapping[str, Any]]
) -> None:
    """Fail-closed validation of the optional operator retirement block: every
    entry names an admitted-pool video exactly once, carries an attested reason
    plus dead-capture evidence packet ids, and never masquerades as removal --
    the compiled observations keep the video; producers exclude it loudly."""
    block = wrapper.get("operator_video_retirements")
    if block is None:
        return
    if not _is_list(block) or not block:
        _fail(
            "invalid_operator_video_retirements",
            "operator_video_retirements must be a non-empty list when present",
        )
    pool: set[str] = set()
    for observation in observations:
        pool.update(observation["video_ids"])
    seen: set[str] = set()
    for index, entry in enumerate(block):
        context = f"operator_video_retirements[{index}]"
        if not isinstance(entry, Mapping):
            _fail("invalid_operator_video_retirement", f"{context} must be an object")
        _reject_unknown_keys(entry, _ALLOWED_RETIREMENT_KEYS, context)
        _require(entry, tuple(sorted(_ALLOWED_RETIREMENT_KEYS)), context)
        video_id = entry["video_id"]
        if not isinstance(video_id, str) or not _VIDEO_ID_RE.fullmatch(video_id):
            _fail("invalid_retirement_video_id", f"{context} video_id must be an 11-char YouTube id")
        if video_id in seen:
            _fail("duplicate_retirement_video_id", f"{context} duplicates retirement for {video_id}")
        seen.add(video_id)
        if video_id not in pool:
            _fail(
                "retirement_video_not_in_pool",
                f"{context} names a video outside the admitted pool: {video_id}",
            )
        reason = entry["reason"]
        if not isinstance(reason, str) or not reason.strip():
            _fail("invalid_retirement_reason", f"{context} reason must be a non-empty string")
        retired_at = entry["retired_at_utc"]
        if not isinstance(retired_at, str) or not _UTC_TIMESTAMP_RE.fullmatch(retired_at):
            _fail(
                "invalid_retirement_timestamp",
                f"{context} retired_at_utc must be an ISO-8601 UTC timestamp ending in Z",
            )
        evidence = entry["evidence_packet_ids"]
        if not _is_list(evidence) or not evidence:
            _fail(
                "invalid_retirement_evidence",
                f"{context} evidence_packet_ids must be a non-empty list",
            )
        for packet_id in evidence:
            if not isinstance(packet_id, str) or not _PACKET_ID_RE.fullmatch(packet_id):
                _fail(
                    "invalid_retirement_evidence",
                    f"{context} evidence_packet_ids entries must be ULID packet ids",
                )


def _reject_unknown_keys(value: Mapping[str, Any], allowed: frozenset[str], context: str) -> None:
    unknown = sorted(set(str(key) for key in value) - allowed)
    if unknown:
        _fail("unknown_field", f"unknown field(s) in {context}: {', '.join(unknown)}")


def _require(value: Mapping[str, Any], keys: Sequence[str], context: str) -> None:
    for key in keys:
        if key not in value:
            _fail(f"missing_{key}", f"{context} missing required field: {key}")


def _validate_str_list(value: Any, context: str, *, allow_empty: bool) -> list[str]:
    if not _is_list(value) or (not allow_empty and not value):
        _fail(f"invalid_{context}", f"{context} must be a list")
    result: list[str] = []
    for item in value:
        if not isinstance(item, str) or not item.strip():
            _fail(f"invalid_{context}", f"{context} entries must be non-empty strings")
        result.append(item)
    return result


def _validate_required_non_claims(value: Any, context: str) -> None:
    claims = set(_validate_str_list(value, f"{context}_non_claims", allow_empty=False))
    required = {"not cross-platform identity linkage", "not metric rollup"}
    missing = sorted(required - claims)
    if missing:
        _fail("missing_required_non_claim", f"{context} missing non-claim(s): {', '.join(missing)}")


def _assert_equal(actual: Any, expected: Any, context: str) -> None:
    if actual != expected:
        _fail("source_rebuild_mismatch", f"{context} mismatch: expected {expected!r}, got {actual!r}")


def _assert_live_equal(actual: Any, expected: Any, context: str) -> None:
    if actual != expected:
        _fail("live_lake_metadata_mismatch", f"{context} mismatch: expected {expected!r}, got {actual!r}")


def _is_list(value: Any) -> bool:
    return isinstance(value, list)


def _fail(code: str, message: str) -> None:
    raise YoutubeCreatorObservationLedgerError(code, message)
