#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Spin up an isolated lane: a git worktree on a fresh branch off main.

.DESCRIPTION
    Implements the lane-isolation rule in AGENTS.md: a writing lane that runs
    alongside other active lanes (or on a dirty base) gets its own worktree off
    `main`, so its uncommitted work never interleaves with the shared tree.

    Creates <Lane> off the latest origin/<Base> and checks it out in a new
    worktree, then prints the work + cleanup-at-close commands. Land changes via
    the per-lane PR flow in
    docs/decisions/dev_workflow_ci_branch_protection_doctrine_v0.md.

    Read-only with -DryRun. Refuses if the branch or worktree path already exists.
    Does NOT clean up for you — cleanup at close is a deliberate step (printed).

    Requires: git. Run from anywhere inside the repo.

.PARAMETER Lane
    Lane name — used for the new branch and, by default, the worktree directory.

.PARAMETER Path
    Worktree directory. Default: a sibling of the repo root, <parent>/wt-<Lane>.

.PARAMETER Base
    Base ref the lane branches from. Default: main.

.PARAMETER DryRun
    Print what would happen without creating anything.

.EXAMPLE
    pwsh .github/scripts/spin-up-lane.ps1 -Lane my-feature

.EXAMPLE
    pwsh .github/scripts/spin-up-lane.ps1 -Lane my-feature -DryRun
#>
[CmdletBinding()]
param(
    [Parameter(Mandatory)][string]$Lane,
    [string]$Path,
    [string]$Base = 'main',
    [switch]$DryRun
)

$ErrorActionPreference = 'Stop'

function Stop-WithError([string]$Message) {
    Write-Host "ABORTED: $Message" -ForegroundColor Red
    exit 1
}

if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    Stop-WithError 'git not found on PATH.'
}

# Resolve repo root and default worktree path.
$repoRoot = git rev-parse --show-toplevel 2>$null
if ($LASTEXITCODE -ne 0 -or -not $repoRoot) { Stop-WithError 'not inside a git repository.' }
if (-not $Path) {
    $Path = Join-Path (Split-Path -Parent $repoRoot) "wt-$Lane"
}

# Refuse on collisions rather than disturbing existing work.
git show-ref --verify --quiet "refs/heads/$Lane" 2>$null
if ($LASTEXITCODE -eq 0) { Stop-WithError "branch '$Lane' already exists." }
if (Test-Path $Path) { Stop-WithError "worktree path already exists: $Path" }

Write-Host "Lane:     $Lane"
Write-Host "Worktree: $Path"
Write-Host "Base:     origin/$Base"

if ($DryRun) {
    Write-Host "DryRun - would run:" -ForegroundColor Yellow
    Write-Host "  git fetch --prune origin"
    Write-Host "  git worktree add -b $Lane `"$Path`" origin/$Base"
    exit 0
}

git fetch --prune origin 2>&1 | Out-Null
if ($LASTEXITCODE -ne 0) { Stop-WithError 'git fetch --prune origin failed.' }
git worktree add -b $Lane "$Path" "origin/$Base"
if ($LASTEXITCODE -ne 0) { Stop-WithError 'git worktree add failed.' }

Write-Host "Lane ready." -ForegroundColor Green
Write-Host ""
Write-Host "Work in it:  cd `"$Path`""
Write-Host "Land it:     commit (explicit paths) -> push -> PR off main -> merge-when-green"
Write-Host "             (docs/decisions/dev_workflow_ci_branch_protection_doctrine_v0.md)"
Write-Host ""
Write-Host "Classify before cleanup (read-only; re-derive live):" -ForegroundColor Cyan
Write-Host "  pwsh `"$repoRoot/.github/scripts/lane-health-check.ps1`" -RepoPath `"$Path`" -Fetch -ClassifyWorktrees -Json"
Write-Host "This helper does not execute the doctrine item-10 lane-start sweep or cleanup."
Write-Host "After the PR is merged and the fresh classifier marks this lane merged_gone_clean:"
Write-Host "  git -C `"$repoRoot`" worktree remove `"$Path`"   # non-force; refuses dirty/untracked"
Write-Host "  git -C `"$repoRoot`" branch -D $Lane              # only after all classifier/doctrine guards pass"
Write-Host "Remote branch deletion is normally handled by the merged PR. Never delete from a cached classification."
