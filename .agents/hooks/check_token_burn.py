#!/usr/bin/env python3
"""
check_token_burn.py -- advisory Stop hook: warn when a single turn's input
context (the quadratic-burn driver) crosses a threshold.

Why per-turn input, not cumulative spend: every turn re-sends the whole
transcript, so total cost grows ~O(turns^2). The leading indicator of "this is
about to get expensive" is how large each turn's prompt is, not what has already
been spent. This hook reads the most recent MAIN-thread assistant turn's prompt
size (new + cache-create + cache-read input tokens) and warns when it crosses a
rung.

Behavior:
  * NON-BLOCKING. Emits a `systemMessage` on stdout (exit 0); never blocks the
    Stop event. (exit 2 on Stop would force the agent to keep going -- avoided.)
  * Escalation-throttled: speaks only when the rung INCREASES, so it does not nag
    every turn. A dip (e.g. after /compact) resets the baseline, so a later climb
    re-warns.
  * Fails OPEN: any internal error -> exit 0, silent. A hook bug must never brick
    the session.

Thresholds (env overrides, in input tokens for one turn's prompt):
  FORSETI_TOKEN_BURN_WARN   default 200000   ("a little absurd")
      legacy fallback: ORCA_TOKEN_BURN_WARN
  FORSETI_TOKEN_BURN_ALARM  default 500000   ("absurd")
      legacy fallback: ORCA_TOKEN_BURN_ALARM
Set a threshold to 0 to disable that rung.

Harness contract + portability: see .agents/hooks/README.md. Advisory tooling --
not validation, readiness, or source-of-truth promotion.
"""
import hashlib
import json
import os
import sys
import tempfile

WARN_DEFAULT = 200_000
ALARM_DEFAULT = 500_000
FORSETI_TOKEN_BURN_WARN_ENV = "FORSETI_TOKEN_BURN_WARN"
FORSETI_TOKEN_BURN_ALARM_ENV = "FORSETI_TOKEN_BURN_ALARM"
LEGACY_ORCA_TOKEN_BURN_WARN_ENV = "ORCA_TOKEN_BURN_WARN"
LEGACY_ORCA_TOKEN_BURN_ALARM_ENV = "ORCA_TOKEN_BURN_ALARM"


def _turn_context_size(usage):
    """Full prompt size for one turn = new + cache-create + cache-read input."""
    if not isinstance(usage, dict):
        return 0

    def _i(key):
        try:
            return int(usage.get(key) or 0)
        except (TypeError, ValueError):
            return 0

    return (
        _i("input_tokens")
        + _i("cache_creation_input_tokens")
        + _i("cache_read_input_tokens")
    )


def _scan_transcript_line(raw):
    """Prompt size for one raw JSONL line, or None to skip it. None covers: blank
    lines, lines without a usage field, unparseable JSON, non-main-thread or
    non-assistant turns, and turns whose computed size is 0 (keep looking older)."""
    try:
        line = raw.decode("utf-8").strip()
    except UnicodeDecodeError:
        return None  # a corrupt older line is skipped, not fatal to the scan
    if not line or '"usage"' not in line:
        return None
    try:
        obj = json.loads(line)
    except ValueError:
        return None
    if obj.get("type") != "assistant" or obj.get("isSidechain"):
        return None  # only the main thread's own turns drive its context
    size = _turn_context_size((obj.get("message") or {}).get("usage"))
    return size if size > 0 else None


TAIL_BLOCK_SIZE = 65536


def _latest_context_size(transcript_path, block_size=TAIL_BLOCK_SIZE):
    """Prompt size of the most recent main-thread assistant turn; 0 if none.

    Reads the transcript backwards in fixed-size blocks and scans lines
    newest-first, stopping at the first match, so it never loads a multi-MB
    transcript in full. Splitting on the ``\\n`` byte (never part of a UTF-8
    multibyte sequence) makes block boundaries safe; a segment straddling a
    boundary is carried into the next, older block before being scanned. Fails
    open (returns 0) on any I/O error."""
    try:
        with open(transcript_path, "rb") as handle:
            handle.seek(0, os.SEEK_END)
            pos = handle.tell()
            carry = b""  # leading, possibly-incomplete segment of the last block
            while pos > 0:
                read_size = min(block_size, pos)
                pos -= read_size
                handle.seek(pos)
                parts = (handle.read(read_size) + carry).split(b"\n")
                if pos > 0:
                    carry = parts[0]  # first segment may span into the older block
                    complete = parts[1:]
                else:
                    complete = parts  # reached start: every segment is complete
                for raw in reversed(complete):
                    size = _scan_transcript_line(raw)
                    if size is not None:
                        return size
            return 0
    except OSError:
        return 0


def _rungs():
    """Ascending [(threshold, kind)]; 'warn' then 'alarm'. Disabled rungs dropped."""
    def _env(primary, legacy, default):
        raw = os.environ.get(primary)
        if raw is None:
            raw = os.environ.get(legacy)
        if raw is None:
            return default
        try:
            return int(raw)
        except (TypeError, ValueError):
            return default

    out = []
    warn = _env(
        FORSETI_TOKEN_BURN_WARN_ENV,
        LEGACY_ORCA_TOKEN_BURN_WARN_ENV,
        WARN_DEFAULT,
    )
    alarm = _env(
        FORSETI_TOKEN_BURN_ALARM_ENV,
        LEGACY_ORCA_TOKEN_BURN_ALARM_ENV,
        ALARM_DEFAULT,
    )
    if warn > 0:
        out.append((warn, "warn"))
    if alarm > 0:
        out.append((alarm, "alarm"))
    out.sort()
    return out


def _rung_index(size, rungs):
    idx = -1
    for i, (threshold, _kind) in enumerate(rungs):
        if size >= threshold:
            idx = i
    return idx


def _state_path(session_id):
    key = hashlib.sha1((session_id or "nosession").encode("utf-8")).hexdigest()[:16]
    return os.path.join(tempfile.gettempdir(), "forseti_token_burn_%s.json" % key)


def _read_last_rung(path):
    try:
        with open(path, "r", encoding="utf-8") as handle:
            return int(json.load(handle).get("last_rung", -1))
    except (OSError, ValueError, TypeError):
        return -1


def _write_last_rung(path, idx):
    try:
        with open(path, "w", encoding="utf-8") as handle:
            json.dump({"last_rung": idx}, handle)
    except OSError:
        pass


def _message(size, kind):
    figure = round(size / 1000.0)
    if kind == "alarm":
        return (
            "\U0001F6A8 Token burn: this turn's prompt was ~%dK input tokens. "
            "Context re-sends every turn (cost grows quadratically) -- strongly "
            "consider /compact, a fresh thread, or a cold handoff to a new lane."
            % figure
        )
    return (
        "⚠️ Token burn: this turn's prompt was ~%dK input tokens and is "
        "climbing quadratically. Consider /compact soon, or push heavy reads into "
        "subagents to keep the main thread lean." % figure
    )


def _run(event):
    """Core logic: return a warning string to surface, or None. Pure-ish (touches
    only the per-session state file)."""
    transcript = event.get("transcript_path")
    if not transcript:
        return None
    rungs = _rungs()
    if not rungs:
        return None
    size = _latest_context_size(transcript)
    idx = _rung_index(size, rungs)
    state = _state_path(event.get("session_id"))
    last = _read_last_rung(state)
    message = None
    if idx > last and idx >= 0:  # speak only when escalating into a higher rung
        message = _message(size, rungs[idx][1])
    if idx != last:  # record current rung so a dip-then-climb re-warns
        _write_last_rung(state, idx)
    return message


def main(argv):
    if "--selftest" in argv:
        return _selftest()
    try:
        raw = sys.stdin.read()
        event = json.loads(raw) if raw and raw.strip() else {}
    except (ValueError, OSError):
        return 0
    try:
        message = _run(event)
    except Exception:  # noqa: BLE001 -- fail open; never brick the session
        return 0
    if message:
        sys.stdout.write(json.dumps({"systemMessage": message}))
    return 0


def _tmp_transcript(size):
    handle = tempfile.NamedTemporaryFile(
        "w", suffix=".jsonl", delete=False, encoding="utf-8"
    )
    handle.write(
        json.dumps(
            {
                "type": "assistant",
                "isSidechain": False,
                "message": {
                    "usage": {
                        "input_tokens": size,
                        "cache_creation_input_tokens": 0,
                        "cache_read_input_tokens": 0,
                    }
                },
            }
        )
        + "\n"
    )
    handle.close()
    return handle.name


def _selftest():
    fails = []
    env_keys = (
        FORSETI_TOKEN_BURN_WARN_ENV,
        FORSETI_TOKEN_BURN_ALARM_ENV,
        LEGACY_ORCA_TOKEN_BURN_WARN_ENV,
        LEGACY_ORCA_TOKEN_BURN_ALARM_ENV,
    )
    saved = {k: os.environ.get(k) for k in env_keys}
    for key in env_keys:
        os.environ.pop(key, None)
    os.environ[FORSETI_TOKEN_BURN_WARN_ENV] = "200000"
    os.environ[FORSETI_TOKEN_BURN_ALARM_ENV] = "500000"
    try:
        # 1. context size sums the three input fields, ignores output
        usage = {
            "input_tokens": 5,
            "cache_creation_input_tokens": 1000,
            "cache_read_input_tokens": 199000,
            "output_tokens": 9999,
        }
        if _turn_context_size(usage) != 200005:
            fails.append("context_size sum wrong: %r" % _turn_context_size(usage))

        # 2. latest picks the main assistant turn, skips sidechain + user lines
        scratch = tempfile.NamedTemporaryFile(
            "w", suffix=".jsonl", delete=False, encoding="utf-8"
        )
        try:
            scratch.write(json.dumps({"type": "assistant", "isSidechain": True,
                "message": {"usage": {"input_tokens": 1, "cache_read_input_tokens": 999999}}}) + "\n")
            scratch.write(json.dumps({"type": "user", "message": {"content": "hi"}}) + "\n")
            scratch.write(json.dumps({"type": "assistant", "isSidechain": False,
                "message": {"usage": {"input_tokens": 250000,
                                      "cache_creation_input_tokens": 0,
                                      "cache_read_input_tokens": 0}}}) + "\n")
            scratch.close()
            got = _latest_context_size(scratch.name)
            if got != 250000:
                fails.append("latest_context_size picked wrong turn: %r" % got)
        finally:
            os.unlink(scratch.name)

        # 2b. tail read finds the newest usage line when it sits many blocks back
        #     from EOF (target line, then filler lines exceeding several blocks).
        big = tempfile.NamedTemporaryFile(
            "w", suffix=".jsonl", delete=False, encoding="utf-8"
        )
        block = 64
        try:
            big.write(json.dumps({"type": "assistant", "isSidechain": False,
                "message": {"usage": {"input_tokens": 314159,
                                      "cache_creation_input_tokens": 0,
                                      "cache_read_input_tokens": 0}}}) + "\n")
            # ~40 usage-free trailing lines >> block, so the match is many
            # blocks back from EOF and multi-block traversal is exercised.
            for i in range(40):
                big.write(json.dumps({"type": "user",
                    "message": {"content": "filler line %d padding padding" % i}}) + "\n")
            big.close()
            if os.path.getsize(big.name) <= block:
                fails.append("2b: transcript not larger than one block")
            got_big = _latest_context_size(big.name, block_size=block)
            if got_big != 314159:
                fails.append("2b: tail read missed cross-block usage line: %r" % got_big)
        finally:
            os.unlink(big.name)

        # 3. rung index boundaries
        rungs = [(200000, "warn"), (500000, "alarm")]
        for size, want in [(0, -1), (199999, -1), (200000, 0), (499999, 0),
                           (500000, 1), (9_000_000, 1)]:
            if _rung_index(size, rungs) != want:
                fails.append("rung_index(%d)=%d want %d"
                             % (size, _rung_index(size, rungs), want))

        # 4. primary Forseti env vars override legacy Orca fallbacks
        os.environ[FORSETI_TOKEN_BURN_WARN_ENV] = "111"
        os.environ[FORSETI_TOKEN_BURN_ALARM_ENV] = "333"
        os.environ[LEGACY_ORCA_TOKEN_BURN_WARN_ENV] = "222"
        os.environ[LEGACY_ORCA_TOKEN_BURN_ALARM_ENV] = "444"
        if _rungs() != [(111, "warn"), (333, "alarm")]:
            fails.append("primary Forseti env vars did not win: %r" % (_rungs(),))
        os.environ.pop(FORSETI_TOKEN_BURN_WARN_ENV, None)
        os.environ.pop(FORSETI_TOKEN_BURN_ALARM_ENV, None)
        if _rungs() != [(222, "warn"), (444, "alarm")]:
            fails.append("legacy Orca env fallback failed: %r" % (_rungs(),))
        os.environ[FORSETI_TOKEN_BURN_WARN_ENV] = "200000"
        os.environ[FORSETI_TOKEN_BURN_ALARM_ENV] = "500000"
        os.environ.pop(LEGACY_ORCA_TOKEN_BURN_WARN_ENV, None)
        os.environ.pop(LEGACY_ORCA_TOKEN_BURN_ALARM_ENV, None)

        # 5. escalation throttle: warn on entry, silent on plateau, alarm on climb,
        #    re-warn after a dip below
        state = _state_path("selftest-session")
        if os.path.exists(state):
            os.unlink(state)

        def step(size):
            event = {"transcript_path": _tmp_transcript(size), "session_id": "selftest-session"}
            try:
                return _run(event)
            finally:
                os.unlink(event["transcript_path"])

        try:
            if not step(210000):
                fails.append("step1: expected warn message on entry")
            if step(260000):
                fails.append("step2: expected silence on plateau")
            climb = step(600000)
            if not (climb and "\U0001F6A8" in climb):
                fails.append("step3: expected alarm message on climb")
            if step(50000):
                fails.append("step4: expected silence after dip")
            if not step(210000):
                fails.append("step5: expected re-warn after dip")
        finally:
            if os.path.exists(state):
                os.unlink(state)

        # 6. message carries the K figure and serializes to ascii JSON cleanly
        msg = _message(213000, "warn")
        if "213K" not in msg or not json.dumps({"systemMessage": msg}):
            fails.append("message format/serialize issue")
    finally:
        for key, val in saved.items():
            if val is None:
                os.environ.pop(key, None)
            else:
                os.environ[key] = val

    if fails:
        sys.stderr.write("SELFTEST FAIL:\n  " + "\n  ".join(fails) + "\n")
        return 1
    sys.stdout.write("SELFTEST PASS (warn=%d alarm=%d)\n" % (WARN_DEFAULT, ALARM_DEFAULT))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
