"""Version-bump gate: derivation-policy modules cannot change silently.

Every consumption-seam obligation envelope enumerates version tokens (and
named constants) whose job is to re-surface committed packets when policy
changes. But the tokens only work if humans remember to bump them — until now
that discipline was COMMENT-BOUND (the standing residual named in every
catch-up adjudication: change ``cleaning/fragrantica.py`` internals without
bumping a version and no packet ever re-derives).

This gate makes the discipline mechanical: each derivation-policy module's
LF-normalized source hash is pinned here. Changing a pinned module fails CI
with a directed ritual instead of drifting silently:

1. Decide whether the change is OUTPUT-SHAPING (could any derived byte,
   selection, status, or ack fingerprint differ for the same committed raw?).
2. If output-shaping: bump the module's version token(s) named below — that
   re-fingerprints obligations and re-surfaces every committed packet, which
   is exactly the seam's S3 behavior.
3. Update the pin here either way, stating the decision in the commit.

Deliberately noisy: every change to these modules forces the conscious
decision that comments used to beg for. Modules pinned = the implementation
modules of every derivation whose version tokens appear in a
``_packet_obligation`` envelope (plus ``fragrance_review_lake.py`` and
``transcript_product_lake.py``, whose projection/write internals currently
ride sibling tokens — the named weak-envelope residuals).
"""
from __future__ import annotations

import hashlib

from data_lake.inventory import HARNESS_ROOT as _HARNESS_ROOT

# module path -> (version token(s) the changer must consider, pinned sha256 of
# LF-normalized source bytes).
POLICY_MODULE_PINS: dict[str, tuple[tuple[str, ...], str]] = {
    "cleaning/basenotes.py": (
        ("BASENOTES_CLEANING_METHOD_ID (cleaning/basenotes_lake.py)",),
        "947303e81e95122488bd7ad4c9577503881cb663b1a5f77b63ad792209658333",
    ),
    "cleaning/basenotes_lake.py": (
        (
            "BASENOTES_AUDIT_PACK_PRODUCER_SCHEMA_VERSION",
            "BASENOTES_SILVER_PRODUCER_SCHEMA_VERSION",
            "BASENOTES_CLEANING_METHOD_ID",
        ),
        "10ac91ef30c17551210f5278baed2675abb54554e3010aa0e525d0e8b344d996",
    ),
    "cleaning/fragrantica.py": (
        ("FRAGRANTICA_CLEANING_METHOD_ID (cleaning/fragrantica_lake.py)",),
        "21a0f124bd42972285eb1cea7a07861bf79cf2dcda4819d612762481d220d1b7",
    ),
    "cleaning/fragrantica_lake.py": (
        (
            "FRAGRANTICA_AUDIT_PACK_PRODUCER_SCHEMA_VERSION",
            "FRAGRANTICA_SILVER_PRODUCER_SCHEMA_VERSION",
            "FRAGRANTICA_SILVER_METRIC_PRODUCER_SCHEMA_VERSION",
            "FRAGRANTICA_CLEANING_METHOD_ID",
        ),
        "f6a9696607c14daf4ef62590a7fc2d528812a73bd0d9e10b99ff7a51927353f2",
    ),
    "cleaning/models.py": (
        ("CLEANING_CORE_VERSION",),
        "3b0c4858333d1bb04937b95ced0e154aa05f5d82b3db56af95732ae85a9009f0",
    ),
    "cleaning/parfumo.py": (
        ("PARFUMO_RATING_CARRY_RULE", "PARFUMO_CLEANING_METHOD_ID (cleaning/parfumo_lake.py)"),
        "65a13d65228ed78737664d023a6d498b8703a294dc133ee0db7d6035cd6a1e32",
    ),
    "cleaning/parfumo_lake.py": (
        (
            "PARFUMO_AUDIT_PACK_PRODUCER_SCHEMA_VERSION",
            "PARFUMO_SILVER_PRODUCER_SCHEMA_VERSION",
            "PARFUMO_SILVER_METRIC_PRODUCER_SCHEMA_VERSION",
            "PARFUMO_CLEANING_METHOD_ID",
        ),
        "5f4465e262424ea9a6c288037adf861ee06354068714668e3dfd91fb906d3cf7",
    ),
    "cleaning/transcript_product_extractor.py": (
        ("EXTRACTOR_RUBRIC_VERSION",),
        "2301b2977bfcdeaa5963bc4e30b0b4c6adcc6d76075d8dda0d9351eb08d4d08c",
    ),
    "cleaning/transcript_product_lake.py": (
        ("EXTRACTOR_RUBRIC_VERSION (cleaning/transcript_product_extractor.py)", "PRODUCT_MENTIONS_RECORD_SCHEMA_VERSION (record-shape token; weak-envelope residual closed)"),
        "5e26f61b50082dd214ae6f2fe756308607a06009c09c84b33f9c95be1f2fddf4",
    ),
    "ecr/deriver.py": (
        ("ECR_DERIVER_VERSION",),
        "b94920e25627537b1cca0503cad52130982de3f5d9a53122e14978912b27b273",
    ),
    "source_capture/basenotes_projection.py": (
        ("BASENOTES_PROJECTION_VERSION",),
        "e3daca78e9dc238844d6452a93a16728fb6b6e8f0e4be936df3e1a98e2ffa2da",
    ),
    "source_capture/fragrance_review_coverage.py": (
        ("FRAGRANCE_REVIEW_COVERAGE_VERSION", "FRAGRANCE_REVIEW_RECORD_SCHEMA_VERSION (record-shape token; weak-envelope residual closed)"),
        "b98de11e2a67abe4fd75c048926ba2b3e95b3dddfc9446a20cdef93adb6a1bad",
    ),
    "source_capture/fragrance_review_lake.py": (
        ("FRAGRANCE_REVIEW_COVERAGE_VERSION (source_capture/fragrance_review_coverage.py; weak-envelope residual)",),
        "f5eeaf437d3e71cab942315228391a238fce923bdae4a935018f6d97508ac089",
    ),
    "source_capture/fragrantica_projection.py": (
        ("FRAGRANTICA_PROJECTION_VERSION",),
        "141df55675bb97ff5e2efabab9789dc2ce4b2a934c15a6feabf4bf3ba9f7f04f",
    ),
    "source_capture/ig_reels_grid_projection.py": (
        ("IG_REELS_PROJECTION_VERSION",),
        "6ad096feefc6e992c56135f87f6f343da9b3d05d895fd30c0435b3862ade1729",
    ),
    "source_capture/parfumo_projection.py": (
        ("PARFUMO_PROJECTION_VERSION",),
        "cb2759c216c9f2561778eac0fa2cfeece23870914a4a5d57e3931eb0d4dc422e",
    ),
    "source_capture/transcript/asr_packet.py": (
        ("transcriber_policy envelope (run_asr_transcript_catchup)", "TRANSCRIPT_ASR_RECORD_SCHEMA_VERSION (record-shape token; weak-envelope residual closed)"),
        "4d99991d5b27c82b8c22981dcddaa2ebd516249cab706e1016ea9379c44bb21e",
    ),
    "source_capture/transcript/audio_asr.py": (
        ("transcriber_policy envelope defaults (model/compute/decode params are CLI-enveloped)",),
        "1b74a9d9df8e111edee05f3350edca1de75f422cdb95715de310c43652a047d6",
    ),
    "source_capture/transcript/ig_reels_audio_packet.py": (
        ("transcriber_policy envelope (run_asr_transcript_catchup)", "TRANSCRIPT_ASR_RECORD_SCHEMA_VERSION (record-shape token, shared from asr_packet.py; weak-envelope residual closed)"),
        "e28bafa6c049d42fb115c52518c6a11d2d666bed386f518964b402589585502a",
    ),
}

# Record-shape schema tokens close the weak-envelope class only if they are
# actually stamped into newly written records. The module hash pins above force a
# conscious bump/no-bump decision, but this direct guard catches a pin update that
# accidentally drops the payload field itself.
RECORD_SCHEMA_TOKEN_FIELD_SITES: dict[str, tuple[str, ...]] = {
    "cleaning/transcript_product_lake.py": (
        'PRODUCT_MENTIONS_RECORD_SCHEMA_VERSION = "transcript_product_mentions_record_v0"',
        '"record_schema_version": PRODUCT_MENTIONS_RECORD_SCHEMA_VERSION',
    ),
    "source_capture/fragrance_review_coverage.py": (
        'FRAGRANCE_REVIEW_RECORD_SCHEMA_VERSION = "fragrance_review_coverage_record_v0"',
        'record_schema_version: Literal["fragrance_review_coverage_record_v0"]',
        "FRAGRANCE_REVIEW_RECORD_SCHEMA_VERSION",
    ),
    "source_capture/transcript/asr_packet.py": (
        'TRANSCRIPT_ASR_RECORD_SCHEMA_VERSION = "transcript_asr_record_v0"',
        '"record_schema_version": TRANSCRIPT_ASR_RECORD_SCHEMA_VERSION',
    ),
    "source_capture/transcript/ig_reels_audio_packet.py": (
        "from source_capture.transcript.asr_packet import TRANSCRIPT_ASR_RECORD_SCHEMA_VERSION",
        '"record_schema_version": TRANSCRIPT_ASR_RECORD_SCHEMA_VERSION',
    ),
}

def _lf_sha256(relative_path: str) -> str:
    data = (_HARNESS_ROOT / relative_path).read_bytes().replace(b"\r\n", b"\n")
    return hashlib.sha256(data).hexdigest()


def test_record_schema_tokens_are_stamped_by_writers() -> None:
    missing = {}
    for module_path, required_tokens in sorted(RECORD_SCHEMA_TOKEN_FIELD_SITES.items()):
        source = (_HARNESS_ROOT / module_path).read_text(encoding="utf-8")
        missing_tokens = [token for token in required_tokens if token not in source]
        if missing_tokens:
            missing[module_path] = missing_tokens

    assert not missing, (
        "Record-shape schema token(s) are declared in a policy-pinned module but "
        "are no longer stamped into the record payload/model field. Restore the "
        "record_schema_version write or remove the weak-envelope closure claim: "
        f"{missing}"
    )

def test_policy_modules_match_their_pins() -> None:
    drifted = {}
    for module_path, (version_tokens, pinned) in sorted(POLICY_MODULE_PINS.items()):
        actual = _lf_sha256(module_path)
        if actual != pinned:
            drifted[module_path] = {"pinned": pinned, "actual": actual, "consider": version_tokens}

    assert not drifted, (
        "Derivation-policy module(s) changed. This is not (necessarily) wrong — but the "
        "version-bump decision may no longer be skipped:\n"
        "  1. Is the change OUTPUT-SHAPING (any derived byte / selection / ack fingerprint "
        "could differ for the same committed raw)?\n"
        "  2. If yes: bump the version token(s) listed under 'consider' so committed "
        "packets re-surface (seam S3 behavior).\n"
        "  3. Update the pin here either way and state the decision in the commit body.\n"
        f"{drifted}"
    )


def test_pinned_modules_exist() -> None:
    missing = [
        module_path
        for module_path in POLICY_MODULE_PINS
        if not (_HARNESS_ROOT / module_path).is_file()
    ]
    assert not missing, (
        "POLICY_MODULE_PINS lists module(s) that no longer exist — a retired policy module "
        f"needs its pin retired deliberately, with its lane's disposition: {missing}"
    )
