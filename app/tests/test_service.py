import pytest
from unittest.mock import MagicMock
from app.shortener.models import URL
from app.shortener.service import UrlService
from app.shortener.schema import URLCreate


class TestUrlService:

    @pytest.fixture
    def db(self):
        return MagicMock()

    @pytest.fixture
    def url_service(self):
        return UrlService()

    def test_get_urls(self, db, url_service):
        db.query().offset().limit().all.return_value = ["url1", "url2"]

        urls = url_service.get_urls(db)

        assert urls == ["url1", "url2"]
        db.query().offset().limit().all.assert_called_once()

    def test_get_url(self, db, url_service):
        mock_url = URL(id=1, original_url="https://example.com", short_url="abcde")
        db.query().filter().first.return_value = mock_url

        url = url_service.get_url(db, url_id=1)

        assert url.id == 1
        assert url.original_url == "https://example.com"
        db.query().filter().first.assert_called_once()

    def test_get_redirect_url_found(self, db, url_service):
        mock_url = URL(id=1, original_url="https://example.com", short_url="abcde")
        db.query().filter().first.return_value = mock_url

        result = url_service.get_redirect_url(db, short_url="abcde")

        assert result ==  "https://example.com"
        db.query().filter().first.assert_called_once()


if __name__ == "__main__":
    pytest.main()
