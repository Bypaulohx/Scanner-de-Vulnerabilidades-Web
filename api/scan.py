"""
Entry point para Vercel Serverless.
Expõe o app FastAPI via Mangum para /api/scan.
"""

from mangum import Mangum
<<<<<<< HEAD
from main import app
=======
from api.main import app
>>>>>>> 200ce21 (Adicionar api/scan.py)

handler = Mangum(app)
