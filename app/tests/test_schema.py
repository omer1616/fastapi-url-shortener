import pytest
from datetime import datetime
from pydantic import ValidationError
from app.shortener.schema import URLBase, URLInfo, URLCreate, URLRedirect


class TestURLModels:

    def test_url_base(self):
        url = URLBase(original_url="https://www.example.com")
        assert url.original_url == "https://www.example.com"

    def test_url_info(self):
        url_info = URLInfo(
            id=1,
            original_url="https://www.example.com/bestway-sisme-havuz-ve-aksesuarlari-x-b105916-c103703",
            short_url="abc123",
            clicks=0,
            is_active=True,
            created_date=datetime.now()
        )
        assert url_info.original_url == "https://www.example.com/bestway-sisme-havuz-ve-aksesuarlari-x-b105916-c103703"
        assert url_info.short_url == "abc123"
        assert url_info.clicks == 0
        assert url_info.is_active == True
        assert isinstance(url_info.created_date, datetime)

    def test_url_create_valid(self):
        url = URLCreate(original_url="https://www.example.com/bestway-sisme-havuz-ve-aksesuarlari-x-b105916-c103703")
        assert url.original_url == "https://www.example.com/bestway-sisme-havuz-ve-aksesuarlari-x-b105916-c103703"

    def test_url_create_invalid_domain(self):
        with pytest.raises(ValidationError):
            URLCreate(original_url="https://")

    def test_url_create_too_short(self):
        with pytest.raises(ValidationError):
            URLCreate(original_url="https://a.b")


if __name__ == "__main__":
    pytest.main()
