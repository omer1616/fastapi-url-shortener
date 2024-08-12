from fastapi import FastAPI
from app.shortener import router
from app.shortener.database import engine, Base

app = FastAPI(title="URL Shortener")


Base.metadata.create_all(bind=engine)


app.include_router(router.router)