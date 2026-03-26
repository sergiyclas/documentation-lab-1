"""Main FastAPI application"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config import API_TITLE, API_VERSION, API_DESCRIPTION
from src.dal import init_db
from src.pl import router
from src.common.logger import get_logger

logger = get_logger(__name__)

# Initialize database
init_db()

# Create FastAPI app
app = FastAPI(title=API_TITLE, version=API_VERSION, description=API_DESCRIPTION)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(router)


@app.on_event("startup")
async def startup_event():
    """Initialize database on startup"""
    logger.info("Application starting up...")
    init_db()
    logger.info("Database initialized")


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    logger.info("Application shutting down...")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
