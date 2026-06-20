# CloakBrowser Local Setup Probe Receipt v0

```yaml
retrieval_header_version: 1
artifact_role: Product artifact
scope: Local CloakBrowser wrapper, binary, and API-shape setup facts for the Source Capture Armory packet-runner path.
use_when:
  - Verifying whether CloakBrowser is locally available for adapter-contract work.
  - Reconstructing the first bounded setup probe before runner or Reddit capture work.
  - Checking the stop line between local setup and source capture execution.
authority_boundary: retrieval_only
```

## Status

`LOCAL_SETUP_PROBE_COMPLETE`

This receipt records a bounded local setup probe only. It does not authorize or perform Reddit capture, source capture packet generation, runner implementation, parser execution, source discovery, crawling, proxy use, persistent profile use, authenticated capture, commercial capture, ECR, Cleaning, Judgment, fixture admission, or source-quality scoring.

## Source Read

- Orca overlay entrypoint: `.agents/workflow-overlay/README.md`
- Accepted artifact folder rule: `.agents/workflow-overlay/artifact-folders.md`
- Retrieval metadata rule: `.agents/workflow-overlay/retrieval-metadata.md`
- CloakBrowser public repository / README: `https://github.com/CloakHQ/cloakbrowser`

## Setup Boundary

The correct first setup step is not to wire CloakBrowser into Orca immediately. The correct first step is a bounded local API discovery setup:

1. Install the Python wrapper into an ignored probe location.
2. Inspect wrapper import/API shape without launching Chromium.
3. Download/verify the CloakBrowser Chromium binary separately.
4. Run a blank headless launch-and-close smoke test.
5. Stop before any URL navigation, Reddit access, packet writing, or runner integration.

## Local Install Facts

- Probe location: `orca-harness/_test_runs/cloakbrowser_api_probe/`
- Probe dependency target: `orca-harness/_test_runs/cloakbrowser_api_probe/site`
- Git hygiene: `orca-harness/_test_runs/` is ignored by `.gitignore`.
- Installed wrapper: `cloakbrowser==0.3.31`
- Installed runtime dependency observed during install: `playwright==1.60.0`
- CloakBrowser Chromium version: `146.0.7680.177.5`
- Platform: `windows-x64`
- Binary path: `C:\Users\vmon7\.cloakbrowser\chromium-146.0.7680.177.5\chrome.exe`
- Binary cache dir: `C:\Users\vmon7\.cloakbrowser\chromium-146.0.7680.177.5`
- Download URL reported by `binary_info()`: `https://cloakbrowser.dev/chromium-v146.0.7680.177.5/cloakbrowser-windows-x64.zip`

## API Shape Observed

Public attributes included:

```text
CHROMIUM_VERSION
ProxySettings
binary_info
build_args
check_for_update
clear_cache
ensure_binary
get_default_stealth_args
launch
launch_async
launch_context
launch_context_async
launch_persistent_context
launch_persistent_context_async
maybe_resolve_geoip
```

Observed `launch(...)` signature:

```text
(headless: 'bool' = True, proxy: 'str | ProxySettings | None' = None, args: 'list[str] | None' = None, stealth_args: 'bool' = True, timezone: 'str | None' = None, locale: 'str | None' = None, geoip: 'bool' = False, backend: 'str | None' = None, humanize: 'bool' = False, human_preset: 'HumanPreset' = 'default', human_config: 'HumanConfigOverrides | None' = None, extension_paths: 'list[str] | None' = None, **kwargs: 'Any') -> 'Any'
```

Adapter implication:

- Anonymous v0 should bind to `launch` or `launch_context`, not `launch_persistent_context`.
- `ensure_binary()` is the binary download boundary.
- `proxy`, `geoip`, `extension_paths`, persistent profile paths, and arbitrary secret-bearing kwargs are not v0 defaults.
- `backend` is available as a parameter and can be fixed by adapter contract rather than exposed to agents as a freeform switch.

## Verification Readback

Fresh durable-target read:

```text
binary_exists=True
binary_path=C:\Users\vmon7\.cloakbrowser\chromium-146.0.7680.177.5\chrome.exe
dist_info_exists=True
probe_site=C:\Users\vmon7\Desktop\projects\orca\orca-harness\_test_runs\cloakbrowser_api_probe\site\cloakbrowser-0.3.31.dist-info
```

Blank launch-and-close smoke test:

```text
browser_type=Browser
contexts=0
closed=True
```

No URL navigation was performed in the smoke test.

## Sandbox / ACL Note

The package installed successfully under the ignored probe target, but sandboxed reads could not traverse the installed package directories after the approved install. Read-only elevated inspection was used for package file listing and API introspection. This is an environment/access note, not a CloakBrowser API failure.

## Next Checkpoint

`READY_FOR_ADAPTER_CONTRACT_SCOPING`

The next smallest complete step is not Reddit capture. It is an adapter-contract scoping pass that defines:

- the minimal `CloakBrowserEngine` protocol;
- the result envelope and failure taxonomy;
- the no-secret / no-persistent-profile guards;
- fake-engine tests that require no live browser;
- the exact point where a future runner may call the engine.

Live Reddit access, packet writing, parser execution, proxy use, authenticated capture, and monitored thread capture remain out of scope until separately authorized.
