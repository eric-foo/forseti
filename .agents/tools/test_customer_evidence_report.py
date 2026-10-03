"""Offline mechanics only: native-shaped responses, never a model quality test."""
import contextlib
import copy
import io
import json
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

import customer_evidence_report as tool
from runners import codex_judgment_profile as profile
from runners.run_codex_provider_attempt import DIRECT_JUDGMENT_INSTRUCTION


def save(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(tool.encoded(value))


def corpus_fixture():
    rows = []
    for i in range(4):
        group = "conversation" if i < 2 else "retailer"
        body = ("Same exact body, different native people. " * 90 if i < 2 else
                (f"Distinct body {i}; skin improved but packaging leaked. " * 90))
        row = {"container_id": group, "evidence_id": f"native:{i}", "text": body,
               "source_ref": f"https://example.test/record/{i}", "public_identity_key": f"person:{i}",
               "independence_key": "person:0" if i == 3 else f"person:{i}",
               "source_family": "reddit_community" if i < 2 else "retailer_review",
               "source_role": "community_post" if i < 2 else "retailer_review",
               "publication_time": f"2026-09-{20+i}", "engagement": {"score": i},
               "parent_context_refs": ["parent"] if i < 2 else [],
               "product_context_refs": ["product"], "conversation_depth": i,
               "unknown_native_field": {"preserve": [None, False, 0, "Café 🧴\nnext line"]}}
        if i >= 2:
            row["retailer_native_metadata"] = {"Title": "Native review title", "Rating": 3,
                "ProductId": "p1", "OriginalProductName": "Literal product",
                "ContextDataValues": {"skinType": {"ValueLabel": "Dry", "Id": "skinType"}},
                "ClientResponses": [{"Response": "We replaced the damaged tube.", "Name": "Retailer"}],
                "retailer_reply": "Support reply in a different native shape."}
        rows.append(row)
    return {"original_rows": rows,
            "original_context": {"parent": {"text": rows[0]["text"], "author": "Parent speaker",
                                            "source_ref": "https://example.test/parent"},
                                 "product": {"text": "Product title and full description.", "native_extra": 7}},
            "original_containers": {key: {"container_id": key, "completeness": "partial",
                                          "source_visible_total": "unavailable"}
                                    for key in ("conversation", "retailer")}}


def native_fixture(root, rid, attempt, obj, outcome="PROCESS_COMPLETED"):
    """Fabricate local transport evidence, explicitly used only inside tests.

    The real receipt/profile/event validators run against it without mocks. This
    checks the consumer contract, not authenticity on an untrusted filesystem.
    """
    attempt = Path(attempt).resolve()
    attempt.mkdir(parents=True, exist_ok=True)
    selection = {"path": str((attempt.parents[0] / "fixture-codex.exe").resolve()),
                 "sha256": profile.NATIVE_SHA256, "version": profile.NATIVE_VERSION}
    if (root / rid / "launch.json").exists():
        selection = tool.load(root / rid / "launch.json")["selection"]
    source = {"slug": "gpt-6-sol", "context_window": 200000,
              "supported_reasoning_levels": [{"effort": "medium"}]}
    projected = {**source, **profile.TOOL_PROJECTION}
    save(attempt / "judgment-source-model.json", source)
    save(attempt / "judgment-model-catalog.json", {"models": [projected]})
    conf = (attempt / "fixture-home/config.toml").resolve()
    preventive = {"version": profile.PROFILE_VERSION, "native_sha256": profile.NATIVE_SHA256,
                  "disabled_features": list(profile.DISABLED_FEATURES), "config": list(profile.CONFIG),
                  "executor_environment": {"CODEX_EXEC_SERVER_URL": "none"},
                  "account": {"type": "chatgpt", "plan": "pro"},
                  "diagnostic_config": {"path": str(conf), "sha256": None},
                  "absent_configuration": [str(p) for p in profile.configuration_paths(tool.REPO, conf.parent)]}
    for name in ("judgment-source-model.json", "judgment-model-catalog.json"):
        preventive[name] = {"path": str(attempt / name), "sha256": tool.hash_file(attempt / name)}
    settings = [*profile.AUTH_CONFIG, *profile.CONFIG, 'model_reasoning_effort="medium"',
                "developer_instructions=" + json.dumps(DIRECT_JUDGMENT_INSTRUCTION),
                "model_catalog_json=" + json.dumps(str(attempt / "judgment-model-catalog.json"))]
    command = [selection["path"], "exec", "--ephemeral", "--ignore-user-config", "--ignore-rules",
               "--strict-config", "--json", "--sandbox", "read-only", "-C", str(tool.REPO),
               "--model", "gpt-6-sol", *[v for s in settings for v in ("--config", s)],
               *[v for f in profile.DISABLED_FEATURES for v in ("--disable", f)],
               "--output-schema", str(root / rid / "schema.json"),
               "--output-last-message", str(attempt / "response.json"), "-"]
    save(attempt / "response.json", obj)
    events = [{"type": "thread.started", "thread_id": "fixture-" + rid}, {"type": "turn.started"},
              {"type": "item.completed", "item": {"type": "agent_message", "text": tool.compact(obj)}},
              {"type": "turn.completed", "usage": {"input_tokens": 100, "output_tokens": 50}}]
    save(attempt / "events.jsonl", "\n".join(tool.compact(e) for e in events) + "\n")
    save(attempt / "stderr.log", "OFFLINE SYNTHETIC FIXTURE; NOT A NATIVE MODEL RUN\n")
    receipt = {"outcome": outcome, "exit_code": 0 if outcome == "PROCESS_COMPLETED" else 1,
               "command": command, "prompt_path": str(root / rid / "prompt.txt"),
               "prompt_sha256": tool.hash_file(root / rid / "prompt.txt"),
               "prompt_bytes": (root / rid / "prompt.txt").stat().st_size,
               "response_schema_sha256": tool.hash_file(root / rid / "schema.json"),
               "response_sha256": tool.hash_file(attempt / "response.json"),
               "response_bytes": (attempt / "response.json").stat().st_size,
               "events_sha256": tool.hash_file(attempt / "events.jsonl"),
               "stderr_sha256": tool.hash_file(attempt / "stderr.log"),
               "launch_metadata": {"direct_judgment": True, "codex_selection": selection,
                   "codex_version": profile.NATIVE_VERSION, "authentication_observed": "chatgpt",
                   "judgment_tool_profile": preventive},
               "usage": {"input_tokens": 100, "output_tokens": 50, "cached_input_tokens": 60},
               "usage_status": "OFFLINE_SYNTHETIC_FIXTURE", "wall_seconds": 0}
    save(attempt / "execution_receipt.json", receipt)
    return receipt


class CustomerEvidenceReport(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="forseti-report-mechanics-")
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name).resolve()
        self.root = self.base / "run"
        self.corpus = self.base / "corpus.json"
        self.question = self.base / "question.txt"
        save(self.corpus, corpus_fixture())
        save(self.question, "Which strengths and objections deserve investigation?")
        self.frozen_bytes = self.corpus.read_bytes()
        # Short test authority keeps packing tests small; real authority is
        # separately exercised by full-corpus offline preparation.
        self.rules = patch.object(tool, "rules", return_value="FIXTURE_AUTHORITY; preserve attribution and uncertainty.")
        self.rules.start()
        self.addCleanup(self.rules.stop)
        self.config = {**tool.DEFAULTS, "unit_input_tokens": 3100}
        self.prepare()
        self.registry = tool.validate_corpus(tool.load(self.corpus))

    def prepare(self, root=None, config=None):
        return tool.prepare(self.corpus, self.question, root or self.root, config or self.config,
                            citation_contract=None)

    def ids(self, root=None):
        return [e["id"] for e in tool.load((root or self.root) / "manifest.json")["requests"]]

    def response(self, rid, root=None):
        root = root or self.root
        request = tool.load(root / rid / "request.json")
        if rid == "synthesis":
            notes = tool.load(root / rid / "payload.json")["notes"]
            citations = [copy.deepcopy(c) for note in notes for c in note["citations"]]
            return {"report_markdown": "OFFLINE FIXTURE report. " + " ".join(c["source"] for c in citations),
                    "citations": citations}
        ref = request["refs"][0]
        return {"notes_markdown": f"OFFLINE FIXTURE {rid}: {ref} reports a bounded observation.",
                "citations": [{"source": ref, "pointer": "/record/text", "speaker": "customer",
                               "quote": self.registry[ref]["text"][:45], "role": "reported experience"}]}

    def fixture(self, rid, obj=None, root=None, outcome="PROCESS_COMPLETED"):
        root = root or self.root
        attempt = root / rid / "attempts/initial"
        native_fixture(root, rid, attempt, obj or self.response(rid, root), outcome)
        return attempt

    def accept_reads(self, root=None):
        root = root or self.root
        for rid in self.ids(root):
            tool.accept(root, rid, self.fixture(rid, root=root))

    def assert_reason(self, text, action):
        with self.assertRaisesRegex(ValueError, text):
            action()

    def test_public_prepare_and_exact_source_delivery_without_row_annotations(self):
        self.assertGreater(len(self.ids()), 1)
        all_refs = []
        for rid in self.ids():
            payload = tool.load(self.root / rid / "payload.json")
            prompt = (self.root / rid / "prompt.txt").read_text(encoding="utf-8")
            supplied = tool.loads(prompt.split("\nCOMPLETE INPUT JSON\n", 1)[1])
            self.assertEqual(payload, supplied)
            rows, contexts, containers = tool.reconstruct(supplied, self.registry, tool.load(self.corpus))
            for ref, row in rows.items():
                self.assertEqual(row, self.registry[ref])
                for key in row["parent_context_refs"] + row["product_context_refs"]:
                    self.assertEqual(contexts[key], tool.load(self.corpus)["original_context"][key])
                self.assertEqual(containers[row["container_id"]], tool.load(self.corpus)["original_containers"][row["container_id"]])
            all_refs += list(rows)
            self.assertIn("No per-row labels", prompt)
            self.assertNotIn("notes_markdown", tool.compact(payload))
        self.assertCountEqual(all_refs, self.registry)
        self.assertEqual(len(all_refs), len(set(all_refs)))
        first = tool.load(self.root / self.ids()[0] / "payload.json")
        a, b = self.registry["R0001"], self.registry["R0002"]
        self.assertEqual(a["text"], b["text"])
        self.assertNotEqual(a["public_identity_key"], b["public_identity_key"])
        self.assertEqual(list(first["texts"].values()).count(a["text"]), 1)
        self.assertEqual(self.corpus.read_bytes(), self.frozen_bytes)

    def test_versioned_shared_metadata_preserves_native_types_owners_and_pointers(self):
        corpus = tool.load(self.corpus)
        product = {"name": "A long native product description " * 12,
                   "version": 1.0, "promoted": True, "limits": [None, False, 0]}
        for row in corpus["original_rows"]:
            row["native_product"] = copy.deepcopy(product)
            row["accounting_reason"] = "Preserved original with its native actor and venue. " * 8
        corpus["original_rows"][0]["native_author"] = [tool.METADATA_REF, "M1"]
        corpus["original_rows"][1]["native_author"] = [tool.METADATA_LITERAL, False]
        corpus["original_rows"][2]["rare_metadata"] = {"unknown": [None, False, 1.0]}
        registry = tool.validate_corpus(corpus)
        payload = tool.source_payload(list(registry), registry, corpus,
                                      metadata_storage=tool.METADATA_STORAGE)
        self.assertEqual(payload["metadata_storage"], tool.METADATA_STORAGE)
        self.assertTrue(payload["metadata_values"])
        self.assertLess(tool.tokens(tool.compact(payload)), tool.tokens(tool.compact(
            tool.source_payload(list(registry), registry, corpus))))
        tool.verify_payload(payload, list(registry), registry, corpus)
        rows, _, _ = tool.reconstruct(payload, registry, corpus)
        self.assertEqual(rows["R0001"]["native_author"], [tool.METADATA_REF, "M1"])
        self.assertEqual(rows["R0002"]["native_author"], [tool.METADATA_LITERAL, False])
        self.assertNotEqual(rows["R0001"]["public_identity_key"], rows["R0002"]["public_identity_key"])
        self.assertEqual(rows["R0003"]["rare_metadata"], {"unknown": [None, False, 1.0]})
        shared_product = next(key for key, value in payload["metadata_values"].items()
                              if isinstance(value, dict) and "promoted" in value)
        changed = copy.deepcopy(payload)
        changed["metadata_values"][shared_product]["promoted"] = 1
        self.assert_reason("lossless native row reconstruction mismatch",
                           lambda: tool.verify_payload(changed, list(registry), registry, corpus))
        changed = copy.deepcopy(payload)
        del changed["metadata_values"][shared_product]
        self.assert_reason("shared metadata reference missing",
                           lambda: tool.verify_payload(changed, list(registry), registry, corpus))
        changed = copy.deepcopy(payload)
        changed["metadata_storage"] = "unknown_version"
        self.assert_reason("unsupported metadata storage",
                           lambda: tool.verify_payload(changed, list(registry), registry, corpus))
        run = self.base / "shared-run"
        save(self.corpus, corpus)
        tool.prepare(self.corpus, self.question, run,
                     {**self.config, "unit_input_tokens": 20000}, citation_contract=tool.CITATION_CONTRACT)
        manifest = tool.load(run / "manifest.json")
        self.assertEqual(manifest["metadata_storage"], tool.METADATA_STORAGE)
        rid = manifest["requests"][0]["id"]
        request = tool.verify_request(run, rid, manifest, corpus, registry,
            {"question": self.question.read_text(), "rules": tool.rules(),
             "products": tool.identity_map(registry), "citation_contract": tool.CITATION_CONTRACT})
        self.assertIn("metadata_values", (run / rid / "prompt.txt").read_text(encoding="utf-8"))
        response = {"paragraphs": [{"text": "Native product metadata remains context.", "evidence": [
            {"handle": "R0001/record/native_product/promoted", "owner": "", "quote": "true",
             "role": "native product flag"},
            {"handle": "R0001/record/native_product/name", "owner": "", "quote": "long native product",
             "role": "native product name"}]}]}
        citations = tool.validate_response(response, request, registry, corpus)["citations"]
        self.assertEqual([c["pointer"] for c in citations],
                         ["/record/native_product/promoted", "/record/native_product/name"])
        self.assertTrue(all(c["speaker"] == "context" for c in citations))
        # Refresh the superficial saved-file pins so the semantic reconstruction
        # guard, rather than a stale-file guard, rejects a missing dictionary value.
        saved = tool.load(run / rid / "payload.json")
        del saved["metadata_values"][next(key for key, value in saved["metadata_values"].items()
                                          if isinstance(value, dict) and "promoted" in value)]
        save(run / rid / "payload.json", saved)
        request["files"]["payload.json"] = tool.hash_file(run / rid / "payload.json")
        save(run / rid / "request.json", request)
        manifest["requests"][0]["request_sha256"] = tool.hash_file(run / rid / "request.json")
        save(run / "manifest.json", manifest)
        self.assert_reason("shared metadata reference missing", lambda: tool.check(run))

    def test_missing_parent_rejected_even_when_otherwise_valid(self):
        corpus = tool.load(self.corpus)
        del corpus["original_context"]["parent"]
        save(self.corpus, corpus)
        self.assert_reason("missing referenced parent/product context", lambda: self.prepare(self.base / "bad"))
        self.assertFalse((self.base / "bad").exists())

    def test_long_technical_references_share_context_without_dropping_unfamiliar_fields(self):
        corpus = tool.load(self.corpus)
        long = "technical/archive/component/" * 500
        for i, row in enumerate(corpus["original_rows"]):
            row["source_ref"] = long + f"source-{i}"
            row["source_artifact_id"] = long + f"artifact-{i}"
            row["product_context_refs"] = [f"product-{i}"]
            corpus["original_context"][f"product-{i}"] = {
                "source_ref": long + f"product-locator-{i}", "source_artifact_id": long,
                "text": "Literal product description; formula version unknown.",
                "unfamiliar_native_metadata": {"conditions": ["unknown", "winter"], "new_field": False}}
        registry = tool.validate_corpus(corpus)
        refs = list(registry)
        payload = tool.source_payload(refs, registry, corpus)
        rows, contexts, containers = tool.reconstruct(payload, registry, corpus)
        self.assertEqual(rows, registry)
        for key, value in contexts.items():
            self.assertEqual(value, corpus["original_context"][key])
        self.assertLess(tool.tokens(tool.compact(payload)), tool.tokens(tool.compact(corpus)) // 4)
        self.assertNotIn(long, tool.compact(payload))
        self.assertIn("unfamiliar_native_metadata", tool.compact(payload))
        self.assertNotEqual(rows["R0001"]["public_identity_key"], rows["R0002"]["public_identity_key"])
        projection = tool.context_projection(corpus)
        self.assertEqual(projection["context_aliases"]["product-0"], projection["context_aliases"]["product-1"])
        # A new, previously unknown material context field cannot be silently
        # ignored just because the existing rows/locators looked redundant.
        corpus["original_context"]["product-1"]["formula_version"] = "revised formula"
        projection = tool.context_projection(corpus)
        self.assertNotEqual(projection["context_aliases"]["product-0"], projection["context_aliases"]["product-1"])
        changed = tool.source_payload(refs, registry, corpus)
        self.assertIn("revised formula", tool.compact(changed))

    def test_native_context_edges_reject_wrong_alias_without_a_hash_failure(self):
        corpus = tool.load(self.corpus)
        payload = tool.source_payload(list(self.registry), self.registry, corpus)
        first = payload["tables"][0]
        column = first["columns"].index("parent_context_refs") + 1
        first["records"][0][column] = ["C2"]
        self.assert_reason("native context edge binding mismatch",
                           lambda: tool.verify_payload(payload, list(self.registry), self.registry, corpus))

    def test_valid_looking_payload_missing_context_fails_reconstruction_guard(self):
        rid = self.ids()[0]
        payload = tool.load(self.root / rid / "payload.json")
        parent_alias = tool.context_projection(tool.load(self.corpus))["context_aliases"]["parent"]
        del payload["context"][parent_alias]
        # Re-pin only packaging hashes to reach the independent semantic-unit
        # reconstruction boundary rather than winning on a stale-file check.
        save(self.root / rid / "payload.json", payload)
        request = tool.load(self.root / rid / "request.json")
        request["files"]["payload.json"] = tool.hash_file(self.root / rid / "payload.json")
        save(self.root / rid / "request.json", request)
        manifest = tool.load(self.root / "manifest.json")
        manifest["requests"][0]["request_sha256"] = tool.hash_file(self.root / rid / "request.json")
        save(self.root / "manifest.json", manifest)
        self.assert_reason("lossless parent/product context reconstruction mismatch", lambda: tool.check(self.root))

    def test_truncated_prompt_rejected_by_reconstruction_after_repin(self):
        rid = self.ids()[0]
        prompt = self.root / rid / "prompt.txt"
        prompt.write_bytes(prompt.read_bytes()[:-25])
        request = tool.load(self.root / rid / "request.json")
        request["files"]["prompt.txt"] = tool.hash_file(prompt)
        save(self.root / rid / "request.json", request)
        manifest = tool.load(self.root / "manifest.json")
        manifest["requests"][0]["request_sha256"] = tool.hash_file(self.root / rid / "request.json")
        save(self.root / "manifest.json", manifest)
        self.assert_reason("request reconstruction mismatch: prompt.txt", lambda: tool.check(self.root))

    def test_body_mutation_rejected_at_lossless_boundary(self):
        root, manifest, corpus, registry, frozen = tool.base(self.root)
        rid = self.ids()[0]
        payload = tool.load(root / rid / "payload.json")
        payload["texts"]["T1"] += " REMOVED_NEGATION"
        refs = tool.load(root / rid / "request.json")["refs"]
        self.assert_reason("lossless native row reconstruction mismatch",
                           lambda: tool.verify_payload(payload, refs, registry, corpus))

    def test_exact_assignments_reject_duplicate_already_admitted_row(self):
        corpus = tool.load(self.corpus)
        corpus["original_rows"][1]["evidence_id"] = corpus["original_rows"][0]["evidence_id"]
        self.assert_reason("duplicate or invalid native identity", lambda: tool.validate_corpus(corpus))

    def test_large_complete_unit_splits_with_parent_and_never_clips(self):
        corpus = tool.load(self.corpus)
        for i, row in enumerate(corpus["original_rows"]):
            row["container_id"] = "conversation"
            row["parent_context_refs"] = ["parent"]
            row["text"] = f"DISTINCT_{i} " + "original complete words " * 120
        save(self.corpus, corpus)
        root = self.base / "split"
        self.prepare(root)
        self.assertGreater(len(self.ids(root)), 1)
        self.assertTrue(tool.check(root)["all_source_context_reconstructed"])
        for rid in self.ids(root):
            self.assertIn(tool.context_projection(corpus)["context_aliases"]["parent"],
                          tool.load(root / rid / "payload.json")["context"])

    def test_capacity_overflow_rejects_before_directory_or_provider(self):
        with patch.object(tool.subprocess, "run") as launch:
            self.assert_reason("single complete native record/context exceeds capacity",
                lambda: self.prepare(self.base / "too-small", {**self.config, "effective_context_tokens": 100}))
            launch.assert_not_called()
        self.assertFalse((self.base / "too-small").exists())
        with patch.object(tool.subprocess, "run") as launch:
            self.assert_reason("single complete native record/context exceeds capacity",
                lambda: self.prepare(self.base / "byte-small", {**self.config, "max_input_bytes": 100}))
            launch.assert_not_called()

    def test_invented_prose_ref_rejected_after_valid_native_receipt(self):
        rid = self.ids()[0]
        obj = self.response(rid)
        obj["notes_markdown"] += " R9999"
        self.assert_reason("invented or unassigned prose reference", lambda: tool.accept(self.root, rid, self.fixture(rid, obj)))
        self.assertFalse((self.root / rid / "accepted.json").exists())

    def test_misbound_literal_and_speaker_reject_for_their_own_reason(self):
        rid = self.ids()[0]
        obj = self.response(rid)
        obj["citations"][0]["quote"] = "This exact quotation never occurs."
        attempt = self.fixture(rid, obj)
        self.assert_reason("citation quote does not match its exact source pointer",
                           lambda: tool.accept(self.root, rid, attempt))
        obj = self.response(rid)
        obj["citations"][0]["speaker"] = "retailer_reply"
        native_fixture(self.root, rid, attempt, obj)
        self.assert_reason("citation speaker misbound", lambda: tool.accept(self.root, rid, attempt))

    def test_extra_valid_context_citation_survives_native_acceptance_and_composition(self):
        root = self.base / "wide"
        self.prepare(root, {**self.config, "unit_input_tokens": 10000})
        rid = self.ids(root)[0]
        obj = self.response(rid, root)
        obj["citations"].append({"source": "R0002", "pointer": "/context/C2/text",
            "quote": "Product title", "speaker": "context", "role": "background product identity"})
        self.assertNotIn("R0002", obj["notes_markdown"])
        attempt = self.fixture(rid, obj, root)
        before = (attempt / "response.json").read_bytes()
        with patch.object(tool.subprocess, "run") as launch:
            tool.accept(root, rid, attempt)
            launch.assert_not_called()
        self.assertEqual((root / rid / "response.json").read_bytes(), before)
        self.assertEqual(tool.load(root / rid / "citations.json"), obj["citations"])
        tool.compose(root)
        self.assertIn("R0002", tool.load(root / "synthesis/payload.json")["reference_context"])

    def test_legacy_prompt_and_acceptance_retain_native_scalar_context(self):
        rid = self.ids()[0]
        request = tool.load(self.root / rid / "request.json")
        ref = request["refs"][0]
        score = self.registry[ref]["engagement"]["score"]
        citation = {"source": ref, "pointer": "/record/engagement/score",
                    "quote": tool.compact(score), "speaker": "context", "role": "native engagement"}
        prompt = (self.root / rid / "prompt.txt").read_text(encoding="utf-8")
        self.assertIn("for a number or boolean, quote is the entire JSON value", prompt)
        obj = self.response(rid)
        obj["citations"].append(citation)
        attempt = self.fixture(rid, obj)
        original = (attempt / "response.json").read_bytes()
        tool.accept(self.root, rid, attempt)
        self.assertEqual((self.root / rid / "response.json").read_bytes(), original)
        self.assertIn(citation, tool.load(self.root / rid / "citations.json"))

    def test_missing_prose_citation_and_invalid_extra_are_still_rejected(self):
        rid = self.ids()[0]
        obj = self.response(rid)
        obj["citations"] = []
        self.assert_reason("prose reference missing citation",
            lambda: tool.accept(self.root, rid, self.fixture(rid, obj)))
        obj = self.response(rid)
        obj["notes_markdown"] = "No commercial claim from this background context."
        obj["citations"][0]["quote"] = "Unstated product outcome."
        self.assert_reason("citation quote does not match its exact source pointer",
            lambda: tool.accept(self.root, rid, self.fixture(rid, obj)))
        self.assertFalse((self.root / rid / "accepted.json").exists())

    def test_unique_case_only_quote_restores_source_bytes_and_preserves_native(self):
        rid = next(rid for rid in self.ids() if "R0003" in tool.load(self.root / rid / "request.json")["refs"])
        obj = {"notes_markdown": "R0003 has product context.", "citations": [
            {"source": "R0003", "pointer": "/record/retailer_native_metadata/Title",
             "quote": "native review title", "speaker": "context", "role": "native title"}]}
        attempt = self.fixture(rid, obj)
        before = (attempt / "response.json").read_bytes()
        tool.accept(self.root, rid, attempt)
        self.assertEqual((self.root / rid / "response.json").read_bytes(), before)
        self.assertEqual(tool.load(self.root / rid / "citations.json")[0]["quote"], "Native review title")
        receipt = tool.load(self.root / rid / "accepted.json")
        self.assertEqual(receipt["quote_case_restorations"][0]["model_quote"], "native review title")
        self.assertEqual(receipt["quote_case_restorations"][0]["source_quote"], "Native review title")
        tool.check(self.root)
        receipt["quote_case_restorations"] = []
        save(self.root / rid / "accepted.json", receipt)
        self.assert_reason("saved quotation restoration record changed", lambda: tool.check(self.root))

    def test_case_recovery_rejects_ambiguous_spans_and_non_case_edits(self):
        rid = self.ids()[0]
        for quote in (self.response(rid)["citations"][0]["quote"].lower(),
                      self.response(rid)["citations"][0]["quote"] + "!"):
            with self.subTest(quote=quote):
                obj = self.response(rid)
                obj["citations"][0]["quote"] = quote
                self.assert_reason("citation quote does not match its exact source pointer",
                    lambda: tool.accept(self.root, rid, self.fixture(rid, obj)))
        self.assertFalse((self.root / rid / "accepted.json").exists())

    def home_correction_fixture(self):
        root = self.base / "home-corrected"
        self.prepare(root, {**self.config, "unit_input_tokens": 10000})
        rid = self.ids(root)[0]
        native = {"notes_markdown": "R0001 reports a leaking package.", "citations": [
            {"source": "R0001", "pointer": "/record/text", "speaker": "customer",
             "quote": "Distinct body 2; skin improved but packaging leaked.", "role": "packaging objection"}]}
        attempt = self.fixture(rid, native, root)
        obj = copy.deepcopy(native)
        obj["notes_markdown"] = "R0003 reports a leaking package."
        obj["citations"][0]["source"] = "R0003"
        correction = self.base / "home-correction.json"
        save(correction, {"native_response_sha256": tool.hash_file(attempt / "response.json"),
            "rationale": "The quoted words belong to native:2, not native:0; preserve the customer role.",
            "response": obj})
        return root, rid, attempt, correction

    def test_explicit_home_correction_preserves_native_and_reaches_synthesis(self):
        root, rid, attempt, correction = self.home_correction_fixture()
        before = {p.name: p.read_bytes() for p in attempt.iterdir() if p.is_file()}
        self.assert_reason("citation quote does not match its exact source pointer",
                           lambda: tool.accept(root, rid, attempt))
        with patch.object(tool.subprocess, "run") as launch, contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(tool.main(["accept", "--run-dir", str(root), "--request", rid,
                "--attempt-dir", str(attempt), "--home-correction", str(correction)]), 0)
            launch.assert_not_called()
        self.assertEqual(before, {p.name: p.read_bytes() for p in attempt.iterdir() if p.is_file()})
        self.assertEqual((root / rid / "response.json").read_bytes(), before["response.json"])
        self.assertIn("home-correction.json", tool.load(root / rid / "accepted.json")["files"])
        tool.compose(root)
        payload = tool.load(root / "synthesis/payload.json")
        self.assertEqual(payload["notes"][0]["notes_markdown"], "R0003 reports a leaking package.")
        self.assertEqual(payload["notes"][0]["citations"][0]["source"], "R0003")
        synthesis_attempt = self.fixture("synthesis", root=root)
        self.assert_reason("home correction is only for unaccepted reading notes",
                           lambda: tool.accept(root, "synthesis", synthesis_attempt, correction))
        tool.accept(root, "synthesis", synthesis_attempt)
        self.assertIn("native:2", (root / "synthesis/report-originals.md").read_text(encoding="utf-8"))
        self.assertEqual(tool.check(root)["status"], "REPORT_SAVED_UNREVIEWED")
        self.assertEqual(tool.check(root)["home_corrected_reads"], [rid])

    def test_home_correction_requires_original_pin_and_still_checks_sources(self):
        root, rid, attempt, correction = self.home_correction_fixture()
        valid = tool.load(correction)
        cases = [("native_response_sha256", "0" * 64, "home correction native response changed"),
                 ("rationale", "", "home correction requires source-backed rationale")]
        for key, value, error in cases:
            save(correction, {**valid, key: value})
            self.assert_reason(error, lambda: tool.accept(root, rid, attempt, correction))
        for field, value, error in [
            ("source", "R9999", "invented or unassigned citation reference"),
            ("quote", "Words that were never said.", "citation quote does not match its exact source pointer"),
            ("speaker", "retailer_reply", "citation speaker misbound")]:
            changed = copy.deepcopy(valid)
            changed["response"]["notes_markdown"] = "Candidate without a prose reference."
            changed["response"]["citations"][0][field] = value
            save(correction, changed)
            self.assert_reason(error, lambda: tool.accept(root, rid, attempt, correction))
        self.assertFalse((root / rid / "accepted.json").exists())

    def test_saved_home_correction_is_pinned_and_cannot_revise_accepted_notes(self):
        root, rid, attempt, correction = self.home_correction_fixture()
        tool.accept(root, rid, attempt, correction)
        original = tool.load(correction)
        changed = copy.deepcopy(original)
        changed["rationale"] += " Changed later."
        save(correction, changed)
        self.assert_reason("cannot change already accepted notes", lambda: tool.accept(root, rid, attempt, correction))
        saved = root / rid / "home-correction.json"
        save(saved, changed)
        self.assert_reason("accepted output changed: home-correction.json", lambda: tool.check(root))
        save(saved, original)
        tool.check(root)

    def test_retailer_reply_and_context_pointers_are_preserved(self):
        rid = next(rid for rid in self.ids() if "R0003" in tool.load(self.root / rid / "request.json")["refs"])
        obj = {"notes_markdown": "R0003 includes a retailer reply, not a customer outcome.", "citations": [
            {"source": "R0003", "pointer": "/record/retailer_native_metadata/ClientResponses/0/Response",
             "speaker": "retailer_reply", "quote": "We replaced the damaged tube.", "role": "service reply"},
            {"source": "R0003", "pointer": "/context/C2/text", "speaker": "context",
             "quote": "Product title", "role": "product identity only"}]}
        tool.accept(self.root, rid, self.fixture(rid, obj))
        self.assertEqual(tool.load(self.root / rid / "citations.json"), obj["citations"])

    def test_wrong_context_owner_and_nonliteral_metadata_do_not_borrow(self):
        rid = next(rid for rid in self.ids() if "R0003" in tool.load(self.root / rid / "request.json")["refs"])
        obj = {"notes_markdown": "R0003", "citations": [{"source": "R0003", "pointer": "/context/C1/text",
               "speaker": "context", "quote": self.registry["R0001"]["text"][:20], "role": "wrong parent"}]}
        self.assert_reason("citation source pointer missing", lambda: tool.accept(self.root, rid, self.fixture(rid, obj)))

    def test_all_notes_fresh_synthesis_and_deterministic_original_mapping(self):
        self.accept_reads()
        result = tool.compose(self.root)
        self.assertEqual(result["notes"], len(self.ids()))
        payload = tool.load(self.root / "synthesis/payload.json")
        self.assertEqual([n["unit"] for n in payload["notes"]], self.ids())
        prompt = (self.root / "synthesis/prompt.txt").read_text(encoding="utf-8")
        self.assertEqual(tool.loads(prompt.split("\nCOMPLETE INPUT JSON\n")[1]), payload)
        for rid in self.ids():
            self.assertIn(tool.load(self.root / rid / "response.json")["notes_markdown"], prompt)
        self.assertNotIn("original complete words", prompt)
        tool.accept(self.root, "synthesis", self.fixture("synthesis"))
        snapshot = tool.check(self.root)
        self.assertEqual(snapshot["status"], "REPORT_SAVED_UNREVIEWED")
        report = (self.root / "synthesis/report-originals.md").read_text(encoding="utf-8")
        for citation in tool.load(self.root / "synthesis/citations.json"):
            self.assertIn(citation["native_evidence_id"], report)
            self.assertEqual(citation["source_ref"], self.registry[citation["source"]]["source_ref"])
        before = {str(p): tool.hash_file(p) for p in self.root.rglob("*") if p.is_file()}
        with patch.object(tool.subprocess, "run") as launch:
            resumed = tool.run(self.root, 99)
            launch.assert_not_called()
        self.assertEqual(resumed["new_requests_launched"], 0)
        self.assertEqual(before, {str(p): tool.hash_file(p) for p in self.root.rglob("*") if p.is_file()})

    def test_compose_refuses_missing_note_before_call(self):
        rid = self.ids()[0]
        tool.accept(self.root, rid, self.fixture(rid))
        self.assert_reason("unfinished source units; cannot omit notes", lambda: tool.compose(self.root))
        self.assertFalse((self.root / "synthesis").exists())

    def test_final_reference_aliases_preserve_identity_role_and_product_distinctions(self):
        context = tool.reference_context(list(self.registry), self.registry)
        table = context["reference_context"]
        self.assertEqual(set(table), set(self.registry))
        self.assertNotEqual(table["R0001"][0], table["R0002"][0])  # same body, different actors
        self.assertEqual(table["R0001"][1], table["R0004"][1])  # repeated native origin
        self.assertNotEqual(table["R0001"][3], table["R0003"][3])
        self.assertIsNone(table["R0001"][4])
        self.assertEqual(table["R0003"][4], table["R0004"][4])
        for ref, values in table.items():
            row = self.registry[ref]
            self.assertEqual(context["family_and_roles"][values[3]], [row["source_family"], row["source_role"]])
            if values[4]:
                fields = tool.identity_map(self.registry)[values[4] - 1]["native_product_fields"]
                self.assertEqual(fields, {k: row["retailer_native_metadata"][k] for k in tool.PRODUCT_KEYS
                                          if k in row["retailer_native_metadata"]})
        for left in self.registry:
            for right in self.registry:
                for col, key in ((0, "public_identity_key"), (1, "independence_key")):
                    self.assertEqual(table[left][col] == table[right][col],
                                     self.registry[left][key] == self.registry[right][key])
        self.assertNotIn("https://example.test/record", tool.compact(context))

    def test_full_synthesis_capacity_counts_all_notes_and_output_reserve(self):
        root = self.base / "synthesis-overflow"
        config = {**self.config, "effective_context_tokens": 6000, "read_output_tokens": 1200,
                  "synthesis_output_tokens": 5000, "other_overhead_tokens": 50}
        self.prepare(root, config)
        for rid in self.ids(root):
            obj = self.response(rid, root)
            obj["notes_markdown"] += " All complete notes matter." * 140
            tool.accept(root, rid, self.fixture(rid, obj, root))
        with patch.object(tool.subprocess, "run") as launch:
            self.assert_reason("whole request capacity exceeded", lambda: tool.run(root, 1))
            launch.assert_not_called()
        self.assertFalse((root / "synthesis/request.json").exists())

    def test_changed_source_question_request_and_accepted_note_are_stale(self):
        save(self.question, "A different commissioned question")
        self.assert_reason("frozen source/input changed", lambda: tool.check(self.root))
        save(self.question, "Which strengths and objections deserve investigation?")
        rid = self.ids()[0]
        tool.accept(self.root, rid, self.fixture(rid))
        notes = self.root / rid / "notes.md"
        notes.write_bytes(notes.read_bytes() + b" changed accepted note")
        self.assert_reason("accepted output changed: notes.md", lambda: tool.run(self.root, 1))

    def test_synthesis_cannot_borrow_an_uncited_original_quote(self):
        self.accept_reads()
        tool.compose(self.root)
        obj = self.response("synthesis")
        c = obj["citations"][0]
        c["quote"] = self.registry[c["source"]]["text"][10:85]
        self.assert_reason("synthesis citation absent from accepted notes",
                           lambda: tool.accept(self.root, "synthesis", self.fixture("synthesis", obj)))

    def test_partial_output_acceptance_recovers_without_overwrite_or_reread(self):
        rid = self.ids()[0]
        attempt = self.fixture(rid)
        real_retain = tool.retain

        def interrupt(path, value):
            if Path(path).name == "accepted.json":
                raise KeyboardInterrupt("fixture interruption after outputs, before acceptance")
            real_retain(path, value)

        with patch.object(tool, "retain", side_effect=interrupt):
            with self.assertRaises(KeyboardInterrupt):
                tool.accept(self.root, rid, attempt)
        original = (self.root / rid / "response.json").read_bytes()
        self.assertFalse((self.root / rid / "accepted.json").exists())
        with patch.object(tool.subprocess, "run") as launch:
            tool.accept(self.root, rid, attempt)
            launch.assert_not_called()
        self.assertEqual((self.root / rid / "response.json").read_bytes(), original)
        self.assertEqual(tool.check(self.root)["saved_notes"], 1)

    def test_saved_partial_different_output_and_prepare_refuse_overwrite(self):
        rid = self.ids()[0]
        attempt = self.fixture(rid)
        save(self.root / rid / "notes.md", "preexisting authored notes")
        self.assert_reason("saved bytes changed; no overwrite", lambda: tool.accept(self.root, rid, attempt))
        self.assertEqual((self.root / rid / "notes.md").read_text(), "preexisting authored notes")
        self.assert_reason("run directory already exists; no overwrite", lambda: self.prepare())

    def test_failed_provider_and_unknown_attempt_never_relaunch(self):
        rid = self.ids()[0]
        self.fixture(rid, outcome="PROCESS_FAILED")
        with patch.object(tool.subprocess, "run") as launch:
            self.assert_reason("provider attempt failed", lambda: tool.run(self.root, 3))
            launch.assert_not_called()
        other = self.base / "unknown"
        self.prepare(other)
        rid = self.ids(other)[0]
        selection = {"path": "fixture", "sha256": "0" * 64, "version": "fixture"}
        manifest = tool.load(other / "manifest.json")
        save(other / rid / "launch.json", {"selection": selection,
             "binding": tool.attempt_binding(other, rid, manifest, selection)})
        with patch.object(tool.subprocess, "run") as launch:
            self.assert_reason("unknown/interrupted attempt", lambda: tool.run(other, 3))
            launch.assert_not_called()
        self.assertEqual(tool.check(other)["attempts_requiring_attention"][0]["state"], "UNKNOWN_OR_INTERRUPTED")

    def test_native_receipt_prompt_length_and_extra_turn_are_rejected(self):
        rid = self.ids()[0]
        attempt = self.fixture(rid)
        receipt = tool.load(attempt / "execution_receipt.json")
        receipt["prompt_bytes"] -= 10
        save(attempt / "execution_receipt.json", receipt)
        self.assert_reason("native prompt delivery length mismatch", lambda: tool.accept(self.root, rid, attempt))
        receipt = native_fixture(self.root, rid, attempt, self.response(rid))
        with (attempt / "events.jsonl").open("ab") as target:
            target.write(b'{"type":"turn.completed"}\n')
        receipt["events_sha256"] = tool.hash_file(attempt / "events.jsonl")
        save(attempt / "execution_receipt.json", receipt)
        self.assert_reason("exactly one completed native turn", lambda: tool.accept(self.root, rid, attempt))

    def test_provider_failure_event_is_not_zero_exit_success(self):
        rid = self.ids()[0]
        attempt = self.fixture(rid)
        with (attempt / "events.jsonl").open("ab") as target:
            target.write(b'{"type":"error","message":"fixture failure"}\n')
        receipt = tool.load(attempt / "execution_receipt.json")
        receipt["events_sha256"] = tool.hash_file(attempt / "events.jsonl")
        save(attempt / "execution_receipt.json", receipt)
        self.assert_reason("direct judgment provider failure: error", lambda: tool.accept(self.root, rid, attempt))

    def test_changed_delivered_report_and_changed_native_response_fail(self):
        self.accept_reads()
        tool.compose(self.root)
        tool.accept(self.root, "synthesis", self.fixture("synthesis"))
        output = self.root / "synthesis/report-originals.md"
        saved = output.read_bytes()
        output.write_bytes(saved + b" silently changed")
        self.assert_reason("accepted output changed: report-originals.md", lambda: tool.check(self.root))
        output.write_bytes(saved)
        native = self.root / "synthesis/attempts/initial/response.json"
        native.write_bytes(native.read_bytes() + b" ")
        self.assert_reason("provider response bytes changed", lambda: tool.check(self.root))

    def test_public_run_uses_maintained_runner_and_resumes_only_unfinished(self):
        calls = []
        selection = {"path": str(self.base / "fixture-codex.exe"), "sha256": profile.NATIVE_SHA256,
                     "version": profile.NATIVE_VERSION}

        def runner(command, **kwargs):
            self.assertIn("run_codex_provider_attempt.py", command[4])
            self.assertIn("--direct-judgment", command)
            self.assertIn("--require-chatgpt", command)
            prompt = Path(command[command.index("--prompt-file") + 1])
            rid = prompt.parent.name
            calls.append(rid)
            native_fixture(self.root, rid, self.root / rid / "attempts/initial", self.response(rid))
            return subprocess.CompletedProcess(command, 0)

        with patch.object(tool, "select_codex_executable", return_value=selection), \
                patch.object(tool.subprocess, "run", side_effect=runner), contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(tool.main(["run", "--run-dir", str(self.root), "--max-requests", "1"]), 0)
            self.assertEqual(calls, [self.ids()[0]])
            first_hash = tool.hash_file(self.root / calls[0] / "notes.md")
            self.assertEqual(tool.main(["run", "--run-dir", str(self.root), "--max-requests", "20"]), 0)
            self.assertEqual(calls, [*self.ids(), "synthesis"])
            self.assertEqual(first_hash, tool.hash_file(self.root / calls[0] / "notes.md"))
            self.assertEqual(tool.main(["run", "--run-dir", str(self.root), "--max-requests", "20"]), 0)
            self.assertEqual(calls, [*self.ids(), "synthesis"])
        for rid in self.ids():
            prompt = (self.root / rid / "prompt.txt").read_text(encoding="utf-8")
            for other in self.ids():
                self.assertNotIn(f"OFFLINE FIXTURE {other}", prompt)
        self.assertEqual(tool.check(self.root)["status"], "REPORT_SAVED_UNREVIEWED")

    def test_run_nonzero_exit_is_durable_and_cannot_turn_into_a_retry(self):
        selection = {"path": str(self.base / "fixture.exe"), "sha256": "0" * 64, "version": "fixture"}
        with patch.object(tool, "select_codex_executable", return_value=selection), \
                patch.object(tool.subprocess, "run", return_value=subprocess.CompletedProcess([], 17)) as launch:
            self.assert_reason("native provider runner failed", lambda: tool.run(self.root, 2))
            self.assertEqual(launch.call_count, 1)
            self.assert_reason("unknown/interrupted attempt", lambda: tool.run(self.root, 2))
            self.assertEqual(launch.call_count, 1)
        result = tool.load(self.root / self.ids()[0] / "launcher-result.json")
        self.assertEqual(result["exit_code"], 17)

    def test_question_and_source_bindings_are_frozen_and_noise_is_irrelevant(self):
        path = self.base / "pins.json"
        save(path, {"source_files": {str(self.corpus): tool.hash_file(self.corpus)}})
        root = self.base / "pinned"
        tool.prepare(self.corpus, self.question, root, self.config, path)
        baseline = tool.check(root)
        save(self.base / "untracked-noise.json", {"new_row": "should never join admitted corpus"})
        self.assertEqual(tool.check(root), baseline)
        save(path, {"source_files": {str(self.corpus): "0" * 64}})
        self.assert_reason("frozen source/input changed", lambda: tool.check(root))
        self.assert_reason("source binding hash changed",
                           lambda: tool.prepare(self.corpus, self.question, self.base / "bad-pins", self.config, path))


class ParagraphEvidence(unittest.TestCase):
    """Exercise the new contract at saved consumers, with native-shaped fixtures."""

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="forseti-paragraph-evidence-")
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name).resolve()
        self.root = self.base / "run"
        self.corpus = corpus_fixture()
        self.corpus["original_rows"][2]["public_identity_key"] = "unknown"
        self.corpus["original_rows"][2]["independence_key"] = "unavailable"
        save(self.base / "corpus.json", self.corpus)
        save(self.base / "question.txt", "What experience and objections recur?")
        with patch.object(tool, "rules", return_value="FIXTURE: preserve source identity and uncertainty"):
            tool.prepare(self.base / "corpus.json", self.base / "question.txt", self.root,
                         {**tool.DEFAULTS, "unit_input_tokens": 15000},
                         citation_contract=tool.LEGACY_PARAGRAPH_CONTRACT)
        self.rid = "read-001"
        self.registry = tool.validate_corpus(self.corpus)
        self.payload = tool.load(self.root / self.rid / "payload.json")

    def select(self, text, owner="", quote=None):
        handle = next(k for k, v in self.payload["texts"].items() if v == text)
        return {"handle": handle, "owner": owner, "quote": quote or text[:45], "role": "bounded support"}

    def body(self, ref="R0003"):
        return self.select(self.registry[ref]["text"])

    def response(self, evidence=None, text="One customer describes a conditional experience."):
        return {"paragraphs": [{"text": text, "evidence": evidence if evidence is not None else [self.body()]}]}

    def attempt(self, obj, rid="read-001"):
        target = self.root / rid / "attempts/initial"
        native_fixture(self.root, rid, target, obj)
        return target

    def reject(self, obj, reason):
        attempt = self.attempt(obj)
        with self.assertRaisesRegex(ValueError, reason):
            tool.accept(self.root, self.rid, attempt)
        self.assertFalse((self.root / self.rid / "accepted.json").exists())

    def test_unique_text_compiles_through_report_and_originals_without_parallel_citations(self):
        response = self.response()
        self.assertEqual(response["paragraphs"][0]["evidence"][0]["owner"], "")
        attempt = self.attempt(response)
        original = (attempt / "response.json").read_bytes()
        tool.accept(self.root, self.rid, attempt)
        citation = tool.load(self.root / self.rid / "citations.json")[0]
        self.assertEqual((citation["source"], citation["pointer"], citation["speaker"]),
                         ("R0003", "/record/text", "customer"))
        self.assertEqual((self.root / self.rid / "response.json").read_bytes(), original)
        tool.compose(self.root)
        synthesis = tool.load(self.root / "synthesis/payload.json")
        self.assertEqual(synthesis["evidence_catalog"]["E1"], citation)
        self.assertEqual(synthesis["notes"][0]["paragraphs"][0]["evidence"], ["E1"])
        self.assertNotIn("notes_markdown", synthesis["notes"][0])
        self.assertNotIn("citations", synthesis["notes"][0]["paragraphs"][0])
        report = {"paragraphs": [{"text": "One customer reports a conditional experience.", "evidence": ["E1"]}]}
        tool.accept(self.root, "synthesis", self.attempt(report, "synthesis"))
        saved = tool.load(self.root / "synthesis/citations.json")[0]
        self.assertEqual(saved["native_evidence_id"], "native:2")
        self.assertEqual(saved["public_identity_key"], "unknown")
        self.assertIn("native:2", (self.root / "synthesis/report-originals.md").read_text())
        self.assertEqual(tool.load(self.root / "synthesis/cited-originals.json")["R0003"]["record"],
                         self.registry["R0003"])
        self.assertEqual(tool.check(self.root)["status"], "REPORT_SAVED_UNREVIEWED")
        before = {str(p): tool.hash_file(p) for p in self.root.rglob("*") if p.is_file()}
        with patch.object(tool.subprocess, "run") as launch:
            self.assertEqual(tool.run(self.root, 5)["new_requests_launched"], 0)
            launch.assert_not_called()
        self.assertEqual(before, {str(p): tool.hash_file(p) for p in self.root.rglob("*") if p.is_file()})

    def test_native_scalars_reach_saved_report_as_context_without_customer_credit(self):
        selections = [
            {"handle": "R0003/record/engagement/score", "owner": "", "quote": "2", "role": "engagement"},
            {"handle": "R0003/record/retailer_native_metadata/Rating", "owner": "", "quote": "3", "role": "rating"},
            {"handle": "R0003/record/unknown_native_field/preserve/1", "owner": "", "quote": "false", "role": "native flag"},
            {"handle": "R0003/record/unknown_native_field/preserve/2", "owner": "", "quote": "0", "role": "native zero"},
        ]
        prompt = (self.root / self.rid / "prompt.txt").read_text(encoding="utf-8")
        self.assertIn("for a number or boolean, quote is the entire JSON value", prompt)
        attempt = self.attempt(self.response(selections, "Native metadata supplies context."))
        original = (attempt / "response.json").read_bytes()
        tool.accept(self.root, self.rid, attempt)
        self.assertEqual((self.root / self.rid / "response.json").read_bytes(), original)
        paragraph = tool.load(self.root / self.rid / "paragraphs.json")[0]
        self.assertEqual(paragraph["support"]["source_observation_count"], 0)
        self.assertEqual(paragraph["support"]["non_customer_sources"], ["R0003"])
        self.assertEqual([c["quote"] for c in paragraph["citations"]], ["2", "3", "false", "0"])
        tool.compose(self.root)
        catalog = tool.load(self.root / "synthesis/payload.json")["evidence_catalog"]
        self.assertEqual({c["quote"] for c in catalog.values()}, {"2", "3", "false", "0"})
        report = {"paragraphs": [{"text": "Native metadata remains contextual evidence.",
                                  "evidence": list(catalog)}]}
        tool.accept(self.root, "synthesis", self.attempt(report, "synthesis"))
        saved = tool.load(self.root / "synthesis/citations.json")
        self.assertEqual({c["quote"] for c in saved}, {"2", "3", "false", "0"})
        self.assertTrue(all(c["speaker"] == "context" and c["public_identity_key"] is None for c in saved))
        originals = tool.load(self.root / "synthesis/cited-originals.json")["R0003"]["record"]
        self.assertIs(type(originals["engagement"]["score"]), int)
        self.assertIs(type(originals["unknown_native_field"]["preserve"][1]), bool)
        self.assertIn("native:2", (self.root / "synthesis/report-originals.md").read_text(encoding="utf-8"))
        self.assertEqual(tool.check(self.root)["status"], "REPORT_SAVED_UNREVIEWED")
        self.assertEqual(tool.check(self.root)["status"], "REPORT_SAVED_UNREVIEWED")

    def test_scalar_quotes_require_exact_finite_native_value_and_pointer(self):
        corpus = copy.deepcopy(self.corpus)
        row = corpus["original_rows"][2]
        row["engagement"]["raw_positive_helpful_count"] = 14
        row["retailer_native_metadata"].update({"FloatRating": 1.0, "IsRecommended": True,
                                                 "IsSyndicated": False, "Absent": None,
                                                 "Array": [14], "Object": {"value": 14},
                                                 "Nonfinite": float("nan")})
        registry = tool.validate_corpus(corpus)
        request = tool.load(self.root / self.rid / "request.json")

        def selection(pointer, quote, ref="R0003", owner=""):
            return {"handle": ref + pointer, "owner": owner, "quote": quote, "role": "native context"}

        good = [selection("/record/engagement/raw_positive_helpful_count", "14"),
                selection("/record/retailer_native_metadata/FloatRating", "1.0"),
                selection("/record/retailer_native_metadata/IsRecommended", "true"),
                selection("/record/retailer_native_metadata/IsSyndicated", "false")]
        result = tool.validate_response(self.response(good), request, registry, corpus)
        self.assertEqual([(c["pointer"], c["quote"], c["speaker"]) for c in result["citations"]],
                         [(e["handle"].split("R0003", 1)[1], e["quote"], "context") for e in good])
        bad = [
            selection("/record/engagement/raw_positive_helpful_count", "4"),
            selection("/record/engagement/raw_positive_helpful_count", "014"),
            selection("/record/engagement/raw_positive_helpful_count", "14.0"),
            selection("/record/retailer_native_metadata/FloatRating", "1"),
            selection("/record/retailer_native_metadata/IsRecommended", "True"),
            selection("/record/retailer_native_metadata/IsRecommended", "yes"),
            selection("/record/retailer_native_metadata/IsRecommended", "1"),
            selection("/record/retailer_native_metadata/IsSyndicated", "0"),
            selection("/record/retailer_native_metadata/Rating", "14"),
            selection("/record/retailer_native_metadata/Rating", "14", "R0004"),
            selection("/record/retailer_native_metadata/Absent", "null"),
            selection("/record/retailer_native_metadata/Array", "[14]"),
            selection("/record/retailer_native_metadata/Object", '{"value":14}'),
            selection("/record/retailer_native_metadata/Nonfinite", "NaN"),
        ]
        for evidence in bad:
            with self.subTest(evidence=evidence), self.assertRaisesRegex(ValueError, "exact source pointer"):
                tool.validate_response(self.response([evidence]), request, registry, corpus)
        with self.assertRaisesRegex(ValueError, "citation source pointer missing"):
            tool.validate_response(self.response([selection("/record/absent", "14")]),
                                   request, registry, corpus)
        with self.assertRaisesRegex(ValueError, "unavailable evidence handle"):
            tool.validate_response(self.response([selection("/record/engagement/raw_positive_helpful_count",
                                                         "14", owner="R0003/record/text")]),
                                   request, registry, corpus)

    def test_wrong_quote_handle_unassigned_source_and_missing_field_fail_at_source_boundary(self):
        for evidence, reason in [
            ({**self.body(), "quote": "Someone else's literal words"}, "exact source pointer"),
            ({**self.body(), "handle": "T9999"}, "unavailable evidence handle"),
            ({**self.body(), "handle": "R9999/record/text"}, "unassigned evidence source"),
            ({**self.body(), "handle": "R0003/record/absent"}, "citation source pointer missing"),
            ({**self.body(), "handle": self.body("R0004")["handle"]}, "exact source pointer")]:
            with self.subTest(reason=reason):
                self.reject(self.response([evidence]), reason)

    def test_native_parent_links_resolve_one_original_without_equal_text_guessing(self):
        corpus = copy.deepcopy(self.corpus)
        corpus["original_rows"][1]["text"] = "A different reply body."
        corpus["original_context"]["parent"]["source_ref"] = corpus["original_rows"][0]["source_ref"]
        registry = tool.validate_corpus(corpus)
        payload = tool.source_payload(list(registry), registry, corpus, contract=tool.CITATION_CONTRACT)
        owners = tool.text_owners(payload)["T1"]
        self.assertEqual(tool.canonical_text_owner(owners, registry, corpus), "R0001/record/text")
        self.assertNotIn("T1", payload["ambiguous_text_owners"])
        request = {"stage": "read", "refs": list(registry), "citation_contract": tool.CITATION_CONTRACT,
                   "capacity": {"output_and_reasoning_reserve_tokens": 12000}}
        response = self.response([{"handle": "T1", "owner": "", "quote": registry["R0001"]["text"][:45],
                                   "role": "one original with linked parent appearances"}])
        result = tool.validate_response(response, request, registry, corpus)
        self.assertEqual(result["citations"][0]["source"], "R0001")
        self.assertEqual(result["paragraphs"][0]["support"]["source_observation_count"], 1)
        for locator in (None, "https://example.test/a-different-original"):
            changed = copy.deepcopy(corpus)
            changed["original_context"]["parent"]["source_ref"] = locator
            self.assertIsNone(tool.canonical_text_owner(owners, registry, changed))
            with self.assertRaisesRegex(ValueError, "ambiguous or invalid text owner"):
                tool.validate_response(response, request, registry, changed)
        # A context alias with equal material text can conceal different native
        # source locators. Every original edge must agree, not just the first.
        changed = copy.deepcopy(corpus)
        changed["original_context"]["other-parent"] = {
            **changed["original_context"]["parent"], "source_ref": "https://example.test/other"}
        changed["original_rows"][1]["parent_context_refs"].append("other-parent")
        changed_registry = tool.validate_corpus(changed)
        self.assertIsNone(tool.canonical_text_owner(owners, changed_registry, changed))
        # Even matching locators do not turn product context into testimony.
        changed = copy.deepcopy(corpus)
        changed["original_rows"][1]["product_context_refs"].append("parent")
        self.assertIsNone(tool.canonical_text_owner(owners, tool.validate_corpus(changed), changed))
        changed = copy.deepcopy(corpus)
        changed["original_rows"][1]["source_ref"] = changed["original_rows"][0]["source_ref"]
        self.assertIsNone(tool.canonical_text_owner(owners, tool.validate_corpus(changed), changed))
        explicit = copy.deepcopy(response)
        explicit["paragraphs"][0]["evidence"][0]["owner"] = "R0002/context/C1/text"
        result = tool.validate_response(explicit, request, registry, corpus)
        self.assertEqual(result["citations"][0]["speaker"], "context")

    def test_ambiguous_delivery_cannot_hide_distinct_people_or_repeated_original_use(self):
        self.assertNotIn(self.body()["handle"], self.payload["ambiguous_text_owners"])
        self.assertIn("T1", self.payload["ambiguous_text_owners"])
        changed = copy.deepcopy(self.payload)
        del changed["ambiguous_text_owners"]["T1"]
        with self.assertRaisesRegex(ValueError, "ambiguous text owner binding mismatch"):
            tool.verify_payload(changed, list(self.registry), self.registry, self.corpus)
        response = self.response()
        response["paragraphs"].append({"text": "The same original also supplies this qualification.",
                                        "evidence": [self.body()]})
        tool.accept(self.root, self.rid, self.attempt(response))
        bindings = tool.load(self.root / self.rid / "source-bindings.json")
        self.assertEqual(bindings["R0003"]["paragraphs"], [1, 2])
        self.assertEqual(bindings["R0003"]["native_evidence_id"], "native:2")
        self.assertEqual(len(tool.load(self.root / self.rid / "citations.json")), 1)

    def test_equal_text_requires_explicit_owner_and_keeps_people_and_context_distinct(self):
        shared = self.select(self.registry["R0001"]["text"])
        self.reject(self.response([shared]), "ambiguous or invalid text owner")
        self.reject(self.response([{**shared, "owner": "R0003/record/text"}]), "ambiguous or invalid text owner")
        evidence = [{**shared, "owner": "R0001/record/text"},
                    {**shared, "owner": "R0002/record/text"},
                    {**shared, "owner": "R0001/context/C1/text"}]
        tool.accept(self.root, self.rid, self.attempt(self.response(evidence)))
        p = tool.load(self.root / self.rid / "paragraphs.json")[0]
        self.assertEqual([c["speaker"] for c in p["citations"]], ["customer", "customer", "context"])
        self.assertEqual(p["support"]["source_observation_count"], 2)
        self.assertEqual(p["support"]["known_origin_identity_count"], 2)
        tool.verify_payload(self.payload, list(self.registry), self.registry, self.corpus)

    def test_context_retailer_and_metadata_speakers_are_compiled_not_model_fields(self):
        context = self.select(self.corpus["original_context"]["product"]["text"], "R0003/context/C2/text")
        reply = {"handle": "R0003/record/retailer_native_metadata/ClientResponses/0/Response",
                 "owner": "", "quote": "We replaced the damaged tube.", "role": "retailer service response"}
        title = {"handle": "R0003/record/retailer_native_metadata/Title", "owner": "",
                 "quote": "Native review title", "role": "metadata"}
        tool.accept(self.root, self.rid, self.attempt(self.response([self.body(), context, reply, title])))
        p = tool.load(self.root / self.rid / "paragraphs.json")[0]
        self.assertEqual([c["speaker"] for c in p["citations"]],
                         ["customer", "context", "retailer_reply", "context"])
        self.assertEqual(p["support"]["source_observation_count"], 1)
        tool.compose(self.root)
        catalog = tool.load(self.root / "synthesis/payload.json")["evidence_catalog"]
        report = {"paragraphs": [{"text": "Customer, retailer and context sources retain their own roles.",
                                  "evidence": list(catalog)}]}
        tool.accept(self.root, "synthesis", self.attempt(report, "synthesis"))
        for citation in tool.load(self.root / "synthesis/citations.json"):
            if citation["speaker"] != "customer":
                self.assertIsNone(citation["public_identity_key"])
                self.assertIsNone(citation["independence_key"])
        # Selecting a reply field with a customer quote fails literal matching.
        request = tool.load(self.root / self.rid / "request.json")
        with self.assertRaisesRegex(ValueError, "exact source pointer"):
            tool.validate_response(self.response([{**reply, "quote": self.body()["quote"]}]),
                                   request, self.registry, self.corpus)
        bad = self.response([{**self.body(), "speaker": "context"}])
        with self.assertRaises(tool.ValidationError):
            tool.validate_response(bad, request, self.registry, self.corpus)

    def test_repeated_original_and_same_actor_observations_cannot_inflate_counts(self):
        self.reject(self.response([self.body(), self.body()]), "repeated evidence selection")
        shared = self.select(self.registry["R0001"]["text"], "R0001/record/text")
        evidence = [shared, self.body("R0004"), self.body(),
                    {**self.body(), "quote": "skin improved but packaging leaked."}]
        tool.accept(self.root, self.rid, self.attempt(self.response(evidence)))
        p = tool.load(self.root / self.rid / "paragraphs.json")[0]
        self.assertEqual(p["support"]["source_observation_count"], 3)
        self.assertEqual(p["support"]["known_origin_identity_count"], 1)
        self.assertEqual(p["support"]["unknown_origin_observations"], ["R0003"])
        self.assertEqual(p["support"]["independence_status"], "NOT_ESTABLISHED_BY_IDENTITY_KEYS")

    def test_source_only_home_repair_cannot_keep_false_distinct_people_prose(self):
        native = self.response([self.body(), {**self.body("R0004"), "quote": self.body()["quote"]}],
                               "Two distinct customers describe the same experience.")
        attempt = self.attempt(native)
        corrected = self.response([self.body()], native["paragraphs"][0]["text"])
        correction = self.base / "correction.json"
        save(correction, {"native_response_sha256": tool.hash_file(attempt / "response.json"),
                          "rationale": "Both excerpts belong to one original with unknown identity.",
                          "response": corrected})
        with self.assertRaisesRegex(ValueError, "paragraph 1: linked-source correction requires"):
            tool.accept(self.root, self.rid, attempt, correction)
        corrected["paragraphs"][0]["text"] = "One original with unknown identity describes this experience."
        record = tool.load(correction)
        record["response"] = corrected
        save(correction, record)
        tool.accept(self.root, self.rid, attempt, correction)
        tool.compose(self.root)
        self.assertNotIn("Two distinct customers", tool.compact(tool.load(self.root / "synthesis/payload.json")))
        self.assertEqual(tool.check(self.root)["home_corrected_reads"], [self.rid])

    def test_source_only_home_repair_cannot_hide_behind_paragraph_shift(self):
        opening = {"text": "One customer reports a conditional experience.", "evidence": [self.body("R0004")]}
        false = {"text": "Two distinct customers describe the same experience.",
                 "evidence": [self.body(), {**self.body("R0004"), "quote": self.body()["quote"]}]}
        attempt = self.attempt({"paragraphs": [opening, false]})
        correction = self.base / "correction.json"
        # Dropping an earlier paragraph must not let unchanged prose keep new links.
        shifted = {"paragraphs": [{**false, "evidence": [self.body()]}]}
        save(correction, {"native_response_sha256": tool.hash_file(attempt / "response.json"),
                          "rationale": "The second excerpt is not from another customer.", "response": shifted})
        with self.assertRaisesRegex(ValueError, "paragraph 1: linked-source correction requires"):
            tool.accept(self.root, self.rid, attempt, correction)
        record = tool.load(correction)
        record["response"] = {"paragraphs": [opening]}
        save(correction, record)
        tool.accept(self.root, self.rid, attempt, correction)
        self.assertNotIn("Two distinct customers", (self.root / self.rid / "notes.md").read_text(encoding="utf-8"))

    def test_source_bindings_do_not_credit_record_actor_for_retailer_or_context_uses(self):
        reply = {"handle": "R0004/record/retailer_native_metadata/ClientResponses/0/Response",
                 "owner": "", "quote": "We replaced the damaged tube.", "role": "retailer service response"}
        response = {"paragraphs": [
            {"text": "Two customers report a conditional experience.",
             "evidence": [self.body("R0004"), self.body()]},
            {"text": "The retailer replied with a replacement.", "evidence": [reply]}]}
        tool.accept(self.root, self.rid, self.attempt(response))
        bindings = tool.load(self.root / self.rid / "source-bindings.json")
        self.assertEqual(bindings["R0004"]["paragraphs"], [1])
        self.assertEqual(bindings["R0004"]["non_customer_paragraphs"], [2])
        # All-customer records keep the earlier saved shape.
        self.assertNotIn("non_customer_paragraphs", bindings["R0003"])
        self.assertEqual(tool.load(self.root / self.rid / "paragraphs.json")[1]["support"]
                         ["source_observation_count"], 0)

    def test_interrupted_compilation_recovers_exactly_without_provider(self):
        attempt = self.attempt(self.response())
        retain = tool.retain
        def interrupt(path, value):
            if Path(path).name == "accepted.json":
                raise KeyboardInterrupt("save interrupted")
            retain(path, value)
        with patch.object(tool, "retain", side_effect=interrupt):
            with self.assertRaises(KeyboardInterrupt):
                tool.accept(self.root, self.rid, attempt)
        before = (self.root / self.rid / "paragraphs.json").read_bytes()
        with patch.object(tool.subprocess, "run") as launch:
            tool.accept(self.root, self.rid, attempt)
            tool.accept(self.root, self.rid, attempt)
            launch.assert_not_called()
        self.assertEqual((self.root / self.rid / "paragraphs.json").read_bytes(), before)
        self.assertEqual(tool.check(self.root)["saved_notes"], 1)

    def test_synthesis_cannot_invent_handle_or_parallel_citation(self):
        tool.accept(self.root, self.rid, self.attempt(self.response()))
        tool.compose(self.root)
        bad = {"paragraphs": [{"text": "Invented report support.", "evidence": ["E999"]}]}
        with self.assertRaisesRegex(ValueError, "absent from accepted notes"):
            tool.accept(self.root, "synthesis", self.attempt(bad, "synthesis"))
        bad["paragraphs"][0]["evidence"] = ["E1"]
        bad["citations"] = []
        with self.assertRaises(tool.ValidationError):
            tool.accept(self.root, "synthesis", self.attempt(bad, "synthesis"))


class MixedSourceEvidence(unittest.TestCase):
    def test_mixed_roles_survive_saved_read_synthesis_counts_and_resume(self):
        with tempfile.TemporaryDirectory(prefix="forseti-mixed-source-") as directory:
            base = Path(directory)
            corpus = corpus_fixture()
            roles = [("customer_review", None), ("community_post", "community_testimony"),
                     ("community_comment", "community_advice"), ("publisher", None),
                     ("guide_author", None), ("map_author", None), ("unrecognized_native_role", None),
                     ("analyst_observation", "unknown")]
            rows = []
            for i, (role, speaker) in enumerate(roles):
                row = copy.deepcopy(corpus["original_rows"][0])
                row.update(evidence_id=f"mixed:{i}", text=f"Source {i} states its bounded assertion.",
                           source_ref=f"https://example.test/mixed/{i}", source_role=role,
                           source_family="mixed_native_venue", container_id=f"own:{i}",
                           parent_context_refs=[], product_context_refs=[],
                           public_identity_key=f"author:{i}", independence_key=f"origin:{i}")
                if speaker:
                    row["body_speaker"] = speaker
                if i in (4, 5):
                    row["independence_key"] = "one-guide-and-map-origin"
                if i >= 6:
                    row["public_identity_key"] = "unknown"
                    row["independence_key"] = "unavailable"
                row["image_references"] = [f"source-pointer-{i}.png"]
                rows.append(row)
            rows[0]["retailer_reply"] = "Retailer reply stays retailer speech."
            corpus = {"original_rows": rows, "original_context": {},
                      "original_containers": {row["container_id"]: {"capture": "own source"} for row in rows}}
            save(base / "corpus.json", corpus)
            save(base / "question.txt", "What do these differently attributed sources establish?")
            root = base / "run"
            with patch.object(tool, "rules", return_value="FIXTURE source attribution authority"):
                tool.prepare(base / "corpus.json", base / "question.txt", root)
            manifest = tool.load(root / "manifest.json")
            self.assertEqual(manifest["citation_contract"], tool.CITATION_CONTRACT)
            payload = tool.load(root / "read-001/payload.json")
            expected = ["customer", "community_testimony", "community_advice", "publisher",
                        "guide_author", "map_author", "unknown", "unknown"]
            self.assertEqual(list(payload["body_speakers"].values()), expected)
            self.assertEqual(payload["context"], {})
            prompt = (root / "read-001/prompt.txt").read_text(encoding="utf-8")
            self.assertNotIn("Body testimony remains customer", prompt)
            self.assertIn("Image references are pointers only", prompt)
            registry = tool.validate_corpus(corpus)
            evidence = [{"handle": ref + "/record/text", "owner": "", "quote": row["text"],
                         "role": "background"} for ref, row in registry.items()]
            evidence.append({**evidence[0], "quote": "states its bounded assertion.", "role": "second excerpt"})
            response = {"paragraphs": [{"text": "Mixed attributed assertions.", "evidence": evidence},
                {"text": "A retailer reply.", "evidence": [{"handle": "R0001/record/retailer_reply",
                    "owner": "", "quote": rows[0]["retailer_reply"], "role": "retailer reply"}]},
                {"text": "A map image pointer is present.", "evidence": [{"handle": "R0006/record/image_references/0",
                    "owner": "", "quote": "source-pointer-5.png", "role": "pointer only"}]}]}
            attempt = root / "read-001/attempts/initial"
            native_fixture(root, "read-001", attempt, response)
            tool.accept(root, "read-001", attempt)
            compiled = tool.load(root / "read-001/paragraphs.json")
            self.assertEqual([c["speaker"] for c in compiled[0]["citations"][:8]], expected)
            self.assertEqual([c["source_role"] for c in compiled[0]["citations"][:8]], [r[0] for r in roles])
            support = compiled[0]["support"]
            self.assertEqual(support["source_observation_count"], 8)
            self.assertEqual(support["known_origin_identity_count"], 5)
            self.assertEqual(support["unknown_origin_observations"], ["R0007", "R0008"])
            self.assertEqual(support["customer_sources"], ["R0001"])
            self.assertEqual(support["customer_observation_count"], 1)
            self.assertEqual(support["customer_known_origin_identity_count"], 1)
            self.assertEqual(support["observations_by_speaker"]["unknown"], 2)
            self.assertEqual(compiled[1]["citations"][0]["speaker"], "retailer_reply")
            self.assertEqual(compiled[2]["citations"][0]["speaker"], "context")
            for paragraph in compiled[1:]:
                self.assertEqual(paragraph["support"]["source_observation_count"], 0)
            tool.compose(root)
            synthesis = tool.load(root / "synthesis/payload.json")
            self.assertEqual(synthesis["reference_columns"][-1], "body_speaker")
            self.assertEqual([v[-1] for v in synthesis["reference_context"].values()], expected)
            self.assertEqual(synthesis["reference_context"]["R0005"][1],
                             synthesis["reference_context"]["R0006"][1])
            self.assertIsNone(synthesis["reference_context"]["R0007"][1])
            final = {"paragraphs": [{"text": "Preserved mixed source evidence.",
                                     "evidence": list(synthesis["evidence_catalog"])}]}
            attempt = root / "synthesis/attempts/initial"
            native_fixture(root, "synthesis", attempt, final)
            tool.accept(root, "synthesis", attempt)
            citations = tool.load(root / "synthesis/citations.json")
            final_support = tool.load(root / "synthesis/paragraphs.json")[0]["support"]
            self.assertEqual(final_support["source_observation_count"], 8)
            self.assertEqual(final_support["known_origin_identity_count"], 5)
            self.assertEqual(final_support["customer_known_origin_identity_count"], 1)
            for citation in citations:
                row = registry[citation["source"]]
                self.assertEqual(citation["source_role"], row["source_role"])
                if citation["pointer"] == "/record/text":
                    self.assertEqual(citation["public_identity_key"], row["public_identity_key"])
                else:
                    self.assertIsNone(citation["public_identity_key"])
                    self.assertIsNone(citation["independence_key"])
            bindings = tool.load(root / "read-001/source-bindings.json")
            self.assertEqual(bindings["R0006"]["body_speaker"], "map_author")
            self.assertEqual(bindings["R0006"]["paragraphs"], [1])
            self.assertEqual(bindings["R0006"]["non_body_paragraphs"], [3])
            saved = {str(path.relative_to(root)): path.read_bytes() for path in root.rglob("*") if path.is_file()}
            tool.check(root)
            self.assertEqual(saved, {str(path.relative_to(root)): path.read_bytes()
                                     for path in root.rglob("*") if path.is_file()})

    def test_explicit_role_is_authoritative_and_unrecognized_roles_are_unknown(self):
        self.assertEqual(tool.body_speaker({"source_role": "retailer_review"}), "customer")
        self.assertEqual(tool.body_speaker({"source_role": "community_post"}), "community")
        self.assertEqual(tool.body_speaker({"source_role": "retailer_review", "body_speaker": "unknown"}), "unknown")
        for role in ("news_customer_review", "GUIDE", "", None, []):
            self.assertEqual(tool.body_speaker({"source_role": role}), "unknown")
        for invalid in ("custmer", None, []):
            with self.assertRaisesRegex(ValueError, "unsupported body_speaker"):
                tool.body_speaker({"source_role": "publisher", "body_speaker": invalid})

    def test_v2_frozen_bytes_match_pre_change_contract(self):
        # Hashes computed from 309f37ed before this change, not from v3 outputs.
        corpus = corpus_fixture()
        registry = tool.validate_corpus(corpus)
        contract = tool.LEGACY_PARAGRAPH_CONTRACT
        payload = tool.source_payload(list(registry), registry, corpus, contract=contract)
        request = {"stage": "read", "refs": list(registry), "citation_contract": contract,
                   "capacity": {"output_and_reasoning_reserve_tokens": 12000}}
        response = {"paragraphs": [{"text": "Historical frozen output.", "evidence": [
            {"handle": "R0001/record/text", "owner": "", "quote": registry["R0001"]["text"][:45], "role": "background"},
            {"handle": "R0003/record/retailer_native_metadata/ClientResponses/0/Response", "owner": "",
             "quote": "We replaced the damaged tube.", "role": "reply"}]}]}
        compiled = tool.validate_response(response, request, registry, corpus)
        values = {"payload": payload,
                  "read_prompt": tool.prompt_for("read", "Frozen question", "Frozen authority", [], payload, 12000, contract),
                  "compiled": compiled,
                  "synthesis_input": tool.synthesis_input([{"unit": "read-001", "accepted_sha256": "fixture", **compiled}], registry, contract),
                  "outputs": tool.derived_outputs(compiled, request, registry, corpus)}
        expected = {"payload": "0ebac30e9f789fe0a6513181458c104780b4162ae445ac86c33f517daf984bfe",
                    "read_prompt": "fd5dc3032b3cd1887625ad50528c882db9660c59c4bed0690bf508ec1b75e335",
                    "compiled": "1b5e2aedcca3946756003b74c52d5972bac89e3488c92e899750917bdf4a2765",
                    "synthesis_input": "fd12a45fdc7ffb440a7057cebedbf15cb92d589bb656b844351de363ea3f554e",
                    "outputs": "0d21342838166367ab5d559e45d8a4ca5a80157a0aaaf14b378e49101f22eed1"}
        self.assertEqual({key: tool.digest(tool.encoded(value)) for key, value in values.items()}, expected)


if __name__ == "__main__":
    unittest.main(verbosity=2)
