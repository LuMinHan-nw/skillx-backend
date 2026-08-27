from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.config import APP_NAME
from app.middleware.error_handler import setup_exception_handlers
from app.routes.api import router as api_router
from app.routes.public import router as public_router


app = FastAPI(title=APP_NAME)
setup_exception_handlers(app)

app.include_router(public_router)
app.include_router(api_router)


class FrontendFiles(StaticFiles):
    """Serves the pages, CSS and JavaScript with revalidation forced.

    Without a Cache-Control header a browser is free to guess how long a file
    stays fresh, and it guesses from the file's age - so an edited script could
    keep being served from cache for hours while the page looked unchanged.
    "no-cache" does not disable caching; it means ask first. The ETag still
    answers 304 when nothing changed, so the copy is only re-downloaded when
    the file has actually been edited.
    """

    def is_not_modified(self, response_headers, request_headers) -> bool:
        response_headers["Cache-Control"] = "no-cache"
        return super().is_not_modified(response_headers, request_headers)

    async def get_response(self, path: str, scope):
        response = await super().get_response(path, scope)
        response.headers["Cache-Control"] = "no-cache"
        return response


FRONTEND_DIR = Path(__file__).resolve().parent.parent / "frontend"
app.mount("/", FrontendFiles(directory=str(FRONTEND_DIR), html=True), name="frontend")
