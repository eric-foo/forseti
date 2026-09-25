"""Offline consumer and rejected-input tests; synthetic provider receipts only."""
import copy
import contextlib
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import source_row_labelling as tool


class SourceRowLabelling(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="forseti-label-tool-test-")
        self.base = Path(self.temp.name).resolve()
        self.addCleanup(self.temp.cleanup)
        self.root = self.base / "run"
        self.authority = self.base / "authority.md"
        self.authority.write_bytes(tool.AUTHORITY.read_bytes())
        self.policy = patch.object(tool, "AUTHORITY", self.authority)
        self.policy.start()
        self.addCleanup(self.policy.stop)
        # These tests verify packing and integrity, not a model/tokenizer estimate.
        self.counter = patch.object(tool, "input_tokens", return_value=100)
        self.counter.start()
        self.addCleanup(self.counter.stop)
        chosen = []
        for index in range(2):
            tid = f"thread-{index}"
            raw = {"thread": {"thread_id": tid, "title": "Routine question", "subreddit": "fixture"},
                   "post": {"body_text": "A stays good; B needs a pause.", "author_state": "speaker-A"},
                   "comments": [{"comment_id": f"c{index}", "parent_id": f"t3_{tid}",
                                 "author_state": "speaker-B", "body_text": "I heard C helps, but never tried it."}],
                   "limitations": ["partial capture"], "unknown_extra": {"keep": ["all", "fields"]}}
            path = self.base / f"{tid}.json"
            tool.write(path, raw)
            chosen.append({"thread_id": tid, "content_record": str(path), "source_sha256": tool.sha(path)})
        self.selection = self.base / "selection.json"
        tool.write(self.selection, {"threads": chosen})
        self.task = "Broad retrieval of source actions; no synthesis or efficacy finding."
        tool.prepare(self.selection, self.root, self.task)
        self.attempt = self.base / "synthetic-attempt"
        self.attempt.mkdir()
        self.rows = [{"id": rid, "types": ["experience"], "topics": ["routine"],
                      "meaning": "A stays good; B needs no pause." if rid == "r0001" else "Café repeated repeated; unchanged.",
                      "context_refs": []} for rid in tool.load(self.root / "registry.json")]
        self.original = (json.dumps({"rows": self.rows}, ensure_ascii=False, indent=3) + "\r\n").encode()
        tool.write(self.attempt / "response.json", self.original)
        manifest = tool.load(self.root / "manifest.json")
        self.receipt = {"outcome": "PROCESS_COMPLETED", "exit_code": 0,
                        "response_sha256": tool.digest(self.original), "prompt_sha256": manifest["files"]["prompt.txt"],
                        "response_schema_sha256": manifest["files"]["response-schema.json"],
                        "usage": {"input_tokens": 12, "output_tokens": 8, "reasoning_output_tokens": 2}}
        tool.write(self.attempt / "execution_receipt.json", self.receipt)
        tool.write(self.base / "private-cases.json", {"expected": "PRIVATE_NOT_MODEL_INPUT_7z3"})

    def build(self):
        return tool.review(self.root, self.attempt)

    def edits(self, **changes):
        edit = {"id": "r0001", "finding": "No pause reverses the source condition and changes usable advice.",
                "severity": "material", "source_refs": ["r0001"],
                "meaning_replacements": [{"old": "B needs no pause", "new": "B needs a pause"}], "set_fields": {}}
        edit.update(changes)
        return {"edits": [edit]}

    def test_rules_reach_every_consumer_and_sources_roundtrip(self):
        result = self.build()
        self.assertEqual(result["reported_generation_tokens"], 20)  # reasoning is a subset
        self.assertIsNone(result["claude_usage"])
        rules = (self.root / "rules.txt").read_text(encoding="utf-8")
        command = tool.load(self.root / "manifest.json")["generation_command"]
        self.assertEqual(Path(command[command.index("--prompt-file") + 1]).read_text(encoding="utf-8"),
                         (self.root / "prompt.txt").read_text(encoding="utf-8"))
        self.assertEqual(tool.load(command[command.index("--output-schema") + 1]), tool.SCHEMA)
        for name in ("prompt.txt", "review/instructions.txt", "adjudication-instructions.txt"):
            supplied = (self.root / name).read_text(encoding="utf-8")
            self.assertEqual(supplied.count(rules), 1)
            self.assertIn(self.task, supplied)
            self.assertNotIn("PRIVATE_NOT_MODEL_INPUT_7z3", supplied)
        view = tool.load(self.root / "review/view.json")
        prompt = (self.root / "prompt.txt").read_text(encoding="utf-8")
        supplied = tool.loads(prompt.split("FROZEN ORIGINAL INPUT (JSON)\n")[1])
        self.assertEqual(len(view["threads"]), 2)  # no baseline + four-thread restriction
        for paired, source in zip(view["threads"], supplied["threads"]):
            restored = copy.deepcopy(paired["metadata"])
            restored["post"] = copy.deepcopy(paired["rows"][0]["source"])
            restored["comments"] = [copy.deepcopy(p["source"]) for p in paired["rows"][1:]]
            self.assertEqual(restored, source)
            for pair in paired["rows"]:
                self.assertEqual(list(pair), ["source", "label"])
                self.assertEqual(pair["source"]["evidence_id"], pair["label"]["id"])
            for row in [restored["post"], *restored["comments"]]:
                del row["evidence_id"]
            native = self.base / (restored["thread"]["thread_id"] + ".json")
            self.assertEqual(restored, tool.load(native))

    def test_frozen_rules_survive_later_policy_change(self):
        old = (self.root / "rules.txt").read_bytes()
        self.authority.write_text("### Source-label materiality\nNEW_POLICY_SENTINEL\n", encoding="utf-8")
        self.build()
        self.assertIn(old.decode(), (self.root / "review/instructions.txt").read_text(encoding="utf-8"))
        new_root = self.base / "later-run"
        tool.prepare(self.selection, new_root)
        self.assertIn("NEW_POLICY_SENTINEL", (new_root / "prompt.txt").read_text(encoding="utf-8"))
        self.assertNotEqual(old, (new_root / "rules.txt").read_bytes())

    def test_missing_authority_and_capacity_fail_before_writes(self):
        destination = self.base / "missing-policy"
        self.authority.write_text("Policy section absent", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "authority missing"):
            tool.prepare(self.selection, destination)
        self.assertFalse(destination.exists())
        self.authority.write_text("### Source-label materiality\nBounded rule\n", encoding="utf-8")
        with patch.object(tool, "input_tokens", return_value=112001):
            with self.assertRaisesRegex(ValueError, "capacity exceeded"):
                tool.prepare(self.selection, destination)
        self.assertFalse(destination.exists())

    def test_exact_application_preserves_original_and_other_bytes(self):
        self.build()
        accepted = self.base / "accepted.json"
        tool.write(accepted, self.edits())
        result = tool.apply(self.root, accepted)
        candidate = self.root / "adjudicated/response.json"
        self.assertEqual(candidate.read_bytes(), self.original.replace(b"B needs no pause", b"B needs a pause"))
        self.assertEqual((self.root / "review/original-response.json").read_bytes(), self.original)
        self.assertEqual((result["changed_rows"], result["changed_fields"]), (1, 1))
        self.assertEqual(result["semantic_acceptance"], "not_established")
        # Later edits to the operator's input cannot silently alter the accepted snapshot.
        accepted.write_text('{"edits":[]}', encoding="utf-8")
        self.assertEqual(tool.check(self.root), result)
        with self.assertRaisesRegex(ValueError, "already reserved"):
            tool.apply(self.root, accepted)

    def test_no_proposals_are_auto_applied_and_zero_edits_preserve_bytes(self):
        self.build()
        tool.write(self.root / "review/edits.json", self.edits())
        self.assertFalse((self.root / "adjudicated").exists())
        accepted = self.base / "accepted-none.json"
        tool.write(accepted, {"edits": []})
        tool.apply(self.root, accepted)
        self.assertEqual((self.root / "adjudicated/response.json").read_bytes(), self.original)

    def test_wrong_receipt_and_failed_attempt_are_rejected(self):
        path = self.attempt / "execution_receipt.json"
        for update, message in [({"prompt_sha256": "0" * 64}, "input hash mismatch"),
                                ({"response_sha256": "0" * 64}, "response hash mismatch"),
                                ({"outcome": "TIMED_OUT"}, "did not complete")]:
            path.write_text(json.dumps(self.receipt | update), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, message):
                self.build()
            self.assertFalse((self.root / "review").exists())

    def test_response_identity_and_cross_thread_context_rejected(self):
        for update, message in [({"id": "foreign"}, "ID/order"),
                                ({"context_refs": ["r0003"]}, "invalid context ref")]:
            response = {"rows": copy.deepcopy(self.rows)}
            response["rows"][0].update(update)
            with self.assertRaisesRegex(ValueError, message):
                tool.validate_response(self.root, response)

    def test_precise_edit_rejections(self):
        self.build()
        samples = [
            (self.edits(id="foreign"), "foreign edit"),
            (self.edits(meaning_replacements=[{"old": "absent", "new": "x"}]), "stale or ambiguous"),
            (self.edits(id="r0002", source_refs=["r0002"], meaning_replacements=[{"old": "repeated", "new": "x"}]), "stale or ambiguous"),
            (self.edits(meaning_replacements=[{"old": "B needs", "new": "x"}, {"old": "needs no", "new": "y"}]), "overlapping"),
            (self.edits(set_fields={"id": {"old": "r0001", "new": "other", "reason": "invalid"}}), "forbidden edit"),
            (self.edits(source_refs=["r0001", "r0003"]), "source refs invalid"),
            (self.edits(set_fields={"types": {"old": ["intent"], "new": ["recommendation"], "reason": "stale"}}), "stale field"),
        ]
        duplicates = self.edits()
        duplicates["edits"] *= 2
        samples.append((duplicates, "duplicate edit row"))
        for value, message in samples:
            with self.subTest(message=message):
                with self.assertRaisesRegex(ValueError, message):
                    tool.corrected_bytes(self.root, value)
        self.assertFalse((self.root / "adjudicated").exists())

    def test_tamper_and_no_overwrite_guards(self):
        self.build()
        with self.assertRaisesRegex(ValueError, "already exists"):
            tool.prepare(self.selection, self.root)
        with self.assertRaisesRegex(ValueError, "review already reserved"):
            self.build()
        original = self.root / "review/original-response.json"
        original.write_bytes(original.read_bytes() + b" ")
        with self.assertRaisesRegex(ValueError, "review input changed"):
            tool.check(self.root)

    def test_changed_source_blocks_prepared_run(self):
        path = self.base / "thread-0.json"
        path.write_bytes(path.read_bytes() + b" ")
        with self.assertRaisesRegex(ValueError, "source hash changed"):
            self.build()
        self.assertFalse((self.root / "review").exists())

    def test_show_and_cli_check_read_durable_packet(self):
        self.build()
        first = tool.show(self.root, 0, 2).splitlines()
        rest = tool.show(self.root, 2, 100).splitlines()
        records = [tool.loads(line) for line in first + rest]
        self.assertEqual(len(records), 6)
        self.assertEqual(sum("metadata" in row for row in records), 2)
        self.assertEqual([row["label"]["id"] for row in records if "label" in row], list(tool.load(self.root / "registry.json")))
        with self.assertRaisesRegex(ValueError, "invalid review record range"):
            tool.show(self.root, 6, 40)
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            self.assertEqual(tool.main(["check", "--run-dir", str(self.root)]), 0)
        self.assertEqual(tool.loads(output.getvalue())["status"], "STRUCTURAL_VALID_ONLY")


if __name__ == "__main__":
    unittest.main()
