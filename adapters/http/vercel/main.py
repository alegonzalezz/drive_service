from fastapi import FastAPI
import os
from adapters.http.vercel.sheets_controller import router
if os.getenv("VERCEL") is None:
    from dotenv import load_dotenv
    load_dotenv()

app = FastAPI()
app.include_router(router)

@app.get("/health")
def health():
    return {"status": "ok"}
