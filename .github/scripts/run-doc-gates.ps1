#!/usr/bin/env pwsh
#requires -Version 7.0
<#
.SYNOPSIS
    Run the CI doc-gate hook battery locally, before pushing.

.DESCRIPTION
    The strict doc-gate hooks in .github/workflows/ci.yml run in CI only. The
    local pre-push guard (pre_push_guard.py) mirrors just a 3-gate subset
    (check_map_links, header_index, check_review_routing), so a doc change that
    trips any OTHER gate -- e.g. check_ontology_tag_validity flagging a prose
    parenthetical like "(Capture)" -- passes pre-push and fails ~3 minutes later
    in CI. This runner executes the SAME hook commands CI runs, locally, in one
    shot, so that class of failure is caught before the push leaves your machine.

    SINGLE SOURCE OF TRUTH: the gate list is PARSED FROM ci.yml, not duplicated
    here. When CI's gate set changes, this runner stays in sync automatically. It
    runs only the `python .agents/hooks/*.py` gate steps -- not `python -m pytest`
    (the code-test job); run that separately if you touched harness code.

    This is local convenience tooling, not validation / readiness / authority.
    CI remains the authoritative gate.

.PARAMETER List
    Print the gates that would run (parsed from ci.yml) and exit, without running
    them.

.EXAMPLE
    pwsh .github/scripts/run-doc-gates.ps1
    Run every CI doc-gate locally; exit 1 if any gate fails.

.EXAMPLE
    pwsh .github/scripts/run-doc-gates.ps1 -List
    Just show the gate commands this runner derives from ci.yml.

.NOTES
    Diff-scoped gates (e.g. --diff origin/main) compare against origin/main; make
    sure it is fetched (`git fetch origin main`) for those to match CI exactly.
#>
[CmdletBinding()]
param(
    [switch]$List
)

# Repo root = two levels up from this script (.github/scripts/<this>), so the
# runner validates the worktree it lives in regardless of the caller's current
# directory (running it from another worktree must not validate the wrong tree).
$root = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
$ciPath = Join-Path $root ".github/workflows/ci.yml"
if (-not (Test-Path -LiteralPath $ciPath)) {
    Write-Error "run-doc-gates: ci.yml not found at $ciPath -- this script must live at .github/scripts/."
    exit 2
}

# Derive the gate commands from ci.yml: every `run:` step that invokes a hook
# under .agents/hooks/. Multi-line `run: |` blocks and `python -m pytest` do not
# match this pattern, so they are naturally excluded. Order is preserved; the
# duplicate review-output-provenance step is de-duplicated.
$gates = [System.Collections.Generic.List[string]]::new()
foreach ($line in Get-Content -LiteralPath $ciPath) {
    if ($line -match 'run:\s+(python\s+\.agents/hooks/.+)$') {
        $cmd = $Matches[1].Trim()
        if (-not $gates.Contains($cmd)) { $gates.Add($cmd) }
    }
}

if ($gates.Count -eq 0) {
    Write-Error "run-doc-gates: no '.agents/hooks/' gate commands found in ci.yml -- has the workflow moved?"
    exit 2
}

$ciRel = [System.IO.Path]::GetRelativePath($root, $ciPath).Replace('\', '/')

if ($List) {
    Write-Host "Doc gates derived from ${ciRel} ($($gates.Count)):"
    foreach ($g in $gates) { Write-Host "  $g" }
    exit 0
}

Write-Host "Running $($gates.Count) doc-gate(s) from ${ciRel} (repo root: $root)"
Write-Host ""

$failed = [System.Collections.Generic.List[string]]::new()
Push-Location $root
try {
    $i = 0
    foreach ($cmd in $gates) {
        $i++
        Write-Host ("[{0}/{1}] {2}" -f $i, $gates.Count, $cmd) -ForegroundColor Cyan
        $tokens = $cmd -split '\s+'
        $exe = $tokens[0]
        $restArgs = @($tokens[1..($tokens.Count - 1)])
        & $exe @restArgs
        $code = $LASTEXITCODE
        if ($code -ne 0) {
            $failed.Add($cmd)
            Write-Host ("      -> FAIL (exit {0})" -f $code) -ForegroundColor Red
        }
        else {
            Write-Host "      -> PASS" -ForegroundColor Green
        }
        Write-Host ""
    }
}
finally {
    Pop-Location
}

$passCount = $gates.Count - $failed.Count
Write-Host ("==== doc gates: {0}/{1} passed ====" -f $passCount, $gates.Count)
if ($failed.Count -gt 0) {
    Write-Host "FAILED:" -ForegroundColor Red
    foreach ($f in $failed) { Write-Host "  $f" -ForegroundColor Red }
    Write-Host "Fix the above, then re-run. (CI runs the same gates; this catches them before push.)"
    exit 1
}
Write-Host "All doc gates passed locally. CI remains the authoritative gate." -ForegroundColor Green
exit 0
