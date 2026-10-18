
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import (
    init_db,
    get_dashboard_summary,
    get_recent_orders,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(
    title="MicroBiz Copilot API",
    description="Business intelligence API for MicroBiz Copilot.",
    version="0.2.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", tags=["health"])
def health_check():
    return {
        "status": "ok",
        "service": "microbiz-copilot-api",
    }


@app.get("/api/dashboard/summary", tags=["dashboard"])
def dashboard_summary():
    return get_dashboard_summary()


@app.get("/api/orders", tags=["orders"])
def list_orders():
    return {"orders": get_recent_orders()}
