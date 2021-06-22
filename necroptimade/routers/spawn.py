from urllib.parse import urlparse
from pathlib import Path
import requests
import bson.json_util as json

from optimade.server.routers.utils import get_base_url
from optimade.server.routers import info, links, structures, references
from optimade.models import (
    LinksResponse,
    LinksResource,
    LinksResourceAttributes,
    ResponseMeta,
)
from optimade.server.routers.utils import BASE_URL_PREFIXES
from optimade.server.routers import versions
from necroptimade.app import app as APP

ACTIVE = set()


def spawn_optimade_app(request, params) -> LinksResponse:
    """Creates a new OPTIMADE API based on the data
    found at the passed location. If the API already
    exists at that base URL, do not do anything.

    Parameters:
        request: The request that triggered the spawn.
        params: The query parameters.

    Returns:
        A JSON:API links response pointing to the base URL
            of the new OPTIMADE API.

    """

    loc = getattr(params, "loc", None)
    if not loc:
        loc = "http://127.0.0.1:8000/static/test_structures.json"

    try:
        parsed_url = urlparse(loc)
        if not parsed_url.scheme:
            raise RuntimeError
        app_prefix = "/" + parsed_url.netloc + parsed_url.path
        description = f"A NecrOPTIMADE instance created from remote resource {loc!r}."
    except Exception:
        parsed_url = Path(loc).resolve()
        app_prefix = str(parsed_url)
        description = f"A NecrOPTIMADE instance created from local file {loc!r}."

    if app_prefix not in ACTIVE:
        ingest_data(loc)
        create_routes(app_prefix)
        ACTIVE.add(app_prefix)

    link_attributes = LinksResourceAttributes(
        name="NecrOPTIMADE instance",
        base_url=get_base_url(request.url) + app_prefix,
        link_type="child",
        homepage="https://necroptimade.herokuapp.com",
        description=description,
        aggregate="no",
        no_aggregate_reason="This is an emphemeral NecrOPTIMADE instance.",
    )

    link = LinksResource(
        id=app_prefix.strip("/"), type="links", attributes=link_attributes
    )

    # Insert child link into index meta-db
    link_attributes.id = link.id
    link_attributes.type = link.type
    links.links_coll.collection.insert_one(json.loads(link_attributes.json()))

    return LinksResponse(
        data=[link],
        meta=ResponseMeta(
            more_data_available=False,
            api_version="1.0.0",
            query={"representation": str(request.url)},
            data_returned=1,
            data_available=1,
        ),
    )


def create_routes(app_prefix: str) -> None:
    """Add info and entry endpoints for the given app prefix.

    Parameters:
        app_prefix: The prefix of the new OPTIMADE API.

    """
    for router in (info.router, links.router, structures.router, references.router):
        for version in ("major", "minor", "patch"):
            APP.include_router(router, prefix=app_prefix + BASE_URL_PREFIXES[version])
        APP.include_router(router, prefix=app_prefix)
        APP.include_router(versions.router, prefix=app_prefix)


def ingest_data(loc: str) -> None:
    """Attempt to ingest the data at the passed loc
    as data to serve with an OPTIMADE API. Currently,
    this function only deals with structure data, and will
    drop any existing structure data when starting a new
    ingestion.

    Parameters:
        loc: A string representing either a URL or a path to a local file.

    """

    structures.structures_coll.collection.drop()

    try:
        data = requests.get(loc, timeout=5)
        if data.headers.get("content-type") == "application/json":
            data = json.loads(data.content)
    except Exception:
        loc = Path(loc)
        if loc.exists():
            with open(loc, "r") as f:
                data = json.loads("".join(f.readlines()))
        else:
            raise RuntimeError(f"Unable to find file {loc.resolve()}")

    for doc in data:
        doc["immutable_id"] = str(doc["immutable_id"])

    structures.structures_coll.insert(data)
