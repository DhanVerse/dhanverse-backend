from fastapi import APIRouter

router = APIRouter(
    prefix="/health",
    tags=["Health"]
)

@router.get("/")
def health():
    return {
        "status": "healthy",
        "service": "DhanVerse Backend",
        "version": "0.0.1"
    }