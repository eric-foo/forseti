# IG Daily Heartbeat Runner Architecture Source Pack Manifest v0

```yaml
retrieval_header_version: 1
artifact_role: Review input - no-repo architecture source pack manifest
scope: >
  Manifest for the no-repo source bundle used with the IG daily heartbeat
  runner architecture planning prompt. Lists packed source files, hashes,
  source boundaries, and non-claims for external model couriering.
use_when:
  - Attaching source files to a no-repo architecture planning model.
  - Checking whether a returned no-repo architecture report used the intended source pack.
  - Rebuilding the no-repo zip for the v0 IG daily heartbeat architecture prompt.
authority_boundary: retrieval_only
open_next:
  - docs/prompts/architecture/ig_daily_heartbeat_runner_architecture_no_repo_prompt_v0.md
  - docs/prompts/architecture/ig_daily_heartbeat_runner_architecture_repo_access_prompt_v0.md
branch_or_commit: codex/ig-heartbeat-architecture-prompts @ 6d5db3d4
stale_if:
  - Any listed source file changes before the no-repo prompt is couriered.
  - The IG daily heartbeat operating policy or source-pack prompt receives a newer version.
```

## Purpose

This manifest belongs to the no-repo source pack for `ig_daily_heartbeat_runner_architecture_no_repo_prompt_v0.md`. It is a courier input, not architecture doctrine and not validation evidence.

The matching zip path is `docs/review-inputs/ig_daily_heartbeat_runner_architecture_no_repo_source_pack_v0.zip`. Inside the zip, this manifest is copied to `SOURCE_PACK_MANIFEST.md` and the source files preserve their repository-relative paths.

## Source Boundary

- Packed files only; no live repository access is assumed for the no-repo reviewer.
- Excludes credentials, cookies, browser storage state, proxy endpoints, public IPs, raw media bytes, ignored `_test_runs/`, and live network artifacts.
- Includes source files needed to reason about IG daily heartbeat policy, the existing IG grid/deep-capture primitives, Creator Registry/Silver boundaries, and relevant tests.
- Non-claims: not validation, not readiness, not live capture authorization, not account-safety proof, not platform permission, not implementation approval.

## Source Revision

- Branch: `codex/ig-heartbeat-architecture-prompts`
- HEAD: `6d5db3d48a16d5717f2cc68c64a451664f1e979a`
- Source policy baseline noted by prompts: `codex/ig-daily-heartbeat-policy @ 6d5db3d4`

## Packed Files

| Path | Size bytes | SHA256 |
| --- | ---: | --- |
| `AGENTS.md` | 9772 | `0ae058b6e0e3bc75e43c3e93e8a0251a5a777cb5b3e6dc522414aa9ae08ba641` |
| `.agents/workflow-overlay/README.md` | 2592 | `049403e4908c3ff5f0562893967897a4f754f2f771b843734d2dbca57059db11` |
| `.agents/workflow-overlay/decision-routing.md` | 12512 | `688aac653fce6aa5dbdd4d5050946509b998b1cac6421520408e029719895c1e` |
| `.agents/workflow-overlay/source-loading.md` | 36427 | `f25af717e382ba183ce35a3422dbec1b5fb7396312fdecd590e31f4ac53e5467` |
| `.agents/workflow-overlay/source-of-truth.md` | 21733 | `59fd7cebef40303ef2bae4a96ff938b21f84264105f4735a41ef5671b6825047` |
| `.agents/workflow-overlay/prompt-orchestration.md` | 54167 | `f471e2a263930edcf25fd0b3ac1f695b18277081810598c0c1cd06143179ee78` |
| `.agents/workflow-overlay/validation-gates.md` | 34214 | `236c8317cd247552dfbd002fdf4558030d88015a574ed6cba17b116db82ad432` |
| `.agents/workflow-overlay/artifact-folders.md` | 30659 | `a82f24c8290362ca2a07a8d50e107f714127dbdf9b8a4530f6c246e47fa61d44` |
| `.agents/workflow-overlay/artifact-roles.md` | 6266 | `d8348206f6209dc3c33cd96a192028cb037d3ed3c7225f859fd828741914775c` |
| `docs/prompts/templates/shared/forseti_preflight_defaults_v0.md` | 3561 | `8c10a4da1b5f3655753f8f905f8ec70e6f1d09a2572d4ee7540812d8395e0c4d` |
| `docs/workflows/forseti_repo_map_v0.md` | 139817 | `7877bcf397c27729158a8af1c681db134868dbf027838c7358429dfcee1b4521` |
| `forseti/product/spines/capture/core/source_families/social_media/instagram/README.md` | 4080 | `13427d74b9393a70b43932b52be3c3f1955fd2259c0a4d76b7ef74eaf886f01c` |
| `forseti/product/spines/capture/core/source_families/social_media/instagram/ig_daily_heartbeat_operating_policy_v0.md` | 9101 | `dce5831c1a9ba6f4e35c822c1c72e1103da8bba167df73bab182f75601c5569d` |
| `forseti/product/spines/capture/core/source_families/social_media/instagram/ig_creator_roster_frontier_ledger_spec_v0.md` | 28350 | `83384e128e65c321bc7d33ab38c2ff55bb69ff5b1015fffa7543ff8ca07825be` |
| `forseti/product/spines/capture/core/source_families/social_media/instagram/ig_at_scale_operating_envelope_v0.md` | 18040 | `10949f732fe20b4831ee9afdff75178e378976c22966931c33a00fc129c54520` |
| `forseti/product/spines/capture/core/source_families/social_media/instagram/forseti_creator_monitoring_policy_architecture_v0.md` | 15957 | `3fb1cab9a353626556b6fd17dcb531ed9e606aedd1554aca96aac2941261dedc` |
| `forseti/product/spines/capture/core/source_families/social_media/instagram/forseti_creator_momentum_pipeline_architecture_v0.md` | 11792 | `6b5286171c9bf094277110540df2243db09f30510c30531d37b256dd82aa319c` |
| `forseti/product/spines/capture/core/source_families/social_media/instagram/ig_profile_grid_dom_engagement_recon_and_spec_v0.md` | 29228 | `f181381f0cc11c35374314ec4842744fa6342a14ff25e43019271e51d5b4c211` |
| `forseti/product/spines/capture/core/source_families/social_media/instagram/ig_capture_shape_contract_spec_v0.md` | 18859 | `0a2d5a2b7b615b2a4996dafc3dc750b1208d4370b134143d3442abbf1b7d70c2` |
| `forseti/product/spines/capture/core/source_families/social_media/instagram/ig_capture_findings_consolidated_v0.md` | 15418 | `16d4a43a90a7127b385372e0f1932ac974cd6e4a3c2f8f344c214b9d30fb45bd` |
| `forseti/product/spines/capture/core/source_families/social_media/creator_registry/README.md` | 8814 | `146e3d47f045f5d2241d695cd9cff4316f5885ef38aa0a4a92b4dcbc78beebbe` |
| `forseti/product/spines/capture/core/source_families/social_media/creator_registry/creator_registry_index_v0.json` | 66622 | `86178cd789bcef60564919e7bb34e05d21e74a02feb2a2be583fcff10d03955e` |
| `forseti/product/spines/capture/core/source_families/social_media/creator_registry/creator_registry_index_spec_v0.md` | 5030 | `fa362fd5f4bdf9e693e104a2fc2f33f913115d566f98ca4893b13a6b732d434b` |
| `forseti/product/spines/capture/core/source_families/social_media/creator_registry/creator_profile_current_view_spec_v0.md` | 31316 | `932255a2e76de2b079e8e564bcb209d2a5ba998649914907e750d7ebe244e08c` |
| `forseti/product/spines/capture/core/source_families/social_media/creator_registry/creator_profile_current_record_contract_v0.md` | 17233 | `03630faf7ee3f98fccdf734afbe9109501c48f85c39c7dfe1774a14789461fa3` |
| `forseti/product/spines/capture/core/source_families/social_media/creator_registry/creator_profile_current_lake_native_record_mapping_v0.md` | 8978 | `4a62ae75baf754f2ffccc7df4611c0755a402b6b6ba2e63e8749d8dd3f9cc7c4` |
| `forseti/product/spines/capture/core/source_families/social_media/creator_registry/creator_metric_silver_record_contract_v0.md` | 7357 | `a082f4d86a7d8b8f87ec1218c11da46139c4a9edd6c35d75ab4f9d318d2a17ba` |
| `forseti-harness/runners/run_source_capture_ig_reels_grid_packet.py` | 35852 | `c5d3daffa148fbe33ad20830d3c8b26e8837ca70f462b772fdd9b7c7a5043d88` |
| `forseti-harness/source_capture/ig_reels_grid_capture.py` | 9996 | `94c2aa7ebbdda3a28d73021b4ba7782418c9de6f55d3667f5e00181fd8355ec4` |
| `forseti-harness/source_capture/ig_reels_grid.py` | 22429 | `53039f0bd4e26a24ec1addb940cb7ab7f26354668facde70d4cc1e1a669ce93d` |
| `forseti-harness/source_capture/ig_reels_grid_projection.py` | 43876 | `0d06be57c07c4e0f43add820add39bf951ee3b3b5f466c1a289377aed612768b` |
| `forseti-harness/runners/run_ig_reels_lane_orchestrator.py` | 25963 | `f9425f5417ecb0cf6da0e8e1dd30a8e100847b5ed6ed0df1a2eecd2f1274cf4b` |
| `forseti-harness/runners/run_source_capture_ig_reels_creator_deep_capture.py` | 18926 | `51072a21bce9e04b56a4a8aadf25549b0a61a4d9042105b11e94b9712af968ce` |
| `forseti-harness/runners/run_source_capture_ig_reels_deep_capture.py` | 12008 | `e2874ddecebbb2a479e325ae5aa5a8793075cee16aefdc3a09db351dface791a` |
| `forseti-harness/source_capture/ig_reels_deep_capture.py` | 8731 | `d337fef87704528ca3551edfa76acbc518251fe1d2311008f303cad23ab8735d` |
| `forseti-harness/source_capture/ig_reels_deep_capture_lake.py` | 6596 | `8dbd6c909ac4b2769ed65f03d11b5f70b8d99132ec91b1d7a36bc9685a477dde` |
| `forseti-harness/runners/run_source_capture_ig_reels_supervised_browser.py` | 9622 | `422232eeb6cd8dfdb270ce05de811709488aa8449bf6ee06b27b70bfe8ab4111` |
| `forseti-harness/source_capture/adapters/browser_snapshot.py` | 108960 | `f249aaaf787e04b7cea708d0bec26c4bbeb8762ea87fd561af882100d03d753d` |
| `forseti-harness/capture_spine/creator_profile_current/instagram_metric_seed.py` | 28524 | `dbc33785d1382383798a0cfeb7f4d1d689c9cbfb2f894c9439e73844f503cf83` |
| `forseti-harness/capture_spine/creator_profile_current/silver_metric_producer.py` | 23939 | `f87996fea1caf759681d065530b55a2e586e04c01b5b362391af685928552150` |
| `forseti-harness/capture_spine/creator_profile_current/materialize.py` | 29028 | `936cc3c8b706290a79b4d716adb84eb2548befa64032485a72771dbf8b8a940b` |
| `forseti-harness/capture_spine/creator_profile_current/validation.py` | 29949 | `3530014c4b0cbbf3578c8a59b90fa506a6a24aebadf64880634e4f5854f102da` |
| `forseti-harness/tests/unit/test_source_capture_ig_reels_grid_packet.py` | 22197 | `0e46ea4b1a48dace2d4f17986e8c8b4a3434f6258863dd037ebea13b8e83464a` |
| `forseti-harness/tests/unit/test_ig_reels_lane_orchestrator.py` | 21240 | `56239f3812f1fa9e5112d7e7f31dea2d5e1ad29cb330881de9385b034783c487` |
| `forseti-harness/tests/unit/test_ig_reels_supervised_browser_runner.py` | 7150 | `69ceba52cfe614433d38c4e2391cd7b0a65a33d7cea2c0645d321bc18d16940a` |
| `forseti-harness/tests/unit/test_ig_reels_creator_deep_capture.py` | 19162 | `aae04cf8178eeddb93f45f0ef273d19b666ce8dae6580ca2170419d6e2a10b01` |
| `forseti-harness/tests/unit/test_creator_metric_silver_producer.py` | 18355 | `d0f6cb4e061f1b1f78cbb8fcd84b3babee7d74f8ea18440442ffba12e7912db8` |
| `forseti-harness/tests/unit/test_creator_registry_index.py` | 5100 | `56ce92f9c7e8096af66c61785a68e784ab04c0cafe95ea1ee82b763fd05d72ea` |
