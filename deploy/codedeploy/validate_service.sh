#!/bin/bash

# This just checks if the container is still running, but can be easily replaced by an http call since that'd be a better healthcheck
if [[ "$(docker ps | grep pocket-strata)" ]] ; then
   exit 0
else
   exit 1
fi

