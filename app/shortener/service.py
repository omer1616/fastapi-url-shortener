import random
import string
from app.shortener.models import URL
from sqlalchemy.orm import Session
from app.shortener.schema import URLCreate






class UrlService:

    def get_urls(self, db: Session, skip: int = 0, limit: int = 100):
        return db.query(URL).offset(skip).limit(limit).all()

    def get_url(self, db: Session, url_id: int):
        return db.query(URL).filter(URL.id == url_id).first()

    def create_url(self, url: URLCreate, db: Session):
        existing_url = self._retrieve_from_db_original_url(url.original_url, db)

        if existing_url:
            return f"{existing_url}"

        while True:
            short_url = self._create_random_key()
            existing_url = db.query(URL).filter(URL.short_url == short_url).first()
            if not existing_url:
                break

        db_url = URL(short_url=short_url, original_url=url.original_url)
        db.add(db_url)
        db.commit()
        db.refresh(db_url)
        short_url = db_url.short_url
        return f"{short_url}"

    def get_redirect_url(self, db: Session, short_url: str):
        url_record = self._retrieve_from_db_short_url(db, short_url)
        if url_record:
            return url_record
        return None

    def _retrieve_from_db_original_url(self, original_url: str, db: Session) -> str:
        url_record = db.query(URL).filter(URL.original_url == original_url).first()
        if url_record:
            return url_record.short_url
        else:
            return None

    def _retrieve_from_db_short_url(self, db: Session, short_url: str) -> str:
        url_record = db.query(URL).filter(URL.short_url == short_url).first()
        if url_record:
            return url_record.original_url
        else:
            return None

    @staticmethod
    def _create_random_key(length: int = 5) -> str:
        chars = string.ascii_uppercase + string.digits
        return "".join(random.choice(chars) for _ in range(length))
