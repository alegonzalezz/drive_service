from fastapi import FastAPI
from adapters.http.vercel.sheets_controller import router

app = FastAPI()
app.include_router(router)
