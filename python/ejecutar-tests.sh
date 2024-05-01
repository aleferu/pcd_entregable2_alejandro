#!/usr/bin/env bash

set -xe

if command -v pytest &> /dev/null; then
    pytest -v .
elif command -v python3 &> /dev/null; then
    python3 -m pytest -v .
elif command -v python &> /dev/null; then
    python -m pytest -v .
else
    echo "No se ha podido encontrar un intérprete Python."
fi
