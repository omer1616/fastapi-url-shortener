from urllib import response

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.shortener.database import Base, get_db
from unittest.mock import patch, MagicMock
from app.shortener.schema import URLInfo
from app.shortener.models import URL

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


@pytest.fixture(scope="module")
def test_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def db_session(test_db):
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture(scope="module")
def client():
    def override_get_db():
        try:
            db = TestingSessionLocal()
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as c:
        yield c


class TestRooter:

    @patch("app.shortener.service")
    def test_get_urls(self, mock_service):
        mock_service.get_urls.return_value = [
            URLInfo(
                id=1,
                original_url="http://example.com/example",
                short_url="exmpl",
                clicks=0,
                is_active=True,
                created_date="2024-08-11T00:00:00"
            )
        ]

        response = client.get("/urls/")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0

    @patch("app.shortener.service.get_settings")
    def test_create_url(self, mock_get_settings, db_session, client):
        mock_get_settings.return_value = MagicMock(BASE_URL="http://localhost")
        response = client.post("/urls/", json={"original_url": "http://example.com/example"})
        url = db_session.query(URL).filter(URL.original_url == "http://example.com/example").first()
        assert response.status_code == 201
        data = response.json()
        short_url = data["short_url"]
        assert short_url == f"http://localhost/{url.short_url}/"

    @patch("app.shortener.service.get_settings")
    def test_redirect_url(self, mock_get_settings, client):
        original_url = "https://github.com/zhanymkanov/fastapi-best-practices"
        mock_get_settings.return_value = MagicMock(BASE_URL="http://localhost")
        response = client.post("/urls/", json={"original_url": original_url})
        data = response.json()
        assert response.status_code == 201
        short_url = data["short_url"].split("/")[-2]
        response_get = client.get(f"/{short_url}/")
        assert response_get.url == original_url







if __name__ == "__main__":
    pytest.main()
