
from urllib.parse import urlparse, parse_qsl
from typing import Dict, List
from ..core import get_with_params, looks_like_db_error
from .common import SQLI_PAYLOADS

def _candidate_params(url: str) -> List[str]:
    parsed = urlparse(url)
    params = [k for k, _ in parse_qsl(parsed.query, keep_blank_values=True)]
    common = ["id", "user", "cat", "page"]
    for c in common:
        if c not in params:
            params.append(c)
    return params

def scan_sqli(session, url: str) -> Dict:
    findings = []
    params = _candidate_params(url)
    tested = 0
    for param in params:
        for payload in SQLI_PAYLOADS:
            tested += 1
            new_url, resp = get_with_params(session, url, {param: payload})
            if resp is None:
                continue
            if looks_like_db_error(resp.text):
                findings.append({
                    "param": param,
                    "payload": payload,
                    "url": new_url,
                    "evidence": "mensagem de erro de banco detectada"
                })
                break
    return {
        "type": "sqli",
        "target": url,
        "tested": tested,
        "vulnerable": len(findings) > 0,
        "findings": findings,
    }
