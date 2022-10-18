#!/bin/bash

docker stop pocket-strata 2> /dev/null || true
docker rm -f pocket-strata 2> /dev/null || true
