from fastapi import APIRouter, Depends, Request

from necroptimade.routers.spawn import spawn_optimade_app

spawn_router = APIRouter()


@spawn_router.get(
    "/spawn",
)
def spawn_optimade_endpoint(request: Request, params=Depends()):
    return spawn_optimade_app(request=request, params=params)
