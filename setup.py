from pathlib import Path
import re
from setuptools import setup, find_packages

module_dir = Path(__file__).resolve().parent

with open(module_dir.joinpath("necroptimade/__init__.py")) as version_file:
    for line in version_file:
        match = re.match(r'__version__ = "(.*)"', line)
        if match is not None:
            VERSION = match.group(1)
            break
    else:
        raise RuntimeError(
            f"Could not determine package version from {version_file.name} !"
        )

docs_deps = [
    "mkdocs~=1.1",
    "mkdocs-awesome-pages-plugin~=2.5",
    "mkdocs-material~=7.1",
    "mkdocs-minify-plugin~=0.4.0",
    "mkdocstrings~=0.15.0",
]
testing_deps = [
    "pytest~=6.2",
    "pytest-cov~=2.11",
    "codecov~=2.1",
]
dev_deps = (
    ["pylint~=2.8", "pre-commit~=2.11", "invoke~=1.5"]
    + docs_deps
    + testing_deps
)

setup(
    name="necroptimade",
    version=VERSION,
    url="https://github.com/ml-evs/necroptimade",
    license="MIT",
    author="Matthew Evans",
    author_email="necroptimade@ml-evs.science",
    description="Dynamic and ephemeral OPTIMADE instances",
    long_description=open(module_dir.joinpath("README.md")).read(),
    long_description_content_type="text/markdown",
    keywords="optimade jsonapi materials",
    include_package_data=True,
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.9",
        "Topic :: Database",
        "Topic :: Database :: Database Engines/Servers",
        "Topic :: Database :: Front-Ends",
    ],
    python_requires=">=3.9",
    install_requires=[
        "optimade~=0.14",
        "uvicorn",
        "aiofiles"
    ],
    extras_require={
        "dev": dev_deps,
        "docs": docs_deps,
        "testing": testing_deps,
    },
)
