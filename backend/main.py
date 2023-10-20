from apis.base import api_router
from apps.base import app_router
from core.config import settings
from db.base import Base
from db.session import engine
from fastapi import FastAPI


def inlude_router(app):
    app.include_router(api_router)
    app.include_router(app_router)


def create_tables():
    Base.metadata.create_all(bind=engine)


def start_application():
    app = FastAPI(title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION)
    create_tables()
    inlude_router(app)
    return app


app = start_application()


# @app.get("/")
# def home():
#     return {"msg": "Hello FastAPI🚀"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
