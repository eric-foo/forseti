# YouTube Shorts Tone Rubric Delegated Review Source Pack Manifest v0

```yaml
retrieval_header_version: 1
artifact_role: Review input manifest
scope: Manifest for the no-repo source zip supporting the delegated review of the YouTube Shorts transcript tone rubric.
use_when:
  - Attaching source files for a no-repo reviewer.
  - Verifying which Orca source files were packaged for this delegated review commission.
authority_boundary: retrieval_only
open_next:
  - docs/prompts/reviews/youtube_shorts_transcript_tone_rubric_delegated_adversarial_artifact_review_patch_prompt_v0.md
```

## Package

- Zip path: `docs/review-inputs/youtube_shorts_tone_rubric_delegated_review_source_pack_v0.zip`
- Zip SHA256: `6c556e319cb7f7df2e7e9232051c1d0f2f04276e09d6e5f5d89b9a753d3304b2`
- Zip bytes: 103654

## Included Files

| Path | SHA256 | Bytes |
| --- | --- | ---: |
| `docs/review-inputs/youtube_shorts_tone_rubric_delegated_review_source_pack_readme_v0.md` | `9f35024066ef6cec993f446486e871dcca604673a4949d5909ce127419cce5db` | 2454 |
| `docs/prompts/reviews/youtube_shorts_transcript_tone_rubric_delegated_adversarial_artifact_review_patch_prompt_v0.md` | `0559f6a5f13c98fabfc7b972f56d3c29ce2a5f6c9f0af4f4e58bab020995380e` | 13011 |
| `docs/review-inputs/youtube_shorts_fragrance_transcript_tone_rubric_v0.md` | `b830c4ae3f220def0d6e787660a5acfdd93dcccc14ccf80d5bcd81b4aef569df` | 1946 |
| `docs/review-inputs/youtube_shorts_fragrance_tone_fixture_hard30_v0.md` | `12365c8f08ec1c18a2d07f17aafb8a3d5e10d8fbe524f311152c2dd7efc87cfe` | 6520 |
| `docs/review-inputs/youtube_shorts_fragrance_tone_fixture_hard30_v0.json` | `b83c4688f9dfce0b0febf33b9141e6ebc9bce4961f4ade5847db2a684f15d78d` | 75056 |
| `docs/review-inputs/youtube_shorts_fragrance_tone_labeling_run_v0.md` | `ce8c065b957b0ded5de2b4e6e201fd00f651e60d77bffaf62dc656ca270770ac` | 8005 |
| `docs/review-inputs/youtube_shorts_fragrance_tone_labeling_run_v0.json` | `18fd4dfc257c6bb74aae4a6416bf74f485b5ba310309b34fb60f77f2d287b173` | 37310 |
| `AGENTS.md` | `4296e7617d8b2675881780cd7be0704a00dcb17adf7758243008de956070940b` | 8383 |
| `.agents/workflow-overlay/README.md` | `a136775da51f7b1b7563292660b705673b26e1a6436a08f7566c221d3b4bcf6a` | 2550 |
| `.agents/workflow-overlay/source-of-truth.md` | `04daf7979fda605a2e7cf334dbc7ecadb02f8c1f1b40a432e14b4f3503235d0c` | 21407 |
| `.agents/workflow-overlay/source-loading.md` | `8fadc263b98f08b73b68e44de71709d4aaf7fea5d2e0390602b93e7863e11ab3` | 32062 |
| `.agents/workflow-overlay/review-lanes.md` | `ad4ccf88478bc726a7711e6480890d56a427108c609d1002ebdc40c88ef57d58` | 18086 |
| `.agents/workflow-overlay/prompt-orchestration.md` | `64740c756aec4a19f5218bcf275e05328b15b82ab62f08d9d977bb89cf849ee5` | 55082 |
| `.agents/workflow-overlay/validation-gates.md` | `25e4b2c96abb137c458ac8088e888e9927b0b57a6bd482ac615dd4f473d43ce5` | 28369 |
| `.agents/workflow-overlay/delegated-review-patch.md` | `41f18f5879d8faab73015822e49376d91e03ff6e5cc4a0835b4f17e6fe7c8688` | 25565 |
| `docs/prompts/templates/review/adversarial_artifact_review_v0.md` | `b7355d6d02cfc522d213dee3f28ed4b824899bc997084efee98df5a710518cc4` | 6899 |
| `docs/prompts/templates/shared/orca_prompt_behavior_contract_v0.md` | `d8d4e956b955722a9a84a38ba9c491e9b616121868c59beed1d71867bdb7791d` | 6761 |
| `docs/prompts/templates/shared/orca_preflight_defaults_v0.md` | `e16570c26c8be0b6a811b13f0fe350edea5bf34038a13392e96f8897cb3a1546` | 3542 |

## Use

Attach the zip to the no-repo reviewer and direct them to open `docs/review-inputs/youtube_shorts_tone_rubric_delegated_review_source_pack_readme_v0.md` first, then the prompt named there.

## Non-Claims

This package is review input only. It is not validation, readiness, acceptance, benchmark proof, product proof, runtime model routing, or a claim that no-repo review can perform repo-mode patch authorship.
