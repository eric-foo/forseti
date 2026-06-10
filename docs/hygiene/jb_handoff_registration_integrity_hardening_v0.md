# Handoff to jb — registration-integrity detector hardening + no_repo review package shape

> **Cross-repo handoff (ORCA → jb).** Two changes ORCA made in the last few turns that
> jb should mirror. **Adapt, don't import:** re-derive against jb's own paths, config
> shape, and policy — do not copy ORCA paths/policy. **Nothing here was applied to jb**
> (ORCA's protected-action guard blocks writing `jb*`; this is a recipe, not an edit).
> The Part A items (F1–F4) are **seams to verify against jb's actual detector**, not
> confirmed jb bugs — the ORCA reviewer never saw jb's code.

## Goal (for the jb lane)

1. **Part A (high value):** bring jb's registration-integrity CI check up to the logic
   ORCA landed *after a cross-vendor review found 4 real seams in the same pattern*.
2. **Part B (optional):** adopt the `no_repo` delegated-review **package-shape**
   refinement in jb's overlay.

## Why this matters

jb **originated** both patterns (the CI missing-artifact check, and the delegated
review-and-patch convention); ORCA replicated them. In use, ORCA's registration-integrity
detector went through a **cross-vendor (different-vendor) `no_repo` adversarial review**,
which found **4 logic seams a same-family review would likely have shared the blind spot
on**. Because jb's detector guards the *same defect class* ("a registry/config names an
artifact by path; the artifact must exist"), it plausibly shares some of these seams.
**Run jb's own cross-vendor review** — do not assume ORCA's findings map 1:1 onto jb's
code.

---

## Part A — detector hardening (verify each seam against jb's detector)

For each: the seam, how it shows up, the fix as a *principle*, and how to verify. jb's
original defect shape was "a `.claude/hooks` entry in settings.json with no script" — the
same config shape as ORCA's — so the fixes likely transfer closely, but **check jb's
actual extraction/existence code first.**

**F1 — existence check accepts directories and out-of-tree paths (major; false-negative).**
- Shows up if the check uses bare `os.path.exists()` / `Path.exists()`. A registered path
  that is actually a **directory**, an **absolute** path, or a `..`-**escape** then counts
  as "present" → a missing artifact passes CI.
- Fix: a registered artifact counts as present only when it resolves to a **regular file
  inside the checkout** — resolve under repo root, reject absolute/`..`-escapes, require
  `is_file()`.
- Verify: a same-named directory, an absolute path, and `../outside` are all rejected.

**F2 — crude artifact-path extraction (major; both false-negative and false-positive).**
- Shows up if the artifact path is pulled by suffix/substring (e.g. "tokens ending in
  `.py`"). It **misses** a compound command (`a.py; b.py` → `a.py;` doesn't match) and
  **over-matches** option values (`--config x.py` is treated as the artifact).
- Fix: extract the artifact **precisely** for jb's config shape — split compound commands
  on `;`/`&&`/`||`/`|`, take the first positional after the interpreter, skip option flags
  and their `=values`.
- Verify: `a.py; b.py` finds both; `--config x.py` / `--flag="x.py"` are NOT the artifact.

**F3 — narrow-type undercapture (major; silent false success).**
- Shows up if the check only covers one artifact type (ORCA's was python-only) but the
  registry can name others → unchecked types **silently pass**.
- Fix (the *non-speculative* branch): **narrow the claim** to what it actually covers AND
  **fail loud** on any registered command it cannot verify (surface it; never silent-pass).
  Do **not** speculatively build support for artifact types jb doesn't actually use.
- Verify: a command outside the supported form is reported and **fails** (non-zero), not
  silently skipped.

**F4 — malformed config silently ignored (minor; coverage can look like success).**
- Shows up if malformed/unexpected config shapes are silently skipped → a schema change
  could make the check a silent no-op.
- Fix: **surface** an unverifiable/unrecognized shape rather than silently passing.
  Declining *full* schema validation is fine — but flag it as a known boundary, don't hide
  it.
- Verify: a readable-but-unsupported shape does not produce an unqualified pass.

**Reference (logic pattern only — do NOT copy paths/policy):** ORCA's hardened detector is
`.agents/checks/registration_integrity.py` (functions `_intree_regular_file`,
`classify_segment`, `scan_command`, `hook_findings`). Use it to see the *shape* of each
fix; re-derive against jb's config and paths.

**After patching:** add a selftest case per finding (F1 dir/escape; F2 compound +
option-value; F3 unverifiable-fails; F4 malformed-surfaced), confirm green on jb's tree,
and run a **cross-vendor adversarial review** of the patched detector before landing.

---

## Part B — `no_repo` delegated-review package shape (optional)

ORCA bound a default **package shape** for `no_repo` delegated reviews (reviewer has no
repo access):

- ship a **self-contained bundle** = the **hash-confirmable verbatim target attachment(s)**
  + a **guardrail-complete `README`** carrying the method, the authority excerpts, and the
  target's contract;
- deliver it with a **thin-wrapper** chat prompt that points the reviewer at the in-bundle
  `README` — the wrapper still carries the **cross-vendor who-constraint** (it must not
  migrate silently into the bundle);
- **inline fallback:** when the reviewer can't read in-bundle files, inline the method in
  the chat prompt instead.

**Where it goes in jb:** jb's **overlay** convention doc (jb owns the delegated-review
convention — ORCA replicated it *from* jb), **not** the reusable skill. The skill owns the
invariants/contract; packaging/delivery shape is an overlay binding. Record a propagation
receipt per jb's conventions. (If jb's convention doesn't yet have a `no_repo` mode, that's
a prerequisite — adopt the mode first, then this shape.)

---

## Process notes (carry these)

- **Run jb's own cross-vendor (`no_repo`) review** of the patched detector — the whole
  point is that a same-family pass shares the author's blind spots.
- **Adapt, don't import:** every path/config detail above is ORCA's; bind jb's.
- **Land per jb's flow** — focused branch, CI green, human-merged (an agent shouldn't merge
  its own PR).
- These are **provisional/advisory** patterns: the review convention claims no validation
  or formal-review authority; the CI check is a strong signal under merge-when-green, not a
  server-enforced gate (state jb's actual enforcement reach honestly).

## What ORCA can additionally hand you (ask)

- ORCA's hardened detector + its selftest as a **reference attachment** (logic pattern).
- A **tailored** version of Part A: ORCA can *read* jb's detector (the guard allows reading
  jb) and pin F1–F4 to jb's actual lines — but that does jb's verification from ORCA, so it
  is opt-in, not the default.
