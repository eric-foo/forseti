# ECR / JSG-01 End-to-End Test Run Report v0 (2026-06-12)

```yaml
retrieval_header_version: 1
artifact_role: Research artifact (machinery test-run record; product-learning cap)
scope: >
  First post-unfreeze end-to-end test run of the ECR spine + JSG-01 machinery on
  fresh input: live armory archive capture -> ECR derivers -> JSG-01-scoped
  binding -> SP-5 finalization act -> composition -> mechanical JSG-01 test
  gate-walk. Test walk only: not an authorized judgment run; clears no case.
use_when:
  - Checking whether the unfrozen JSG-01 machinery was exercised end-to-end on input it had never seen, and what it showed.
authority_boundary: retrieval_only
stale_if:
  - A real authorized run evaluates JSG-01 (its run record supersedes this as the latest exercise).
```

## What ran (owner-authorized in-thread, 2026-06-12: "test run of this ECR — set it up")

1. **Live armory capture (fresh input):** `runners/run_source_capture_archive_packet.py`
   on the neutral subject `https://en.wikipedia.org/wiki/RSS`, cutoff
   `20200101000000` → packet `01KTXB0CCDTJ6FD204ZSQ09XDS`
   (`reports/source_capture/ecr_test_run_rss_2020/`). The anti-leakage
   `select_snapshot <= cutoff` selector chose snapshot `20191230235534` —
   genuinely the last snapshot before the cutoff. One honest runner refusal was
   observed first (ISO cutoff rejected; 14-digit Wayback form required).
   Subject deliberately neutral: NOT Beauty Pie (its capture belongs to the
   outcome-clean Phase-4 lane).
2. **Unit + binding authored:** `E2` (`e002.yaml`, hash anchored to the packet's
   preserved body file) + `jsg01_binding_E2.yaml` in
   `cases/product_learning/jsg01_binding_assembly_proof_v0/`.
3. **Finalization act recorded** via the SP-5 producer: receipt
   `01KTXB2HYNH9VYR6RSQ2Y4CAKC` (proxy-recorded per the owner's test-run word;
   judge family = explicit placeholder, same convention as E1; post-write
   verified).
4. **Composition + JSG-01 test gate-walk** over BOTH units (E1 proof + E2 fresh).

## Observed (verbatim walk output, 2026-06-12)

Both units, all checks: SP-1 `resolved` CLEARS; SP-2 bound
`inspectable_verifiable` CLEARS; SP-3 bound `pre_cutoff` CLEARS; SP-6
`archive_only` CLEARS (decision-C grade); SP-5 finalization CLEARED (E1 receipt
`01KTW48P5PW4JJQG7NBG6G6DBP`; E2 receipt `01KTXB2HYNH9VYR6RSQ2Y4CAKC`); final
value `verified_pre_decision` allowed-cleared. JSG-01 TEST WALK: all
subpredicates clear — **evaluated at the placeholder judge family**.

## What this does and does not show

- **Shows:** the full spine works end-to-end on input it had never seen —
  capture discipline (anti-leakage selection observed live), pure derivation,
  key-bound composition, append-only finalization, and a determinate JSG-01
  evaluation. Machinery existence at product-learning grade.
- **Does NOT show:** any case clearance (test walk, not an authorized run — the
  placeholder judge family must be correction-receipted before any real run),
  any judgment quality, JSG-02..10 (not a judged case), or readiness. The
  evidence ladder + claim-defense doctrine cap every externally-shaped sentence.
