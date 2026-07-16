# Commission Signal Board Validator Tests Pointer

```yaml
retrieval_header_version: 1
artifact_role: Test pointer
scope: Spine-local pointer to executable validator tests and fixtures for standard CSB boards and the conditional company report.
use_when:
  - Finding the CSB validator test suite from the live CSB spine.
  - Checking why executable tests and fixtures remain in forseti-harness during the pilot.
authority_boundary: retrieval_only
open_next:
  - forseti-harness/tests/unit/test_commission_signal_board_output_validator.py
  - forseti-harness/tests/fixtures/commission_signal_board_outputs/
  - forseti/product/spines/commission_signal_board/harness/validator.md
stale_if:
  - The executable validator tests or fixtures move out of forseti-harness.
  - The Commission Signal Board output contract changes.
```

Executable test:

```text
forseti-harness/tests/unit/test_commission_signal_board_output_validator.py
```

Fixtures:

```text
forseti-harness/tests/fixtures/commission_signal_board_outputs/
```

Focused test command:

```powershell
cd forseti-harness
python -B -m pytest -q -p no:cacheprovider tests\unit\test_commission_signal_board_output_validator.py
```

This pointer does not move tests, move fixtures, create CI, or claim validator
truth beyond the mechanical checks owned by the executable test suite.
