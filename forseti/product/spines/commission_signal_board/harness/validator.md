# Commission Signal Board Validator Pointer

```yaml
retrieval_header_version: 1
artifact_role: Harness pointer
scope: Spine-local pointer to the manual conditional validator for standard CSB boards and company competitive-intelligence reports.
use_when:
  - Finding how to run the Commission Signal Board validator from the live CSB spine.
  - Checking why validator code remains outside the spine during the pilot.
authority_boundary: retrieval_only
open_next:
  - .agents/hooks/check_commission_signal_board_output.py
  - forseti/product/spines/commission_signal_board/workflows/commission_signal_board_playbook_v0.md
  - forseti/product/spines/commission_signal_board/tests/validator_tests.md
stale_if:
  - The validator becomes CI, pre-commit, runtime, or product-owned infrastructure.
  - The validator script moves out of .agents/hooks.
```

Executable validator:

```text
.agents/hooks/check_commission_signal_board_output.py
```

Manual command:

```powershell
python -B .agents\hooks\check_commission_signal_board_output.py <board-output-file>
```

Selftest command:

```powershell
python -B .agents\hooks\check_commission_signal_board_output.py --selftest
```

The checker selects the standard or company contract from the output headings.
This pointer does not move validator code, install a hook, create CI, classify
demand, validate evidence truth, import Company Surface candidates, prove
readiness, or authorize runtime work.
