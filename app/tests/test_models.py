import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timezone
from app.shortener.models import URL, Base
from sqlalchemy.sql import func


class TestURLModel:

    @pytest.fixture(scope="function")
    def db_session(self):
        engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        session = Session()
        yield session
        session.close()

    def test_create_url(self, db_session):
        url = URL(original_url="https://www.example.com", short_url="abc123")
        db_session.add(url)
        db_session.commit()

        retrieved_url = db_session.query(URL).filter_by(short_url="abc123").first()

        assert retrieved_url is not None
        assert retrieved_url.original_url == "https://www.example.com"
        assert retrieved_url.short_url == "abc123"
        assert retrieved_url.clicks == 0
        assert retrieved_url.is_active == True


if __name__ == "__main__":
    pytest.main()
