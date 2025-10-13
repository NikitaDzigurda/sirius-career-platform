"""
Роутер для проверки здоровья приложения
"""
from fastapi import APIRouter
from api.app.schemas.base import BaseResponse

router = APIRouter(prefix="/health", tags=["health"])


@router.get("/", response_model=BaseResponse)
async def health_check():
    """
    Проверка здоровья приложения
    """
    return BaseResponse(
        success=True,
        message="Sirius Career Platform is running!"
    )


@router.get("/ready")
async def readiness_check():
    """
    Проверка готовности приложения
    """
    # Здесь можно добавить проверки БД, внешних сервисов и т.д.
    return {"status": "ready"}


@router.get("/live")
async def liveness_check():
    """
    Проверка жизнеспособности приложения
    """
    return {"status": "alive"}
