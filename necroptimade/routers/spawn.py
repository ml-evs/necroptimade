from urllib.parse import urlparse
import requests
import bson.json_util as json

from optimade.server.routers.utils import get_base_url
from optimade.server.routers import info, links, structures, references
from optimade.models import (
    LinksResponse,
    LinksResource,
    ResponseMeta,
)
from optimade.server.routers.utils import BASE_URL_PREFIXES
from optimade.server.routers import versions
from necroptimade.app import app as APP


def spawn_optimade_app(request, params) -> LinksResponse:

    url = getattr(params, "url", None)
    if not url:
        url = "http://127.0.0.1:8000/static/test_structures.json"

    parsed_url = urlparse(url)
    app_prefix = "/" + parsed_url.netloc + parsed_url.path

    data = requests.get(url, timeout=5)

    if data.headers.get("content-type") == "application/json":
        test_data = json.loads(data.content)
        for doc in test_data:
            doc["immutable_id"] = str(doc["immutable_id"])

    for router in (info.router, links.router, structures.router, references.router):
        for version in ("major", "minor", "patch"):
            APP.include_router(router, prefix=app_prefix + BASE_URL_PREFIXES[version])
        APP.include_router(router, prefix=app_prefix)
        APP.include_router(versions.router, prefix=app_prefix)

    link = LinksResource(
        id=app_prefix,
        attributes=dict(
            name="NecrOPTIMADE instance",
            base_url=get_base_url(request.url) + app_prefix,
            link_type="child",
            homepage="https://necroptimade.herokuapp.com",
            description=f"A NecrOPTIMADE instance created from {url!r}.",
            aggregate="no",
            no_aggregate_reason="This is an emphemeral NecrOPTIMADE instance.",
        ),
    )

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
