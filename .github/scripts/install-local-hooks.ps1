#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Install Forseti's tracked local Git hooks for this Git clone.

.DESCRIPTION
    Sets local git config core.hooksPath to .githooks so Git uses the tracked
    Forseti hook adapters. In linked worktree setups this local config is shared by
    the clone; each checkout where hooks should fire must contain the tracked
    .githooks files. This is local Git-client enforcement: it is useful for
    Codex, Claude Code, and humans, but remains bypassable with --no-verify and
    does not replace server-side branch protection.

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

if (-not $VerifyOnly) {
    git config --local core.hooksPath $hookPath
    if ($LASTEXITCODE -ne 0) {
        Stop-WithError 'failed to set git config core.hooksPath.'
    }
}

$configured = git config --local --get core.hooksPath 2>$null
if ($VerifyOnly -and $configured -ne $hookPath) {
    Stop-WithError "core.hooksPath is '$configured', expected '$hookPath'."
}
if (-not $VerifyOnly -and $configured -ne $hookPath) {
    Stop-WithError "core.hooksPath readback is '$configured', expected '$hookPath'."
}

Write-Host "Forseti local hooks path: $configured"
Write-Host "Tracked hooks present: $($requiredHooks -join ', ')"
Write-Host "Boundary: local Git hooks are bypassable with --no-verify; server-side branch protection remains the unbypassable target."
Write-Host "Linked-worktree note: core.hooksPath is clone-local unless worktreeConfig is enabled; check out .githooks in each active worktree that should enforce it."
