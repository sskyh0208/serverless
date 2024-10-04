from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import router
from .config import (
    ALLOW_ORIGINS,
    ALLOW_CREDENTIALS,
    ALLOW_METHODS,
    ALLOW_HEADERS,
)

app = FastAPI()

# CORS対策
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOW_ORIGINS,
    allow_credentials=ALLOW_CREDENTIALS,
    allow_methods=ALLOW_METHODS,
    allow_headers=ALLOW_HEADERS,
)
app.include_router(router)