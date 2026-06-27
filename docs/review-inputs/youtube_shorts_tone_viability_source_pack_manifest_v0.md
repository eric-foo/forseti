# YouTube Shorts Tone Viability Source Pack Manifest v0

```yaml
retrieval_header_version: 1
artifact_role: Review input manifest
scope: Manifest for the no-repo-access source zip supporting the YouTube Shorts tone viability ChatGPT Pro prompt.
use_when:
  - Attaching source files for ChatGPT Pro or another reviewer with no repo access.
  - Verifying which Orca source files were packaged for the YouTube Shorts tone viability review.
authority_boundary: retrieval_only
open_next:
  - docs/prompts/deep-thinking/youtube_shorts_tone_viability_chatgpt_pro_prompt_v0.md
```

## Package

- Zip path: `docs/review-inputs/youtube_shorts_tone_viability_source_pack_v0.zip`
- Zip SHA256: `7235c96d1018c0d823e45705b0e69c5accee6394b5f93aa67ca0b4c4119010e5`
- Zip bytes: 47027

## Included Files

| Path | SHA256 |
| --- | --- |
| `docs/prompts/deep-thinking/youtube_shorts_tone_viability_chatgpt_pro_prompt_v0.md` | `4f27e07af87e6ac8e506dc696854c8adf6293d7f931905f7d1f859e405a13221` |
| `orca-harness/source_capture/transcript/youtube_captions.py` | `4e8d78377d47089fb92a10a3678f421ca5ec5160eb9560fd6d05742ad27c0175` |
| `orca-harness/source_capture/transcript/caption_packet.py` | `7e8d436d2b124506f5b9ddb94ab55f289460c46817560c1441c245bced7db348` |
| `orca-harness/source_capture/transcript/audio_asr.py` | `fb664eb567a2b591c8b199b90b5f95c52691af7b0bf6b6941068a8649ec2f974` |
| `orca-harness/source_capture/transcript/asr_packet.py` | `1fc53fc31c0d3a21ceb0c3a8ec4bcb8ede3814be2cdb1d7452cc3e35eec25d25` |
| `orca-harness/runners/run_source_capture_youtube_caption_packet.py` | `484c13e4bb991849bce8c74783d4e2c28a39b8a6510b13524eb554bff3ef8423` |
| `orca-harness/runners/run_source_capture_youtube_asr_packet.py` | `b41343ff9e6dffa8cbcffc0add2ba28cba2a9592769b5ae37b926c3c43bb8b5a` |
| `orca-harness/signal_content/models.py` | `b4c7b86d860983d0da6485456eb03b5ea9bbece0bbe15c3755c5c60bdff0876f` |
| `orca/product/spines/capture/core/source_families/social_media/youtube/youtube_transcript_product_extraction_spec_v0.md` | `e1eb4c29525d9ebdc21fab1545e92715ce76c11c4fdd1fc268ab04ef7060b8b5` |
| `orca/product/spines/capture/core/source_families/social_media/youtube/youtube_capture_recon_v0.md` | `39b003459afbba9d1825ee9f83de0182659bf84f8aa377cad01b1fd8af3d094b` |
| `orca/product/spines/capture/core/source_families/social_media/youtube/youtube_video_capture_surface_findings_v0.md` | `56ee8e3259ced41a864429d517885033af2b139c9bd78863bc6599cb74e92f2a` |

## Use

Paste the prompt file into ChatGPT Pro and attach the zip. The receiver should open `README.md` first, then inspect only the included files needed to answer the viability question.

## Non-Claims

This package is review input only. It is not validation, readiness, implementation authorization, source promotion, or a claim that the YouTube Shorts tone lane is viable.