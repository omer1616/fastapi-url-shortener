import redis
from sqlalchemy.orm import Session

r = redis.Redis(host='localhost', port=6379, db=0)
# Clear the current database's cache
r.flushdb()

# OR to clear all databases' caches
r.flushall()


def get_or_create_short_url(original_url, db: Session, create_url):
    short_url = r.get(str(original_url))
    if short_url:
        return short_url.decode('utf-8')
    else:
        short_url = create_url(original_url, db)
        r.set(str(original_url), str(short_url))
        return short_url


def get_original_url(short_url, db: Session, get_redirect_url):
    original_url = r.get(short_url)
    if original_url:
        return original_url.decode('utf-8')
    else:
        original_url = get_redirect_url(db, short_url)
        r.set(short_url, str(original_url))
        return original_url
