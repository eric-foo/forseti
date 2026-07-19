#!/bin/sh
set -eu

socat TCP-LISTEN:9222,fork,reuseaddr TCP:127.0.0.1:9223 &
relay_pid=$!

cleanup() {
  kill "$relay_pid" 2>/dev/null || true
}
trap cleanup EXIT INT TERM

xvfb-run -a --server-args="-screen 0 ${XVFB_SCREEN:-1280x800x24}" "$@"
