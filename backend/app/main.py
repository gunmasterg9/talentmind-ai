import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.database import engine, Base
from app.api import router

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create tables on startup automatically
try:
    Base.metadata.create_all(bind=engine)
    logger.info("Database tables verified/created successfully")
except Exception as e:
    logger.error(f"Error creating database tables: {e}")

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Intelligent Recruiter Matching and Ranking Platform API",
    version="1.0.0"
)

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routes
app.include_router(router, prefix="/api")

@app.get("/")
def read_root():
    return {
        "status": "online",
        "service": settings.PROJECT_NAME,
        "docs": "/docs"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
