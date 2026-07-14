#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Install Forseti's tracked local Git hooks for this Git clone.

.DESCRIPTION
    Sets the effective git config core.hooksPath to .githooks so Git uses the
    active worktree's tracked Forseti hook adapters. When extensions.worktreeConfig
    is enabled, the value is written to the active worktree's config; otherwise it
    is clone-local. Each checkout where hooks should fire must contain the tracked
    .githooks files. This is local Git-client enforcement: it is useful for Codex,
    Claude Code, and humans, but remains bypassable with --no-verify and does not
    replace server-side branch protection.

.PARAMETER VerifyOnly
    Check the current hooksPath and required hook files without changing config.
#>
[CmdletBinding()]
param(
    [switch]$VerifyOnly
)

$ErrorActionPreference = 'Stop'

function Stop-WithError([string]$Message) {
    Write-Host "ABORTED: $Message" -ForegroundColor Red
    exit 1
}

if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    Stop-WithError 'git not found on PATH.'
}

$repoRoot = git rev-parse --show-toplevel 2>$null
if ($LASTEXITCODE -ne 0 -or -not $repoRoot) {
    Stop-WithError 'not inside a git repository.'
}

$hookPath = '.githooks'
$requiredHooks = @('pre-push', 'commit-msg')

foreach ($hook in $requiredHooks) {
    $path = Join-Path $repoRoot (Join-Path $hookPath $hook)
    if (-not (Test-Path $path)) {
        Stop-WithError "missing hook file: $path"
    }
}

$isWindowsVariable = Get-Variable -Name IsWindows -ErrorAction SilentlyContinue
if ($isWindowsVariable) {
    $runningOnWindows = [bool]$isWindowsVariable.Value
} else {
    $runningOnWindows = ($env:OS -eq 'Windows_NT')
}

if (-not $runningOnWindows) {
    foreach ($hook in $requiredHooks) {
        $path = Join-Path $repoRoot (Join-Path $hookPath $hook)
        chmod +x $path
    }
}

$worktreeConfig = git config --local --type=bool --get extensions.worktreeConfig 2>$null
$worktreeConfigExit = $LASTEXITCODE
if ($worktreeConfigExit -ne 0 -and $worktreeConfigExit -ne 1) {
    Stop-WithError 'failed to read extensions.worktreeConfig.'
}
$configScope = if ($worktreeConfigExit -eq 0 -and $worktreeConfig -eq 'true') {
    '--worktree'
} else {
    '--local'
}

if (-not $VerifyOnly) {
    git config $configScope core.hooksPath $hookPath
    if ($LASTEXITCODE -ne 0) {
        Stop-WithError "failed to set git config $configScope core.hooksPath."
    }
}

$configured = git config --get core.hooksPath 2>$null
$configuredExit = $LASTEXITCODE
if ($configuredExit -ne 0 -and $configuredExit -ne 1) {
    Stop-WithError 'failed to read effective git config core.hooksPath.'
}
if ($configuredExit -eq 0 -and [System.IO.Path]::IsPathRooted($configured)) {
    $configuredResolved = [System.IO.Path]::GetFullPath($configured)
} elseif ($configuredExit -eq 0 -and $configured) {
    $configuredResolved = [System.IO.Path]::GetFullPath((Join-Path $repoRoot $configured))
} else {
    $configuredResolved = $null
}
$expectedResolved = [System.IO.Path]::GetFullPath((Join-Path $repoRoot $hookPath))
$actualDisplay = if ($configuredResolved) { $configuredResolved } else { '<unset>' }
$configuredDisplay = if ($configured) { $configured } else { '<unset>' }

if ($configuredResolved -ne $expectedResolved) {
    Stop-WithError "core.hooksPath resolves to '$actualDisplay', expected '$expectedResolved' for worktree '$repoRoot' (configured value: '$configuredDisplay')."
}

Write-Host "Forseti local hooks path: $configured"
Write-Host "Configuration scope: $configScope"
Write-Host "Tracked hooks present: $($requiredHooks -join ', ')"
Write-Host "Boundary: local Git hooks are bypassable with --no-verify; active server-side branch protection is the unbypassable merge gate."
Write-Host "Linked-worktree note: core.hooksPath is clone-local unless worktreeConfig is enabled; check out .githooks in each active worktree that should enforce it."
