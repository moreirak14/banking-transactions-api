import logging

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from config import settings
from src.routers.v1 import router as v1_router

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_app() -> FastAPI:
    app = FastAPI(
        title=settings.TITLE,
        version=settings.VERSION,
        description=settings.DESCRIPTION,
    )

    app.add_middleware(
        middleware_class=CORSMiddleware,  # noqa https://github.com/tiangolo/fastapi/discussions/10968
        allow_origins=settings.ALLOWED_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(router=v1_router)

    @app.get("/favicon.ico")
    def root():
        return {"message": "banking-transactions-api is up and running"}

    return app


if __name__ == "__main__":
    import uvicorn

    # https://inboard.bws.bio/logging
    log_config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "standard": {
                "class": "logging.Formatter",
                "format": "%(asctime)s [%(process)d] [%(levelname)s] %(message)s",  # noqa
                "datefmt": "%Y-%m-%d %H:%M:%S",
            }
        },
        "handlers": {
            "default": {
                "class": "logging.StreamHandler",
                "formatter": "standard",
                "level": settings.LOG_LEVEL.upper(),
            },
        },
        "loggers": {
            "": {
                "handlers": ["default"],
                "level": settings.LOG_LEVEL.upper(),
                "propagate": False,
            },
        },
    }
    uvicorn.run(
        app="main:get_app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.RELOAD,
        log_level=settings.LOG_LEVEL.lower(),
        log_config=log_config,
        factory=True,
    )
