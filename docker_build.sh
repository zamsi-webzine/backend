#!/usr/bin/env bash
docker build -f Dockerfile.local -t lanark/zamsee-local .
docker run --rm -it -p 8000:80 -p 5432:5432 -p 6379:6379 lanark/zamsee-local /bin/zsh