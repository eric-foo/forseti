#!/bin/sh
set -eu

profile_dir="${CHROME_PROFILE_DIR:-/data/chrome-profile}"
install -d -o chrome -g chrome "$profile_dir"
chown chrome:chrome "$profile_dir"

set -- \
  google-chrome \
  --remote-debugging-port=9223 \
  --user-data-dir="$profile_dir" \
  --no-first-run \
  --no-default-browser-check \
  --window-size=1280,800

if [ "${CHROME_NO_SANDBOX:-0}" = "1" ]; then
  set -- "$@" --no-sandbox
fi

set -- "$@" about:blank
exec gosu chrome /usr/local/bin/run-xvfb-chrome.sh "$@"
