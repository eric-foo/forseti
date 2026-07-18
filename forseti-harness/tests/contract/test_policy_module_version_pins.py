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
    "capture_spine/creator_profile_current/tiktok_comment_attention_producer.py": (
        (
            "COMMENT_ATTENTION_RECIPE_VERSION",
            "COMMENT_ATTENTION_PRODUCER_SCHEMA_VERSION",
            "COMMENT_ATTENTION_POLICY_FINGERPRINT",
        ),
        # Output-shaping: temporal pairing, amplification/rank context, and the
        # cid-less mechanics fix now ride the producer's v1 recipe/schema tokens.
        "38def9d04a913acd1818be5194d23122f51c182ca0f59bfdf0859606b0e2dcd6",
    ),
    "capture_spine/creator_profile_current/tiktok_grid_observation_producer.py": (
        (
            "TIKTOK_GRID_OBSERVATION_POLICY_VERSION",
            "TIKTOK_GRID_OBSERVATION_PRODUCER_SCHEMA_VERSION",
            "TIKTOK_GRID_OBSERVATION_POLICY_FINGERPRINT",
            "TIKTOK_PROFILE_METRIC_OBSERVATION_POLICY_VERSION",
            "TIKTOK_PROFILE_METRIC_OBSERVATION_PRODUCER_SCHEMA_VERSION",
            "TIKTOK_PROFILE_METRIC_OBSERVATION_POLICY_FINGERPRINT",
        ),
        # Output-shaping profile v0 adds two deterministic exact-or-unavailable
        # account metric records; incumbent per-video set bytes remain unchanged.
        "30dae4e4fd3f51621ff6442498de89d48f5b0e7c7b064d31179fe49b8d02d905",
    ),
    "cleaning/_shared.py": (
        (
            "the cleaning method / producer schema tokens of all three cleaning "
            "lanes (fragrantica, parfumo, basenotes) -- shared helper home",
        ),
        # Initial pin: byte-identical helpers consolidated out of the three
        # cleaning adapters and *_lake modules; not output-shaping.
        # Pin bumped: raw_refs None-first sort key (bugfix -- mixed None/str ref
        # keys raised TypeError; previously-successful inputs order identically),
        # not output-shaping.
        "99aee399f1a989c50c3c100ad6aebd84daef3fcfaa6fb62dcc8ce4eddc182f0f",
    ),
    "cleaning/basenotes.py": (
        ("BASENOTES_CLEANING_METHOD_ID (cleaning/basenotes_lake.py)",),
        # Admission-shaping v1: user-cleared persistent Chrome replaces the retired proxy surface.
        # Pin bumped: byte-identical helper dedup onto cleaning/_shared.py; not output-shaping.
        "c1f3fa8e66d16551e585c734cb2fa76da1bf44f69a31499807104afb7794f734",
    ),
    "cleaning/basenotes_lake.py": (
        (
            "BASENOTES_AUDIT_PACK_PRODUCER_SCHEMA_VERSION",
            "BASENOTES_SILVER_PRODUCER_SCHEMA_VERSION",
            "BASENOTES_CLEANING_METHOD_ID",
        ),
        # Cleaning method v1 re-fingerprints obligations for the changed source admission.
        # Pin bumped: byte-identical helper dedup onto cleaning/_shared.py and
        # data_lake/canonical_json.py; not output-shaping.
        "a44fe51c0908f38b53a48092e12c9c4c1c75f0c2528941b18c60b3f4a98467ad",
    ),
    "cleaning/fragrantica.py": (
        ("FRAGRANTICA_CLEANING_METHOD_ID (cleaning/fragrantica_lake.py)",),
        # Output-shaping: projection-v1 residual names change raw-pull-required output;
        # the cleaning method token is bumped to v1.
        "a06d40ecb8c83bee8a8b1dad01c16b29a00c0a16270bd24038e2d45410975af4",
    ),
    "cleaning/fragrantica_lake.py": (
        (
            "FRAGRANTICA_AUDIT_PACK_PRODUCER_SCHEMA_VERSION",
            "FRAGRANTICA_SILVER_PRODUCER_SCHEMA_VERSION",
            "FRAGRANTICA_SILVER_METRIC_PRODUCER_SCHEMA_VERSION",
            "FRAGRANTICA_REVIEW_VOTE_POLICY_VERSION",
            "FRAGRANTICA_CLEANING_METHOD_ID",
        ),
        # Output-shaping: FRAGRANTICA_CLEANING_METHOD_ID v1 re-fingerprints
        # obligations for the projection-v1 residual vocabulary.
        "673cd8b2cd391345d154518bac6bf50a57f2f412ac80007415ee77ad208d3f16",
    ),
    "cleaning/models.py": (
        ("CLEANING_CORE_VERSION",),
        "3b0c4858333d1bb04937b95ced0e154aa05f5d82b3db56af95732ae85a9009f0",
    ),
    "cleaning/parfumo.py": (
        ("PARFUMO_RATING_CARRY_RULE", "PARFUMO_CLEANING_METHOD_ID (cleaning/parfumo_lake.py)"),
        # Pin bumped: byte-identical helper dedup onto cleaning/_shared.py; not output-shaping.
        "6f4c4cda538e94056eb124d6006c8e5c7ea4749df4fe4bfe22ec92d57009b176",
    ),
    "cleaning/parfumo_lake.py": (
        (
            "PARFUMO_AUDIT_PACK_PRODUCER_SCHEMA_VERSION",
            "PARFUMO_SILVER_PRODUCER_SCHEMA_VERSION",
            "PARFUMO_SILVER_METRIC_PRODUCER_SCHEMA_VERSION",
            "PARFUMO_CLEANING_METHOD_ID",
        ),
        # Pin bumped: byte-identical helper dedup onto cleaning/_shared.py and
        # data_lake/canonical_json.py; not output-shaping.
        "d19fd40113b4410530804fcadab0689db125885af9af058477deaf1a6fe59911",
    ),
    "cleaning/transcript_product_extractor.py": (
        ("EXTRACTOR_RUBRIC_VERSION",),
        # Import-only transport relocation; output-shaping rubric is unchanged.
        "45a1878754192b6cab344fc11d74770851e19c49f46741947e7ac3378136054f",
    ),
    "cleaning/transcript_product_lake.py": (
        ("EXTRACTOR_RUBRIC_VERSION (cleaning/transcript_product_extractor.py)", "PRODUCT_MENTIONS_RECORD_SCHEMA_VERSION (record-shape token; weak-envelope residual closed)"),
        # Output-shaping: the official Silver envelope is retained, while durable
        # record/completion identity now binds the full policy fingerprint; the
        # PRODUCT_MENTIONS_RECORD_SCHEMA_VERSION bump to v2 re-surfaces V1 records.
        "6885729bc1b5bee6b250ce2d40f4b3bd7ca66e225fbbc6cc3c6c5649dd1afbef",
    ),
    "ecr/deriver.py": (
        ("ECR_DERIVER_VERSION",),
        "b94920e25627537b1cca0503cad52130982de3f5d9a53122e14978912b27b273",
    ),
    "source_capture/basenotes_projection.py": (
        ("BASENOTES_PROJECTION_VERSION",),
        # Projection v1 rejects the retired proxy surface and admits the proven persistent-Chrome surface.
        # Pin bumped: helper dedup onto source_capture/projection_shared.py plus adoption of the
        # containment-guarded shared packet reader (security hardening: path traversal); not output-shaping.
        # Pin bumped: family-owned content-record schema/parser and JSON-pointer packet binding.
        # Raw/legacy row semantics remain equivalent, so BASENOTES_PROJECTION_VERSION stays v1;
        # content and parser behavior carry separate version constants.
        "b3f276b8ff5c0ba69be08db81e5b624428ce794b4087582d2436ad9fd331407e",
    ),
    "source_capture/fragrance_review_coverage.py": (
        ("FRAGRANCE_REVIEW_COVERAGE_VERSION", "FRAGRANCE_REVIEW_RECORD_SCHEMA_VERSION (record-shape token; weak-envelope residual closed)"),
        "df33ab6c6de41986fcc796fbb9b4e162884ef650796a25398cdd1597cc1b29fc",
    ),
    "source_capture/fragrance_review_lake.py": (
        ("FRAGRANCE_REVIEW_COVERAGE_VERSION (source_capture/fragrance_review_coverage.py; weak-envelope residual)",),
        "f5eeaf437d3e71cab942315228391a238fce923bdae4a935018f6d97508ac089",
    ),
    "source_capture/fragrantica_projection.py": (
        ("FRAGRANTICA_PROJECTION_VERSION",),
        # Output-shaping: projection v1 admits the two Fragrantica CloakBrowser
        # surfaces and tightens body selection plus residual vocabulary. The
        # family-owned content record adds parser-versioned retention and
        # JSON-pointer rebinding without another projection semantic change.
        "5568bffd0918e851c46b6983509daa3509d533593e1cd81352d782e92370bbab",
    ),
    "source_capture/ig_reels_grid_projection.py": (
        ("IG_REELS_PROJECTION_VERSION",),
        # Pin bumped: byte-identical _append_residual_once dedup onto
        # harness_utils.append_residual_once; not output-shaping.
        "cec6047919c73bc954b07ea15f3596929e511b11f851ed70177da6d58645aa11",
    ),
    "source_capture/parfumo_projection.py": (
        ("PARFUMO_PROJECTION_VERSION",),
        # Pin bumped: corrected a latent in-memory hash-basis literal; the anchor is
        # discarded before serialization, so projection outputs remain unchanged.
        "efb6592a166cb7aa8c064a05a68ab4d9213d7b62b8b3450f8262254a66408a1a",
    ),
    "source_capture/projection_shared.py": (
        (
            "the projection version tokens of its adopting surfaces "
            "(basenotes, fragrantica, parfumo, ig, reddit, retail grid, "
            "retail PDP) -- shared helper home",
        ),
        # Initial pin: byte-identical helpers consolidated out of the projection
        # surfaces; not output-shaping.
        # Pin bumped: added canonical_old_reddit_thread_url, the body adopted
        # from grid_projection's byte-identical private copy; not output-shaping.
        # Pin bumped: corrected the retained-copy docstring to distinguish the
        # byte-identical candidate-intake copy from the divergent screening copy
        # (post-merge review W6-1); docstring-only, not output-shaping.
        "ff04f0767731be27f81ccf1e420fe9d51c7c0b510173e9af73e53d071fd45675",
    ),
    "source_capture/transcript/asr_packet.py": (
        ("transcriber_policy envelope (run_asr_transcript_catchup)", "TRANSCRIPT_ASR_RECORD_SCHEMA_VERSION (record-shape token; weak-envelope residual closed)"),
        "4d99991d5b27c82b8c22981dcddaa2ebd516249cab706e1016ea9379c44bb21e",
    ),
    "source_capture/transcript/audio_asr.py": (
        ("transcriber_policy envelope defaults (model/compute/decode params are CLI-enveloped)",),
        # Pin bumped: added a bounded yt-dlp subprocess timeout (liveness guard). NOT output-shaping
        # -- only the hang-failure path changes; a successful bestaudio download derives identically.
        "9e778b107a3e3deec7fee83c0dc06b5cb7dc5a36e71e4d8c48393564abb98b09",
    ),
    "source_capture/transcript/ig_reels_audio_packet.py": (
        ("transcriber_policy envelope (run_asr_transcript_catchup)", "TRANSCRIPT_ASR_RECORD_SCHEMA_VERSION (record-shape token, shared from asr_packet.py; weak-envelope residual closed)"),
        # Pin bumped: added a bounded yt-dlp subprocess timeout (liveness guard). NOT output-shaping
        # -- only the hang-failure path changes; a successful Reel bestaudio download derives identically.
        "3f2bcd15d3f201fc30fe066d4ebfd0e6b2c592e7e7a85ad9209253095204ee57",
    ),
    "runners/run_tiktok_product_extract.py": (
        ("EXTRACTOR_RUBRIC_VERSION", "TikTok cue-normalization and packet-obligation policy"),
        # Output-shaping obligation change: record schema version now re-surfaces
        # packets for the envelope migration even when the extraction rubric is unchanged.
        "054645d4501ed6084197efa3e34620b54dda7bb80e22ab6dda7907e23cc5414e",
    ),
}

# Record-shape schema tokens close the weak-envelope class only if they are
# actually stamped into newly written records. The module hash pins above force a
# conscious bump/no-bump decision, but this direct guard catches a pin update that
# accidentally drops the payload field itself.
RECORD_SCHEMA_TOKEN_FIELD_SITES: dict[str, tuple[str, ...]] = {
    "cleaning/transcript_product_lake.py": (
        'PRODUCT_MENTIONS_RECORD_SCHEMA_VERSION = "transcript_product_mentions_record_v3"',
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
