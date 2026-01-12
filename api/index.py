import os

# SOLO cargar dotenv en local
if os.getenv("VERCEL") is None:
    from dotenv import load_dotenv
    load_dotenv()

from adapters.http.vercel.main import app
