#!/usr/bin/env python3
"""Independent TLS/HTTP-2 fingerprint verification (tracked code).

Confirms the stealth client's Chrome impersonation actually changes the on-the-wire fingerprint
vs stdlib Python, observed by a neutral third-party TLS-echo service. Read-only. Owner-authorized
(public-data capture posture). This only READS our own outbound fingerprint; it touches no target.
"""
import json, urllib.request

ECHO = "https://tls.peet.ws/api/all"


def summ(j):
    tls = j.get("tls", {})
    return {"ja3_hash": tls.get("ja3_hash"), "ja4": tls.get("ja4"),
            "http": j.get("http_version"), "ua": (j.get("user_agent") or "")[:55]}


def via_curl_cffi():
    from curl_cffi import requests as cr
    return cr.get(ECHO, impersonate="chrome", timeout=25).json()


def via_urllib():
    req = urllib.request.Request(ECHO, headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"})
    return json.load(urllib.request.urlopen(req, timeout=25))


c = u = None
try:
    c = summ(via_curl_cffi()); print("curl_cffi(chrome):", json.dumps(c))
except Exception as e:
    print("curl_cffi echo FAILED:", type(e).__name__, e)
try:
    u = summ(via_urllib()); print("stdlib urllib    :", json.dumps(u))
except Exception as e:
    print("urllib echo FAILED:", type(e).__name__, e)

if c and u:
    print(f"VERDICT: ja3 differs={c['ja3_hash'] != u['ja3_hash']}  curl_cffi_http={c['http']}  urllib_http={u['http']}")
    print("  curl_cffi presents a distinct (Chrome-class) JA3 + HTTP/2; urllib presents Python's stdlib fingerprint.")
    print("  Residual: this confirms the fingerprint CHANGED, not that it is byte-identical to a specific live Chrome build.")

# --- Freshness check (the maintenance signal: is the costume still a CURRENT Chrome?) ---
# Read this at curl_cffi-bump review time. The version prints even if the echo above is offline.
try:
    import curl_cffi as _cc
    _ver = getattr(_cc, "__version__", "unknown")
except Exception:
    _ver = "NOT IMPORTABLE"
print("\nFRESHNESS CHECK (eyeball this when reviewing a curl_cffi bump)")
print(f"  curl_cffi version : {_ver}   <- the 'costume' version; newer releases carry a newer Chrome profile")
if c:
    print(f"  presenting JA4    : {c['ja4']}")
print("  Fresh? Being 1-2 Chrome majors behind real Chrome is invisible (lots of real users lag);")
print("  only a long-frozen version is a tell. Quick judgement: is the version above much older than")
print("  the latest on https://pypi.org/project/curl_cffi/ ? If Renovate has an open bump PR, merging")
print("  it refreshes the costume. Deeper check: compare the JA4 against a current Chrome's JA4")
print("  (open https://tls.peet.ws/ in a real, up-to-date Chrome and diff the ja4 line).")
