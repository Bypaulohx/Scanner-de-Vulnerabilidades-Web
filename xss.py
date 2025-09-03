
from urllib.parse import urlparse, parse_qsl
from typing import Dict, List
from ..core import get_with_params, is_reflected
from .common import XSS_PAYLOADS

def _candidate_params(url: str) -> List[str]:
    parsed = urlparse(url)
    params = [k for k, _ in parse_qsl(parsed.query, keep_blank_values=True)]
    # add common param names if none present
    common = ["q", "search", "s", "id", "page"]
    for c in common:
        if c not in params:
            params.append(c)
    return params

def scan_xss(session, url: str) -> Dict:
    findings = []
    params = _candidate_params(url)
    tested = 0
    for param in params:
        for payload in XSS_PAYLOADS:
            tested += 1
            new_url, resp = get_with_params(session, url, {param: payload})
            if resp is None:
                continue
            if is_reflected(resp.text, payload):
                findings.append({
                    "param": param,
                    "payload": payload,
                    "url": new_url,
                    "evidence": "payload refletido na resposta"
                })
                break  # stop after first hit for this parameter
    return {
        "type": "xss",
        "target": url,
        "tested": tested,
        "vulnerable": len(findings) > 0,
        "findings": findings,
    }
