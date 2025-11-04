import httpx
from fastapi import FastAPI
from router import router as auto_router

app = FastAPI()
app.include_router(auto_router)
