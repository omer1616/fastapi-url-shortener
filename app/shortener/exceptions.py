from fastapi import HTTPException
from typing import  Union


class NotFoundException(HTTPException):
    def __init__(self, url_id: Union[str, int]):
        super().__init__(status_code=404, detail=f"URL with ID {url_id} not found.")
