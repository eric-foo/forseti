#!/usr/bin/env python3
"""W2c doc-term lint: SSOT-scoped ontology-term usage + drift report (REPORT MODE).

WHAT THIS DOES
  Reads the demand-ontology SSOT (`ontology.yaml`) and reports how the migrated
  product corpus (`forseti/product/`) uses ontology TYPE vocabulary:

    KNOWN references  -- distinctive ontology-type tokens that ARE in the SSOT
                         (canonical type names + runtime/storage aliases): a
                         usage map seeding Track-2 (where is each type discussed).
    NEW-TERM-         -- distinctive CamelCase coinages whose HEAD NOUN is an
    CANDIDATES           ontology head-noun ({Caller, Event, Packet, Unit,
                         Vector}, derived from the multi-hump canonical types)
                         but whose full token is NOT in the SSOT (e.g.
                         DemandVector, SignalPacket): ontology-shaped drift.

  A "distinctive" token is >=2 CamelCase humps (Upper+lower each). Single
  ambiguous words (Brand, Product, Call, Reading, Case, ...) are deliberately
  NOT matched -- that exclusion IS the no-naive-prose-grep discipline. CamelCase
  whose head noun is non-ontology (e.g. ...Record, ...Ledger) is ignored, so
  engineering identifiers do not become findings.

WHY (enforcement placement)
  The corpus was migrated out of the doc-checkers' scope and predates ontology
  adoption. As docs evolve they coin type-shaped names the ontology never
  adopted; that semantic drift is invisible until a reader trips on it. This
  surfaces it at the moment a diff lands -- without grepping prose.

HARD BOUNDARY
  Read-only. No git calls. No writes. REPORT MODE only: the frozen predicate is
  strict-minus-exit-0 -- it computes what a future orca/ strict gate would flag
  but ALWAYS exits 0 (the Phase-3 ratchet flips the exit only). Fails OPEN on
  infrastructure gaps (no PyYAML, missing ontology.yaml / corpus): prints an
  advisory and exits 0, never ghost-fails. Excludes the ontology's own
  definition home (foundation/ontology/ -- the term home, not drift) and
  _scratch/_inbox.

MODES
  check_doc_terms.py --report-orca   REPORT MODE over forseti/product/; always exit 0
  check_doc_terms.py --check         verbose human-readable report; always exit 0
  check_doc_terms.py --selftest      pure-function cases (+ live SSOT vocab); exit 0/1
"""
from __future__ import annotations

import os
import re
import sys
from pathlib import Path
from typing import NamedTuple

YAML_REL = "forseti/product/spines/foundation/ontology/ontology.yaml"
CORPUS_REL = "forseti/product"
ONTOLOGY_HOME_REL = "forseti/product/spines/foundation/ontology"  # the term home (excluded)

# A distinctive ontology-shaped token: >=2 CamelCase humps (Upper followed by
# lower, repeated). Matches TrendVector / SourceCapturePacket; NOT single words
# (Brand), NOT acronyms (HTTP), NOT lowercase-leading identifiers.
_CAMEL_TOKEN_RE = re.compile(r"\b[A-Z][a-z]+(?:[A-Z][a-z]+)+\b")
_HUMP_RE = re.compile(r"[A-Z][a-z]+")


def repo_root() -> Path:
    """Repo root, derived from this file's location (.agents/hooks/<this>)."""
    return Path(__file__).resolve().parents[2]


# ---------------------------------------------------------------------------
# Pure token helpers
# ---------------------------------------------------------------------------

def _humps(name: str) -> list[str]:
    return _HUMP_RE.findall(name)


def head_noun_of(token: str) -> str | None:
    """Last CamelCase hump of a >=2-hump token, else None (single-word tokens
    have no distinctive head noun)."""
    h = _humps(token)
    return h[-1] if len(h) >= 2 else None


def _singular(token: str) -> str:
    """Strip a single trailing plural 's' (not 'ss'), so TrendVectors folds to
    the known TrendVector. Conservative: only touches >2-char tokens."""
    if len(token) > 2 and token.endswith("s") and not token.endswith("ss"):
        return token[:-1]
    return token


def classify_token(
    token: str, canonical: set[str], aliases: set[str], head_nouns: set[str]
) -> tuple[str, str]:
    """Return (kind, resolved) where kind is 'known' | 'candidate' | 'ignore'.

    known     : token (or its singular) is an SSOT canonical type or alias.
    candidate : not known, but its head noun is an ontology head noun
                (an ontology-shaped coinage -- the Track-2 drift signal).
    ignore    : a CamelCase token with a non-ontology head noun.
    Pure function (testable).
    """
    sing = _singular(token)
    if token in canonical or token in aliases:
        return "known", token
    if sing in canonical or sing in aliases:
        return "known", sing
    if head_noun_of(sing) in head_nouns:
        return "candidate", token
    return "ignore", token


def build_vocab(
    ss: dict,
) -> tuple[set[str], set[str], set[str], dict[str, str]]:
    """From the ontology SSOT mapping, derive:
      canonical        : canonical type names (the `types` roster keys)
      aliases          : runtime/composed class names + name_alias values that
                         are NOT already canonical (CamelCase storage aliases)
      head_nouns       : distinctive head nouns from MULTI-HUMP CANONICAL types
                         only (alias head nouns like Ledger/Report are excluded
                         to stay ontology-grounded and low-noise)
      alias_to_concept : alias -> ontology concept (for the usage map)
    Pure function (testable).
    """
    canonical = set((ss.get("types") or {}).keys())
    aliases: set[str] = set()
    alias_to_concept: dict[str, str] = {}

    def _class_of(spec: object) -> str | None:
        if isinstance(spec, str) and ":" in spec:
            return spec.rsplit(":", 1)[1].strip() or None
        return None

    def _add_alias(cls: str | None, concept: str) -> None:
        if cls and cls not in canonical:
            aliases.add(cls)
            alias_to_concept.setdefault(cls, concept)

    for concept, b in (ss.get("runtime_bindings") or {}).items():
        if not isinstance(b, dict):
            continue
        _add_alias(_class_of(b.get("runtime")), concept)
        na = b.get("name_alias")
        if isinstance(na, str):
            _add_alias(na.strip() or None, concept)
        cw = b.get("composed_with")
        if isinstance(cw, list):
            for spec in cw:
                _add_alias(_class_of(spec), concept)

    head_nouns = {h for t in canonical if (h := head_noun_of(t)) is not None}
    return canonical, aliases, head_nouns, alias_to_concept


# ---------------------------------------------------------------------------
# Corpus scan
# ---------------------------------------------------------------------------

class TermReport(NamedTuple):
    known: dict[str, tuple[int, set[str]]]       # token -> (count, files)
    candidates: dict[str, tuple[int, set[str]]]  # token -> (count, files)
    files_scanned: int


def _iter_corpus_md(root: Path):
    corpus = root / CORPUS_REL
    if not corpus.is_dir():
        return
    for dirpath, dirnames, filenames in os.walk(corpus):
        dirnames[:] = [
            d for d in dirnames
            if "_scratch" not in d and d not in ("_inbox", "node_modules")
        ]
        rel_dir = Path(dirpath).relative_to(root).as_posix()
        if rel_dir == ONTOLOGY_HOME_REL or rel_dir.startswith(ONTOLOGY_HOME_REL + "/"):
            continue  # the ontology definition home is the term home, not drift
        for fn in filenames:
            if fn.endswith(".md"):
                yield Path(dirpath) / fn


def analyze(
    root: Path, canonical: set[str], aliases: set[str], head_nouns: set[str]
) -> TermReport:
    known: dict[str, list] = {}
    cands: dict[str, list] = {}
    files = 0
    for fp in _iter_corpus_md(root):
        files += 1
        try:
            text = fp.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        rel = fp.relative_to(root).as_posix()
        for m in _CAMEL_TOKEN_RE.finditer(text):
            kind, resolved = classify_token(m.group(0), canonical, aliases, head_nouns)
            if kind == "known":
                e = known.setdefault(resolved, [0, set()])
            elif kind == "candidate":
                e = cands.setdefault(resolved, [0, set()])
            else:
                continue
            e[0] += 1
            e[1].add(rel)
    return TermReport(
        known={k: (c, fs) for k, (c, fs) in known.items()},
        candidates={k: (c, fs) for k, (c, fs) in cands.items()},
        files_scanned=files,
    )


def _load_ssot(root: Path):
    """Return the parsed SSOT mapping, or None on a fail-open infra gap."""
    try:
        import yaml
    except Exception:
        return None
    yp = root / YAML_REL
    if not yp.is_file():
        return None
    try:
        ss = yaml.safe_load(yp.read_text(encoding="utf-8"))
    except Exception:
        return None
    return ss if isinstance(ss, dict) else None


# ---------------------------------------------------------------------------
# Mode runners
# ---------------------------------------------------------------------------

def _print_report(root: Path, verbose: bool) -> int:
    ss = _load_ssot(root)
    if ss is None:
        print("check_doc_terms: SSOT unavailable (no PyYAML / missing ontology.yaml); nothing to report")
        return 0
    canonical, aliases, head_nouns, alias_to_concept = build_vocab(ss)
    rep = analyze(root, canonical, aliases, head_nouns)

    known_refs = sum(c for c, _ in rep.known.values())
    known_files = len({f for _, fs in rep.known.values() for f in fs})
    cand_refs = sum(c for c, _ in rep.candidates.values())
    cand_files = len({f for _, fs in rep.candidates.values() for f in fs})

    print("check_doc_terms --report-orca (REPORT MODE, exit 0; not a gate):")
    print("  scope: %s/  (excl. foundation/ontology/, _scratch)  |  predicate = strict-minus-exit-0" % CORPUS_REL)
    print("  SSOT vocab: %d canonical types, %d aliases, head-nouns %s"
          % (len(canonical), len(aliases), "{%s}" % ", ".join(sorted(head_nouns))))
    print("  files scanned: %d" % rep.files_scanned)
    print()
    print("  KNOWN ontology-type references (usage map): %d refs across %d files"
          % (known_refs, known_files))
    for tok in sorted(rep.known, key=lambda t: (-rep.known[t][0], t)):
        count, files = rep.known[tok]
        tag = ("  [alias -> %s]" % alias_to_concept[tok]) if tok in aliases else ""
        print("    %-24s : %3d refs in %2d files%s" % (tok, count, len(files), tag))
    print()
    print("  NEW-TERM-CANDIDATES (ontology head-noun, not in SSOT): %d refs across %d files"
          % (cand_refs, cand_files))
    for tok in sorted(rep.candidates, key=lambda t: (-rep.candidates[t][0], t)):
        count, files = rep.candidates[tok]
        print("    %-24s : %3d refs in %2d files   [head: %s]"
              % (tok, count, len(files), head_noun_of(_singular(tok))))
        if verbose:
            for f in sorted(files):
                print("        %s" % f)
    print()
    print("  total report findings (candidates): %d" % len(rep.candidates))
    return 0


def run_report_orca(root: Path) -> int:
    return _print_report(root, verbose=False)


def run_check(root: Path) -> int:
    return _print_report(root, verbose=True)


# ---------------------------------------------------------------------------
# Selftest
# ---------------------------------------------------------------------------

def selftest() -> int:
    ok = True

    def check(label: str, got, exp):
        nonlocal ok
        status = "PASS" if got == exp else "FAIL"
        if got != exp:
            ok = False
        print("%s  %-44s got=%s" % (status, label, got))

    print("--- head_noun_of / _singular / token regex ---")
    check("head TrendVector", head_noun_of("TrendVector"), "Vector")
    check("head WindCaller", head_noun_of("WindCaller"), "Caller")
    check("head single word -> None", head_noun_of("Brand"), None)
    check("head SourceCapturePacket", head_noun_of("SourceCapturePacket"), "Packet")
    check("singular plural", _singular("TrendVectors"), "TrendVector")
    check("singular keeps ss", _singular("Address"), "Address")
    check("regex multi-hump", _CAMEL_TOKEN_RE.findall("a TrendVector here"), ["TrendVector"])
    check("regex skips single word", _CAMEL_TOKEN_RE.findall("the Brand and HTTP API"), [])
    check("regex catches alias", _CAMEL_TOKEN_RE.findall("see SourceCapturePacket x"), ["SourceCapturePacket"])

    print()
    print("--- build_vocab (synthetic SSOT) ---")
    synth = {
        "types": {"TrendVector": {}, "CapturePacket": {}, "Brand": {}, "Case": {}},
        "runtime_bindings": {
            "CapturePacket": {"runtime": "x/y.py:SourceCapturePacket", "name_alias": "SourceCapturePacket"},
            "Case": {"runtime": "a/b.py:FacilitatorLedger", "composed_with": ["c/d.py:CaseReport"]},
        },
    }
    can, ali, heads, a2c = build_vocab(synth)
    check("canonical", can, {"TrendVector", "CapturePacket", "Brand", "Case"})
    check("aliases", ali, {"SourceCapturePacket", "FacilitatorLedger", "CaseReport"})
    check("head_nouns (canonical multi-hump only)", heads, {"Vector", "Packet"})
    check("alias_to_concept Ledger", a2c.get("FacilitatorLedger"), "Case")

    print()
    print("--- classify_token ---")
    check("known canonical", classify_token("TrendVector", can, ali, heads), ("known", "TrendVector"))
    check("known alias", classify_token("SourceCapturePacket", can, ali, heads), ("known", "SourceCapturePacket"))
    check("known plural folds", classify_token("TrendVectors", can, ali, heads), ("known", "TrendVector"))
    check("candidate head-noun", classify_token("DemandVector", can, ali, heads), ("candidate", "DemandVector"))
    check("ignore non-ontology head", classify_token("SignalContentRecord", can, ali, heads), ("ignore", "SignalContentRecord"))

    print()
    print("--- live SSOT vocab (faithfulness) ---")
    ss = _load_ssot(repo_root())
    if ss is None:
        print("INFO  live SSOT unavailable -- skipping live vocab check (fail-open)")
    else:
        can, ali, heads, _ = build_vocab(ss)
        check("live head_nouns", heads, {"Caller", "Event", "Packet", "Unit", "Vector"})
        live_ok = len(can) == 17 and {"SourceCapturePacket", "FacilitatorLedger", "CaseReport"} <= ali
        check("live canonical=17 & aliases present", live_ok, True)

    print()
    print("SELFTEST", "OK" if ok else "FAILED")
    return 0 if ok else 1


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main(argv: list[str]) -> int:
    if "--selftest" in argv:
        return selftest()
    try:
        root = repo_root()
    except Exception as exc:
        sys.stderr.write("check_doc_terms: cannot determine repo root: %s\n" % exc)
        return 0
    if "--check" in argv:
        return run_check(root)
    if "--report-orca" in argv:
        return run_report_orca(root)
    print("Usage: check_doc_terms.py --report-orca | --check | --selftest")
    print("  --report-orca  REPORT MODE over forseti/product/: usage map + new-term-candidates, exit 0")
    print("  --check        verbose report (lists candidate files), exit 0")
    print("  --selftest     pure-function self-check")
    return 1


if __name__ == "__main__":
    try:
        sys.exit(main(sys.argv[1:]))
    except Exception as exc:
        sys.stderr.write("check_doc_terms: internal error, allowing: %s\n" % exc)
        sys.exit(0)  # fail open
