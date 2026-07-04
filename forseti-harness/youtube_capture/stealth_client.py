#!/usr/bin/env python3
"""Stealth HTTP client for YouTube capture (tracked code; captured data gitignored).

Makes the capture's network traffic resemble real Chrome (TLS + HTTP/2 + headers via curl_cffi
"impersonate") instead of stdlib Python, to reduce anti-bot detectability when capturing PUBLIC
data at volume. ANONYMOUS ONLY: a persistent Session carries anonymous cookies (CONSENT /
visitor_data) across requests; NO account login, NO po_token (no JS engine), NO proxy — proxy /
residential rotation is a SEPARATE higher rung (CloakBrowser), never part of this default transport.
Falls back to plain urllib (more detectable) if curl_cffi is unavailable.

Owner-authorized: public data only, SG-legal non-criminal use, Orca source-access posture
(anti-detect/fingerprint config accepted-risk). It accesses nothing gated; a costume, not a lockpick.
Public read-only. Tracked at forseti-harness/youtube_capture/.

Accepted residuals (Mini God Tier lens — named, not hidden):
  - po_token NOT minted -> escalate that request to a real browser (CloakBrowser) if a surface enforces it.
  - proxy / residential rotation is a SEPARATE higher rung (CloakBrowser), NOT in this transport; single IP here.
  - first request is cookieless until the Session seeds cookies (no explicit warmup).
  - TLS/JA3 verification RUN (owner-run 2026-06-21): curl_cffi(chrome) JA3=bc54cda9.../JA4=t13d1516h2_ over HTTP/2,
    distinct from stdlib urllib JA3=a1ebe7f9.../JA4=t13d1713h1_ HTTP/1.1 -> fingerprint confirmed Chrome-class and
    coherent (Mac-Chrome UA+TLS+h2 as a set). Residual: Chrome-class, NOT proven byte-identical to a live Chrome build (version drift).
  - cannot see YouTube's actual detector -> "not blocked != undetected".
"""
import urllib.request

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

try:
    from curl_cffi import requests as _cr
    _session = _cr.Session(impersonate="chrome")  # no proxy: proxy lives at the higher rung
    BACKEND = "curl_cffi:chrome"

    def http_get(url, data=None):
        if data is not None:
            r = _session.post(url, data=data, headers={"Content-Type": "application/json"}, timeout=30)
        else:
            r = _session.get(url, timeout=30)
        return r.status_code, r.url, r.content

except Exception:  # curl_cffi missing -> degraded (more detectable) stdlib fallback
    BACKEND = "urllib_fallback"

    def http_get(url, data=None):
        h = {"User-Agent": UA, "Accept-Language": "en-US,en;q=0.9"}
        if data is not None:
            h["Content-Type"] = "application/json"
        r = urllib.request.urlopen(urllib.request.Request(url, data=data, headers=h), timeout=30)
        return r.getcode(), r.geturl(), r.read()


# Code-enforced: never run the detectable fallback silently at volume.
STEALTH_OK = BACKEND.startswith("curl_cffi")
if not STEALTH_OK:
    import sys as _sys
    print("WARNING [stealth_client]: curl_cffi unavailable -> urllib fallback; on-the-wire fingerprint is "
          "DETECTABLE as Python. Install curl_cffi before capturing at volume.", file=_sys.stderr)
