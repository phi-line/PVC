#!/bin/bash
# update conda .venv
conda env update --prefix ./.venv --file environment.yml  --prune
