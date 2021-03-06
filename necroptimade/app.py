"""The nectroptimade server app.

This server is based on the reference implementation in the
optimade-python-tools package.

"""
import warnings
from pathlib import Path

with warnings.catch_warnings(record=False) as _:
    from necroptimade.config import CONFIG

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from optimade.server.routers import (
    index_info,
    links,
    versions,
)

from optimade import __api_version__
from optimade.server.exception_handlers import OPTIMADE_EXCEPTIONS
from optimade.server.middleware import OPTIMADE_MIDDLEWARE
from optimade.server.routers.utils import BASE_URL_PREFIXES

from necroptimade.routers import landing

APP_PREFIX = ""

app = FastAPI(
    root_path=CONFIG.root_path,
    version=__api_version__,
    docs_url=f"{BASE_URL_PREFIXES['major']}/extensions/docs",
    redoc_url=f"{BASE_URL_PREFIXES['major']}/extensions/redoc",
    openapi_url=f"{BASE_URL_PREFIXES['major']}/extensions/openapi.json",
)

# Add CORS middleware first
app.add_middleware(CORSMiddleware, allow_origins=["*"])

# Then add required OPTIMADE middleware
for middleware in OPTIMADE_MIDDLEWARE:
    app.add_middleware(middleware)

# Add exception handlers
for exception, handler in OPTIMADE_EXCEPTIONS:
    app.add_exception_handler(exception, handler)

# Add various endpoints to unversioned URL
for endpoint in (index_info, links, landing, versions):
    app.include_router(endpoint.router, prefix=APP_PREFIX)

# Mount some static files for testing
STATIC_DIR = Path(__file__).parent.joinpath("static")
app.mount(
    "/static",
    StaticFiles(directory=STATIC_DIR),
    name="static",
)

# Add the spawn endpoint
from necroptimade.routers import spawn_router

app.include_router(spawn_router, prefix=APP_PREFIX + "/extensions")


def add_major_version_base_url(app: FastAPI):
    """Add mandatory vMajor endpoints, i.e. all except versions."""
    for endpoint in (index_info, links, landing):
        app.include_router(
            endpoint.router, prefix=APP_PREFIX + BASE_URL_PREFIXES["major"]
        )


def add_optional_versioned_base_urls(app: FastAPI):
    """Add the following OPTIONAL prefixes/base URLs to server:
    ```
        /vMajor.Minor
        /vMajor.Minor.Patch
    ```
    """
    for version in ("minor", "patch"):
        for endpoint in (index_info, links, landing):
            app.include_router(
                endpoint.router, prefix=APP_PREFIX + BASE_URL_PREFIXES[version]
            )


@app.on_event("startup")
async def startup_event():
    # Add API endpoints for MANDATORY base URL `/vMAJOR`
    add_major_version_base_url(app)
    # Add API endpoints for OPTIONAL base URLs `/vMAJOR.MINOR` and `/vMAJOR.MINOR.PATCH`
    add_optional_versioned_base_urls(app)
