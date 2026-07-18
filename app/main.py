from fastapi import FastAPI

from app.core.logger import logger
from app.core.settings import settings

# Database
from app.db.database import Base, engine

# Import models (Required for Alembic metadata discovery)
from app.models.user import User
from app.models.company import Company
from app.models.stock import Stock

# Import routers
from app.api.v1.health.router import router as health_router
from app.api.v1.auth.router import router as auth_router
from app.api.v1.companies.router import router as company_router
from app.api.v1.stocks import router as stock_router


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
)

# ==========================================================
# NOTE:
# Database schema is now managed by Alembic.
# DO NOT use Base.metadata.create_all() after baseline migration.
# ==========================================================

# Base.metadata.create_all(bind=engine)

logger.info("DhanVerse Backend Started Successfully")

# Register Routers
app.include_router(health_router)
app.include_router(auth_router)
app.include_router(company_router)
app.include_router(stock_router)

@app.get("/")
def root():
    return {
        "message": "Welcome to DhanVerse 🚀"
    }