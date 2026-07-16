#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Shared helpers for the scripts in .github/scripts (dot-source; not an entry point).

.DESCRIPTION
    Owning home for helpers shared across this directory's PowerShell scripts.
    Dot-source it at the top of a script:

        . (Join-Path $PSScriptRoot '_common.ps1')

    Before writing a private helper in a script here, check this file; if the
    shared home already has it, dot-source and use it. A deliberately divergent
    copy stays local with a one-line helper-delta comment naming the delta
    (e.g. merge-when-green.ps1's Stop-WithRefusal REFUSED wording,
    lane-health-check.ps1's exit-2 diagnostic aborts).
#>

function Stop-WithError([string]$Message) {
    Write-Host "ABORTED: $Message" -ForegroundColor Red
    exit 1
}

function Resolve-RepoRoot {
    # Aborts via Stop-WithError when git is missing or we are outside a repo.
    if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
        Stop-WithError 'git not found on PATH.'
    }
    $root = git rev-parse --show-toplevel 2>$null
    if ($LASTEXITCODE -ne 0 -or -not $root) {
        Stop-WithError 'not inside a git repository.'
    }
    return $root
}
