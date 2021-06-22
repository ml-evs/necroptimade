from typing import Union
from urllib.parse import urlparse
import requests
import bson.json_util as json
from fastapi import APIRouter, Depends, Request

from optimade.server.entry_collections import create_collection
from optimade.server.mappers import StructureMapper
from optimade.models import (
    StructureResource,
    StructureResponseMany,
    ErrorResponse,
    LinksResponse,
    LinksResource,
)
from optimade.server.routers.utils import get_entries

from necroptimade.app import app as APP


def spawn_optimade_app(request, params) -> LinksResponse:

    url = getattr(params, "url", None)
    if not url:
        url = "http://127.0.0.1:8000/static/test_structures.json"

    parsed_url = urlparse(url)
    app_prefix = parsed_url.netloc + parsed_url.path

    data = requests.get(url, timeout=5)

    if data.headers.get("content-type") == "application/json":
        test_data = json.loads(data.content)
        for doc in test_data:
            doc["immutable_id"] = str(doc["immutable_id"])

    new_collection = create_collection(
        name=url + "_structures",
        resource_cls=StructureResource,
        resource_mapper=StructureMapper,
    )

    new_collection.insert(test_data)

    router = APIRouter()

    @router.get(
        "/structures",
        response_model=Union[StructureResponseMany, ErrorResponse],
        response_model_exclude_unset=True,
        tags=["Structures"],
    )
    def get_structures(request: Request, params=Depends()):
        return get_entries(
            collection=new_collection,
            response=StructureResponseMany,
            request=request,
            params=params,
        )

    APP.include_router(router, prefix=app_prefix)

    link = LinksResource(
        name="NecrOPTIMADE instance",
        base_url=APP.base_url + app_prefix,
        link_type="child",
        aggregate="ephemeral",
        no_aggregate_reason="This is an emphemeral NecrOPTIMADE instance.",
    )

    return LinksResponse(data=link)
