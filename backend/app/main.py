"""
Knowledge Intelligence Platform — FastAPI Main Application Entry Point
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database.init_db import initialize_database
from app.database.user_db import seed_admin_user
from app.core.auth import hash_password
from app.services.watcher import start_watcher
from app.core.middleware import RequestLoggingMiddleware
from app.core.logger import logger

# Import API Routers
from app.api.auth import router as auth_router
from app.api.documents import router as documents_router
from app.api.search import router as search_router
from app.api.chat import router as chat_router
from app.api.registry import router as registry_router
from app.api.admin import router as admin_router
from app.api.analytics import router as analytics_router

# Import Legacy/Test Routers
from app.api.scanner import router as scanner_router
from app.api.db_test import router as db_test_router
from app.api.index import router as index_router
from app.api.document_test import router as document_router
from app.api.metadata_test import router as metadata_router
from app.api.topic_test import router as topic_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic
    logger.info("Initializing Database Schema...")
    initialize_database()

    # Seed default admin user (admin / admin123)
    admin_created = seed_admin_user(hash_password("admin123"))
    if admin_created:
        logger.info("Default Admin User Created: username='admin', password='admin123'")

    logger.info("Starting Knowledge Base File Watcher...")
    start_watcher()

    logger.info("=" * 60)
    logger.info("Enterprise Knowledge Intelligence Assistant Online")
    logger.info("=" * 60)

    yield

    # Shutdown logic
    logger.info("Shutting down Knowledge Assistant API...")


app = FastAPI(
    title="Enterprise Knowledge Intelligence Platform API",
    version="2.0.0",
    description="Enterprise RAG System with Hybrid Search, Reranking, Conflict Resolution & Security",
    lifespan=lifespan
)

# Custom Middlewares
app.add_middleware(RequestLoggingMiddleware)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:5174",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {
        "title": "Enterprise Knowledge Intelligence Platform API",
        "status": "online",
        "version": "2.0.0"
    }


# Include Production Routers
app.include_router(auth_router)
app.include_router(documents_router)
app.include_router(search_router)
app.include_router(chat_router)
app.include_router(registry_router)
app.include_router(admin_router)
app.include_router(analytics_router)

# Include Legacy/Test Routers (for backwards compatibility)
app.include_router(scanner_router)
app.include_router(db_test_router)
app.include_router(index_router)
app.include_router(document_router)
app.include_router(metadata_router)
app.include_router(topic_router)