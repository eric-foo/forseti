#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Read-only lane health check: early detection of lane-isolation drift and of
    enforcement that lives only on this machine (not on origin/main).

.DESCRIPTION
    Backs the lane-isolation rule in AGENTS.md and the per-lane PR flow in
    docs/decisions/dev_workflow_ci_branch_protection_doctrine_v0.md. Lane
    isolation is a JUDGMENT rule, so this is a DETECTOR, not a gate: it surfaces
    drift early instead of hard-blocking. Run it yourself (or wire it into a
    periodic check); a non-zero exit is a nudge, not a block.

    Read-only with respect to the working tree, index, and local branches/commits:
    it never writes, stages, commits, pushes, or changes your checkout. It runs
    `git status` / `worktree list` / `ls-tree` / `ls-files` / `rev-parse`. `-Fetch`
    additionally performs a network `git fetch origin`, which updates only
    remote-tracking refs (refs/remotes/origin/*) and FETCH_HEAD - never the working
    tree, index, or local branches - so the not-on-main check sees current origin/main.

    Checks:
      1. dirty-volume          - modified + untracked count vs -DirtyThreshold.
                                 A large uncommitted pile-up on a shared base is the
                                 lane-isolation drift the rule guards against.
      2. worktree-sprawl       - linked-worktree count (the main worktree excluded)
                                 vs -WorktreeThreshold. Lanes are meant to be
                                 cleaned up at close.
      3. machine-local-        - any .agents/hooks/*.py physically present in the
         enforcement             working tree (tracked, untracked, or git-ignored)
                                 but NOT tracked on origin/main. Such a hook enforces
                                 only on this machine; a fresh clone of main would
                                 not have it, so any doctrine that calls it
                                 "enforced" is ahead of main's durable state.

    Exit codes: 0 = healthy (no warnings); 1 = one or more warnings (detection
    nudge); 2 = usage/abort error (no git, not a repo). Use -Json for machine
    output, -SelfTest to validate the detection logic without touching git.

.PARAMETER RepoPath
    Repository working tree to inspect. Default: the git toplevel of the cwd.

.PARAMETER DirtyThreshold
    Warn when modified+untracked file count exceeds this. Default 30.

.PARAMETER WorktreeThreshold
    Warn when the repo has more than this many linked worktrees (the main worktree
    is not counted). Default 4.

.PARAMETER Fetch
    Run `git fetch --prune origin` first so checks compare against fresh remote
    state. Off by default (no network). The fetch updates only
    remote-tracking refs and FETCH_HEAD, not the working tree, index, or local
    branches; the report notes when origin/main is only the local ref.

.PARAMETER ClassifyWorktrees
    Add a read-only classification of every linked worktree. Requires -Fetch
    so remote-tracking refs are freshly pruned, and requires authenticated `gh`
    access so open, merged, and closed-unmerged PR states can be distinguished.
    The result may identify fresh cleanup candidates but never removes a
    worktree or branch and never grants cleanup authority.

.PARAMETER GitHubRepo
    GitHub owner/repository used for PR-state reads. When omitted, derive it
    from the origin remote.

.PARAMETER Json
    Emit findings and any requested classification as JSON instead of
    human-readable text.

.PARAMETER SelfTest
    Run the detection logic against synthetic inputs and exit (0 ok / 1 fail).

.EXAMPLE
    pwsh .github/scripts/lane-health-check.ps1

.EXAMPLE
    pwsh .github/scripts/lane-health-check.ps1 -RepoPath C:\path\to\repo -Fetch

.EXAMPLE
    pwsh .github/scripts/lane-health-check.ps1 -RepoPath C:\path\to\repo -Fetch -ClassifyWorktrees -Json

.EXAMPLE
    pwsh .github/scripts/lane-health-check.ps1 -SelfTest
#>
[CmdletBinding()]
param(
    [string]$RepoPath,
    [int]$DirtyThreshold = 30,
    [int]$WorktreeThreshold = 4,
    [switch]$Fetch,
    [switch]$ClassifyWorktrees,
    [string]$GitHubRepo,
    [switch]$Json,
    [switch]$SelfTest
)

$ErrorActionPreference = 'Stop'

# --- pure detection logic (no git, no IO; this is what -SelfTest exercises) --

function New-Finding([string]$Check, [string]$Level, [string]$Message) {
    [pscustomobject]@{ check = $Check; level = $Level; message = $Message }
}

function Test-DirtyVolume([int]$Modified, [int]$Untracked, [int]$Threshold) {
    $total = $Modified + $Untracked
    if ($total -gt $Threshold) {
        return New-Finding 'dirty-volume' 'warn' (
            "$total uncommitted files (modified=$Modified, untracked=$Untracked) exceed " +
            "threshold $Threshold - looks like lane pile-up on a shared base. Isolate work " +
            "in its own worktree/branch off main and land via the per-lane PR flow.")
    }
    New-Finding 'dirty-volume' 'ok' (
        "$total uncommitted files (modified=$Modified, untracked=$Untracked) within threshold $Threshold.")
}

function Test-WorktreeSprawl([int]$Count, [int]$Threshold) {
    if ($Count -gt $Threshold) {
        return New-Finding 'worktree-sprawl' 'warn' (
            "$Count linked worktrees exceed threshold $Threshold - stale lanes may not have " +
            "been cleaned up at close.")
    }
    New-Finding 'worktree-sprawl' 'ok' "$Count linked worktrees within threshold $Threshold."
}

function Test-MachineLocalEnforcement([string[]]$LocalHooks, [string[]]$MainHooks, [bool]$MainAvailable = $true) {
    if (-not $MainAvailable) {
        return New-Finding 'machine-local-enforcement' 'ok' (
            'skipped: origin/main not available locally (run with -Fetch to compare).')
    }
    $mainSet = @{}
    foreach ($h in $MainHooks) { if ($h) { $mainSet[$h] = $true } }
    $local = @($LocalHooks | Where-Object { $_ })
    $orphan = @($local | Where-Object { -not $mainSet.ContainsKey($_) })
    if ($orphan.Count -gt 0) {
        return New-Finding 'machine-local-enforcement' 'warn' (
            "enforcement hook(s) present locally but NOT tracked on origin/main: " +
            ($orphan -join ', ') + " - these enforce only on this machine; a fresh clone of " +
            "main lacks them, so any doctrine that calls them 'enforced' is ahead of main's " +
            "durable state. Land the hook on main, or state the liveness boundary in doctrine.")
    }
    if ($local.Count -eq 0) {
        return New-Finding 'machine-local-enforcement' 'ok' 'no .agents/hooks/*.py present in the working tree.'
    }
    New-Finding 'machine-local-enforcement' 'ok' (
        "all $($local.Count) local enforcement hook(s) are tracked on origin/main.")
}

function Select-PrStateRecord($Current, $Candidate) {
    if ($null -eq $Current) { return $Candidate }
    $priority = @{ open = 3; closed_unmerged = 2; merged = 1 }
    $currentPriority = $priority[$Current.state]
    $candidatePriority = $priority[$Candidate.state]
    if ($candidatePriority -gt $currentPriority) { return $Candidate }
    if ($candidatePriority -lt $currentPriority) { return $Current }
    if ($Candidate.createdAt -gt $Current.createdAt) { return $Candidate }
    $Current
}

function Resolve-WorktreeCategory(
    [string]$Branch,
    [string]$Path,
    [string]$Tracking,
    [string]$PrState,
    [bool]$Locked,
    [string]$DirtyState,
    [string]$PrHeadState = 'not_applicable',
    [string]$Upstream = ''
) {
    $leaf = Split-Path -Leaf $Path
    if ($Locked -or $Branch -eq 'pilot-seal-outcome' -or $leaf -eq 'orca-seal-wt') {
        return [pscustomobject]@{
            category = 'sealed_protected'; cleanupCandidate = $false
            reason = 'locked worktree or named seal; never inspect content or prune.'
        }
    }
    if ($PrState -eq 'open') {
        return [pscustomobject]@{
            category = 'open_pr'; cleanupCandidate = $false
            reason = 'branch has an open PR.'
        }
    }
    if ($Tracking -match '\[ahead') {
        return [pscustomobject]@{
            category = 'ahead_unpushed'; cleanupCandidate = $false
            reason = 'upstream tracking reports local commits ahead.'
        }
    }
    if ($PrState -eq 'closed_unmerged') {
        return [pscustomobject]@{
            category = 'closed_unmerged'; cleanupCandidate = $false
            reason = 'latest PR closed without merge.'
        }
    }
    if ($Tracking -match '\[gone\]') {
        if ($Upstream -ne "origin/$Branch") {
            return [pscustomobject]@{
                category = 'unknown'; cleanupCandidate = $false
                reason = 'gone upstream is not the exact origin branch; preserve because another remote cannot authorize cleanup.'
            }
        }
        if ($PrState -ne 'merged') {
            return [pscustomobject]@{
                category = 'unknown'; cleanupCandidate = $false
                reason = 'upstream is gone but no merged latest PR was observed.'
            }
        }
        if ($PrHeadState -eq 'mismatch') {
            return [pscustomobject]@{
                category = 'ahead_unpushed'; cleanupCandidate = $false
                reason = 'local HEAD differs from the latest merged PR head; preserve as possible unpushed or rewritten work.'
            }
        }
        if ($PrHeadState -ne 'match') {
            return [pscustomobject]@{
                category = 'unknown'; cleanupCandidate = $false
                reason = 'latest merged PR head SHA was not available for comparison.'
            }
        }
        if ($DirtyState -eq 'clean') {
            return [pscustomobject]@{
                category = 'merged_gone_clean'; cleanupCandidate = $true
                reason = 'latest PR merged, upstream gone, and current worktree status clean.'
            }
        }
        if ($DirtyState -eq 'dirty') {
            return [pscustomobject]@{
                category = 'merged_gone_dirty'; cleanupCandidate = $false
                reason = 'latest PR merged and upstream gone, but worktree has tracked or untracked changes.'
            }
        }
        return [pscustomobject]@{
            category = 'unknown'; cleanupCandidate = $false
            reason = 'merged/gone candidate could not be classified clean or dirty.'
        }
    }
    [pscustomobject]@{
        category = 'unknown'; cleanupCandidate = $false
        reason = 'no cleanup-safe merged/gone state was observed.'
    }
}
# --- selftest ---------------------------------------------------------------

function Invoke-SelfTest {
    $cases = @(
        @{ name = 'dirty-under';  got = (Test-DirtyVolume 3 5 30).level;   expect = 'ok'   }
        @{ name = 'dirty-over';   got = (Test-DirtyVolume 10 40 30).level;  expect = 'warn' }
        @{ name = 'dirty-edge';   got = (Test-DirtyVolume 15 15 30).level;  expect = 'ok'   }  # total 30, not > 30
        @{ name = 'wt-under';     got = (Test-WorktreeSprawl 3 4).level;    expect = 'ok'   }
        @{ name = 'wt-over';      got = (Test-WorktreeSprawl 7 4).level;    expect = 'warn' }
        @{ name = 'wt-edge';      got = (Test-WorktreeSprawl 4 4).level;    expect = 'ok'   }  # 4, not > 4
        @{ name = 'enf-clean';    got = (Test-MachineLocalEnforcement @('.agents/hooks/a.py') @('.agents/hooks/a.py')).level; expect = 'ok' }
        @{ name = 'enf-orphan';   got = (Test-MachineLocalEnforcement @('.agents/hooks/guard.py') @('.agents/hooks/other.py')).level; expect = 'warn' }
        @{ name = 'enf-partial';  got = (Test-MachineLocalEnforcement @('.agents/hooks/a.py', '.agents/hooks/b.py') @('.agents/hooks/a.py')).level; expect = 'warn' }
        @{ name = 'enf-none';     got = (Test-MachineLocalEnforcement @() @('.agents/hooks/a.py')).level; expect = 'ok' }
        @{ name = 'enf-no-main';  got = (Test-MachineLocalEnforcement @('.agents/hooks/guard.py') @() $false).level; expect = 'ok' }
        @{ name = 'pr-closed';     got = (Select-PrStateRecord ([pscustomobject]@{ state='merged'; createdAt=[datetime]'2026-02-01' }) ([pscustomobject]@{ state='closed_unmerged'; createdAt=[datetime]'2026-01-01' })).state; expect = 'closed_unmerged' }
        @{ name = 'pr-open';       got = (Select-PrStateRecord ([pscustomobject]@{ state='closed_unmerged'; createdAt=[datetime]'2026-02-01' }) ([pscustomobject]@{ state='open'; createdAt=[datetime]'2026-01-01' })).state; expect = 'open' }
        @{ name = 'pr-merged-new'; got = (Select-PrStateRecord ([pscustomobject]@{ state='merged'; createdAt=[datetime]'2026-01-01' }) ([pscustomobject]@{ state='merged'; createdAt=[datetime]'2026-02-01' })).createdAt.ToString('yyyy-MM-dd'); expect = '2026-02-01' }
        @{ name = 'class-open';   got = (Resolve-WorktreeCategory 'lane' 'C:\wt-lane' '[gone]' 'open' $false 'clean').category; expect = 'open_pr' }
        @{ name = 'class-ahead';  got = (Resolve-WorktreeCategory 'lane' 'C:\wt-lane' '[ahead 2]' 'none' $false 'not_checked').category; expect = 'ahead_unpushed' }
        @{ name = 'class-closed'; got = (Resolve-WorktreeCategory 'lane' 'C:\wt-lane' '[gone]' 'closed_unmerged' $false 'clean').category; expect = 'closed_unmerged' }
        @{ name = 'class-seal';   got = (Resolve-WorktreeCategory 'pilot-seal-outcome' 'C:\orca-seal-wt' '[gone]' 'merged' $false 'clean').category; expect = 'sealed_protected' }
        @{ name = 'class-clean';  got = (Resolve-WorktreeCategory 'lane' 'C:\wt-lane' '[gone]' 'merged' $false 'clean' 'match' 'origin/lane').category; expect = 'merged_gone_clean' }
        @{ name = 'class-dirty';  got = (Resolve-WorktreeCategory 'lane' 'C:\wt-lane' '[gone]' 'merged' $false 'dirty' 'match' 'origin/lane').category; expect = 'merged_gone_dirty' }
        @{ name = 'class-head';   got = (Resolve-WorktreeCategory 'lane' 'C:\wt-lane' '[gone]' 'merged' $false 'clean' 'mismatch' 'origin/lane').category; expect = 'ahead_unpushed' }
        @{ name = 'class-remote'; got = (Resolve-WorktreeCategory 'lane' 'C:\wt-lane' '[gone]' 'merged' $false 'clean' 'match' 'other/lane').category; expect = 'unknown' }
        @{ name = 'class-no-pr';  got = (Resolve-WorktreeCategory 'lane' 'C:\wt-lane' '[gone]' 'none' $false 'clean').category; expect = 'unknown' }
        @{ name = 'class-live';   got = (Resolve-WorktreeCategory 'lane' 'C:\wt-lane' '' 'merged' $false 'not_checked').category; expect = 'unknown' }
    )
    $ok = $true
    foreach ($c in $cases) {
        $pass = $c.got -eq $c.expect
        if (-not $pass) { $ok = $false }
        Write-Host ("{0}  {1,-12} expect={2,-5} got={3,-5}" -f ($(if ($pass) { 'PASS' } else { 'FAIL' })), $c.name, $c.expect, $c.got)
    }
    if ($ok) { Write-Host 'SELFTEST OK' -ForegroundColor Green; return 0 }
    Write-Host 'SELFTEST FAILED' -ForegroundColor Red
    return 1
}

if ($SelfTest) { exit (Invoke-SelfTest) }
function Get-WorktreeRecords([string]$Root) {
    $raw = @(git -C $Root worktree list --porcelain 2>$null)
    if ($LASTEXITCODE -ne 0) { throw 'git worktree list failed.' }
    $records = [System.Collections.Generic.List[object]]::new()
    $current = $null
    foreach ($line in @($raw) + @('')) {
        if ([string]::IsNullOrWhiteSpace($line)) {
            if ($null -ne $current) {
                $records.Add([pscustomobject]$current)
                $current = $null
            }
            continue
        }
        if ($line -match '^worktree (.+)$') {
            $current = [ordered]@{
                path = $Matches[1]; head = ''; branch = ''; locked = $false
                lockReason = ''; prunable = $false
            }
            continue
        }
        if ($null -eq $current) { continue }
        if ($line -match '^HEAD (.+)$') { $current.head = $Matches[1]; continue }
        if ($line -match '^branch refs/heads/(.+)$') { $current.branch = $Matches[1]; continue }
        if ($line -match '^locked(?: (.*))?$') {
            $current.locked = $true; $current.lockReason = $Matches[1]; continue
        }
        if ($line -match '^prunable(?: .*)?$') { $current.prunable = $true; continue }
    }
    @($records)
}

function Get-BranchStateMap([string]$Root) {
    $raw = @(git -C $Root for-each-ref '--format=%(refname:short)%09%(upstream:short)%09%(upstream:track)' refs/heads 2>$null)
    if ($LASTEXITCODE -ne 0) { throw 'git for-each-ref failed.' }
    $map = @{}
    foreach ($line in $raw) {
        $parts = @($line -split "`t", 3)
        if ($parts.Count -lt 1 -or -not $parts[0]) { continue }
        $map[$parts[0]] = [pscustomobject]@{
            upstream = $(if ($parts.Count -ge 2) { $parts[1] } else { '' })
            tracking = $(if ($parts.Count -ge 3) { $parts[2] } else { '' })
        }
    }
    $map
}

function Resolve-GitHubRepo([string]$Root, [string]$ExplicitRepo) {
    if ($ExplicitRepo) { return $ExplicitRepo }
    $origin = git -C $Root remote get-url origin 2>$null
    if ($LASTEXITCODE -ne 0 -or -not $origin) { throw 'cannot resolve origin remote for GitHub PR reads.' }
    if ($origin -match 'github\.com[:/](?<owner>[^/]+)/(?<repo>[^/]+?)(?:\.git)?$') {
        return "$($Matches.owner)/$($Matches.repo)"
    }
    throw "origin is not a recognized GitHub remote: $origin"
}

function Get-PrStateMap([string]$Repo) {
    if (-not (Get-Command gh -ErrorAction SilentlyContinue)) { throw 'gh not found on PATH.' }
    $repoOwner = ($Repo -split '/', 2)[0]
    $raw = @(gh pr list --repo $Repo --state all --limit 2000 --json number,headRefName,headRefOid,state,mergedAt,url,createdAt,isCrossRepository,headRepositoryOwner 2>$null)
    if ($LASTEXITCODE -ne 0) { throw "gh pr list failed for $Repo." }
    try { $rows = @(($raw -join "`n") | ConvertFrom-Json) }
    catch { throw "gh pr list returned invalid JSON for $Repo." }
    if ($rows.Count -ge 2000) { throw 'gh pr list reached the 2000-row limit; PR history completeness is unproven.' }
    $map = @{}
    foreach ($row in $rows) {
        if (-not $row.headRefName) { continue }
        if ($row.isCrossRepository -or $row.headRepositoryOwner.login -ne $repoOwner) { continue }
        $created = [datetime]$row.createdAt
        $state = if ($row.state -eq 'OPEN') { 'open' } elseif ($row.mergedAt) { 'merged' } else { 'closed_unmerged' }
        $candidate = [pscustomobject]@{
            state = $state; number = $row.number; url = $row.url; createdAt = $created; headRefOid = $row.headRefOid
        }
        $current = if ($map.ContainsKey($row.headRefName)) { $map[$row.headRefName] } else { $null }
        $map[$row.headRefName] = Select-PrStateRecord $current $candidate
    }
    $map
}

function Get-WorktreeDirtyState([string]$Path) {
    if (-not (Test-Path -LiteralPath $Path)) {
        return [pscustomobject]@{ state = 'unknown'; detail = 'worktree path does not exist.' }
    }
    $lines = @(git -C $Path status --porcelain --untracked-files=normal 2>$null)
    if ($LASTEXITCODE -ne 0) {
        return [pscustomobject]@{ state = 'unknown'; detail = 'git status failed.' }
    }
    if ($lines.Count -eq 0) {
        return [pscustomobject]@{ state = 'clean'; detail = 'no tracked or untracked changes observed.' }
    }
    [pscustomobject]@{ state = 'dirty'; detail = "$($lines.Count) status entr$(if ($lines.Count -eq 1) { 'y' } else { 'ies' }) observed." }
}

function Get-WorktreeClassification([string]$Root, [string]$Repo) {
    $timer = [System.Diagnostics.Stopwatch]::StartNew()
    $worktrees = @(Get-WorktreeRecords $Root)
    $branchStates = Get-BranchStateMap $Root
    $prStates = Get-PrStateMap $Repo
    $entries = [System.Collections.Generic.List[object]]::new()

    for ($i = 1; $i -lt $worktrees.Count; $i++) {
        $wt = $worktrees[$i]
        $branchState = if ($wt.branch -and $branchStates.ContainsKey($wt.branch)) {
            $branchStates[$wt.branch]
        } else { [pscustomobject]@{ upstream = ''; tracking = '' } }
        $pr = if ($wt.branch -and $prStates.ContainsKey($wt.branch)) {
            $prStates[$wt.branch]
        } else { [pscustomobject]@{ state = 'none'; number = $null; url = ''; createdAt = $null; headRefOid = '' } }
        $prHeadState = if ($pr.state -ne 'merged') {
            'not_applicable'
        } elseif (-not $pr.headRefOid) {
            'unknown'
        } elseif ($wt.head -eq $pr.headRefOid) {
            'match'
        } else {
            'mismatch'
        }
        $dirty = [pscustomobject]@{ state = 'not_checked'; detail = 'not a merged/gone cleanup candidate.' }
        $decision = Resolve-WorktreeCategory $wt.branch $wt.path $branchState.tracking $pr.state $wt.locked $dirty.state $prHeadState $branchState.upstream
        if ($decision.category -eq 'unknown' -and $branchState.upstream -eq "origin/$($wt.branch)" -and $branchState.tracking -match '\[gone\]' -and $pr.state -eq 'merged' -and $prHeadState -eq 'match' -and -not $wt.locked) {
            $dirty = Get-WorktreeDirtyState $wt.path
            $decision = Resolve-WorktreeCategory $wt.branch $wt.path $branchState.tracking $pr.state $wt.locked $dirty.state $prHeadState $branchState.upstream
        }
        $entries.Add([pscustomobject]@{
            path = $wt.path
            branch = $wt.branch
            head = $wt.head
            upstream = $branchState.upstream
            tracking = $branchState.tracking
            prState = $pr.state
            prNumber = $pr.number
            prUrl = $pr.url
            prHeadOid = $pr.headRefOid
            prHeadState = $prHeadState
            locked = $wt.locked
            prunable = $wt.prunable
            dirtyState = $dirty.state
            dirtyDetail = $dirty.detail
            category = $decision.category
            cleanupCandidate = $decision.cleanupCandidate
            reason = $decision.reason
        })
    }

    $counts = [ordered]@{}
    foreach ($entry in $entries) {
        if (-not $counts.Contains($entry.category)) { $counts[$entry.category] = 0 }
        $counts[$entry.category]++
    }
    $timer.Stop()
    [pscustomobject]@{
        observedAtUtc = [datetime]::UtcNow.ToString('o')
        githubRepo = $Repo
        linkedWorktrees = $entries.Count
        elapsedSeconds = [math]::Round($timer.Elapsed.TotalSeconds, 3)
        counts = $counts
        cleanupCandidates = @($entries | Where-Object cleanupCandidate)
        entries = @($entries)
        boundary = 'Read-only volatile classification. Re-derive before action; non-force removal and all doctrine guards still apply.'
    }
}

# --- IO: gather real state (read-only) --------------------------------------

# helper-delta vs _common.ps1 Stop-WithError/Resolve-RepoRoot: this read-only
# diagnostic aborts with exit 2 and honors a -RepoPath override; kept local.
if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    Write-Host 'ABORTED: git not found on PATH.' -ForegroundColor Red; exit 2
}
if (-not $RepoPath) {
    $RepoPath = git rev-parse --show-toplevel 2>$null
    if ($LASTEXITCODE -ne 0 -or -not $RepoPath) {
        Write-Host 'ABORTED: not inside a git repository (pass -RepoPath).' -ForegroundColor Red; exit 2
    }
}
if (-not (Test-Path $RepoPath)) {
    Write-Host "ABORTED: path does not exist: $RepoPath" -ForegroundColor Red; exit 2
}
$RepoPath = (Resolve-Path $RepoPath).Path
git -C $RepoPath rev-parse --show-toplevel *> $null
if ($LASTEXITCODE -ne 0) {
    Write-Host "ABORTED: not a git repository: $RepoPath" -ForegroundColor Red; exit 2
}

if ($ClassifyWorktrees -and -not $Fetch) {
    Write-Host 'ABORTED: -ClassifyWorktrees requires -Fetch so [gone]/ahead state is freshly pruned.' -ForegroundColor Red
    exit 2
}
if ($Fetch) {
    git -C $RepoPath fetch --prune origin --quiet 2>&1 | Out-Null
    if ($LASTEXITCODE -ne 0) {
        Write-Host 'ABORTED: git fetch --prune origin failed; remote state is not fresh.' -ForegroundColor Red
        exit 2
    }
}

$branch = git -C $RepoPath rev-parse --abbrev-ref HEAD 2>$null

# 1) dirty volume
$porcelain = @(git -C $RepoPath status --porcelain 2>$null)
$modified  = @($porcelain | Where-Object { $_ -and $_ -notmatch '^\?\?' }).Count
$untracked = @($porcelain | Where-Object { $_ -match '^\?\?' }).Count

# 2) worktrees - exclude the main worktree (always the first entry) so the count
#    reflects lane worktrees only
$wtTotal  = @(git -C $RepoPath worktree list --porcelain 2>$null | Where-Object { $_ -match '^worktree ' }).Count
$wtLinked = [Math]::Max(0, $wtTotal - 1)

# 3) machine-local enforcement: local hooks vs origin/main hooks. No
#    --exclude-standard, so a hook that is both untracked AND git-ignored (the most
#    invisible machine-local enforcement) is still seen.
git -C $RepoPath rev-parse --verify --quiet origin/main *> $null
$mainAvailable = ($LASTEXITCODE -eq 0)
$localHooks = @(git -C $RepoPath ls-files --others --cached -- '.agents/hooks/' 2>$null |
    Where-Object { $_ -match '\.py$' } | Sort-Object -Unique)
$mainHooks = @()
if ($mainAvailable) {
    $mainHooks = @(git -C $RepoPath ls-tree -r --name-only origin/main -- '.agents/hooks/' 2>$null |
        Where-Object { $_ -match '\.py$' })
}

$findings = @(
    Test-DirtyVolume $modified $untracked $DirtyThreshold
    Test-WorktreeSprawl $wtLinked $WorktreeThreshold
    Test-MachineLocalEnforcement $localHooks $mainHooks $mainAvailable
)
$warns = @($findings | Where-Object { $_.level -eq 'warn' })

$classification = $null
if ($ClassifyWorktrees) {
    try {
        $resolvedRepo = Resolve-GitHubRepo $RepoPath $GitHubRepo
        $classification = Get-WorktreeClassification $RepoPath $resolvedRepo
    }
    catch {
        Write-Host "ABORTED: worktree classification failed: $($_.Exception.Message)" -ForegroundColor Red
        exit 2
    }
}

if ($Json) {
    $output = [ordered]@{
        repoPath      = $RepoPath
        branch        = $branch
        originMainRef = $(if ($Fetch) { 'fetched+pruned' } elseif ($mainAvailable) { 'local-ref (use -Fetch to refresh)' } else { 'unavailable' })
        findings      = $findings
        warnings      = $warns.Count
    }
    if ($ClassifyWorktrees) { $output.worktreeClassification = $classification }
    [pscustomobject]$output | ConvertTo-Json -Depth 8
    exit $(if ($warns.Count -gt 0) { 1 } else { 0 })
}

Write-Host "Lane health check - $RepoPath"
Write-Host "  branch: $branch    origin/main: $(if ($Fetch) { 'fetched' } elseif ($mainAvailable) { 'local ref (use -Fetch to refresh)' } else { 'unavailable' })"
Write-Host ''
foreach ($f in $findings) {
    $isWarn = $f.level -eq 'warn'
    Write-Host ("  [{0}] {1,-26} {2}" -f ($(if ($isWarn) { 'WARN' } else { ' ok ' })), $f.check, $f.message) -ForegroundColor ($(if ($isWarn) { 'Yellow' } else { 'Green' }))
}
Write-Host ''
if ($ClassifyWorktrees) {
    Write-Host "Read-only worktree classification - $($classification.observedAtUtc)"
    Write-Host "  linked worktrees: $($classification.linkedWorktrees)    elapsed: $($classification.elapsedSeconds)s"
    foreach ($item in $classification.counts.GetEnumerator()) {
        Write-Host ("  {0,-24} {1}" -f $item.Key, $item.Value)
    }
    Write-Host "  cleanup candidates: $($classification.cleanupCandidates.Count)"
    foreach ($candidate in $classification.cleanupCandidates) {
        Write-Host "    $($candidate.branch)  $($candidate.path)"
    }
    Write-Host "  Boundary: $($classification.boundary)"
    Write-Host ''
}
if ($warns.Count -gt 0) {
    Write-Host "$($warns.Count) warning(s) - detection nudge, not a block." -ForegroundColor Yellow
    exit 1
}
Write-Host 'healthy.' -ForegroundColor Green
exit 0
