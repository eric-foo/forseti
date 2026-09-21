"""Preparation is offline, preserves inputs, and cannot turn uncertainty into fit."""
from copy import deepcopy
import hashlib
from pathlib import Path
import sys
from types import ModuleType

import pytest

from runners import finite_preparation as prep
from runners import run_finite_semantic_consolidation as finite
from judgment.verified_evidence_selection import derive_verified_selection
from test_verified_evidence_selection import originals, write, rehash


@pytest.fixture
def case(originals, tmp_path, monkeypatch):
    dependencies, ids, _ = originals
    source, bundle, verified = derive_verified_selection(dependencies, ids)
    questions = {"questions": [{"id": "q", "question": "What is supported?"}],
        "worker_instructions": "Preserve uncertainty.", "coverage": {"scope": "selected rows"},
        "assessment_only": {"checks": [{"id": "check", "source_rows": [ids[0]], "expectation": "Retain source meaning."}]}}
    paths = {}
    for name, value in zip(("source", "bundle", "verified", "questions", "previous-answer"),
                          (source, bundle, verified, questions, {"status": "unavailable"})):
        paths[name] = tmp_path / "inputs" / (name + ".json")
        write(paths[name], value)
    execution = [arg for name, path in paths.items() for arg in ("--" + name, str(path))]
    execution += ["--output-dir", str(tmp_path / "run")]
    settings = ["--encoding", "fixture", "--effective-context-tokens", "10000000",
        "--generated-content-reserve-tokens", "40000", "--output-reserve-tokens", "16000",
        "--other-overhead-reserve-tokens", "8000"]
    result = tmp_path / "preparation.json"
    def forbidden(*args, **kwargs):
        pytest.fail("preparation invoked an execution/provider boundary")
    monkeypatch.setattr(finite.subprocess, "run", forbidden)
    monkeypatch.setattr(finite.FiniteRun, "run", forbidden)
    monkeypatch.setattr(finite, "select_codex_executable", forbidden)
    # Test-double units ONLY; real-case token validation uses actual tiktoken.
    class CharacterCounter:
        def encode(self, text, **kwargs):
            return text
    monkeypatch.setattr(prep, "offline_tokenizer", lambda name: (CharacterCounter(), "test-double-not-token-measurement"))
    return paths, result, settings, execution


def invoke(case, settings=None, execution=None):
    _, result, default_settings, default_execution = case
    code = finite.main(["prepare", "--result-out", str(result),
        *(default_settings if settings is None else settings), "--",
        *(default_execution if execution is None else execution)])
    return code, finite.read(result) if result.exists() else None


def test_fresh_fit_preserves_semantics_and_emits_owner_parsable_launch(case, tmp_path):
    paths, output, _, execution = case
    before = {p: p.read_bytes() for p in paths.values()}
    execution = ["run-and-report", "--report-dir", str(tmp_path / "report"), "--model", "gpt-6-astra",
                 "--reasoning-effort", "high", "--timeout-seconds", "1800", "--", *execution]
    code, result = invoke(case, execution=execution)
    assert code == 0 and result["status"] == "FINITE_PREPARATION_ESTIMATED_FIT"
    assert result["counts"] == {"source_rows": 3, "semantic_units": 3, "no_unit_rows": 1,
                                "containers": 3, "formation_batches": 1}
    assert result["provider_calls"] == 0 and result["preparation_invocations"] == 1
    assert result["execution_settings"]["model"] == "gpt-5.6-sol"
    argv = result["launch"]["argv"]
    args, report, rebuilt = prep.launch_arguments(argv[5:])
    assert rebuilt == argv and report.model == "gpt-6-astra" and report.reasoning_effort == "high"
    assert report.timeout_seconds == 1800 and args.questions == paths["questions"]
    assert not args.output_dir.exists() and not report.report_dir.exists()
    assert before == {p: p.read_bytes() for p in paths.values()}
    assert "not upper bounds" in " ".join(result["capacity"]["limitations"])


def test_capacity_failure_has_no_launch(case):
    settings = list(case[2])
    settings[settings.index("--effective-context-tokens") + 1] = "1"
    code, result = invoke(case, settings=settings)
    assert code == 1 and result["status"] == "FINITE_PREPARATION_CAPACITY_EXCEEDED"
    assert result["launch"] is None and result["validation"] == "passed"


def test_missing_capacity_inputs_stay_unknown(case):
    code, result = invoke(case, settings=[])
    assert code == 1 and result["status"] == "FINITE_PREPARATION_CAPACITY_UNKNOWN"
    assert "missing explicit capacity inputs" in result["error"] and result["launch"] is None


def test_unavailable_tokenizer_stays_unknown(case, monkeypatch):
    def unavailable(name):
        raise prep.CapacityUnknown("local tokenizer unavailable")
    monkeypatch.setattr(prep, "offline_tokenizer", unavailable)
    code, result = invoke(case)
    assert code == 1 and result["status"] == "FINITE_PREPARATION_CAPACITY_UNKNOWN"
    assert result["validation"] == "passed" and result["launch"] is None


@pytest.mark.parametrize("change, cause", [
    ("absent", "references absent source rows"), ("missing", "requires nonempty source_rows"),
    ("wrong_shape", "requires nonempty source_rows"), ("blank", "requires nonempty source_rows"),
    ("duplicate_check", "unique nonempty identities"), ("expectation", "expectation text"),
    ("bad_checks", "checks must be a list"), ("bad_question", "question text"),
])
def test_commission_failures_report_actual_cause(case, change, cause):
    path = case[0]["questions"]
    questions = finite.read(path)
    check = questions["assessment_only"]["checks"][0]
    if change == "absent": check["source_rows"] = ["not-selected"]
    elif change == "missing": del check["source_rows"]
    elif change == "wrong_shape": check["source_rows"] = "not-a-list"
    elif change == "blank": check["source_rows"] = [""]
    elif change == "duplicate_check": questions["assessment_only"]["checks"].append(deepcopy(check))
    elif change == "expectation": del check["expectation"]
    elif change == "bad_checks": questions["assessment_only"]["checks"] = {}
    else: del questions["questions"][0]["question"]
    write(path, questions)
    code, result = invoke(case)
    assert code == 1 and result["status"] == "FINITE_PREPARATION_REFUSED"
    assert cause in result["error"] and result["launch"] is None


def test_new_case_can_be_sized_before_checks_without_inventing_them(case):
    path = case[0]["questions"]
    questions = finite.read(path)
    del questions["assessment_only"]
    write(path, questions)
    before = path.read_bytes()
    code, result = invoke(case)
    assert code == 1 and result["status"] == "FINITE_PREPARATION_CHECKS_PENDING"
    assert result["capacity"]["fits_planning_allowances"] and result["launch"] is None
    assert path.read_bytes() == before


@pytest.mark.parametrize("change", ["selected", "original", "missing_original"])
def test_changed_provenance_never_passes(case, change):
    path = case[0]["verified"]
    value = finite.read(path)
    if change == "selected":
        value["semantic_units"][0]["conditions"] = ["changed meaning"]
        rehash(value, "compilation_sha256")
        write(path, value)
        cause = "differs from complete unchanged original rows"
    else:
        original = Path(value["verified_row_selection"]["original_inputs"]["source"]["path"])
        if change == "original": original.write_bytes(original.read_bytes() + b" ")
        else: original.unlink()
        cause = "original dependency changed" if change == "original" else "original dependency unavailable"
    code, result = invoke(case)
    assert code == 1 and cause in result["error"] and result["launch"] is None


@pytest.mark.parametrize("target", ["result", "run", "report", "overlap"])
def test_existing_outputs_are_never_overwritten(case, target, tmp_path):
    paths, result, settings, execution = case
    if target == "result":
        result.write_text("prior evidence", encoding="utf-8")
        assert finite.main(["prepare", "--result-out", str(result), *settings, "--", *execution]) == 1
        assert result.read_text() == "prior evidence"
        return
    if target == "overlap":
        result = tmp_path / "run" / "prep.json"
        assert finite.main(["prepare", "--result-out", str(result), *settings, "--", *execution]) == 1
        assert not result.exists() and not result.parent.exists()
        return
    directory = tmp_path / target
    directory.mkdir()
    (directory / "evidence").write_text("unchanged")
    if target == "report":
        execution = ["run-and-report", "--report-dir", str(directory), "--model", "gpt-6-astra",
                     "--reasoning-effort", "high", "--timeout-seconds", "1800", "--", *execution]
    code, record = invoke(case, execution=execution)
    assert code == 1 and "fresh output" in record["error"] and record["launch"] is None
    assert (directory / "evidence").read_text() == "unchanged"


@pytest.mark.parametrize("flag", ["--replay-from", "--provider-root"])
def test_resume_routes_not_admitted(case, flag):
    code, result = invoke(case, execution=[*case[3], flag, str(case[1].parent)])
    assert code == 1 and "fresh run" in result["error"]


def test_offline_encoding_cache_fails_closed_without_download_or_rewrite(tmp_path, monkeypatch):
    tokenizer = ModuleType("tiktoken")
    loader = ModuleType("tiktoken.load")
    tokenizer.load, tokenizer.__version__ = loader, "fixture"
    def network(*a, **kw):
        pytest.fail("attempted tokenizer download")
    loader.read_file_cached = network
    url, data = "https://example.invalid/vocabulary", b"frozen-vocabulary"
    expected = hashlib.sha256(data).hexdigest()
    tokenizer.get_encoding = lambda encoding: loader.read_file_cached(url, expected_hash=expected)
    monkeypatch.setitem(sys.modules, "tiktoken", tokenizer)
    monkeypatch.setitem(sys.modules, "tiktoken.load", loader)
    monkeypatch.setenv("TIKTOKEN_CACHE_DIR", str(tmp_path))
    with pytest.raises(prep.CapacityUnknown, match="cache unavailable"):
        prep.offline_tokenizer("fixture")
    cache = tmp_path / hashlib.sha1(url.encode()).hexdigest()
    cache.write_bytes(b"corrupt")
    with pytest.raises(prep.CapacityUnknown, match="hash unavailable or mismatched"):
        prep.offline_tokenizer("fixture")
    assert cache.read_bytes() == b"corrupt" and loader.read_file_cached is network
    cache.write_bytes(data)
    assert prep.offline_tokenizer("fixture") == (data, "fixture")
