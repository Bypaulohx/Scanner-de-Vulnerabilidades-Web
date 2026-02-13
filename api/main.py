"""
API REST para o WebVulnScanner.
Expõe os endpoints do scanner para consumo pelo frontend.
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from scanner.core import build_session, normalize_url
from scanner.checks import scan_xss, scan_sqli, scan_headers


# --- Schemas ---

class ScanRequest(BaseModel):
    url: str
    xss: bool = True
    sqli: bool = True
    headers: bool = True
    timeout: float = 10.0
    insecure: bool = False


class ScanResponse(BaseModel):
    success: bool = True
    target: str
    results: list


# --- App ---

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


app = FastAPI(
    title="WebVulnScanner API",
    description="API para scanner de vulnerabilidades web (XSS, SQLi, Headers)",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite frontend local e Vercel
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    """Health check."""
    return {"status": "ok", "message": "WebVulnScanner API"}


@app.post("/api/scan", response_model=ScanResponse)
def run_scan(req: ScanRequest):
    """
    Executa varredura de vulnerabilidades na URL fornecida.
    """
    try:
        url = normalize_url(req.url)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"URL inválida: {e}")

    session = build_session(
        timeout=req.timeout,
        verify_tls=not req.insecure,
    )

    results = []

    if req.headers:
        results.append(scan_headers(session, url))

    if req.xss:
        results.append(scan_xss(session, url))

    if req.sqli:
        results.append(scan_sqli(session, url))

    return ScanResponse(
        target=url,
        results=results,
    )
