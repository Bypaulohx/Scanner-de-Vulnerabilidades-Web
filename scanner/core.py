import re
import time
from urllib.parse import urlparse, urlencode, urlunparse, parse_qsl
import requests

DEFAULT_UA = "webvulnscanner/0.1 (+https://example.com)"

def build_session(timeout: float = 10.0, verify_tls: bool = True, user_agent: str = DEFAULT_UA) -> requests.Session:
    s = requests.Session()
    s.headers.update({"User-Agent": user_agent})
    s.verify = verify_tls
    s.timeout = timeout
    adapter = requests.adapters.HTTPAdapter(max_retries=2, pool_connections=10, pool_maxsize=10)
    s.mount("http://", adapter)
    s.mount("https://", adapter)
    return s

def normalize_url(url: str) -> str:
    parsed = urlparse(url)
    scheme = parsed.scheme or "http"
    netloc = parsed.netloc or parsed.path
    path = parsed.path if parsed.netloc else ""
    rebuilt = urlunparse((scheme, netloc, path or "/", "", "", ""))
    return rebuilt

def get_with_params(session: requests.Session, url: str, params: dict):
    parsed = urlparse(url)
    q = dict(parse_qsl(parsed.query, keep_blank_values=True))
    q.update(params)
    new_query = urlencode(q, doseq=True)
    new_url = urlunparse((parsed.scheme, parsed.netloc, parsed.path or "/", parsed.params, new_query, parsed.fragment))
    resp = session.get(new_url, timeout=getattr(session, "timeout", 10))
    return new_url, resp

DB_ERRORS = re.compile(
    r"(SQL syntax|mysql_fetch|ORA-|SQLite.Exception|psql:|UNEXPECTED ERROR|Warning:|Microsoft OLE DB Provider|ODBC|SQLSTATE)",
    re.IGNORECASE
)

def looks_like_db_error(text: str) -> bool:
    return bool(DB_ERRORS.search(text or ""))

def is_reflected(response_text: str, marker: str) -> bool:
    # basic reflection check allowing for minimal encoding
    if marker in response_text:
        return True
    # common HTML encoding
    enc = marker.replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;").replace("&", "&amp;")
    return enc in response_text
