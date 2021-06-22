from fastapi import APIRouter, Depends, Request, Query


class QueryParams:
    def __init__(
        self, *, loc: str = Query("", description="The location of the data to serve.")
    ):
        self.loc = loc


spawn_router = APIRouter()


@spawn_router.get(
    "/spawn",
)
def spawn_optimade_endpoint(request: Request, params: QueryParams = Depends()):
    from necroptimade.routers.spawn import spawn_optimade_app

    return spawn_optimade_app(request=request, params=params)
