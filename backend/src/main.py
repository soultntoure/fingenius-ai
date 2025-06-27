from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from .api.v1 import api_router
from .core.config import settings
from .db.session import init_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup event
    print("Starting up FinGenius AI backend...")
    await init_db() # Initialize DB tables if they don't exist
    yield
    # Shutdown event
    print("Shutting down FinGenius AI backend...")

app = FastAPI(
    title="FinGenius AI API",
    version="0.1.0",
    description="API for the AI-powered personal finance assistant",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Adjust in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"message": "Welcome to FinGenius AI API! Visit /docs for OpenAPI documentation."}