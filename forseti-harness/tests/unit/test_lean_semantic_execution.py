"""Native delivery/consumer contracts with simulated providers, not quality proof."""
from copy import deepcopy
import json
from pathlib import Path
from threading import Barrier, Lock

import pytest

from judgment import lean_evidence_consolidation as lean
from judgment.phase_a_evidence_consumer import consume_checked_packet
from runners import run_semantic_evidence_integration as native
from runners import semantic_execution as execution
from test_lean_evidence_consolidation import fixture, respond
from test_semantic_execution import simulated_provider, write


def inputs(tmp_path, rows=40):
    source, commission, _ = fixture()
    capacity = {**lean.DEFAULT_CAPACITY, "max_rows_per_slice": rows}
    paths = {name: tmp_path / (name + ".json") for name in ("source", "commission", "capacity")}
    for name, value in zip(paths, (source, commission, capacity)):
        write(paths[name], value)
    return dict(source_path=paths["source"], run_dir=tmp_path / "run",
                answer_commission_path=paths["commission"], answer_capacity_path=paths["capacity"])


def offline_complete(kwargs, tmp_path):
    for _ in range(20):
        state = native.advance_semantic_run(**kwargs)
        if not state["judgment_requests"]:
            assert state["status"] == "LEAN_EVIDENCE_CONSOLIDATION_CHECKED", state
            return state
        for item in state["judgment_requests"]:
            candidate = tmp_path / (item["job_sha256"] + ".json")
            write(candidate, respond(lean.read(item["job_path"])))
            native.submit_judgment_job(job_path=Path(item["job_path"]),
                expected_sha256=item["job_sha256"], response_path=candidate)
    raise AssertionError("did not complete")


def test_default_native_route_intake_and_exact_checked_consumer(tmp_path):
    kwargs = inputs(tmp_path)
    first = native.advance_semantic_run(**kwargs)
    assert first["phase"] == "lean_read"
    job = first["judgment_requests"][0]
    intake = native.intake_judgment_job(job_path=Path(job["job_path"]), expected_sha256=job["job_sha256"])
    assert intake["status"] == "SEMANTIC_JUDGMENT_INTAKE_COMPLETE"
    state = offline_complete(kwargs, tmp_path)
    packet = lean.read(state["packet_path"])
    artifact = consume_checked_packet(packet)
    assert artifact["answers"] == packet["answers"]
    assert artifact["review"] == packet["review"]
    assert any("gift" in r["text"] for r in artifact["original_observations"])
    assert not (kwargs["run_dir"] / "extraction").exists()
    assert not (kwargs["run_dir"] / "bundle.json").exists()
    with pytest.raises(ValueError, match="question"):
        consume_checked_packet(packet, question_ids=["foreign"])
    before = {p: p.read_bytes() for p in kwargs["run_dir"].rglob("*") if p.is_file()}
    assert native.advance_semantic_run(**kwargs)["packet_sha256"] == packet["packet_sha256"]
    assert {p: p.read_bytes() for p in before} == before


def test_maintained_provider_three_calls_no_project_preload_and_zero_call_restart(tmp_path, monkeypatch):
    kwargs = inputs(tmp_path)
    calls = []

    class Answers:
        def pop(self, index):
            command = calls[-1]["command"]
            job_hash = Path(command[command.index("--prompt-file") + 1]).parent.name
            return respond(lean.read(kwargs["run_dir"] / "requests" / job_hash / "request.json"))

    simulated_provider(monkeypatch, tmp_path, Answers(), calls)
    settings = dict(advance_kwargs=kwargs, model="offline-model", reasoning_effort="high",
                    timeout_seconds=60, max_jobs=3)
    state = execution.execute_semantic_run(**settings)
    assert state["status"] == "LEAN_EVIDENCE_CONSOLIDATION_CHECKED", state
    assert state["executed_job_count"] == len(calls) == 3
    assert all("--preload-context" not in c["command"] for c in calls)
    assert [lean.read(p)["phase"] for p in sorted((kwargs["run_dir"] / "requests").glob("*/request.json"))].count("lean_review") == 1
    again = execution.execute_semantic_run(**settings)
    assert again["executed_job_count"] == 0 and len(calls) == 3
    assert again["packet_sha256"] == state["packet_sha256"]


@pytest.mark.parametrize("failure", [False, True])
def test_parallel_slices_respect_bound_and_preserve_successful_peer(tmp_path, monkeypatch, failure):
    kwargs = inputs(tmp_path, rows=1)
    barrier, guard = Barrier(2), Lock()
    seen, accepted = [], []

    def execute(**job):
        request = lean.read(job["job_path"])
        with guard:
            seen.append(job["job_sha256"])
        intent = job["provider_root"] / job["job_sha256"] / "job/launch-001.json"
        write(intent, {"simulated": True})
        barrier.wait(timeout=10)
        if failure and request["payload"]["records"][0]["row_id"] == "r0":
            raise ValueError("injected provider failure")
        candidate = tmp_path / (job["job_sha256"] + ".json")
        write(candidate, respond(request))
        result = native.submit_judgment_job(job_path=job["job_path"],
            expected_sha256=job["job_sha256"], response_path=candidate)
        with guard:
            accepted.append(job["job_sha256"])
        return result

    monkeypatch.setattr(execution, "execute_judgment_job", execute)
    result = execution.execute_semantic_run(advance_kwargs=kwargs, model="offline-model",
        reasoning_effort="high", timeout_seconds=60, max_jobs=2)
    assert len(seen) == result["executed_job_count"] == 2
    assert result["status"] == ("SEMANTIC_EXECUTION_BLOCKED" if failure else "SEMANTIC_EXECUTION_LIMIT_REACHED")
    assert len(accepted) == (1 if failure else 2)
    remaining = native.advance_semantic_run(**kwargs)["judgment_requests"]
    assert not set(accepted) & {r["job_sha256"] for r in remaining}
    assert all((kwargs["run_dir"] / "requests" / value / "response.receipt.json").exists() for value in accepted)


def test_cli_projection_delivery_and_pin_rejections(tmp_path, capsys):
    kwargs = inputs(tmp_path)
    state = offline_complete(kwargs, tmp_path)
    projected, delivered = tmp_path / "projected.json", tmp_path / "answer.json"
    assert native.main(["project-evidence-packet", "--view", state["packet_path"],
                        "--packet-out", str(projected)]) == 0
    assert json.loads(capsys.readouterr().out)["model_api_calls"] == 0
    assert lean.read(projected) == lean.read(state["packet_path"])
    assert native.main(["consume-evidence-packet", "--packet", str(projected),
                        "--artifact-out", str(delivered)]) == 0
    assert json.loads(capsys.readouterr().out)["model_api_calls"] == 0
    assert lean.read(delivered)["answers"] == lean.read(projected)["answers"]
    changed = deepcopy(lean.read(kwargs["answer_commission_path"]))
    changed["questions"][0]["question"] += " changed"
    write(kwargs["answer_commission_path"], changed)
    assert native.advance_semantic_run(**kwargs)["status"] == "SEMANTIC_ADVANCE_BLOCKED"
    assert native.advance_semantic_run(**{**inputs(tmp_path / "fresh"), "max_prompt_bytes": 120000})["status"] == "SEMANTIC_ADVANCE_BLOCKED"


def test_unknown_saved_method_cannot_fall_back_to_history(tmp_path):
    kwargs = inputs(tmp_path)
    write(kwargs["run_dir"] / "start.json", {"method_version": "future-unknown"})
    result = native.advance_semantic_run(**kwargs)
    assert result["status"] == "SEMANTIC_ADVANCE_BLOCKED"
    assert "unsupported pinned" in result["error"]
    assert not (kwargs["run_dir"] / "requests").exists()
