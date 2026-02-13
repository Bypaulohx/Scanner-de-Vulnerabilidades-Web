
from typing import Dict, List, Tuple
from ..core import normalize_url

RECOMMENDED = {
    "Content-Security-Policy": "Define política para mitigar XSS.",
    "X-Content-Type-Options": "nosniff",
    "X-Frame-Options": "DENY ou SAMEORIGIN",
    "Referrer-Policy": "no-referrer ou strict-origin-when-cross-origin",
    "Permissions-Policy": "Restringe APIs sensíveis (camera, geolocation, etc).",
    "Strict-Transport-Security": "Força HTTPS (apenas em sites HTTPS).",
}

def scan_headers(session, url: str) -> Dict:
    url = normalize_url(url)
    r = session.get(url)
    headers = {k.title(): v for k, v in r.headers.items()}
    missing: List[Tuple[str, str]] = []
    notes: List[str] = []
    for h, hint in RECOMMENDED.items():
        if h not in headers:
            missing.append((h, hint))
    if r.url.startswith("https://") and "Strict-Transport-Security" not in headers:
        notes.append("Site é HTTPS mas não envia Strict-Transport-Security.")
    return {
        "target": r.url,
        "type": "headers",
        "ok": len(missing) == 0,
        "missing": [{"header": h, "hint": hint} for h, hint in missing],
        "headers_seen": headers,
        "notes": notes,
    }
