#Requires -Version 5.1
param(
    [string]$CodexCommand = "codex"
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$TargetUuid = "01KW1E6N133JT0XCN2KCN0V5A4"
$Model = "codex-extraction-v0"
$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..\..")).Path
$HarnessPath = Join-Path $RepoRoot "orca-harness"
$PromptPath = Join-Path $RepoRoot "docs\prompts\handoffs\ig_reels_product_extract_codex_exec_prompt_v0.md"
$PromptSha256 = "68243EF7DC57A8B3C08DF4D6A918453CAA5A98B61F2A3C1C5A0873E962B7A332"
$LogDir = Join-Path $HarnessPath "_scratch\ig_reels_extract_routine"

function Get-OrcaDriveLetters {
    try {
        if (Get-Command Get-Volume -ErrorAction SilentlyContinue) {
            return @((Get-Volume -ErrorAction Stop | Where-Object DriveLetter | Sort-Object DriveLetter).DriveLetter)
        }
    } catch {
        # Fall back below. UUID marker matching remains the safety check.
    }
    return @((Get-PSDrive -PSProvider FileSystem | Where-Object { $_.Name -match "^[A-Za-z]$" } | Sort-Object Name).Name)
}

function Resolve-OrcaLake {
    foreach ($d in Get-OrcaDriveLetters) {
        $marker = "${d}:\orca-data-lake\.orca-data-root"
        if (Test-Path $marker) {
            try {
                $u = (Get-Content $marker -Raw | ConvertFrom-Json).root_uuid
            } catch {
                continue
            }
            if ($u -eq $TargetUuid) {
                return "${d}:\orca-data-lake"
            }
        }
    }
    return $null
}

function Invoke-PendingCheck {
    $raw = & python -m runners.run_ig_reels_product_extract --check --model $Model 2>&1
    $code = $LASTEXITCODE
    if ($code -ne 0) {
        Write-Output ("check_exit={0}" -f $code)
        Write-Output ("check_output={0}" -f (($raw | Out-String).Trim()))
        exit $code
    }
    $text = (($raw | Out-String).Trim())
    if ($text -notmatch "^\d+$") {
        Write-Output "check_exit=2"
        Write-Output ("check_output={0}" -f $text)
        exit 2
    }
    return [int]$text
}

$root = Resolve-OrcaLake
if (-not $root) {
    Write-Output "lake=<not found>"
    Write-Output "status=skipped_lake_offline"
    exit 0
}

Write-Output ("lake={0}" -f $root)

$env:ORCA_DATA_ROOT = $root
$env:PYTHONPATH = $HarnessPath

Push-Location $RepoRoot
try {
    $pending = Invoke-PendingCheck
    Write-Output ("pending_before={0}" -f $pending)
    if ($pending -le 0) {
        Write-Output "status=skipped_done"
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
    Write-Output ("pending_after={0}" -f $after)
    if ($after -eq 0) {
        Write-Output "status=done"
    } else {
        Write-Output "status=remaining"
    }
    exit 0
} finally {
    Pop-Location
}
