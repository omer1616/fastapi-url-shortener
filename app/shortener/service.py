import random
import string
from typing import Optional
from app.shortener.models import URL
from sqlalchemy.orm import Session
from app.shortener.schema import URLCreate
from functools import lru_cache
from app.core.config import Settings


@lru_cache
def get_settings():
    return Settings()


class UrlService:

    def get_urls(self, db: Session, skip: int = 0, limit: int = 100):
        return db.query(URL).offset(skip).limit(limit).all()

    def get_url(self, db: Session, url_id: int):
        return db.query(URL).filter(URL.id == url_id).first()

    def create_url(self, db: Session, url: URLCreate):
        existing_url = self._get_existing_url(db, url.original_url)

        if existing_url:
            return f"{get_settings().BASE_URL}/{existing_url.short_url}/"

        db_url = URL(short_url=self._create_random_key(), original_url=url.original_url)
        db.add(db_url)
        db.commit()
        db.refresh(db_url)
        db_url = db_url.short_url
        return f"{get_settings().BASE_URL}/{db_url}/"

    def get_redirect_url(self, db: Session, short_url: str):
        url = db.query(URL).filter(URL.short_url == short_url).first()
        if url:
            original_url = url.original_url
            return {'original_url': original_url}
        return {'original_url': None}

    def _get_existing_url(self, db: Session, original_url: str) -> Optional[URL]:
        return db.query(URL).filter(URL.original_url == original_url).first()

    @staticmethod
    def _create_random_key(length: int = 5) -> str:
        chars = string.ascii_uppercase + string.digits
        return "".join(random.choice(chars) for _ in range(length))
