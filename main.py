import httpx
from fastapi import FastAPI
from router import router as auto_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
PROD_ORIGINS = [
    "https://www.akademia-profi.ru",
    "https://akademia-profi.ru",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=PROD_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
    allow_headers=["*"],
)

app.include_router(auto_router)
