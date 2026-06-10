# Opus v0.14 Code-Ready Sanity Review — Orca Judgement Harness

```yaml
retrieval_header_version: 1
artifact_role: Imported Judgment Harness review prompt
scope: Imported Opus sanity-review prompt for the v0.14 code-ready docset.
use_when:
  - Working from the v0.14 Judgment Harness spec.
  - Checking this file's specific v0.14 harness contract.
authority_boundary: retrieval_only
```


You are reviewing whether v0.14 is now code-ready after the implementation-readiness blockers were patched.

Do not re-litigate strategy.
Do not expand architecture.
Do not add Phase 2 features.

Answer only:

```yaml
is_v0_14_ready_to_code: yes | no | mixed
remaining_blockers:
first_file_to_code:
first_week_build_sequence_corrections:
decision: start_coding | patch_then_code | pause
```

Focus on:
- numeric mapping table completeness
- scoring formulas
- judgement_class/laddder mapping
- memorization probe protocol
- Pydantic schema readiness
- whether any hidden subjective decision remains before mapping_table.py
