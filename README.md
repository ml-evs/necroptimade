<img width="10%" align="left" src="docs/static/necroptimade_logo_180x180.svg">

# necroptimade

Spawn and revive OPTIMADE APIs from static data, e.g., JSON files on disk, or a Zenodo archive.

Extremely WIP.

## Current functionality

After starting your server (with `run.sh` or otherwise), you will have a valid OPTIMADE index meta-database implementation that does not serve anything.
This server has an extensions endpoint `/extensions/spawn` that can be passed a `loc` of a remote or local resource, e.g. `localhost:8000/extensions/spawn?loc=./necroptimade/static/test_structures.json`.
This will then construct a database and the appropriate routes to serve this data at a URL generated from the passed `loc`, with the URL returned as a links resource in the call to `/spawn`.
In the case of a local file (as above), the base URL of the new OPTIMADE implementation will be e.g. `localhost:8000/<absolute_path_to_file>/`, and for remote resources (e.g. `http://localhost:8000/static/test_structures.json`, which is available by default) it will be `localhost:8000/localhost:8000/static/test_structures.json`, i.e. the original minus the URL scheme is appended to the base URL of the app.
Currently, the location MUST refer to a JSON (well, BSON) file that contains structures in an OPTIMADE format.

The app is deployed to Heroku at https://necroptimade.herokuapp.com, so you can try e.g. https://necroptimade.herokuapp.com/extensions/spawn?loc=./necroptimade/static/test_structures.json and https://necroptimade.herokuapp.com/app/necroptimade/static/test_structures.json/v1/structures.

### Caveats:

- If spawn is called multiple times, only the most recent spawned implementation survives.
- This app currently will not work with multiple workers as mongomock is being used as a per-process database

### To-do

- [ ] Allow multiple implementations to be served simultaneously, with an additional persistent database of implementations
    - [ ] Active implementations can then be served by the index-meta database directly.
    - [ ] Add a timeout for implementations (e.g. last request time + 10 minutes)
    - [ ] Cache to disk after timeout, then re-up if the implementation is requested?
    - [ ] Accept Keep-Alive requests to enable clients to work with necroptimade more easily
- [ ] Lay out a scheme for providing non-structure and archived data (e.g. a folder hierarchy corresponding to the endpoint data).
- [ ] Go beyond mongomock and enable persistence
- [ ] Allow for optimade-python-tools config files to be provided to enable aliasing etc.
- [ ] Add some automatic indexes to the data
- [ ] Add data validation on ingestion, not just on response
