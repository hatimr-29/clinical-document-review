import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.database import engine, Base, SessionLocal
from app.models import ClinicalReport
from app.api.routes import health_router, analyze_router, reports_router
from app.utils.error_handlers import document_validation_exception_handler, generic_exception_handler
from app.utils.validation import DocumentValidationError
from app.seed_data import seed_synthetic_data

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("clinreview.main")

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Initializing ClinReview AI Backend Services...")
    # Create DB tables
    Base.metadata.create_all(bind=engine)
    # Seed synthetic demo data
    db = SessionLocal()
    try:
        seed_synthetic_data(db)
    finally:
        db.close()
    logger.info("ClinReview AI Startup Complete.")
    yield
    logger.info("ClinReview AI Shutting Down...")

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Intelligent Clinical Document Reviewer Backend API",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Exception Handlers
app.add_exception_handler(DocumentValidationError, document_validation_exception_handler)
app.add_exception_handler(Exception, generic_exception_handler)

# Include API Routers
app.include_router(health_router, prefix=settings.API_PREFIX, tags=["Health"])
app.include_router(analyze_router, prefix=settings.API_PREFIX, tags=["Analysis"])
app.include_router(reports_router, prefix=settings.API_PREFIX, tags=["Reports"])

@app.get("/")
def root():
    return {
        "message": "Welcome to ClinReview AI API Services",
        "documentation": "/docs",
        "health": f"{settings.API_PREFIX}/health"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
