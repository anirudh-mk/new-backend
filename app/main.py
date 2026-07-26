from fastapi import FastAPI

from app.api.router import router as api_router

app = FastAPI(
    title="ERP Backend",
    version="1.0.0",
)

app.include_router(api_router)
