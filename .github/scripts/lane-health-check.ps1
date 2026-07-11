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
      4. stale-worktrees       - linked worktrees whose newest observable material
                                 signal is older than -StaleAfterHours. Every stale
                                 record retains independent open-PR, dirty,
                                 ahead/unpushed, sealed/locked, and unknown guards.

    Stale-worktree telemetry is classification only. It never emits cleanup
    commands or cleanup authority. Per-worktree reads run as owned child processes
    with both per-command and whole-run deadlines. A timeout is reported as
    incomplete evidence; it is never inferred safe. This command currently fails
    closed on non-Windows runtimes before starting telemetry subprocesses because
    equivalent descendant containment is not proven there.

    Exit codes: 0 = healthy (no warnings); 1 = one or more warnings (detection
    nudge); 2 = usage, prerequisite, containment, or essential-inventory abort.
    Use -Json for machine output, -SelfTest to validate detection logic without touching git.

.PARAMETER RepoPath
    Repository working tree to inspect. Default: the git toplevel of the cwd.

.PARAMETER DirtyThreshold
    Warn when modified+untracked file count exceeds this. Default 30.

.PARAMETER WorktreeThreshold
    Warn when the repo has more than this many linked worktrees (the main worktree
    is not counted). Default 4.

.PARAMETER Fetch
    Opt in to `git fetch origin` so the not-on-main check compares against an
    up-to-date origin/main. The fetch updates only remote-tracking refs and
    FETCH_HEAD, not the working tree, index, or local branches. `-QueryPullRequests`
    is the detector's other opt-in, read-only network action.

.PARAMETER StaleAfterHours
    Classify a linked worktree as stale when its newest observable material signal
    is more than this many hours before the observation time. Default 48.

.PARAMETER AsOfUtc
    Optional ISO-8601 observation time for deterministic tests. Repository and PR
    state remain live, so this is not a historical replay control.

.PARAMETER ClockSkewToleranceSeconds
    Allow material timestamps up to this many seconds after the observation time.
    Later timestamps become explicit unknown evidence. Default 300.

.PARAMETER QueryPullRequests
    Opt in to a bounded, read-only `gh pr list` query. Without it, PR evidence is
    explicitly unknown.

.PARAMETER CommandTimeoutMs
    Maximum normal execution time for one owned git/gh command or lane worker.
    Bounded containment/drain occurs inside the overall budget. Default 4000 ms.

.PARAMETER OverallTimeoutMs
    Monotonic subprocess budget including containment and stream drain. Default
    45000 ms; coordinator-only serialization may add a small bounded tail.

.PARAMETER ProtectedLaneName
    Exact worktree leaf or branch names treated as protected in addition to Git's
    locked marker. Defaults retain the historical `orca-seal-wt` compatibility
    guard plus current Forseti/pilot seal names.

.PARAMETER Json
    Emit findings as JSON instead of human-readable text.

.PARAMETER SelfTest
    Run the detection logic against synthetic inputs and exit (0 ok / 1 fail).

.EXAMPLE
    pwsh .github/scripts/lane-health-check.ps1

.EXAMPLE
    pwsh .github/scripts/lane-health-check.ps1 -RepoPath C:\path\to\repo -Fetch

.EXAMPLE
    pwsh .github/scripts/lane-health-check.ps1 -Json -QueryPullRequests -AsOfUtc 2026-07-11T00:00:00Z

.EXAMPLE
    pwsh .github/scripts/lane-health-check.ps1 -SelfTest
#>
[CmdletBinding()]
param(
    [string]$RepoPath,
    [int]$DirtyThreshold = 30,
    [int]$WorktreeThreshold = 4,
    [ValidateRange(1, 87600)]
    [int]$StaleAfterHours = 48,
    [string]$AsOfUtc,
    [ValidateRange(0, 86400)]
    [int]$ClockSkewToleranceSeconds = 300,
    [switch]$QueryPullRequests,
    [ValidateRange(100, 60000)]
    [int]$CommandTimeoutMs = 4000,
    [ValidateRange(1000, 60000)]
    [int]$OverallTimeoutMs = 45000,
    [string[]]$ProtectedLaneName = @('orca-seal-wt', 'forseti-seal-wt', 'pilot-seal-outcome'),
    [switch]$Fetch,
    [switch]$Json,
    [switch]$SelfTest,
    [switch]$InternalWorktreeProbe,
    [string]$ProbePath,
    [long]$ProbeHeadEpoch,
    [long]$ProbeCutoffEpoch,
    [long]$ProbeObservationEpoch,
    [int]$ProbeClockSkewToleranceSeconds
)

$ErrorActionPreference = 'Stop'

# Windows process-tree ownership is enforced with a named, kill-on-close Job
# Object. Internal workers use the name to prove membership in the coordinator's
# specific job before touching Git or the filesystem.
$script:UseWindowsJobIsolation = [bool]$IsWindows -and -not $InternalWorktreeProbe
if ($script:UseWindowsJobIsolation -and -not ('ForsetiOwnedProcessJob' -as [type])) {
    Add-Type -TypeDefinition @"
using System;
using System.ComponentModel;
using System.Diagnostics;
using System.Runtime.InteropServices;
using System.Threading;

public sealed class ForsetiOwnedProcessJob : IDisposable
{
    private const uint JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE = 0x00002000;
    private IntPtr handle;

    [StructLayout(LayoutKind.Sequential)]
    private struct JOBOBJECT_BASIC_LIMIT_INFORMATION
    {
        public long PerProcessUserTimeLimit;
        public long PerJobUserTimeLimit;
        public uint LimitFlags;
        public UIntPtr MinimumWorkingSetSize;
        public UIntPtr MaximumWorkingSetSize;
        public uint ActiveProcessLimit;
        public UIntPtr Affinity;
        public uint PriorityClass;
        public uint SchedulingClass;
    }

    [StructLayout(LayoutKind.Sequential)]
    private struct IO_COUNTERS
    {
        public ulong ReadOperationCount;
        public ulong WriteOperationCount;
        public ulong OtherOperationCount;
        public ulong ReadTransferCount;
        public ulong WriteTransferCount;
        public ulong OtherTransferCount;
    }

    [StructLayout(LayoutKind.Sequential)]
    private struct JOBOBJECT_EXTENDED_LIMIT_INFORMATION
    {
        public JOBOBJECT_BASIC_LIMIT_INFORMATION BasicLimitInformation;
        public IO_COUNTERS IoInfo;
        public UIntPtr ProcessMemoryLimit;
        public UIntPtr JobMemoryLimit;
        public UIntPtr PeakProcessMemoryUsed;
        public UIntPtr PeakJobMemoryUsed;
    }

    [StructLayout(LayoutKind.Sequential)]
    private struct JOBOBJECT_BASIC_ACCOUNTING_INFORMATION
    {
        public long TotalUserTime;
        public long TotalKernelTime;
        public long ThisPeriodTotalUserTime;
        public long ThisPeriodTotalKernelTime;
        public uint TotalPageFaultCount;
        public uint TotalProcesses;
        public uint ActiveProcesses;
        public uint TotalTerminatedProcesses;
    }

    [DllImport("kernel32.dll", CharSet = CharSet.Unicode, SetLastError = true)]
    private static extern IntPtr CreateJobObject(IntPtr securityAttributes, string name);


    [DllImport("kernel32.dll", SetLastError = true)]
    private static extern bool SetInformationJobObject(
        IntPtr job, int infoClass, ref JOBOBJECT_EXTENDED_LIMIT_INFORMATION info, uint length);

    [DllImport("kernel32.dll", SetLastError = true)]
    private static extern bool AssignProcessToJobObject(IntPtr job, IntPtr process);


    [DllImport("kernel32.dll", SetLastError = true)]
    private static extern bool TerminateJobObject(IntPtr job, uint exitCode);

    [DllImport("kernel32.dll", SetLastError = true)]
    private static extern bool QueryInformationJobObject(
        IntPtr job, int infoClass, out JOBOBJECT_BASIC_ACCOUNTING_INFORMATION info,
        uint length, IntPtr returnLength);

    [DllImport("kernel32.dll", SetLastError = true)]
    private static extern bool CloseHandle(IntPtr handle);

    public ForsetiOwnedProcessJob(string name)
    {
        if (String.IsNullOrWhiteSpace(name)) throw new ArgumentException("job name is required", "name");
        handle = CreateJobObject(IntPtr.Zero, name);
        if (handle == IntPtr.Zero) throw new Win32Exception(Marshal.GetLastWin32Error());
        var info = new JOBOBJECT_EXTENDED_LIMIT_INFORMATION();
        info.BasicLimitInformation.LimitFlags = JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE;
        if (!SetInformationJobObject(
            handle, 9, ref info, (uint)Marshal.SizeOf(typeof(JOBOBJECT_EXTENDED_LIMIT_INFORMATION))))
        {
            int error = Marshal.GetLastWin32Error();
            CloseHandle(handle);
            handle = IntPtr.Zero;
            throw new Win32Exception(error);
        }
    }

    public void Assign(int processId)
    {
        using (var process = Process.GetProcessById(processId))
        {
            if (!AssignProcessToJobObject(handle, process.Handle))
                throw new Win32Exception(Marshal.GetLastWin32Error());
        }
    }


    public bool TerminateAndWait(int timeoutMs)
    {
        if (handle == IntPtr.Zero) return true;
        if (!TerminateJobObject(handle, 1)) return false;
        var watch = Stopwatch.StartNew();
        while (true)
        {
            JOBOBJECT_BASIC_ACCOUNTING_INFORMATION info;
            if (!QueryInformationJobObject(
                handle, 1, out info,
                (uint)Marshal.SizeOf(typeof(JOBOBJECT_BASIC_ACCOUNTING_INFORMATION)),
                IntPtr.Zero)) return false;
            if (info.ActiveProcesses == 0) return true;
            if (watch.ElapsedMilliseconds >= timeoutMs) return false;
            Thread.Sleep(Math.Min(10, Math.Max(1, timeoutMs - (int)watch.ElapsedMilliseconds)));
        }
    }

    public bool Close()
    {
        if (handle == IntPtr.Zero) return true;
        IntPtr value = handle;
        handle = IntPtr.Zero;
        return CloseHandle(value);
    }

    public void Dispose() { Close(); }
}
"@
}
if ([bool]$IsWindows -and $InternalWorktreeProbe -and -not ('ForsetiJobMembership' -as [type])) {
    Add-Type -TypeDefinition @"
using System;
using System.ComponentModel;
using System.Diagnostics;
using System.Runtime.InteropServices;

public static class ForsetiJobMembership
{
    private const uint JOB_OBJECT_QUERY = 0x0004;

    [DllImport("kernel32.dll", CharSet = CharSet.Unicode, SetLastError = true)]
    private static extern IntPtr OpenJobObject(uint desiredAccess, bool inheritHandle, string name);

    [DllImport("kernel32.dll", SetLastError = true)]
    private static extern bool IsProcessInJob(IntPtr process, IntPtr job, out bool result);

    [DllImport("kernel32.dll", SetLastError = true)]
    private static extern bool CloseHandle(IntPtr handle);

    public static bool IsCurrentProcessInNamedJob(string name)
    {
        if (String.IsNullOrWhiteSpace(name)) return false;
        IntPtr job = OpenJobObject(JOB_OBJECT_QUERY, false, name);
        if (job == IntPtr.Zero) return false;
        try
        {
            using (var process = Process.GetCurrentProcess())
            {
                bool result;
                if (!IsProcessInJob(process.Handle, job, out result))
                    throw new Win32Exception(Marshal.GetLastWin32Error());
                return result;
            }
        }
        finally
        {
            CloseHandle(job);
        }
    }
}
"@
}
$script:PwshExecutable = (Get-Command pwsh -ErrorAction Stop).Source

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


function Test-IsStale([datetime]$LastMaterialUtc, [datetime]$CutoffUtc) {
    $LastMaterialUtc.ToUniversalTime() -lt $CutoffUtc.ToUniversalTime()
}

function Test-IsFutureSkew(
    [datetime]$MaterialUtc,
    [datetime]$ObservationUtc,
    [int]$ToleranceSeconds
) {
    $MaterialUtc.ToUniversalTime() -gt $ObservationUtc.ToUniversalTime().AddSeconds($ToleranceSeconds)
}

function Resolve-StaleClassification(
    [bool]$Protected,
    [AllowNull()][Nullable[bool]]$OpenPr,
    [bool]$Dirty,
    [bool]$AheadOrUnpushed,
    [AllowNull()][Nullable[bool]]$Merged,
    [AllowNull()][Nullable[bool]]$ClosedUnmerged
) {
    if ($Protected) { return 'sealed_or_protected' }
    if ($OpenPr -eq $true) { return 'open_pr' }
    if ($AheadOrUnpushed) { return 'ahead_or_unpushed' }
    if ($Dirty -and $Merged -eq $true) { return 'merged_or_gone_dirty' }
    if ($Dirty) { return 'dirty' }
    if ($OpenPr -eq $null -or $Merged -eq $null -or $ClosedUnmerged -eq $null) {
        return 'unknown'
    }
    if ($Merged -eq $true) { return 'merged_or_gone_clean' }
    if ($ClosedUnmerged -eq $true) { return 'closed_unmerged' }
    'unknown'
}

function Resolve-AheadOrUnpushed(
    [bool]$Detached,
    [AllowNull()][string]$Upstream,
    [AllowNull()][string]$Track,
    [AllowNull()][Nullable[bool]]$Merged
) {
    if ($Detached -or -not $Upstream -or $Track -match '\[gone\]') {
        return $Merged -ne $true
    }
    [bool]($Track -match '\[ahead')
}
function Test-StaleWorktrees(
    [int]$StaleCount,
    [int]$UnknownAgeCount,
    [int]$UnknownGuardCount,
    [int]$TerminationFailureCount,
    [int]$Hours
) {
    if ($UnknownAgeCount -gt 0 -or $UnknownGuardCount -gt 0 -or $TerminationFailureCount -gt 0) {
        return New-Finding 'stale-worktrees' 'warn' (
            "telemetry incomplete: stale=$StaleCount, unknown_age=$UnknownAgeCount, " +
            "unknown_guards=$UnknownGuardCount, termination_failures=$TerminationFailureCount " +
            "at $Hours hours; missing evidence was not inferred safe.")
    }
    if ($StaleCount -gt 0) {
        return New-Finding 'stale-worktrees' 'warn' (
            "$StaleCount linked worktree(s) exceed the $Hours-hour material-age horizon; " +
            'classification only, with no cleanup authority.')
    }
    New-Finding 'stale-worktrees' 'ok' "no linked worktree exceeds the $Hours-hour material-age horizon."
}

function Test-ExecutionEvidence([pscustomobject]$Stats) {
    $incomplete = (
        [int]$Stats.timedOut -gt 0 -or [int]$Stats.notStarted -gt 0 -or
        [int]$Stats.failed -gt 0 -or [int]$Stats.terminationFailures -gt 0
    )
    if ($incomplete) {
        return New-Finding 'execution-evidence' 'warn' (
            "subprocess evidence incomplete: timed_out=$($Stats.timedOut), " +
            "not_started=$($Stats.notStarted), failed=$($Stats.failed), " +
            "termination_failures=$($Stats.terminationFailures).")
    }
    New-Finding 'execution-evidence' 'ok' 'all requested subprocess evidence completed inside the owned execution boundary.'
}

function Test-ContainmentRuntime([bool]$ContainmentComplete) {
    if (-not $ContainmentComplete) {
        return New-Finding 'process-containment' 'warn' (
            'owned descendant containment is not proven on this runtime; telemetry remains incomplete.')
    }
    New-Finding 'process-containment' 'ok' (
        'Windows Job Object containment is active with release-after-assignment supervision.')
}
function Test-RequestedRemoteEvidence(
    [bool]$FetchRequested,
    [bool]$FetchSucceeded,
    [bool]$PrRequested,
    [bool]$PrAvailable,
    [bool]$PrComplete
) {
    $complete = ((-not $FetchRequested) -or $FetchSucceeded) -and (
        (-not $PrRequested) -or ($PrAvailable -and $PrComplete)
    )
    if (-not $complete) {
        return New-Finding 'remote-evidence' 'warn' (
            'requested fetch or PR evidence is unavailable/incomplete; remote guards remain unknown.')
    }
    New-Finding 'remote-evidence' 'ok' 'all requested remote evidence completed.'
}
function Resolve-TelemetryStatus(
    [int]$UnknownAgeCount,
    [int]$UnknownGuardCount,
    [pscustomobject]$Stats,
    [bool]$ContainmentComplete,
    [bool]$RequestedRemoteEvidenceComplete
) {
    if (-not $ContainmentComplete -or -not $RequestedRemoteEvidenceComplete -or $UnknownAgeCount -gt 0 -or $UnknownGuardCount -gt 0 -or
        [int]$Stats.timedOut -gt 0 -or [int]$Stats.notStarted -gt 0 -or
        [int]$Stats.failed -gt 0 -or [int]$Stats.terminationFailures -gt 0) {
        return 'incomplete'
    }
    'complete'
}
function ConvertFrom-WorktreePorcelain([string[]]$Lines) {
    $records = [Collections.Generic.List[object]]::new()
    $current = $null
    foreach ($line in @($Lines) + @('')) {
        if (-not $line) {
            if ($null -ne $current) {
                $records.Add([pscustomobject]$current)
                $current = $null
            }
            continue
        }
        if ($line.StartsWith('worktree ')) {
            if ($null -ne $current) { $records.Add([pscustomobject]$current) }
            $current = [ordered]@{
                path = $line.Substring(9); head = $null; branch = $null
                detached = $false; locked = $false; lockReason = $null
                prunable = $false; prunableReason = $null
            }
            continue
        }
        if ($null -eq $current) { continue }
        if ($line.StartsWith('HEAD ')) { $current.head = $line.Substring(5); continue }
        if ($line.StartsWith('branch refs/heads/')) { $current.branch = $line.Substring(18); continue }
        if ($line -eq 'detached') { $current.detached = $true; continue }
        if ($line -eq 'locked') { $current.locked = $true; continue }
        if ($line.StartsWith('locked ')) {
            $current.locked = $true
            $current.lockReason = $line.Substring(7)
            continue
        }
        if ($line -eq 'prunable') { $current.prunable = $true; continue }
        if ($line.StartsWith('prunable ')) {
            $current.prunable = $true
            $current.prunableReason = $line.Substring(9)
        }
    }
    @($records)
}

function ConvertFrom-StatusPorcelain([string]$Raw) {
    $records = [Collections.Generic.List[object]]::new()
    if (-not $Raw) { return @() }
    $tokens = $Raw.Split([char]0)
    for ($i = 0; $i -lt $tokens.Count; $i++) {
        $token = $tokens[$i]
        if (-not $token) { continue }
        if ($token.Length -lt 4 -or $token[2] -ne ' ') {
            throw 'invalid_status_porcelain'
        }
        $code = $token.Substring(0, 2)
        $records.Add([pscustomobject]@{ code = $code; path = $token.Substring(3) })
        if ($code -match '[RC]' -and $i + 1 -lt $tokens.Count) { $i += 1 }
    }
    @($records)
}

function Invoke-OwnedProcess(
    [string]$FilePath,
    [string[]]$ArgumentList,
    [long]$DeadlineTick,
    [int]$TimeoutMs
) {
    $remainingRaw = $DeadlineTick - [Environment]::TickCount64
    $remainingMs = [int][Math]::Min([int]::MaxValue, $remainingRaw)
    if ($remainingMs -le 0) {
        return [pscustomobject][ordered]@{
            started = $false; completed = $false; timedOut = $true
            terminationConfirmed = $true; exitCode = $null
            stdout = ''; stderr = ''; failure = 'overall_budget_exhausted'
            isolationMode = $(if ($script:UseWindowsJobIsolation) { 'windows_job_object' } else { 'kill_true_timeout_only' })
        }
    }
    $effectiveMs = [Math]::Max(1, [Math]::Min($TimeoutMs, $remainingMs))
    $environment = [ordered]@{
        GIT_OPTIONAL_LOCKS = '0'; GIT_TERMINAL_PROMPT = '0'
        GIT_PAGER = 'cat'; PAGER = 'cat'; LC_ALL = 'C'; LANG = 'C'
    }
    $useJob = [bool]$script:UseWindowsJobIsolation
    $isolationMode = $(if ($useJob) { 'windows_job_object' } else { 'kill_true_timeout_only' })
    $job = $null
    $jobAssigned = $false
    $payload = $null

    $psi = [Diagnostics.ProcessStartInfo]::new()
    $psi.UseShellExecute = $false
    $psi.RedirectStandardOutput = $true
    $psi.RedirectStandardError = $true
    $psi.CreateNoWindow = $true
    foreach ($entry in $environment.GetEnumerator()) { $psi.Environment[$entry.Key] = $entry.Value }

    if ($useJob) {
        try {
            $jobName = "Local\ForsetiOwnedProcess_$([guid]::NewGuid().ToString('N'))"
            $job = [ForsetiOwnedProcessJob]::new($jobName)
            $environment['FORSETI_OWNED_JOB_NAME'] = $jobName
        }
        catch {
            return [pscustomobject][ordered]@{
                started = $false; completed = $false; timedOut = $false
                terminationConfirmed = $false; exitCode = $null
                stdout = ''; stderr = ''; failure = "job_create_failed:$($_.Exception.Message)"
                isolationMode = $isolationMode
            }
        }
        $supervisorCommand = '$ErrorActionPreference=''Stop''; $payload=[Console]::In.ReadLine()|ConvertFrom-Json; $childPsi=[Diagnostics.ProcessStartInfo]::new(); $childPsi.FileName=[string]$payload.filePath; $childPsi.UseShellExecute=$false; $childPsi.RedirectStandardOutput=$true; $childPsi.RedirectStandardError=$true; $childPsi.CreateNoWindow=$true; foreach($argument in @($payload.arguments)){[void]$childPsi.ArgumentList.Add([string]$argument)}; foreach($property in $payload.environment.PSObject.Properties){$childPsi.Environment[$property.Name]=[string]$property.Value}; $child=[Diagnostics.Process]::new(); $child.StartInfo=$childPsi; if(-not $child.Start()){throw ''owned child failed to start''}; $stdoutTask=$child.StandardOutput.ReadToEndAsync(); $stderrTask=$child.StandardError.ReadToEndAsync(); $child.WaitForExit(); $exitCode=$child.ExitCode; $stdout=$stdoutTask.GetAwaiter().GetResult(); $stderr=$stderrTask.GetAwaiter().GetResult(); [Console]::Out.Write($stdout); [Console]::Error.Write($stderr); $child.Dispose(); exit $exitCode'
        $psi.FileName = $script:PwshExecutable
        [void]$psi.ArgumentList.Add('-NoProfile')
        [void]$psi.ArgumentList.Add('-NonInteractive')
        [void]$psi.ArgumentList.Add('-Command')
        [void]$psi.ArgumentList.Add($supervisorCommand)
        $psi.RedirectStandardInput = $true
        $payload = [pscustomobject][ordered]@{
            filePath = $FilePath
            arguments = @($ArgumentList)
            environment = [pscustomobject]$environment
        } | ConvertTo-Json -Depth 5 -Compress
    }
    else {
        $psi.FileName = $FilePath
        foreach ($argument in $ArgumentList) { [void]$psi.ArgumentList.Add($argument) }
    }

    $process = [Diagnostics.Process]::new()
    $process.StartInfo = $psi
    $started = $false
    try {
        $started = $process.Start()
        if (-not $started) { throw 'process_start_returned_false' }
        if ($useJob) {
            $job.Assign($process.Id)
            $jobAssigned = $true
            $process.StandardInput.WriteLine($payload)
            $process.StandardInput.Flush()
            $process.StandardInput.Close()
        }
        $stdoutTask = $process.StandardOutput.ReadToEndAsync()
        $stderrTask = $process.StandardError.ReadToEndAsync()
        if (-not $process.WaitForExit($effectiveMs)) {
            $cleanupMs = [int][Math]::Max(0, [Math]::Min(500, $DeadlineTick - [Environment]::TickCount64))
            $terminated = $false
            if ($jobAssigned) {
                $terminated = $job.TerminateAndWait($cleanupMs)
                $closed = $job.Close()
                $job = $null
                $terminated = $terminated -and $closed
            }
            else {
                try {
                    $process.Kill($true)
                    $terminated = $process.WaitForExit($cleanupMs)
                }
                catch { $terminated = $false }
            }
            return [pscustomobject][ordered]@{
                started = $true; completed = $false; timedOut = $true
                terminationConfirmed = $terminated; exitCode = $null
                stdout = $(if ($stdoutTask.IsCompleted) { $stdoutTask.GetAwaiter().GetResult() } else { '' })
                stderr = $(if ($stderrTask.IsCompleted) { $stderrTask.GetAwaiter().GetResult() } else { '' })
                failure = 'command_timeout'; isolationMode = $isolationMode
            }
        }

        $exitCode = $process.ExitCode
        $treeContained = $true
        if ($jobAssigned) {
            $cleanupMs = [int][Math]::Max(0, [Math]::Min(500, $DeadlineTick - [Environment]::TickCount64))
            $treeContained = $job.TerminateAndWait($cleanupMs)
            $closed = $job.Close()
            $job = $null
            $treeContained = $treeContained -and $closed
        }
        $drainDeadline = [Math]::Min($DeadlineTick, [Environment]::TickCount64 + 250)
        while ((-not $stdoutTask.IsCompleted -or -not $stderrTask.IsCompleted) -and
            [Environment]::TickCount64 -lt $drainDeadline) {
            Start-Sleep -Milliseconds 10
        }
        if (-not $stdoutTask.IsCompleted -or -not $stderrTask.IsCompleted) {
            return [pscustomobject][ordered]@{
                started = $true; completed = $false; timedOut = $true
                terminationConfirmed = $treeContained; exitCode = $exitCode
                stdout = ''; stderr = ''; failure = 'stream_drain_timeout'
                isolationMode = $isolationMode
            }
        }
        return [pscustomobject][ordered]@{
            started = $true; completed = $true; timedOut = $false
            terminationConfirmed = $treeContained; exitCode = $exitCode
            stdout = $stdoutTask.GetAwaiter().GetResult()
            stderr = $stderrTask.GetAwaiter().GetResult(); failure = $null
            isolationMode = $isolationMode
        }
    }
    catch {
        $terminated = $true
        if ($jobAssigned) {
            $cleanupMs = [int][Math]::Max(0, [Math]::Min(500, $DeadlineTick - [Environment]::TickCount64))
            $terminated = $job.TerminateAndWait($cleanupMs)
            $closed = $job.Close()
            $job = $null
            $terminated = $terminated -and $closed
        }
        elseif ($started) {
            try {
                if (-not $process.HasExited) {
                    $process.Kill($true)
                    $cleanupMs = [int][Math]::Max(0, [Math]::Min(500, $DeadlineTick - [Environment]::TickCount64))
                    $terminated = $process.WaitForExit($cleanupMs)
                }
            }
            catch { $terminated = $false }
        }
        return [pscustomobject][ordered]@{
            started = $started; completed = $false; timedOut = $false
            terminationConfirmed = $terminated; exitCode = $null
            stdout = ''; stderr = ''; failure = "process_error:$($_.Exception.Message)"
            isolationMode = $isolationMode
        }
    }
    finally {
        if ($null -ne $job) { [void]$job.Close() }
        $process.Dispose()
    }
}
$script:CommandStats = [ordered]@{
    started = 0; completed = 0; timedOut = 0
    notStarted = 0; failed = 0; terminationFailures = 0
}
$script:OwnedProcessTerminationCompromised = $false

function Invoke-TelemetryCommand(
    [string]$FilePath,
    [string[]]$ArgumentList,
    [long]$DeadlineTick,
    [int]$TimeoutMs
) {
    if ($script:OwnedProcessTerminationCompromised) {
        $script:CommandStats.notStarted += 1
        return [pscustomobject][ordered]@{
            started = $false; completed = $false; timedOut = $false
            terminationConfirmed = $false; exitCode = $null
            stdout = ''; stderr = ''; failure = 'owned_process_termination_unconfirmed'
        }
    }
    $result = Invoke-OwnedProcess $FilePath $ArgumentList $DeadlineTick $TimeoutMs
    if ($result.started) { $script:CommandStats.started += 1 } else { $script:CommandStats.notStarted += 1 }
    if ($result.completed) { $script:CommandStats.completed += 1 }
    if ($result.timedOut) { $script:CommandStats.timedOut += 1 }
    if (($result.completed -and $result.exitCode -ne 0) -or
        (-not $result.completed -and -not $result.timedOut)) {
        $script:CommandStats.failed += 1
    }
    if (-not $result.terminationConfirmed) {
        $script:CommandStats.terminationFailures += 1
        $script:OwnedProcessTerminationCompromised = $true
    }
    $result
}

function Resolve-PullRequestState([string]$BranchName, [string]$Head, [pscustomobject]$Snapshot) {
    $unknown = [pscustomobject]@{
        state = 'unknown'; open = $null; merged = $null; closedUnmerged = $null
        evidenceComplete = $false; matchingPrNumbers = @()
    }
    if (-not $BranchName -or -not $Snapshot.available) { return $unknown }
    $matches = @($Snapshot.records | Where-Object { $_.headRefName -eq $BranchName })
    $numbers = @($matches | ForEach-Object { $_.number } | Sort-Object -Unique)
    if (@($matches | Where-Object { $_.state -eq 'OPEN' }).Count -gt 0) {
        return [pscustomobject]@{
            state = 'open'; open = $true; merged = $false; closedUnmerged = $false
            evidenceComplete = [bool]$Snapshot.complete; matchingPrNumbers = $numbers
        }
    }
    $exact = @($matches | Where-Object { $_.headRefOid -eq $Head })
    if ($matches.Count -gt 0 -and $exact.Count -eq 0) {
        $unknown.matchingPrNumbers = $numbers
        return $unknown
    }
    if ($exact.Count -eq 0) {
        if (-not $Snapshot.complete) { return $unknown }
        return [pscustomobject]@{
            state = 'none'; open = $false; merged = $false; closedUnmerged = $false
            evidenceComplete = $true; matchingPrNumbers = @()
        }
    }
    $merged = @($exact | Where-Object { $_.mergedAt }).Count -gt 0
    $closed = @($exact | Where-Object { $_.state -eq 'CLOSED' -and -not $_.mergedAt }).Count -gt 0
    [pscustomobject]@{
        state = $(if ($merged) { 'merged' } elseif ($closed) { 'closed_unmerged' } else { 'unknown' })
        open = $false; merged = $merged; closedUnmerged = $closed
        evidenceComplete = [bool]$Snapshot.complete; matchingPrNumbers = $numbers
    }
}

function Invoke-InternalWorktreeProbe(
    [string]$Path, [long]$HeadEpoch, [long]$CutoffEpoch,
    [long]$ObservationEpoch, [int]$ClockSkewToleranceSeconds
) {
    $headTime = [DateTimeOffset]::FromUnixTimeSeconds($HeadEpoch).UtcDateTime
    $result = [ordered]@{
        headTimeUtc = $headTime.ToString('o')
        lastMaterialUtc = $headTime.ToString('o')
        stale = ($HeadEpoch -lt $CutoffEpoch)
        ageEvidenceComplete = $false
        dirty = $null
        dirtyCount = $null
        unresolvedMaterialPaths = 0
        error = $null
    }
    if (-not (Test-Path -LiteralPath $Path -PathType Container)) {
        $result.error = 'worktree_path_missing'
        return [pscustomobject]$result
    }
    $gitCommand = Get-Command git -ErrorAction SilentlyContinue
    if (-not $gitCommand) {
        $result.error = 'git_not_found'
        return [pscustomobject]$result
    }
    $status = Invoke-OwnedProcess $gitCommand.Source @(
        '-c', 'core.fsmonitor=false', '-C', $Path,
        'status', '--porcelain=v1', '-z', '--untracked-files=all'
    ) ([Environment]::TickCount64 + 10000) 9000
    if (-not $status.completed -or $status.exitCode -ne 0) {
        $result.error = $(if ($status.timedOut) { 'git_status_timeout' } else { 'git_status_failed' })
        return [pscustomobject]$result
    }
    try {
        $records = @(ConvertFrom-StatusPorcelain $status.stdout)
    }
    catch {
        $result.error = 'git_status_parse_failed'
        return [pscustomobject]$result
    }
    $result.dirty = ($records.Count -gt 0)
    $result.dirtyCount = $records.Count
    $lastMaterial = $headTime
    foreach ($record in $records) {
        $full = Join-Path $Path ($record.path -replace '/', [IO.Path]::DirectorySeparatorChar)
        if (-not (Test-Path -LiteralPath $full)) {
            $result.unresolvedMaterialPaths += 1
            continue
        }
        $mtime = (Get-Item -LiteralPath $full -Force).LastWriteTimeUtc
        if ($mtime -gt $lastMaterial) { $lastMaterial = $mtime }
    }
    $result.lastMaterialUtc = $lastMaterial.ToString('o')
    $observationLimit = [DateTimeOffset]::FromUnixTimeSeconds($ObservationEpoch).UtcDateTime.AddSeconds($ClockSkewToleranceSeconds)
    if ($lastMaterial -gt $observationLimit) {
        $result.error = 'material_time_after_observation'
        return [pscustomobject]$result
    }
    if ($result.unresolvedMaterialPaths -gt 0) {
        $result.error = 'one_or_more_material_paths_unresolved'
        return [pscustomobject]$result
    }
    $result.ageEvidenceComplete = $true
    $result.stale = ($lastMaterial -lt [DateTimeOffset]::FromUnixTimeSeconds($CutoffEpoch).UtcDateTime)
    [pscustomobject]$result
}
function Test-MachineLocalEnforcement([string[]]$LocalHooks, [string[]]$MainHooks, [bool]$MainAvailable = $true) {
    if (-not $MainAvailable) {
        return New-Finding 'machine-local-enforcement' 'warn' (
            'unknown: origin/main not available locally (run with -Fetch to compare).')
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


function Test-InternalWorkerOwnership {
    if (-not [bool]$IsWindows) { return $false }
    $ownedJobName = [Environment]::GetEnvironmentVariable('FORSETI_OWNED_JOB_NAME')
    if (-not $ownedJobName) { return $false }
    try {
        [ForsetiJobMembership]::IsCurrentProcessInNamedJob($ownedJobName)
    }
    catch {
        $false
    }
}

if ($InternalWorktreeProbe) {
    if (-not (Test-InternalWorkerOwnership)) {
        [pscustomobject]@{
            ageEvidenceComplete = $false; dirty = $null; dirtyCount = $null
            unresolvedMaterialPaths = 0; error = 'internal_probe_not_coordinator_owned'
        } | ConvertTo-Json -Compress
        exit 2
    }
    try {
        Invoke-InternalWorktreeProbe (
            $ProbePath
        ) $ProbeHeadEpoch $ProbeCutoffEpoch $ProbeObservationEpoch $ProbeClockSkewToleranceSeconds |
            ConvertTo-Json -Depth 5 -Compress
        exit 0
    }
    catch {
        [pscustomobject]@{
            ageEvidenceComplete = $false; dirty = $null; dirtyCount = $null
            unresolvedMaterialPaths = 0; error = "worker_error:$($_.Exception.Message)"
        } | ConvertTo-Json -Compress
        exit 0
    }
}

if (-not [bool]$IsWindows) {
    Write-Host ('ABORTED: Windows Job Object containment is required; ' +
        'no equivalent non-Windows descendant-containment proof is implemented.') -ForegroundColor Red
    exit 2
}

# --- selftest ---------------------------------------------------------------

function Invoke-SelfTest {
    $cutoff = [datetime]'2026-07-09T00:00:00Z'
    $parsedWorktrees = @(ConvertFrom-WorktreePorcelain @(
        'worktree C:/main', 'HEAD aaaaaaaa', 'branch refs/heads/main', '',
        'worktree C:/lane', 'HEAD bbbbbbbb', 'detached', 'locked sealed lane', ''
    ))
    $parsedStatus = @(ConvertFrom-StatusPorcelain (" M tracked.txt`0?? odd`nname.txt`0"))
    $incompletePrSnapshot = [pscustomobject]@{
        available = $true; complete = $false; records = @()
    }
    $pwshCommand = Get-Command pwsh -ErrorAction SilentlyContinue
    $timeoutProbe = $null
    $childPid = $null
    $childGone = $false
    $pidFile = Join-Path ([IO.Path]::GetTempPath()) ("forseti-lane-health-$([guid]::NewGuid().ToString('N')).pid")
    if ($pwshCommand) {
        $childTemplate = '$pidFile=''{0}''; $psi=[Diagnostics.ProcessStartInfo]::new(); $psi.FileName=''pwsh''; $psi.UseShellExecute=$false; [void]$psi.ArgumentList.Add(''-NoProfile''); [void]$psi.ArgumentList.Add(''-NonInteractive''); [void]$psi.ArgumentList.Add(''-Command''); [void]$psi.ArgumentList.Add(''Start-Sleep -Seconds 3''); $child=[Diagnostics.Process]::Start($psi); [IO.File]::WriteAllText($pidFile,[string]$child.Id); $child.WaitForExit()'
        $childCommand = $childTemplate -f $pidFile.Replace('''', '''''')
        $timeoutProbe = Invoke-OwnedProcess $pwshCommand.Source @(
            '-NoProfile', '-NonInteractive', '-Command', $childCommand
        ) ([Environment]::TickCount64 + 5000) 1500
        if (Test-Path -LiteralPath $pidFile) {
            $rawPid = [IO.File]::ReadAllText($pidFile).Trim()
            if ($rawPid -match '^\d+$') { $childPid = [int]$rawPid }
        }
        if ($childPid) {
            $waitUntil = [datetime]::UtcNow.AddSeconds(1)
            do {
                $childGone = $null -eq (Get-Process -Id $childPid -ErrorAction SilentlyContinue)
                if (-not $childGone) { Start-Sleep -Milliseconds 50 }
            } while (-not $childGone -and [datetime]::UtcNow -lt $waitUntil)
        }
    }
    Remove-Item -LiteralPath $pidFile -Force -ErrorAction SilentlyContinue

    $earlyProbe = $null
    $earlyElapsedMs = $null
    $earlyPid = $null
    $earlyGone = $false
    $pipeProbe = $null
    $pipeElapsedMs = $null
    $pipePid = $null
    $pipeGone = $false
    if ($script:UseWindowsJobIsolation) {
        $earlyPidFile = Join-Path ([IO.Path]::GetTempPath()) ("forseti-lane-health-early-$([guid]::NewGuid().ToString('N')).pid")
        $earlyTemplate = '$pidFile=''{0}''; $child=Start-Process -FilePath pwsh -ArgumentList @(''-NoProfile'',''-NonInteractive'',''-Command'',''Start-Sleep -Seconds 5'') -WindowStyle Hidden -PassThru; [IO.File]::WriteAllText($pidFile,[string]$child.Id); exit 0'
        $earlyCommand = $earlyTemplate -f $earlyPidFile.Replace('''', '''''')
        $earlyWatch = [Diagnostics.Stopwatch]::StartNew()
        $earlyProbe = Invoke-OwnedProcess $pwshCommand.Source @(
            '-NoProfile', '-NonInteractive', '-Command', $earlyCommand
        ) ([Environment]::TickCount64 + 4000) 2500
        $earlyWatch.Stop()
        $earlyElapsedMs = $earlyWatch.ElapsedMilliseconds
        if (Test-Path -LiteralPath $earlyPidFile) {
            $rawPid = [IO.File]::ReadAllText($earlyPidFile).Trim()
            if ($rawPid -match '^\d+$') { $earlyPid = [int]$rawPid }
        }
        if ($earlyPid) {
            $waitUntil = [datetime]::UtcNow.AddSeconds(1)
            do {
                $earlyGone = $null -eq (Get-Process -Id $earlyPid -ErrorAction SilentlyContinue)
                if (-not $earlyGone) { Start-Sleep -Milliseconds 25 }
            } while (-not $earlyGone -and [datetime]::UtcNow -lt $waitUntil)
        }
        Remove-Item -LiteralPath $earlyPidFile -Force -ErrorAction SilentlyContinue

        $pipePidFile = Join-Path ([IO.Path]::GetTempPath()) ("forseti-lane-health-pipe-$([guid]::NewGuid().ToString('N')).pid")
        $pipeTemplate = '$pidFile=''{0}''; $psi=[Diagnostics.ProcessStartInfo]::new(); $psi.FileName=''pwsh''; $psi.UseShellExecute=$false; [void]$psi.ArgumentList.Add(''-NoProfile''); [void]$psi.ArgumentList.Add(''-NonInteractive''); [void]$psi.ArgumentList.Add(''-Command''); [void]$psi.ArgumentList.Add(''Write-Output inherited-pipe-open; Start-Sleep -Seconds 5''); $child=[Diagnostics.Process]::Start($psi); [IO.File]::WriteAllText($pidFile,[string]$child.Id); Write-Output ''parent-done''; exit 0'
        $pipeCommand = $pipeTemplate -f $pipePidFile.Replace('''', '''''')
        $pipeWatch = [Diagnostics.Stopwatch]::StartNew()
        $pipeProbe = Invoke-OwnedProcess $pwshCommand.Source @(
            '-NoProfile', '-NonInteractive', '-Command', $pipeCommand
        ) ([Environment]::TickCount64 + 3500) 1500
        $pipeWatch.Stop()
        $pipeElapsedMs = $pipeWatch.ElapsedMilliseconds
        if (Test-Path -LiteralPath $pipePidFile) {
            $rawPid = [IO.File]::ReadAllText($pipePidFile).Trim()
            if ($rawPid -match '^\d+$') { $pipePid = [int]$rawPid }
        }
        if ($pipePid) {
            $waitUntil = [datetime]::UtcNow.AddSeconds(1)
            do {
                $pipeGone = $null -eq (Get-Process -Id $pipePid -ErrorAction SilentlyContinue)
                if (-not $pipeGone) { Start-Sleep -Milliseconds 25 }
            } while (-not $pipeGone -and [datetime]::UtcNow -lt $waitUntil)
        }
        Remove-Item -LiteralPath $pipePidFile -Force -ErrorAction SilentlyContinue
    }

    $cases = @(
        @{ name = 'dirty-under'; got = (Test-DirtyVolume 3 5 30).level; expect = 'ok' }
        @{ name = 'dirty-over'; got = (Test-DirtyVolume 10 40 30).level; expect = 'warn' }
        @{ name = 'dirty-edge'; got = (Test-DirtyVolume 15 15 30).level; expect = 'ok' }
        @{ name = 'wt-under'; got = (Test-WorktreeSprawl 3 4).level; expect = 'ok' }
        @{ name = 'wt-over'; got = (Test-WorktreeSprawl 7 4).level; expect = 'warn' }
        @{ name = 'wt-edge'; got = (Test-WorktreeSprawl 4 4).level; expect = 'ok' }
        @{ name = 'enf-clean'; got = (Test-MachineLocalEnforcement @('.agents/hooks/a.py') @('.agents/hooks/a.py')).level; expect = 'ok' }
        @{ name = 'enf-orphan'; got = (Test-MachineLocalEnforcement @('.agents/hooks/guard.py') @('.agents/hooks/other.py')).level; expect = 'warn' }
        @{ name = 'enf-partial'; got = (Test-MachineLocalEnforcement @('.agents/hooks/a.py', '.agents/hooks/b.py') @('.agents/hooks/a.py')).level; expect = 'warn' }
        @{ name = 'enf-none'; got = (Test-MachineLocalEnforcement @() @('.agents/hooks/a.py')).level; expect = 'ok' }
        @{ name = 'enf-no-main'; got = (Test-MachineLocalEnforcement @('.agents/hooks/guard.py') @() $false).level; expect = 'warn' }
        @{ name = 'exec-timeout-warn'; got = (Test-ExecutionEvidence ([pscustomobject]@{ timedOut = 1; notStarted = 0; failed = 0; terminationFailures = 0 })).level; expect = 'warn' }
        @{ name = 'exec-failed-warn'; got = (Test-ExecutionEvidence ([pscustomobject]@{ timedOut = 0; notStarted = 0; failed = 1; terminationFailures = 0 })).level; expect = 'warn' }
        @{ name = 'status-timeout'; got = (Resolve-TelemetryStatus 0 0 ([pscustomobject]@{ timedOut = 1; notStarted = 0; failed = 0; terminationFailures = 0 }) $true $true); expect = 'incomplete' }
        @{ name = 'status-complete'; got = (Resolve-TelemetryStatus 0 0 ([pscustomobject]@{ timedOut = 0; notStarted = 0; failed = 0; terminationFailures = 0 }) $true $true); expect = 'complete' }
        @{ name = 'status-no-containment'; got = (Resolve-TelemetryStatus 0 0 ([pscustomobject]@{ timedOut = 0; notStarted = 0; failed = 0; terminationFailures = 0 }) $false $true); expect = 'incomplete' }
        @{ name = 'status-remote-missing'; got = (Resolve-TelemetryStatus 0 0 ([pscustomobject]@{ timedOut = 0; notStarted = 0; failed = 0; terminationFailures = 0 }) $true $false); expect = 'incomplete' }
        @{ name = 'remote-pr-warn'; got = (Test-RequestedRemoteEvidence $false $false $true $true $false).level; expect = 'warn' }
        @{ name = 'future-skew'; got = (Test-IsFutureSkew ([datetime]'2026-07-11T00:05:01Z') ([datetime]'2026-07-11T00:00:00Z') 300); expect = $true }
        @{ name = 'future-tolerance'; got = (Test-IsFutureSkew ([datetime]'2026-07-11T00:05:00Z') ([datetime]'2026-07-11T00:00:00Z') 300); expect = $false }
        @{ name = 'stale-before'; got = (Test-IsStale ([datetime]'2026-07-08T23:59:59Z') $cutoff); expect = $true }
        @{ name = 'stale-edge'; got = (Test-IsStale $cutoff $cutoff); expect = $false }
        @{ name = 'gone-unmerged'; got = (Resolve-AheadOrUnpushed $false 'origin/lane' '[gone]' $false); expect = $true }
        @{ name = 'gone-merged'; got = (Resolve-AheadOrUnpushed $false 'origin/lane' '[gone]' $true); expect = $false }
        @{ name = 'ahead-track'; got = (Resolve-AheadOrUnpushed $false 'origin/lane' '[ahead 1]' $false); expect = $true }
        @{ name = 'pr-incomplete-null'; got = (Resolve-PullRequestState 'missing' 'abc' $incompletePrSnapshot).state; expect = 'unknown' }
        @{ name = 'class-seal'; got = (Resolve-StaleClassification $true $true $true $true $false $true); expect = 'sealed_or_protected' }
        @{ name = 'class-open'; got = (Resolve-StaleClassification $false $true $true $true $false $false); expect = 'open_pr' }
        @{ name = 'class-ahead'; got = (Resolve-StaleClassification $false $false $false $true $false $false); expect = 'ahead_or_unpushed' }
        @{ name = 'class-dirty'; got = (Resolve-StaleClassification $false $false $true $false $false $false); expect = 'dirty' }
        @{ name = 'class-unknown'; got = (Resolve-StaleClassification $false $null $false $false $true $false); expect = 'unknown' }
        @{ name = 'parse-wt-count'; got = $parsedWorktrees.Count; expect = 2 }
        @{ name = 'parse-wt-lock'; got = $parsedWorktrees[1].lockReason; expect = 'sealed lane' }
        @{ name = 'parse-status-count'; got = $parsedStatus.Count; expect = 2 }
        @{ name = 'parse-status-path'; got = $parsedStatus[1].path; expect = "odd`nname.txt" }
        @{ name = 'owned-timeout'; got = [bool]($timeoutProbe -and $timeoutProbe.timedOut); expect = $true }
        @{ name = 'owned-termination'; got = [bool]($timeoutProbe -and $timeoutProbe.terminationConfirmed); expect = $true }
        @{ name = 'owned-child-tree'; got = [bool]($childPid -and $childGone); expect = $true }
        @{ name = 'job-early-complete'; got = [bool](-not $script:UseWindowsJobIsolation -or ($earlyProbe.completed -and $earlyProbe.exitCode -eq 0)); expect = $true }
        @{ name = 'job-early-contained'; got = [bool](-not $script:UseWindowsJobIsolation -or ($earlyPid -and $earlyGone -and $earlyProbe.terminationConfirmed)); expect = $true }
        @{ name = 'job-early-bound'; got = [bool](-not $script:UseWindowsJobIsolation -or $earlyElapsedMs -lt 3000); expect = $true }
        @{ name = 'job-pipe-contained'; got = [bool](-not $script:UseWindowsJobIsolation -or ($pipePid -and $pipeGone -and $pipeProbe.terminationConfirmed)); expect = $true }
        @{ name = 'job-pipe-bound'; got = [bool](-not $script:UseWindowsJobIsolation -or $pipeElapsedMs -lt 2500); expect = $true }
    )
    $ok = $true
    foreach ($c in $cases) {
        $pass = $c.got -eq $c.expect
        if (-not $pass) { $ok = $false }
        Write-Host ("{0}  {1,-20} expect={2,-8} got={3,-8}" -f ($(if ($pass) { 'PASS' } else { 'FAIL' })), $c.name, $c.expect, $c.got)
    }
    if ($ok) { Write-Host 'SELFTEST OK' -ForegroundColor Green; return 0 }
    Write-Host 'SELFTEST FAILED' -ForegroundColor Red
    return 1
}

if ($SelfTest) { exit (Invoke-SelfTest) }

# --- IO: gather real state (read-only) --------------------------------------

$runWatch = [Diagnostics.Stopwatch]::StartNew()
$deadlineTick = [Environment]::TickCount64 + $OverallTimeoutMs
try {
    $observationUtc = $(if ($AsOfUtc) {
        [DateTimeOffset]::Parse(
            $AsOfUtc,
            [Globalization.CultureInfo]::InvariantCulture,
            [Globalization.DateTimeStyles]::AssumeUniversal
        ).UtcDateTime
    } else {
        [datetime]::UtcNow
    })
}
catch {
    Write-Host "ABORTED: invalid -AsOfUtc value: $AsOfUtc" -ForegroundColor Red
    exit 2
}
$cutoffUtc = $observationUtc.AddHours(-$StaleAfterHours)
$cutoffEpoch = [DateTimeOffset]::new($cutoffUtc).ToUnixTimeSeconds()
$observationEpoch = [DateTimeOffset]::new($observationUtc).ToUnixTimeSeconds()

$gitCommand = Get-Command git -ErrorAction SilentlyContinue
$pwshCommand = Get-Command pwsh -ErrorAction SilentlyContinue
if (-not $gitCommand -or -not $pwshCommand) {
    Write-Host 'ABORTED: git and pwsh are required.' -ForegroundColor Red
    exit 2
}

function Invoke-BoundedGit([string[]]$GitArguments, [int]$TimeoutMs = $CommandTimeoutMs) {
    [string[]]$allArguments = @('-c', 'core.fsmonitor=false') + $GitArguments
    Invoke-TelemetryCommand $gitCommand.Source $allArguments $deadlineTick $TimeoutMs
}

if (-not $RepoPath) {
    $repoResult = Invoke-BoundedGit @('rev-parse', '--show-toplevel')
    if (-not $repoResult.completed -or $repoResult.exitCode -ne 0 -or -not $repoResult.stdout.Trim()) {
        Write-Host 'ABORTED: not inside a git repository (pass -RepoPath).' -ForegroundColor Red
        exit 2
    }
    $RepoPath = $repoResult.stdout.Trim()
}
if (-not (Test-Path -LiteralPath $RepoPath -PathType Container)) {
    Write-Host "ABORTED: path does not exist: $RepoPath" -ForegroundColor Red
    exit 2
}
$RepoPath = (Resolve-Path -LiteralPath $RepoPath).Path
$repoCheck = Invoke-BoundedGit @('-C', $RepoPath, 'rev-parse', '--show-toplevel')
if (-not $repoCheck.completed -or $repoCheck.exitCode -ne 0) {
    Write-Host "ABORTED: not a git repository: $RepoPath" -ForegroundColor Red
    exit 2
}

$fetchSucceeded = $false
$fetchFailure = $null
if ($Fetch) {
    $fetchResult = Invoke-BoundedGit @('-C', $RepoPath, 'fetch', 'origin', '--quiet') ([Math]::Max(5000, $CommandTimeoutMs))
    $fetchSucceeded = $fetchResult.completed -and $fetchResult.exitCode -eq 0
    if (-not $fetchSucceeded) {
        $fetchFailure = $(if ($fetchResult.timedOut) { $fetchResult.failure } else { 'git_fetch_failed' })
    }
}

$branchResult = Invoke-BoundedGit @('-C', $RepoPath, 'rev-parse', '--abbrev-ref', 'HEAD')
$branch = $(if ($branchResult.completed -and $branchResult.exitCode -eq 0) {
    $branchResult.stdout.Trim()
} else {
    '(unknown)'
})

$rootStatus = Invoke-BoundedGit @('-C', $RepoPath, 'status', '--porcelain', '--untracked-files=all')
if (-not $rootStatus.completed -or $rootStatus.exitCode -ne 0) {
    Write-Host 'ABORTED: root worktree status inventory failed or timed out.' -ForegroundColor Red
    exit 2
}
$rootStatusLines = @($rootStatus.stdout -split "\r?\n" | Where-Object { $_ })
$modified = @($rootStatusLines | Where-Object { $_ -notmatch '^\?\?' }).Count
$untracked = @($rootStatusLines | Where-Object { $_ -match '^\?\?' }).Count

$worktreeResult = Invoke-BoundedGit @('-C', $RepoPath, 'worktree', 'list', '--porcelain')
if (-not $worktreeResult.completed -or $worktreeResult.exitCode -ne 0) {
    Write-Host 'ABORTED: git worktree inventory failed or timed out.' -ForegroundColor Red
    exit 2
}
$worktrees = @(ConvertFrom-WorktreePorcelain ($worktreeResult.stdout -split "\r?\n"))
if ($worktrees.Count -eq 0) {
    Write-Host 'ABORTED: git worktree inventory returned no records.' -ForegroundColor Red
    exit 2
}
$laneWorktrees = @($worktrees | Select-Object -Skip 1)
$wtTotal = $worktrees.Count
$wtLinked = $laneWorktrees.Count

$mainRefResult = Invoke-BoundedGit @('-C', $RepoPath, 'rev-parse', '--verify', '--quiet', 'origin/main')
$mainAvailable = $mainRefResult.completed -and $mainRefResult.exitCode -eq 0

$localHooksResult = Invoke-BoundedGit @('-C', $RepoPath, 'ls-files', '--others', '--cached', '--', '.agents/hooks/')
if (-not $localHooksResult.completed -or $localHooksResult.exitCode -ne 0) {
    Write-Host 'ABORTED: local hook inventory failed or timed out.' -ForegroundColor Red
    exit 2
}
$localHooks = @($localHooksResult.stdout -split "\r?\n" | Where-Object { $_ -match '\.py$' } | Sort-Object -Unique)
$mainHooks = @()
if ($mainAvailable) {
    $mainHooksResult = Invoke-BoundedGit @('-C', $RepoPath, 'ls-tree', '-r', '--name-only', 'origin/main', '--', '.agents/hooks/')
    if ($mainHooksResult.completed -and $mainHooksResult.exitCode -eq 0) {
        $mainHooks = @($mainHooksResult.stdout -split "\r?\n" | Where-Object { $_ -match '\.py$' })
    } else {
        $mainAvailable = $false
    }
}

$trackingResult = Invoke-BoundedGit @(
    '-C', $RepoPath, 'for-each-ref',
    '--format=%(refname:short)|%(upstream:short)|%(upstream:track)', 'refs/heads'
)
$trackingMap = @{}
if ($trackingResult.completed -and $trackingResult.exitCode -eq 0) {
    foreach ($line in @($trackingResult.stdout -split "\r?\n" | Where-Object { $_ })) {
        $parts = $line -split '\|', 3
        if ($parts.Count -ne 3 -or -not $parts[0]) { continue }
        $trackingMap[$parts[0]] = [pscustomobject]@{
            upstream = $(if ($parts[1]) { $parts[1] } else { $null })
            track = $(if ($parts[2]) { $parts[2] } else { $null })
        }
    }
}
$trackingEvidenceAvailable = $trackingResult.completed -and $trackingResult.exitCode -eq 0

$mergedSet = @{}
$branchesMergedIntoMain = $null
if ($mainAvailable) {
    $mergedResult = Invoke-BoundedGit @(
        '-C', $RepoPath, 'for-each-ref', '--merged=origin/main', '--format=%(refname:short)', 'refs/heads'
    )
    if ($mergedResult.completed -and $mergedResult.exitCode -eq 0) {
        foreach ($name in @($mergedResult.stdout -split "\r?\n" | Where-Object { $_ })) {
            $mergedSet[$name] = $true
        }
        $branchesMergedIntoMain = $mergedSet.Count
    } else {
        $mainAvailable = $false
    }
}

$headTimeMap = @{}
$heads = @($laneWorktrees | ForEach-Object { $_.head } | Where-Object { $_ } | Sort-Object -Unique)
if ($heads.Count -gt 0) {
    [string[]]$headArguments = @('-C', $RepoPath, 'show', '-s', '--format=%H|%ct', '--no-show-signature') + $heads
    $headResult = Invoke-BoundedGit $headArguments
    if ($headResult.completed -and $headResult.exitCode -eq 0) {
        foreach ($line in @($headResult.stdout -split "\r?\n" | Where-Object { $_ -match '^[0-9a-fA-F]+\|\d+$' })) {
            $parts = $line -split '\|', 2
            $headTimeMap[$parts[0]] = [long]$parts[1]
        }
    }
}

$prSnapshot = [pscustomobject][ordered]@{
    queried = [bool]$QueryPullRequests; available = $false; complete = $false
    repo = $null; records = @(); error = $(if ($QueryPullRequests) { $null } else { 'not_requested' })
}
if ($QueryPullRequests) {
    $remoteResult = Invoke-BoundedGit @('-C', $RepoPath, 'remote', 'get-url', 'origin')
    if ($remoteResult.completed -and $remoteResult.exitCode -eq 0 -and
        $remoteResult.stdout.Trim() -match 'github\.com[:/](?<owner>[^/]+)/(?<repo>[^/]+?)(?:\.git)?$') {
        $prSnapshot.repo = "$($Matches.owner)/$($Matches.repo)"
        $ghCommand = Get-Command gh -ErrorAction SilentlyContinue
        if ($ghCommand) {
            $prResult = Invoke-TelemetryCommand $ghCommand.Source @(
                'pr', 'list', '--repo', $prSnapshot.repo, '--state', 'all', '--limit', '1000',
                '--json', 'number,headRefName,headRefOid,state,mergedAt,closedAt,updatedAt'
            ) $deadlineTick ([Math]::Max(8000, $CommandTimeoutMs))
            if ($prResult.completed -and $prResult.exitCode -eq 0) {
                try {
                    $prSnapshot.records = @($prResult.stdout | ConvertFrom-Json)
                    $prSnapshot.available = $true
                    $prSnapshot.complete = ($prSnapshot.records.Count -lt 1000)
                    $prSnapshot.error = $(if ($prSnapshot.complete) { $null } else { 'gh_pr_limit_reached' })
                }
                catch {
                    $prSnapshot.error = 'gh_pr_json_invalid'
                }
            } else {
                $prSnapshot.error = $(if ($prResult.timedOut) { $prResult.failure } else { 'gh_pr_list_failed' })
            }
        } else {
            $prSnapshot.error = 'gh_not_found'
        }
    } else {
        $prSnapshot.error = 'github_origin_slug_unavailable'
    }
}

$protectedSet = @{}
foreach ($name in $ProtectedLaneName) { if ($name) { $protectedSet[[string]$name] = $true } }
$staleRecords = [Collections.Generic.List[object]]::new()
$unknownAgeRecords = [Collections.Generic.List[object]]::new()
$unknownGuardCount = 0
$classificationCounts = [ordered]@{
    sealed_or_protected = 0; open_pr = 0; ahead_or_unpushed = 0
    merged_or_gone_dirty = 0; dirty = 0; merged_or_gone_clean = 0
    closed_unmerged = 0; unknown = 0
}

foreach ($wt in @($laneWorktrees | Sort-Object path)) {
    $unknownReason = $null
    if ($wt.prunable) { $unknownReason = 'worktree_prunable' }
    elseif (-not $wt.head -or -not $headTimeMap.ContainsKey($wt.head)) { $unknownReason = 'head_time_unavailable' }
    if ($unknownReason) {
        $unknownAgeRecords.Add([pscustomobject][ordered]@{
            path = $wt.path; branch = $(if ($wt.branch) { $wt.branch } else { '(detached)' })
            head = $wt.head; reason = $unknownReason; observedAtUtc = $observationUtc.ToString('o')
        })
        continue
    }

    $headEpoch = [long]$headTimeMap[$wt.head]
    if ($headEpoch -gt ($observationEpoch + $ClockSkewToleranceSeconds)) {
        $unknownAgeRecords.Add([pscustomobject][ordered]@{
            path = $wt.path; branch = $(if ($wt.branch) { $wt.branch } else { '(detached)' })
            head = $wt.head; reason = 'head_time_after_observation'
            observedAtUtc = $observationUtc.ToString('o')
        })
        continue
    }
    if ($headEpoch -ge $cutoffEpoch) { continue }
    $workerResult = Invoke-TelemetryCommand $pwshCommand.Source @(
        '-NoProfile', '-NonInteractive', '-File', $PSCommandPath,
        '-InternalWorktreeProbe', '-ProbePath', $wt.path,
        '-ProbeHeadEpoch', [string]$headEpoch, '-ProbeCutoffEpoch', [string]$cutoffEpoch,
        '-ProbeObservationEpoch', [string]$observationEpoch,
        '-ProbeClockSkewToleranceSeconds', [string]$ClockSkewToleranceSeconds
    ) $deadlineTick $CommandTimeoutMs
    if (-not $workerResult.completed -or $workerResult.exitCode -ne 0) {
        $unknownAgeRecords.Add([pscustomobject][ordered]@{
            path = $wt.path; branch = $(if ($wt.branch) { $wt.branch } else { '(detached)' })
            head = $wt.head
            reason = $(if ($workerResult.failure) { $workerResult.failure } else { 'worktree_probe_failed' })
            observedAtUtc = $observationUtc.ToString('o')
        })
        continue
    }
    try {
        $probe = $workerResult.stdout | ConvertFrom-Json
    }
    catch {
        $probe = $null
    }
    if (-not $probe -or -not $probe.ageEvidenceComplete) {
        $unknownAgeRecords.Add([pscustomobject][ordered]@{
            path = $wt.path; branch = $(if ($wt.branch) { $wt.branch } else { '(detached)' })
            head = $wt.head
            reason = $(if ($probe -and $probe.error) { $probe.error } else { 'worktree_probe_json_invalid' })
            observedAtUtc = $observationUtc.ToString('o')
        })
        continue
    }
    if (-not [bool]$probe.stale) { continue }

    $prState = Resolve-PullRequestState $wt.branch $wt.head $prSnapshot
    $merged = $null
    if ($wt.branch -and $mainAvailable) { $merged = $mergedSet.ContainsKey($wt.branch) }
    if ($prState.merged -eq $true) { $merged = $true }
    elseif ($merged -eq $false -and $prState.merged -eq $false) { $merged = $false }

    $tracking = $null
    $trackingKnown = $false
    if ($wt.branch -and $trackingEvidenceAvailable -and $trackingMap.ContainsKey($wt.branch)) {
        $tracking = $trackingMap[$wt.branch]
        $trackingKnown = $true
    } elseif ($wt.detached -and $trackingEvidenceAvailable) {
        $trackingKnown = $true
    }
    $aheadOrUnpushed = $false
    if ($trackingKnown) {
        $aheadOrUnpushed = Resolve-AheadOrUnpushed (
            [bool]$wt.detached
        ) $(if ($tracking) { $tracking.upstream } else { $null }) $(if ($tracking) { $tracking.track } else { $null }) $merged
    }

    $leaf = [IO.Path]::GetFileName($wt.path.TrimEnd(
        [IO.Path]::DirectorySeparatorChar, [IO.Path]::AltDirectorySeparatorChar
    ))
    $protected = [bool]$wt.locked -or $protectedSet.ContainsKey($leaf) -or (
        $wt.branch -and $protectedSet.ContainsKey($wt.branch)
    )
    $dirty = [bool]$probe.dirty
    $classification = Resolve-StaleClassification (
        $protected
    ) $prState.open $dirty $aheadOrUnpushed $merged $prState.closedUnmerged
    $guardComplete = (
        $null -ne $probe.dirty -and $prState.evidenceComplete -and
        $null -ne $merged -and $null -ne $prState.closedUnmerged -and $trackingKnown
    )
    if (-not $guardComplete) { $unknownGuardCount += 1 }
    $classificationCounts[$classification] = [int]$classificationCounts[$classification] + 1

    $lastMaterialUtc = [datetime]$probe.lastMaterialUtc
    $staleRecords.Add([pscustomobject][ordered]@{
        path = $wt.path
        branch = $(if ($wt.branch) { $wt.branch } else { '(detached)' })
        head = $wt.head
        lastMaterialUtc = $lastMaterialUtc.ToUniversalTime().ToString('o')
        ageHours = [Math]::Round(($observationUtc - $lastMaterialUtc.ToUniversalTime()).TotalHours, 3)
        staleAfterHours = $StaleAfterHours
        clockSkewToleranceSeconds = $ClockSkewToleranceSeconds
        classification = $classification
        guardEvidenceComplete = $guardComplete
        guards = [pscustomobject][ordered]@{
            sealedOrProtected = $protected; lockedReason = $wt.lockReason
            openPr = $prState.open; pullRequestState = $prState.state
            pullRequestNumbers = @($prState.matchingPrNumbers)
            dirty = $probe.dirty; dirtyFileCount = $probe.dirtyCount
            aheadOrUnpushed = $(if ($trackingKnown) { $aheadOrUnpushed } else { $null })
            upstream = $(if ($tracking) { $tracking.upstream } else { $null })
            upstreamTrack = $(if ($tracking) { $tracking.track } else { $null })
            mergedIntoMainOrPr = $merged; closedUnmerged = $prState.closedUnmerged
            unknown = (-not $guardComplete)
        }
        cleanupAuthority = 'none'
    })
}

$requestedRemoteEvidenceComplete = ((-not $Fetch) -or $fetchSucceeded) -and (
    (-not $QueryPullRequests) -or ($prSnapshot.available -and $prSnapshot.complete)
)
$telemetryStatus = Resolve-TelemetryStatus (
    $unknownAgeRecords.Count
) $unknownGuardCount ([pscustomobject]$script:CommandStats) $script:UseWindowsJobIsolation $requestedRemoteEvidenceComplete
$staleFinding = Test-StaleWorktrees (
    $staleRecords.Count
) $unknownAgeRecords.Count $unknownGuardCount $script:CommandStats.terminationFailures $StaleAfterHours
$findings = @(
    Test-DirtyVolume $modified $untracked $DirtyThreshold
    Test-WorktreeSprawl $wtLinked $WorktreeThreshold
    Test-MachineLocalEnforcement $localHooks $mainHooks $mainAvailable
    Test-ExecutionEvidence ([pscustomobject]$script:CommandStats)
    Test-ContainmentRuntime $script:UseWindowsJobIsolation
    Test-RequestedRemoteEvidence ([bool]$Fetch) $fetchSucceeded ([bool]$QueryPullRequests) $prSnapshot.available $prSnapshot.complete
    $staleFinding
)
$warns = @($findings | Where-Object { $_.level -eq 'warn' })
$originMainState = $(if ($Fetch -and $fetchSucceeded) {
    'fetched'
} elseif ($Fetch -and -not $fetchSucceeded) {
    "fetch_failed:$fetchFailure"
} elseif ($mainAvailable) {
    'local-ref (use -Fetch to refresh)'
} else {
    'unavailable'
})

$telemetry = [pscustomobject][ordered]@{
    schemaVersion = 'forseti_lane_health_v2'
    status = $telemetryStatus
    observedAtUtc = $observationUtc.ToString('o')
    cutoffUtc = $cutoffUtc.ToString('o')
    staleAfterHours = $StaleAfterHours
    clockSkewToleranceSeconds = $ClockSkewToleranceSeconds
    activityBasis = 'max(head_commit_utc, existing_changed_or_untracked_file_mtime_utc); ignored_files_excluded'
    cleanupAuthority = 'none'
    executionBound = [pscustomobject][ordered]@{
        overallTimeoutMs = $OverallTimeoutMs; commandTimeoutMs = $CommandTimeoutMs
        containmentComplete = [bool]$script:UseWindowsJobIsolation
        ownedProcessTermination = $(if ($script:UseWindowsJobIsolation) {
            'Windows Job Object; supervisor released only after assignment; active job count confirmed zero before close'
        } else {
            'best-effort Process.Kill(true); descendant containment not proven on this runtime'
        })
        commands = [pscustomobject]$script:CommandStats
        elapsedMs = [Math]::Round($runWatch.Elapsed.TotalMilliseconds, 3)
    }
    counts = [pscustomobject][ordered]@{
        worktreesTotal = $wtTotal; linkedWorktrees = $wtLinked
        localBranches = $(if ($trackingEvidenceAvailable) { $trackingMap.Count } else { $null })
        branchesMergedIntoOriginMain = $branchesMergedIntoMain
        staleLinkedWorktrees = $staleRecords.Count
        unknownAgeLinkedWorktrees = $unknownAgeRecords.Count
        unknownGuardStaleWorktrees = $unknownGuardCount
    }
    classifications = [pscustomobject]$classificationCounts
    pullRequestEvidence = [pscustomobject][ordered]@{
        queried = $prSnapshot.queried; available = $prSnapshot.available
        complete = $prSnapshot.complete; repo = $prSnapshot.repo; error = $prSnapshot.error
    }
    protectedLaneNames = @($ProtectedLaneName | Sort-Object -Unique)
    staleWorktrees = @($staleRecords | Sort-Object path)
    unknownAgeWorktrees = @($unknownAgeRecords | Sort-Object path)
}

if ($Json) {
    [pscustomobject][ordered]@{
        repoPath = $RepoPath; branch = $branch; originMainRef = $originMainState
        findings = $findings; warnings = $warns.Count; telemetry = $telemetry
    } | ConvertTo-Json -Depth 10
    exit $(if ($warns.Count -gt 0) { 1 } else { 0 })
}

Write-Host "Lane health check - $RepoPath"
Write-Host "  branch: $branch    origin/main: $originMainState"
Write-Host ''
foreach ($finding in $findings) {
    $isWarn = $finding.level -eq 'warn'
    Write-Host ("  [{0}] {1,-26} {2}" -f (
        $(if ($isWarn) { 'WARN' } else { ' ok ' }), $finding.check, $finding.message
    )) -ForegroundColor ($(if ($isWarn) { 'Yellow' } else { 'Green' }))
}
Write-Host ''
Write-Host (
    "  telemetry: status=$telemetryStatus total=$wtTotal linked=$wtLinked " +
    "stale=$($staleRecords.Count) unknown_age=$($unknownAgeRecords.Count) " +
    "unknown_guards=$unknownGuardCount elapsed_ms=$($telemetry.executionBound.elapsedMs)"
)
foreach ($item in @($staleRecords | Sort-Object path)) {
    Write-Host ("    {0}  {1}  {2}" -f $item.classification, $item.branch, $item.path)
}
Write-Host ''
if ($warns.Count -gt 0) {
    Write-Host "$($warns.Count) warning(s) - detection nudge, not a block." -ForegroundColor Yellow
    exit 1
}
Write-Host 'healthy.' -ForegroundColor Green
exit 0