#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Human tool: verify a PR's CI check is green, then land it to main.

.DESCRIPTION
    Backs the merge-when-green flow under STRUCTURE B in
    docs/decisions/dev_workflow_ci_branch_protection_doctrine_v0.md (Decision item 7):
    agents PREPARE green PRs but do not self-merge; a HUMAN (or otherwise authorized
    action) lands the PR to main, and only when green. THIS SCRIPT IS THAT HUMAN STEP
    - run it yourself to green-check-and-merge.

    Agents must NOT use this to self-merge. The enforcement lane's protected-action
    guard blocks an agent's `gh pr merge` -> main; this helper merely wraps that merge,
    so running it from an agent would bypass the guard - which structure B forbids.

    Convenience, not a server-side gate (branch protection is 403-blocked on this
    private/free repo). It merges only when the required check is present and passing
    AND no check is failing or pending. Use -DryRun to evaluate read-only.

    Requires: GitHub CLI (gh) authenticated with repo access (recent enough to
    support `gh pr checks --json`).

.PARAMETER Pr
    Pull request number.

.PARAMETER Repo
    owner/repo. Defaults to FORSETI_GITHUB_REPOSITORY, then GITHUB_REPOSITORY, then eric-foo/orca.

.PARAMETER Check
    Name of the required check that must be green (default: orca-harness-tests).

.PARAMETER Method
    Merge method: squash (default), merge, or rebase.

.PARAMETER DryRun
    Evaluate and report the gate decision without merging.

.EXAMPLE
    pwsh .github/scripts/merge-when-green.ps1 -Pr 7

.EXAMPLE
    pwsh .github/scripts/merge-when-green.ps1 -Pr 7 -DryRun
#>
[CmdletBinding()]
param(
    [Parameter(Mandatory)][int]$Pr,
    [string]$Repo = '',
    [string]$Check = 'orca-harness-tests',
    [ValidateSet('squash', 'merge', 'rebase')][string]$Method = 'squash',
    [switch]$DryRun
)

$ErrorActionPreference = 'Stop'

function Stop-WithRefusal([string]$Message) {
    Write-Host "REFUSED: $Message" -ForegroundColor Red
    exit 1
}

function Resolve-RepoSlug {
    $candidate = if ($env:FORSETI_GITHUB_REPOSITORY) {
        $env:FORSETI_GITHUB_REPOSITORY
    } elseif ($env:GITHUB_REPOSITORY) {
        $env:GITHUB_REPOSITORY
    } else {
        'eric-foo/orca'
    }
    if ($candidate -notmatch '^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$') {
        Stop-WithRefusal "invalid repo slug '$candidate'."
    }
    return $candidate
}

if ([string]::IsNullOrWhiteSpace($Repo)) {
    $Repo = Resolve-RepoSlug
}

if ($Repo -notmatch '^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$') {
    Stop-WithRefusal "invalid repo slug '$Repo'."
}

if (-not (Get-Command gh -ErrorAction SilentlyContinue)) {
    Stop-WithRefusal 'GitHub CLI (gh) not found on PATH.'
}

# 1) The PR must be OPEN and not conflicting.
$prJson = gh pr view $Pr --repo $Repo --json 'state,mergeable,headRefName' 2>$null
if ($LASTEXITCODE -ne 0 -or -not $prJson) { Stop-WithRefusal "could not read PR #$Pr in $Repo." }
$prInfo = $prJson | ConvertFrom-Json
if ($prInfo.state -ne 'OPEN') { Stop-WithRefusal "PR #$Pr is $($prInfo.state), not OPEN." }
if ($prInfo.mergeable -eq 'CONFLICTING') { Stop-WithRefusal "PR #$Pr has merge conflicts; resolve them first." }

# 2) The required check must be present and passing, with nothing failing/pending.
#    `gh pr checks` exits non-zero while checks are pending/failing, so do not gate
#    on its exit code; gate on the parsed buckets instead.
$checksJson = gh pr checks $Pr --repo $Repo --json 'name,bucket,state' 2>$null
if (-not $checksJson) { Stop-WithRefusal "no CI checks reported on PR #$Pr; cannot confirm green." }
$checks = $checksJson | ConvertFrom-Json

Write-Host "PR #$Pr ($($prInfo.headRefName)) checks:"
foreach ($c in $checks) { Write-Host ("  {0,-26} {1}" -f $c.name, $c.bucket) }

$required = @($checks | Where-Object { $_.name -eq $Check })
if ($required.Count -lt 1) { Stop-WithRefusal "required check '$Check' not found on PR #$Pr." }
if (@($required | Where-Object { $_.bucket -eq 'pass' }).Count -lt 1) {
    Stop-WithRefusal "required check '$Check' is not passing (bucket: $($required[0].bucket))."
}
$blocking = @($checks | Where-Object { $_.bucket -in @('fail', 'pending', 'cancel') })
if ($blocking.Count -gt 0) {
    $list = ($blocking | ForEach-Object { "$($_.name)=$($_.bucket)" }) -join ', '
    Stop-WithRefusal "not all checks are green ($list)."
}

# 3) Green.
if ($DryRun) {
    Write-Host "GREEN: '$Check' passed and no checks are failing or pending. (DryRun: not merging.)" -ForegroundColor Green
    exit 0
}

Write-Host "GREEN: merging PR #$Pr via --$Method ..." -ForegroundColor Green
gh pr merge $Pr --repo $Repo "--$Method"
if ($LASTEXITCODE -ne 0) { Stop-WithRefusal "gh pr merge failed for PR #$Pr." }
Write-Host "Merged PR #$Pr." -ForegroundColor Green
