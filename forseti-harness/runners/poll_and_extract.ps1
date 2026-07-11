#Requires -Version 5.1
param(
    [string]$CodexCommand = "codex"
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

# Pinned lake identity: v4.1 forward epoch (primary F:\forseti-data-lake; legacy F:\orca-data-lake remains UUID-gated);
# the prior v0 root is archived at F:\orca-data-lake-legacy-v0-20260628T174129Z.
$TargetUuid = "01KW7N6ERSVVANCEZ8SD6YW3EQ"
$Model = "codex-extraction-v0"
$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..\..")).Path
$HarnessPath = Join-Path $RepoRoot "forseti-harness"
$PromptPath = Join-Path $RepoRoot "docs\prompts\handoffs\ig_reels_product_extract_codex_exec_prompt_v0.md"
$PromptSha256 = "7D8CAC53DC4F4AA80A53907B50FD3DC1F81FF2B2DE6B3726C0A8CC03F574F1CB"
$LogDir = Join-Path ([System.IO.Path]::GetTempPath()) "forseti_ig_reels_extract_routine"

function Get-ForsetiDriveLetters {
    try {
        if (Get-Command Get-Volume -ErrorAction SilentlyContinue) {
            return @((Get-Volume -ErrorAction Stop | Where-Object DriveLetter | Sort-Object DriveLetter).DriveLetter)
        }
    } catch {
        # Fall back below. UUID marker matching remains the safety check.
    }
    return @((Get-PSDrive -PSProvider FileSystem | Where-Object { $_.Name -match "^[A-Za-z]$" } | Sort-Object Name).Name)
}

$script:RootUuidMismatches = @()

function Resolve-ForsetiLake {
    foreach ($d in Get-ForsetiDriveLetters) {
        $candidates = @(
            @{ Root = "${d}:\forseti-data-lake"; Marker = "${d}:\forseti-data-lake\.forseti-data-root" },
            @{ Root = "${d}:\orca-data-lake"; Marker = "${d}:\orca-data-lake\.orca-data-root" }
        )
        foreach ($candidate in $candidates) {
            $marker = $candidate.Marker
            if (-not (Test-Path $marker)) {
                continue
            }
            try {
                $u = (Get-Content $marker -Raw | ConvertFrom-Json).root_uuid
            } catch {
                continue
            }
            if ($u -eq $TargetUuid) {
                return $candidate.Root
            }
            $script:RootUuidMismatches += ("{0} root_uuid={1}" -f $candidate.Root, $u)
        }
    }
    return $null
}

function Invoke-CheckCount {
    param([string]$Mode)

    $checkArgs = @("-m", "runners.run_ig_reels_product_extract", "--model", $Model)
    if ($Mode -eq "partials") {
        $checkArgs += "--check-partials"
    } else {
        $checkArgs += "--check"
    }

    $raw = & python @checkArgs 2>&1
    $code = $LASTEXITCODE
    if ($code -ne 0) {
        Write-Output ("check_exit={0}" -f $code)
        Write-Output ("check_mode={0}" -f $Mode)
        Write-Output ("check_output={0}" -f (($raw | Out-String).Trim()))
        exit $code
    }
    $text = (($raw | Out-String).Trim())
    if ($text -notmatch "^\d+$") {
        Write-Output "check_exit=2"
        Write-Output ("check_mode={0}" -f $Mode)
        Write-Output ("check_output={0}" -f $text)
        exit 2
    }
    return [int]$text
}

function Invoke-PendingCheck {
    return Invoke-CheckCount -Mode "pending"
}

function Invoke-PartialCheck {
    return Invoke-CheckCount -Mode "partials"
}

$root = Resolve-ForsetiLake
if (-not $root) {
    if ($script:RootUuidMismatches.Count -gt 0) {
        Write-Output "lake=<root identity mismatch>"
        Write-Output ("expected_root_uuid={0}" -f $TargetUuid)
        foreach ($m in $script:RootUuidMismatches) {
            Write-Output ("found={0}" -f $m)
        }
        Write-Output "status=blocked_root_uuid_mismatch"
        exit 2
    }
    Write-Output "lake=<not found>"
    Write-Output "status=skipped_lake_offline"
    exit 0
}

Write-Output ("lake={0}" -f $root)

$env:FORSETI_DATA_ROOT = $root
$env:PYTHONPATH = $HarnessPath

Push-Location $RepoRoot
try {
    $pending = Invoke-PendingCheck
    $partials = Invoke-PartialCheck
    Write-Output ("pending_before={0}" -f $pending)
    if ($partials -gt 0) {
        Write-Output ("partial_needs_cleanup={0}" -f $partials)
    }
    if ($pending -le 0) {
        if ($partials -gt 0) {
            Write-Output "status=skipped_partial_needs_cleanup"
        } else {
            Write-Output "status=skipped_done"
        }
        exit 0
    }

    if (-not (Test-Path $PromptPath)) {
        Write-Output "status=blocked_prompt_missing"
        exit 2
    }
    $actualPromptHash = (Get-FileHash $PromptPath -Algorithm SHA256).Hash
    if ($actualPromptHash -ne $PromptSha256) {
        Write-Output "status=blocked_prompt_hash_mismatch"
        Write-Output ("expected_prompt_sha256={0}" -f $PromptSha256)
        Write-Output ("actual_prompt_sha256={0}" -f $actualPromptHash)
        exit 2
    }

    $codex = Get-Command $CodexCommand -ErrorAction SilentlyContinue
    if (-not $codex) {
        Write-Output "status=blocked_codex_not_found"
        exit 2
    }
    $codexPath = $codex.Source
    if (-not $codexPath) { $codexPath = $codex.Path }

    New-Item -ItemType Directory -Force $LogDir | Out-Null
    $stamp = Get-Date -Format "yyyyMMdd_HHmmss"
    $lastMessagePath = Join-Path $LogDir ("codex_last_message_{0}.txt" -f $stamp)

    $prompt = Get-Content $PromptPath -Raw
    $codexArgs = @(
        "exec",
        "--cd", $RepoRoot,
        "--add-dir", $root,
        "--sandbox", "workspace-write",
        "--ask-for-approval", "never",
        "--color", "never",
        "--output-last-message", $lastMessagePath,
        "-"
    )

    Write-Output "status=codex_start"
    $prompt | & $codexPath @codexArgs
    $codexExit = $LASTEXITCODE
    Write-Output ("codex_exit={0}" -f $codexExit)
    if ($codexExit -ne 0) {
        Write-Output "status=blocked_codex_failed"
        exit $codexExit
    }

    $after = Invoke-PendingCheck
    $afterPartials = Invoke-PartialCheck
    Write-Output ("pending_after={0}" -f $after)
    if ($afterPartials -gt 0) {
        Write-Output ("partial_needs_cleanup_after={0}" -f $afterPartials)
    }
    if ($after -eq 0) {
        if ($afterPartials -gt 0) {
            Write-Output "status=done_with_partial_needs_cleanup"
        } else {
            Write-Output "status=done"
        }
    } else {
        Write-Output "status=remaining"
    }
    exit 0
} finally {
    Pop-Location
}
