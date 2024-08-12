from typing import Optional
from datetime import datetime
from urllib.parse import urlparse
from pydantic import BaseModel, ValidationError, validator



class URLBase(BaseModel):
    original_url: str


class URLInfo(URLBase):
    id: int
    short_url: str
    clicks: int
    is_active: bool
    created_date: datetime
    updated_date: Optional[datetime] = None

    class Config:
        orm_mode = True


class URLCreate(URLBase):

    @validator('original_url')
    def validate_url(cls, v):
        if not v.startswith(('http://', 'https://')):
            raise ValueError('URL must start with http:// or https://')
        parsed_url = urlparse(v)

        if not parsed_url.netloc:
            raise ValueError('URL must contain a valid domain')
        if len(v) < 20:
            raise ValueError('URL is too long (max 20 characters)')
        return v


class URLRedirect(URLBase):
    pass
