#!/usr/bin/env python3
"""Legacy compatibility shim for the renamed Forseti Codex hook adapter."""
import pathlib
import runpy
import sys

TARGET = pathlib.Path(__file__).with_name("forseti_guard_codex_adapter.py")

if __name__ == "__main__":
    sys.argv[0] = str(TARGET)
    runpy.run_path(str(TARGET), run_name="__main__")
