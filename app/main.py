from fastapi import FastAPI

from app.core.logger import logger
from app.core.settings import settings

from app.db.database import Base, engine

# Import models
from app.models.user import User
from app.models.company import Company

# Import routers
from app.api.v1.health.router import router as health_router
from app.api.v1.auth.router import router as auth_router
from app.api.v1.companies.router import router as company_router

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
)

Base.metadata.create_all(bind=engine)

logger.info("DhanVerse Backend Started Successfully")

app.include_router(health_router)
app.include_router(auth_router)
app.include_router(company_router)


@app.get("/")
def root():
    return {
        "message": "Welcome to DhanVerse 🚀"
    }