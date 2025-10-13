"""
Тесты для основного приложения
"""
import pytest
from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)


def test_root_endpoint():
    """Тест корневого эндпоинта"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "version" in data
    assert data["message"] == "Welcome to Sirius Career Platform!"


def test_health_endpoint():
    """Тест эндпоинта проверки здоровья"""
    response = client.get("/health/")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "message" in data


def test_health_ready():
    """Тест эндпоинта готовности"""
    response = client.get("/health/ready")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ready"


def test_health_live():
    """Тест эндпоинта жизнеспособности"""
    response = client.get("/health/live")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "alive"


def test_docs_endpoint():
    """Тест доступности документации"""
    response = client.get("/docs")
    # В debug режиме должен быть доступен
    assert response.status_code in [200, 404]  # 404 если debug=False


@pytest.mark.parametrize("endpoint", [
    "/",
    "/health/",
    "/health/ready",
    "/health/live"
])
def test_endpoints_are_accessible(endpoint):
    """Параметризованный тест доступности эндпоинтов"""
    response = client.get(endpoint)
    assert response.status_code == 200
