"""
Entry point para Vercel Serverless.
Expõe o app FastAPI via Mangum para /api/scan.
"""

from mangum import Mangum
from api.main import app

handler = Mangum(app)
