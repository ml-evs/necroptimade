"""This submodule describes the configuration of a remote resource (e.g., a Zenodo repository)
to be ingested by NecrOPTIMADE.

"""

from pathlib import Path
from pydantic import BaseModel, Field, UrlStr


class RemoteConfig(BaseModel):

    endpoint_data: dict[str, Path | list[Path]] = Field(
        ...,
        description="A map from endpoint names (e.g., `structures`) to a file of list of files to ingest."
    )

    description: str | None = Field(
        None,
        description="A human-readable description of the dataset using Markdown/HTML."
    )

    links: UrlStr | list[UrlStr] | None = Field(
        None,
        description=(
            "A URL to a related resource, e.g., a DOI of a paper or a website describing the dataset. "
            "These links will be added to the links endpoint of the NecrOPTIMADE API, and to every resource. "
            "The repository link will automatically be added to this list."
        )
    )