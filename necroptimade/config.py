from optimade.server.config import CONFIG
from optimade.models import Provider, Implementation
from necroptimade import __version__

__all__ = ("CONFIG",)

CONFIG.implementation = Implementation(
    **{
        "name": "NecrOPTIMADE",
        "source_url": "https://github.com/ml-evs/necroptimade",
        "maintainer": {"email": "git@ml-evs.science"},
        "version": __version__,
    }
)

CONFIG.provider = Provider(
    **{
        "name": "NecrOPTIMADE",
        "description": "The NecrOPTIMADE provider for reviving static data",
        "prefix": "necro",
        "homepage": "https://necroptimade.herokuapp.com",
    }
)
