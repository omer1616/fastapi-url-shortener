from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session
from fastapi.responses import RedirectResponse
from app.shortener.database import get_db
from app.shortener.schema import URLInfo, URLCreate, URLRedirect
from app.shortener.service import UrlService
from typing import List
from app.core.config import get_settings
from app.shortener.exceptions import NotFoundException
from app.shortener.cache import get_or_create_short_url, get_original_url
router = APIRouter()
service = UrlService()


@router.get("/urls/", response_model=List[URLInfo])
def get_urls(db: Session = Depends(get_db)):
    urls = service.get_urls(db)

    return urls


@router.get("/urls/{url_id}/", response_model=URLInfo)
def get_url_detail(url_id=int, db: Session = Depends(get_db)):
    url_detail = service.get_url(db, url_id)
    if not url_detail:
        raise NotFoundException(url_id)

    return url_detail


@router.post("/urls/",  status_code=201)
def create_url(url: URLCreate, db: Session = Depends(get_db)):
    url = get_or_create_short_url(url, db,  service.create_url)
    BASE_URL = get_settings().BASE_URL
    return {"short_url": f"{BASE_URL}/{url}/"}


@router.get("/{short_url}/", response_model=URLRedirect)
def get_redirect_url(short_url: str, db: Session = Depends(get_db)):
    redirect_url = get_original_url(short_url, db, service.get_redirect_url)
    if not redirect_url:
        raise NotFoundException(short_url)

    return RedirectResponse(redirect_url)