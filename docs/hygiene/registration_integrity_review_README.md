# Adversarial Review Commission — `registration_integrity.py` (no-repo, cross-vendor)

> You are reading the **executable instructions** for this review. Read this whole
> file, then perform the review and return your findings. You need nothing outside
> this bundle — no repo, no tools, no skills.

## 0. Who may run this — de-correlation gate (do this first)

You are commissioned as a **de-correlated adversarial reviewer (the "controller")**.
You **must be from a different model vendor than Anthropic / Claude**, which authored
the artifact under review. **If you are an Anthropic / Claude model, stop now and say
so** — you cannot satisfy the cross-vendor de-correlation this commission requires.
Your role is controller (review only); you do **not** patch.

## 1. This bundle

Confirm each file's `sha256` against `MANIFEST.txt`. If a hash does not match, proceed
**advisory-only** and say so.

- `registration_integrity.py` — **the TARGET** under review (a CI defect detector).
- `settings.json` — the file the detector parses (decision-bearing input).
- `ci_registration_integrity_check_proposal_v0.md` — the detector's stated intent / contract.

The formal ORCA review tooling is **not available to you**, so your result is **advisory
critique, not a formal verdict** — state that explicitly.

## 2. What the target is

`registration_integrity.py` is a high-stakes **validation instrument**: a CI check that
fails when a hook registered in `settings.json` (`python .agents/hooks/<x>.py`) points at
a script that does not exist in the tree. A bug in it could **mask the defect** it guards
(false-negative) or **fail valid pull requests** (false-positive). Review its **runtime
behavior and logic** — reason concretely about what the Python does on real and
adversarial inputs, not its prose.

## 3. Authority the target must conform to (ORCA `AGENTS.md` kernel — scope discipline)

> Surface ambiguity before acting. **Default to the smallest complete intervention.**
> Every changed line must trace to the request or required validation. **Preserve real
> failure visibility; never create fake success paths.**
> *Complete* is load-bearing — do not underfix to minimize diff. *Smallest* is also
> load-bearing — no unrelated cleanup, speculative abstractions, or broad rewrites.

## 4. What "correct" means for this target (its stated contract)

1. **Decidable from the checked-out tree alone** — no base ref, no git history, no network
   (must work on a shallow CI checkout and never false-positive on "new in this PR, not
   yet on main").
2. **Directional** — a registry entry must have its file (entry → file); it must **never**
   flag a file that merely lacks a registry entry (READMEs / special files are legitimately
   unregistered).
3. **Fails loud** — unknown/empty `--checks` or unreadable settings → non-zero; **never a
   silent no-op**. Exit codes: `0` pass · `1` dangling reference (the defect) · `2`
   misuse/internal error.

## 5. The review method (follow in order)

### 5.1 Your stance
Read-only, **advisory-only** adversarial review. Be **maximally adversarial** about
material, decision-relevant failure modes; do not soften a real failure mode because
remediation is hard. Do not retarget or widen beyond the named target.

### 5.2 Method (order matters)
First a structured reasoning pass: enumerate the target's load-bearing claims, the
boundary/decision criteria, and the likely failure modes — **before** any finding.

### 5.3 Review checks (be maximally adversarial)
- **Authority / hierarchy conformance** with §3.
- **Internal consistency**; self-contradiction.
- **Missing required inputs / unbound roles or intent.**
- **Output-mode / interface correctness** (exit codes, `--checks` selector).
- **Downstream executability:** can a CI job actually act on this from the stated command?
- **Fitness to goal:** does it meet §4, and **is the goal itself right?** Does "every
  registered hook script exists" actually capture the fresh-clone-breaking defect class,
  or is there a seam it misses (other registries? `settings.local.json`? non-`python`
  hook commands? a `.py` token that isn't the script)? If no checkable success bar is
  provided, name `no checkable success bar bound`.
- **Overclaims:** readiness/validation/approval/proof unsupported by evidence.
- **Leakage** of out-of-scope or unrelated-project policy.
- **Scope discipline:** does it do *more* than its purpose requires (scope inflation,
  speculative additions) — or *less* (underfix, symptom-only)? Flag both.

### 5.4 Severity meaning
`critical` / `major` / `minor` are **finding-priority labels only** — no approval,
rejection, readiness, validation, or mandatory-remediation authority.

## 6. Return contract (findings, NOT a diff)

Lead with a compact `review_summary`, then findings:

    review_summary:
      status: review_complete | blocked
      recommendation: <one line; advisory>
      findings_count: <int>
      blocking_findings: []      # critical/major, one line each
      advisory_findings: []      # minor/optional, one line each
      summary: <one line>

Then findings ordered `critical` → `major` → `minor`. For each: `severity`, `location`,
`issue`, `evidence` (cite the target line **and** the conflicting authority/contract
clause), `impact`, `minimum_closure_condition` (the end state that resolves it — **not**
how to implement), `next_authorized_action`, and an advisory remediation direction.
**Do not emit executor-ready patch steps or a diff** — you have no repo. If you find no
issues, say so and list residual risks / test gaps.

## 7. Review-use boundary (non-claims)

Your findings are **decision input only** for the commissioning owner — not approval,
validation, readiness, proof, mandatory remediation, or executor-ready instructions. The
ORCA home model (Anthropic/Claude) will **adjudicate each finding as a claim**, apply any
accepted fix itself within a bounded scope, and run a **same-vendor bounded recheck**
before keeping anything. Nothing downstream is bound by this review unless a separate
authorized decision accepts it.
