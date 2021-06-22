#!/bin/bash
set -ex

export PORT=8000
export OPTIMADE_DEBUG=1
export OPTIMADE_LOG_LEVEL=debug

uvicorn necroptimade.app:app --host 0.0.0.0 --port $PORT
